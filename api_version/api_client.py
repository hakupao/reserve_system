"""
横滨市设施预约系统 API 客户端
处理与API服务器的所有通信
"""

import time
import requests
import random
import string
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from config import API_CONFIG, SEARCH_CONFIG

from parsers import parse_html_content

class YokohamaFacilityAPI:
    def __init__(self):
        """初始化API客户端"""
        self.base_url = API_CONFIG["base_url"]
        self.session = requests.Session()
        self.token = None
        self.token_expire_time = None
        self.last_request_time = 0
        
        # 设置默认请求头
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8,ja;q=0.7",
            "Origin": "https://www.shisetsu.city.yokohama.lg.jp",
            "Referer": "https://www.shisetsu.city.yokohama.lg.jp/"
        })

    def _wait_for_interval(self):
        """等待请求间隔"""
        if self.last_request_time > 0:
            elapsed = time.time() - self.last_request_time
            if elapsed < API_CONFIG["request_interval"]:
                wait_time = API_CONFIG["request_interval"] - elapsed
                print(f"等待 {wait_time:.1f} 秒...")
                time.sleep(wait_time)
        self.last_request_time = time.time()

    def _make_request(self, method: str, url: str, raise_for_status: bool = True, **kwargs) -> requests.Response:
        """发送HTTP请求并处理重试逻辑"""
        self._wait_for_interval()
        
        headers = kwargs.get('headers', {})
        
        # 添加通用请求头
        common_headers = {
            'origin': 'https://www.shisetsu.city.yokohama.lg.jp',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            'request-context': 'appId=cid-v1:70e4af49-efc9-4f8c-a767-3b815b116b3a',
            'traceparent': '00-' + ''.join(random.choices(string.hexdigits, k=32)).lower() + '-' + ''.join(random.choices(string.hexdigits, k=16)).lower() + '-01'
        }
        
        headers.update(common_headers)
        
        # 处理不同类型的请求数据
        if method.upper() == 'POST':
            # 检查请求数据类型
            data = kwargs.get('data', None)
            
            # 如果是字典类型且包含token字段，且未指定Content-Type，则使用multipart/form-data
            if isinstance(data, dict) and '__RequestVerificationToken' in data and 'content-type' not in headers:
                boundary = '----WebKitFormBoundary' + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                headers['content-type'] = f'multipart/form-data; boundary={boundary}'
                
                # 将普通form数据转换为multipart格式
                form_data = ""
                for key, value in data.items():
                    form_data += f"--{boundary}\r\n"
                    form_data += f"Content-Disposition: form-data; name=\"{key}\"\r\n\r\n"
                    form_data += f"{value}\r\n"
                form_data += f"--{boundary}--\r\n"
                
                kwargs['data'] = form_data
            # 如果是字符串类型且包含 RequestVerificationToken 但未指定Content-Type
            elif isinstance(data, str) and 'RequestVerificationToken' in data and 'content-type' not in headers:
                headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        
        kwargs['headers'] = headers
        max_retries = API_CONFIG.get("retry_times", 3)
        retry_count = 0
        
        while retry_count < max_retries:
            retry_count += 1
            try:
                print(f"正在发送{method}请求 (尝试 {retry_count}/{max_retries}): {url}")
                response = self.session.request(method, url, **kwargs)
                if raise_for_status:
                    response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                print(f"请求失败: {e}")
                if retry_count < max_retries:
                    wait_time = API_CONFIG.get("retry_delay", 5) * (2 ** (retry_count - 1))  # 指数退避
                    print(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    raise

    def _init_session(self) -> bool:
        """初始化会话"""
        try:
            # 重置会话以确保干净状态
            self.session = requests.Session()
            self.session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8,ja;q=0.7",
                "Origin": "https://www.shisetsu.city.yokohama.lg.jp",
                "Referer": "https://www.shisetsu.city.yokohama.lg.jp/"
            })
            
            # 访问主页
            print("正在初始化会话...")
            response = self._make_request("GET", f"{self.base_url}/Home")
            
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找包含token的input元素
            token_input = soup.find('input', {'name': '__RequestVerificationToken'})
            if token_input and 'value' in token_input.attrs:
                self.token = token_input['value']
                self.token_expire_time = time.time() + API_CONFIG["session_expire"]
                print("成功获取验证token")
                
                # 获取站点状态和会话间隔，模拟浏览器自动请求
                self._get_site_status()
                self._get_session_interval()
                
                # 确保会话完全初始化
                time.sleep(1)
                
                return True
            else:
                print("未找到验证token")
                return False
                
        except Exception as e:
            print(f"初始化会话失败: {e}")
            return False

    def _get_site_status(self) -> Optional[Dict]:
        """获取站点状态"""
        try:
            url = f"{self.base_url}/api/Header/GetSiteClosing"
            print(f"正在获取站点状态: {url}")
            
            # 准备表单数据
            data = {
                '__RequestVerificationToken': self.token
            }
            
            response = self._make_request(
                "POST",
                url,
                data=data,
                headers={
                    "Accept": "application/json, text/plain, */*",
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": f"{self.base_url}/Home"
                }
            )
            return response.json()
        except Exception as e:
            print(f"获取站点状态失败: {e}")
            return None

    def _get_session_interval(self) -> Optional[Dict]:
        """获取会话间隔信息"""
        try:
            url = f"{self.base_url}/api/Header/GetSessionInterval"
            print(f"正在获取会话间隔: {url}")
            
            # 准备表单数据
            data = {
                '__RequestVerificationToken': self.token
            }
            
            response = self._make_request(
                "POST",
                url,
                data=data,
                headers={
                    "Accept": "application/json, text/plain, */*",
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": f"{self.base_url}/Home"
                }
            )
            return response.json()
        except Exception as e:
            print(f"获取会话间隔失败: {e}")
            return None

    def search_facilities(self, 
                         date_from: str,
                         date_to: str,
                         time_from: str = SEARCH_CONFIG["default_time_range"]["from"],
                         time_to: str = SEARCH_CONFIG["default_time_range"]["to"],
                         areas: List[int] = None,
                         purpose_category: int = SEARCH_CONFIG["default_purpose_category"],
                         place_class_category: int = SEARCH_CONFIG["default_place_class_category"]) -> Optional[Dict]:
        """
        搜索设施
        
        Args:
            date_from: 开始日期 (YYYY-MM-DD)
            date_to: 结束日期 (YYYY-MM-DD)
            time_from: 开始时间 (HHMM)
            time_to: 结束时间 (HHMM)
            areas: 区域ID列表
            purpose_category: 用途类别
            place_class_category: 设施类别
        """
        # 每次搜索前都重新获取token
        if not self._init_session():
            print("无法初始化会话")
            return None

        if areas is None:
            areas = SEARCH_CONFIG["default_areas"]

        try:
            # 先访问主页以确保正确的会话状态
            print("访问主页以确保会话状态...")
            self._make_request(
                "GET", 
                f"{self.base_url}/Home", 
                headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
                }
            )
            
            # 准备URL编码的表单数据（处理多值字段）
            form_data = ""
            
            # 添加基本字段
            basic_fields = {
                'HomeModel.SearchByDateTimeModel.SelectedPurposeCategory': str(purpose_category),
                'HomeModel.SearchByDateTimeModel.SelectedPurpose': '1',
                'HomeModel.DateFrom': date_from,
                'HomeModel.DateTo': date_to,
                'HomeModel.TimeFrom': time_from,
                'HomeModel.TimeTo': time_to,
                'HomeModel.SelectedSearchTarget': '1',
                'HomeModel.SelectedPlaceClassCategory': str(place_class_category),
                'HomeModel.SelectedPurposeCategory': str(purpose_category),
                'SelectedLanguageCode': '0',
                '__RequestVerificationToken': self.token
            }
            
            # 将字段转换为URL编码格式
            for key, value in basic_fields.items():
                if form_data:
                    form_data += "&"
                form_data += f"{key}={value}"
                
            # 添加区域参数（多个同名字段）
            for area in areas:
                form_data += f"&HomeModel.SearchByDateTimeModel.SelectedArea={area}"
                
            # 添加星期参数（多个同名字段）
            for weekday in SEARCH_CONFIG["default_weekdays"]:
                form_data += f"&HomeModel.SelectedWeekDays={weekday}"

            search_url = f"{self.base_url}/Home/SearchByDateTime"
            print(f"正在发送搜索请求: {search_url}")
            print(f"请求参数: {form_data}")
            
            response = self._make_request(
                "POST",
                search_url,
                data=form_data,  # 使用拼接好的表单数据
                headers={
                    "Accept": "application/json, text/plain, */*",
                    "X-Requested-With": "XMLHttpRequest",
                    "Referer": f"{self.base_url}/Home",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
                }
            )
            
            # 检查响应内容
            import json
            result = response.json()
            print(f"收到响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
            
            # 如果返回的是相对路径，需要获取实际数据
            if isinstance(result, dict) and "Information" in result and isinstance(result["Information"], str) and (result["Information"].startswith("./") or result["Information"].startswith("/")):
                print(f"需要获取详细信息路径: {result['Information']}")
                
                # 构建完整的URL
                detail_url = f"{self.base_url}{result['Information'][1:]}" if result["Information"].startswith("./") else f"{self.base_url}{result['Information']}"
                
                # 直接访问详细页面
                print(f"尝试访问详细信息页面: {detail_url}")
                detail_response = self._make_request(
                    "GET",
                    detail_url,
                    headers={
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                        "Referer": f"{self.base_url}/Home"
                    },
                    raise_for_status=False
                )
                
                # 检查是否成功
                if detail_response.status_code == 200:
                    # 解析HTML内容
                    detail_result = parse_html_content(detail_response.text)
                    if detail_result:
                        print("成功获取详细信息")
                        result["DetailData"] = detail_result
                    else:
                        print("警告: 无法解析详细信息")
                else:
                    print(f"警告: 访问详细页面失败，状态码: {detail_response.status_code}")
            
            return result
            
        except Exception as e:
            print(f"搜索请求失败: {e}")
            return None 