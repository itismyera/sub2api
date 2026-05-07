package admin

import (
	"crypto/sha256"
	"encoding/hex"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"regexp"
	"strings"
	"time"

	"github.com/Wei-Shaw/sub2api/internal/pkg/response"
	"github.com/gin-gonic/gin"
)

const maxSitePageAssetBytes = 10 << 20

var (
	markdownImagePattern = regexp.MustCompile(`!\[([^\]]*)\]\((https?://[^)\s]+)(?:\s+"[^"]*")?\)`)
	htmlImagePattern     = regexp.MustCompile(`(?i)<img\b([^>]*?)\bsrc=["'](https?://[^"']+)["']([^>]*)>`)
)

type ImportSitePageAssetsRequest struct {
	Slug    string `json:"slug"`
	Content string `json:"content"`
}

type ImportSitePageAssetsResponse struct {
	Content string   `json:"content"`
	Assets  []string `json:"assets"`
}

// ImportSitePageAssets downloads remote images referenced by a public page into
// data/public/site-assets, then rewrites the content to local URLs.
func (h *SettingHandler) ImportSitePageAssets(c *gin.Context) {
	var req ImportSitePageAssetsRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		response.BadRequest(c, "Invalid request: "+err.Error())
		return
	}

	content, assets, err := importSitePageAssets(c.Request.Context().Done(), req.Slug, req.Content)
	if err != nil {
		response.BadRequest(c, err.Error())
		return
	}

	response.Success(c, ImportSitePageAssetsResponse{
		Content: content,
		Assets:  assets,
	})
}

func importSitePageAssets(done <-chan struct{}, slug string, content string) (string, []string, error) {
	safeSlug := safeAssetSegment(slug)
	if safeSlug == "" {
		safeSlug = "page"
	}
	dir := filepath.Join("data", "public", "site-assets", safeSlug)
	client := &http.Client{Timeout: 15 * time.Second}
	assets := make([]string, 0)
	seen := make(map[string]string)

	download := func(rawURL string) (string, error) {
		if local, ok := seen[rawURL]; ok {
			return local, nil
		}
		select {
		case <-done:
			return "", fmt.Errorf("request cancelled")
		default:
		}
		local, err := downloadSitePageAsset(client, dir, safeSlug, rawURL)
		if err != nil {
			return "", err
		}
		seen[rawURL] = local
		assets = append(assets, local)
		return local, nil
	}

	var firstErr error
	content = markdownImagePattern.ReplaceAllStringFunc(content, func(match string) string {
		if firstErr != nil {
			return match
		}
		parts := markdownImagePattern.FindStringSubmatch(match)
		if len(parts) != 3 {
			return match
		}
		local, err := download(parts[2])
		if err != nil {
			firstErr = err
			return match
		}
		return fmt.Sprintf("![%s](%s)", parts[1], local)
	})
	if firstErr != nil {
		return "", nil, firstErr
	}

	content = htmlImagePattern.ReplaceAllStringFunc(content, func(match string) string {
		if firstErr != nil {
			return match
		}
		parts := htmlImagePattern.FindStringSubmatch(match)
		if len(parts) != 4 {
			return match
		}
		local, err := download(parts[2])
		if err != nil {
			firstErr = err
			return match
		}
		return fmt.Sprintf(`<img%s src="%s"%s>`, parts[1], local, parts[3])
	})
	if firstErr != nil {
		return "", nil, firstErr
	}

	return content, assets, nil
}

func downloadSitePageAsset(client *http.Client, dir string, slug string, rawURL string) (string, error) {
	parsed, err := url.Parse(rawURL)
	if err != nil || (parsed.Scheme != "http" && parsed.Scheme != "https") {
		return "", fmt.Errorf("invalid image URL: %s", rawURL)
	}

	resp, err := client.Get(rawURL)
	if err != nil {
		return "", fmt.Errorf("download image %s: %w", rawURL, err)
	}
	defer func() { _ = resp.Body.Close() }()
	if resp.StatusCode < 200 || resp.StatusCode >= 300 {
		return "", fmt.Errorf("download image %s: HTTP %d", rawURL, resp.StatusCode)
	}
	contentType := strings.ToLower(strings.TrimSpace(resp.Header.Get("Content-Type")))
	if !strings.HasPrefix(contentType, "image/") {
		return "", fmt.Errorf("download image %s: unsupported content type %q", rawURL, contentType)
	}

	limited := io.LimitReader(resp.Body, maxSitePageAssetBytes+1)
	data, err := io.ReadAll(limited)
	if err != nil {
		return "", fmt.Errorf("read image %s: %w", rawURL, err)
	}
	if len(data) > maxSitePageAssetBytes {
		return "", fmt.Errorf("image %s exceeds %d MB", rawURL, maxSitePageAssetBytes>>20)
	}

	sum := sha256.Sum256(data)
	ext := imageExtension(contentType, parsed.Path)
	name := hex.EncodeToString(sum[:])[:16] + ext
	if err := os.MkdirAll(dir, 0o755); err != nil {
		return "", fmt.Errorf("create asset directory: %w", err)
	}
	path := filepath.Join(dir, name)
	if err := os.WriteFile(path, data, 0o644); err != nil {
		return "", fmt.Errorf("write image asset: %w", err)
	}
	return "/site-assets/" + slug + "/" + name, nil
}

func imageExtension(contentType string, rawPath string) string {
	switch {
	case strings.Contains(contentType, "png"):
		return ".png"
	case strings.Contains(contentType, "webp"):
		return ".webp"
	case strings.Contains(contentType, "gif"):
		return ".gif"
	case strings.Contains(contentType, "svg"):
		return ".svg"
	case strings.Contains(contentType, "jpeg"), strings.Contains(contentType, "jpg"):
		return ".jpg"
	}
	ext := strings.ToLower(filepath.Ext(rawPath))
	if ext == ".png" || ext == ".webp" || ext == ".gif" || ext == ".svg" || ext == ".jpg" || ext == ".jpeg" {
		return ext
	}
	return ".img"
}

func safeAssetSegment(value string) string {
	value = strings.ToLower(strings.TrimSpace(value))
	var builder strings.Builder
	for _, r := range value {
		switch {
		case r >= 'a' && r <= 'z':
			builder.WriteRune(r)
		case r >= '0' && r <= '9':
			builder.WriteRune(r)
		case r == '-' || r == '_':
			builder.WriteRune(r)
		case r == '/' || r == ' ' || r == '.':
			builder.WriteRune('-')
		}
	}
	return strings.Trim(builder.String(), "-_")
}
