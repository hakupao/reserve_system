"""
横滨市设施预约系统 工具函数模块
提供各种通用辅助功能
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

def get_date_range(days: int = 30) -> tuple:
    """
    获取日期范围
    
    Args:
        days: 从今天开始的天数
        
    Returns:
        tuple: (from_date, to_date) 格式为 YYYY-MM-DD
    """
    today = datetime.now()
    date_from = today.strftime("%Y-%m-%d")
    date_to = (today + timedelta(days=days)).strftime("%Y-%m-%d")
    
    return date_from, date_to

def format_log_message(message: str, level: str = "INFO") -> str:
    """
    格式化日志消息
    
    Args:
        message: 日志消息
        level: 日志级别
        
    Returns:
        str: 格式化后的日志消息
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"[{timestamp}] [{level}] {message}"

def print_log(message: str, level: str = "INFO") -> None:
    """
    打印带格式的日志
    
    Args:
        message: 日志消息
        level: 日志级别
    """
    formatted_message = format_log_message(message, level)
    print(formatted_message)

def print_summary(data: Dict[str, Any]) -> None:
    """
    打印结果摘要
    
    Args:
        data: 要总结的数据
    """
    print_log("\n结果摘要:", "INFO")
    
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            count = len(value) if isinstance(value, list) else len(value.items())
            print_log(f"{key}: {type(value).__name__} ({count} 项)", "INFO")
        else:
            print_log(f"{key}: {value}", "INFO") 