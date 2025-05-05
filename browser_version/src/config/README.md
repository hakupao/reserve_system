# 配置文件说明

本文档详细说明了系统的配置文件结构和使用方法。

## 配置文件位置

配置文件位于 `src/config/search_tasks_config.py`。

## 配置项说明

### 1. 搜索任务配置 (SEARCH_TASKS)

搜索任务配置是一个列表，每个任务包含以下字段：

```python
{
    "name": "任务名称",
    "start_time": "1900",        # 开始时间，24小时制，格式：HHMM
    "end_time": "2100",          # 结束时间，24小时制，格式：HHMM
    "selected_days": [1, 2, 3],  # 选择的星期几
    "include_holidays": False,    # 是否包含节假日
    "output_file": "结果文件名.csv"  # 输出文件名
}
```

#### 星期几对照表
- 1: 月曜日（周一）
- 2: 火曜日（周二）
- 3: 水曜日（周三）
- 4: 木曜日（周四）
- 5: 金曜日（周五）
- 6: 土曜日（周六）
- 7: 日曜日（周日）
- 8: 祝日（节假日）

### 2. 日期范围配置 (DATE_CONFIG)

日期范围配置决定了搜索的时间范围：

```python
{
    "start_date": "2024-03-20",  # 开始日期，格式：YYYY-MM-DD
    "end_date": "2024-04-20"     # 结束日期，格式：YYYY-MM-DD
}
```

默认配置为：
- 开始日期：当前日期
- 结束日期：当前日期 + 4周

### 3. 星期配置 (WEEKDAYS_CONFIG)

全局星期配置，可以覆盖单个任务的配置：

```python
{
    "selected_days": [1, 2, 3, 4, 5, 6, 7],  # 要搜索的星期几
    "include_holidays": True                   # 是否包含节假日
}
```

## 配置示例

### 工作日搜索配置
```python
{
    "name": "工作日",
    "start_time": "1900",
    "end_time": "2100",
    "selected_days": [1, 2, 3, 4, 5],  # 周一到周五
    "include_holidays": False,          # 不包含节假日
    "output_file": "weekday_results.csv"
}
```

### 周末搜索配置
```python
{
    "name": "周末",
    "start_time": "0900",
    "end_time": "2100",
    "selected_days": [6, 7],     # 周六和周日
    "include_holidays": True,    # 包含节假日
    "output_file": "weekend_results.csv"
}
```

## 注意事项

1. 时间格式必须是24小时制，且为4位数字（如：0900、1830）
2. 日期格式必须是 YYYY-MM-DD
3. 星期几必须是1-8的整数
4. 文件名必须包含 .csv 后缀
5. 每个任务的名称必须唯一

## 配置修改步骤

1. 打开 `src/config/search_tasks_config.py`
2. 根据需要修改相应的配置项
3. 保存文件
4. 重新运行程序以应用新的配置

## 配置验证

系统会在启动时自动验证配置文件的正确性，如果存在错误，会显示相应的错误信息。 