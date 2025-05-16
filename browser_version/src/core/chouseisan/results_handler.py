"""
结果处理模块
"""

import os
import glob
import logging
import time
import pandas as pd
from datetime import datetime
from selenium.webdriver.common.by import By

# 获取模块日志记录器
logger = logging.getLogger('ChouseisanBrowser.ResultsHandler')

class ResultsHandler:
    """结果处理类"""
    
    def __init__(self, element_handler):
        """
        初始化结果处理器
        
        Args:
            element_handler: ElementHandler实例
        """
        self.element_handler = element_handler
        self.driver = element_handler.driver
    
    def get_latest_results_file(self):
        """获取最新的all_results.csv文件路径"""
        # 获取当前文件所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 向上导航到browser_version目录
        browser_version_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        output_dir = os.path.join(browser_version_dir, "output")
        
        # 获取所有日期文件夹
        date_folders = glob.glob(os.path.join(output_dir, "*"))
        if not date_folders:
            logger.error("未找到任何输出文件夹")
            return None
        
        # 按修改时间排序，获取最新的文件夹
        latest_folder = max(date_folders, key=os.path.getmtime)
        
        # 在最新文件夹中查找all_results.csv
        results_file = os.path.join(latest_folder, "all_results.csv")
        if os.path.exists(results_file):
            logger.info(f"找到最新的结果文件: {results_file}")
            return results_file
        else:
            logger.error(f"在最新文件夹中未找到all_results.csv: {latest_folder}")
            return None
    
    def delete_existing_slots(self):
        """
        删除现有的时间段
        
        Returns:
            bool: 是否成功删除
            textarea_element: 找到的文本域元素，用于后续输入
        """
        logger.info("开始删除现有时间段...")
        
        # 使用XPath找到所有带有垃圾图标的按钮
        garbage_buttons = self.element_handler.find_elements(
            By.XPATH, 
            "//a[contains(@class, 'garbage')]", 
            10,
            "删除按钮"
        )
        
        if not garbage_buttons:
            logger.warning("未找到任何删除按钮")
            # 即使没有按钮，也尝试获取输入框
            textarea = self.element_handler.find_element(
                By.ID, 
                "kouho", 
                10, 
                "输入框"
            )
            if textarea:
                return True, textarea
            else:
                return False, None
        
        logger.info(f"找到 {len(garbage_buttons)} 个的删除按钮")
        
        # 依次点击每个按钮
        for i, button in enumerate(garbage_buttons, 1):
            try:
                # 获取按钮的alt属性，用于日志记录
                alt_text = button.find_element(By.TAG_NAME, "img").get_attribute("alt")
                logger.info(f"正在点击第 {i} 个按钮: {alt_text}")
                
                # 点击按钮
                button.click()
                time.sleep(0.5)  # 等待一下，避免点击太快
                
            except Exception as e:
                logger.error(f"点击第 {i} 个按钮时出错: {str(e)}")
                continue
        
        logger.info("所有时间段的删除按钮已点击完成")
        
        # 等待输入框加载
        textarea = self.element_handler.find_element(
            By.ID, 
            "kouho", 
            10, 
            "输入框"
        )
        
        if textarea:
            return True, textarea
        else:
            return False, None
    
    def update_with_search_results(self, textarea):
        """
        使用搜索结果更新输入框
        
        Args:
            textarea: 文本域元素
            
        Returns:
            bool: 是否成功更新
        """
        logger.info("开始使用搜索结果更新输入框...")
        
        # 从最新的output文件读取数据
        latest_results_file = self.get_latest_results_file()
        if not latest_results_file:
            logger.error("未找到最新的结果文件")
            return False
            
        # 读取CSV文件
        try:
            results_df = pd.read_csv(latest_results_file)
            
            if results_df.empty:
                logger.warning("CSV文件中没有数据")
                return False
                
            # 构建输入文本
            input_text = ""
            for _, row in results_df.iterrows():
                line = f"{row['设施名称']} {row['室场名称']} {row['日期']} {row['时间段']}"
                input_text += line + "\n"
            
            # 清空输入框并输入文本
            textarea.clear()
            textarea.send_keys(input_text)
            logger.info("已输入所有搜索结果数据")
            
            # 获取当前日期时间
            current_datetime = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            
            # 尝试获取name输入框并填入当前日期时间
            try:
                # 首先尝试使用CSS选择器
                name_input = self.element_handler.find_element(
                    By.CSS_SELECTOR, 
                    "p[data-v-6fb79e1f] input#name", 
                    5, 
                    "name输入框"
                )
                
                if name_input:
                    # 清空并输入当前日期时间
                    name_input.clear()
                    name_input.send_keys(f"更新日期: {current_datetime}")
                    logger.info(f"已在name输入框中填入当前日期时间: {current_datetime}")
            except Exception:
                # 尝试其他可能的选择器
                try:
                    name_input = self.element_handler.find_element(
                        By.ID, 
                        "name", 
                        3, 
                        "备用name输入框"
                    )
                    if name_input:
                        name_input.clear()
                        name_input.send_keys(f"更新日期: {current_datetime}")
                        logger.info(f"已在备用name输入框中填入当前日期时间: {current_datetime}")
                except Exception as e:
                    logger.warning(f"未找到name输入框，将继续保存: {str(e)}")
            
            # 点击保存按钮
            if not self.element_handler.click_element(
                By.ID, 
                "submit-form", 
                10, 
                "保存按钮"
            ):
                logger.error("无法找到或点击保存按钮")
                return False
            
            # 添加短暂延迟以确保JavaScript事件触发
            time.sleep(2)
                
            logger.info("已点击保存按钮，更新完成")
            return True
            
        except Exception as e:
            logger.error(f"处理搜索结果数据时出错: {str(e)}")
            return False 