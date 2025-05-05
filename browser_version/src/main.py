"""
横滨市设施预约系统主程序
"""

import os
from datetime import datetime
from config.search_tasks_config import SEARCH_TASKS
from core import SearchExecutor, FileHandler

def main():
    # 尝试多种路径策略来定位ChromeDriver
    chromedriver_path = r"browser_version\chromedriver-win64\chromedriver.exe"
    
    # 如果第一个路径不存在，尝试使用基于脚本位置的绝对路径
    if not os.path.exists(chromedriver_path):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(script_dir))
        chromedriver_path = os.path.join(project_root, "browser_version", "chromedriver-win64", "chromedriver.exe")
    
    print(f"使用ChromeDriver路径: {chromedriver_path}")
    
    # 初始化组件
    search_executor = SearchExecutor(chromedriver_path)
    file_handler = FileHandler()
    
    # 执行所有搜索任务
    all_results = []
    success_count = 0
    total_tasks = len(SEARCH_TASKS)
    
    for task in SEARCH_TASKS:
        # 执行搜索任务
        results = search_executor.execute_task(task)
        
        if results is None:
            # None表示执行任务时出错
            print(f"任务 {task['name']} 执行失败")
            continue
            
        # 保存单个任务的结果(即使是空的)
        file_handler.save_task_results(results, task['name'])
        all_results.append(results)
        success_count += 1
    
    # 处理合并结果
    if all_results:
        # 保存合并结果
        merged_file = file_handler.save_merged_results(all_results)
        # 生成表格图片
        file_handler.generate_table_image(merged_file)
        
        print(f"\n执行了 {success_count}/{total_tasks} 个任务")
        if any(len(df) > 0 for df in all_results):
            print("有任务找到了符合条件的结果")
        else:
            print("所有任务都没有找到符合条件的结果")
    else:
        print("\n所有搜索任务都失败了，请检查错误信息")
    
    print("\n所有操作已完成！")
    print("请检查结果文件。")

if __name__ == "__main__":
    main() 