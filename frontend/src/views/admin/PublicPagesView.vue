<template>
  <AppLayout>
    <div class="mx-auto max-w-7xl space-y-6">
      <div class="flex flex-col gap-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm dark:border-white/10 dark:bg-slate-900/80 md:flex-row md:items-center md:justify-between">
        <div>
          <p class="text-sm font-black uppercase tracking-[0.24em] text-cyan-600 dark:text-cyan-300">Public Pages</p>
          <h1 class="mt-2 text-3xl font-black tracking-[-0.04em] text-slate-950 dark:text-white">公开页面</h1>
          <p class="mt-2 text-sm text-slate-500 dark:text-slate-400">
            管理首页二级入口页面。只有管理员可以编辑和发布，保存时会把内容中的外链图片导入到站内资源目录。
          </p>
        </div>
        <div class="flex flex-wrap gap-3">
          <button class="btn btn-secondary" :disabled="loading || saving" @click="resetDefaults">
            补齐默认页面
          </button>
          <button class="btn btn-primary" :disabled="loading || saving" @click="savePages">
            {{ saving ? "保存中..." : "保存发布" }}
          </button>
        </div>
      </div>

      <div v-if="loading" class="rounded-3xl border border-slate-200 bg-white p-10 text-center text-slate-500 dark:border-white/10 dark:bg-slate-900 dark:text-slate-400">
        正在加载公开页面配置...
      </div>

      <div v-else class="grid gap-6 lg:grid-cols-[340px_minmax(0,1fr)]">
        <aside class="space-y-3">
          <button
            v-for="(page, index) in pages"
            :key="page.key"
            class="w-full rounded-2xl border p-4 text-left transition"
            :class="index === activeIndex ? 'border-cyan-400 bg-cyan-50 text-cyan-950 dark:border-cyan-400/60 dark:bg-cyan-400/10 dark:text-white' : 'border-slate-200 bg-white text-slate-700 hover:border-cyan-200 dark:border-white/10 dark:bg-slate-900 dark:text-slate-200'"
            @click="activeIndex = index"
          >
            <div class="flex items-center justify-between gap-3">
              <strong class="text-base">{{ page.title || page.key }}</strong>
              <span class="rounded-full px-2 py-1 text-xs font-bold" :class="page.enabled ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-400/15 dark:text-emerald-200' : 'bg-slate-100 text-slate-500 dark:bg-white/10 dark:text-slate-300'">
                {{ page.enabled ? "已发布" : "未发布" }}
              </span>
            </div>
            <p class="mt-2 text-xs text-slate-500 dark:text-slate-400">/{{ page.slug }}</p>
          </button>
          <button class="w-full rounded-2xl border border-dashed border-slate-300 bg-white p-4 text-sm font-bold text-slate-600 hover:border-cyan-300 hover:text-cyan-700 dark:border-white/15 dark:bg-slate-900 dark:text-slate-300" @click="addPage">
            添加页面
          </button>
        </aside>

        <section v-if="activePage" class="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm dark:border-white/10 dark:bg-slate-900">
          <div class="grid gap-4 md:grid-cols-2">
            <label class="form-field">
              <span>页面 Key</span>
              <input v-model.trim="activePage.key" class="input" placeholder="docs" />
            </label>
            <label class="form-field">
              <span>公开路径</span>
              <input v-model.trim="activePage.slug" class="input" placeholder="docs" />
            </label>
            <label class="form-field">
              <span>标题</span>
              <input v-model.trim="activePage.title" class="input" placeholder="文档" />
            </label>
            <label class="form-field">
              <span>内容类型</span>
              <select v-model="activePage.mode" class="input">
                <option value="markdown">Markdown</option>
                <option value="html">HTML</option>
                <option value="link">外部链接</option>
              </select>
            </label>
          </div>

          <div class="mt-5 flex flex-wrap items-center justify-between gap-3">
            <label class="inline-flex items-center gap-2 text-sm font-bold text-slate-700 dark:text-slate-200">
              <input v-model="activePage.enabled" type="checkbox" class="h-4 w-4 rounded border-slate-300 text-cyan-600" />
              发布这个页面
            </label>
            <button class="rounded-full border border-red-200 px-4 py-2 text-sm font-bold text-red-600 hover:bg-red-50 dark:border-red-400/30 dark:text-red-300 dark:hover:bg-red-400/10" @click="removeActivePage">
              删除
            </button>
          </div>

          <label class="form-field mt-5">
            <span>{{ activePage.mode === "link" ? "外部链接" : "页面内容" }}</span>
            <textarea
              v-model="activePage.content"
              class="input min-h-[420px] resize-y font-mono text-sm leading-6"
              :placeholder="activePage.mode === 'link' ? 'https://example.com/docs' : '输入 Markdown 或 HTML 内容'"
            ></textarea>
          </label>

          <div class="mt-4 rounded-2xl bg-slate-50 p-4 text-sm text-slate-500 dark:bg-white/5 dark:text-slate-400">
            公开访问地址：
            <router-link class="font-bold text-cyan-600 dark:text-cyan-300" :to="`/${trimSlash(activePage.slug)}`">/{{ trimSlash(activePage.slug) }}</router-link>
          </div>
        </section>
      </div>
    </div>
  </AppLayout>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import AppLayout from "@/components/layout/AppLayout.vue";
import { adminAPI } from "@/api/admin";
import { useAppStore } from "@/stores/app";
import type { SitePage } from "@/types";
import type { SystemSettings, UpdateSettingsRequest } from "@/api/admin/settings";

const appStore = useAppStore();
const loading = ref(false);
const saving = ref(false);
const pages = ref<SitePage[]>([]);
const settingsSnapshot = ref<SystemSettings | null>(null);
const activeIndex = ref(0);

const defaultPages: SitePage[] = [
  { key: "docs", title: "文档", slug: "docs", mode: "markdown", content: "# 文档\n\n请在管理员后台编辑并发布文档内容。", enabled: true },
  { key: "terms", title: "服务条款", slug: "terms", mode: "markdown", content: "# 服务条款\n\n请在管理员后台编辑并发布服务条款。", enabled: true },
  { key: "privacy", title: "隐私保护", slug: "privacy", mode: "markdown", content: "# 隐私保护\n\n请在管理员后台编辑并发布隐私保护内容。", enabled: true },
];

const activePage = computed(() => pages.value[activeIndex.value] ?? null);

function trimSlash(value: string): string {
  return value.replace(/^\/+|\/+$/g, "");
}

function clonePage(page: SitePage): SitePage {
  return { ...page, slug: trimSlash(page.slug || page.key) };
}

function resetDefaults(): void {
  const existing = new Map(pages.value.map((page) => [page.key, page]));
  for (const page of defaultPages) {
    if (!existing.has(page.key)) {
      pages.value.push(clonePage(page));
    }
  }
  if (pages.value.length > 0 && activeIndex.value >= pages.value.length) {
    activeIndex.value = 0;
  }
}

function addPage(): void {
  const next = pages.value.length + 1;
  pages.value.push({
    key: `page-${next}`,
    title: `公开页面 ${next}`,
    slug: `page-${next}`,
    mode: "markdown",
    content: "# 新页面\n\n在这里编辑内容。",
    enabled: false,
  });
  activeIndex.value = pages.value.length - 1;
}

function removeActivePage(): void {
  if (!activePage.value) return;
  pages.value.splice(activeIndex.value, 1);
  activeIndex.value = Math.max(0, Math.min(activeIndex.value, pages.value.length - 1));
}

function buildFullSettingsPayload(settings: SystemSettings, sitePages: SitePage[]): UpdateSettingsRequest {
  const { openai_fast_policy_settings: _openaiFastPolicySettings, ...payload } = settings;
  return {
    ...payload,
    site_pages: sitePages,
  };
}

async function importPageAssets(page: SitePage): Promise<SitePage> {
  if (page.mode === "link" || !/https?:\/\/[^\s"'<>)]/i.test(page.content)) {
    return page;
  }
  const imported = await adminAPI.settings.importSitePageAssets({
    slug: page.slug || page.key,
    content: page.content,
  });
  return { ...page, content: imported.content };
}

async function loadPages(): Promise<void> {
  loading.value = true;
  try {
    const settings = await adminAPI.settings.getSettings();
    settingsSnapshot.value = settings;
    pages.value = Array.isArray(settings.site_pages) ? settings.site_pages.map(clonePage) : [];
    resetDefaults();
  } finally {
    loading.value = false;
  }
}

async function savePages(): Promise<void> {
  saving.value = true;
  try {
    const normalized = pages.value.map((page) => ({
      ...page,
      key: page.key.trim(),
      title: page.title.trim(),
      slug: trimSlash(page.slug.trim()),
      mode: page.mode,
      content: page.content,
      enabled: page.enabled,
    }));
    const withLocalAssets = [];
    for (const page of normalized) {
      withLocalAssets.push(await importPageAssets(page));
    }
    const baseSettings = settingsSnapshot.value ?? await adminAPI.settings.getSettings();
    const updated = await adminAPI.settings.updateSettings(buildFullSettingsPayload(baseSettings, withLocalAssets));
    settingsSnapshot.value = updated;
    pages.value = Array.isArray(updated.site_pages) ? updated.site_pages.map(clonePage) : withLocalAssets;
    appStore.clearPublicSettingsCache();
    await appStore.fetchPublicSettings(true);
  } finally {
    saving.value = false;
  }
}

onMounted(() => {
  loadPages();
});
</script>

<style scoped>
.form-field {
  @apply flex flex-col gap-2 text-sm font-bold text-slate-700 dark:text-slate-200;
}

.input {
  @apply rounded-2xl border border-slate-200 bg-white px-4 py-3 text-slate-950 outline-none transition focus:border-cyan-400 focus:ring-4 focus:ring-cyan-100 dark:border-white/10 dark:bg-slate-950 dark:text-white dark:focus:ring-cyan-400/10;
}
</style>
