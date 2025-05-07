# 横滨市设施预约系统

这是一个工具集，用于监控和查询横滨市公共设施的预约情况。系统提供两种不同的实现方式：

## 项目结构

```
reserve_system/
├── browser_version/       # 模拟浏览器执行版本
│   ├── src/               # 源代码
│   ├── output/            # 输出结果
│   ├── chromedriver-win64/ # ChromeDriver
│   └── README.md          # 浏览器版本说明文档
│
├── api_version/           # API调用版本 
│   ├── __init__.py        # 包初始化文件
│   ├── main.py            # 主程序入口
│   ├── api_client.py      # API客户端模块
│   ├── parsers.py         # HTML解析器模块
│   ├── output_handlers.py # 输出处理模块
│   ├── utils.py           # 工具函数模块
│   ├── config.py          # 配置文件
│   ├── output/            # 输出结果
│   └── README.md          # API版本说明文档
│
└── requirements.txt       # 整体项目依赖
```

## 功能版本

### 1. 模拟浏览器版本 (browser_version)

通过Selenium模拟浏览器访问和操作横滨市设施预约系统网站，自动化查询和监控设施预约情况。

**主要特点**：
- 多设施并发搜索
- 数据可视化处理
- 智能文件管理

详情请参阅 [浏览器版本文档](./browser_version/README.md)

### 2. API版本 (api_version)

通过直接调用横滨市设施预约系统的API接口获取数据，实现高效的设施预约情况查询。

**主要特点**：
- 直接API调用，无需浏览器
- 支持按区域、日期和时间搜索
- 结果保存为JSON和CSV格式
- 模块化设计，便于维护和扩展
- 自动会话管理和token处理
- 智能重试机制和错误处理

**模块说明**：
- `api_client.py`: 处理所有API通信，包括会话管理、请求发送和响应处理
- `parsers.py`: 负责解析HTML内容，提取设施信息
- `output_handlers.py`: 处理数据输出，支持JSON和CSV格式
- `utils.py`: 提供日期处理、日志记录等通用功能
- `config.py`: 集中管理配置参数

详情请参阅 [API版本文档](./api_version/README.md)

## 使用指南

根据您的需求选择适合的版本：
- 如果需要完整的可视化结果和界面交互，请使用**浏览器版本**
- 如果追求高效率和轻量级操作，请使用**API版本**

每个版本目录下都包含详细的使用说明和配置指南。

## 环境要求

请确保已安装以下环境：
- Python 3.8+
- 相关依赖包(详见requirements.txt)

### 安装依赖

安装项目所需的所有依赖：
```bash
pip install -r requirements.txt
```

注意：
- 建议使用虚拟环境安装依赖，避免与系统Python环境冲突
- 如果使用虚拟环境，请先创建并激活虚拟环境：
  ```bash
  # Windows
  python -m venv venv
  .\venv\Scripts\activate

  # Linux/Mac
  python3 -m venv venv
  source venv/bin/activate
  ```

## 开源许可

本项目仅供学习和研究使用，请遵守相关网站的使用条款。 