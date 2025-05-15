# 横滨市设施预约系统

这是一个用于监控和查询横滨市公共设施预约情况的工具集。系统提供两种不同的实现方式，满足不同的使用需求。

## 快速开始

1. 克隆仓库
```bash
git clone https://github.com/yourusername/reserve_system.git
cd reserve_system
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行程序
```bash
# API版本
python api_version/main.py

# 浏览器版本
python browser_version/src/main.py
```

## 功能版本

### 1. 模拟浏览器版本 (browser_version)
- 多设施并发搜索
- 数据可视化处理
- 智能文件管理
- 模块化设计的调整さん更新工具
- 完善的日志系统

[查看详细文档](./browser_version/README.md)

### 2. API版本 (api_version)
- 直接API调用，无需浏览器
- 支持按区域、日期和时间搜索
- 结果保存为JSON和CSV格式
- 模块化设计，便于维护和扩展

[查看详细文档](./api_version/README.md)

## 最新更新

- **模块化重构**：ChouseisanUpdater已重构为模块化结构，提高了代码可维护性
- **强化日志系统**：添加了全面的日志记录系统
- **改进的数据处理**：优化从output读取数据的流程

详细更新内容请查看[变更日志](./docs/CHANGELOG.md)。

## 文档

- [开发指南](./docs/DEVELOPMENT.md)
- [贡献指南](./docs/CONTRIBUTING.md)
- [变更日志](./docs/CHANGELOG.md)

## 环境要求

- Python 3.8+
- 相关依赖包(详见requirements.txt)

## 开源许可

本项目采用MIT许可证。详见 [LICENSE](LICENSE) 文件。

## 贡献

欢迎提交问题和功能请求！请查看[贡献指南](./docs/CONTRIBUTING.md)了解如何参与项目开发。 