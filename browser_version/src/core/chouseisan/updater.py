"""
ChouseisanUpdater类 - 主模块
用于打开调整さん(chouseisan.com)网站
"""

import os
import sys
import time
import logging
from .browser import Browser
from .element_handler import ElementHandler
from .login_handler import LoginHandler
from .results_handler import ResultsHandler
from .utils import find_chromedriver_path, setup_logging

# 配置根日志记录器
logger = logging.getLogger('ChouseisanBrowser')

class ChouseisanUpdater:
    """简化版调整さん网站浏览器，整合了所有功能"""
    
    def __init__(self, chromedriver_path, headless=False):
        """
        初始化ChouseisanUpdater
        
        Args:
            chromedriver_path: ChromeDriver的路径
            headless: 是否使用无头模式（默认为False，显示浏览器窗口）
        """
        self.chromedriver_path = chromedriver_path
        self.headless = headless
        
        # 初始化浏览器
        self.browser = Browser(chromedriver_path, headless)
        self.driver = None
        
        # 其他处理器将在初始化浏览器后创建
        self.element_handler = None
        self.login_handler = None
        self.results_handler = None
    
    def init_handlers(self):
        """初始化所有处理器"""
        if not self.driver:
            return False
            
        self.element_handler = ElementHandler(self.driver)
        self.login_handler = LoginHandler(self.element_handler)
        self.results_handler = ResultsHandler(self.element_handler)
        return True
    
    def open_url(self, url):
        """
        打开指定URL
        
        Args:
            url: 要打开的网址
            
        Returns:
            bool: 是否成功打开
        """
        result = self.browser.open_url(url)
        if result:
            # 保存driver引用并初始化处理器
            self.driver = self.browser.driver
            self.init_handlers()
        return result
    
    def login(self, email, password, url):
        """
        登录到调整さん网站并更新数据
        
        Args:
            email: 登录邮箱
            password: 登录密码
            url: 调整さん网站URL
            
        Returns:
            bool: 是否成功登录和更新
        """
        if not self.driver:
            logger.error("浏览器未初始化，无法登录")
            return False
            
        try:
            logger.info("开始登录和更新流程...")
            
            # 执行登录
            if not self.login_handler.perform_login(email, password):
                logger.error("登录失败")
                return False
            
            # 导航到编辑页面
            if not self.login_handler.navigate_to_edit_page(url):
                logger.error("导航到编辑页面失败")
                return False
            
            # 删除现有时间段
            success, textarea = self.results_handler.delete_existing_slots()
            if not success or textarea is None:
                logger.error("删除现有时间段失败")
                return False
            
            # 使用搜索结果更新输入框
            if not self.results_handler.update_with_search_results(textarea):
                logger.error("更新搜索结果失败")
                return False
            
            logger.info("登录和更新流程成功完成")
            return True
            
        except Exception as e:
            logger.error(f"登录过程中出现错误: {str(e)}")
            return False
    
    def close(self):
        """关闭浏览器"""
        self.browser.close()

def main():
    """主函数"""
    # 设置日志
    setup_logging()
    
    # 尝试从配置文件加载URL
    config = {}
    try:
        sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        from config.chouseisan_config import CHOUSEISAN_CONFIG
        config = CHOUSEISAN_CONFIG
    except ImportError:
        logger.error("未找到配置文件，请确保config/chouseisan_config.py文件存在")
        return False
    
    # 获取URL、登录信息和无头模式设置
    url = config.get('url', '')
    email = config.get('email', '')
    password = config.get('password', '')
    headless = config.get('headless', False)
    
    if not url:
        logger.error("配置文件中未指定URL")
        return False
    
    # 检查是否提供了登录信息
    login_enabled = bool(email and password)
    
    # 查找ChromeDriver路径
    chromedriver_path = find_chromedriver_path()
    if not chromedriver_path:
        logger.error("未找到ChromeDriver，请确保chromedriver.exe在合适的位置")
        return False
    
    # 显示配置信息
    print("\n===== 调整さん网站浏览器 =====")
    print(f"ChromeDriver路径: {chromedriver_path}")
    print(f"打开URL: {url}")
    if login_enabled:
        print(f"登录账号: {email}")
        print("登录密码: ******")
    else:
        print("登录功能: 已禁用 (未提供账号密码)")
    print(f"无头模式: {'是' if headless else '否'}")
    print("==============================\n")
    
    # 初始化浏览器并打开网页
    browser = ChouseisanUpdater(chromedriver_path, headless=headless)
    if browser.open_url(url):
        print("浏览器已成功打开，网页已加载。")
        
        # 如果提供了登录信息，尝试登录
        if login_enabled:
            print("正在尝试登录...")
            if browser.login(email, password, url):
                print("登录成功！")
            else:
                print("登录失败，请检查账号密码是否正确。")
        
        print("浏览器会保持打开状态，请手动关闭。")
        print("\n按Ctrl+C可以关闭此程序（浏览器窗口会保持打开）")
        
        # 使程序保持运行，但不会关闭浏览器
        try:
            # 无限等待，直到用户按Ctrl+C中断
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n程序已退出，浏览器窗口仍保持打开")
        
        return True
    else:
        print("打开网页失败")
        return False

if __name__ == "__main__":
    main() 