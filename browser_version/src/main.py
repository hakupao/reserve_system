"""
横滨市设施预约系统主程序
"""

import os
import logging
from datetime import datetime
import glob
import pandas as pd
from config.search_tasks_config import SEARCH_TASKS
from config.chouseisan_config import CHOUSEISAN_CONFIG
from core import SearchExecutor, FileHandler
from core.chouseisan import ChouseisanUpdater
from core.chouseisan.utils import find_chromedriver_path, setup_logging

# 配置日志
logger = setup_logging()

def get_latest_results_file():
    """获取最新的all_results.csv文件路径"""
    output_dir = "output"
    # 获取所有日期文件夹
    date_folders = glob.glob(os.path.join(output_dir, "*"))
    if not date_folders:
        return None
    
    # 按修改时间排序，获取最新的文件夹
    latest_folder = max(date_folders, key=os.path.getmtime)
    
    # 在最新文件夹中查找all_results.csv
    results_file = os.path.join(latest_folder, "all_results.csv")
    if os.path.exists(results_file):
        return results_file
    return None

def main():
    # 使用工具函数查找ChromeDriver路径
    chromedriver_path = find_chromedriver_path()
    if not chromedriver_path:
        logger.error("未找到ChromeDriver，程序无法继续执行")
        return
    
    logger.info(f"使用ChromeDriver路径: {chromedriver_path}")
    print(f"使用ChromeDriver路径: {chromedriver_path}")
    
    # 初始化组件
    search_executor = SearchExecutor(chromedriver_path)
    file_handler = FileHandler()
    
    # 执行所有搜索任务
    all_results = []
    success_count = 0
    total_tasks = len(SEARCH_TASKS)
    total_results_count = 0
    
    for task in SEARCH_TASKS:
        logger.info(f"开始执行任务: {task['name']}")
        # 执行搜索任务
        results = search_executor.execute_task(task)
        
        if results is None:
            # None表示执行任务时出错
            logger.error(f"任务 {task['name']} 执行失败")
            print(f"任务 {task['name']} 执行失败")
            continue
            
        # 保存单个任务的结果(即使是空的)
        file_handler.save_task_results(results, task['name'])
        all_results.append(results)
        success_count += 1
        
        # 统计结果数量
        if results is not None:
            total_results_count += len(results)
            logger.info(f"任务 {task['name']} 找到 {len(results)} 条结果")
    
    # 处理合并结果
    if all_results:
        # 保存合并结果
        merged_file = file_handler.save_merged_results(all_results)
        logger.info(f"合并结果保存到: {merged_file}")
        
        # 生成表格图片
        image_path = file_handler.generate_table_image(merged_file)
        logger.info(f"表格图片生成到: {image_path}")
        
        print(f"\n执行了 {success_count}/{total_tasks} 个任务")
        if total_results_count > 0:
            print(f"总共找到了 {total_results_count} 条符合条件的结果")
        else:
            print("所有任务都没有找到符合条件的结果")
    else:
        logger.error("所有搜索任务都失败了")
        print("\n所有搜索任务都失败了，请检查错误信息")
    
    # 更新调整さん网站
    update_chouseisan(chromedriver_path)
    
    logger.info("所有操作已完成")
    print("\n所有操作已完成！")
    print("请检查结果文件。")

def update_chouseisan(chromedriver_path):
    """
    登录调整さん网站并更新消息
    
    Args:
        chromedriver_path: ChromeDriver路径
    """
    # 检查配置是否完整
    if not CHOUSEISAN_CONFIG['email'] or not CHOUSEISAN_CONFIG['password'] or not CHOUSEISAN_CONFIG['url']:
        logger.warning("调整さん网站配置不完整，跳过更新")
        print("\n调整さん网站配置不完整，跳过更新")
        return
    
    logger.info("正在登录调整さん网站更新消息...")
    print("\n正在登录调整さん网站更新消息...")
    
    # 初始化更新器，使用新的模块化结构
    updater = ChouseisanUpdater(
        chromedriver_path, 
        headless=CHOUSEISAN_CONFIG.get('headless', False)
    )
    
    try:
        # 打开网页
        if not updater.open_url(CHOUSEISAN_CONFIG['url']):
            logger.error("打开调整さん网站失败")
            print("打开调整さん网站失败")
            return
            
        # 登录并更新数据
        if updater.login(
            CHOUSEISAN_CONFIG['email'], 
            CHOUSEISAN_CONFIG['password'], 
            CHOUSEISAN_CONFIG['url']
        ):
            logger.info("登录调整さん网站并更新数据成功")
            print("登录调整さん网站并更新数据成功")
        else:
            logger.error("登录调整さん网站或更新数据失败")
            print("登录调整さん网站或更新数据失败")
    finally:
        # 关闭浏览器
        updater.close()
        logger.info("调整さん网站浏览器已关闭")

if __name__ == "__main__":
    main() 