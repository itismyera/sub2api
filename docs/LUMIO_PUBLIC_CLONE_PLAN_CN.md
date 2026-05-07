# Lumio 公开主页复刻记录

## 当前目标

- 只复刻 `https://api.lumio.games/home` 的公开主页内容。
- 不复刻 `https://api.lumio.games/dashboard`，继续使用本项目现有控制台和管理后台。
- 以最小耦合方式实现：使用本项目现有 Vue、Pinia、Tailwind、Icon、API client，不引入新依赖，不复制目标站构建产物。

## 参考证据

- 目标 HTML/JS/CSS 抓取结果保存在 `.omx/state/web-clone-lumio/`。
- 目标首页主内容来自 `.omx/state/web-clone-lumio/target-HomeView.js`。
- 目标站运行时配置里包含：
  - `site_name: LumioAPI`
  - `site_subtitle: 企业级API服务`
  - `api_base_url: https://api.lumio.games/`
  - `contact_info: QQ 群: 1073671738     Telegram： https://t.me/lumiochat`
  - `doc_url: https://fast-note.zeabur.app/share/373/7hEuSRdssutC6NcIkayNEQ`

## 已实现范围

- 重做 `/home` 默认公开主页，覆盖目标站主要内容块：
  - 顶部导航、站点 Logo、文档入口、控制台入口。
  - 首屏公告、主标题、副标题、CTA、悬浮能力标签。
  - Hero 徽章区和模型提供商展示。
  - 核心能力卡片。
  - Claude、ChatGPT、Gemini 三类 AI 引擎展示。
  - 系统状态指标卡片。
  - 模型定价表。
  - 愿景 CTA。
  - 技术支持和页脚。
- 定价表优先请求 `/pricing/public`，请求失败时使用静态兜底数据，避免接口不可用导致首页空白。
- 支持 `contact_channels` 公开配置；存在配置时展示渠道按钮，不存在时展示 `contact_info` 兜底文本。
- 增加 `site_pages` 类型兼容和 `/doc/:page` 公开承载页，用于文档、服务条款、隐私协议等公开页面入口。
- Image2 生图入口指向 `https://img.lumio.games/`。
- 导航里的文档、服务条款、隐私保护、Image2 生图按目标站行为改为直接打开外部页面，不再 iframe 嵌入，避免页面显示不全。

## 未纳入范围

- 不改 `/dashboard`、登录、注册、用户中心和管理后台。
- 不复制目标站 Logo 的 base64 资源，运行时仍使用本项目 `site_logo` 配置。
- 不复制 fast-note 外部文档正文到本仓库。
- 不新增后台配置入口；`site_pages`、`contact_channels` 目前只是前端兼容运行时公开配置。

## 验证记录

- 已运行 `cd frontend && corepack pnpm build`，`vue-tsc -b` 和 Vite 生产构建通过。
- 已运行 `git diff --check`，无新增 whitespace 错误；仅提示 `.gitignore` 工作区 LF 将被 Git 转为 CRLF。
- 构建输出存在 Vite 既有 chunk-size/dynamic-import 警告，本次未处理，因为与主页内容复刻无直接关系。

## 本地预览

- 本地 Docker Desktop 使用项目 `deploy/docker-compose.dev.yml`。
- 预览地址：`http://127.0.0.1:18080/home`。
- 健康检查地址：`http://127.0.0.1:18080/health`。

## 内置公开页面管理

- 已将文档、服务条款、隐私保护从外部 Fast Note 链接改为 sub2api 内置公开页面。
- 管理入口：`/admin/public-pages`，只有管理员可访问、编辑和发布。
- 数据存储：复用 `settings` 表，新增 `site_pages` JSON 配置，不新增数据库表和迁移。
- 公开访问：`/docs`、`/terms`、`/privacy` 读取已发布的 `site_pages` 内容；未发布时显示“页面未发布”。
- 内容模式：支持 `markdown`、`html`、`link`。`html` 由管理员发布，和既有 `home_content` 一样属于管理员可信内容。
- 保存策略：管理员页面保存前读取当前完整系统设置，只覆盖 `site_pages`，避免调用现有全量设置接口时清空其他配置。

## 后续如果继续追求像素级还原

- 需要进一步对齐目标站的浅色/暗色自适应背景、字体权重、首屏间距、Logo 资产、轨道动画和按钮阴影。
- 建议用浏览器截图 + 像素 diff 进行迭代，每轮只改 1-2 类视觉偏差。
