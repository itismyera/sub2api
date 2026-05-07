import base64
import subprocess
from pathlib import Path


def b64(value: str) -> str:
    return base64.b64encode(value.encode("utf-8")).decode("ascii")


terms = """# 服务条款

欢迎使用 Dwanshift。Dwanshift 是面向开发者和团队的 AI 接口中转与额度管理服务，提供统一请求地址、密钥管理、用量统计、计费结算和基础运维支持。你注册、登录、充值、创建 API Key、调用接口或继续访问本服务，即表示你已经阅读、理解并同意本条款。

> **统一请求地址**：`https://dawnshift.xyz`

## 1. 服务内容

Dwanshift 提供 AI 模型接口聚合、请求转发、账号分组、额度管理、账单统计和相关控制台功能。平台不拥有第三方模型、SDK、CLI 或上游服务的知识产权，也不对第三方服务的永久可用性作绝对承诺。

平台可能根据上游供应商策略、网络质量、成本变化、合规要求或安全风控需要，调整可用模型、请求限制、价格、折扣、分组和调用规则。页面展示、实际账单和调用记录不一致时，以后台实时记录和平台最终核算为准。

## 2. 账号、安全与使用责任

你应使用真实、合法、有效的信息注册和使用 Dwanshift，并妥善保管账号、密码、API Key、访问令牌、支付凭证和管理权限。账号下发生的调用、消费、上传、生成、分发和管理行为，默认由账号持有人承担责任。

未经 Dwanshift 书面同意，不得转租、转售、共享、批量分发账号或密钥，不得以自动化、代理池、撞库、刷量、绕过限速等方式规避平台管理规则。发现密钥泄露、异常消费或账号被盗时，应立即停用相关密钥并联系平台处理。

## 3. 计费、余额与退款

Dwanshift 可采用预充值、按量扣费、套餐、订阅或混合计费方式。模型价格、汇率、渠道成本、税费或上游政策变化时，平台可对价格和规则进行调整，并通过页面或公告展示。

已实际消耗的额度、已完成的接口调用、已交付的套餐权益通常不支持退款。因用户配置错误、密钥泄露、误调用、第三方客户端异常导致的消费，原则上仍按实际调用记录计费。法律法规另有强制要求或平台另行书面承诺的除外。

## 4. 合规使用要求

你不得利用 Dwanshift 生成、传播、存储、协助制作或引流违法违规内容，包括但不限于涉黄、涉赌、涉毒、诈骗、洗钱、钓鱼、跑分、侵权、恶意营销、仿冒客服、非法荐股、黑灰产工具、攻击脚本、批量注册、垃圾信息和侵犯他人隐私或知识产权的内容。

你应自行确认输入数据、上传文件、生成内容和业务用途具有合法来源、处理权限和使用依据。AI 输出具有概率性，平台不保证输出内容真实、准确、完整、合法或适用于特定业务场景；你应自行复核并承担使用后果。

## 5. 服务中断与责任限制

因上游模型、云服务、网络线路、支付通道、DNS、证书、系统升级、攻击、监管要求、不可抗力或其他非平台可完全控制因素导致的延迟、中断、错误、失败或数据异常，Dwanshift 将尽力恢复，但在法律允许范围内不承担扩张性赔偿责任。

在任何情况下，Dwanshift 对间接损失、预期收益损失、业务中断损失、数据丢失或第三方索赔不承担超出法律强制范围的责任。平台对用户的责任上限以争议发生前合理期间内用户实际支付且未消耗的服务费用为限，法律另有规定的除外。

## 6. 违规处置

如平台判断存在违规、滥用、异常风险或安全事件，Dwanshift 有权在无需提前通知的情况下采取限速、暂停接口、冻结余额、禁用密钥、封禁账号、拒绝退款、留存日志、终止服务、向主管机关或合作方提供必要线索等措施。

## 7. 条款变更

Dwanshift 可根据业务、合规和安全需要更新本条款。更新后的条款发布后生效；如你不同意更新内容，应停止使用服务。继续使用即视为接受更新后的条款。
"""

privacy = """# 隐私保护

Dwanshift 尊重并保护用户隐私。我们仅在提供 AI 接口中转、账号管理、计费结算、安全风控、客户支持和履行法定义务所必需的范围内收集和处理信息，不以出售个人信息作为业务模式。

> **服务域名**：`https://dawnshift.xyz`

## 1. 我们可能收集的信息

| 类别 | 示例 |
|------|------|
| 账号信息 | 邮箱、用户名、注册时间、登录时间、账号状态 |
| 使用信息 | API Key 标识、请求时间、模型名称、接口路径、用量、余额、账单和错误记录 |
| 设备与网络信息 | IP 地址、浏览器信息、设备基础信息、地区、访问日志 |
| 支付与对账信息 | 订单号、支付渠道、金额、支付状态、退款或争议记录 |
| 安全风控信息 | 异常频率、封禁记录、风险标记、申诉和处理记录 |

我们通常不会主动查看你的完整业务内容；但为排查故障、安全审计、响应投诉、处理违法违规行为或履行法律义务，可能在必要范围内处理相关日志、请求元数据或用户提交的信息。

## 2. 信息使用目的

- 完成注册、登录、身份验证、密钥管理和控制台展示。
- 进行额度扣减、订单处理、支付对账、发票或财务核验。
- 维护接口稳定性，定位错误、优化性能、防止滥用和攻击。
- 提供客户支持、通知服务变更、处理投诉、申诉和安全事件。
- 满足法律法规、监管要求、司法协助、审计和合规留存要求。

## 3. 对外共享与第三方服务

Dwanshift 不会擅自出售用户个人信息。为了提供服务，我们可能在最小必要范围内与支付机构、云基础设施服务商、邮件或消息服务商、日志与安全服务商、上游模型服务商共享必要信息。

当法律法规、监管机关、司法机关或争议处理程序要求时，我们可能依法提供必要记录。若发生合并、分立、资产转让或服务迁移，我们会要求新的处理方继续按照不低于本政策的标准保护相关信息。

## 4. 存储与安全

我们会采取合理的技术和管理措施保护数据安全，包括访问控制、权限分离、日志审计、加密传输、密钥管理和异常监控。但互联网环境无法保证绝对安全，你也应妥善保存账号密码和 API Key，避免在公开仓库、聊天记录或客户端明文泄露。

涉及财务对账、风控审计、安全事件、法律合规的数据，可能会在必要期限内保留。超过必要期限后，我们会删除、匿名化或按合规要求继续留存。

## 5. 用户权利

你可以申请查询、更正或删除账号相关信息，也可以申请注销账号。为保障安全，平台可能要求你完成身份验证。对于法律要求留存、财务对账、风控审计、争议处理所必需的信息，我们可能无法立即删除，但会限制其使用范围。

## 6. 你的义务

请勿向 Dwanshift 输入、上传或转发你无权处理的数据，包括涉密信息、他人隐私、侵权内容、非法数据或受特殊监管保护的数据。你应确保提交给平台的数据具有合法来源、合法授权和明确使用目的。

## 7. 政策更新

我们可能根据服务变化、法律法规或安全要求更新本隐私政策。更新后会在页面发布；你继续使用 Dwanshift，即表示接受更新后的政策。
"""

sql = f"""
WITH vals AS (
  SELECT
    convert_from(decode('{b64(terms)}','base64'),'UTF8') AS terms_content,
    convert_from(decode('{b64(privacy)}','base64'),'UTF8') AS privacy_content,
    convert_from(decode('{b64("Dwanshift")}','base64'),'UTF8') AS site_name,
    convert_from(decode('{b64("/site-assets/branding/dwanshift-logo.png")}','base64'),'UTF8') AS site_logo,
    convert_from(decode('{b64("https://dawnshift.xyz")}','base64'),'UTF8') AS base_url,
    convert_from(decode('{b64("AI API Relay Platform")}','base64'),'UTF8') AS subtitle
), updated_pages AS (
  SELECT jsonb_agg(
    CASE
      WHEN elem->>'key' = 'terms'
        THEN elem || jsonb_build_object('title','服务条款','content', vals.terms_content, 'updated_at', to_char(now(), 'YYYY-MM-DD HH24:MI:SS'))
      WHEN elem->>'key' = 'privacy'
        THEN elem || jsonb_build_object('title','隐私保护','content', vals.privacy_content, 'updated_at', to_char(now(), 'YYYY-MM-DD HH24:MI:SS'))
      ELSE elem || jsonb_build_object(
        'title', replace(replace(elem->>'title', 'LumioAPI', 'Dwanshift'), 'Lumio', 'Dwanshift'),
        'content', replace(replace(replace(replace(replace(replace(elem->>'content', 'LumioAPI', 'Dwanshift'), 'Lumio', 'Dwanshift'), 'https://api.lumio.games', vals.base_url), 'https://img.lumio.games', vals.base_url || '/image2'), 'api.lumio.games', 'dawnshift.xyz'), 'img.lumio.games', 'dawnshift.xyz/image2'),
        'updated_at', to_char(now(), 'YYYY-MM-DD HH24:MI:SS')
      )
    END
  ) AS pages
  FROM vals, jsonb_array_elements((SELECT value::jsonb FROM settings WHERE key='site_pages')) elem
)
INSERT INTO settings (key, value)
SELECT k, v
FROM vals,
LATERAL (VALUES
  ('site_name', vals.site_name),
  ('site_logo', vals.site_logo),
  ('api_base_url', vals.base_url),
  ('frontend_url', vals.base_url),
  ('site_subtitle', vals.subtitle),
  ('doc_url', vals.base_url || '/docs'),
  ('site_pages', (SELECT pages::text FROM updated_pages)),
  ('home_content', replace(replace(replace(replace(coalesce((SELECT value FROM settings WHERE key='home_content'), ''), 'LumioAPI', 'Dwanshift'), 'Lumio', 'Dwanshift'), 'https://api.lumio.games', vals.base_url), 'https://img.lumio.games', vals.base_url || '/image2'))
) AS data(k, v)
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;
"""

sql_path = Path("deploy/data/update-dwanshift-branding.sql")
sql_path.write_text(sql, encoding="utf-8")
subprocess.run(["docker", "cp", str(sql_path), "sub2api-postgres-dev:/tmp/update-dwanshift-branding.sql"], check=True)
subprocess.run(["docker", "exec", "sub2api-postgres-dev", "psql", "-U", "sub2api", "-d", "sub2api", "-f", "/tmp/update-dwanshift-branding.sql"], check=True)
