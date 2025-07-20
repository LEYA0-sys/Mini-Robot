# 贡献指南

感谢你对 MCP-Server 项目的兴趣！我们欢迎所有形式的贡献，包括但不限于：

- 🐛 报告 Bug
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交代码修复或新功能
- 📖 分享使用经验

## 🚀 开始贡献

### 1. 环境准备

```bash
# 克隆仓库
git clone https://github.com/your-username/MCP-Server.git
cd MCP-Server

# 安装依赖
uv sync
# 或者
pip install -r requirements.txt
```

### 2. 开发流程

1. **Fork 仓库** - 点击页面右上角的 Fork 按钮
2. **创建分支** - 为你的功能创建一个新分支
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **开发代码** - 遵循项目的代码规范
4. **测试代码** - 确保你的代码能正常工作
5. **提交代码** - 使用清晰的提交信息
   ```bash
   git commit -m "feat: add amazing new feature"
   ```
6. **推送分支** - 推送到你的 Fork 仓库
   ```bash
   git push origin feature/your-feature-name
   ```
7. **创建 PR** - 在 GitHub 上创建 Pull Request

## 📝 代码规范

### Python 代码规范

- 遵循 [PEP 8](https://pep8.org/) 编码规范
- 使用类型注解
- 函数和类必须有文档字符串
- 变量和函数名使用 snake_case
- 类名使用 PascalCase

### 示例代码

```python
@mcp.tool()
async def your_tool(param1: str, param2: int = 10) -> str:
    """
    工具的简短描述

    Args:
        param1: 第一个参数的描述
        param2: 第二个参数的描述，默认值为 10

    Returns:
        处理结果的描述

    Raises:
        ValueError: 当参数无效时抛出
    """
    if not param1:
        raise ValueError("param1 不能为空")

    # 业务逻辑
    result = f"处理 {param1} 与 {param2}"
    return result
```

### 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 格式：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建工具或辅助工具的变动

示例：

```
feat: add new text analysis tool
fix: resolve STDIO server startup issue
docs: update installation instructions
```

## 🧪 测试

### 运行测试

```bash
# 运行所有服务器测试
python mcp_server_stdio.py &
python mcp_server_sse.py &
python mcp_server_streamable_http.py &

# 使用 MCP Inspector 测试
npx -y @modelcontextprotocol/inspector uv run './mcp_server_sse.py'
```

### 添加新功能测试

当你添加新的工具、提示或资源时，请确保：

1. 功能能正常工作
2. 错误处理得当
3. 文档字符串完整
4. 与现有功能兼容

## 📋 Issue 规范

### Bug 报告

使用以下模板报告 Bug：

```markdown
**描述问题**
简要描述遇到的问题

**重现步骤**

1. 执行 '...'
2. 点击 '....'
3. 滚动到 '....'
4. 看到错误

**期望行为**
描述你期望发生的行为

**实际行为**
描述实际发生的行为

**环境信息**

- 操作系统: [例如 Windows 11]
- Python 版本: [例如 3.12.0]
- MCP 版本: [例如 1.12.0]

**附加信息**
添加任何其他相关的截图或信息
```

### 功能建议

使用以下模板提出功能建议：

```markdown
**功能描述**
简要描述你希望添加的功能

**解决的问题**
这个功能解决了什么问题？

**建议的解决方案**
描述你希望如何实现这个功能

**其他方案**
描述你考虑过的其他解决方案

**附加信息**
添加任何其他相关信息或截图
```

## 📞 获取帮助

如果你在贡献过程中遇到问题，可以通过以下方式获取帮助：

- 📝 [GitHub Issues](https://github.com/your-username/MCP-Server/issues) - 报告问题
- 💬 [GitHub Discussions](https://github.com/your-username/MCP-Server/discussions) - 讨论和提问

## 🙏 行为准则

参与本项目时，请遵循以下原则：

- 保持友善和尊重
- 欢迎不同观点和经验
- 接受建设性批评
- 专注于对社区最有利的事情
- 对其他社区成员表示同理心

## 📄 许可证

通过贡献代码，你同意你的贡献将在 [CC BY-NC-SA 4.0](LICENSE) 许可证下发布。

---

再次感谢你的贡献！🎉
