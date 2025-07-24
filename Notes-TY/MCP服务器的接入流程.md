## MCP服务器的接入流程
xiaozhi-esp32-server系统支持三种类型的MCP服务器接入方式：

### 1. 服务端MCP (Server MCP)
配置文件 ： `mcp_server_settings.json`

接入流程 ：

1. 
   配置文件准备 ：在 data/.mcp_server_settings.json 中配置MCP服务
   - 支持 stdio 模式（通过命令行启动）
   - 支持 sse 模式（通过HTTP SSE连接）
   - 配置示例包括文件系统、playwright、Home Assistant等服务
2. 
   初始化过程 ：
   - `ServerMCPManager` 负责管理多个MCP服务
   - `load_config` 加载配置文件
   - `initialize_servers` 初始化所有配置的MCP服务
3. 
   连接建立 ：
   - `ServerMCPClient` 处理单个MCP服务连接
   - 支持stdio和SSE两种连接方式
   - 自动获取工具列表并注册到系统中
### 2. 设备端MCP (Device MCP)
接入流程 ：

1. 
   WebSocket连接 ：ESP32设备通过WebSocket与xiaozhi-server建立连接
2. 
   MCP协议握手 ：
   - 发送初始化消息（ `send_mcp_initialize_message` ）
   - 交换工具列表
   - 建立双向通信通道
3. 3.
   工具注册 ：设备端的MCP工具会自动注册到系统的工具列表中
### 3. MCP接入点 (MCP Endpoint)
接入流程 ：

1. 
   部署MCP接入点服务 ：独立的WebSocket服务，提供MCP协议接入能力
2. 
   配置连接 ：在xiaozhi-server配置中设置MCP接入点URL
3. 
   动态工具扩展 ：
   - 第三方MCP服务通过接入点连接到系统
   - 支持运行时动态添加/移除工具
   - 适合扩展自定义功能（如计算器、文件操作等）
### 核心技术实现
统一工具处理 ：

- `UnifiedToolHandler` 统一管理所有类型的工具
- 每种MCP类型都有对应的执行器（Executor）
- 支持工具的自动发现、注册和调用
错误处理和重连 ：

- 内置重试机制，连接失败时自动重连
- 支持工具调用的超时处理
- 完善的日志记录和错误追踪
协议支持 ：

- 完全兼容MCP 2024-11-05协议规范
- 支持工具调用、结果返回、错误处理
- 支持视觉功能扩展（通过vision参数）
这种多层次的MCP接入架构使得xiaozhi-esp32-server能够灵活地集成各种AI工具和服务，既支持本地部署的服务，也支持远程的云端服务，还支持设备端的原生功能扩展。