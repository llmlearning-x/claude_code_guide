---
title: 实战二：后端 API 服务与运维助手
---

# 第 13 章　实战二：后端 API 服务与运维助手

![实战：后端 API 服务与自动化运维](../images/practices-backend-ops-cover.png)

在上一章，我们构建了一个面向用户的 Web 应用。但在企业级开发中，后端服务和运维（Ops）往往占据了更多精力。

本章我们将视角转向幕后，看看 Claude Code 如何化身为你的 **SRE（站点可靠性工程师）助手**，帮你处理繁琐的日志查询、服务监控和部署任务。

## 13.1 现有服务的痛点分析

想象你是一个后端工程师，负责维护一套微服务架构。你的日常可能充斥着这样的对话：

-   “服务挂了，快看看日志！” -> SSH 登录服务器 -> `tail -f /var/log/app.log` -> `grep "Error"`
-   “数据库 CPU 飙高了！” -> 登录 Grafana -> 找对应的 Dashboard -> 分析慢查询
-   “部署新版本” -> 跑 Jenkins 流水线 -> 盯着控制台等结果

这些操作虽然不难，但非常**碎片化**且**上下文切换成本高**。

如果能直接对 Claude 说：“帮我看看 `order-service` 最近 10 分钟有没有报错”，那该多好？

## 13.2 设计运维类 Skill 与 MCP 集成

要实现上述愿景，我们需要给 Claude 装上“手”和“眼”。

### 13.2.1 方案 A：通过 SSH 连接 (Simple)

最简单的方法是让 Claude 能够执行远程命令。你可以编写一个简单的 MCP Server，封装 SSH 命令。

**Risk**: 直接给 SSH 权限风险很大。
**Better**: 封装特定的运维脚本。

例如，创建一个 `ops-tool` 脚本，只允许执行特定命令：
```bash
# ops-tool.sh
case $1 in
  "logs") tail -n 100 /var/log/$2.log ;;
  "status") systemctl status $2 ;;
  *) echo "Unknown command" ;;
esac
```

然后配置 Claude：
```json
{
  "mcpServers": {
    "ops": {
      "command": "ssh",
      "args": ["user@prod-server", "/usr/local/bin/ops-tool-wrapper"]
    }
  }
}
```

### 13.2.2 方案 B：集成云厂商 API (Advanced)

更现代的做法是直接调用 AWS/Azure/Aliyun 的 API。

你可以使用 `mcp-server-aws`（假设存在或自己实现），赋予 Claude 读取 CloudWatch Logs 的权限。

**User**: “检查 CloudWatch 中 `production/api-gateway` 日志组，查找最近 1 小时的 5xx 错误。”

**Claude (via MCP)**: 调用 `aws logs filter-log-events ...`，返回结果。

### 13.2.3 方案 C：Kubernetes 集成

对于 K8s 环境，官方的 `mcp-server-kubernetes` 是神器。

**配置**：
```json
{
  "mcpServers": {
    "k8s": {
      "command": "uvx",
      "args": ["mcp-server-kubernetes", "--kubeconfig", "~/.kube/config"]
    }
  }
}
```

**User**: “列出 `default` 命名空间下所有重启次数超过 5 次的 Pod。”

**Claude**: 调用 `kubectl get pods`，解析 JSON，过滤出重启次数高的 Pod 并列出。

## 13.3 落地“运维助手”工作流

有了工具，我们来看实际工作流。

### 13.3.1 故障排查 (Troubleshooting)

**场景**：用户反馈“订单支付失败”。

**User**: “@k8s 查看 `payment-service` 的日志，搜索 'PaymentFailed' 关键字。”

**Claude**:
1.  调用 K8s MCP 找到 `payment-service` 的 Pod 名称。
2.  获取该 Pod 的日志。
3.  过滤出错误堆栈。
4.  **分析原因**：“发现是连接第三方支付网关超时。可能是网络抖动或配置错误。”

### 13.3.2 数据库巡检

**场景**：通过 `mcp-server-postgres` 连接只读副本。

**User**: “检查 `orders` 表，统计过去 1 小时创建的订单状态分布。”

**Claude**: 执行 SQL `SELECT status, count(*) FROM orders WHERE created_at > NOW() - INTERVAL '1 hour' GROUP BY status;` 并生成报表。

### 13.3.3 自动化运维脚本生成

除了查问题，Claude 还可以帮你写脚本。

**User**: “编写一个 Python 脚本，每天凌晨 3 点备份 `user-db`，并将备份文件上传到 S3。使用 `boto3` 库。”

Claude 会生成完整的脚本，甚至帮你写好 Crontab 配置。

## 小结

通过将 Claude 集成到运维体系中，我们实现了：
1.  **ChatOps**: 用自然语言执行复杂的运维指令。
2.  **Context Aware**: Claude 能结合代码库（它知道错误代码的含义）和运行时日志（它看到实际发生了什么）进行综合诊断。
3.  **Safety**: 通过 MCP 的权限控制，确保操作都在安全边界内。

下一章，我们将挑战软件工程中最困难的领域：**遗留系统重构**。
