<template>
  <div class="public-page-shell">
    <header class="border-b border-slate-200/70 bg-white/85 px-5 py-4 backdrop-blur dark:border-white/10 dark:bg-slate-950/85">
      <nav class="mx-auto flex max-w-7xl items-center justify-between gap-4">
        <router-link to="/home" class="flex items-center gap-3 text-sm font-black text-slate-950 dark:text-white">
          <span class="flex h-9 w-9 items-center justify-center overflow-hidden rounded-xl bg-slate-950 text-white dark:bg-white dark:text-slate-950">
            <img v-if="siteLogo" :src="siteLogo" :alt="siteName" class="h-full w-full object-contain" />
            <span v-else>{{ siteInitial }}</span>
          </span>
          {{ siteName }}
        </router-link>

        <div class="flex items-center gap-3">
          <a
            v-if="externalUrl"
            :href="externalUrl"
            target="_blank"
            rel="noopener noreferrer"
            class="rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-bold text-slate-700 shadow-sm transition hover:bg-slate-50 dark:border-white/10 dark:bg-white/10 dark:text-white dark:hover:bg-white/15"
          >
            新标签打开
          </a>
          <router-link :to="isAuthenticated ? dashboardPath : '/login'" class="rounded-full bg-cyan-500 px-4 py-2 text-sm font-black text-white shadow-lg shadow-cyan-500/20">
            {{ isAuthenticated ? "进入控制台" : "登录" }}
          </router-link>
        </div>
      </nav>
    </header>

    <main class="mx-auto flex min-h-[calc(100vh-73px)] max-w-5xl flex-col px-5 py-8">
      <div class="mb-5">
        <p class="text-sm font-black uppercase tracking-[0.28em] text-cyan-500">PUBLIC PAGE</p>
        <h1 class="mt-2 text-3xl font-black tracking-[-0.04em] text-slate-950 dark:text-white">
          {{ pageTitle }}
        </h1>
      </div>

      <section v-if="loading" class="state-card">
        <div class="h-8 w-8 animate-spin rounded-full border-2 border-cyan-500 border-t-transparent"></div>
      </section>

      <section v-else-if="!sitePage" class="state-card">
        <Icon name="document" size="xl" class="text-slate-400" />
        <h2>页面未发布</h2>
        <p>当前公开设置中没有找到这个页面，或者页面尚未启用。</p>
        <router-link to="/home" class="btn btn-primary mt-4">返回首页</router-link>
      </section>

      <section v-else-if="externalUrl" class="state-card">
        <Icon name="externalLink" size="xl" class="text-cyan-500" />
        <h2>{{ sitePage.title }}</h2>
        <p>这个页面配置为外部链接。</p>
        <a :href="externalUrl" target="_blank" rel="noopener noreferrer" class="btn btn-primary mt-4">打开页面</a>
      </section>

      <article v-else-if="sitePage.mode === 'html'" class="content-card public-html" v-html="sanitizedHtml"></article>
      <article v-else class="content-card public-markdown" v-html="renderedMarkdown"></article>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { marked } from "marked";
import DOMPurify from "dompurify";
import { useAppStore, useAuthStore } from "@/stores";
import Icon from "@/components/icons/Icon.vue";

marked.setOptions({
  breaks: true,
  gfm: true,
});

const route = useRoute();
const appStore = useAppStore();
const authStore = useAuthStore();
const loading = ref(false);

const siteName = computed(() => appStore.cachedPublicSettings?.site_name || appStore.siteName || "Dwanshift");
const siteLogo = computed(() => appStore.cachedPublicSettings?.site_logo || appStore.siteLogo || "");
const siteInitial = computed(() => siteName.value.trim().charAt(0).toUpperCase() || "S");
const isAuthenticated = computed(() => authStore.isAuthenticated);
const dashboardPath = computed(() => (authStore.isAdmin ? "/admin/dashboard" : "/dashboard"));
const requestedSlug = computed(() => trimSlash(String(route.params.slug || route.params.page || "")));

const sitePage = computed(() => {
  const pages = appStore.cachedPublicSettings?.site_pages ?? [];
  return pages.find((page) => page.enabled && trimSlash(page.slug) === requestedSlug.value) ?? null;
});

const pageTitle = computed(() => sitePage.value?.title || "公开页面");
const externalUrl = computed(() => {
  if (sitePage.value?.mode !== "link") return "";
  const content = sitePage.value.content.trim();
  return content.startsWith("http://") || content.startsWith("https://") ? content : "";
});
const sanitizedHtml = computed(() => sanitizeContent(sitePage.value?.content || ""));
const renderedMarkdown = computed(() => renderMarkdown(sitePage.value?.content || ""));

function trimSlash(value: string): string {
  return value.replace(/^\/+|\/+$/g, "");
}

function renderMarkdown(markdown: string): string {
  if (!markdown) return "";
  const html = marked.parse(markdown) as string;
  return sanitizeContent(html);
}

function sanitizeContent(html: string): string {
  return DOMPurify.sanitize(html, {
    ADD_ATTR: ["target", "rel", "width", "height", "loading"],
    ADD_TAGS: ["iframe"],
  });
}

onMounted(async () => {
  authStore.checkAuth();
  if (appStore.publicSettingsLoaded) return;
  loading.value = true;
  try {
    await appStore.fetchPublicSettings();
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.public-page-shell {
  @apply min-h-screen bg-gradient-to-b from-slate-50 via-white to-cyan-50/40 text-slate-950 dark:from-slate-950 dark:via-slate-950 dark:to-cyan-950/20 dark:text-white;
}

.state-card,
.content-card {
  @apply flex flex-1 flex-col rounded-[1.75rem] border border-slate-200 bg-white p-6 shadow-sm dark:border-white/10 dark:bg-white/5 md:p-9;
  min-height: 60vh;
}

.state-card {
  @apply items-center justify-center text-center;
}

.state-card h2 {
  @apply mt-4 text-xl font-black text-slate-950 dark:text-white;
}

.state-card p {
  @apply mt-2 max-w-md text-sm leading-6 text-slate-500 dark:text-slate-400;
}

.content-card {
  @apply overflow-hidden text-left text-slate-700 dark:text-slate-200;
}

.public-markdown,
.public-html {
  font-size: 16px;
  line-height: 1.85;
}

.public-markdown :deep(h1),
.public-html :deep(h1) {
  @apply mb-6 text-4xl font-black tracking-[-0.05em] text-slate-950 dark:text-white;
}

.public-markdown :deep(h2),
.public-html :deep(h2) {
  @apply mb-4 mt-10 border-b border-slate-200 pb-3 text-2xl font-black tracking-[-0.03em] text-slate-950 dark:border-white/10 dark:text-white;
}

.public-markdown :deep(h3),
.public-html :deep(h3) {
  @apply mb-3 mt-7 text-xl font-black text-slate-950 dark:text-white;
}

.public-markdown :deep(p),
.public-html :deep(p) {
  @apply mb-5 text-base leading-8;
}

.public-markdown :deep(ul),
.public-html :deep(ul) {
  @apply mb-5 list-disc space-y-2 pl-6;
}

.public-markdown :deep(ol),
.public-html :deep(ol) {
  @apply mb-5 list-decimal space-y-2 pl-6;
}

.public-markdown :deep(li),
.public-html :deep(li) {
  @apply pl-1 leading-8;
}

.public-markdown :deep(blockquote),
.public-html :deep(blockquote) {
  @apply mb-6 rounded-2xl border-l-4 border-cyan-400 bg-cyan-50 px-5 py-4 leading-8 text-cyan-950 dark:bg-cyan-400/10 dark:text-cyan-100;
}

.public-markdown :deep(table),
.public-html :deep(table) {
  @apply mb-7 block w-full overflow-x-auto rounded-2xl border border-slate-200 text-sm dark:border-white/10;
  border-collapse: separate;
  border-spacing: 0;
}

.public-markdown :deep(th),
.public-html :deep(th) {
  @apply whitespace-nowrap bg-slate-100 px-4 py-3 text-left font-black text-slate-950 dark:bg-white/10 dark:text-white;
}

.public-markdown :deep(td),
.public-html :deep(td) {
  @apply border-t border-slate-200 px-4 py-3 align-top dark:border-white/10;
}

.public-markdown :deep(pre),
.public-html :deep(pre) {
  @apply mb-7 overflow-x-auto rounded-2xl bg-slate-950 p-5 text-sm leading-7 text-slate-100 shadow-inner;
}

.public-markdown :deep(pre code),
.public-html :deep(pre code) {
  @apply bg-transparent p-0 text-slate-100;
}

.public-markdown :deep(img),
.public-html :deep(img) {
  @apply mx-auto my-7 max-w-full rounded-2xl border border-slate-200 bg-white shadow-xl dark:border-white/10 dark:bg-slate-900;
}

.public-markdown :deep(hr),
.public-html :deep(hr) {
  @apply my-10 border-slate-200 dark:border-white/10;
}

.public-markdown :deep(a),
.public-html :deep(a) {
  @apply font-bold text-cyan-600 underline decoration-cyan-300 underline-offset-4 transition hover:text-cyan-700 dark:text-cyan-300;
}

.public-markdown :deep(code),
.public-html :deep(code) {
  @apply rounded bg-slate-100 px-1.5 py-0.5 text-sm text-slate-900 dark:bg-white/10 dark:text-white;
}
</style>
