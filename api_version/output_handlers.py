"""
横滨市设施预约系统 输出处理模块
处理输出和文件保存相关的功能
"""

import os
import json
from typing import Dict, List
from datetime import datetime

def create_output_directory(base_dir: str) -> tuple:
    """
    创建输出目录结构
    
    Args:
        base_dir: 基础输出目录
        
    Returns:
        tuple: (timestamp, output_dir_path)
    """
    # 确保基础目录存在
    os.makedirs(base_dir, exist_ok=True)
    
    # 创建以时间戳命名的子文件夹
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(base_dir, timestamp)
    os.makedirs(output_dir, exist_ok=True)
    
    return timestamp, output_dir

def save_json_result(result: Dict, output_dir: str, filename: str = "data.json") -> str:
    """
    保存JSON格式的结果
    
    Args:
        result: 要保存的结果数据
        output_dir: 输出目录
        filename: 输出文件名
        
    Returns:
        str: 保存的文件路径
    """
    json_file = os.path.join(output_dir, filename)
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return json_file

def save_csv_result(facilities: List[Dict], output_dir: str, filename: str = "facilities.csv") -> str:
    """
    保存CSV格式的结果
    
    Args:
        facilities: 设施数据列表
        output_dir: 输出目录
        filename: 输出文件名
        
    Returns:
        str: 保存的文件路径
    """
    # 准备排序
    # 先按日期排序，再按时间排序
    sorted_facilities = sorted(facilities, key=lambda x: (x.get("日付", ""), x.get("時間帯", "")))
    
    csv_file = os.path.join(output_dir, filename)
    with open(csv_file, "w", encoding="utf-8") as f:
        # 写入表头（不包含No字段）
        f.write("施設,室場,日付,時間帯\n")
        
        # 写入数据行
        for facility in sorted_facilities:
            row = f"{facility.get('施設', '')},{facility.get('室場', '')},{facility.get('日付', '')},{facility.get('時間帯', '')}\n"
            f.write(row)
    
    return csv_file 