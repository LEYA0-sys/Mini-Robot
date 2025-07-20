# mcp_server_sse.py - 基于 SSE 传输的 MCP 服务器
# ================================================
# 
# 这是一个使用 Server-Sent Events (SSE) 传输的 MCP 服务器
# 基于 mcp_server_stdio.py 的功能，使用 FastMCP 和 SSE 传输实现
# 
# 本服务器特性：
# 1. 完整的 MCP 功能支持（工具、提示、资源）
# 2. 使用 SSE 传输方式，支持 Web 客户端连接
# 3. 优雅的错误处理和编码问题解决
# 4. 详细的开发指导注释
# 5. 生产环境就绪的代码结构
#
# 使用方法：
# python mcp_server_sse.py
# 服务器将在 HTTP 上运行，支持 SSE 连接

import argparse
import sys
import logging
import datetime
import os
import math
import random
import uvicorn
from typing import Any, Dict, List, Optional
from pathlib import Path

# MCP 相关导入 - 使用 FastMCP
from mcp.server.fastmcp import FastMCP

# ==========================================
# 1. 系统配置和编码问题处理
# ==========================================

# 修复 Windows 控制台的 UTF-8 编码问题
if sys.platform == 'win32':
    try:
        sys.stderr.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)
logger = logging.getLogger('MCPServerSSE')

# ==========================================
# 2. 服务器配置
# ==========================================

# 服务器基本信息配置
SERVER_NAME = "mcp-server-sse-template"
SERVER_VERSION = "1.0.0"
SERVER_DESCRIPTION = "A comprehensive MCP server template using SSE transport"

# 创建 FastMCP 服务器实例
# json_response=True: 使用 JSON 响应而不是 SSE 流（用于 SSE 传输）
# stateless_http=True: 使用无状态模式（用于 SSE 传输）
mcp = FastMCP(name=SERVER_NAME, json_response=True, stateless_http=True)

# ==========================================
# 3. 工具 (Tools) 实现
# ==========================================

@mcp.tool()
async def calculate(expression: str) -> str:
    """
    Execute mathematical expressions safely
    
    Args:
        expression: Mathematical expression to evaluate (e.g., '2 + 3 * 4', 'math.sqrt(16)')
    """
    try:
        # 安全的数学计算，只允许使用 math 模块
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
        analysis_type: Type of analysis to perform ("length", "words", "lines", "all")
    """
    try:
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
    except Exception as e:
        return f"文本分析错误: {str(e)}"

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
    try:
        result = a + b
        return f"计算结果: {a} + {b} = {result}"
    except Exception as e:
        return f"加法计算错误: {str(e)}"

@mcp.tool()
async def calculate_multiply(a: float, b: float) -> str:
    """
    Multiply two numbers
    
    Args:
        a: First number
        b: Second number
    """
    try:
        result = a * b
        return f"计算结果: {a} × {b} = {result}"
    except Exception as e:
        return f"乘法计算错误: {str(e)}"

@mcp.tool()
async def string_length(text: str) -> str:
    """
    Get the length of a string
    
    Args:
        text: Input string
    """
    try:
        length = len(text)
        return f"字符串 '{text}' 的长度为: {length}"
    except Exception as e:
        return f"字符串长度计算错误: {str(e)}"

@mcp.tool()
async def reverse_string(text: str) -> str:
    """
    Reverse a string
    
    Args:
        text: String to reverse
    """
    try:
        reversed_text = text[::-1]
        return f"原字符串: '{text}'\n反转后: '{reversed_text}'"
    except Exception as e:
        return f"字符串反转错误: {str(e)}"

# ==========================================
# 4. 提示模板 (Prompts) 实现
# ==========================================

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

# ==========================================
# 5. 资源 (Resources) 实现
# ==========================================

@mcp.resource("file://./logs/server.log")
async def get_server_logs() -> str:
    """Get server logs"""
    log_file = "./logs/server.log"
    try:
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # 创建示例日志内容
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return f"""[{current_time}] INFO: MCP SSE 服务器启动
[{current_time}] INFO: 已注册 7 个工具
[{current_time}] INFO: 已注册 5 个提示模板
[{current_time}] INFO: 已注册 3 个资源
[{current_time}] INFO: 服务器运行正常
[{current_time}] NOTE: 这是示例日志内容"""
    except Exception as e:
        return f"读取日志文件错误: {str(e)}"

@mcp.resource("file://./config/server_config.json")
async def get_server_config() -> str:
    """Get server configuration"""
    config_file = "./config/server_config.json"
    try:
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # 创建示例配置内容
            return f"""{{
    "server_name": "{SERVER_NAME}",
    "server_version": "{SERVER_VERSION}",
    "description": "{SERVER_DESCRIPTION}",
    "transport": "sse",
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
    except Exception as e:
        return f"读取配置文件错误: {str(e)}"

@mcp.resource("virtual://system-info")
async def get_system_info() -> str:
    """Get system information (virtual resource)"""
    try:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"""MCP SSE 服务器系统信息
=====================
服务器名称: {SERVER_NAME}
版本: {SERVER_VERSION}
描述: {SERVER_DESCRIPTION}
传输方式: SSE (Server-Sent Events)
当前时间: {current_time}
Python 版本: {sys.version}
平台: {sys.platform}
工作目录: {os.getcwd()}
=====================
这是动态生成的虚拟资源"""
    except Exception as e:
        return f"获取系统信息错误: {str(e)}"

# ==========================================
# 6. 辅助函数
# ==========================================

def create_safe_environment():
    """
    创建安全的执行环境（用于工具开发参考）
    """
    return {
        "math": math,
        "random": random,
        "datetime": datetime,
        "__builtins__": {}  # 禁用危险的内置函数
    }

def ensure_directories():
    """确保必要的目录存在"""
    os.makedirs("./logs", exist_ok=True)
    os.makedirs("./config", exist_ok=True)

# ==========================================
# 7. 程序入口点
# ==========================================

def main():
    """
    主程序入口
    
    使用说明：
    1. 运行服务器：python mcp_server_sse.py --port 8124
    2. 服务器将启动并监听 SSE 连接
    3. 客户端可以通过 HTTP 连接到服务器
    4. 支持所有 MCP 功能：工具、提示、资源
    
    功能特性：
    - 7 个实用工具（数学计算、文本分析、文件操作等）
    - 5 个提示模板（代码审查、文档生成、错误分析等）
    - 3 个资源（日志、配置、系统信息）
    - 基于 SSE 的实时通信
    """
    parser = argparse.ArgumentParser(description="Run MCP SSE based server")
    parser.add_argument("--port", type=int, default=8124, help="Localhost port to listen on")
    args = parser.parse_args()
    
    try:
        logger.info(f"启动 MCP SSE 服务器: {SERVER_NAME} v{SERVER_VERSION}")
        logger.info(f"服务器描述: {SERVER_DESCRIPTION}")
        logger.info("传输方式: SSE (Server-Sent Events)")
        logger.info(f"监听端口: {args.port}")
        
        # 创建必要的目录
        ensure_directories()
        
        logger.info("服务器配置完成，开始运行...")
        logger.info("可用工具: calculate, text_analyzer, file_info, calculate_sum, calculate_multiply, string_length, reverse_string")
        logger.info("可用提示: code_review, documentation, error_analysis, git_commit, explain_code")
        logger.info("可用资源: server_logs, server_config, system_info")
        
        # 使用 SSE 传输运行服务器
        uvicorn.run(mcp.sse_app, host="localhost", port=args.port)
        
    except KeyboardInterrupt:
        logger.info("服务器被用户中断")
    except Exception as e:
        logger.error(f"服务器启动失败: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    """
    程序入口点
    
    开发者使用说明：
    1. 本文件是完整的 MCP SSE 服务器实现
    2. 基于 mcp_server_stdio.py 的功能，使用 SSE 传输
    3. 支持 Web 客户端和其他 HTTP 客户端连接
    4. 提供丰富的工具、提示和资源功能
    
    测试建议：
    - 运行服务器后，可以使用支持 SSE 的 MCP 客户端连接
    - 测试各个工具的响应和功能
    - 验证提示模板的生成效果
    - 检查资源的访问和内容
    """
    main()
