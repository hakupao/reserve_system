"""
横滨市设施预约系统 API 版本
使用直接API调用方式获取数据
"""

import os
from config import SEARCH_CONFIG, OUTPUT_CONFIG
from api_client import YokohamaFacilityAPI
from utils import get_date_range, print_log, print_summary
from output_handlers import create_output_directory, save_json_result, save_csv_result

def main():
    """主程序入口"""
    # 创建API客户端
    api = YokohamaFacilityAPI()
    
    # 获取日期范围
    date_from, date_to = get_date_range(days=30)
    
    print_log("开始搜索设施...", "INFO")
    print_log(f"搜索日期范围: {date_from} 至 {date_to}", "INFO")
    print_log(f"搜索时间范围: {SEARCH_CONFIG['default_time_range']['from']} 至 {SEARCH_CONFIG['default_time_range']['to']}", "INFO")
    print_log(f"搜索区域: {SEARCH_CONFIG['default_areas']}", "INFO")
    
    # 执行搜索
    results = api.search_facilities(
        date_from=date_from,
        date_to=date_to,
        areas=SEARCH_CONFIG["default_areas"]
    )
    
    if results:
        # 创建输出目录
        timestamp, output_dir = create_output_directory(OUTPUT_CONFIG["output_dir"])
        
        # 保存JSON结果
        json_file = save_json_result(results, output_dir)
        print_log(f"JSON结果已保存到: {json_file}", "INFO")
        
        # 打印结果摘要
        if isinstance(results, dict):
            print_summary(results)
            
            # 生成CSV文件
            if "DetailData" in results and "facilities" in results["DetailData"]:
                facilities = results["DetailData"]["facilities"]
                
                # 保存CSV结果
                csv_file = save_csv_result(facilities, output_dir)
                print_log(f"CSV格式数据已保存到: {csv_file}", "INFO")
    else:
        print_log("未获取到结果", "ERROR")

if __name__ == "__main__":
    main() 