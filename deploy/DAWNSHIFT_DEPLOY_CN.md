# Dawnshift 本地构建与服务器部署手册

本文档对应当前这套实际落地方案：

- 本地用 Docker Desktop 从源码构建并验证
- 服务器不编译源码，只导入本地构建好的镜像
- 服务器最终由 `sub2api-caddy` 直接承接 `80/443`
- `dawnshift.xyz` 最终指向 `sub2api`

## 1. 现状与约束

- 本地环境已有 Docker Desktop、Node.js；前端可通过 `corepack pnpm` 使用 pnpm。
- 服务器 `38.181.57.100` 已安装 Docker 与 Docker Compose。
- 最初 `80/443` 由旧入口容器 `new-api-caddy` 占用。
- `dawnshift.xyz` 的 DNS 已指向 `38.181.57.100`。
- 为了避免在服务器编译，所有应用镜像都在本地构建并通过 `docker save` / `docker load` 迁移。

## 2. 仓库内新增或调整的部署资产

- `deploy/docker-compose.server.yml`
  - 服务器专用 Compose。
  - `sub2api` 只在 `127.0.0.1:${HOST_SERVER_PORT}` 暴露诊断端口。
  - `sub2api-caddy` 直接承接 `80/443`。
  - 数据库与 Redis 使用唯一主机名，避免和其他容器网络中的同名服务冲突。
- `deploy/Caddyfile.dawnshift.example`
  - `sub2api-caddy` 可直接使用的 Caddy 配置。
- `deploy/Caddyfile.server`
  - 当前部署直接使用的服务器入口配置。
- `deploy/init-env.ps1`
  - 从 `deploy/.env.example` 生成 `.env`。
  - 自动填充数据库/JWT/TOTP 密钥。
  - 支持写入 `SUB2API_IMAGE`、`CADDY_DATA_VOLUME`、`CADDY_CONFIG_VOLUME`。
- `deploy/build_image.sh`
  - 支持自定义镜像名、标签，以及导出 tar 包。
- `deploy/docker-compose.yml`
- `deploy/docker-compose.local.yml`
- `deploy/docker-compose.standalone.yml`
  - 统一支持 `SUB2API_IMAGE` 环境变量，方便切换到本地构建镜像。

## 3. 本地开发 / 构建 / 验证流程

### 3.1 生成本地部署环境文件

在仓库根目录执行：

```powershell
.\deploy\init-env.ps1 -OutputPath .env -AdminEmail admin@dawnshift.xyz -AdminPassword '<your-admin-password>'
```

这会在 `deploy/` 目录下：

- 生成 `deploy/.env`
- 创建 `deploy/data`
- 创建 `deploy/postgres_data`
- 创建 `deploy/redis_data`

### 3.2 从源码在本机构建并启动

```powershell
docker compose -f deploy/docker-compose.dev.yml --env-file deploy/.env up --build -d
```

说明：

- `deploy/docker-compose.dev.yml` 直接使用仓库根目录的 `Dockerfile`
- 前端与后端都在本地 Docker Desktop 中完成构建
- 这满足“本地编译、服务器不编译”的要求
- 如果本机 `8080` 被占用，可以把 `deploy/.env` 中的 `SERVER_PORT` 改为 `18080`、`28080` 等空闲端口

### 3.3 本地验证

```powershell
docker compose -f deploy/docker-compose.dev.yml --env-file deploy/.env ps
Invoke-WebRequest http://127.0.0.1:18080/health
```

如需查看启动日志：

```powershell
docker compose -f deploy/docker-compose.dev.yml --env-file deploy/.env logs -f sub2api
```

## 4. 镜像打包与服务器环境文件

### 4.1 在本地构建最终生产镜像

建议使用“日期 + commit”的标签：

```powershell
$tag = "2026-04-29-a16c6650"
docker build -t "sub2api:$tag" -f Dockerfile .
docker save -o "deploy\sub2api-$tag.tar" "sub2api:$tag"
```

也可以用 Bash：

```bash
IMAGE_NAME=sub2api IMAGE_TAG=2026-04-29-a16c6650 OUTPUT_TAR=deploy/sub2api-2026-04-29-a16c6650.tar ./deploy/build_image.sh
```

### 4.2 生成服务器 `.env`

如果是从旧 `new-api-caddy` 迁移，建议复用旧证书卷：

```powershell
.\deploy\init-env.ps1 `
  -OutputPath .env.server `
  -AdminEmail admin@dawnshift.xyz `
  -AdminPassword '<strong-password>' `
  -Sub2ApiImage 'sub2api:2026-04-29-a16c6650' `
  -HostServerPort 18080 `
  -CaddyDataVolume 'newapi_caddy_data' `
  -CaddyConfigVolume 'newapi_caddy_config'
```

生成后把 `deploy/.env.server` 上传到服务器并命名为 `.env`。

## 5. 服务器目录结构

推荐目录：

```text
/opt/sub2api/
  docker-compose.server.yml
  .env
  Caddyfile.server
  data/
  postgres_data/
  redis_data/
  sub2api-2026-04-29-a16c6650.tar
```

## 6. 服务器部署流程

### 6.1 上传文件

需要上传：

- `deploy/docker-compose.server.yml`
- `deploy/.env.server`（上传后命名为 `.env`）
- `deploy/Caddyfile.server`
- `deploy/sub2api-2026-04-29-a16c6650.tar`

### 6.2 导入镜像并启动应用栈

```bash
cd /opt/sub2api
docker load -i sub2api-2026-04-29-a16c6650.tar
mv .env.server .env   # 如果上传时保留了原名
docker compose -f docker-compose.server.yml up -d sub2api postgres redis
docker compose -f docker-compose.server.yml ps
curl http://127.0.0.1:18080/health
```

如果 `curl` 返回 `{"status":"ok"}`，说明 `sub2api` 在服务器内网已经可用。

## 7. 从 new-api-caddy 迁移到 sub2api-caddy

### 7.1 旧环境现状

旧入口通常类似：

```caddy
www.dawnshift.xyz {
    redir https://dawnshift.xyz{uri} permanent
}

dawnshift.xyz {
    encode gzip zstd
    reverse_proxy new-api:3000
}
```

旧证书卷一般是：

- `newapi_caddy_data`
- `newapi_caddy_config`

### 7.2 迁移步骤

1. 确认 `sub2api` 在服务器内部健康。
2. 确认 `/opt/sub2api/.env` 中设置了：

```env
CADDY_DATA_VOLUME=newapi_caddy_data
CADDY_CONFIG_VOLUME=newapi_caddy_config
```

3. 停掉旧入口：

```bash
docker update --restart=no new-api-caddy
docker stop new-api-caddy
```

4. 启动新的入口：

```bash
cd /opt/sub2api
docker compose -f docker-compose.server.yml up -d caddy
```

### 7.3 切换后验证

```bash
curl -I https://dawnshift.xyz
curl https://dawnshift.xyz/health
```

期望结果：

- `https://dawnshift.xyz/health` 返回 `{"status":"ok"}`
- 首页标题是 `Sub2API - AI API Gateway`

## 8. 回滚方案

如果入口迁移后发现异常：

1. 停掉 `sub2api-caddy`
2. 重新启用旧入口

```bash
docker start new-api-caddy
docker update --restart=unless-stopped new-api-caddy
```

回滚只需要恢复入口容器，不需要先删除 `sub2api`。

## 9. 常用运维命令

本地：

```powershell
docker compose -f deploy/docker-compose.dev.yml --env-file deploy/.env logs -f sub2api
docker compose -f deploy/docker-compose.dev.yml --env-file deploy/.env down
```

服务器：

```bash
cd /opt/sub2api
docker compose -f docker-compose.server.yml ps
docker compose -f docker-compose.server.yml logs -f sub2api
docker compose -f docker-compose.server.yml logs -f caddy
docker compose -f docker-compose.server.yml restart sub2api
docker compose -f docker-compose.server.yml restart caddy
docker compose -f docker-compose.server.yml down
```

## 10. 风险说明

- 入口容器切换属于生产变更。
- 当前方案已经把风险压到较低：
  - 先并行部署 `sub2api`
  - 验证内网健康
  - 再切换 `443` 入口
  - 证书卷沿用旧 Caddy 数据
- 但仍建议保留旧入口容器与旧数据一段时间，确认业务稳定后再彻底清理。
