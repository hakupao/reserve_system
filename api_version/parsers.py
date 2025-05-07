"""
横滨市设施预约系统 解析器模块
处理HTML内容解析等功能
"""

from bs4 import BeautifulSoup
from typing import Dict

def parse_html_content(html_content: str) -> Dict:
    """解析HTML内容提取有用数据"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 创建结果字典
        result = {
            "html_content": True,
            "title": soup.title.text if soup.title else "无标题"
        }
        
        # 检查是否为错误页面
        error_heading = soup.select(".page-header h2")
        if error_heading and "処理を続行いただけません" in error_heading[0].text:
            result["error"] = True
            result["error_message"] = soup.select(".page-body")[0].text.strip() if soup.select(".page-body") else "未知错误"
            return result
        
        # 尝试提取设施表格数据
        facility_tables = soup.select("table.table-hover, table.table-bordered")
        if facility_tables:
            facilities = []
            for table in facility_tables:
                # 获取表头
                headers = [th.text.strip() for th in table.select("thead th")]
                if not headers and table.select("th"):
                    headers = [th.text.strip() for th in table.select("th")]
                
                # 获取表格行
                for row in table.select("tbody tr"):
                    facility = {}
                    cells = row.select("td")
                    for i, cell in enumerate(cells):
                        if i < len(headers):
                            # 简化表头名称，移除空格和特殊字符
                            header_name = headers[i].replace(" ", "_").replace("　", "_")
                            facility[header_name] = cell.text.strip()
                            
                            # 提取链接
                            links = cell.select("a")
                            if links:
                                facility[f"{header_name}_link"] = links[0].get("href")
                                
                            # 提取其他属性
                            data_attrs = cell.attrs
                            for attr_name, attr_value in data_attrs.items():
                                if attr_name.startswith("data-"):
                                    facility[f"{header_name}_{attr_name}"] = attr_value
                                    
                    if facility:
                        facilities.append(facility)
            
            if facilities:
                result["facilities"] = facilities
        
        # 尝试提取日期信息
        date_info = soup.select(".dateTerm, .date-term")
        if date_info:
            result["date_range"] = date_info[0].text.strip()
        
        # 尝试提取区域和设施类型信息
        info_sections = soup.select(".card-header, .section-header")
        for section in info_sections:
            section_text = section.text.strip()
            if "区" in section_text:
                result["area_info"] = section_text
            elif "施設" in section_text or "設備" in section_text:
                result["facility_type"] = section_text
            elif "用途" in section_text:
                result["purpose_info"] = section_text
        
        # 尝试提取错误信息（如果存在）
        error_messages = soup.select(".alert, .error-message")
        if error_messages:
            result["warnings"] = [msg.text.strip() for msg in error_messages]
        
        return result
        
    except Exception as e:
        print(f"解析HTML内容失败: {e}")
        return {
            "html_content": True,
            "title": "解析失败",
            "error": str(e)
        } 