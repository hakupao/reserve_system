"""
HAR文件分析工具
从浏览器导出的HAR文件中提取关键的API请求信息
"""

import json
import urllib.parse
from utils import print_log

class HARAnalyzer:
    def __init__(self, har_file_path):
        self.har_file_path = har_file_path
        self.har_data = None
        
    def load_har_file(self):
        """加载HAR文件"""
        try:
            with open(self.har_file_path, 'r', encoding='utf-8') as f:
                self.har_data = json.load(f)
            print_log(f"成功加载HAR文件: {self.har_file_path}", "INFO")
            return True
        except Exception as e:
            print_log(f"加载HAR文件失败: {e}", "ERROR")
            return False
    
    def extract_search_requests(self):
        """提取搜索相关的请求"""
        if not self.har_data:
            print_log("HAR数据未加载", "ERROR")
            return []
            
        search_requests = []
        
        try:
            entries = self.har_data.get('log', {}).get('entries', [])
            print_log(f"HAR文件包含 {len(entries)} 个网络请求", "INFO")
            
            # 查找搜索相关的请求
            search_patterns = [
                'SearchByDateTime',
                'GetSiteClosing', 
                'GetSessionInterval',
                'Home'
            ]
            
            for entry in entries:
                request = entry.get('request', {})
                url = request.get('url', '')
                method = request.get('method', '')
                
                # 检查是否是我们关心的请求
                for pattern in search_patterns:
                    if pattern in url:
                        search_requests.append({
                            'url': url,
                            'method': method,
                            'request': request,
                            'response': entry.get('response', {}),
                            'timings': entry.get('timings', {}),
                            'pattern': pattern
                        })
                        break
            
            print_log(f"找到 {len(search_requests)} 个相关请求", "INFO")
            return search_requests
            
        except Exception as e:
            print_log(f"提取请求失败: {e}", "ERROR")
            return []
    
    def analyze_search_request(self, request_data):
        """分析SearchByDateTime请求"""
        print_log("=== 分析 SearchByDateTime 请求 ===", "INFO")
        
        request = request_data['request']
        response = request_data['response']
        
        # 分析请求头
        print_log("--- 请求头 ---", "INFO")
        headers = request.get('headers', [])
        important_headers = ['content-type', 'user-agent', 'referer', 'origin', 'x-requested-with', 'accept', 'accept-language']
        
        for header in headers:
            name = header.get('name', '').lower()
            value = header.get('value', '')
            if name in important_headers:
                print_log(f"{header.get('name', '')}: {value}", "INFO")
        
        # 分析请求体
        print_log("\n--- 请求体 ---", "INFO")
        post_data = request.get('postData', {})
        
        if post_data:
            mime_type = post_data.get('mimeType', '')
            text = post_data.get('text', '')
            
            print_log(f"Content-Type: {mime_type}", "INFO")
            print_log(f"请求体内容:", "INFO")
            
            # 如果是表单数据，解析参数
            if 'application/x-www-form-urlencoded' in mime_type:
                try:
                    params = urllib.parse.parse_qsl(text)
                    print_log("解析后的表单参数:", "INFO")
                    for key, value in params:
                        print_log(f"  {key} = {value}", "INFO")
                except Exception as e:
                    print_log(f"解析表单数据失败: {e}", "ERROR")
                    print_log(f"原始数据: {text[:500]}...", "INFO")
            else:
                print_log(f"原始数据: {text[:500]}...", "INFO")
        
        # 分析响应
        print_log("\n--- 响应 ---", "INFO")
        status = response.get('status', 0)
        status_text = response.get('statusText', '')
        print_log(f"状态码: {status} {status_text}", "INFO")
        
        response_content = response.get('content', {})
        response_text = response_content.get('text', '')
        if response_text:
            try:
                response_json = json.loads(response_text)
                print_log(f"响应内容: {json.dumps(response_json, ensure_ascii=False, indent=2)}", "INFO")
            except json.JSONDecodeError:
                print_log(f"响应内容 (非JSON): {response_text[:200]}...", "INFO")
    
    def generate_code_template(self, search_requests):
        """根据分析结果生成代码模板"""
        print_log("\n=== 生成代码模板 ===", "INFO")
        
        # 查找成功的SearchByDateTime请求
        search_request = None
        for req in search_requests:
            if req['pattern'] == 'SearchByDateTime':
                response = req['response']
                if response.get('status') == 200:
                    search_request = req
                    break
        
        if not search_request:
            print_log("未找到成功的SearchByDateTime请求", "ERROR")
            return
        
        request = search_request['request']
        post_data = request.get('postData', {})
        
        if not post_data:
            print_log("SearchByDateTime请求没有POST数据", "ERROR")
            return
        
        text = post_data.get('text', '')
        if not text:
            print_log("POST数据为空", "ERROR")
            return
        
        try:
            # 解析表单参数
            params = urllib.parse.parse_qsl(text)
            
            print_log("Python代码模板:", "INFO")
            print_log("```python", "INFO")
            print_log("# 基于HAR分析的正确参数", "INFO")
            print_log("form_data = {", "INFO")
            
            for key, value in params:
                print_log(f"    '{key}': '{value}',", "INFO")
            
            print_log("}", "INFO")
            print_log("```", "INFO")
            
            # 生成请求头模板
            print_log("\n请求头模板:", "INFO")
            print_log("```python", "INFO")
            print_log("headers = {", "INFO")
            
            headers = request.get('headers', [])
            important_headers = ['content-type', 'user-agent', 'referer', 'origin', 'x-requested-with', 'accept', 'accept-language']
            
            for header in headers:
                name = header.get('name', '').lower()
                value = header.get('value', '')
                if name in important_headers:
                    print_log(f"    '{header.get('name', '')}': '{value}',", "INFO")
            
            print_log("}", "INFO")
            print_log("```", "INFO")
            
        except Exception as e:
            print_log(f"生成代码模板失败: {e}", "ERROR")
    
    def run_analysis(self):
        """运行完整分析"""
        print_log("开始HAR文件分析...", "INFO")
        print_log("=" * 60, "INFO")
        
        if not self.load_har_file():
            return False
        
        # 提取搜索请求
        search_requests = self.extract_search_requests()
        if not search_requests:
            print_log("未找到相关请求", "ERROR")
            return False
        
        # 分析每个请求
        for i, req_data in enumerate(search_requests):
            print_log(f"\n--- 请求 {i+1}: {req_data['pattern']} ---", "INFO")
            print_log(f"URL: {req_data['url']}", "INFO")
            print_log(f"方法: {req_data['method']}", "INFO")
            
            if req_data['pattern'] == 'SearchByDateTime':
                self.analyze_search_request(req_data)
        
        # 生成代码模板
        self.generate_code_template(search_requests)
        
        print_log("=" * 60, "INFO")
        print_log("HAR文件分析完成！", "INFO")
        
        return True

def main():
    """主程序"""
    import sys
    import os
    
    # HAR文件路径
    har_file = "output/www.shisetsu.city.yokohama.lg.jp.har"
    
    if not os.path.exists(har_file):
        print_log(f"HAR文件不存在: {har_file}", "ERROR")
        print_log("请确保HAR文件放在正确的位置", "ERROR")
        return
    
    analyzer = HARAnalyzer(har_file)
    analyzer.run_analysis()

if __name__ == "__main__":
    main() 