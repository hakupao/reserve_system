# 横滨市设施预约系统 - 浏览器模拟版本

这是一个自动化系统，用于监控和追踪横滨市公共设施的预约情况。系统通过模拟浏览器定期检查指定设施的预约状态，并将结果以结构化的方式保存和展示。

## 主要功能

- 🎯 多设施并发搜索：同时监控多个设施的预约情况
- 📊 数据可视化：自动生成预约状态表格图片
- 📁 智能文件管理：自动清理和归档历史数据
- 📝 数据导出：支持 CSV 格式导出

## 技术栈

- Python 3.8+
- Selenium 4.18.1：用于网页自动化
- Pandas 2.2.1：数据处理和分析
- Pillow 10.2.0：图像处理
- WebDriver Manager 4.0.1：ChromeDriver 管理

## 项目结构

```
browser_version/
├── src/                    # 源代码目录
│   ├── core/              # 核心功能模块
│   │   ├── search/        # 搜索相关功能
│   │   └── utils/         # 工具类
│   ├── config/            # 配置文件
│   ├── pages/             # 页面操作模块
│   └── utils/             # 通用工具
├── output/                # 输出文件目录
└── chromedriver-win64/    # ChromeDriver
```

## 输出文件结构

```
output/
├── 20240220_123456/          # 当前执行结果目录
│   ├── task1.csv            # 设施1的预约数据
│   ├── task2.csv            # 设施2的预约数据
│   ├── all_results.csv      # 合并后的所有数据
│   └── results_table.png    # 可视化表格
└── 20240220_120000/         # 上一次执行结果
```

## 快速开始

1. 环境准备：
   ```bash
   # 创建虚拟环境（推荐）
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   .\venv\Scripts\activate   # Windows

   # 安装依赖
   pip install -r ../requirements.txt
   ```

2. 配置搜索任务：
   - 编辑 `src/config/search_tasks_config.py`
   - 添加或修改需要监控的设施信息

3. 运行程序：
   ```bash
   python src/main.py
   ```

## 注意事项

- 确保已安装 Chrome 浏览器
- ChromeDriver 版本需与 Chrome 浏览器版本匹配
- 建议使用虚拟环境运行程序
- 定期检查并更新依赖包

## 文件管理说明

- 系统自动创建时间戳命名的结果目录
- 保留最新的两个执行结果
- 自动清理过期的结果文件

## 维护说明

- 定期检查 ChromeDriver 版本
- 监控系统运行日志
- 及时更新配置文件
- 定期备份重要数据 
