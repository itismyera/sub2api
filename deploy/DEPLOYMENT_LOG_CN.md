# Dawnshift 部署记录

本文记录线上部署事实、验证结果和回滚入口。敏感信息不写入仓库文档。

## 2026-05-06 线上部署

- 部署时间：2026-05-06 12:37-12:41 Asia/Shanghai
- 部署分支：`2026-04-29`
- 部署提交：`cfb7e993`
- 本地源镜像：`deploy-sub2api:latest`
- 线上镜像：`sub2api:2026-05-06-cfb7e993`
- 本地镜像包：`deploy/sub2api-2026-05-06-cfb7e993.tar`
- 服务器：`38.181.57.100`
- 服务器目录：`/opt/sub2api`
- 域名：`dawnshift.xyz`
- 入口：`sub2api-caddy` 直接监听 `80/443`
- 应用诊断端口：`127.0.0.1:18080`

### 部署方式

服务器不编译源码。流程是本地 Docker Desktop 构建完成后，把镜像保存为 tar 包上传到服务器，服务器只执行 `docker load` 和 `docker compose up -d`。

```powershell
docker tag deploy-sub2api:latest sub2api:2026-05-06-cfb7e993
docker save -o deploy\sub2api-2026-05-06-cfb7e993.tar sub2api:2026-05-06-cfb7e993
```

服务器侧执行的关键步骤：

```bash
cd /opt/sub2api
docker load -i sub2api-2026-05-06-cfb7e993.tar
docker compose -f docker-compose.server.yml up -d postgres redis sub2api
curl -fsS http://127.0.0.1:18080/health
docker compose -f docker-compose.server.yml up -d caddy
docker exec sub2api-caddy caddy reload --config /etc/caddy/Caddyfile
```

### 配置保护

部署时没有用本地 `deploy/.env.server` 整体覆盖服务器 `.env`，而是读取服务器现有 `/opt/sub2api/.env`，仅替换：

```env
SUB2API_IMAGE=sub2api:2026-05-06-cfb7e993
```

部署前自动备份了服务器文件：

- `/opt/sub2api/.env.bak-20260506-123746`
- `/opt/sub2api/docker-compose.server.yml.bak-20260506-123746`
- `/opt/sub2api/Caddyfile.server.bak-20260506-123746`

### 验证结果

服务器容器状态：

- `sub2api`：`sub2api:2026-05-06-cfb7e993`，healthy
- `sub2api-postgres`：healthy
- `sub2api-redis`：healthy
- `sub2api-caddy`：运行中，监听 `80/443`

健康检查结果：

```bash
curl -fsS http://127.0.0.1:18080/health
# {"status":"ok"}

curl -fsS https://dawnshift.xyz/health
# {"status":"ok"}

curl -I https://dawnshift.xyz/
# HTTP/2 200
```

DNS 在服务器侧解析到：

```text
38.181.57.100 dawnshift.xyz
```

### 回滚方式

如果需要回滚到部署前镜像，先查看服务器 `/opt/sub2api/.env.bak-20260506-123746` 中原来的 `SUB2API_IMAGE`，当前部署前记录到的旧镜像是：

```env
SUB2API_IMAGE=sub2api:20260430-4385b6af-compat
```

回滚命令：

```bash
cd /opt/sub2api
cp -a .env .env.rollback-from-20260506
cp -a .env.bak-20260506-123746 .env
docker compose -f docker-compose.server.yml up -d postgres redis sub2api
curl -fsS http://127.0.0.1:18080/health
docker compose -f docker-compose.server.yml up -d caddy
docker exec sub2api-caddy caddy reload --config /etc/caddy/Caddyfile
```

### 注意事项

- 本次部署的是 `2026-04-29@cfb7e993`。
- 本次部署未包含 `2026-04-30` 分支上的生图入口提交。
- 不要把服务器 SSH 密码、数据库密码、JWT/TOTP 密钥写入仓库文档。
