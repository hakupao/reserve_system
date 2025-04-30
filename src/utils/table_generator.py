import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 设置后端为Agg（非交互式）
import matplotlib.pyplot as plt
from matplotlib.table import Table
import numpy as np
import os
from matplotlib.font_manager import FontProperties

def get_chinese_font():
    """
    获取系统中可用的中文字体
    """
    # 按优先级尝试不同的中文字体
    font_list = [
        'Microsoft YaHei',  # Windows 微软雅黑
        'SimHei',          # Windows 黑体
        'SimSun',          # Windows 宋体
        'Noto Sans CJK JP',  # Linux/Mac
        'Noto Sans CJK SC',  # Linux/Mac
        'Hiragino Sans GB'   # Mac
    ]
    
    for font_name in font_list:
        try:
            font_prop = FontProperties(fname=matplotlib.font_manager.findfont(font_name))
            return font_prop
        except:
            continue
    
    # 如果没有找到任何中文字体，返回系统默认字体
    return FontProperties()

def get_column_widths(table_data):
    """
    计算每列的最佳宽度
    """
    max_widths = [0] * len(table_data[0])
    for row in table_data:
        for i, cell in enumerate(row):
            # 计算每个单元格内容的长度（考虑换行）
            lines = str(cell).split('\n')
            max_line_length = max(len(line) for line in lines)
            # 根据列的类型调整宽度权重
            if i == 0:  # 搜索类型列
                max_widths[i] = max(max_widths[i], max_line_length * 0.8)
            elif i == 3:  # 日期和时间段列
                max_widths[i] = max(max_widths[i], max_line_length * 1.2)
            else:  # 其他列
                max_widths[i] = max(max_widths[i], max_line_length)
    
    # 将宽度转换为相对比例
    total_width = sum(max_widths)
    return [width/total_width for width in max_widths]

def generate_table_image(csv_path, output_path):
    """
    从CSV文件生成表格图片
    :param csv_path: CSV文件路径
    :param output_path: 输出图片路径
    """
    # 读取CSV文件
    df = pd.read_csv(csv_path)
    
    # 获取中文字体
    chinese_font = get_chinese_font()
    
    # 合并日期和时间段
    df['日期和时间段'] = df['日期'] + ' ' + df['时间段']
    
    # 按search_type分组
    grouped = df.groupby('search_type')
    
    # 创建图形
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    
    # 根据数据行数动态调整图形大小
    num_rows = len(df) + 1  # 加1是为了表头
    fig_height = max(8, min(num_rows * 0.5, 15))  # 限制最小和最大高度
    fig_width = 12
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    ax.axis('off')
    
    # 创建表格
    table_data = []
    headers = ['时间', '设施名称', '室场名称', '日期和时间段']
    
    # 添加表头
    table_data.append(headers)
    
    # 添加数据
    for search_type, group in grouped:
        # 按设施名称和室场名称分组
        facility_groups = group.groupby(['设施名称', '室场名称'])
        for (facility, room), sub_group in facility_groups:
            # 合并日期和时间段，每两个时间段换一行
            date_times = sub_group['日期和时间段'].unique()
            formatted_times = []
            for i in range(0, len(date_times), 2):
                formatted_times.append('\n'.join(date_times[i:i+2]))
            date_times_text = '\n'.join(formatted_times)
            table_data.append([search_type, facility, room, date_times_text])
    
    # 计算最佳列宽
    col_widths = get_column_widths(table_data)
    
    # 创建表格
    table = ax.table(cellText=table_data,
                    cellLoc='center',
                    colLabels=None,
                    loc='center',
                    colWidths=col_widths,
                    cellColours=[['lightgray']*4] + [['white']*4]*(len(table_data)-1))
    
    # 设置表格样式
    table.auto_set_font_size(False)
    table.set_fontsize(9)  # 设置字体大小
    
    # 计算行高（根据内容的行数）
    row_heights = []
    for row in table_data:
        max_lines = max(len(str(cell).split('\n')) for cell in row)
        row_heights.append(max_lines * 0.025 + 0.01)  # 减小整体行高
    
    # 设置单元格边框、字体和行高
    for i in range(len(table_data)):
        for j in range(4):
            cell = table[i, j]
            cell.visible_edges = "LTRB"  # 显示全部边框
            cell.set_text_props(fontproperties=chinese_font)
            cell.set_height(row_heights[i])
            cell._text.set_wrap(True)
            cell._text.set_linespacing(1.75)  # 增加行内文字间距
    
    # 调整整体表格大小（减小缩放比例）
    table.scale(1.0, 1.2)
    
    # 保存图片（减小边距）
    plt.savefig(output_path, bbox_inches='tight', dpi=300, pad_inches=0.1)
    plt.close()

if __name__ == "__main__":
    # 测试代码
    print("开始生成表格图片...")
    
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建output目录路径
    output_dir = os.path.join(current_dir, "..", "..", "output")
    
    # 获取output目录下所有文件夹
    folders = [f for f in os.listdir(output_dir) if os.path.isdir(os.path.join(output_dir, f))]
    
    if not folders:
        print("错误：output目录下没有找到任何文件夹")
        exit(1)
    
    # 按修改时间排序，获取最新的文件夹
    latest_folder = max(folders, key=lambda f: os.path.getmtime(os.path.join(output_dir, f)))
    
    # 构建CSV文件路径
    csv_path = os.path.join(output_dir, latest_folder, "all_results.csv")
    
    # 构建输出图片路径（保存在同一文件夹中）
    output_path = os.path.join(output_dir, latest_folder, "results_table.png")
    
    try:
        generate_table_image(csv_path, output_path)
        print(f"表格图片已生成: {output_path}")
    except Exception as e:
        print(f"生成表格图片时发生错误: {str(e)}")
        print("请确保:")
        print("1. CSV文件存在且格式正确")
        print("2. 已安装所有必要的依赖 (pandas, matplotlib)")
        print("3. CSV文件包含所需的列: search_type, 设施名称, 室场名称, 日期, 时间段")