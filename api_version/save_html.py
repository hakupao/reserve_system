"""
HTML内容保存工具

该脚本用于保存横滨市设施预约系统的网页内容以便分析。
这是一个调试工具，主要用于了解网站结构和API返回内容。
"""

import requests
import os
import time

# 创建会话
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8,ja;q=0.7"
})

# 首先获取主页以获取token
print("正在获取主页...")
homepage_response = session.get("https://www.shisetsu.city.yokohama.lg.jp/user/Home")
with open("homepage.html", "w", encoding="utf-8") as f:
    f.write(homepage_response.text)
print(f"主页HTML已保存到 homepage.html")

# 适当延迟，避免请求过快
time.sleep(3)

# 获取设施页面
print("正在获取设施页面...")
facilities_response = session.get("https://www.shisetsu.city.yokohama.lg.jp/user/VacantFrameFacilityStatus")
with open("facilities.html", "w", encoding="utf-8") as f:
    f.write(facilities_response.text)
print(f"设施页面HTML已保存到 facilities.html")

print("\n注意: 这些HTML文件仅用于开发和调试，可以随时删除。")
print("如果需要分析其他页面，可以修改此脚本添加更多URL。") 