[根目录](../../CLAUDE.md) > **ui**

# ui 模块文档

## 模块职责

ui 模块负责构建用户交互界面，基于 Streamlit 框架提供直观易用的 Web 界面。支持大盘分析、个股分析、回测模拟、系统设置等功能，是用户与系统交互的主要入口。

## 入口与启动

### 主要入口文件
- **`app.py`**：Streamlit 应用主程序
- **`start_ui.py`**：UI 启动脚本
- **`config.py`**：UI 配置文件
- **`components/`**：页面组件目录

### 启动方式

```bash
# 方式一：直接运行
python -m streamlit run ui/app.py --server.address=0.0.0.0 --server.port=8811

# 方式二：使用启动脚本
python ui/start_ui.py

# 方式三：Docker 容器
docker run -p 8811:8811 xieyan800811/xystock:latest
```

### 访问地址
- 本地访问：http://localhost:8811
- 远程访问：http://[服务器IP]:8811

## 页面结构

### 主要页面组件

```
ui/
├── components/
│   ├── page_settings.py           # 设置页面
│   ├── page_token_stats.py        # Token统计页面
│   ├── page_stock.py              # 个股分析页面
│   ├── page_market_overview.py    # 大盘分析页面
│   ├── page_cache_management.py   # 缓存管理页面
│   ├── page_export.py             # 报告导出页面
│   └── page_common.py             # 通用组件
```

### 页面功能说明

1. **设置页面** (`page_settings.py`)
   - API密钥配置
   - 模型选择和参数设置
   - 用户画像和风险偏好设置
   - 数据源配置

2. **Token统计页面** (`page_token_stats.py`)
   - API使用量统计
   - 成本分析
   - 模型使用效率
   - 使用历史记录

3. **个股分析页面** (`page_stock.py`)
   - 股票代码输入和选择
   - 实时行情展示
   - AI分析结果展示
   - 技术图表显示

4. **大盘分析页面** (`page_market_overview.py`)
   - 指数选择和切换
   - 市场整体概况
   - 技术指标展示
   - 新闻资讯聚合

5. **缓存管理页面** (`page_cache_management.py`)
   - 缓存文件管理
   - 清理过期数据
   - 缓存空间统计
   - 数据备份

6. **报告导出页面** (`page_export.py`)
   - 多格式报告导出
   - 批量处理任务
   - 导出历史记录

## 对外接口

### 详细接口文档

📋 **完整的组件接口文档**：查看 [API_DOCUMENTATION.md](./components/API_DOCUMENTATION.md) 获取详细的接口说明、参数定义和使用示例。

### 主应用配置

```python
# app.py 主程序
def main():
    """主应用程序"""
    st.set_page_config(
        page_title="XY Stock 股票分析系统",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 设置全局配置
    set_requests_timeout(30)

    # 侧边栏导航
    page = st.sidebar.selectbox("选择功能", PAGES)

    # 渲染对应页面
    render_page(page)
```

### 页面组件接口概览

```python
# 通用页面组件 (page_common.py)
def display_technical_indicators(tech_data: dict) -> None
def display_technical_analysis_tab(stock_identity: dict = None, index_name: str = None) -> None
def display_risk_analysis(risk_metrics: dict) -> None
def display_kline_charts(df: pd.DataFrame, chart_type: str = "stock", title_prefix: str = "") -> None

# 个股分析页面 (page_stock.py)
def display_stock_info(stock_identity: dict) -> None
def display_basic_info(stock_identity: dict) -> None
def display_fundamental_analysis(stock_identity: dict) -> None
def display_technical_analysis(stock_identity: dict) -> None
def display_news_analysis(stock_identity: dict) -> None
def display_chips_analysis(stock_identity: dict) -> None
def display_company_analysis(stock_identity: dict) -> None
def display_comprehensive_analysis(stock_identity: dict) -> None

# 大盘分析页面 (page_market_overview.py)
def display_market_overview() -> None
def display_valuation_analysis(index_name: str = '沪深300', use_cache: bool = True) -> None
def display_money_flow_analysis(use_cache: bool = True) -> None
def display_margin_trading_analysis(use_cache: bool = True) -> None
def display_market_sentiment_analysis(use_cache: bool = True) -> None
def display_market_technical_analysis(index_name: str = '上证指数') -> None

# 系统设置页面 (page_settings.py)
def save_config(section: str, key: str, value: any) -> bool
def main() -> None

# 报告导出页面 (page_export.py)
def display_report_export_section(entity_id: str, report_type: str = "report", ...) -> None
def display_quick_export_buttons(entity_id: str, report_type: str = "report", ...) -> None
def display_batch_export_options(entities: list, report_type: str = "report", ...) -> None

# 缓存管理页面 (page_cache_management.py)
def main() -> None

# Token统计页面 (page_token_stats.py)
def show_usage_overview(days: int = 30) -> None
def show_model_distribution(days: int = 30) -> None
def show_detailed_logs() -> None
def main() -> None
```

### UI配置参数

```python
# config.py 配置项
STREAMLIT_CONFIG = {
    "port": 8811,
    "host": "0.0.0.0",
    "headless": True,
    "title": "XY Stock 股票分析系统"
}

# 市场类型配置
MARKET_TYPES = ["A股", "港股", "ETF"]

# 股票代码示例
STOCK_CODE_EXAMPLES = {
    "A股": ["000001", "000002", "600000", "600036"],
    "港股": ["00700", "00941", "02318"],
    "ETF": ["159915", "510300", "512100"]
}

# UI主题配置
UI_THEME = {
    "primary_color": "#1f77b4",
    "background_color": "#ffffff",
    "secondary_background_color": "#f0f2f6",
    "text_color": "#262730"
}
```

## 关键依赖与配置

### 主要依赖
- **streamlit**: Web应用框架 (>=1.48.0)
- **plotly**: 交互式图表
- **pandas**: 数据处理
- **matplotlib**: 基础绘图

### 内部依赖
- **stock模块**: 股票数据和分析
- **market模块**: 市场数据分析
- **llm模块**: AI分析功能
- **utils模块**: 数据格式化和工具
- **version**: 版本信息

### 浏览器兼容性
- Chrome/Edge (推荐)
- Firefox
- Safari
- 移动端浏览器 (部分功能)

## 使用示例

### 1. 创建新页面组件

```python
# components/page_new_feature.py
import streamlit as st
import sys
import os

# 添加项目路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

def main():
    st.header("新功能页面")

    # 页面内容
    with st.container():
        st.write("这是新功能的描述")

        # 用户输入
        user_input = st.text_input("请输入参数")

        # 操作按钮
        if st.button("执行"):
            # 执行逻辑
            result = process_input(user_input)

            # 显示结果
            st.success(f"处理结果: {result}")

if __name__ == "__main__":
    main()
```

### 2. 添加交互式图表

```python
def display_interactive_chart(data: pd.DataFrame):
    """显示交互式K线图"""
    import plotly.graph_objects as go

    fig = go.Figure(data=go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name="K线"
    ))

    fig.update_layout(
        title="股价K线图",
        yaxis_title="价格",
        xaxis_title="时间",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)
```

### 3. 实现数据导出功能

```python
def export_report(report_content: str, format_type: str):
    """导出报告"""
    if format_type == "Markdown":
        st.download_button(
            label="下载Markdown报告",
            data=report_content,
            file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )

    elif format_type == "PDF":
        # 转换为PDF
        pdf_content = convert_to_pdf(report_content)
        st.download_button(
            label="下载PDF报告",
            data=pdf_content,
            file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf"
        )
```

## 测试与质量

### UI测试策略
1. **功能测试**: 验证各页面功能正常
2. **兼容性测试**: 多浏览器测试
3. **性能测试**: 页面加载速度测试
4. **用户体验测试**: 界面易用性评估

### 质量保证
- 使用 Streamlit 的内置错误处理
- 实施加载状态提示
- 提供操作反馈和确认
- 优化移动端显示效果

## 常见问题

### Q: 如何自定义页面主题？
A: 修改 `config.py` 中的 `UI_THEME` 配置，或通过 CSS 注入自定义样式。

### Q: 如何处理长时间运行的任务？
A: 使用 `st.spinner` 显示加载状态，或通过 `st.empty()` 实现异步更新。

### Q: 如何优化页面加载速度？
A:
- 使用缓存机制存储数据
- 懒加载非关键内容
- 压缩静态资源
- 使用 CDN 加速

### Q: 如何实现页面间的数据共享？
A: 使用 Streamlit 的 `st.session_state` 或自定义缓存机制。

## 相关文件清单

```
ui/
├── __init__.py                # 模块初始化
├── app.py                     # Streamlit主应用
├── start_ui.py               # UI启动脚本
├── config.py                 # UI配置
├── start_ui.sh               # Shell启动脚本
├── README.md                 # UI说明文档
└── components/               # 页面组件目录
    ├── API_DOCUMENTATION.md  # 📋 组件接口文档（新增）
    ├── page_settings.py      # 设置页面
    ├── page_token_stats.py   # Token统计
    ├── page_stock.py         # 个股分析
    ├── page_market_overview.py # 大盘分析
    ├── page_cache_management.py # 缓存管理
    ├── page_export.py        # 报告导出
    └── page_common.py        # 通用组件
```

## 变更记录

### 2025-12-07 22:57:00
- ✨ 创建完整的组件接口文档 `API_DOCUMENTATION.md`
- 📝 详细记录所有函数签名、参数说明和使用示例
- 🔧 添加Session State使用指南和设计模式
- 🎯 提供最佳实践建议

### 2025-12-07 22:48:54
- ✨ 创建模块文档
- 📱 整理页面组件结构
- 🎨 提供UI定制指南

---

*该模块是用户与系统交互的桥梁，持续优化用户体验是关键。*