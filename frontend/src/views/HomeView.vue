<template>
  <div v-if="homeContent" class="min-h-screen">
    <iframe
      v-if="isHomeContentUrl"
      :src="homeContent.trim()"
      class="h-screen w-full border-0"
      allowfullscreen
    ></iframe>
    <div v-else v-html="homeContent"></div>
  </div>

  <div v-else class="lumio-shell">
    <div class="hero-orbit" aria-hidden="true"></div>

    <header class="relative z-20 px-6 py-5">
      <nav class="mx-auto flex max-w-[1216px] items-center justify-between gap-4">
        <router-link to="/home" class="brand-link" aria-label="Home">
          <span class="brand-mark">
            <img
              v-if="siteLogo"
              :src="siteLogo"
              :alt="siteName"
              class="h-full w-full object-contain"
            />
            <span v-else>{{ siteInitial }}</span>
          </span>
          <span>{{ siteName }}</span>
        </router-link>

        <div class="nav-pill">
          <router-link to="/features">特性</router-link>
          <router-link to="/pricing">定价</router-link>
          <router-link to="/status">状态</router-link>
          <router-link to="/docs">文档</router-link>
          <router-link to="/terms">服务条款</router-link>
          <router-link to="/privacy">隐私保护</router-link>
          <router-link to="/image2">Image2生图</router-link>
        </div>

        <div class="right-actions">
          <component :is="docLinkComponent" v-bind="docLinkAttrs" class="icon-action" title="文档">
            <Icon name="book" size="md" />
          </component>
          <LocaleSwitcher />
          <button
            @click="toggleTheme"
            class="icon-action"
            :title="isDark ? t('home.switchToLight') : t('home.switchToDark')"
          >
            <Icon v-if="isDark" name="sun" size="md" />
            <Icon v-else name="moon" size="md" />
          </button>
          <router-link :to="isAuthenticated ? dashboardPath : '/login'" class="console-button">
            控制台
          </router-link>
        </div>
      </nav>
    </header>

    <main class="relative z-10">
      <section class="hero-section">
        <div class="floating-chip chip-left-top">
          <Icon name="sparkles" size="sm" />
          多模态全面进化
        </div>
        <div class="floating-chip chip-left-bottom">
          <Icon name="chart" size="sm" />
          更高效的生产力
        </div>
        <div class="floating-chip chip-right-top">
          <Icon name="shield" size="sm" />
          更稳定的对话
        </div>
        <div class="floating-chip chip-right-bottom">
          <Icon name="cpu" size="sm" />
          突破边界 · 超越想象
        </div>

        <div class="release-badge">
          <span></span>
          Claude 4.7 和 GPT-5.5 现已可用
          <strong>全新升级</strong>
        </div>

        <h1>
          <span>极致优雅的</span>
          <strong>AI 接口引擎</strong>
        </h1>

        <p class="hero-subtitle">更智能，更懂你 — Smarter. More capable. Closer to you.</p>
        <p class="hero-copy">
          一行代码，直连全网最顶尖大模型。更稳定的架构，更极简的接入，低至官方 0.1 折的颠覆性定价。
        </p>

        <div class="hero-actions">
          <router-link :to="isAuthenticated ? dashboardPath : '/login'" class="primary-cta">
            获取 API Key
            <Icon name="arrowRight" size="md" :stroke-width="2" />
          </router-link>
          <component :is="docLinkComponent" v-bind="docLinkAttrs" class="secondary-cta">
            <Icon name="terminal" size="sm" />
            查看文档
          </component>
        </div>

        <div class="hero-badges">
          <div v-for="badge in heroBadges" :key="badge.text" class="hero-badge">
            <span><Icon :name="badge.icon" size="sm" /></span>
            {{ badge.text }}
          </div>
        </div>
      </section>

      <section class="content-section compact">
        <div class="model-strip">
          <article v-for="provider in providers" :key="provider.name" class="provider-pill">
            <span :class="provider.tone">{{ provider.initial }}</span>
            <div>
              <strong>{{ provider.name }}</strong>
              <small>{{ provider.status }}</small>
            </div>
          </article>
        </div>
      </section>

      <section id="features" class="content-section">
        <div class="section-heading">
          <p>核心能力</p>
          <h2>重新定义 <span>API 体验</span></h2>
          <small>从配置到调用，每一处细节都为你精心打磨。</small>
        </div>
        <div class="feature-grid">
          <article v-for="feature in features" :key="feature.title" class="feature-card">
            <Icon :name="feature.icon" size="lg" />
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.desc }}</p>
          </article>
        </div>

        <div class="engine-status-grid">
          <div class="engine-panel">
            <div class="panel-head">
              <h3>三大 AI 引擎 · 各司其职</h3>
              <span>动态调度最适合模型</span>
            </div>
            <div class="engine-grid">
              <article v-for="engine in engines" :key="engine.name" class="engine-card">
                <div class="engine-top">
                  <span class="engine-icon">
                    <Icon :name="engine.icon" size="lg" />
                  </span>
                  <small :class="engine.tone">{{ engine.pill }}</small>
                </div>
                <h4>{{ engine.name }}</h4>
                <p>{{ engine.models }}</p>
              </article>
            </div>
          </div>

          <div id="status" class="status-panel">
            <div class="status-badge"><span></span>系统全绿运行</div>
            <div class="status-list">
              <div v-for="item in statusItems" :key="item.label">
                <span>
                  <Icon :name="item.icon" size="sm" />
                  {{ item.label }}
                </span>
                <strong>{{ item.value }}</strong>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="pricing" class="content-section pricing-section">
        <div class="section-heading">
          <h2>模型 <span>定价</span></h2>
          <small>官方原价以美元（USD）标注 · 折合价与 Dwanshift 价格以人民币（CNY）计价 · 单位：百万 tokens</small>
          <div class="pricing-notes">
            <span>充值规则：¥1 人民币 = $1 美元额度</span>
            <span>先享 1.43 折，再叠加渠道倍率算最终折扣</span>
          </div>
        </div>

        <div class="pricing-table-wrap">
          <table class="pricing-table">
            <thead>
              <tr>
                <th>模型</th>
                <th>分组</th>
                <th>官方输入 <small>美元 USD</small></th>
                <th>官方输出 <small>美元 USD</small></th>
                <th>人民币折合 <small>人民币 CNY</small></th>
                <th>人民币折合 <small>人民币 CNY</small></th>
                <th>Dwanshift 输入价 <small>人民币 CNY</small></th>
                <th>Dwanshift 输出价 <small>人民币 CNY</small></th>
                <th>最终折扣 <small>最终折扣</small></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in displayPricingRows" :key="row.model" :class="row.tone">
                <td>{{ row.model }}</td>
                <td>{{ row.group }}</td>
                <td><span class="official-price">${{ row.officialInput }}</span></td>
                <td><span class="official-price">${{ row.officialOutput }}</span></td>
                <td><span class="converted-price">¥{{ row.convertedInput }}</span></td>
                <td><span class="converted-price">¥{{ row.convertedOutput }}</span></td>
                <td><span class="lumio-price">CNY ¥{{ row.inputPrice }}</span></td>
                <td><span class="lumio-price">CNY ¥{{ row.outputPrice }}</span></td>
                <td>
                  <span class="discount-pill">
                    <small>最终折扣</small>
                    <strong>{{ row.discount }}</strong>
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <section id="vision" class="content-section vision-section">
        <div class="vision-card">
          <p>
            “让每一个开发者都能以<span>可接受的价格</span>与<span>稳定的服务</span>，触达世界上最聪明的 AI。”
          </p>
          <small>— Dwanshift</small>
          <router-link :to="isAuthenticated ? dashboardPath : '/login'" class="primary-cta">
            加入我们的愿景
            <Icon name="arrowRight" size="sm" />
          </router-link>
        </div>
      </section>

      <section id="support" class="support-section">
        <div class="support-inner">
          <div>
            <span class="support-icon"><Icon name="chatBubble" size="lg" /></span>
            <h2>技术支持</h2>
            <p>选择任意联系渠道，直接加入 QQ 群、飞书群或 Telegram 群获取支持。</p>
          </div>
          <div v-if="contactChannels.length" class="support-channels">
            <a
              v-for="channel in contactChannels"
              :key="`${channel.label}-${channel.url}`"
              :href="channel.url"
              target="_blank"
              rel="noopener noreferrer"
              class="support-channel group"
            >
              <span>
                <strong>{{ channel.label }}</strong>
                <small>{{ channel.url }}</small>
              </span>
              <Icon name="externalLink" size="sm" />
            </a>
          </div>
          <div v-else class="support-card">
            <small>客服联系方式</small>
            <p>{{ contactInfo || '通过控制台公告或站点联系信息获取支持。' }}</p>
          </div>
        </div>
      </section>
    </main>

    <footer class="relative z-10 border-t border-white/10 px-6 py-8">
      <div class="mx-auto flex max-w-[1216px] flex-col gap-4 text-sm text-slate-400 md:flex-row md:items-center md:justify-between">
        <div class="footer-brand">
          <span class="brand-mark small">
            <img v-if="siteLogo" :src="siteLogo" :alt="siteName" class="h-full w-full object-contain" />
            <span v-else>{{ siteInitial }}</span>
          </span>
          <div>
            <strong>{{ siteName }}</strong>
            <p>企业级API服务</p>
          </div>
        </div>
        <div class="footer-links">
          <component :is="docLinkComponent" v-bind="docLinkAttrs">文档</component>
          <a href="https://github.com/Wei-Shaw/sub2api" target="_blank" rel="noopener noreferrer">GitHub</a>
          <span>© {{ currentYear }} {{ siteName }}.</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { apiClient } from '@/api'
import { useAuthStore, useAppStore } from '@/stores'
import LocaleSwitcher from '@/components/common/LocaleSwitcher.vue'
import Icon from '@/components/icons/Icon.vue'
import type { SitePage } from '@/types'

const { t } = useI18n()
const authStore = useAuthStore()
const appStore = useAppStore()

const siteName = computed(() => appStore.cachedPublicSettings?.site_name || appStore.siteName || 'Dwanshift')
const siteLogo = computed(() => appStore.cachedPublicSettings?.site_logo || appStore.siteLogo || '')
const contactInfo = computed(() => appStore.cachedPublicSettings?.contact_info || appStore.contactInfo || '')
const contactChannels = computed(() =>
  (appStore.cachedPublicSettings?.contact_channels ?? []).filter((channel) => channel.label && channel.url)
)
const docUrl = computed(() => appStore.cachedPublicSettings?.doc_url || appStore.docUrl || '')
const homeContent = computed(() => appStore.cachedPublicSettings?.home_content || '')
const sitePages = computed(() => appStore.cachedPublicSettings?.site_pages ?? [])

const isHomeContentUrl = computed(() => {
  const content = homeContent.value.trim()
  return content.startsWith('http://') || content.startsWith('https://')
})

const enabledSitePages = computed(() =>
  sitePages.value.filter((page): page is SitePage => Boolean(page?.enabled && page.title && page.slug))
)
const docPage = computed(() =>
  enabledSitePages.value.find((page) => page.key === 'docs' || page.title.includes('文档')) ?? null
)
const docLinkComponent = computed(() => (docPage.value ? RouterLink : 'a'))
const docLinkAttrs = computed(() => {
  if (docPage.value) return { to: sitePagePath(docPage.value) }
  return docUrl.value
    ? { href: docUrl.value, target: '_blank', rel: 'noopener noreferrer' }
    : { href: '#features' }
})

const isDark = ref(true)
const isAuthenticated = computed(() => authStore.isAuthenticated)
const dashboardPath = computed(() => (authStore.isAdmin ? '/admin/dashboard' : '/dashboard'))
const currentYear = computed(() => new Date().getFullYear())
const siteInitial = computed(() => siteName.value.trim().charAt(0).toUpperCase() || 'L')
const publicPricingRows = ref<PricingRow[]>([])

type PricingTone = 'purple' | 'green' | 'blue'
type PublicPricingItem = {
  model?: string
  group?: string
  multiplier?: string
  officialInput?: number
  officialOutput?: number
  inputPrice?: number
  outputPrice?: number
  discount?: string
  tone?: PricingTone
}

type PricingRow = {
  model: string
  group: string
  officialInput: number
  officialOutput: number
  convertedInput: string
  convertedOutput: string
  inputPrice: string
  outputPrice: string
  discount: string
  tone: PricingTone
}

const features = [
  { icon: 'bolt', title: '5 分钟极速接入', desc: '统一域名与密钥格式，无缝覆盖主流 IDE 与 CLI。' },
  { icon: 'server', title: '极致性价比', desc: '低至官方原价 0.1 折，计价透明无套路。' },
  { icon: 'chartBar', title: '可视化费用分析', desc: '精确到每次调用的日志与消费明细。' },
  { icon: 'terminal', title: '为编码而生', desc: '专注最强编码模型，拒绝滥竽充数。' },
] as const

const heroBadges = [
  { icon: 'swap', text: 'API 兼容' },
  { icon: 'shield', text: '稳定服务' },
  { icon: 'chart', text: '透明计费' },
  { icon: 'sparkles', text: '多模态模型' },
] as const

const providers = [
  { initial: 'C', name: 'Claude', status: 'Supported', tone: 'orange' },
  { initial: 'G', name: 'GPT', status: 'Supported', tone: 'green' },
  { initial: 'G', name: 'Gemini', status: 'Supported', tone: 'blue' },
  { initial: 'I', name: 'Image2', status: 'New', tone: 'violet' },
] as const

const engines = [
  { icon: 'cpu', pill: '架构规划', name: 'Claude', models: 'Opus 4.7 · Sonnet 4.6 · Haiku 4.5', tone: 'orange' },
  { icon: 'brain', pill: '编码实战', name: 'ChatGPT', models: 'GPT-5.5 · GPT-5.4 · GPT-5.3 Codex', tone: 'green' },
  { icon: 'sparkles', pill: '多模态设计', name: 'Gemini', models: '2.5 Pro · 2.0 Flash', tone: 'blue' },
] as const

const statusItems = [
  { icon: 'users', label: '注册开发者', value: '2,000+' },
  { icon: 'chartBar', label: '月调用次数', value: '100万+' },
  { icon: 'clock', label: '平均响应', value: '16.3ms' },
] as const

const fallbackPricingRows: PricingRow[] = [
  { model: 'Claude Opus 4.7', group: 'Claude', officialInput: 5, officialOutput: 25, convertedInput: '35.00', convertedOutput: '175.00', inputPrice: '7.00', outputPrice: '35.00', discount: '2折', tone: 'purple' },
  { model: 'Claude Sonnet 4.6', group: 'Claude', officialInput: 3, officialOutput: 15, convertedInput: '21.00', convertedOutput: '105.00', inputPrice: '4.20', outputPrice: '21.00', discount: '2折', tone: 'purple' },
  { model: 'GPT5.5', group: 'OpenAI', officialInput: 5, officialOutput: 30, convertedInput: '35.00', convertedOutput: '210.00', inputPrice: '1.00', outputPrice: '6.00', discount: '0.29折', tone: 'blue' },
  { model: 'GPT5.4', group: 'OpenAI', officialInput: 2.5, officialOutput: 15, convertedInput: '17.50', convertedOutput: '105.00', inputPrice: '0.50', outputPrice: '3.00', discount: '0.29折', tone: 'blue' },
] as const

const displayPricingRows = computed(() => publicPricingRows.value.length ? publicPricingRows.value : fallbackPricingRows)

function sitePagePath(page: SitePage): string {
  return `/${page.slug.replace(/^\/+/, '')}`
}

function toggleTheme() {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

async function fetchPublicPricing() {
  try {
    const { data } = await apiClient.get<PublicPricingItem[]>('/pricing/public')
    publicPricingRows.value = data.map(mapPricingRow).filter((row) => row.model)
  } catch (error) {
    console.warn('Failed to load public pricing', error)
  }
}

function mapPricingRow(row: PublicPricingItem): PricingRow {
  const officialInput = Number(row.officialInput) || 0
  const officialOutput = Number(row.officialOutput) || 0
  const inputPrice = Number(row.inputPrice) || 0
  const outputPrice = Number(row.outputPrice) || 0
  return {
    model: row.model || '',
    group: row.group || '',
    officialInput,
    officialOutput,
    convertedInput: formatCny(officialInput * 7),
    convertedOutput: formatCny(officialOutput * 7),
    inputPrice: formatCny(inputPrice),
    outputPrice: formatCny(outputPrice),
    discount: row.discount || formatDiscount(row.multiplier),
    tone: row.tone || inferPricingTone(row),
  }
}

function inferPricingTone(row: PublicPricingItem): PricingTone {
  const value = `${row.model || ''} ${row.group || ''}`.toLowerCase()
  if (value.includes('claude') || value.includes('opus') || value.includes('sonnet')) return 'purple'
  if (value.includes('gemini') || value.includes('google')) return 'green'
  return 'blue'
}

function formatCny(value: number): string {
  return value.toFixed(2)
}

function formatDiscount(multiplier?: string): string {
  const parsed = Number.parseFloat((multiplier || '').replace(/[xX倍倍率\s]/g, ''))
  if (!Number.isFinite(parsed) || parsed <= 0) return ''
  return `${(parsed / 7 * 10).toFixed(parsed < 1 ? 2 : 1).replace(/(\.\d*?[1-9])0+$/, '$1').replace(/\.0$/, '')}折`
}

onMounted(() => {
  isDark.value = true
  document.documentElement.classList.add('dark')
  authStore.checkAuth()
  fetchPublicPricing()
  if (!appStore.publicSettingsLoaded) {
    appStore.fetchPublicSettings()
  }
})
</script>

<style scoped>
.lumio-shell {
  @apply relative min-h-screen overflow-hidden bg-[#020616] text-white;
  font-family: "Aptos Display", "HarmonyOS Sans SC", "Microsoft YaHei", sans-serif;
}

.lumio-shell::before {
  content: "";
  @apply pointer-events-none absolute inset-0;
  background:
    radial-gradient(circle at 50% 58%, rgba(84, 64, 255, 0.22), transparent 26%),
    radial-gradient(circle at 50% 54%, rgba(126, 62, 255, 0.14), transparent 18%),
    linear-gradient(180deg, #020616 0%, #020616 72%, #05091d 100%);
}

.hero-orbit {
  @apply pointer-events-none absolute left-1/2 top-[342px] h-[520px] w-[520px] -translate-x-1/2 rounded-full opacity-70;
  background:
    radial-gradient(circle, transparent 42%, rgba(93, 77, 255, 0.16) 43%, transparent 44%),
    radial-gradient(circle, transparent 56%, rgba(135, 70, 255, 0.22) 57%, transparent 58%),
    radial-gradient(circle, transparent 70%, rgba(56, 118, 255, 0.18) 71%, transparent 72%);
  box-shadow: 0 0 90px rgba(79, 70, 229, 0.25);
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

.right-actions {
  @apply flex items-center gap-3;
}

.icon-action {
  @apply hidden rounded-full p-2 text-slate-300 transition hover:bg-white/10 hover:text-white md:inline-flex;
}

.console-button {
  @apply rounded-full bg-gradient-to-r from-blue-500 to-violet-600 px-6 py-3 text-sm font-black text-white shadow-xl shadow-violet-500/30 transition hover:-translate-y-0.5;
}

.hero-section {
  @apply relative mx-auto min-h-[610px] max-w-[1216px] px-6 pb-8 pt-20 text-center;
}

.release-badge,
.floating-chip {
  @apply inline-flex items-center gap-2 rounded-full border border-slate-600/70 bg-slate-900/70 px-4 py-2 text-sm font-bold text-slate-200 shadow-lg shadow-black/20 backdrop-blur-xl;
}

.release-badge span {
  @apply h-2.5 w-2.5 rounded-full bg-emerald-400 shadow-lg shadow-emerald-400/50;
}

.release-badge strong {
  @apply rounded-full bg-violet-600 px-3 py-1 text-xs text-white;
}

.floating-chip {
  @apply absolute hidden text-slate-300 lg:inline-flex;
}

.floating-chip :deep(svg) {
  @apply text-blue-400;
}

.chip-left-top {
  @apply left-24 top-32;
}

.chip-left-bottom {
  @apply left-16 top-[370px];
}

.chip-right-top {
  @apply right-24 top-36;
}

.chip-right-bottom {
  @apply right-16 top-[385px];
}

.hero-section h1 {
  @apply mx-auto mt-7 max-w-3xl text-[78px] font-black leading-[0.93] tracking-[-0.07em] md:text-[118px];
}

.hero-section h1 span {
  @apply block text-white;
}

.hero-section h1 strong {
  @apply block bg-gradient-to-r from-blue-500 via-indigo-500 to-violet-500 bg-clip-text text-transparent;
}

.hero-subtitle {
  @apply mt-8 text-xl font-semibold text-slate-200;
}

.hero-copy {
  @apply mx-auto mt-5 max-w-3xl text-lg leading-8 text-slate-400;
}

.hero-actions {
  @apply mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row;
}

.hero-badges {
  @apply mt-16 flex flex-wrap items-center justify-center gap-3;
}

.hero-badge {
  @apply flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.06] px-5 py-2.5 text-sm font-bold text-slate-300 shadow-lg shadow-black/10 backdrop-blur-xl transition hover:-translate-y-0.5 hover:bg-white/[0.09];
}

.hero-badge span {
  @apply flex h-6 w-6 items-center justify-center rounded-full border border-white/10 bg-white/[0.08] text-blue-300;
}

.primary-cta,
.secondary-cta {
  @apply inline-flex items-center justify-center gap-2 rounded-full px-8 py-4 text-lg font-black transition;
}

.primary-cta {
  @apply bg-gradient-to-r from-blue-500 to-violet-600 text-white shadow-2xl shadow-blue-500/30 hover:-translate-y-1;
}

.secondary-cta {
  @apply border border-slate-600 bg-slate-900/60 text-slate-100 backdrop-blur-xl hover:-translate-y-1 hover:bg-white/10;
}

.content-section {
  @apply relative z-10 mx-auto max-w-[1216px] px-6 py-20;
}

.content-section.compact {
  @apply py-10;
}

.section-heading {
  @apply mb-8 text-center;
}

.section-heading p,
.eyebrow {
  @apply text-sm font-black uppercase tracking-[0.32em] text-violet-300;
}

.section-heading h2,
.glass-panel h2 {
  @apply mt-3 text-4xl font-black tracking-[-0.04em] text-white;
}

.section-heading h2 span {
  @apply bg-gradient-to-r from-blue-500 via-indigo-500 to-violet-500 bg-clip-text text-transparent;
}

.section-heading small {
  @apply mx-auto mt-4 block max-w-2xl text-base leading-7 text-slate-400;
}

.feature-grid {
  @apply grid gap-5 md:grid-cols-2 lg:grid-cols-4;
}

.feature-card,
.glass-panel {
  @apply rounded-[1.75rem] border border-white/10 bg-white/[0.06] p-7 shadow-2xl shadow-black/20 backdrop-blur-xl;
}

.feature-card :deep(svg) {
  @apply mb-5 text-violet-300;
}

.feature-card h3 {
  @apply text-xl font-black text-white;
}

.feature-card p,
.glass-panel p {
  @apply mt-3 leading-7 text-slate-300;
}

.engine-status-grid {
  @apply mt-8 grid gap-5 lg:grid-cols-5;
}

.engine-panel {
  @apply rounded-[1.75rem] border border-white/10 bg-white/[0.06] p-7 shadow-2xl shadow-black/20 backdrop-blur-xl lg:col-span-3;
}

.panel-head {
  @apply mb-6 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between;
}

.panel-head h3 {
  @apply text-lg font-black tracking-[-0.03em] text-white;
}

.panel-head span {
  @apply text-xs text-slate-400;
}

.engine-grid {
  @apply grid gap-4 md:grid-cols-3;
}

.engine-card {
  @apply rounded-2xl border border-white/10 bg-slate-950/50 p-5 transition hover:-translate-y-1 hover:bg-white/[0.08];
}

.engine-top {
  @apply mb-4 flex items-center justify-between;
}

.engine-icon {
  @apply flex h-10 w-10 items-center justify-center rounded-xl border border-white/10 bg-white/[0.06] text-blue-300;
}

.engine-card small {
  @apply rounded-full px-2 py-1 text-[10px] font-black text-white;
}

.engine-card small.orange {
  @apply bg-orange-500;
}

.engine-card small.green {
  @apply bg-green-500;
}

.engine-card small.blue {
  @apply bg-blue-500;
}

.engine-card h4 {
  @apply text-xl font-black text-white;
}

.engine-card p {
  @apply mt-2 text-sm leading-6 text-slate-400;
}

.status-panel {
  @apply relative overflow-hidden rounded-[1.75rem] border border-white/10 bg-gradient-to-br from-blue-950/50 via-slate-950/70 to-violet-950/50 p-7 shadow-2xl shadow-black/20 lg:col-span-2;
}

.status-badge {
  @apply mb-5 inline-flex items-center gap-2 rounded-full border border-emerald-400/30 bg-emerald-500/10 px-3 py-1 text-xs font-bold text-emerald-200;
}

.status-badge span {
  @apply h-1.5 w-1.5 rounded-full bg-emerald-400;
}

.status-list {
  @apply space-y-3;
}

.status-list div {
  @apply flex items-center justify-between border-b border-white/10 py-3 last:border-0;
}

.status-list span {
  @apply flex items-center gap-2 text-sm text-slate-300;
}

.status-list strong {
  @apply text-2xl font-black text-white;
}

.pricing-section {
  @apply pt-12;
}

.pricing-notes {
  @apply mx-auto mt-5 flex max-w-3xl flex-wrap items-center justify-center gap-2 text-sm;
}

.pricing-notes span {
  @apply rounded-full border border-violet-400/30 bg-violet-500/10 px-3 py-1.5 font-bold text-violet-200;
}

.pricing-notes span:first-child {
  @apply border-emerald-400/30 bg-emerald-500/10 text-emerald-200;
}

.pricing-table-wrap {
  @apply overflow-x-auto rounded-3xl border border-white/10 bg-white/[0.06] shadow-2xl shadow-black/20 backdrop-blur-xl;
}

.pricing-table {
  @apply min-w-full divide-y divide-white/10 text-sm;
}

.pricing-table th {
  @apply whitespace-nowrap bg-white/[0.05] px-5 py-4 text-left font-black text-white;
}

.pricing-table th small {
  @apply mt-1 block rounded-full border border-white/10 px-2 py-0.5 text-[10px] text-slate-400;
}

.pricing-table td {
  @apply whitespace-nowrap px-5 py-4 text-slate-300;
}

.pricing-table tbody tr {
  @apply transition hover:bg-white/[0.04];
}

.pricing-table tbody tr.green {
  @apply bg-emerald-500/10;
}

.pricing-table tbody tr.purple {
  @apply bg-violet-500/10;
}

.official-price {
  @apply inline-flex min-w-[4.75rem] justify-center rounded-md border border-amber-400/30 bg-amber-500/10 px-2.5 py-1 font-bold text-amber-200;
}

.converted-price {
  @apply inline-flex min-w-[4.75rem] justify-center rounded-md border border-emerald-400/20 bg-emerald-500/10 px-2.5 py-1 font-bold text-emerald-300 line-through decoration-red-400 decoration-2;
}

.lumio-price {
  @apply inline-flex min-w-[6.25rem] justify-center rounded-lg border border-blue-400/30 bg-blue-500/10 px-3 py-1.5 font-black text-blue-200;
}

.discount-pill {
  @apply inline-flex min-w-[7rem] flex-col items-center justify-center rounded-full bg-gradient-to-r from-blue-500 via-sky-500 to-violet-600 px-5 py-2 text-white shadow-xl shadow-blue-500/30;
}

.discount-pill small {
  @apply text-[10px] font-bold text-white/80;
}

.discount-pill strong {
  @apply text-xl font-black leading-none;
}

.vision-section {
  @apply py-16;
}

.vision-card {
  @apply relative overflow-hidden rounded-[2rem] border border-white/10 bg-white/[0.06] p-10 text-center shadow-2xl shadow-black/20 backdrop-blur-xl md:p-16;
}

.vision-card p {
  @apply mx-auto max-w-4xl text-2xl font-black leading-snug tracking-[-0.04em] text-white md:text-4xl;
}

.vision-card p span {
  @apply bg-gradient-to-r from-blue-500 to-violet-500 bg-clip-text text-transparent;
}

.vision-card small {
  @apply mt-6 block text-sm text-slate-400;
}

.vision-card .primary-cta {
  @apply mt-10;
}

.support-section {
  @apply relative z-10 border-t border-white/10 bg-slate-950/50 px-6 py-14;
}

.support-inner {
  @apply mx-auto grid max-w-[1216px] gap-8 lg:grid-cols-[0.9fr_1.1fr] lg:items-center;
}

.support-icon {
  @apply mb-4 inline-flex h-11 w-11 items-center justify-center rounded-xl border border-blue-400/30 bg-blue-500/10 text-blue-300;
}

.support-section h2 {
  @apply text-3xl font-black tracking-[-0.04em] text-white md:text-4xl;
}

.support-section p {
  @apply mt-4 max-w-xl text-base leading-7 text-slate-300;
}

.support-card {
  @apply rounded-xl border border-white/10 bg-white/[0.06] px-5 py-4;
}

.support-channels {
  @apply grid min-w-0 gap-3 sm:grid-cols-2;
}

.support-channel {
  @apply flex min-w-0 items-center justify-between gap-3 rounded-xl border border-white/10 bg-white/[0.06] px-5 py-4 text-left transition hover:-translate-y-0.5 hover:bg-white/[0.09];
}

.support-channel span {
  @apply min-w-0;
}

.support-channel strong {
  @apply block text-sm font-black text-white;
}

.support-channel small {
  @apply mt-1 block break-all text-xs leading-5 text-slate-400;
}

.support-channel :deep(svg) {
  @apply shrink-0 text-slate-400 transition group-hover:text-blue-300;
}

.support-card small {
  @apply text-xs font-black uppercase text-slate-400;
}

.support-card p {
  @apply mt-2 whitespace-pre-wrap break-words text-sm font-medium text-slate-200;
  overflow-wrap: anywhere;
}

.footer-brand {
  @apply flex items-center gap-3;
}

.brand-mark.small {
  @apply h-9 w-9 rounded-xl text-xs;
}

.footer-brand strong {
  @apply text-lg font-black text-white;
}

.footer-brand p {
  @apply text-sm text-slate-500;
}

.footer-links {
  @apply flex items-center gap-4;
}

.footer-links a {
  @apply transition hover:text-white;
}

.footer-links :deep(a) {
  @apply transition hover:text-white;
}

.model-strip {
  @apply flex flex-wrap justify-center gap-4;
}

.provider-pill {
  @apply flex items-center gap-3 rounded-2xl border border-white/10 bg-white/[0.06] px-5 py-4 backdrop-blur-xl;
}

.provider-pill span {
  @apply flex h-10 w-10 items-center justify-center rounded-xl text-sm font-black text-white;
}

.provider-pill span.orange {
  @apply bg-gradient-to-br from-orange-400 to-orange-600;
}

.provider-pill span.green {
  @apply bg-gradient-to-br from-emerald-400 to-emerald-600;
}

.provider-pill span.blue {
  @apply bg-gradient-to-br from-blue-400 to-blue-600;
}

.provider-pill span.violet {
  @apply bg-gradient-to-br from-violet-400 to-violet-600;
}

.provider-pill strong {
  @apply text-sm font-black text-white;
}

.provider-pill small {
  @apply rounded-full bg-violet-500/15 px-2 py-1 text-[10px] font-black uppercase tracking-wide text-violet-200;
}

@media (max-width: 768px) {
  .hero-section {
    @apply min-h-[560px] pt-16;
  }

  .hero-section h1 {
    @apply text-[58px];
  }

  .brand-link {
    @apply text-lg;
  }
}
</style>
