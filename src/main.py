"""
横滨市设施预约系统主程序
"""

from datetime import datetime
from config.search_tasks_config import SEARCH_TASKS
from core import SearchExecutor, FileHandler

def main():
    # ChromeDriver路径
    chromedriver_path = r"C:\Local\test\reserve_system\chromedriver-win64\chromedriver.exe"
    
    # 初始化组件
    search_executor = SearchExecutor(chromedriver_path)
    file_handler = FileHandler()
    
    # 执行所有搜索任务
    all_results = []
    for task in SEARCH_TASKS:
        # 执行搜索任务
        results = search_executor.execute_task(task)
        
        if results is not None:
            # 保存单个任务的结果
            file_handler.save_task_results(results, task['name'])
            all_results.append(results)
    
    # 处理合并结果
    if all_results:
        # 保存合并结果
        merged_file = file_handler.save_merged_results(all_results)
        # 生成表格图片
        file_handler.generate_table_image(merged_file)
    else:
        print("\n所有搜索任务都失败了，请检查错误信息")
    
    print("\n所有操作已完成！")
    print("请检查结果文件。")

if __name__ == "__main__":
    main() 