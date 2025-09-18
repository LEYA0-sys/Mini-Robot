# screen用法

开启API、WEB、SERVER服务

```python
cd /home/ubuntu/prjs/xiaozhi-esp32-server/main/manager-api
screen -L -Logfile ~/manager_api.log -dmS manager_api mvn spring-boot:run
cd /home/ubuntu/prjs/xiaozhi-esp32-server/main/manager-web
screen -L -Logfile ~/manager_web.log -dmS manager_web npm run serve 
cd /home/ubuntu/prjs/xiaozhi-esp32-server/main/xiaozhi-server
conda activate xiaozhi-esp32-server
screen -L -Logfile ~/xiaozhi_server.log -dmS xiaozhi_server python app.py 
```

# 连接 [readme.md](readme.md) 数据库

```
# 进入容器shell
docker exec -it xiaozhi-esp32-server-db bash

# 在容器内使用本地连接（如MySQL）
mysql -u root -p

#密码：Sztu@xiaozhi
```

# 密钥更新

1.用户在注册界面添加密钥

2.说话时检测到的人名与sys_user中的人名进行等值连接，获取密钥

3.更新后的密钥保存在'/home/ubuntu/prjs/xiaozhi-esp32-server/main/xiaozhi-server/data/.env'

```
TENCENT_SECRET_ID=AKIDxlOtDKEnERSTUH4iCVYQ7ase3FEyUmph
TENCENT_SECRET_KEY=mLjtqZ4OX5RZT9crBLLBnIaeU7UmwY8Z
TENCENT_DEFAULT_REGION=ap-nanjing
Bucket=nanjin-xiaozhi-1333445595 #存储桶
QWEN_API_KEY=sk-007041782a294808a9e164562d0998fd #阿里云LLM密钥
```



# 数据分析智能体

```
# 1. 运行 ai-data-audit
cd /home/ubuntu/prjs/ai-data-audit
python run_event_log_agent.py {log_path} analyzed --ai
python build_vector_kb_offline.py

# 2. 运行 ai-data-event  
cd /home/ubuntu/prjs/ai-data-event
python run_event_log_agent.py {log_path} analyzed --ai
python build_vector_kb_offline.py

# 3. 运行 ai-data-yewu
cd /home/ubuntu/prjs/ai-data-yewu
python run_event_log_agent.py {log_path} analyzed --ai
python build_vector_kb_offline.py

{log_path}参考/home/ubuntu/prjs/cos-mcp/downloads/logs/audit/2025-08-12

LLM密钥保存在/home/ubuntu/prjs/ai-data-audit/ai_data_science_team/agents/.env，使用的是qwen-turbo,如果额度用完了需要更换三个智能体中的模型，在/home/ubuntu/prjs/ai-data-audit/ai_data_science_team/agents/event_log_agent.py修改


```

> [!IMPORTANT]
>
> 均在base环境下执行



# 编排器

```
编排器文件路径
用于每天早上调度，下载前一天的所有日志/home/ubuntu/prjs/xiaozhi-esp32-server/main/xiaozhi-server/plugins_func/functions/log_analysis_orchestrator.py
用户工作时间随时下载最新时刻的日志/home/ubuntu/prjs/xiaozhi-esp32-server/main/xiaozhi-server/plugins_func/functions/log_analysis_orchestrator——latest.py


调度器路径
/home/ubuntu/prjs/xiaozhi-esp32-server/main/xiaozhi-server/plugins_func/functions/schedule_log_analysis.py
```



```
1.调用COS桶下载文件，路径
/home/ubuntu/prjs/cos-mcp/downloads/logs/audit/2025-08-11
2.调用智能体进行数据分析+构建向量知识库，分别保存在
/home/ubuntu/prjs/ai-data-audit/analyzed
/home/ubuntu/prjs/ai-data-audit/vector_kb
3.LLM总结文件保存在
/home/ubuntu/prjs/xiaozhi-esp32-server/analysis_results/2025-08-07/llm_summary.txt
```



## 手动触发编排器

```
cd /home/ubuntu/prjs/xiaozhi-esp32-server/main/xiaozhi-server
conda activate xiaozhi-esp32-server
/home/ubuntu/miniconda3/envs/xiaozhi-esp32-server/bin/python -m plugins_func.functions.schedule_log_analysis --manual
```

日志可见/home/ubuntu/prjs/xiaozhi-esp32-server/main/xiaozhi-server/tmp/server.log

## 定时任务触发编排器



```
- `sudo systemctl status log-analysis-scheduler` - 查看服务状态
- `sudo systemctl restart log-analysis-scheduler` - 重启服务
- `sudo systemctl stop log-analysis-scheduler` - 停止服务
- `sudo journalctl -u log-analysis-scheduler` - 查看服务日志
- `systemctl enable` - 设置服务在系统启动时自动启动
- `systemctl disable` - 取消服务的开机自启动
```

# MCP工具调用

## 开始播报日志

## 调度日志分析编排器

# webhook接口

 http://0.0.0.0:8003/webhook/alert/rag

```
##测试接口是否开通
# 测试RAG告警接口
curl -X GET http://localhost:8003/webhook/alert/rag

# 测试POST请求
curl -X POST http://localhost:8003/webhook/alert/rag \
  -H "Content-Type: application/json" \
  -d '{
    "alarmPolicyName": "CPU使用率过高",
    "alarmStatus": "ALARM",
    "alarmType": "metric",
    "instanceId": "ins-12345678",
    "region": "ap-nanjing",
    "alarmContent": "CPU使用率超过80%",
    "metricName": "CPUUtilization",
    "threshold": "80",
    "currentValue": "85.6"
  }'
```

设置镜像源：export HF_ENDPOINT=https://hf-mirror.com

# 重启docker容器

```
docker start xiaozhi-esp32-server-redis
docker start xiaozhi-esp32-server-db
```

若重启服务器，需要systemctl stop mysql

# 新文件路径

```
(xiaozhi-esp32-server) ubuntu@VM-0-15-ubuntu:~/prjs/xiaozhi-esp32-server/main/xiaozhi-server$    python scripts/quick_start.py --skip-deps
============================================================
🚀 告警分析系统快速启动
============================================================

设置目录结构...
✓ 创建目录: /home/ubuntu/prjs/alert-analysis
✓ 创建目录: /home/ubuntu/prjs/alert-analysis/daily/2025-08-28
✓ 创建目录: /home/ubuntu/prjs/alert-analysis/alerts/2025-08-28
✓ 创建目录: /home/ubuntu/prjs/alert-analysis/broadcast/2025-08-28
✓ 创建目录: /home/ubuntu/prjs/alert-analysis/rag/2025-08-28
✓ 创建目录: /home/ubuntu/prjs/alert-analysis/vector-db
✓ 创建目录: /home/ubuntu/prjs/alert-analysis/cache
✓ 创建目录: /home/ubuntu/prjs/alert-analysis/temp
✓ 创建目录: /home/ubuntu/prjs/alert-analysis/logs

检查权限...
✓ 目录 /home/ubuntu/prjs/alert-analysis 可写

优化系统设置...
✓ 性能配置已优化

测试基本功能...
✓ 路径配置正常
  每日分析: /home/ubuntu/prjs/alert-analysis/daily/2025-08-28
  告警分析: /home/ubuntu/prjs/alert-analysis/alerts/2025-08-28
  播报文件: /home/ubuntu/prjs/alert-analysis/broadcast/2025-08-28
从API读取配置
✓ 性能监控正常 (内存使用: 49.00%)

生成配置文件...
✓ 配置文件已生成: /home/ubuntu/prjs/alert-analysis/system_config.txt

============================================================
🎉 系统设置完成！
============================================================

📁 新文件结构:
   基础目录: /home/ubuntu/prjs/alert-analysis
   每日分析: /home/ubuntu/prjs/alert-analysis/daily/2025-08-28
   告警分析: /home/ubuntu/prjs/alert-analysis/alerts/2025-08-28
   播报文件: /home/ubuntu/prjs/alert-analysis/broadcast/2025-08-28
   向量数据库: /home/ubuntu/prjs/alert-analysis/vector-db

🚀 下一步操作:
   1. 运行路径迁移: python scripts/migrate_paths.py --dry-run
   2. 启动定时任务: python plugins_func/functions/schedule_log_analysis.py
   3. 测试告警处理: 发送测试告警到 /webhook/alert/rag

📊 性能监控:
   - 查看性能日志: tail -f /var/log/xiaozhi-server.log
   - 监控内存使用: 系统会自动记录内存使用情况
   - 缓存统计: 查看缓存命中率和性能指标

🔧 配置调整:
   - 编辑 config/paths.py 调整路径配置
   - 编辑 PerformanceConfig 调整性能参数
   - 使用 @performance_monitor 装饰器监控关键函数

📚 更多信息:
   - 查看文档: docs/PERFORMANCE_OPTIMIZATION.md
   - 迁移帮助: python scripts/migrate_paths.py --help
   - 性能调优: 参考文档中的最佳实践

✅ 系统设置成功完成！

```

