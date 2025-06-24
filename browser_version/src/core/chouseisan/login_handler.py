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
        time.sleep(2)
        
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
        time.sleep(2)
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
        
        # 等待广告加载完成
        time.sleep(3)
        
        # 尝试点击幹事メニュー按钮，最多重试3次
        for attempt in range(3):
            try:
                # 尝试多个选择器
                selectors = [
                    # 1. 使用ID选择器
                    (By.ID, "edit-popup-open-button"),
                    # 2. 使用class组合
                    (By.CSS_SELECTOR, "button.c-btn.c-btn-primary.size-s.fill.c-icon.menu-host"),
                    # 3. 使用包含文本的XPath
                    (By.XPATH, "//button[.//div[contains(text(), '幹事メニュー')]]"),
                    # 4. 使用父元素定位
                    (By.CSS_SELECTOR, ".event-header__menu__right__host-menu button"),
                    # 5. 使用完整的class路径
                    (By.CSS_SELECTOR, ".event-header__menu__right__host-menu .c-btn.c-btn-primary")
                ]
                
                for by, value in selectors:
                    try:
                        if self.element_handler.click_element(
                            by,
                            value,
                            5,
                            f"幹事メニュー按钮 ({by}={value})"
                        ):
                            logger.info(f"使用选择器 {by}={value} 成功点击幹事メニュー按钮")
                            break
                    except Exception as e:
                        logger.debug(f"选择器 {by}={value} 点击失败: {str(e)}")
                        continue
                else:
                    # 如果所有选择器都失败，等待后重试
                    time.sleep(2)
                    continue
                
                # 等待弹出菜单加载
                time.sleep(2)
                
                # 尝试点击イベントを編集する链接，最多重试3次
                for edit_attempt in range(3):
                    try:
                        # 尝试多个选择器
                        edit_selectors = [
                            # 1. 使用href和class组合
                            (By.CSS_SELECTOR, "a[href*='/schedule/editEvent'] div.edit-popup__content__menu"),
                            # 2. 使用data-v属性
                            (By.CSS_SELECTOR, "a[data-v-6df4c216] div[data-v-6df4c216]"),
                            # 3. 使用文本内容
                            (By.XPATH, "//a[.//div[contains(text(), 'イベントを編集する')]]"),
                            # 4. 使用href
                            (By.CSS_SELECTOR, "a[href*='/schedule/editEvent']"),
                            # 5. 使用class
                            (By.CSS_SELECTOR, "div.edit-popup__content__menu.color-normal.c-icon.edit")
                        ]
                        
                        for by, value in edit_selectors:
                            try:
                                if self.element_handler.click_element(
                                    by,
                                    value,
                                    5,
                                    f"イベントを編集する链接 ({by}={value})"
                                ):
                                    logger.info(f"使用选择器 {by}={value} 成功点击イベントを編集する链接")
                                    logger.info("成功导航到编辑页面")
                                    return True
                            except Exception as e:
                                logger.debug(f"选择器 {by}={value} 点击失败: {str(e)}")
                                continue
                        
                        # 如果所有选择器都失败，等待后重试
                        time.sleep(2)
                        
                    except Exception as e:
                        logger.error(f"点击イベントを編集する链接时出错: {str(e)}")
                        time.sleep(2)
                        continue
                
                # 如果所有尝试都失败，返回False
                logger.error("无法点击イベントを編集する链接")
                return False
                
            except Exception as e:
                logger.error(f"点击幹事メニュー按钮时出错: {str(e)}")
                time.sleep(2)
                continue
        
        # 如果所有尝试都失败，返回False
        logger.error("无法点击幹事メニュー按钮")
        return False 