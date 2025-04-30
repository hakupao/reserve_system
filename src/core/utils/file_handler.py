"""
文件处理器模块
负责处理所有文件操作
"""

import os
import shutil
from datetime import datetime
from utils.csv_utils import CSVHandler
from utils.table_generator import generate_table_image

class FileHandler:
    def __init__(self):
        self.csv_handler = CSVHandler()
        self.base_output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(self.base_output_dir, exist_ok=True)
        self.current_timestamp = None
        self.current_dir = None
        
    def _get_timestamp_dir(self):
        """获取当前时间戳目录"""
        if self.current_timestamp is None:
            self.current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.current_dir = os.path.join(self.base_output_dir, self.current_timestamp)
            os.makedirs(self.current_dir, exist_ok=True)
        return self.current_dir
        
    def _cleanup_old_dirs(self):
        """清理旧的输出目录，只保留最新的两个"""
        # 获取所有时间戳目录
        dirs = [d for d in os.listdir(self.base_output_dir) 
                if os.path.isdir(os.path.join(self.base_output_dir, d)) 
                and d != "differ"]
        
        if len(dirs) > 2:
            # 按时间戳排序，删除最旧的目录
            dirs.sort()
            for old_dir in dirs[:-2]:
                shutil.rmtree(os.path.join(self.base_output_dir, old_dir))
        
    def save_task_results(self, results, task_name):
        """
        保存单个任务的结果
        :param results: 搜索结果DataFrame
        :param task_name: 任务名称
        :return: 保存的文件路径
        """
        # 获取当前时间戳目录
        current_dir = self._get_timestamp_dir()
        
        # 保存结果文件
        output_file = os.path.join(current_dir, f"{task_name}.csv")
        self.csv_handler.save_results(results, output_file)
        
        return output_file
        
    def save_merged_results(self, all_results):
        """
        保存合并后的结果
        :param all_results: 所有结果的列表
        :return: 保存的文件路径
        """
        # 获取当前时间戳目录
        current_dir = self._get_timestamp_dir()
        
        # 保存合并结果
        merged_file = os.path.join(current_dir, "all_results.csv")
        self.csv_handler.merge_results(all_results, merged_file)
        
        # 清理旧的目录
        self._cleanup_old_dirs()
        
        return merged_file
            
    def generate_table_image(self, merged_file):
        """
        生成表格图片
        :param merged_file: 合并结果文件路径
        :return: 图片文件路径
        """
        current_dir = os.path.dirname(merged_file)
        image_path = os.path.join(current_dir, "results_table.png")
        generate_table_image(merged_file, image_path)
        return image_path 