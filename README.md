# AI-Crawler-Accessibility-Testing

Tool for Fast Detection of Website/Server AI Crawler/Spider/Robots Blocking Policies (Not robots.txt)

一个快速检测网站/服务器对AI爬虫/蜘蛛/机器人阻止策略的工具（非robots.txt检测）

## 🌟 Features 功能特性

- ✅ **多线程并发测试** - 支持1-50个并发线程，大幅提升测试速度
- 🕷️ **全面的AI爬虫检测** - 测试30+种主流AI爬虫User-Agent
- 🌐 **灵活的代理支持** - 支持系统代理、自定义代理或无代理模式
- 📊 **详细的结果分析** - 提供状态码分类、错误统计等详细报告
- 💻 **交互式界面** - 友好的命令行交互界面
- 🔄 **实时进度显示** - 实时显示测试进度和结果

## 📋 Requirements 系统要求

- Python 3.6+
- requests库

## 🚀 Installation 安装

1. 克隆或下载此项目到本地
```bash
git clone https://github.com/your-username/AI-Crawler-Accessibility-Testing.git
cd AI-Crawler-Accessibility-Testing
```

2. 安装依赖
```bash
pip install requests
```

## 📖 Usage 使用方法

### 交互式模式（推荐）
```bash
python ai-crawler-accessibility-testing.py
```

然后按照提示输入：
- 目标域名或URL
- 代理设置（系统代理/自定义代理/无代理）
- 并发线程数（1-50，默认10）

### 命令行模式
```bash
python ai-crawler-accessibility-testing.py https://example.com
```

## 🎯 Example Output 示例输出

```
AI爬虫可访问性测试工具
========================================
请输入要测试的目标域名或URL: example.com

代理设置选项:
1. 不使用代理
2. 使用系统代理
3. 自定义代理
请选择代理选项 (1-3，默认为2): 1

请输入并发线程数 (1-50，默认10): 20

开始测试目标: https://example.com
不使用代理
并发线程数: 20
--------------------------------------------------

待测试的 User-Agent (32 个):
 1. ChatGPT-User
 2. Claude-Web
 3. GPTBot
 ...

开始并发测试 (并发数: 20)...
--------------------------------------------------
[  1/ 32] User-Agent: ChatGPT-User, HTTP 状态码: 200
[  2/ 32] User-Agent: Claude-Web, HTTP 状态码: 403
[  3/ 32] User-Agent: GPTBot, HTTP 状态码: 403
...

============================================================
测试完成！统计结果:
总测试数量: 32
正常访问: 18
被拒绝/出错: 14

被拒绝访问或出错的 User-Agent:
 1. Claude-Web
 2. GPTBot
 3. Bard
 ...
```

## 📊 Test Results Analysis 测试结果分析

工具会检测以下状态：
- **200 OK** - 正常访问，网站允许此AI爬虫
- **403 Forbidden** - 被拒绝访问，网站阻止此AI爬虫
- **404 Not Found** - 页面不存在
- **超时/网络错误** - 连接问题

## 🤖 Supported AI Crawlers 支持的AI爬虫

本工具测试以下AI爬虫的可访问性：
- ChatGPT-User
- Claude-Web
- GPTBot
- Bard
- BingBot
- FacebookBot
- Google-Extended
- PerplexityBot
- 等30+种主流AI爬虫...

完整列表来源：[ai-robots-txt](https://github.com/ai-robots-txt/ai.robots.txt)

## ⚙️ Configuration Options 配置选项

### 代理设置
1. **不使用代理** - 直接连接
2. **系统代理** - 自动检测并使用系统代理设置
3. **自定义代理** - 手动指定本地代理端口（如Clash、V2Ray等）

### 并发设置
- 并发线程数范围：1-50
- 推荐设置：10-20（避免对目标服务器造成过大压力）
- 默认值：10

## 🔍 Use Cases 使用场景

- **网站管理员** - 检测自己网站的AI爬虫阻止策略是否生效
- **SEO专家** - 了解搜索引擎和AI爬虫的访问情况
- **开发者** - 测试爬虫脚本的可行性
- **安全研究** - 分析网站的反爬虫机制

## ⚠️ Notes 注意事项

- 请合理设置并发数，避免对目标服务器造成过大压力
- 某些网站可能有IP限制，高并发可能导致IP被暂时封禁
- 本工具仅用于测试目的，请遵守目标网站的使用条款
- 建议在测试前先查看目标网站的robots.txt文件

## 🤝 Contributing 贡献

欢迎提交Issue和Pull Request来改进这个工具！

## 📄 License 许可证

[MIT License](LICENSE)

## 🙏 Acknowledgments 致谢

- AI Crawler列表来源：[ai-robots-txt](https://github.com/ai-robots-txt/ai.robots.txt)
- 策划：JerryZhi
- 开发：Gemini Advanced 2.0 Flash & Copilot@Claude Sonnet 4

## 📧 Contact 联系

如有问题或建议，请通过Issue联系我们。


