# 实战指南：ECS 直连部署 (Node.js 方案)

如果你不想配置 Nginx，或者只是想快速测试，可以使用 Node.js 的静态文件服务工具（如 `serve`）直接运行网站。

这种方案简单直接，适合测试环境或小型个人站点。

## 1. 服务器准备

### 1.1 开放端口
在阿里云 ECS 控制台的“安全组”中，开放你需要使用的端口。
- **3000** (或者 8080 等你喜欢的端口)
- **80** (如果你想直接通过 IP 访问而不加端口，需要 root 权限)

## 2. 环境初始化

### 2.1 安装 Node.js
```bash
# 安装 nvm (Node Version Manager)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc

# 安装 Node.js LTS 版本
nvm install --lts
nvm use --lts
```

### 2.2 安装 PM2 和 serve
`serve` 是一个简单的静态文件服务器。
`pm2` 用于在后台运行 `serve`，保证它在关闭终端后继续运行，并支持开机自启。

```bash
npm install -g serve pm2
```

## 3. 部署代码

### 3.1 获取代码
```bash
mkdir -p ~/apps
cd ~/apps
git clone https://github.com/llmlearning-x/claude_code_guide.git
cd claude_code_guide
```

### 3.2 构建项目
```bash
cd site
npm install
npm run docs:build
```
构建完成后，静态文件会在 `site/dist` 目录。

## 4. 启动服务

### 4.1 使用 PM2 启动 serve
我们将使用 `serve` 命令托管 `dist` 目录，并用 `pm2` 来管理它。

```bash
# 格式: pm2 start serve --name <应用名> -- -s <构建目录> -p <端口>

# 进入构建后的 dist 目录所在的 site 文件夹
cd site

# 方案 A: 运行在 3000 端口 (推荐，不需要 root)
# 注意 serve 后面跟着的是 dist 目录
pm2 start serve --name claude-guide -- -s dist -p 3000


# 方案 B: 运行在 80 端口 (需要 root 权限，或者是 sudo)
# 注意: 非 root 用户通常无法绑定 1024 以下的端口。
# 如果必须用 80 且不想用 Nginx，建议使用 authbind 或者 sudo 运行
sudo pm2 start serve --name claude-guide -- -s dist -p 80
```

### 4.2 保存进程 (开机自启)
```bash
pm2 save
pm2 startup
# 按照提示运行生成的命令
```

## 5. 访问网站

现在，你可以直接通过浏览器访问：
`http://<你的公网IP>:3000`

## 6. 使用 pm2 运行 HTTPS (高级)

如果你想用 HTTPS，serve 也支持。

```bash
# 生成自签名证书 (或者从 Certbot 获取)
# serve-handler options: https://github.com/vercel/serve-handler#options

# 启动 HTTPS
pm2 start serve --name claude-guide -- -s dist -p 443 --ssl-cert path/to/cert.pem --ssl-key path/to/key.pem
```

## 7. 更新部署

当有代码更新时：

```bash
cd ~/apps/claude_code_guide/site
git pull
npm install
npm run docs:build

# 重启服务 (通常 serve 不需要重启，因为它只是托管静态文件，
# 但为了确保缓存清除，重启一下更稳妥)
pm2 restart claude-guide
```

---
**对比 Nginx 方案的优缺点：**
- **优点**：配置极其简单，不需要学习 Nginx 配置文件，纯 Node.js 技术栈。
- **缺点**：静态资源处理性能不如 Nginx，缺乏高级功能（如 Gzip 细粒度控制、SSL 证书自动管理、负载均衡等）。HTTPS 配置稍微麻烦一点（serve 支持 HTTPS 但需要手动指定证书路径）。
