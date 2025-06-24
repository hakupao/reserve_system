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
        
        # 等待页面加载完成
        time.sleep(2)
        
        # 使用多个选择器查找删除按钮
        selectors = [
            # 1. 使用class和data-v属性
            (By.CSS_SELECTOR, "a.garbage[data-v-a6b7f302]"),
            # 2. 使用class和img组合
            (By.CSS_SELECTOR, "a.garbage img.block"),
            # 3. 使用alt属性
            (By.XPATH, "//a[contains(@class, 'garbage')]//img[contains(@alt, '_delete_button')]"),
            # 4. 使用class
            (By.CSS_SELECTOR, "a.garbage")
        ]
        
        garbage_buttons = []
        for by, value in selectors:
            try:
                buttons = self.element_handler.find_elements(
                    by,
                    value,
                    5,
                    f"删除按钮 ({by}={value})"
                )
                if buttons:
                    garbage_buttons = buttons
                    logger.info(f"使用选择器 {by}={value} 找到 {len(buttons)} 个删除按钮")
                    break
            except Exception as e:
                logger.debug(f"选择器 {by}={value} 未找到按钮: {str(e)}")
                continue
        
        if not garbage_buttons:
            logger.warning("未找到任何删除按钮")
            # 即使没有按钮，也尝试获取输入框
            textarea = self.find_textarea()
            if textarea:
                return True, textarea
            else:
                return False, None
        
        logger.info(f"找到 {len(garbage_buttons)} 个删除按钮")
        
        # 依次点击每个按钮
        for i, button in enumerate(garbage_buttons, 1):
            try:
                # 获取按钮的alt属性，用于日志记录
                alt_text = button.find_element(By.TAG_NAME, "img").get_attribute("alt")
                logger.info(f"正在点击第 {i} 个按钮: {alt_text}")
                
                # 滚动到按钮位置
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(2)  # 等待滚动完成
                
                # 尝试使用JavaScript点击
                try:
                    self.driver.execute_script("arguments[0].click();", button)
                    logger.info(f"使用JavaScript点击第 {i} 个按钮成功")
                except Exception as e:
                    logger.debug(f"JavaScript点击失败，尝试普通点击: {str(e)}")
                    button.click()
                    logger.info(f"使用普通点击第 {i} 个按钮成功")
                
                time.sleep(2)  # 等待点击响应
                
            except Exception as e:
                logger.error(f"点击第 {i} 个按钮时出错: {str(e)}")
                continue
        
        logger.info("所有时间段的删除按钮已点击完成")
        
        # 等待并获取输入框
        textarea = self.find_textarea()
        if textarea:
            return True, textarea
        else:
            return False, None
    
    def find_textarea(self):
        """查找输入框"""
        # 使用多个选择器查找输入框
        selectors = [
            # 1. 使用ID和class组合
            (By.CSS_SELECTOR, "textarea#kouho.form-textarea.choice-textarea"),
            # 2. 使用ID和data-v属性
            (By.CSS_SELECTOR, "textarea#kouho[data-v-a6b7f302]"),
            # 3. 使用ID
            (By.ID, "kouho"),
            # 4. 使用name属性
            (By.NAME, "kouho_add"),
            # 5. 使用placeholder内容
            (By.XPATH, "//textarea[contains(@placeholder, '候補の区切りは改行で判断されます')]")
        ]
        
        for by, value in selectors:
            try:
                textarea = self.element_handler.find_element(
                    by,
                    value,
                    5,
                    f"输入框 ({by}={value})"
                )
                if textarea:
                    logger.info(f"使用选择器 {by}={value} 找到输入框")
                    return textarea
            except Exception as e:
                logger.debug(f"选择器 {by}={value} 未找到输入框: {str(e)}")
                continue
        
        logger.error("未找到输入框")
        return None
    
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
                # 定义多个选择器，按优先级排序
                selectors = [
                    # 1. 精确匹配当前版本
                    (By.CSS_SELECTOR, "p[data-v-a6b7f302] input#name.form-input"),
                    # 2. 匹配任何data-v-*属性
                    (By.CSS_SELECTOR, "p[data-v-] input#name.form-input"),
                    # 3. 只匹配class和id
                    (By.CSS_SELECTOR, "input#name.form-input"),
                    # 4. 使用name属性
                    (By.NAME, "name"),
                    # 5. 使用XPath
                    (By.XPATH, "//input[@name='name' and @type='text']")
                ]
                
                name_input = None
                for by, value in selectors:
                    try:
                        name_input = self.element_handler.find_element(
                            by,
                            value,
                            3,
                            f"name输入框 ({by}={value})"
                        )
                        if name_input:
                            logger.info(f"使用选择器 {by}={value} 找到name输入框")
                            break
                    except Exception as e:
                        logger.debug(f"选择器 {by}={value} 未找到元素: {str(e)}")
                        continue
                
                if name_input:
                    # 清空并输入当前日期时间
                    name_input.clear()
                    name_input.send_keys(f"更新日期: {current_datetime}")
                    logger.info(f"已在name输入框中填入当前日期时间: {current_datetime}")
                else:
                    logger.warning("未找到任何name输入框，将继续保存")
            except Exception as e:
                logger.warning(f"处理name输入框时出错，将继续保存: {str(e)}")
            
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