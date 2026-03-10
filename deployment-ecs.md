---
title: 实战指南：阿里云 ECS 部署流程
---

# 实战指南：阿里云 ECS 部署流程

![阿里云 ECS 部署](../images/practices-backend-ops-cover.png)

本文档将手把手带你完成从零开始配置阿里云 ECS 服务器，并将 Web 应用（以 Node.js 为例）部署上线的完整流程。

## 1. 服务器准备

### 1.1 选购 ECS 实例
对于个人开发者或小型项目，推荐以下配置：
- **计费方式**：包年包月（长期更划算）或按量付费（测试用）。
- **地域**：选择距离目标用户最近的节点（如华东 1 杭州）。
- **实例规格**：2 vCPU / 2 GiB (e.g., ecs.t6-c1m1.large) 起步即可。
- **操作系统**：Alibaba Cloud Linux 3 或 Ubuntu 22.04 LTS。
- **公网 IP**：分配公网 IPv4 地址，带宽选择 "按使用流量"（峰值带宽可设高一点，如 100Mbps）。

### 1.2 配置安全组（防火墙）
在购买过程中或控制台的“网络与安全” -> “安全组”中，开放以下端口：
- **22 (SSH)**: 用于远程连接（建议仅对你的 IP 开放）。
- **80 (HTTP)**: Web 服务默认端口。
- **443 (HTTPS)**: 加密 Web 服务端口。
- **3000-9000 (可选)**: 如果你的应用直接暴露端口测试，需临时开放。

## 2. 系统初始化

### 2.1 远程连接
使用终端（macOS/Linux）或 PowerShell（Windows）连接服务器：

```bash
ssh root@<你的公网IP>
# 输入密码登录
```

### 2.2 更新系统与安装基础工具
登录后，首先更新软件包列表：

```bash
# Ubuntu
apt update && apt upgrade -y
apt install -y git curl wget vim unzip

# Alibaba Cloud Linux / CentOS
yum update -y
yum install -y git curl wget vim unzip
```

### 2.3 创建非 root 用户 (推荐)
为了安全，不建议一直使用 root 操作。

```bash
# 创建用户 (例如: deployer)
adduser deployer
# 设置密码
passwd deployer
# 赋予 sudo 权限
# Ubuntu 系统
usermod -aG sudo deployer
# Alibaba Cloud Linux / CentOS 系统 (使用 wheel 组)
usermod -aG wheel deployer
# 切换用户
su - deployer
```

## 3. 环境搭建 (Node.js + Nginx)

### 3.1 安装 Node.js (使用 nvm)
推荐使用 nvm 管理 Node 版本：

```bash
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# 重新加载配置
source ~/.bashrc

# 安装 LTS 版本 Node.js
nvm install --lts
nvm use --lts

# 验证
node -v
npm -v
```

### 3.2 安装 PM2 (进程管理)
PM2 用于保持 Node 应用在后台运行，并支持自动重启。

```bash
npm install -g pm2
```

### 3.3 安装 Nginx (Web 服务器)

```bash
# Ubuntu
sudo apt install -y nginx

# Alibaba Cloud Linux
sudo yum install -y nginx

# 启动并设置开机自启
sudo systemctl start nginx
sudo systemctl enable nginx
```

此时访问服务器 IP，应能看到 Nginx 欢迎页面。

## 4. 部署应用

### 4.1 获取代码
假设你的代码在 GitHub/GitLab 上：

```bash
# 生成部署密钥 (如果项目是私有的)
ssh-keygen -t ed25519 -C "deploy@server"
cat ~/.ssh/id_ed25519.pub
# -> 将公钥添加到 GitHub/GitLab 的 Deploy Keys 中

# 克隆代码
mkdir -p ~/apps
cd ~/apps
git clone git@github.com:yourname/your-repo.git
cd your-repo
```

### 4.2 安装依赖与构建

```bash
# 安装依赖
npm install

# 如果是构建型项目 (如 Next.js, Vue/React SSR)
npm run build
```

### 4.3 启动应用
使用 PM2 启动服务：

```bash
# 假设入口文件是 app.js 或 server.js
pm2 start app.js --name "my-app"

# 或者运行 npm 脚本
pm2 start npm --name "my-app" -- run start

# 保存当前进程列表，以便重启后自动恢复
pm2 save
pm2 startup
# (根据提示运行生成的命令)
```

## 5. 配置 Nginx 反向代理与 HTTPS

### 5.1 配置反向代理
编辑 Nginx 配置文件：

```bash
sudo vim /etc/nginx/conf.d/my-app.conf
```

写入以下内容：

```nginx
server {
    listen 80;
    server_name example.com www.example.com; # 替换为你的域名

    location / {
        proxy_pass http://127.0.0.1:3000; # 替换为你应用的端口
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

测试并重载 Nginx：

```bash
sudo nginx -t
sudo systemctl reload nginx
```

### 5.2 配置 HTTPS (Certbot)
使用 Certbot 免费申请 Let's Encrypt 证书。

```bash
# Ubuntu
sudo apt install -y certbot python3-certbot-nginx

# Alibaba Cloud Linux (可能需要启用 EPEL)
sudo yum install -y certbot python3-certbot-nginx

# 自动获取证书并配置 Nginx
sudo certbot --nginx -d example.com -d www.example.com
```

按照提示输入邮箱并同意协议。Certbot 会自动修改 Nginx 配置以启用 HTTPS。

## 6. 常用运维命令速查

- **查看应用日志**: `pm2 logs my-app`
- **重启应用**: `pm2 restart my-app`
- **查看 Nginx 状态**: `sudo systemctl status nginx`
- **查看服务器资源**: `htop` (需安装: `sudo apt install htop`)
- **查看磁盘空间**: `df -h`

## 7. 下一步：CI/CD 自动化
手动部署虽然稳健，但繁琐。你可以考虑：
1.  **GitHub Actions**: 编写 `.github/workflows/deploy.yml`，在 push 代码时自动 SSH 到服务器执行 `git pull && pm2 restart`。
2.  **Docker**: 将应用容器化，使用 Docker Compose 一键启动。

---
*注：本文档中的命令以 Ubuntu/Debian 为主，Alibaba Cloud Linux/CentOS 请替换相应的包管理器命令 (apt -> yum/dnf)。*
