## 插件系统与MCP服务的关系
通过分析代码，我发现 插件系统 和 MCP服务 是两套不同但互补的功能扩展机制：

### 插件系统（Server Plugins）
实现机制：

- 基于Python装饰器的本地插件系统
- 使用 `register_function` 装饰器注册函数到 all_function_registry
- 插件文件位于 `plugins_func/functions` 目录
- 通过 `auto_import_modules` 自动加载所有插件模块
功能特点：

- 支持多种工具类型： SYSTEM_CTL （系统控制）、 IOT_CTL （IoT设备控制）、 WAIT （等待返回）、 CHANGE_SYS_PROMPT （角色切换）等
- 内置功能包括：天气查询、时间查询、角色切换、Home Assistant集成、音乐播放等
- 由 `ServerPluginExecutor` 执行
### MCP服务（Model Context Protocol）
实现机制：

- 基于标准MCP协议的外部服务集成
- 支持三种接入方式：
  - Server MCP ：通过 data/.mcp_server_settings.json 配置的外部MCP服务
  - Device MCP ：ESP32设备通过WebSocket连接提供的工具
  - MCP Endpoint ：独立的WebSocket MCP服务
  技术特点：

- 遵循MCP 2024-11-05协议标准
- 支持stdio和SSE连接模式
- 动态工具发现和注册
- 具备错误重试和重连机制
### 核心区别
特性 插件系统 MCP服务 部署方式 本地Python模块 外部独立服务 协议标准 自定义装饰器 标准MCP协议 扩展性 需要重启服务 动态加载 语言支持 仅Python 任意语言 连接方式 直接函数调用 WebSocket/stdio/SSE 配置管理 代码内配置 外部配置文件

### 统一管理
两套系统通过 `UnifiedToolHandler` 进行统一管理，为LLM提供一致的工具调用接口。这种设计既保证了核心功能的稳定性（插件系统），又提供了灵活的扩展能力（MCP服务）。

总结： 插件系统适合核心功能的快速开发，MCP服务适合第三方集成和动态扩展，两者共同构成了完整的功能扩展生态。