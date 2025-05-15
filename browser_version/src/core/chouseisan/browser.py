"""
浏览器基础操作模块
"""

import os
import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 获取模块日志记录器
logger = logging.getLogger('ChouseisanBrowser')

class Browser:
    """浏览器基础操作类"""
    
    def __init__(self, chromedriver_path, headless=False):
        """
        初始化浏览器
        
        Args:
            chromedriver_path: ChromeDriver的路径
            headless: 是否使用无头模式（默认为False，显示浏览器窗口）
        """
        self.chromedriver_path = chromedriver_path
        self.headless = headless
        self.driver = None
    
    def init_browser(self):
        """初始化浏览器"""
        logger.info("初始化浏览器...")
        
        try:
            service = Service(executable_path=self.chromedriver_path)
            options = webdriver.ChromeOptions()
            
            if self.headless:
                options.add_argument('--headless')
            
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            # 添加防止浏览器自动关闭的选项
            options.add_experimental_option("detach", True)
            
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.maximize_window()
            logger.info("浏览器初始化成功")
            return True
        
        except Exception as e:
            logger.error(f"初始化浏览器失败: {str(e)}")
            return False
    
    def open_url(self, url):
        """
        打开指定URL
        
        Args:
            url: 要打开的网址
            
        Returns:
            bool: 是否成功打开
        """
        if not self.driver:
            if not self.init_browser():
                return False
        
        try:
            logger.info(f"正在打开网址: {url}")
            self.driver.get(url)
            
            # 等待页面加载
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            logger.info("网页已成功打开")
            return True
            
        except Exception as e:
            logger.error(f"打开网页失败: {str(e)}")
            return False
    
    def close(self):
        """关闭浏览器"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("浏览器已关闭")
            except Exception as e:
                logger.error(f"关闭浏览器时出错: {str(e)}") 