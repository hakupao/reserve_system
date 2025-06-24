import os
import sys
import logging
from datetime import datetime
from core.chouseisan import ChouseisanUpdater
from config.chouseisan_config import CHOUSEISAN_CONFIG

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def test_chouseisan():
    """测试调整さん功能"""
    try:
        # 检查配置是否完整
        if not CHOUSEISAN_CONFIG['email'] or not CHOUSEISAN_CONFIG['password'] or not CHOUSEISAN_CONFIG['url']:
            logger.error("调整さん网站配置不完整")
            return False
            
        # ChromeDriver路径
        chromedriver_path = r"C:\Local\test\reserve_system\browser_version\chromedriver-win64\chromedriver.exe"
        if not os.path.exists(chromedriver_path):
            logger.error(f"ChromeDriver不存在: {chromedriver_path}")
            return False
            
        # 创建更新器实例
        updater = ChouseisanUpdater(
            chromedriver_path=chromedriver_path,
            headless=CHOUSEISAN_CONFIG.get('headless', False)
        )
        
        # 打开网页
        if not updater.open_url(CHOUSEISAN_CONFIG['url']):
            logger.error("打开调整さん网站失败")
            return False
            
        # 登录并更新数据
        if not updater.login(
            CHOUSEISAN_CONFIG['email'],
            CHOUSEISAN_CONFIG['password'],
            CHOUSEISAN_CONFIG['url']
        ):
            logger.error("登录调整さん网站或更新数据失败")
            return False
            
        logger.info("登录调整さん网站并更新数据成功")
        return True
        
    except Exception as e:
        logger.error(f"测试过程中发生错误: {str(e)}")
        return False
    finally:
        # 确保浏览器关闭
        if 'updater' in locals():
            updater.close()

if __name__ == "__main__":
    logger.info("开始调整さん功能测试...")
    if test_chouseisan():
        logger.info("测试完成")
    else:
        logger.error("测试失败") 