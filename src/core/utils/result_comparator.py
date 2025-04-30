"""
结果比较器模块
负责比较两次搜索结果的不同
"""

import os
import pandas as pd
from datetime import datetime

class ResultComparator:
    def __init__(self, base_output_dir):
        self.base_output_dir = base_output_dir
        self.differ_dir = os.path.join(base_output_dir, "differ")
        os.makedirs(self.differ_dir, exist_ok=True)
        
    def compare(self, current_file, previous_file):
        """
        比较两次搜索结果的不同
        :param current_file: 当前结果文件路径
        :param previous_file: 上一次结果文件路径
        :return: 差异结果字典
        """
        try:
            current_df = pd.read_csv(current_file)
            previous_df = pd.read_csv(previous_file)
            
            # 合并两个DataFrame，标记来源
            current_df['source'] = 'current'
            previous_df['source'] = 'previous'
            
            # 找出新增的记录
            new_records = current_df[~current_df['施設名'].isin(previous_df['施設名'])]
            # 找出消失的记录
            removed_records = previous_df[~previous_df['施設名'].isin(current_df['施設名'])]
            
            # 找出修改的记录
            common_records = pd.merge(current_df, previous_df, on='施設名', suffixes=('_current', '_previous'))
            changed_records = common_records[common_records['空き状況_current'] != common_records['空き状況_previous']]
            
            # 输出比较结果
            print(f"\n比较结果:")
            print(f"新增记录数: {len(new_records)}")
            print(f"消失记录数: {len(removed_records)}")
            print(f"修改记录数: {len(changed_records)}")
            
            # 保存差异结果
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = os.path.basename(current_file)
            base_name = os.path.splitext(file_name)[0]
            
            if len(new_records) > 0:
                new_records.to_csv(os.path.join(self.differ_dir, f"{base_name}_new_{timestamp}.csv"), index=False)
            if len(removed_records) > 0:
                removed_records.to_csv(os.path.join(self.differ_dir, f"{base_name}_removed_{timestamp}.csv"), index=False)
            if len(changed_records) > 0:
                changed_records.to_csv(os.path.join(self.differ_dir, f"{base_name}_changed_{timestamp}.csv"), index=False)
                
            return {
                'new': new_records,
                'removed': removed_records,
                'changed': changed_records
            }
            
        except Exception as e:
            print(f"比较结果时发生错误: {str(e)}")
            return None 