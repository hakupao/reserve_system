"""
搜索执行器模块
负责执行搜索任务和管理浏览器实例
"""

from utils.driver_utils import setup_driver
from pages.home_page import (
    open_website,
    click_date_tab_button,
    check_badminton_checkbox,
    input_date_range,
    select_time_range,
    select_all_weekdays,
    select_empty_slots,
    click_area_filter_button,
    select_specific_areas,
    click_search_button
)
from pages.search_results_page import load_all_results

class SearchExecutor:
    def __init__(self, chromedriver_path):
        self.chromedriver_path = chromedriver_path
        
    def perform_search(self, driver, task_config):
        """
        执行一次搜索
        :param driver: WebDriver实例
        :param task_config: 搜索任务配置
        :return: 搜索结果DataFrame
        """
        try:
            # 点击日期标签按钮
            if not click_date_tab_button(driver):
                raise Exception("无法点击日期标签按钮")
            
            # 勾选羽毛球复选框
            if not check_badminton_checkbox(driver):
                raise Exception("无法勾选羽毛球复选框")
                
            # 输入日期范围
            if not input_date_range(driver):
                raise Exception("无法输入日期范围")
                
            # 选择空きコマ
            if not select_empty_slots(driver):
                raise Exception("无法选择空きコマ")
                
            # 点击区名などで絞り込む按钮
            if not click_area_filter_button(driver):
                raise Exception("无法点击区名などで絞り込む按钮")
                
            # 选择指定区域
            if not select_specific_areas(driver):
                raise Exception("无法选择指定区域")
            
            # 选择时间范围
            if not select_time_range(driver, task_config):
                raise Exception("无法选择时间范围")
                
            # 选择星期几和节假日
            if not select_all_weekdays(driver, task_config):
                raise Exception("无法选择星期几和节假日")
                
            # 点击搜索按钮
            if not click_search_button(driver):
                raise Exception("无法点击搜索按钮")
                
            # 加载并获取搜索结果
            results = load_all_results(driver)
            # 注意：load_all_results现在总是返回DataFrame，可能是空的
            
            # 添加搜索类型列
            results['search_type'] = task_config['name']
            
            # 检查是否有数据
            if len(results) == 0:
                print(f"{task_config['name']}：无符合条件的结果")
            else:
                print(f"{task_config['name']}：找到 {len(results)} 条结果")
                
            return results
            
        except Exception as e:
            print(f"执行{task_config['name']}时发生错误: {str(e)}")
            return None

    def execute_task(self, task_config):
        """
        执行单个搜索任务
        :param task_config: 任务配置
        :return: 搜索结果DataFrame
        """
        driver = None
        try:
            print(f"\n开始执行{task_config['name']}...")
            
            # 创建浏览器实例
            driver = setup_driver(self.chromedriver_path)
            print("浏览器已启动")
            
            # 打开目标网站
            target_url = "https://www.shisetsu.city.yokohama.lg.jp/user/Home"
            if not open_website(driver, target_url):
                raise Exception("无法打开目标网站")
            
            # 执行搜索
            results = self.perform_search(driver, task_config)
            return results
            
        except Exception as e:
            print(f"执行{task_config['name']}时发生错误: {str(e)}")
            return None
        finally:
            # 确保浏览器被关闭
            if driver:
                driver.quit()
                print("浏览器已关闭") 