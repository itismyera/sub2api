<template>
  <div class="public-nav-shell">
    <header class="relative z-20 px-6 py-5">
      <nav class="mx-auto flex max-w-[1216px] items-center justify-between gap-4">
        <router-link to="/home" class="brand-link">
          <span class="brand-mark">
            <img v-if="siteLogo" :src="siteLogo" :alt="siteName" class="h-full w-full object-contain" />
            <span v-else>{{ siteInitial }}</span>
          </span>
          <span>{{ siteName }}</span>
        </router-link>

        <div class="nav-pill">
          <router-link v-for="item in navItems" :key="item.path" :to="item.path">
            {{ item.label }}
          </router-link>
        </div>

        <router-link :to="isAuthenticated ? dashboardPath : '/login'" class="console-button">
          控制台
        </router-link>
      </nav>
    </header>

    <main class="relative z-10 mx-auto max-w-[1216px] px-6 pb-20 pt-10">
      <section class="page-hero">
        <p>{{ page.eyebrow }}</p>
        <h1>{{ page.title }}</h1>
        <small>{{ page.description }}</small>
      </section>

      <section v-if="page.kind === 'features'" class="card-grid">
        <article v-for="feature in features" :key="feature.title" class="glass-card">
          <Icon :name="feature.icon" size="lg" />
          <h2>{{ feature.title }}</h2>
          <p>{{ feature.desc }}</p>
        </article>
      </section>

      <section v-else-if="page.kind === 'pricing'" class="pricing-panel">
        <div class="pricing-notes">
          <span>充值规则：¥1 人民币 = $1 美元额度</span>
          <span>先享 1.43 折，再叠加渠道倍率算最终折扣</span>
        </div>
        <div class="pricing-table-wrap">
          <table class="pricing-table">
            <thead>
              <tr>
                <th>模型</th>
                <th>分组</th>
                <th>官方输入</th>
                <th>官方输出</th>
                <th>人民币折合</th>
                <th>人民币折合</th>
                <th>Dwanshift 输入价</th>
                <th>Dwanshift 输出价</th>
                <th>最终折扣</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in pricingRows" :key="row.model" :class="row.tone">
                <td>{{ row.model }}</td>
                <td>{{ row.group }}</td>
                <td>${{ row.officialInput }}</td>
                <td>${{ row.officialOutput }}</td>
                <td class="strike">¥{{ row.convertedInput }}</td>
                <td class="strike">¥{{ row.convertedOutput }}</td>
                <td class="lumio">CNY ¥{{ row.inputPrice }}</td>
                <td class="lumio">CNY ¥{{ row.outputPrice }}</td>
                <td><span class="discount">{{ row.discount }}</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section v-else-if="page.kind === 'status'" class="status-layout">
        <article v-for="item in statusItems" :key="item.label" class="status-card">
          <Icon :name="item.icon" size="lg" />
          <span>{{ item.label }}</span>
          <strong>{{ item.value }}</strong>
        </article>
        <div class="status-banner">
          <span></span>
          系统全绿运行，API 网关、计费、模型调度与控制台入口保持可用。
        </div>
      </section>

      <section v-else class="embed-panel">
        <iframe :src="page.externalUrl" class="h-full w-full border-0" allowfullscreen></iframe>
        <a :href="page.externalUrl" target="_blank" rel="noopener noreferrer" class="open-link">
          新标签打开
          <Icon name="externalLink" size="sm" />
        </a>
      </section>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAppStore, useAuthStore } from '@/stores'
import Icon from '@/components/icons/Icon.vue'

type PageKind = 'features' | 'pricing' | 'status' | 'external'

const route = useRoute()
const appStore = useAppStore()
const authStore = useAuthStore()

const siteName = computed(() => appStore.cachedPublicSettings?.site_name || appStore.siteName || 'Dwanshift')
const siteLogo = computed(() => appStore.cachedPublicSettings?.site_logo || appStore.siteLogo || '')
const siteInitial = computed(() => siteName.value.trim().charAt(0).toUpperCase() || 'L')
const isAuthenticated = computed(() => authStore.isAuthenticated)
const dashboardPath = computed(() => (authStore.isAdmin ? '/admin/dashboard' : '/dashboard'))

const navItems = [
  { path: '/features', label: '特性' },
  { path: '/pricing', label: '定价' },
  { path: '/status', label: '状态' },
  { path: '/docs', label: '文档' },
  { path: '/terms', label: '服务条款' },
  { path: '/privacy', label: '隐私保护' },
  { path: '/image2', label: 'Image2生图' },
] as const

const externalFallbacks = {
  image2: 'https://dawnshift.xyz/image2',
} as const

const page = computed(() => {
  const key = String(route.params.page || 'features')
  const pages: Record<string, { kind: PageKind; eyebrow: string; title: string; description: string; externalUrl: string }> = {
    features: {
      kind: 'features',
      eyebrow: 'CORE FEATURES',
      title: '重新定义 API 体验',
      description: '从配置、接入、调度到计费，公开主页展示的核心能力在这里独立呈现。',
      externalUrl: '',
    },
    pricing: {
      kind: 'pricing',
      eyebrow: 'MODEL PRICING',
      title: '模型定价',
      description: '以 Dwanshift 公开主页的展示结构展示模型价格、折扣与计价说明。',
      externalUrl: '',
    },
    status: {
      kind: 'status',
      eyebrow: 'SERVICE STATUS',
      title: '运行状态',
      description: '展示公开主页状态区的核心指标与服务可用性说明。',
      externalUrl: '',
    },
    image2: {
      kind: 'external',
      eyebrow: 'IMAGE GENERATION',
      title: 'Image2 生图',
      description: '承载目标站 Image2 生图入口。',
      externalUrl: externalFallbacks.image2,
    },
  }
  return pages[key] || pages.features
})

const features = [
  { icon: 'bolt', title: '5 分钟极速接入', desc: '统一域名与密钥格式，无缝覆盖主流 IDE 与 CLI。' },
  { icon: 'server', title: '极致性价比', desc: '低至官方原价 0.1 折，计价透明无套路。' },
  { icon: 'chartBar', title: '可视化费用分析', desc: '精确到每次调用的日志与消费明细。' },
  { icon: 'terminal', title: '为编码而生', desc: '专注最强编码模型，拒绝滥竽充数。' },
] as const

const statusItems = [
  { icon: 'users', label: '注册开发者', value: '2,000+' },
  { icon: 'chartBar', label: '月调用次数', value: '100万+' },
  { icon: 'clock', label: '平均响应', value: '16.3ms' },
] as const

const pricingRows = [
  { model: 'Claude Opus 4.7', group: 'Claude', officialInput: 5, officialOutput: 25, convertedInput: '35.00', convertedOutput: '175.00', inputPrice: '7.00', outputPrice: '35.00', discount: '2折', tone: 'purple' },
  { model: 'Claude Sonnet 4.6', group: 'Claude', officialInput: 3, officialOutput: 15, convertedInput: '21.00', convertedOutput: '105.00', inputPrice: '4.20', outputPrice: '21.00', discount: '2折', tone: 'purple' },
  { model: 'GPT5.5', group: 'OpenAI', officialInput: 5, officialOutput: 30, convertedInput: '35.00', convertedOutput: '210.00', inputPrice: '1.00', outputPrice: '6.00', discount: '0.29折', tone: 'blue' },
  { model: 'GPT5.4', group: 'OpenAI', officialInput: 2.5, officialOutput: 15, convertedInput: '17.50', convertedOutput: '105.00', inputPrice: '0.50', outputPrice: '3.00', discount: '0.29折', tone: 'blue' },
] as const

</script>

<style scoped>
.public-nav-shell {
  @apply relative min-h-screen overflow-hidden bg-[#020616] text-white;
  font-family: "Aptos Display", "HarmonyOS Sans SC", "Microsoft YaHei", sans-serif;
}

.public-nav-shell::before {
  content: "";
  @apply pointer-events-none absolute inset-0;
  background:
    radial-gradient(circle at 50% 10%, rgba(68, 91, 255, 0.25), transparent 28%),
    radial-gradient(circle at 80% 35%, rgba(124, 58, 237, 0.18), transparent 24%),
    linear-gradient(180deg, #020616 0%, #05091d 100%);
}

.brand-link {
  @apply flex items-center gap-3 text-2xl font-black tracking-[-0.04em] text-white;
}

.brand-mark {
  @apply flex h-11 w-11 items-center justify-center overflow-hidden rounded-2xl bg-gradient-to-br from-blue-500 to-violet-600 text-sm font-black shadow-xl shadow-violet-500/30;
}

.nav-pill {
  @apply hidden items-center gap-1 rounded-full border border-slate-600/70 bg-slate-900/55 px-3 py-2 shadow-2xl shadow-black/20 backdrop-blur-xl lg:flex;
}

.nav-pill a {
  @apply rounded-full px-4 py-2 text-sm font-bold text-slate-300 transition hover:bg-white/10 hover:text-white;
}

.nav-pill a.router-link-active {
  @apply bg-white/10 text-white;
}

.console-button {
  @apply rounded-full bg-gradient-to-r from-blue-500 to-violet-600 px-6 py-3 text-sm font-black text-white shadow-xl shadow-violet-500/30 transition hover:-translate-y-0.5;
}

.page-hero {
  @apply mx-auto max-w-4xl py-16 text-center;
}

.page-hero p {
  @apply text-sm font-black uppercase tracking-[0.32em] text-violet-300;
}

.page-hero h1 {
  @apply mt-5 text-5xl font-black tracking-[-0.06em] md:text-7xl;
}

.page-hero small {
  @apply mx-auto mt-5 block max-w-2xl text-lg leading-8 text-slate-400;
}

.card-grid {
  @apply grid gap-5 md:grid-cols-2 lg:grid-cols-4;
}

.glass-card,
.status-card {
  @apply rounded-[1.75rem] border border-white/10 bg-white/[0.06] p-7 shadow-2xl shadow-black/20 backdrop-blur-xl;
}

.glass-card :deep(svg) {
  @apply mb-5 text-violet-300;
}

.glass-card h2 {
  @apply text-xl font-black;
}

.glass-card p {
  @apply mt-3 leading-7 text-slate-300;
}

.pricing-notes {
  @apply mx-auto mb-6 flex max-w-3xl flex-wrap items-center justify-center gap-2 text-sm;
}

.pricing-notes span {
  @apply rounded-full border border-violet-400/30 bg-violet-500/10 px-3 py-1.5 font-bold text-violet-200;
}

.pricing-table-wrap,
.embed-panel {
  @apply overflow-hidden rounded-3xl border border-white/10 bg-white/[0.06] shadow-2xl shadow-black/20 backdrop-blur-xl;
}

.pricing-table {
  @apply min-w-full divide-y divide-white/10 text-sm;
}

.pricing-table th {
  @apply whitespace-nowrap bg-white/[0.05] px-5 py-4 text-left font-black text-white;
}

.pricing-table td {
  @apply whitespace-nowrap px-5 py-4 text-slate-300;
}

.pricing-table tr.purple {
  @apply bg-violet-500/10;
}

.strike {
  @apply text-emerald-300 line-through decoration-red-400 decoration-2;
}

.lumio {
  @apply font-black text-blue-200;
}

.discount {
  @apply rounded-full bg-gradient-to-r from-blue-500 to-violet-600 px-4 py-2 font-black text-white;
}

.status-layout {
  @apply grid gap-5 md:grid-cols-3;
}

.status-card {
  @apply flex flex-col gap-3;
}

.status-card :deep(svg) {
  @apply text-blue-300;
}

.status-card span {
  @apply text-sm text-slate-400;
}

.status-card strong {
  @apply text-4xl font-black;
}

.status-banner {
  @apply flex items-center gap-3 rounded-[1.75rem] border border-emerald-400/30 bg-emerald-500/10 p-7 text-emerald-100 md:col-span-3;
}

.status-banner span {
  @apply h-3 w-3 rounded-full bg-emerald-400 shadow-lg shadow-emerald-400/50;
}

.embed-panel {
  @apply relative h-[70vh];
}

.open-link {
  @apply absolute bottom-5 right-5 inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-blue-500 to-violet-600 px-5 py-3 text-sm font-black text-white shadow-xl shadow-blue-500/25;
}
</style>
