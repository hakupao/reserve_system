"""
元素操作工具模块
"""

import logging
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 获取模块日志记录器
logger = logging.getLogger('ChouseisanBrowser.ElementHandler')

class ElementHandler:
    """元素操作工具类"""
    
    def __init__(self, driver):
        """
        初始化元素处理器
        
        Args:
            driver: WebDriver实例
        """
        self.driver = driver
    
    def click_element(self, by, value, timeout=10, description="元素"):
        """
        等待并点击元素
        
        Args:
            by: 定位方式，例如By.ID
            value: 定位值
            timeout: 超时时间
            description: 元素描述，用于日志
            
        Returns:
            bool: 是否成功点击
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            logger.info(f"点击{description}成功")
            return True
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"无法找到或点击{description}: {str(e)}")
            return False
    
    def input_text(self, by, value, text, clear_first=True, description="输入框"):
        """
        在输入框中输入文本
        
        Args:
            by: 定位方式，例如By.ID
            value: 定位值
            text: 要输入的文本
            clear_first: 是否先清空输入框
            description: 元素描述，用于日志
            
        Returns:
            bool: 是否成功输入
        """
        try:
            input_element = self.driver.find_element(by, value)
            if clear_first:
                input_element.clear()
            input_element.send_keys(text)
            logger.info(f"在{description}中输入文本成功")
            return True
        except NoSuchElementException as e:
            logger.error(f"无法找到{description}: {str(e)}")
            return False
    
    def find_element(self, by, value, timeout=10, description="元素"):
        """
        查找元素
        
        Args:
            by: 定位方式，例如By.ID
            value: 定位值
            timeout: 超时时间
            description: 元素描述，用于日志
            
        Returns:
            element: 找到的元素，未找到则返回None
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            logger.info(f"找到{description}")
            return element
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"未找到{description}: {str(e)}")
            return None
    
    def find_elements(self, by, value, timeout=10, description="元素集合"):
        """
        查找多个元素
        
        Args:
            by: 定位方式，例如By.XPATH
            value: 定位值
            timeout: 超时时间
            description: 元素描述，用于日志
            
        Returns:
            elements: 找到的元素列表，未找到则返回空列表
        """
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value))
            )
            logger.info(f"找到{len(elements)}个{description}")
            return elements
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"未找到{description}: {str(e)}")
            return []
    
    def wait_for_page_load(self, timeout=10):
        """
        等待页面加载完成
        
        Args:
            timeout: 超时时间
            
        Returns:
            bool: 是否成功加载
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(("tag name", "body"))
            )
            logger.info("页面加载完成")
            return True
        except TimeoutException as e:
            logger.error(f"等待页面加载超时: {str(e)}")
            return False 