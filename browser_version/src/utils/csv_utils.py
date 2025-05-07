import pandas as pd
import os
from datetime import datetime

class CSVHandler:
    def __init__(self, output_dir=None):
        """
        初始化CSV处理器
        :param output_dir: 输出目录
        """
        if output_dir is None:
            # 默认使用browser_version目录下的output文件夹
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 从utils目录向上导航两层到browser_version目录
            browser_version_dir = os.path.dirname(os.path.dirname(current_dir))
            output_dir = os.path.join(browser_version_dir, "output")
        self.output_dir = output_dir
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

    def save_results(self, results, filename=None):
        """
        保存搜索结果到CSV文件
        :param results: 搜索结果DataFrame
        :param filename: 文件名，如果为None则自动生成
        :return: 保存的文件路径
        """
        try:
            if filename is None:
                # 生成带时间戳的文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"search_results_{timestamp}.csv"
            
            # 确保文件名以.csv结尾
            if not filename.endswith('.csv'):
                filename += '.csv'
            
            # 构建完整的文件路径
            filepath = os.path.join(self.output_dir, filename)
            
            # 保存到CSV文件
            results.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            print(f"搜索结果已保存到: {os.path.abspath(filepath)}")
            return filepath
            
        except Exception as e:
            print(f"保存CSV文件时发生错误: {str(e)}")
            return None

    def merge_results(self, results_list, filename=None):
        """
        合并多个搜索结果并保存到CSV文件
        :param results_list: 搜索结果DataFrame列表
        :param filename: 文件名，如果为None则自动生成
        :return: 保存的文件路径
        """
        try:
            # 合并所有结果
            all_results = pd.concat(results_list, ignore_index=True)
            
            # 保存合并后的结果
            return self.save_results(all_results, filename)
            
        except Exception as e:
            print(f"合并和保存结果时发生错误: {str(e)}")
            return None 