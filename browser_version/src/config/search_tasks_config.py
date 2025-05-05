from datetime import datetime, timedelta

# 计算日期范围
today = datetime.now()
end_date = today + timedelta(weeks=4)

# 搜索任务配置
SEARCH_TASKS = [
    {
        "name": "工作日",
        "start_time": "1900",        # 开始时间，格式：HHMM
        "end_time": "2100",          # 结束时间，格式：HHMM
        "selected_days": [1, 2, 3, 4, 5],  # 月曜日到金曜日
        "include_holidays": False,   # 不包含节假日
        "output_file": "weekday_results.csv"
    },
    {
        "name": "周末和假日",
        "start_time": "0900",        # 开始时间，格式：HHMM
        "end_time": "2100",          # 结束时间，格式：HHMM
        "selected_days": [6, 7],     # 土曜日和日曜日
        "include_holidays": True,    # 包含节假日
        "output_file": "weekend_results.csv"
    }
]

# 日期范围配置
DATE_CONFIG = {
    "start_date": today.strftime("%Y-%m-%d"),  # 开始日期，格式：YYYY-MM-DD
    "end_date": end_date.strftime("%Y-%m-%d")  # 结束日期，格式：YYYY-MM-DD
}

# 星期几配置
# 1: 月曜日(周一), 2: 火曜日(周二), 3: 水曜日(周三), 4: 木曜日(周四), 
# 5: 金曜日(周五), 6: 土曜日(周六), 7: 日曜日(周日), 8: 祝日(节假日)
WEEKDAYS_CONFIG = {
    "selected_days": [1, 2, 3, 4, 5, 6, 7],  # 要选择的星期几，None表示选择所有
    "include_holidays": True                  # 是否包含节假日
} 