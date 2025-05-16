"""
浏览器基础操作模块
"""

import os
import logging
import time
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# 获取模块日志记录器
logger = logging.getLogger('ChouseisanBrowser')

# 尝试不同的导入方式来获取setup_driver函数
setup_driver = None

# 方法1：添加项目根目录到系统路径
try:
    # 添加项目根目录到系统路径
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../'))
    sys.path.insert(0, project_root)
    from browser_version.src.utils.driver_utils import setup_driver
    logger.info("成功通过绝对导入获取setup_driver")
except ImportError:
    logger.info("绝对导入失败，尝试其他方法")

# 方法2：直接导入utils模块
if setup_driver is None:
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "driver_utils", 
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../utils/driver_utils.py'))
        )
        driver_utils = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(driver_utils)
        setup_driver = driver_utils.setup_driver
        logger.info("成功通过动态导入获取setup_driver")
    except (ImportError, FileNotFoundError, AttributeError):
        logger.error("所有导入方法都失败了")
        raise ImportError("无法导入setup_driver函数，请检查项目结构")

class Browser:
    """浏览器基础操作类"""
    
    def __init__(self, chromedriver_path=None, headless=True):
        """
        初始化浏览器
        
        Args:
            chromedriver_path: ChromeDriver的路径（可选）
            headless: 是否使用无头模式（默认为True，不显示浏览器窗口）
        """
        self.chromedriver_path = chromedriver_path
        self.headless = headless
        self.driver = None
    
    def init_browser(self):
        """初始化浏览器"""
        logger.info("初始化浏览器...")
        
        try:
            self.driver = setup_driver(self.chromedriver_path)
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