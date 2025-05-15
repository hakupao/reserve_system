# 开发指南

## 开发环境设置

### 系统要求
- Python 3.8+
- Git
- 虚拟环境工具（推荐使用venv）

### 环境配置步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/reserve_system.git
cd reserve_system
```

2. 创建并激活虚拟环境
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

## 代码规范

### Python代码风格
- 遵循PEP 8规范
- 使用4个空格缩进
- 最大行长度限制为88字符
- 使用类型注解

### 命名规范
- 类名：使用驼峰命名法（CamelCase）
- 函数和变量：使用下划线命名法（snake_case）
- 常量：使用大写字母和下划线

### 文档规范
- 所有公共函数和类必须有文档字符串
- 使用Google风格的文档字符串格式
- 保持README文件及时更新

## 项目结构

### 浏览器版本模块化结构
浏览器版本中的ChouseisanUpdater已经被重构为模块化结构：

- `browser.py` - 浏览器基础操作模块
- `element_handler.py` - 元素操作工具模块
- `login_handler.py` - 登录处理模块
- `results_handler.py` - 结果处理模块
- `utils.py` - 工具函数模块
- `updater.py` - 主类（整合其他模块）

每个模块负责特定的功能，遵循单一职责原则，降低了代码耦合度，提高了可维护性。

## 测试指南

### 运行测试
```bash
python -m pytest tests/
```

### 测试覆盖率
```bash
python -m pytest --cov=./ tests/
```

## 部署说明

### 环境变量配置
创建 `.env` 文件并设置必要的环境变量：
```
API_BASE_URL=your_api_url
DEBUG=False
```

### 构建和部署
1. 确保所有测试通过
2. 更新版本号
3. 生成新的requirements.txt
4. 提交更改并创建新的发布标签

## 调试指南

### 日志级别
- DEBUG：详细的调试信息
- INFO：常规操作信息
- WARNING：警告信息
- ERROR：错误信息

### 日志系统
系统使用Python标准日志库，主要日志记录器包括：
- `ChouseisanBrowser` - 主日志记录器
- `ChouseisanBrowser.ElementHandler` - 元素处理日志
- `ChouseisanBrowser.LoginHandler` - 登录处理日志
- `ChouseisanBrowser.ResultsHandler` - 结果处理日志
- `ChouseisanBrowser.Utils` - 工具函数日志

### 常见问题解决
1. API连接问题
2. 数据解析错误
3. 文件权限问题

## 性能优化

### 代码优化建议
1. 使用异步IO处理网络请求
2. 实现请求缓存机制
3. 优化数据库查询
4. 使用连接池

### 监控指标
1. 响应时间
2. 内存使用
3. CPU使用率
4. 错误率 