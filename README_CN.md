[English](README.md) | [中文](README_CN.md)

<div align="center">

![Reserve System](https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1000&color=8B5CF6&width=500&lines=🏸+reserve_system;设施批量检查工具;Python+·+Selenium+·+HTTP+API)

</div>

我是 **Bojiang**，一名在横滨的羽毛球爱好者。有时候自动化设施查询需要突破浏览器扩展的限制，用上更强大的工具。**reserve_system** 是我用 Python 开发的设施查询工具，支持两种灵活的方式：Selenium 浏览器自动化或直接 HTTP API 调用。

---

## 📋 项目简介

**reserve_system** 是 **[badminton-yoyaku](../badminton-yoyaku)** 浏览器扩展的编程化补充。用 Python 自动化批量查询设施可用性，几秒内检查数百个时段。

### 核心功能

| 功能 | 说明 |
|------|------|
| 🔄 **批量处理** | 同时检查多个设施、日期、时段 |
| 🌐 **双重查询方式** | Selenium 浏览器自动化或直接 HTTP API 调用 |
| 📊 **CSV 导出** | 结果导出至电子表格便于分析 |
| ⚙️ **高度可配置** | YAML/JSON 配置文件，灵活排程 |
| 🔐 **安全凭证管理** | `.env.example` 模板保护敏感信息 |
| 📝 **完整日志** | 详细操作日志便于调试 |
| 🐳 **Docker 就绪** | 容器化部署方案 |

---

## 🚀 技术栈

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-4.x-00B244?style=for-the-badge&logo=selenium)
![Requests](https://img.shields.io/badge/Requests-2.31-2E86AB?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?style=for-the-badge&logo=pandas)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker)

</div>

**核心**: Python 3.11+，支持类型提示

**网页自动化**: Selenium 4 用于浏览器查询

**HTTP 客户端**: Requests 库用于直接 API 调用

**数据处理**: Pandas 用于 CSV 导出和分析

**配置管理**: YAML/JSON 格式，灵活可配

---

## 📦 项目结构

```
reserve_system/
├── main.py              # 入口点
├── config/
│   ├── facilities.yaml  # 设施定义
│   └── schedule.yaml    # 查询排程
├── src/
│   ├── selenium_checker.py    # 浏览器自动化
│   ├── api_checker.py         # 直接 HTTP 查询
│   ├── csv_exporter.py        # 结果导出
│   └── logger.py              # 日志工具
├── docs/
│   ├── SETUP.md
│   ├── SELENIUM.md
│   └── API.md
├── results/             # 输出 CSV
├── logs/                # 操作日志
├── .env.example         # 凭证模板
├── requirements.txt     # Python 依赖
├── docker-compose.yml   # 容器配置
└── README.md
```

---

## 🛠️ 安装与配置

### 前置要求
- Python 3.11+
- pip 包管理器
- Chrome/Chromium（Selenium 选项需要）
- Docker（可选）

### 本地设置

```bash
# 克隆仓库
git clone https://github.com/hakupao/reserve_system.git
cd reserve_system

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境文件
cp .env.example .env
# 如需凭证，编辑 .env
```

### 配置文件

编辑或创建 `config/facilities.yaml`:

```yaml
facilities:
  - name: "神奈川羽毛球中心"
    id: "kanagawa-001"
    url: "https://facility-booking.yokohama.jp/kanagawa"
    courts:
      - "第1号场"
      - "第2号场"
    
  - name: "横滨体育中心"
    id: "yokohama-sports"
    url: "https://facility-booking.yokohama.jp/sports"
    courts:
      - "羽毛球 A"
      - "羽毛球 B"

queries:
  batch_size: 10          # 一次检查 10 个
  timeout: 30             # 30 秒超时
  retry_count: 3          # 失败重试 3 次
```

---

## 🚀 使用示例

### 方式 1：Selenium 浏览器自动化

```bash
# 用 Selenium 检查可用性
python main.py --method selenium \
  --facility "神奈川羽毛球中心" \
  --dates 2025-04-04 2025-04-15 \
  --times "18:00-20:00" "20:00-22:00"
```

**优势**:
- 支持 JavaScript 重型网站
- 兼容现代 web 应用
- 能处理复杂交互
- 对动态内容可靠

**劣势**:
- 速度较慢（浏览器启动开销）
- 资源占用多
- 需要 Chrome/Chromium

### 方式 2：HTTP API 直接调用

```bash
# 用直接 API 调用检查可用性
python main.py --method api \
  --facility "神奈川羽毛球中心" \
  --dates 2025-04-04 2025-04-15 \
  --times "18:00-20:00" "20:00-22:00"
```

**优势**:
- 速度快（无浏览器开销）
- 资源占用少
- 轻量级，易扩展
- 适合批处理

**劣势**:
- 需要 API 文档
- 网站结构变化时可能失效
- 无 JavaScript 执行

### 批量处理

```bash
# 一次处理多个设施
python main.py \
  --method api \
  --batch-file config/batch_query.yaml \
  --export-csv results/availability.csv
```

---

## 📊 配置文件详解

### facilities.yaml

```yaml
facilities:
  - name: "设施名称"
    id: "唯一-id"
    url: "https://..."
    courts: ["场地 1", "场地 2"]
    max_days_ahead: 30
    holidays: [2025-05-05, 2025-05-06]
```

### schedule.yaml

```yaml
queries:
  target_facilities:
    - "神奈川羽毛球中心"
    - "横滨体育中心"
  
  date_ranges:
    - start: 2025-04-04
      end: 2025-04-30
  
  time_slots:
    - 18:00-20:00
    - 20:00-22:00
  
  method: "api"  # 或 "selenium"
  export_format: "csv"
```

---

## 📁 CSV 导出格式

结果导出为：

```csv
facility,date,time_slot,court,available,booked_count,checked_at
神奈川羽毛球中心,2025-04-04,18:00-20:00,第1号场,true,0,2025-04-04T14:30:00Z
神奈川羽毛球中心,2025-04-04,18:00-20:00,第2号场,false,1,2025-04-04T14:30:00Z
横滨体育中心,2025-04-04,20:00-22:00,羽毛球A,true,0,2025-04-04T14:30:01Z
```

---

## 📝 日志记录

所有操作记录到 `logs/` 目录：

```
logs/
├── 2025-04-04_selenium_check.log
└── 2025-04-04_api_check.log
```

**日志条目示例**:
```
[2025-04-04 14:30:00] INFO: 开始检查神奈川羽毛球中心
[2025-04-04 14:30:01] INFO: 2025-04-05 发现 2 个可用时段
[2025-04-04 14:30:01] INFO: 结果已导出到 results/availability.csv
[2025-04-04 14:30:02] INFO: 检查成功完成
```

---

## 🐳 Docker 部署

### 构建镜像

```bash
# 构建容器
docker build -t reserve-system:latest .
```

### Docker Compose 运行

```yaml
# docker-compose.yml
version: '3.9'
services:
  reserve-checker:
    image: reserve-system:latest
    volumes:
      - ./config:/app/config
      - ./results:/app/results
      - ./logs:/app/logs
    environment:
      - METHOD=api
      - LOG_LEVEL=INFO
```

```bash
# 启动容器
docker-compose up -d

# 查看日志
docker-compose logs -f reserve-checker

# 停止容器
docker-compose down
```

---

## 🔐 环境和凭证

### .env 文件

```env
# 横滨设施登录（如需）
FACILITY_USERNAME=your_username
FACILITY_PASSWORD=your_password

# 代理设置（可选）
HTTP_PROXY=http://proxy.example.com:8080
HTTPS_PROXY=http://proxy.example.com:8080

# 日志
LOG_LEVEL=INFO
LOG_DIR=./logs

# 性能
MAX_RETRIES=3
TIMEOUT_SECONDS=30
BATCH_SIZE=10
```

---

## 📊 API 模式实现

对于有公开 API 的网站，直接调用端点：

```python
import requests

def check_availability_api(facility_id: str, date: str, time_slot: str) -> dict:
    """通过 HTTP API 查询设施可用性"""
    url = f"https://api.yokohama-facilities.jp/availability"
    params = {
        "facility_id": facility_id,
        "date": date,
        "time_slot": time_slot
    }
    
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    
    return response.json()
```

---

## 🔄 Selenium 模式实现

对于 JavaScript 重型网站，使用 Selenium：

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

def check_availability_selenium(facility_url: str, date: str) -> dict:
    """通过浏览器自动化查询设施可用性"""
    driver = webdriver.Chrome()
    
    try:
        driver.get(facility_url)
        
        # 填充日期选择器
        date_input = driver.find_element(By.ID, "date-picker")
        date_input.send_keys(date)
        
        # 点击搜索
        search_btn = driver.find_element(By.ID, "search-btn")
        search_btn.click()
        
        # 提取可用性数据
        # ... 解析逻辑 ...
        
        return availability_data
    finally:
        driver.quit()
```

---

## 📖 相关项目

- **[badminton-yoyaku](../badminton-yoyaku)** - 浏览器扩展，实时监控
- **[badminton-tournament-v2](../badminton-tournament-v2)** - 赛事管理系统
- **[shuttle-path](../shuttle-path)** - 教学知识库平台
- **[badminton_tournament_tool](../badminton_tournament_tool)** - 赛事工具 v1

---

## 🧪 测试

```bash
# 运行测试
python -m pytest tests/

# 带覆盖率
python -m pytest --cov=src tests/

# 运行特定测试
python -m pytest tests/test_api_checker.py -v
```

---

## 📝 更新日志

### v1.2.0（当前版本）
- 双重查询方式（Selenium + API）
- CSV 导出功能
- Docker Compose 支持
- 增强日志记录

### v1.1.0
- 配置文件支持
- 批处理功能
- 错误重试逻辑

### v1.0.0
- 初版发布，支持 Selenium
- 基础设施检查
- 日志输出

---

## 🤝 参与贡献

欢迎贡献代码！需要帮助的方面：

1. **更多设施**：添加更多横滨设施
2. **API 集成**：直接 API 支持更多网站
3. **导出格式**：JSON、Excel、数据库导出
4. **通知功能**：邮件、Slack 可用性告警
5. **定时排程**：Cron 集成实现定期检查

---

## 📄 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 💬 联系与支持

- **GitHub**: [@hakupao](https://github.com/hakupao)
- **Issues**: [GitHub Issues](https://github.com/hakupao/reserve_system/issues)
- **文档**: [docs/](docs/) 目录

---

<div align="center">

**批量检查设施，快速找到你的球场**

![Last Commit](https://img.shields.io/github/last-commit/hakupao/reserve_system?style=flat-square&color=8B5CF6)
![Stars](https://img.shields.io/github/stars/hakupao/reserve_system?style=flat-square&color=F59E0B)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

</div>
