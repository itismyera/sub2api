# 2026-04-30 兼容性升级记录

## 目标

- 从 `main` 拉取最新代码，并合并到当前分支 `2026-04-29`。
- 修复旧支付 provider 数据中 `supported_types` 为空时前后端不兼容的问题。
- 避免在服务器上编译：本机 Docker Desktop 构建镜像，导出 tar 后上传服务器。
- 保持生产入口为 `https://dawnshift.xyz`，由 `sub2api-caddy` 承接 `80/443`。

## 代码变更

- 后端 `splitTypes("")` 返回空数组而不是 `nil`，避免 API 序列化为 `null`。
- 前端 payment provider 读取、展示、切换支付类型时兼容 `supported_types=null`。
- 增加回归测试 `TestSplitTypesEmptyReturnsNonNilSlice`。

## 分支同步

```powershell
git checkout main
git pull --ff-only origin main
git checkout 2026-04-29
git merge main --no-edit
```

本次同步结果：`main` 已是最新，合并到 `2026-04-29` 后无冲突。

## 本机构建与验证

生产镜像标签：

```text
sub2api:20260430-4385b6af-compat
```

构建与导出：

```powershell
docker build -t sub2api:20260430-4385b6af-compat --build-arg COMMIT=4385b6af-compat -f Dockerfile .
docker save -o deploy\sub2api-20260430-4385b6af-compat.tar sub2api:20260430-4385b6af-compat
```

本机 Docker Desktop 验证：

```powershell
docker compose -f deploy\docker-compose.dev.yml up -d --build sub2api
Invoke-WebRequest http://127.0.0.1:18080/health
```

验证结果：

```json
{"status":"ok"}
```

## 服务器升级

服务器目录：

```text
/opt/sub2api
```

服务器 Docker 环境：

```text
Docker 26.1.3
Docker Compose v2.27.0
```

升级步骤：

```bash
cd /opt/sub2api
docker load -i sub2api-20260430-4385b6af-compat.tar
cp .env ".env.backup.$(date +%Y%m%d%H%M%S)"
sed -i 's|^SUB2API_IMAGE=.*|SUB2API_IMAGE=sub2api:20260430-4385b6af-compat|' .env
docker compose -f docker-compose.server.yml up -d sub2api
```

本次 `.env` 备份文件：

```text
/opt/sub2api/.env.backup.20260430010103
```

## 线上验证

服务器内网健康检查：

```bash
curl -fsS http://127.0.0.1:18080/health
```

公网 HTTPS 健康检查：

```powershell
Invoke-WebRequest https://dawnshift.xyz/health
```

验证结果：

```json
{"status":"ok"}
```

DNS 验证：

```text
dawnshift.xyz A 38.181.57.100
```

容器状态：

```text
sub2api          sub2api:20260430-4385b6af-compat   healthy   127.0.0.1:18080->8080
sub2api-caddy    caddy:2.11.2-alpine                running   80/443
sub2api-postgres postgres:18-alpine                 healthy
sub2api-redis    redis:8-alpine                     healthy
```

数据库兼容性核对：

```text
users.role: admin=3
payment_provider_instances: alipay supported_types=alipay
```

## 回滚

如需回滚应用镜像，不需要动数据库：

```bash
cd /opt/sub2api
cp .env.backup.20260430010103 .env
docker compose -f docker-compose.server.yml up -d sub2api
curl -fsS http://127.0.0.1:18080/health
```

如仅需回滚到上一个镜像，也可以直接修改 `.env`：

```env
SUB2API_IMAGE=sub2api:2026-04-29-a16c6650
```

然后执行：

```bash
docker compose -f docker-compose.server.yml up -d sub2api
```
