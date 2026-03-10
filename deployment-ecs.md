---
title: 实战指南：将本书部署到阿里云 ECS
---

# 实战指南：将本书部署到阿里云 ECS

![阿里云 ECS 部署](../images/practices-backend-ops-cover.png)

本文档将介绍如何将《Claude Code 工程实践》这本书（基于 VitePress 构建的静态网站）部署到阿里云 ECS 服务器上，让读者可以通过公网访问。

## 1. 服务器准备

### 1.1 选购 ECS 实例
对于静态文档网站，资源消耗非常低，入门级配置即可：
- **计费方式**：包年包月（长期）或按量付费（测试）。
- **地域**：建议选择华东 1（杭州）或华北 2（北京）。
- **实例规格**：1 vCPU / 1 GiB (如 ecs.t6-c1m1.large) 足够。
- **操作系统**：Alibaba Cloud Linux 3 或 Ubuntu 22.04 LTS。
- **公网 IP**：需要分配公网 IP，带宽建议 3Mbps 以上（静态资源加载更快）。

### 1.2 配置安全组
在阿里云控制台开放以下端口：
- **22 (SSH)**: 用于远程连接。
- **80 (HTTP)**: Web 服务端口。
- **443 (HTTPS)**: 如果需要 HTTPS 访问。

## 2. 环境初始化

### 2.1 登录服务器
```bash
ssh root@<你的公网IP>
```

### 2.2 安装 Nginx
Nginx 是高性能的 Web 服务器，非常适合托管静态网站。

```bash
# Ubuntu
sudo apt update
sudo apt install -y nginx git

# Alibaba Cloud Linux / CentOS
sudo yum update -y
sudo yum install -y nginx git
```

启动 Nginx 并设置开机自启：
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
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

### 2.4 安装 Node.js (用于构建)
虽然 Nginx 只负责托管静态文件，但我们需要 Node.js 来运行构建命令。

```bash
# 安装 nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc

# 安装 Node.js LTS
nvm install --lts
nvm use --lts
```

## 3. 部署代码

### 3.1 获取项目代码
我们将代码克隆到 `/var/www` 目录下。为了避免权限问题，我们需要先修改目录所有权。

```bash
# 1. 创建目录 (使用 sudo，因为 /var 通常归 root 所有)
sudo mkdir -p /var/www

# 2. 将目录所有权交给 deployer 用户
# 这一步非常重要！否则后续 git clone 和 npm install 会报 Permission denied
sudo chown -R deployer:deployer /var/www

# 3. 进入目录
cd /var/www

# 4. 克隆代码库 (不需要 sudo)
git clone https://github.com/llmlearning-x/claude_code_guide.git

cd claude_code_guide
```

### 3.2 安装依赖与构建
本书的源码位于 `docs` 目录，但构建配置在 `site` 目录。

```bash
# 进入 site 目录
cd site

# 安装依赖
npm install

# 执行构建
npm run docs:build
```

构建完成后，静态文件会生成在 `site/dist` 目录下。

## 4. 配置 Nginx

### 4.1 创建站点配置
新建一个 Nginx 配置文件：

```bash
sudo vim /etc/nginx/conf.d/claude-guide.conf
```

写入以下内容：

```nginx
server {
    listen 80;
    server_name llmlearning.org.cn www.llmlearning.org.cn;

    # 网站根目录指向构建生成的 dist 目录
    root /var/www/claude_code_guide/site/dist;
    index index.html;

    # 开启 Gzip 压缩，加速访问
    gzip on;
    gzip_min_length 1k;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/javascript application/json application/javascript application/x-javascript application/xml;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # 缓存静态资源
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
}
```

*注意：如果 `/etc/nginx/nginx.conf` 中包含了 default server 配置，可能需要先移除或修改它，避免冲突。*

### 4.2 重载 Nginx
检查配置是否正确并重启：

```bash
sudo nginx -t
sudo systemctl reload nginx
```

此时，访问服务器的公网 IP，应该就能看到部署好的《Claude Code 工程实践》了！

### 4.3 配置 HTTPS

```bash
# 自动获取证书并配置 Nginx
sudo certbot --nginx -d llmlearning.org.cn -d www.llmlearning.org.cn
```

## 5. 持续更新

当书稿内容有更新时，只需在服务器上执行：

```bash
cd /var/www/claude_code_guide/site
git pull
npm install # 如果依赖有变化
npm run docs:build
```

无需重启 Nginx，刷新浏览器即可看到最新内容。

## 6. 进阶：自动化部署 (GitHub Actions)

为了避免每次都要手动 SSH 上去构建，可以配置 GitHub Actions。

在项目根目录创建 `.github/workflows/deploy.yml`：

```yaml
name: Deploy to Aliyun ECS

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 18

      - name: Build
        run: |
          cd site
          npm install
          npm run docs:build

      - name: Deploy to Server
        uses: appleboy/scp-action@master
        with:
          host: ${{ secrets.HOST }}
          username: ${{ secrets.USERNAME }}
          key: ${{ secrets.SSH_KEY }}
          source: "site/dist/*"
          target: "/var/www/claude_code_guide/site/dist"
          strip_components: 2 # 根据实际路径层级调整
```

这样，每次 push 代码，GitHub 就会自动帮你构建并将最新的静态文件传输到服务器上。
