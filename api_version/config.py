"""
配置文件
包含API调用、搜索参数和输出设置
"""

# API配置
API_CONFIG = {
    "base_url": "https://www.shisetsu.city.yokohama.lg.jp/user",
    "timeout": 30,  # 请求超时时间（秒）
    "retry_times": 3,  # 重试次数
    "retry_delay": 5,  # 重试延迟（秒）
    "request_interval": 3,  # 请求间隔（秒）
    "session_expire": 1800,  # 会话过期时间（秒）
    "endpoints": {
        "search": "/Home/SearchByDateTime",
        "detail": "/user/VacantFrameFacilityStatus",
        "session": "/api/Header/GetSessionInterval",
        "site_status": "/api/Header/GetSiteClosing"
    }
}

# 搜索配置
SEARCH_CONFIG = {
    "default_time_range": {
        "from": "0900",
        "to": "2100"
    },
    "default_areas": [5, 14, 15],  # 默认搜索区域
    "default_purpose_category": 1,  # 默认用途类别
    "default_place_class_category": 1,  # 默认设施类别
    "default_weekdays": [1, 2, 3, 4, 5, 6, 7, 8],  # 默认搜索星期：6=周六, 7=周日, 8=节假日
    "default_search_target": 1,  # 搜索目标
    "default_language_code": 0,  # 语言代码
    "default_purpose": 1,  # 用途
    "default_place_class": 1,  # 设施类别
}

# 输出配置
OUTPUT_CONFIG = {
    "output_dir": "api_version\output",  # 输出目录
    "file_prefix": "api_results_",  # 文件前缀
    "file_extension": ".json",  # 文件扩展名
} 