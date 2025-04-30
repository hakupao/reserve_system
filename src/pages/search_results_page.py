from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import csv
from datetime import datetime
import pandas as pd

def load_all_results(driver):
    """
    加载并获取所有搜索结果
    :param driver: WebDriver实例
    :return: 包含所有搜索结果的DataFrame
    """
    try:
        print("正在等待搜索结果加载...")
        
        # 等待表格加载完成
        table = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "facilities"))
        )
        
        # 准备数据列表
        all_data = []
        processed_rows = set()  # 用于跟踪已处理的行
        
        # 循环加载所有数据
        while True:
            try:
                # 获取当前页面的所有行
                rows = table.find_elements(By.TAG_NAME, "tr")
                if not rows:
                    print("未找到任何结果")
                    break
                    
                print(f"当前页面找到 {len(rows)} 条结果")
                
                # 处理当前页面的数据
                for row in rows[1:]:  # 跳过表头
                    try:
                        # 获取行内容的唯一标识
                        row_content = row.text.strip()
                        if not row_content or row_content in processed_rows:
                            continue
                            
                        processed_rows.add(row_content)
                        
                        # 获取所有单元格
                        cells = row.find_elements(By.TAG_NAME, "td")
                        if len(cells) < 5:
                            continue
                            
                        # 提取数据
                        facility_name = cells[1].text.strip()
                        room_name = cells[2].text.strip()
                        date = cells[3].text.strip()
                        time_slot = cells[4].text.strip()
                        
                        # 获取隐藏的输入字段
                        hidden_inputs = row.find_elements(By.TAG_NAME, "input")
                        facility_code = None
                        object_code = None
                        use_date = None
                        
                        for input_field in hidden_inputs:
                            name = input_field.get_attribute("name")
                            value = input_field.get_attribute("value")
                            
                            if "FacilityCode" in name:
                                facility_code = value
                            elif "ObjectCode" in name:
                                object_code = value
                            elif "UseDate" in name and "Display" not in name:
                                use_date = value
                        
                        # 添加到数据列表
                        all_data.append({
                            "设施名称": facility_name,
                            "室场名称": room_name,
                            "日期": date,
                            "时间段": time_slot,
                            "设施代码": facility_code,
                            "室场代码": object_code,
                            "使用日期": use_date
                        })
                        
                    except Exception as e:
                        print(f"处理行数据时发生错误: {str(e)}")
                        continue
                
                # 尝试找到并点击"さらに読み込む"按钮
                try:
                    load_more_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-quaternary')]"))
                    )
                    
                    # 滚动到按钮位置
                    driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
                    time.sleep(0.5)
                    
                    # 尝试点击按钮
                    try:
                        load_more_button.click()
                    except:
                        # 如果直接点击失败，尝试使用JavaScript点击
                        driver.execute_script("arguments[0].click();", load_more_button)
                    
                    print("点击了'さらに読み込む'按钮")
                    time.sleep(1)  # 等待新数据加载
                    
                except:
                    print("未找到'さらに読み込む'按钮，可能数据已全部加载")
                    break
                    
            except Exception as e:
                print(f"加载数据时发生错误: {str(e)}")
                break
        
        if not all_data:
            print("未能提取到任何有效数据")
            return None
            
        # 转换为DataFrame
        df = pd.DataFrame(all_data)
        print(f"成功提取 {len(df)} 条数据")
        return df
        
    except Exception as e:
        print(f"获取搜索结果时发生错误: {str(e)}")
        return None 