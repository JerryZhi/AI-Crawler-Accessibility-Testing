# AI-Crawler-Detector

Fast Detection Tool for Website AI Crawler/Bot/Spider Blocking Policies

## 🌐 Hreflang

[中文文档](README.md) | [English Version](README_EN.md)

## 🌟 Features

- ✅ **Multi-threaded Concurrent Testing** - Supports 1-50 concurrent threads for dramatically improved testing speed
- 🕷️ **Comprehensive AI Crawler Detection** - Tests 30+ mainstream AI crawler User-Agents
- 🌐 **Flexible Proxy Support** - Supports system proxy, custom proxy, or no proxy modes
- 📊 **Detailed Result Analysis** - Provides status code classification, error statistics, and detailed reports
- 💻 **Interactive Interface** - User-friendly command-line interactive interface
- 🔄 **Real-time Progress Display** - Real-time display of testing progress and results

## 📋 Requirements

- Python 3.6+
- requests library

## 🚀 Installation

1. Clone or download this project locally
```bash
git clone https://github.com/JerryZhi/AI-Crawler-Detector.git
cd AI-Crawler-Detector
```

2. Install dependencies
```bash
pip install requests
```

## 📖 Usage

### Interactive Mode (Recommended)
```bash
python ai-crawler-detector-en.py
```

Then follow the prompts to enter:
- Target domain or URL
- Proxy settings (system proxy/custom proxy/no proxy)
- Number of concurrent threads (1-50, default 10)

### Command Line Mode
```bash
python ai-crawler-detector-en.py https://example.com
```

## 🎯 Example Output

```
AI Crawler Accessibility Testing Tool
========================================
Please enter the target domain or URL to test: example.com

Proxy options:
1. No proxy
2. Use system proxy
3. Custom proxy
Please choose proxy option (1-3, default is 2): 1

Please enter number of concurrent threads (1-50, default 10): 20

Starting test on target: https://example.com
Not using proxy
Concurrent threads: 20
--------------------------------------------------

User-Agents to test (32 total):
 1. ChatGPT-User
 2. Claude-Web
 3. GPTBot
 ...

Starting concurrent testing (concurrency: 20)...
--------------------------------------------------
[  1/ 32] User-Agent: ChatGPT-User, HTTP Status: 200
[  2/ 32] User-Agent: Claude-Web, HTTP Status: 403
[  3/ 32] User-Agent: GPTBot, HTTP Status: 403
...

============================================================
Testing completed! Summary:
Total tests: 32
Successful access: 18
Rejected/Error: 14

Rejected or errored User-Agents:
 1. Claude-Web
 2. GPTBot
 3. Bard
 ...
```

## 📊 Test Results Analysis

The tool detects the following statuses:
- **200 OK** - Normal access, website allows this AI crawler
- **403 Forbidden** - Access denied, website blocks this AI crawler
- **404 Not Found** - Page does not exist
- **Timeout/Network Error** - Connection issues

## 🤖 Supported AI Crawlers

This tool tests accessibility for the following AI crawlers:
- ChatGPT-User
- Claude-Web
- GPTBot
- Bard
- BingBot
- FacebookBot
- Google-Extended
- PerplexityBot
- And 30+ other mainstream AI crawlers...

Complete list source: [ai-robots-txt](https://github.com/ai-robots-txt/ai.robots.txt)

## ⚙️ Configuration Options

### Proxy Settings
1. **No proxy** - Direct connection
2. **System proxy** - Automatically detect and use system proxy settings
3. **Custom proxy** - Manually specify local proxy port (such as Clash, V2Ray, etc.)

### Concurrency Settings
- Concurrent thread range: 1-50
- Recommended setting: 10-20 (to avoid excessive pressure on target server)
- Default value: 10

## 🔍 Use Cases

- **Website Administrators** - Check if AI crawler blocking policies on their websites are effective
- **SEO Experts** - Understand search engine and AI crawler access patterns
- **Developers** - Test feasibility of crawler scripts
- **Security Research** - Analyze website anti-crawler mechanisms

## ⚠️ Notes

- Please set concurrency reasonably to avoid excessive pressure on target servers
- Some websites may have IP restrictions; high concurrency may result in temporary IP bans
- This tool is for testing purposes only; please comply with target website terms of use
- It's recommended to check the target website's robots.txt file before testing

## 🤝 Contributing

Welcome to submit Issues and Pull Requests to improve this tool!

### Development Roadmap
- [ ] Add GUI interface
- [ ] Support batch URL testing
- [ ] Add test report export functionality
- [ ] Support custom User-Agent lists
- [ ] Add performance monitoring features

## 📄 License

[MIT License](LICENSE)

## 🙏 Acknowledgments

- AI Crawler list source: [ai-robots-txt](https://github.com/ai-robots-txt/ai.robots.txt)
- Planner: JerryZhi
- Developer: Gemini Advanced 2.0 Flash & GitHub Copilot

## 📧 Contact

For questions or suggestions, please contact me through Issues.

---

**⭐ If this tool helps you, please give it a Star for support!**