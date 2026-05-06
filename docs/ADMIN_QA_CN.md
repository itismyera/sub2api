# 管理后台问题记录

本文记录管理后台使用过程中出现的问题、结论和代码依据。截图可以存放在 `docs/assets/admin-qa/`，再用 Markdown 图片语法引用。

## 截图保存方式

Markdown 文档本身通常不直接“存图片”，而是引用仓库里的图片文件。建议目录：

```text
docs/assets/admin-qa/
```

引用示例：

```markdown
![账号管理容量列示例](assets/admin-qa/account-capacity-column.png)
```

当前对话里发送的截图只能在聊天上下文中查看，不能自动作为文件写入仓库。若需要把它长期留在文档里，需要先把截图文件放到 `docs/assets/admin-qa/`，再补上引用。

## 2026-05-06：账号管理里的“容量”是什么意思？

### 问题

在管理后台 `账号管理` 页面里，表格有一列叫 `容量`，截图中显示类似：

```text
0 / 10
```

### 结论

这里的 `容量` 不是磁盘容量，也不是账号余额。截图中的 `0 / 10` 是账号的并发槽位：

- `0` 表示当前这个上游账号正在占用的并发请求数。
- `10` 表示这个账号允许的最大并发数，即账号字段 `concurrency`。
- 当显示为 `10 / 10` 时，表示并发槽位已满，调度层不应继续把新的并发请求分配给该账号。
- 颜色会根据占用情况变化：空闲通常是灰色，有占用时偏黄，满额时偏红。

### 额外说明

`容量` 是一个聚合展示列，不只用于并发。如果账号配置了其他限制，这一列还可能额外显示：

- 5h 窗口费用限制，例如 `$3.20 / $10.00`
- 活跃会话数限制，例如 `2 / 5`
- RPM 限制，例如 `80 / 100 [T]`
- API Key / Bedrock 账号的日、周、总配额，例如 `D $5.00 / $10.00`

本次截图里只出现 `0 / 10`，所以当前看到的是并发容量。

### 代码依据

- 前端页面列定义：`frontend/src/views/admin/AccountsView.vue`
- 容量列组件：`frontend/src/components/account/AccountCapacityCell.vue`
- 容量徽章组件：`frontend/src/components/account/CapacityBadge.vue`
- 配额徽章组件：`frontend/src/components/account/QuotaBadge.vue`

关键逻辑：

```ts
const currentConcurrency = computed(() => props.account.current_concurrency || 0)

<CapacityBadge
  :color-class="concurrencyClass"
  :current="currentConcurrency"
  :max="account.concurrency"
/>
```
