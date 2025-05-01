from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import sys

def setup_driver(chromedriver_path=None):
    try:
        # 设置 Chrome 选项
        chrome_options = Options()
        # chrome_options.add_argument('--headless')  # 无头模式，取消注释可以隐藏浏览器窗口
        
        # 添加一些额外的选项来避免常见问题
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        
        # 获取当前 Python 解释器的位数
        is_64bits = sys.maxsize > 2**32
        
        # 根据系统位数选择合适的 ChromeDriver
        if is_64bits:
            print("使用 64 位 ChromeDriver")
        else:
            print("使用 32 位 ChromeDriver")
        
        # 初始化 WebDriver
        if chromedriver_path and os.path.exists(chromedriver_path):
            print(f"使用手动指定的 ChromeDriver 路径: {chromedriver_path}")
            # 检查路径是否指向可执行文件
            if not chromedriver_path.endswith('.exe'):
                chromedriver_path = os.path.join(chromedriver_path, 'chromedriver.exe')
                print(f"尝试使用路径: {chromedriver_path}")
            
            if not os.path.exists(chromedriver_path):
                raise FileNotFoundError(f"ChromeDriver 可执行文件不存在: {chromedriver_path}")
            
            service = Service(executable_path=chromedriver_path)
        else:
            print("使用自动下载的 ChromeDriver")
            service = Service(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        print(f"初始化浏览器时发生错误: {str(e)}")
        print("请确保：")
        print("1. Chrome 浏览器已正确安装")
        print("2. Chrome 浏览器版本与 ChromeDriver 版本匹配")
        print("3. 系统环境变量 PATH 中包含 Chrome 的安装路径")
        raise 