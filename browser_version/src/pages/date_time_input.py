from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from config.search_tasks_config import DATE_CONFIG

class DateTimeInput:
    def __init__(self, driver):
        self.driver = driver
        self.date_config = DATE_CONFIG

    def input_date_range(self, start_date=None, end_date=None):
        """
        输入日期范围
        :param start_date: 开始日期，格式为 YYYY-MM-DD，如果为None则使用配置文件中的值
        :param end_date: 结束日期，格式为 YYYY-MM-DD，如果为None则使用配置文件中的值
        :return: bool 是否成功
        """
        try:
            # 使用配置文件中的值或传入的参数
            start_date = start_date or self.date_config["start_date"]
            end_date = end_date or self.date_config["end_date"]
            
            print("正在输入日期范围...")
            
            # 等待页面完全加载
            time.sleep(1)
            
            # 等待日期输入框出现
            print("等待开始日期输入框...")
            start_date_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='HomeModel.DateFrom']"))
            )
            print("找到开始日期输入框")
            
            print("等待结束日期输入框...")
            end_date_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='HomeModel.DateTo']"))
            )
            print("找到结束日期输入框")
            
            # 滚动到开始日期输入框
            self.driver.execute_script("arguments[0].scrollIntoView(true);", start_date_input)
            time.sleep(0.5)
            
            # 清除现有值并输入新值
            start_date_input.clear()
            start_date_input.send_keys(start_date)
            time.sleep(0.5)
            
            # 滚动到结束日期输入框
            self.driver.execute_script("arguments[0].scrollIntoView(true);", end_date_input)
            time.sleep(0.5)
            
            # 清除现有值并输入新值
            end_date_input.clear()
            end_date_input.send_keys(end_date)
            time.sleep(0.5)
            
            # 验证日期是否设置成功
            start_value = start_date_input.get_attribute("value")
            end_value = end_date_input.get_attribute("value")
            print(f"开始日期当前值: {start_value}")
            print(f"结束日期当前值: {end_value}")
            
            if start_value == start_date and end_value == end_date:
                print(f"成功设置日期范围：{start_date} 至 {end_date}")
                return True
            else:
                print("日期设置可能未成功")
                return False
                
        except Exception as e:
            print(f"输入日期时发生错误: {str(e)}")
            return False

    def select_time_range(self, task_config):
        """
        选择时间范围
        :param task_config: 搜索任务配置
        :return: bool 是否成功
        """
        try:
            start_time = task_config["start_time"]
            end_time = task_config["end_time"]
            
            print("正在选择时间范围...")
            
            # 等待页面完全加载
            time.sleep(1)
            
            # 选择开始时间
            print(f"选择开始时间: {start_time}")
            start_time_select = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "HomeModel_TimeFrom"))
            )
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView(true);", start_time_select)
            time.sleep(0.5)
            
            # 确保元素可见
            self.driver.execute_script("arguments[0].style.display='block';", start_time_select)
            self.driver.execute_script("arguments[0].style.visibility='visible';", start_time_select)
            time.sleep(0.5)
            
            # 尝试选择值
            try:
                Select(start_time_select).select_by_value(start_time)
            except:
                print("尝试使用JavaScript选择开始时间")
                self.driver.execute_script(f"arguments[0].value = '{start_time}';", start_time_select)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", start_time_select)
            
            time.sleep(0.5)
            
            # 选择结束时间
            print(f"选择结束时间: {end_time}")
            end_time_select = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "HomeModel_TimeTo"))
            )
            
            # 滚动到元素位置
            self.driver.execute_script("arguments[0].scrollIntoView(true);", end_time_select)
            time.sleep(0.5)
            
            # 确保元素可见
            self.driver.execute_script("arguments[0].style.display='block';", end_time_select)
            self.driver.execute_script("arguments[0].style.visibility='visible';", end_time_select)
            time.sleep(0.5)
            
            # 尝试选择值
            try:
                Select(end_time_select).select_by_value(end_time)
            except:
                print("尝试使用JavaScript选择结束时间")
                self.driver.execute_script(f"arguments[0].value = '{end_time}';", end_time_select)
                self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", end_time_select)
            
            time.sleep(0.5)
            
            # 验证选择是否成功
            start_value = start_time_select.get_attribute("value")
            end_value = end_time_select.get_attribute("value")
            print(f"开始时间当前值: {start_value}")
            print(f"结束时间当前值: {end_value}")
            
            if start_value == start_time and end_value == end_time:
                print("时间范围选择完成")
                return True
            else:
                print("时间范围选择可能未成功")
                return False
                
        except Exception as e:
            print(f"选择时间时发生错误: {str(e)}")
            return False

    def select_weekdays(self, task_config):
        """
        选择星期几
        :param task_config: 搜索任务配置
        :return: bool 是否成功
        """
        try:
            weekdays = task_config["selected_days"]
            include_holidays = task_config["include_holidays"]
            
            print("正在选择星期几...")
            
            # 等待页面完全加载
            time.sleep(1)
            
            # 找到所有的星期几复选框
            checkboxes = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//input[@name='HomeModel.SelectedWeekDays']"))
            )
            
            if not checkboxes:
                print("未找到星期几复选框")
                return False
                
            print(f"找到 {len(checkboxes)} 个星期几复选框")
            
            # 遍历并选中指定的复选框
            for checkbox in checkboxes:
                value = checkbox.get_attribute("value")
                if not value:
                    print("复选框没有value属性")
                    continue
                    
                # 检查是否是节假日复选框
                is_holiday = value == "8"
                
                # 如果是节假日复选框
                if is_holiday:
                    if include_holidays:
                        print("尝试选择节假日")
                        self._click_checkbox(checkbox)
                # 如果是普通星期几复选框
                elif int(value) in weekdays:
                    print(f"尝试选择星期 {value}")
                    self._click_checkbox(checkbox)
            
            # 验证选择是否成功
            selected_values = []
            for checkbox in checkboxes:
                if checkbox.is_selected():
                    selected_values.append(checkbox.get_attribute("value"))
            
            print(f"已选择的星期几: {selected_values}")
            
            # 检查是否所有需要的星期几都被选中
            all_selected = True
            for day in weekdays:
                if str(day) not in selected_values:
                    all_selected = False
                    break
            
            if include_holidays and "8" not in selected_values:
                all_selected = False
            
            if all_selected:
                print("成功选择指定的星期几")
                return True
            else:
                print("星期几选择可能未完全成功")
                return False
                
        except Exception as e:
            print(f"选择星期几时发生错误: {str(e)}")
            return False
            
    def _click_checkbox(self, checkbox):
        """
        点击复选框的辅助方法
        :param checkbox: 复选框元素
        """
        try:
            # 滚动到复选框位置
            self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
            time.sleep(0.5)
            
            # 确保复选框可见
            self.driver.execute_script("arguments[0].style.display='block';", checkbox)
            self.driver.execute_script("arguments[0].style.visibility='visible';", checkbox)
            time.sleep(0.5)
            
            # 尝试点击
            try:
                checkbox.click()
            except:
                # 如果直接点击失败，尝试使用 JavaScript 点击
                self.driver.execute_script("arguments[0].click();", checkbox)
            
            time.sleep(0.5)
            
        except Exception as e:
            print(f"点击复选框时发生错误: {str(e)}")
            raise 