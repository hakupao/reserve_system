# 横滨市设施预约系统 API版本

基于直接API调用的横滨市设施预约系统，用于自动搜索和获取可用设施信息。

## 🚀 功能特点

- ✅ **自动设施搜索** - 根据日期、时间、区域自动搜索可用设施
- ✅ **多格式输出** - 支持JSON和CSV格式结果保存
- ✅ **智能会话管理** - 自动处理验证token和会话状态
- ✅ **错误恢复机制** - 自动重试和会话重建
- ✅ **configurable配置** - 灵活的搜索参数配置

## 📁 项目结构

```
api_version/
├── main.py              # 主程序入口
├── api_client.py        # 核心API客户端
├── config.py           # 配置文件
├── utils.py            # 工具函数
├── output_handlers.py  # 输出处理模块
├── parsers.py          # 数据解析模块
├── har_analyzer.py     # HAR文件分析工具
├── multipart_parser.py # Multipart数据解析器
├── output/             # 输出结果目录
└── README.md           # 项目文档
```

## 🛠️ 安装和配置

### 环境要求

- Python 3.7+
- requests 库
- beautifulsoup4 库

### 安装依赖

```bash
pip install requests beautifulsoup4
```

### 配置参数

编辑 `config.py` 文件中的搜索参数：

```python
SEARCH_CONFIG = {
    "default_areas": [5, 14, 15],           # 搜索区域（已验证有效）
    "default_time_range": {
        "from": "0900",                     # 开始时间
        "to": "2100"                        # 结束时间
    },
    "time_range_limits": {
        "max_days": 21,                     # 系统最大支持天数
        "recommended_days": 7,              # 建议天数
        "note": "超过21天会返回E-yokohama-202-000014错误"
    }
}
```

## 🏃‍♂️ 使用方法

### 基本使用

```bash
cd api_version
python main.py
```

### 自定义搜索

```python
from api_client import YokohamaFacilityAPI
from utils import get_date_range

# 创建API客户端
api = YokohamaFacilityAPI()

# 设置搜索参数
date_from, date_to = get_date_range(days=7)  # 搜索7天

# 执行搜索
results = api.search_facilities(
    date_from=date_from,
    date_to=date_to,
    areas=[5, 14, 15]  # 指定搜索区域
)
```

## 📊 输出格式

### JSON格式
```json
{
  "Result": "Ok",
  "Information": "./VacantFrameFacilityStatus",
  "DetailData": {
    "facilities": [
      {
        "No": "1",
        "施设": "神奈川スポーツセンター",
        "室场": "第一体育室Ａ（半面）",
        "日期": "令和7年6月26日(木)",
        "时间带": "13:00～15:00",
        "选择": "选择"
      }
    ]
  }
}
```

### CSV格式
| No | 施设 | 室场 | 日期 | 时间带 | 选择 |
|----|------|------|------|--------|------|
| 1 | 神奈川スポーツセンター | 第一体育室Ａ（半面） | 令和7年6月26日(木) | 13:00～15:00 | 选择 |

## ⚙️ 配置说明

### 区域代码对照表

| 区域ID | 区域名称 | 状态 |
|--------|----------|------|
| 5 | 神奈川区 | ✅ 已验证 |
| 14 | 保土ヶ谷区 | ✅ 已验证 |
| 15 | 旭区 | ✅ 已验证 |

### 时间范围限制

- **推荐范围**: 7天（最佳稳定性）
- **最大范围**: 21天（系统限制）
- **注意**: 超过21天会返回`E-yokohama-202-000014`错误

### 搜索参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `date_from` | 搜索开始日期 | 今天 |
| `date_to` | 搜索结束日期 | 7天后 |
| `areas` | 搜索区域列表 | [5, 14, 15] |
| `time_from` | 时间范围开始 | "0900" |
| `time_to` | 时间范围结束 | "2100" |

## 🔧 工具模块

### har_analyzer.py
用于分析浏览器HAR文件，提取网络请求信息。

```python
from har_analyzer import HarAnalyzer

analyzer = HarAnalyzer("path/to/har_file.har")
analyzer.analyze_search_requests()
```

### multipart_parser.py
用于解析multipart/form-data格式数据。

```python
from multipart_parser import MultipartParser

parser = MultipartParser()
parsed_data = parser.parse(form_data)
```

## 🐛 错误处理

### 常见错误代码

| 错误代码 | 说明 | 解决方案 |
|----------|------|----------|
| `E-yokohama-202-000014` | 请求参数验证失败 | 检查时间范围（不超过21天） |
| `E-205-000004` | 会话状态异常 | 系统会自动重建会话 |

### 调试模式

设置环境变量启用详细日志：

```bash
export DEBUG=1
python main.py
```

## 📝 输出文件

所有结果保存在 `output/` 目录下：

```
output/
├── api_results_20250624_123456.json    # JSON格式结果
└── facilities_20250624_123456.csv      # CSV格式结果
```

## ⚠️ 注意事项

1. **请求频率**: 系统会自动控制请求间隔，避免过于频繁的API调用
2. **会话管理**: 程序会自动管理验证token和会话状态
3. **时间限制**: 建议搜索时间范围不超过21天
4. **区域选择**: 只使用已验证的有效区域ID

## 🔄 更新日志

### v2.0.0 (2025-06-24)
- ✅ 修复E-yokohama-202-000014错误
- ✅ 实现正确的multipart/form-data格式
- ✅ 优化时间范围限制（7天推荐）
- ✅ 验证区域5、14、15有效性
- ✅ 清理临时调试文件

### v1.0.0 (初始版本)
- 基础API调用功能
- JSON和CSV输出支持
- 配置文件系统

## 📞 技术支持

如果遇到问题，请检查：

1. **网络连接** - 确保可以访问横滨市官网
2. **时间范围** - 不要超过21天
3. **区域代码** - 使用已验证的区域ID
4. **Python版本** - 确保使用Python 3.7+

---

**横滨市设施预约系统 API版本** - 高效、稳定的设施搜索解决方案 🏢
