# mcp_server_streamable_http.py - MCP 服务器开发模板 (Streamable HTTP 版本)
# ================================================
# 
# 这是一个基于 Streamable HTTP 的 MCP (Model Context Protocol) 服务器开发模板
# 使用 FastMCP 框架实现，支持 HTTP 传输协议
# 
# 本模板特性：
# 1. 完整的 MCP 功能支持（工具、提示、资源）
# 2. 基于 FastMCP 的简洁实现
# 3. 详细的开发指导注释
# 4. 生产环境就绪的代码结构
# 5. HTTP 传输协议支持
#
# 开发者使用指南：
# - 复制此模板作为新项目的起点
# - 根据注释指引修改相应部分
# - 添加你自己的工具、提示和资源
# - 测试并部署你的 MCP 服务器

import argparse
import sys
import logging
import datetime
import os
from typing import Any, Dict, List, Optional
from pathlib import Path
import uvicorn

# MCP 相关导入
from mcp.server.fastmcp import FastMCP

# ==========================================
# 1. 系统配置和编码问题处理
# ==========================================

# 修复 Windows 控制台的 UTF-8 编码问题
if sys.platform == 'win32':
    try:
        sys.stderr.reconfigure(encoding='utf-8')  # 重新配置错误输出流编码
        sys.stdout.reconfigure(encoding='utf-8')  # 重新配置标准输出流编码
    except AttributeError:
        # 在一些旧版本的 Python 中可能不支持 reconfigure 方法
        pass

# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)  # 输出到标准错误流
    ]
)
logger = logging.getLogger('MCPServerStreamableHTTP')

# ==========================================
# 2. 服务器配置
# ==========================================

# 服务器基本信息配置
# 开发者：修改这些配置以匹配你的项目
SERVER_NAME = "mcp-server-template-http"
SERVER_VERSION = "1.0.0"
SERVER_DESCRIPTION = "A comprehensive MCP server template with Streamable HTTP transport"

# 创建 FastMCP 服务器实例
# json_response=False: 使用 SSE 流响应而不是 JSON
# stateless_http=False: 使用有状态模式，可以跨请求保持状态
mcp = FastMCP(name=SERVER_NAME, json_response=False, stateless_http=False)

# ==========================================
# 3. 工具 (Tools) 实现
# ==========================================

# 开发者指南：如何添加新工具
# 1. 使用 @mcp.tool() 装饰器定义工具
# 2. 函数名即为工具名
# 3. 函数参数自动成为工具参数
# 4. 返回字符串作为工具输出

@mcp.tool()
async def calculate(expression: str) -> str:
    """
    Execute mathematical expressions safely
    
    Args:
        expression: Mathematical expression to evaluate (e.g., '2 + 3 * 4', 'math.sqrt(16)')
    """
    try:
        # 安全的数学计算，只允许使用 math 模块
        import math
        import random
        
        # 限制可用的命名空间，防止执行危险代码
        safe_dict = {
            "math": math,
            "random": random,
            "__builtins__": {}  # 禁用内置函数
        }
        
        result = eval(expression, safe_dict)
        logger.info(f"计算表达式: {expression}, 结果: {result}")
        return f"计算结果: {expression} = {result}"
    except Exception as e:
        return f"计算错误: {str(e)}"

@mcp.tool()
async def text_analyzer(text: str, analysis_type: str = "all") -> str:
    """
    Analyze text and provide statistics
    
    Args:
        text: Text to analyze
        analysis_type: Type of analysis to perform (length/words/lines/all)
    """
    results = []
    
    if analysis_type in ["length", "all"]:
        results.append(f"字符数: {len(text)}")
    
    if analysis_type in ["words", "all"]:
        word_count = len(text.split())
        results.append(f"单词数: {word_count}")
    
    if analysis_type in ["lines", "all"]:
        line_count = len(text.splitlines())
        results.append(f"行数: {line_count}")
    
    return f"文本分析结果:\n" + "\n".join(results)

@mcp.tool()
async def file_info(file_path: str) -> str:
    """
    Get information about a file
    
    Args:
        file_path: Path to the file
    """
    try:
        path = Path(file_path)
        if not path.exists():
            return f"文件不存在: {file_path}"
        
        stat = path.stat()
        info = f"""文件信息:
路径: {path.absolute()}
大小: {stat.st_size} 字节
创建时间: {datetime.datetime.fromtimestamp(stat.st_ctime)}
修改时间: {datetime.datetime.fromtimestamp(stat.st_mtime)}
是否为目录: {'是' if path.is_dir() else '否'}"""
        
        return info
    
    except Exception as e:
        return f"获取文件信息时出错: {str(e)}"

@mcp.tool()
async def calculate_sum(a: float, b: float) -> str:
    """
    Add two numbers together
    
    Args:
        a: First number
        b: Second number
    """
    result = a + b
    return f"计算结果: {a} + {b} = {result}"

@mcp.tool()
async def calculate_multiply(a: float, b: float) -> str:
    """
    Multiply two numbers
    
    Args:
        a: First number
        b: Second number
    """
    result = a * b
    return f"计算结果: {a} × {b} = {result}"

@mcp.tool()
async def string_length(text: str) -> str:
    """
    Get the length of a string
    
    Args:
        text: Input string
    """
    length = len(text)
    return f"字符串 '{text}' 的长度为: {length}"

@mcp.tool()
async def reverse_string(text: str) -> str:
    """
    Reverse a string
    
    Args:
        text: String to reverse
    """
    reversed_text = text[::-1]
    return f"原字符串: '{text}'\n反转后: '{reversed_text}'"

# 开发者：在这里添加更多工具...
# @mcp.tool()
# async def your_tool_name(param1: str, param2: int = 10) -> str:
#     """
#     Your tool description
#     
#     Args:
#         param1: Parameter description
#         param2: Another parameter with default value
#     """
#     # 你的工具逻辑
#     result = f"处理结果: {param1}, {param2}"
#     return result

# ==========================================
# 4. 提示模板 (Prompts) 实现
# ==========================================

# 在 FastMCP 中，提示模板通过 @mcp.prompt() 装饰器定义

@mcp.prompt()
async def code_review(code: str, language: str = "未知语言") -> str:
    """
    Generate a code review prompt
    
    Args:
        code: Code to review
        language: Programming language
    """
    return f"""请对以下 {language} 代码进行详细的代码审查：

代码:
```{language.lower() if language != "未知语言" else ""}
{code}
```

请检查：
1. 代码质量和最佳实践
2. 潜在的错误和安全问题
3. 性能优化建议
4. 代码可读性和维护性
5. 改进建议"""

@mcp.prompt()
async def documentation(code: str, style: str = "google") -> str:
    """
    Generate documentation for code
    
    Args:
        code: Code to document
        style: Documentation style (e.g., 'google', 'numpy', 'sphinx')
    """
    return f"""请为以下代码生成 {style} 风格的文档：

代码:
```
{code}
```

请生成：
1. 函数/类的描述
2. 参数说明
3. 返回值说明
4. 使用示例
5. 注意事项（如有）"""

@mcp.prompt()
async def error_analysis(error_message: str, context: str = "") -> str:
    """
    Analyze and suggest fixes for errors
    
    Args:
        error_message: Error message or stack trace
        context: Additional context about the error
    """
    return f"""请分析以下错误并提供解决方案：

错误信息:
```
{error_message}
```

上下文信息:
{context if context else "无额外上下文"}

请提供：
1. 错误原因分析
2. 具体的解决步骤
3. 预防类似错误的建议
4. 相关的最佳实践"""

@mcp.prompt()
async def git_commit(changes: str) -> str:
    """
    Generate a Git commit message
    
    Args:
        changes: Git diff or description of changes
    """
    return f"为以下更改生成一个简洁但描述性的提交消息：\n\n{changes}"

@mcp.prompt()
async def explain_code(code: str, language: str = "未知") -> str:
    """
    Explain how code works
    
    Args:
        code: Code to explain
        language: Programming language
    """
    return f"解释以下 {language} 代码的工作原理：\n\n{code}"

# 开发者：在这里添加更多提示模板...
# @mcp.prompt()
# async def your_prompt_name(param1: str, param2: str = "default") -> str:
#     """
#     Your prompt description
#     
#     Args:
#         param1: Parameter description
#         param2: Another parameter
#     """
#     return f"Your prompt content with {param1} and {param2}"

# ==========================================
# 5. 资源 (Resources) 实现
# ==========================================

# 在 FastMCP 中，资源通过 @mcp.resource() 装饰器定义

@mcp.resource("file://logs/server.log")
async def server_logs() -> str:
    """
    Server Logs
    服务器运行日志
    """
    log_file = "./logs/server.log"
    
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        # 如果文件不存在，创建一个示例内容
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"""[{current_time}] INFO: MCP 服务器模板启动 (Streamable HTTP)
[{current_time}] INFO: 已注册 7 个工具
[{current_time}] INFO: 已注册 5 个提示模板
[{current_time}] INFO: 已注册 3 个资源
[{current_time}] INFO: HTTP 服务器运行正常
[{current_time}] NOTE: 这是示例日志内容"""

@mcp.resource("file://config/server_config.json")
async def server_configuration() -> str:
    """
    Server Configuration
    服务器配置文件
    """
    config_file = "./config/server_config.json"
    
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return f"""{{
    "server_name": "{SERVER_NAME}",
    "server_version": "{SERVER_VERSION}",
    "description": "{SERVER_DESCRIPTION}",
    "transport": "streamable-http",
    "features": {{
        "tools": true,
        "prompts": true,
        "resources": true
    }},
    "logging": {{
        "level": "INFO",
        "file": "./logs/server.log"
    }},
    "created": "{datetime.datetime.now().isoformat()}",
    "note": "这是示例配置文件"
}}"""

@mcp.resource("virtual://system-info")
async def system_information() -> str:
    """
    System Information
    系统运行信息（虚拟资源）
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""MCP 服务器系统信息 (Streamable HTTP)
=====================
服务器名称: {SERVER_NAME}
版本: {SERVER_VERSION}
描述: {SERVER_DESCRIPTION}
传输协议: Streamable HTTP
当前时间: {current_time}
Python 版本: {sys.version}
平台: {sys.platform}
工作目录: {os.getcwd()}
=====================
这是动态生成的虚拟资源"""

# 开发者：在这里添加更多资源...
# @mcp.resource("your://custom-resource")
# async def your_resource_name() -> str:
#     """
#     Your Resource Name
#     Your resource description
#     """
#     return "Your resource content"

# ==========================================
# 6. 开发者自定义区域
# ==========================================

# 开发者：在这里添加你自己的辅助函数和类

def create_safe_environment():
    """
    创建安全的执行环境（用于工具开发参考）
    """
    import math
    import random
    import datetime
    
    return {
        "math": math,
        "random": random,
        "datetime": datetime,
        "__builtins__": {}  # 禁用危险的内置函数
    }

class ResourceManager:
    """
    资源管理器示例类（可扩展用于复杂的资源管理）
    """
    def __init__(self):
        self.resources = {}
    
    def register_resource(self, uri: str, handler):
        """注册资源处理器"""
        self.resources[uri] = handler
    
    async def get_resource(self, uri: str) -> str:
        """获取资源内容"""
        if uri in self.resources:
            return await self.resources[uri]()
        else:
            raise ValueError(f"资源未找到: {uri}")

# 开发者：实例化你的自定义类
# resource_manager = ResourceManager()

# ==========================================
# 7. 程序入口点
# ==========================================

if __name__ == "__main__":
    """
    程序入口点
    
    开发者使用说明：
    1. 复制此模板文件到你的项目目录
    2. 修改 SERVER_NAME, SERVER_VERSION 等配置
    3. 在相应的区域添加你的工具、提示和资源
    4. 运行服务器：python mcp_server_streamable_http.py --port 8123
    5. 在客户端中连接到 http://localhost:8123
    
    测试建议：
    - 使用 MCP 客户端工具测试各个功能
    - 检查日志输出确保服务器正常运行
    - 验证工具、提示和资源的响应
    - 测试 HTTP 传输协议的稳定性
    """
    parser = argparse.ArgumentParser(description="Run MCP Streamable HTTP based server")
    parser.add_argument("--port", type=int, default=8123, help="Localhost port to listen on")
    args = parser.parse_args()
    
    try:
        logger.info(f"启动 MCP 服务器: {SERVER_NAME} v{SERVER_VERSION}")
        logger.info(f"传输协议: Streamable HTTP")
        logger.info(f"监听端口: {args.port}")
        
        # 可选：创建必要的目录
        os.makedirs("./logs", exist_ok=True)
        os.makedirs("./config", exist_ok=True)
        
        # 使用 Streamable HTTP 传输协议启动服务器
        uvicorn.run(mcp.streamable_http_app, host="localhost", port=args.port)
    
    except KeyboardInterrupt:
        logger.info("服务器被用户中断")
    except Exception as e:
        logger.error(f"服务器启动失败: {str(e)}")
        sys.exit(1)
