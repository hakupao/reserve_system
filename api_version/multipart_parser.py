"""
Multipart/form-data 解析器
从HAR文件的multipart数据中提取表单字段
"""

import re
from typing import Dict, List, Tuple
from utils import print_log

class MultipartParser:
    def __init__(self):
        pass
    
    def parse_multipart_data(self, multipart_text: str) -> List[Tuple[str, str]]:
        """解析multipart/form-data格式的数据"""
        fields = []
        
        try:
            # 查找boundary
            boundary_match = re.search(r'------WebKitFormBoundary\w+', multipart_text)
            if not boundary_match:
                print_log("未找到boundary", "ERROR")
                return fields
            
            boundary = boundary_match.group(0)
            print_log(f"找到boundary: {boundary}", "INFO")
            
            # 按boundary分割数据
            parts = multipart_text.split(boundary)
            
            for part in parts:
                if not part.strip() or part.strip() == '--':
                    continue
                
                # 查找name属性
                name_match = re.search(r'Content-Disposition: form-data; name="([^"]*)"', part)
                if not name_match:
                    continue
                
                field_name = name_match.group(1)
                
                # 查找值（在两个换行符之后）
                lines = part.split('\n')
                value = ""
                capture_value = False
                
                for line in lines:
                    if capture_value:
                        if line.strip():  # 非空行就是值
                            value = line.strip()
                            break
                    elif line.strip() == "":  # 空行之后开始捕获值
                        capture_value = True
                
                if field_name and value:
                    fields.append((field_name, value))
                    print_log(f"解析字段: {field_name} = {value}", "INFO")
            
            print_log(f"成功解析 {len(fields)} 个字段", "INFO")
            return fields
            
        except Exception as e:
            print_log(f"解析multipart数据失败: {e}", "ERROR")
            return fields

def extract_fields_from_har():
    """从HAR文件中提取字段并生成Python代码"""
    print_log("=== 从HAR文件提取字段 ===", "INFO")
    
    # 这里是从HAR分析中提取的multipart数据
    multipart_data = """------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.SearchByDateTimeModel.SelectedPurposeCategory"

1
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.SearchByDateTimeModel.SelectedPurpose"

1
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.DateFrom"

2025-06-24
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.DateTo"

2025-07-22
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.TimeFrom"

0900
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.TimeTo"

2100
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.SelectedWeekDays"

1
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.SelectedWeekDays"

2
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.SelectedWeekDays"

3
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.SelectedWeekDays"

4
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.SelectedWeekDays"

5
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.SelectedWeekDays"

6
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.SelectedWeekDays"

7
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.SelectedWeekDays"

8
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.SelectedSearchTarget"

1
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.SearchByDateTimeModel.SelectedArea"

5
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.SearchByDateTimeModel.SelectedArea"

12
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.SearchByDateTimeModel.SelectedArea"

14
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.SearchByDateTimeModel.SelectedArea"

15
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.SearchByDateTimeModel.SelectedPlaceClassCategory"

1
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.SelectedPurposeCategory"

1
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="HomeModel.SelectedPlaceClassCategory"

1
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="SelectedLanguageCode"

0
------WebKitFormBoundary79PnBKpkagSZnIGl
Content-Disposition: form-data; name="__RequestVerificationToken"

CfDJ8GvggzThaPhHmAwC79zYTuJDgB24UfX3qD-vRdEBY8-Wh6fPuy2ho3K-cDyAoxQKKjKsvuEwantybrbPIDDoRYtR5-PKxLgxrn0YtSL69qWYHcnRWIfcT555SoprJEw23WkVjtAZrVPDcBOZXxIwNBc
------WebKitFormBoundary79PnBKpkagSZnIGl--"""
    
    parser = MultipartParser()
    fields = parser.parse_multipart_data(multipart_data)
    
    if fields:
        print_log("\n=== 生成正确的Python代码 ===", "INFO")
        
        # 生成基本字段字典
        basic_fields = {}
        area_fields = []
        weekday_fields = []
        
        for name, value in fields:
            if name == "HomeModel.SearchByDateTimeModel.SelectedArea":
                area_fields.append(value)
            elif name == "HomeModel.SelectedWeekDays":
                weekday_fields.append(value)
            else:
                basic_fields[name] = value
        
        print_log("基本字段:", "INFO")
        for name, value in basic_fields.items():
            print_log(f"  '{name}': '{value}',", "INFO")
        
        print_log(f"\n区域字段: {area_fields}", "INFO")
        print_log(f"星期字段: {weekday_fields}", "INFO")
        
        # 生成完整的代码模板
        print_log("\n=== 完整代码模板 ===", "INFO")
        print_log("```python", "INFO")
        print_log("# 基于HAR分析的正确参数配置", "INFO")
        print_log("basic_fields = {", "INFO")
        for name, value in basic_fields.items():
            if name != "__RequestVerificationToken":  # token需要动态获取
                print_log(f"    '{name}': '{value}',", "INFO")
        print_log("    '__RequestVerificationToken': self.token", "INFO")
        print_log("}", "INFO")
        print_log("", "INFO")
        print_log(f"areas = {area_fields}", "INFO")
        print_log(f"weekdays = {weekday_fields}", "INFO")
        print_log("```", "INFO")
        
        return basic_fields, area_fields, weekday_fields
    
    return None, None, None

def main():
    """主程序"""
    extract_fields_from_har()

if __name__ == "__main__":
    main() 