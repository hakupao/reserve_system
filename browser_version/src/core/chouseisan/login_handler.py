"""
登录处理模块
"""

import logging
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# 获取模块日志记录器
logger = logging.getLogger('ChouseisanBrowser.LoginHandler')

class LoginHandler:
    """登录处理类"""
    
    def __init__(self, element_handler):
        """
        初始化登录处理器
        
        Args:
            element_handler: ElementHandler实例
        """
        self.element_handler = element_handler
    
    def perform_login(self, email, password):
        """
        执行登录操作
        
        Args:
            email: 登录邮箱
            password: 登录密码
            
        Returns:
            bool: 是否成功登录
        """
        logger.info("开始执行登录操作...")
        
        # 尝试点击登录按钮
        login_success = False
        
        # 尝试使用用户提供的选择器
        if self.element_handler.click_element(
            By.CSS_SELECTOR, 
            "#header_user_menu_ul a", 
            3, 
            "登录按钮"
        ):
            login_success = True
        
        # 如果找不到，尝试其他可能的选择器
        if not login_success and self.element_handler.click_element(
            By.XPATH, 
            "//a[contains(text(), 'Register / Login') or contains(text(), '会員登録 / ログイン')]", 
            3, 
            "备用登录按钮"
        ):
            login_success = True
        
        if not login_success:
            logger.error("无法找到登录按钮")
            return False
            
        # 等待登录表单加载
        time.sleep(0.5)
        
        # 输入邮箱
        if not self.element_handler.input_text(
            By.ID, 
            "form_email", 
            email, 
            True, 
            "邮箱输入框"
        ):
            if not self.element_handler.input_text(
                By.NAME, 
                "email", 
                email, 
                True, 
                "备用邮箱输入框"
            ):
                logger.error("无法找到邮箱输入框")
                return False
        
        # 输入密码
        if not self.element_handler.input_text(
            By.ID, 
            "form_password", 
            password, 
            True, 
            "密码输入框"
        ):
            if not self.element_handler.input_text(
                By.NAME, 
                "password", 
                password, 
                True, 
                "备用密码输入框"
            ):
                logger.error("无法找到密码输入框")
                return False
        
        # 勾选"Remember Me"复选框
        try:
            driver = self.element_handler.driver
            remember_checkbox = driver.find_element(By.ID, "form_remember")
            if not remember_checkbox.is_selected():
                remember_checkbox.click()
                logger.info("勾选'Remember Me'复选框成功")
        except NoSuchElementException:
            try:
                driver = self.element_handler.driver
                remember_checkbox = driver.find_element(By.NAME, "remember")
                if not remember_checkbox.is_selected():
                    remember_checkbox.click()
                    logger.info("使用备用选择器勾选'Remember Me'复选框成功")
            except NoSuchElementException as e:
                logger.warning(f"未找到'Remember Me'复选框，继续登录: {str(e)}")
        
        # 点击登录按钮
        if not self.element_handler.click_element(
            By.ID, 
            "form_submit", 
            3, 
            "登录提交按钮"
        ):
            if not self.element_handler.click_element(
                By.XPATH, 
                "//input[@type='submit'] | //button[@type='submit']", 
                3, 
                "备用登录提交按钮"
            ):
                logger.error("无法找到登录提交按钮")
                return False
        
        # 等待登录完成
        time.sleep(0.5)
        logger.info("登录过程完成")
        return True
    
    def navigate_to_edit_page(self, url):
        """
        导航到编辑页面
        
        Args:
            url: 要导航到的URL
            
        Returns:
            bool: 是否成功导航
        """
        logger.info(f"开始导航到编辑页面: {url}")
        
        # 获取driver
        driver = self.element_handler.driver
        
        # 重新打开网址
        driver.get(url)
        
        # 等待页面加载
        if not self.element_handler.wait_for_page_load(10):
            logger.error("页面加载失败")
            return False
        
        logger.info("网页已重新加载完成")
        
        # 点击幹事メニュー按钮
        if not self.element_handler.click_element(
            By.ID, 
            "edit-popup-open-button", 
            10, 
            "幹事メニュー按钮"
        ):
            logger.error("无法找到幹事メニュー按钮")
            return False
        
        # 等待并点击イベントを編集する链接
        if not self.element_handler.click_element(
            By.XPATH, 
            "//a[contains(@href, '/schedule/editEvent')]", 
            10, 
            "イベントを編集する链接"
        ):
            logger.error("无法找到イベントを編集する链接")
            return False
        
        # 等待页面加载完成
        time.sleep(1)
        logger.info("成功导航到编辑页面")
        return True 