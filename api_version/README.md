# 横滨市设施预约系统 API 版本

这是一个用于获取横滨市公共设施预约信息的API客户端程序。

## 功能特点

- 支持使用API直接获取横滨市设施预约信息
- 自动处理会话令牌和请求验证
- 支持按区域、日期和时间搜索空闲设施
- 自动解析返回的数据，包括HTML和JSON格式
- 结果保存为JSON和CSV格式
- 模块化设计，便于维护和扩展
- 智能重试机制和错误处理

## 项目结构

```
api_version/
├── __init__.py        # 包初始化文件
├── main.py            # 主程序入口
├── api_client.py      # API客户端模块
├── parsers.py         # HTML解析器模块
├── output_handlers.py # 输出处理模块
├── utils.py           # 工具函数模块
├── config.py          # 配置文件
└── output/            # 结果输出目录
```

## 模块说明

### 1. API客户端模块 (api_client.py)
- 处理所有API通信
- 管理会话和令牌
- 实现请求重试机制
- 处理请求头和表单数据

### 2. 解析器模块 (parsers.py)
- 解析HTML内容
- 提取设施信息
- 处理表格数据
- 提取日期和区域信息

### 3. 输出处理模块 (output_handlers.py)
- 管理输出目录结构
- 保存JSON格式数据
- 生成CSV格式报告
- 处理文件命名和路径

### 4. 工具函数模块 (utils.py)
- 日期处理功能
- 日志记录工具
- 通用辅助函数
- 结果摘要生成

### 5. 配置文件 (config.py)
- API相关配置
- 搜索参数设置
- 输出选项配置
- 系统常量定义

## 安装

1. 确保安装了Python 3.8+
2. 安装依赖库：

```bash
pip install -r requirements.txt
```

## 使用方法

运行主程序：

```bash
python main.py
```

默认情况下，程序将：
1. 搜索接下来30天内指定区域的可用设施
2. 将结果保存为JSON和CSV格式
3. 在output目录下创建时间戳子目录
4. 生成结果摘要

## 配置文件详细说明

配置文件`config.py`分为三个主要部分：

### 1. API 配置 (API_CONFIG)

```python
API_CONFIG = {
    "base_url": "https://www.shisetsu.city.yokohama.lg.jp/user",  # API基础URL
    "timeout": 30,            # 请求超时时间（秒）
    "retry_times": 3,         # 请求失败时的重试次数
    "retry_delay": 5,         # 重试间隔（秒）
    "request_interval": 3,    # 两次请求之间的最小间隔（秒），避免请求过于频繁
    "session_expire": 1800,   # 会话过期时间（秒），超过此时间会重新获取令牌
    "endpoints": {            # API端点路径
        "search": "/Home/SearchByDateTime",           # 搜索设施的端点
        "detail": "/user/VacantFrameFacilityStatus",  # 获取详细信息的端点
        "session": "/api/Header/GetSessionInterval",  # 获取会话间隔的端点
        "site_status": "/api/Header/GetSiteClosing"   # 获取站点状态的端点
    }
}
```

### 2. 搜索配置 (SEARCH_CONFIG)

```python
SEARCH_CONFIG = {
    "default_time_range": {   # 默认时间范围
        "from": "0900",       # 开始时间（24小时制，无冒号）
        "to": "2100"          # 结束时间（24小时制，无冒号）
    },
    "default_areas": [5, 14, 15],  # 默认搜索区域ID
    # 区域ID参考:
    # 5 = 神奈川区
    # 14 = 西区
    # 15 = 中区
    # 可添加更多区域ID
    
    "default_purpose_category": 1,     # 默认用途类别ID
    "default_place_class_category": 1, # 默认设施类别ID
    "default_weekdays": [1, 2, 3, 4, 5, 6, 7, 8],  # 默认搜索星期
    # 星期ID参考:
    # 1 = 周一
    # 2 = 周二
    # 3 = 周三
    # 4 = 周四
    # 5 = 周五
    # 6 = 周六
    # 7 = 周日
    # 8 = 节假日
    
    "default_search_target": 1,    # 搜索目标（1=空闲设施）
    "default_language_code": 0,    # 语言代码（0=日语）
    "default_purpose": 1,          # 用途ID
    "default_place_class": 1       # 设施类别ID
}
```

### 3. 输出配置 (OUTPUT_CONFIG)

```python
OUTPUT_CONFIG = {
    "output_dir": "output",             # 输出目录路径
    "file_prefix": "api_results_",      # 输出文件名前缀
    "file_extension": ".json"           # 输出文件扩展名
}
```

## 自定义搜索参数

如需使用自定义参数搜索，可以修改配置文件或在代码中传递参数：

```python
# 在代码中自定义搜索参数示例
results = api.search_facilities(
    date_from="2025-06-01",         # 开始日期
    date_to="2025-06-30",           # 结束日期
    time_from="1800",               # 开始时间
    time_to="2100",                 # 结束时间
    areas=[5, 6, 7],                # 自定义区域
    purpose_category=2,             # 自定义用途类别
    place_class_category=3          # 自定义设施类别
)
```

## 输出数据格式

程序输出的JSON文件包含以下主要字段：

```json
{
  "Result": "状态码",
  "Information": "相对路径或其他信息",
  "DetailData": {
    "html_content": true,
    "title": "页面标题",
    "facilities": [
      {
        "No": "序号",
        "施設": "设施名称",
        "室場": "房间名称",
        "日付": "可用日期",
        "時間帯": "可用时间段",
        "選択": "选择状态"
      },
      // 更多设施...
    ]
  }
}
```

### CSV格式输出
CSV文件包含以下列：
- 施設（设施名称）
- 室場（房间名称）
- 日付（可用日期）
- 時間帯（可用时间段）

数据按日期和时间排序。

## 主要问题修复记录

本程序曾经存在的主要问题及其修复：

1. **请求头设置错误**：
   - 修正了Origin和Referer头部字段
   - 修正了Content-Type设置

2. **表单数据处理问题**：
   - 修复了处理相同名称多值字段的问题
   - 正确实现了URL编码和multipart请求

3. **请求路径处理**：
   - 修正了相对路径的处理方式
   - 增强了URL构建逻辑

4. **HTML内容提取**：
   - 增加了从HTML中提取有用数据的功能
   - 支持解析表格、日期范围和区域信息

## 数据解析待优化

当前的HTML解析可能仍不完善，根据实际情况，可能需要：

1. 进一步分析返回的HTML结构
2. 扩展BeautifulSoup选择器以提取更多数据
3. 模拟浏览器渲染（如有需要）

## 工作原理

1. 初始化会话并获取验证令牌
2. 使用令牌发送搜索请求
3. 处理返回的JSON响应
4. 如需要，获取并解析详细页面
5. 合并所有数据并保存

## 依赖库

- requests：HTTP请求库
- beautifulsoup4：HTML解析
- datetime：日期时间处理
- json：JSON数据处理
- os：文件系统操作

## 注意事项

本程序仅供学习和研究使用，请勿用于任何商业用途。使用时请遵守相关网站的使用条款。

为避免对目标网站造成负担，建议：
1. 保持较大的请求间隔（至少3秒）
2. 避免短时间内频繁运行程序
3. 仅在必要时获取数据
4. 合理设置搜索参数，避免过大范围的查询
