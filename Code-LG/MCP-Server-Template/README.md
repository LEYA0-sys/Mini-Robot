# MCP 服务器模板 - 装饰器版本

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![MCP Version](https://img.shields.io/badge/MCP-1.12.0+-green.svg)](https://github.com/modelcontextprotocol)
[![License](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

> **📢 重要声明**  
> 本项目由学生作者在学习和实践 MCP 协议过程中开发完成。项目中的注释和文档主要由 AI 辅助生成，虽然代码功能已经过验证可以正常运行，但注释内容可能存在不准确之处。如发现任何问题或改进建议，欢迎通过 Issues 指出，我们将及时修正。感谢您的理解与支持！

这个项目包含了三种不同传输方式的 MCP (Model Context Protocol) 服务器模板，全部使用 **FastMCP 装饰器** 实现，为开发者提供了完整的 MCP 服务器开发示例和最佳实践。

## 📚 目录

- [🌟 特性](#-特性)
- [🚀 快速开始](#-快速开始)
- [📦 项目结构](#-项目结构)
- [📁 文件说明](#-文件说明)
- [✨ 功能示例](#-功能示例)
- [🎯 适用场景](#-适用场景)
- [🏗️ 开发指南](#️-开发指南)
- [📦 依赖说明](#-依赖说明)
- [🔧 故障排除](#-故障排除)
- [🤝 贡献指南](#-贡献指南)
- [📄 许可证](#-许可证)
- [📚 参考资源](#-参考资源)
- [🙏 致谢](#-致谢)
- [📞 联系方式](#-联系方式)

## 🌟 特性

- 🚀 **三种传输方式**: STDIO、SSE、Streamable HTTP
- 🎯 **装饰器实现**: 使用 FastMCP 装饰器，代码简洁易懂
- 🛠️ **丰富示例**: 7 个工具、5 个提示模板、3 个资源示例
- 📝 **详细文档**: 完整的使用说明和开发指南
- 🔧 **开箱即用**: 包含完整的依赖管理和配置文件
- 🐛 **错误处理**: 完善的异常处理和日志记录

## � 项目结构

```
MCP-Server/
├── mcp_server_stdio.py          # STDIO 传输服务器
├── mcp_server_sse.py            # SSE 传输服务器
├── mcp_server_streamable_http.py # HTTP 流式传输服务器
├── pyproject.toml               # uv 项目配置
├── requirements.txt             # 依赖列表
├── uv.lock                      # 依赖锁定文件
├── README.md                    # 项目文档
├── LICENSE                      # 许可证文件
├── config/                      # 配置文件目录
└── logs/                        # 日志文件目录
```

## 🀽 文件说明

### 主要服务器文件

1. **`mcp_server_stdio.py`** - STDIO 传输版本

   - 使用标准输入输出进行通信
   - 适合命令行工具和进程间通信

2. **`mcp_server_sse.py`** - SSE 传输版本

   - 使用 Server-Sent Events 进行通信
   - 适合 Web 客户端和实时通信

3. **`mcp_server_streamable_http.py`** - Streamable HTTP 传输版本

   - 使用 HTTP 流式传输进行通信
   - 适合高性能 Web 应用

## ✨ 功能示例

### 🛠️ 工具 (Tools)

所有服务器都提供以下 7 个工具：

1. **`calculate`** - 数学表达式计算
2. **`text_analyzer`** - 文本分析统计
3. **`file_info`** - 获取文件信息
4. **`calculate_sum`** - 两数相加
5. **`calculate_multiply`** - 两数相乘
6. **`string_length`** - 获取字符串长度
7. **`reverse_string`** - 字符串反转

### 📝 提示模板 (Prompts)

所有服务器都提供以下 5 个提示模板：

1. **`code_review`** - 生成代码审查提示
2. **`documentation`** - 生成代码文档提示
3. **`error_analysis`** - 错误分析提示
4. **`git_commit`** - Git 提交消息生成
5. **`explain_code`** - 代码解释提示

### 📂 资源 (Resources)

所有服务器都提供以下 3 个资源：

1. **`file://logs/server.log`** - 服务器日志
2. **`file://config/server_config.json`** - 服务器配置
3. **`virtual://system-info`** - 系统信息（虚拟资源）

## � 快速开始

### 环境要求

- Python 3.12+
- uv (推荐) 或 pip

### 安装依赖

```bash
# 使用 uv (推荐)
uv sync

# 或使用 pip
pip install -r requirements.txt
```

### 运行服务器

```bash
# STDIO 版本
uv run .\mcp_server_stdio.py

# SSE 版本
python mcp_server_sse.py
npx -y @modelcontextprotocol/inspector uv run '.\mcp_server_sse.py'

# Streamable HTTP 版本
python mcp_server_streamable_http.py
npx -y @modelcontextprotocol/inspector uv run '.\mcp_server_streamable_http.py'
```

### 使用 MCP Inspector 测试

```bash
# 启动 Inspector 连接 STDIO 服务器
npx -y @modelcontextprotocol/inspector uv run '.\mcp_server_stdio.py'

# 启动 Inspector 连接 SSE 服务器
npx -y @modelcontextprotocol/inspector uv run '.\mcp_server_sse.py'

# 启动 Inspector 连接 HTTP 服务器
npx -y @modelcontextprotocol/inspector uv run '.\mcp_server_streamable_http.py'
```

## 🏗️ 开发指南

### 添加新工具

```python
@mcp.tool()
async def your_new_tool(param1: str, param2: int = 10) -> str:
    """
    工具描述

    Args:
        param1: 参数描述
        param2: 可选参数，默认值为 10
    """
    # 工具实现逻辑
    return f"处理结果: {param1}, {param2}"
```

### 添加新提示

```python
@mcp.prompt()
async def your_new_prompt(content: str, style: str = "default") -> str:
    """
    提示描述

    Args:
        content: 内容参数
        style: 样式参数
    """
    return f"为以下内容生成{style}风格的提示：\n{content}"
```

### 添加新资源

```python
@mcp.resource("your://custom-resource")
async def your_new_resource() -> str:
    """
    资源描述
    """
    return "你的资源内容"
```

## 🎯 适用场景

- **STDIO**: 命令行工具、进程间通信、开发调试
- **SSE**: Web 应用、实时通信、浏览器客户端
- **Streamable HTTP**: 高性能应用、微服务架构、生产环境

## 📦 依赖说明

### 核心依赖

- `mcp>=1.12.0` - Model Context Protocol 核心库
- `pydantic>=2.11.7` - 数据验证和序列化
- `fastapi>=0.116.1` - Web 框架 (SSE 服务器)
- `websockets>=15.0.1` - WebSocket 支持
- `python-dotenv>=1.1.1` - 环境变量管理

完整依赖列表详见 [`requirements.txt`](requirements.txt) 和 [`pyproject.toml`](pyproject.toml)。

## 🔧 故障排除

### STDIO 服务器问题

如果遇到 "Already running asyncio in this thread" 错误：

- ✅ **已修复**: 现在使用同步的 `mcp.run()` 方法，不再有事件循环冲突
- 确保使用最新版本的代码

### 端口占用问题

如果 SSE 或 HTTP 服务器启动失败：

```bash
# 检查端口是否被占用
netstat -ano | findstr :8124  # 检查 SSE 端口
netstat -ano | findstr :8123  # 检查 HTTP 端口

# 使用不同端口启动
python mcp_server_sse.py --port 8125
python mcp_server_streamable_http.py --port 8124
```

## 🤝 贡献指南

我们欢迎社区贡献！请遵循以下指南：

### 开发流程

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 基于现有模板创建新功能
4. 使用装饰器方式保持代码简洁
5. 添加详细的文档字符串
6. 确保错误处理完善
7. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
8. 推送到分支 (`git push origin feature/AmazingFeature`)
9. 创建 Pull Request

### 代码规范

- 遵循 PEP 8 编码规范
- 使用类型注解
- 编写单元测试
- 保持代码覆盖率

## 📄 许可证

本项目采用 [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可证。

**简单说明：**

- ✅ **可以**: 分享、修改、用于个人学习和研究
- ❌ **不可以**: 商业使用
- 📋 **要求**: 署名原作者、相同许可证发布衍生作品

详细许可条款请查看 [LICENSE](LICENSE) 文件。

## � 参考资源

本项目在开发过程中参考了以下优秀的资源和项目：

### Github 仓库

- 📖 [Model Context Protocol 官方介绍](https://modelcontextprotocol.io/introduction) - MCP 协议官方文档
- 🐙 [MCP 计算器示例](https://github.com/78/mcp-calculator) - MCP 工具实现参考
- 🌊 [MCP Streamable HTTP 实现](https://github.com/invariantlabs-ai/mcp-streamable-http/commits/main/) - HTTP 流式传输参考

### 学习资料

- 📝 [MCP 开发实践博客](https://ccnphfhqs21z.feishu.cn/wiki/HiPEwZ37XiitnwktX13cEM5KnSb) - 详细的开发指南和实践经验
- 🎥 [MCP 视频教程](https://www.bilibili.com/video/BV1fdMgzPEAk/?spm_id_from=333.788.videopod.episodes&vd_source=2f758a08e066db2801f9d6bece289ee7&p=14) - B 站视频教程

## 📞 联系方式

- 🐛 报告问题: [GitHub Issues](https://github.com/your-username/MCP-Server/issues)
- 💡 功能建议: [GitHub Discussions](https://github.com/your-username/MCP-Server/discussions)

---

⭐ 如果这个项目对你有帮助，请给个 Star！
