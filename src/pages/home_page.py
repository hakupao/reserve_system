from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
from .date_time_input import DateTimeInput

def open_website(driver, url):
    try:
        print(f"正在打开网站: {url}")
        driver.get(url)
        
        # 等待页面加载完成
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # 等待额外的 2 秒确保页面完全加载
        time.sleep(1)
        
        print("网站已成功打开")
        return True
    except Exception as e:
        print(f"打开网站时发生错误: {str(e)}")
        return False

def click_date_tab_button(driver):
    try:
        print("正在点击'日時から探す'标签...")
        button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'nav-link')]//li[contains(@class, 'tab-name') and contains(text(), '日時から探す')]"))
        )
        button.click()
        time.sleep(1)
        return True
    except Exception as e:
        print(f"点击标签时发生错误: {str(e)}")
        return False

def check_badminton_checkbox(driver):
    try:
        print("正在查找并勾选羽毛球复选框...")
        
        # 等待页面完全加载
        time.sleep(0.5)
        
        # 打印当前页面标题和URL，用于调试
        print(f"当前页面标题: {driver.title}")
        print(f"当前页面URL: {driver.current_url}")
        
        # 尝试多种定位方式
        try:
            # 方法1：使用 label 文本定位
            label = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//label[normalize-space()='バドミントン']"))
            )
            print("找到羽毛球标签")
            
            # 获取对应的复选框
            checkbox_id = label.get_attribute("for")
            checkbox = driver.find_element(By.ID, checkbox_id)
            print(f"找到对应的复选框，ID: {checkbox_id}")
            
            # 滚动到元素位置
            driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
            time.sleep(0.3)
            
            # 确保复选框可见
            driver.execute_script("arguments[0].style.display='block';", checkbox)
            driver.execute_script("arguments[0].style.visibility='visible';", checkbox)
            time.sleep(0.3)
            
            # 尝试点击
            try:
                checkbox.click()
            except:
                # 如果直接点击失败，尝试使用 JavaScript 点击
                driver.execute_script("arguments[0].click();", checkbox)
            
            print("成功勾选羽毛球复选框")
            return True
            
        except Exception as e:
            print(f"尝试定位复选框时发生错误: {str(e)}")
            return False
            
    except Exception as e:
        print(f"勾选复选框时发生错误: {str(e)}")
        return False

def input_date_range(driver):
    """
    使用DateTimeInput类输入日期范围
    """
    date_time_input = DateTimeInput(driver)
    return date_time_input.input_date_range()

def select_time_range(driver, task_config):
    """
    使用DateTimeInput类选择时间范围
    :param driver: WebDriver实例
    :param task_config: 搜索任务配置
    :return: bool 是否成功
    """
    date_time_input = DateTimeInput(driver)
    return date_time_input.select_time_range(task_config)

def select_all_weekdays(driver, task_config):
    """
    使用DateTimeInput类选择所有星期几
    :param driver: WebDriver实例
    :param task_config: 搜索任务配置
    :return: bool 是否成功
    """
    date_time_input = DateTimeInput(driver)
    return date_time_input.select_weekdays(task_config)

def select_empty_slots(driver):
    try:
        print("正在选择'空きコマ'...")
        
        # 等待页面完全加载
        time.sleep(0.5)
        
        # 找到并点击空きコマ的单选按钮
        empty_slots_radio = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='空きコマ']"))
        )
        
        # 滚动到元素位置
        driver.execute_script("arguments[0].scrollIntoView(true);", empty_slots_radio)
        time.sleep(0.3)
        
        # 点击
        empty_slots_radio.click()
        
        print("成功选择'空きコマ'")
        return True
    except Exception as e:
        print(f"选择'空きコマ'时发生错误: {str(e)}")
        return False

def click_area_filter_button(driver):
    try:
        print("正在点击'区名などで絞り込む'按钮...")
        
        # 等待页面完全加载
        time.sleep(0.5)
        
        # 找到并点击按钮
        filter_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '区名などで絞り込む')]"))
        )
        
        # 滚动到元素位置
        driver.execute_script("arguments[0].scrollIntoView(true);", filter_button)
        time.sleep(0.3)
        
        # 点击
        filter_button.click()
        
        print("成功点击'区名などで絞り込む'按钮")
        return True
    except Exception as e:
        print(f"点击'区名などで絞り込む'按钮时发生错误: {str(e)}")
        return False

def select_specific_areas(driver):
    try:
        print("正在选择指定区域...")
        
        # 等待页面完全加载
        time.sleep(0.5)
        
        # 要选择的区域列表
        areas = [
            "神奈川区",
            "中区",
            "西区"
        ]
        
        # 遍历并选择每个区域
        for area in areas:
            # 找到对应的复选框
            checkbox_label = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, f"//label[normalize-space()='{area}']"))
            )
            
            # 获取对应的复选框
            checkbox_id = checkbox_label.get_attribute("for")
            checkbox = driver.find_element(By.ID, checkbox_id)
            
            # 滚动到复选框位置
            driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
            time.sleep(0.1)
            
            # 确保复选框可见
            driver.execute_script("arguments[0].style.display='block';", checkbox)
            driver.execute_script("arguments[0].style.visibility='visible';", checkbox)
            time.sleep(0.1)
            
            # 尝试点击
            try:
                checkbox.click()
            except:
                # 如果直接点击失败，尝试使用 JavaScript 点击
                driver.execute_script("arguments[0].click();", checkbox)
            
            print(f"成功选择区域: {area}")
        
        print("所有指定区域选择完成")
        return True
    except Exception as e:
        print(f"选择区域时发生错误: {str(e)}")
        return False

def click_search_button(driver):
    try:
        print("正在点击搜索按钮...")
        
        # 等待页面完全加载
        time.sleep(1)
        
        # 使用JavaScript点击按钮
        click_script = """
        var button = document.querySelector('button.btn-lg.btn-secondary');
        if (button) {
            // 确保按钮可见
            button.style.display = 'block';
            button.scrollIntoView({block: 'center', behavior: 'smooth'});
            
            // 模拟点击
            var event = new MouseEvent('click', {
                view: window,
                bubbles: true,
                cancelable: true
            });
            
            // 直接触发点击事件
            button.dispatchEvent(event);
            
            return true;
        }
        return false;
        """
        
        # 执行点击脚本
        result = driver.execute_script(click_script)
        if not result:
            print("未找到搜索按钮")
            return False
            
        # 等待页面响应
        time.sleep(1)
        
        # 检查是否成功跳转
        current_url = driver.current_url
        if "VacantFrameFacilityStatus" in current_url:
            print("成功跳转到搜索结果页面")
            return True
        else:
            print("未成功跳转到搜索结果页面")
            return False
            
    except Exception as e:
        print(f"点击搜索按钮时发生错误: {str(e)}")
        return False 