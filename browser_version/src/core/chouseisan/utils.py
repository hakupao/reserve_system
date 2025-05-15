"""
工具函数模块
"""

import os
import logging

# 获取模块日志记录器
logger = logging.getLogger('ChouseisanBrowser.Utils')

def find_chromedriver_path():
    """
    尝试多种路径策略来定位ChromeDriver
    
    Returns:
        str: ChromeDriver的路径，如果未找到则返回None
    """
    logger.info("开始查找ChromeDriver路径...")
    
    # 尝试当前目录
    chromedriver_path = "chromedriver.exe"
    if os.path.exists(chromedriver_path):
        abs_path = os.path.abspath(chromedriver_path)
        logger.info(f"在当前目录找到ChromeDriver: {abs_path}")
        return abs_path
    
    # 尝试项目结构中的路径
    paths_to_try = [
        r"browser_version\chromedriver-win64\chromedriver.exe",
        r"..\..\chromedriver-win64\chromedriver.exe",
        r"..\..\..\chromedriver-win64\chromedriver.exe"
    ]
    
    for path in paths_to_try:
        if os.path.exists(path):
            abs_path = os.path.abspath(path)
            logger.info(f"在相对路径找到ChromeDriver: {abs_path}")
            return abs_path
    
    # 尝试使用基于脚本位置的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for i in range(5):  # 向上最多查找5层目录
        parent_dir = os.path.dirname(script_dir)
        if parent_dir == script_dir:  # 已经到达根目录
            break
        script_dir = parent_dir
        
        possible_path = os.path.join(script_dir, "browser_version", "chromedriver-win64", "chromedriver.exe")
        if os.path.exists(possible_path):
            logger.info(f"在绝对路径找到ChromeDriver: {possible_path}")
            return possible_path
    
    logger.error("未找到ChromeDriver")
    return None

def setup_logging(level=logging.INFO):
    """
    设置日志记录
    
    Args:
        level: 日志级别
    """
    # 配置根日志记录器
    logging.basicConfig(
        level=level, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 获取ChouseisanBrowser日志记录器并设置级别
    logger = logging.getLogger('ChouseisanBrowser')
    logger.setLevel(level)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    
    # 设置格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # 添加处理器到记录器
    logger.addHandler(console_handler)
    
    return logger 