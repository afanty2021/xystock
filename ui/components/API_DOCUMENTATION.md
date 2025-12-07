# UI 组件接口文档

[模块首页](../CLAUDE.md) > **组件接口文档**

> 更新时间：2025-12-07 22:56:00

## 概述

本文档详细描述了 UI 模块中所有组件的接口定义、参数说明、使用示例和最佳实践。所有组件都基于 Streamlit 框架构建，遵循统一的编码规范和设计模式。

## 目录

1. [通用组件 (page_common.py)](#通用组件)
2. [个股分析组件 (page_stock.py)](#个股分析组件)
3. [大盘分析组件 (page_market_overview.py)](#大盘分析组件)
4. [系统设置组件 (page_settings.py)](#系统设置组件)
5. [报告导出组件 (page_export.py)](#报告导出组件)
6. [缓存管理组件 (page_cache_management.py)](#缓存管理组件)
7. [Token统计组件 (page_token_stats.py)](#token统计组件)

---

## 通用组件

### 文件：`page_common.py`

提供可复用的UI组件，被其他多个页面模块引用。

#### 1. 技术指标展示

```python
def display_technical_indicators(tech_data: dict) -> None
```

**功能描述**：以卡片形式展示各项技术指标数值

**参数**：
- `tech_data` (dict): 技术指标数据字典，包含以下键值：
  - `MA5`, `MA10`, `MA20`, `MA60`: 移动平均线数值
  - `MACD`: MACD指标值
  - `Signal`: MACD信号线
  - `Histogram`: MACD柱状图
  - `RSI`: RSI相对强弱指标
  - `K`, `D`, `J`: KDJ随机指标值

**使用示例**：
```python
tech_data = {
    'MA5': 10.50,
    'MA10': 10.45,
    'MA20': 10.40,
    'MA60': 10.35,
    'RSI': 65.2,
    'MACD': 0.05,
    'Signal': 0.03,
    'Histogram': 0.02
}
display_technical_indicators(tech_data)
```

#### 2. 技术分析标签页

```python
def display_technical_analysis_tab(stock_identity: dict = None, index_name: str = None) -> None
```

**功能描述**：展示完整的技术分析标签页内容

**参数**：
- `stock_identity` (dict, optional): 股票标识信息
  - `code`: 股票代码
  - `name`: 股票名称
  - `market_name`: 市场名称（A股/港股/ETF）
- `index_name` (str, optional): 指数名称（用于大盘分析）

**使用示例**：
```python
# 个股技术分析
stock_identity = {
    'code': '000001',
    'name': '平安银行',
    'market_name': 'A股'
}
display_technical_analysis_tab(stock_identity=stock_identity)

# 大盘技术分析
display_technical_analysis_tab(index_name='上证指数')
```

#### 3. 风险分析展示

```python
def display_risk_analysis(risk_metrics: dict) -> None
```

**功能描述**：展示风险评估结果

**参数**：
- `risk_metrics` (dict): 风险指标数据
  - `risk_level`: 风险等级（低/中/高）
  - `volatility`: 波动率
  - `max_drawdown`: 最大回撤
  - `sharpe_ratio`: 夏普比率

#### 4. K线图渲染

```python
def display_kline_charts(
    df: pd.DataFrame,
    chart_type: str = "stock",
    title_prefix: str = ""
) -> None
```

**功能描述**：渲染交互式K线图和成交量图表

**参数**：
- `df` (pd.DataFrame): K线数据，必须包含列：
  - `datetime`: 时间戳
  - `open`: 开盘价
  - `high`: 最高价
  - `low`: 最低价
  - `close`: 收盘价
  - `volume`: 成交量
- `chart_type` (str): 图表类型，可选值：
  - `"stock"`: 股票K线图（默认）
  - `"index"`: 指数K线图
- `title_prefix` (str): 标题前缀（股票名称或指数名称）

**使用示例**：
```python
# 准备K线数据
kline_data = pd.DataFrame({
    'datetime': pd.date_range('2024-01-01', periods=100),
    'open': np.random.randn(100).cumsum() + 100,
    'high': np.random.randn(100).cumsum() + 102,
    'low': np.random.randn(100).cumsum() + 98,
    'close': np.random.randn(100).cumsum() + 100,
    'volume': np.random.randint(1000000, 10000000, 100)
})

# 渲染K线图
display_kline_charts(kline_data, chart_type="stock", title_prefix="平安银行")
```

---

## 个股分析组件

### 文件：`page_stock.py`

实现完整的个股分析界面，包含5个主要功能标签页。

#### 1. 主显示函数

```python
def display_stock_info(stock_identity: dict) -> None
```

**功能描述**：展示股票的完整分析界面

**参数**：
- `stock_identity` (dict): 股票标识信息
  - `code`: 股票代码（必填）
  - `name`: 股票名称（可选）
  - `market_name`: 市场名称（默认"A股"）

**使用示例**：
```python
stock_identity = {
    'code': '000001',
    'name': '平安银行',
    'market_name': 'A股'
}
display_stock_info(stock_identity)
```

#### 2. 基本信息展示

```python
def display_basic_info(stock_identity: dict) -> None
```

**功能描述**：显示股票基本信息和实时行情

**参数**：
- `stock_identity` (dict): 股票标识信息

**功能**：
- 显示股票代码、名称、当前价格
- 涨跌幅、成交量等实时数据
- 市场状态（交易中/休市）

#### 3. 各类分析函数

```python
def display_fundamental_analysis(stock_identity: dict) -> None
```
- 功能：展示基本面分析（PE、PB、ROE等财务指标）

```python
def display_technical_analysis(stock_identity: dict) -> None
```
- 功能：展示技术面分析（调用page_common组件）

```python
def display_news_analysis(stock_identity: dict) -> None
```
- 功能：展示相关新闻和分析

```python
def display_chips_analysis(stock_identity: dict) -> None
```
- 功能：展示筹码分析（仅A股）

```python
def display_company_analysis(stock_identity: dict) -> None
```
- 功能：展示公司分析（仅A股）

```python
def display_comprehensive_analysis(stock_identity: dict) -> None
```
- 功能：展示AI综合分析报告

#### 3. Session State 使用

个股分析组件使用以下 session state 变量：

```python
# 缓存控制
st.session_state.get('use_cache', True)

# AI分析结果缓存
st.session_state.get('ai_fundamental_report', {})
st.session_state.get('ai_market_report', {})
st.session_state.get('ai_news_report', {})
st.session_state.get('ai_chip_report', {})
st.session_state.get('ai_company_report', {})
st.session_state.get('ai_comprehensive_report', {})

# AI分析开关
st.session_state.get('include_ai_analysis', False)
```

---

## 大盘分析组件

### 文件：`page_market_overview.py`

#### 1. 主显示函数

```python
def display_market_overview() -> None
```

**功能描述**：显示大盘分析的主界面，包含指数选择器和各项分析

**流程**：
1. 显示指数选择器
2. 显示市场整体概况
3. 分标签页展示各类分析
4. AI分析集成

#### 2. 估值分析

```python
def display_valuation_analysis(index_name: str = '沪深300', use_cache: bool = True) -> None
```

**参数**：
- `index_name` (str): 指数名称，默认'沪深300'
- `use_cache` (bool): 是否使用缓存，默认True

**功能**：
- PE、PB估值历史分位
- 估值曲线图
- 估值风险评估

#### 3. 资金流向分析

```python
def display_money_flow_analysis(use_cache: bool = True) -> None
```

**功能**：
- 北向资金流向
- 主力资金净流入
- 行业资金分布

#### 4. 融资融券分析

```python
def display_margin_trading_analysis(use_cache: bool = True) -> None
```

**功能**：
- 融资余额变化
- 融券余额变化
- 融资融券比例

#### 5. 市场情绪分析

```python
def display_market_sentiment_analysis(use_cache: bool = True) -> None
```

**功能**：
- 恐贪指数
- 涨跌停统计
- 市场热度指标

#### 6. 技术分析

```python
def display_market_technical_analysis(index_name: str = '上证指数') -> None
```

**参数**：
- `index_name` (str): 分析的指数名称

**功能**：
- 指数K线图
- 技术指标分析
- 趋势判断

#### 7. Session State 使用

```python
# 缓存控制
st.session_state['market_use_cache'] = True

# 分析状态
st.session_state['show_analysis_results'] = True
st.session_state['current_analysis_index'] = selected_index

# AI报告
st.session_state.ai_index_report

# 用户观点
st.session_state.market_user_opinion
```

---

## 系统设置组件

### 文件：`page_settings.py`

#### 1. 配置保存函数

```python
def save_config(section: str, key: str, value: any) -> bool
```

**功能描述**：保存配置项到配置文件

**参数**：
- `section` (str): 配置节名称
  - `'LLM_OPENAI'`: OpenAI API配置
  - `'LLM_CACHE'`: 缓存配置
  - `'ANALYSIS'`: 分析配置
  - `'USER_PROFILE'`: 用户画像
- `key` (str): 配置键名
- `value` (any): 配置值

**返回值**：
- `bool`: 保存是否成功

**使用示例**：
```python
# 保存API Key
success = save_config('LLM_OPENAI', 'API_KEY', 'sk-xxx...')

# 保存温度参数
success = save_config('LLM_OPENAI', 'DEFAULT_TEMPERATURE', 0.7)
```

#### 2. 配置项结构

##### OpenAI API配置
```python
LLM_OPENAI = {
    'API_KEY': str,           # API密钥
    'BASE_URL': str,          # API基础URL
    'DEFAULT_MODEL': str,     # 默认模型
    'INFERENCE_MODEL': str,   # 推理模型
    'TIMEOUT': int,           # 超时时间（秒）
    'MAX_RETRIES': int,       # 最大重试次数
    'DEFAULT_TEMPERATURE': float  # 默认温度参数（0.0-2.0）
}
```

##### 缓存配置
```python
LLM_CACHE = {
    'ENABLE_CACHE': bool,     # 是否启用缓存
    'CACHE_TTL': int         # 缓存生存时间（秒）
}
```

##### 分析配置
```python
ANALYSIS = {
    'RISK_PREFERENCE': str,   # 风险偏好
    'CUSTOM_PRINCIPLES': str  # 自定义投资原则
}

# 风险偏好选项
RISK_OPTIONS = [
    'conservative',  # 保守型
    'neutral',       # 中性
    'aggressive',    # 激进型
    'custom'         # 自定义
]
```

##### 用户画像
```python
USER_PROFILE = {
    'RAW': str,           # 原始用户画像描述
    'MISTAKES': list      # 常犯错误列表
}

# 预定义常犯错误
COMMON_MISTAKES = [
    '追涨杀跌',
    '频繁交易',
    '过度集中',
    '缺乏耐心',
    '盲目跟风',
    '情绪化交易'
]
```

---

## 报告导出组件

### 文件：`page_export.py`

#### 1. 核心导出函数

```python
def display_report_export_section(
    entity_id: str,
    report_type: str = "report",
    title: str = "📋 导出报告",
    info_text: str = "💡 可以导出完整的分析报告",
    generate_func: callable = None,
    generate_args: tuple = None,
    filename_prefix: str = "报告"
) -> None
```

**功能描述**：显示完整的报告导出界面

**参数**：
- `entity_id` (str): 实体ID（股票代码或指数名称）
- `report_type` (str): 报告类型，用于区分不同类型的报告
- `title` (str): 导出区域的标题
- `info_text` (str): 提示信息
- `generate_func` (callable): 报告生成函数
- `generate_args` (tuple): 生成函数的参数
- `filename_prefix` (str): 文件名前缀

**使用示例**：
```python
# 导出个股报告
display_report_export_section(
    entity_id='000001',
    report_type='stock',
    title='📊 导出个股分析报告',
    generate_func=generate_stock_report,
    generate_args=('000001', '平安银行'),
    filename_prefix='平安银行分析报告'
)
```

#### 2. 快速导出

```python
def display_quick_export_buttons(
    entity_id: str,
    report_type: str = "report",
    generate_func: callable = None,
    generate_args: tuple = None,
    filename_prefix: str = "报告"
) -> None
```

**功能描述**：显示快速导出按钮，不包含格式选择

#### 3. 批量导出

```python
def display_batch_export_options(
    entities: list,
    report_type: str = "report",
    generate_func: callable = None,
    generate_args_func: callable = None,
    filename_prefix: str = "报告"
) -> None
```

**参数**：
- `entities` (list): 要批量导出的实体列表
- `generate_args_func` (callable): 为每个实体生成参数的函数

#### 4. 支持的导出格式

| 格式 | 文件扩展名 | MIME类型 | 说明 |
|------|------------|----------|------|
| PDF | .pdf | application/pdf | 适合打印和分享 |
| DOCX | .docx | application/vnd.openxmlformats-officedocument.wordprocessingml.document | Word文档，可编辑 |
| Markdown | .md | text/markdown | 纯文本，版本控制友好 |
| HTML | .html | text/html | 网页格式，可在浏览器打开 |

#### 5. Session State 使用

```python
# 存储生成的内容
st.session_state[f'{report_type}_content_{entity_id}']
st.session_state[f'{report_type}_filename_{entity_id}']
st.session_state[f'{report_type}_mime_{entity_id}']
st.session_state[f'{report_type}_timestamp_{entity_id}']
```

---

## 缓存管理组件

### 文件：`page_cache_management.py`

#### 1. 主函数

```python
def main() -> None
```

**功能描述**：显示缓存管理界面

#### 2. 缓存清理功能

组件提供以下缓存清理选项：

- **个股数据缓存**
  - 基本信息：`stock_basic_info_{code}`
  - 技术指标：`stock_technical_{code}`
  - 新闻数据：`stock_news_{code}`
  - AI分析：`ai_*_report_{code}`
  - 筹码分析：`stock_chips_{code}`

- **大盘数据缓存**
  - 市场情绪：`market_sentiment`
  - 估值指标：`market_valuation_*`
  - 资金流向：`money_flow`
  - 融资融券：`margin_trading`

- **通用缓存**
  - K线数据：`kline_data_*`
  - 股票名映射：`stock_name_map`

#### 3. 缓存确认机制

```python
# 确认对话框
if st.session_state.get('confirm_clear_all', False):
    st.warning("⚠️ 确认要清理所有缓存吗？此操作不可恢复！")
    if st.button("确认清理", key="confirm_clear_all_btn"):
        # 执行清理
```

---

## Token统计组件

### 文件：`page_token_stats.py`

#### 1. 统计概览

```python
def show_usage_overview(days: int = 30) -> None
```

**参数**：
- `days` (int): 统计天数，默认30天

**功能**：
- 总请求数展示
- 总Token使用量
- 平均响应时间
- 成功率统计

#### 2. 模型分布

```python
def show_model_distribution(days: int = 30) -> None
```

**功能**：
- 各模型使用占比柱状图
- 使用次数统计
- Token消耗分布

#### 3. 详细记录

```python
def show_detailed_logs() -> None
```

**功能**：
- 分页显示详细使用记录
- 记录包含：
  - 时间戳
  - 模型名称
  - Prompt Token
  - Completion Token
  - 总Token
  - 成本
  - 响应时间
  - 状态（成功/失败）

#### 4. 时间范围选择

```python
# 快速选择
time_options = {
    "最近7天": 7,
    "最近30天": 30,
    "最近90天": 90,
    "最近180天": 180,
    "全部": 0
}
```

---

## 通用设计模式

### 1. 错误处理模式

```python
try:
    # 业务逻辑
    result = some_function()
    st.success("操作成功")
except Exception as e:
    st.error(f"操作失败：{str(e)}")
    logger.error(f"Error in function: {e}")
```

### 2. 加载状态管理

```python
with st.spinner("正在处理数据..."):
    data = fetch_data()
    processed_data = process_data(data)
```

### 3. 缓存控制模式

```python
use_cache = st.session_state.get('use_cache', True)
if use_cache and 'cached_data' in st.session_state:
    data = st.session_state['cached_data']
else:
    data = fetch_fresh_data()
    st.session_state['cached_data'] = data
```

### 4. 响应式布局

```python
# 响应式列布局
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("指标1", value1)
with col2:
    st.metric("指标2", value2)
with col3:
    st.metric("指标3", value3)
```

### 5. 数据验证模式

```python
def validate_stock_code(code: str) -> bool:
    """验证股票代码格式"""
    if not code:
        return False
    # A股：6位数字
    if re.match(r'^\d{6}$', code):
        return True
    # 港股：5位数字，以0开头
    if re.match(r'^0\d{4}$', code):
        return True
    return False
```

---

## 最佳实践

### 1. 性能优化
- 合理使用缓存避免重复请求
- 大数据集使用分页加载
- 图表数据适当采样

### 2. 用户体验
- 提供清晰的操作反馈
- 使用加载提示避免用户焦虑
- 错误信息友好易懂

### 3. 代码质量
- 保持函数单一职责
- 使用类型提示
- 编写完整的文档字符串

### 4. 安全考虑
- API密钥安全存储
- 用户输入验证
- 防止XSS攻击

---

## 更新记录

### 2025-12-07 22:56:00
- ✨ 创建完整的组件接口文档
- 📝 详细记录所有函数签名和参数
- 💡 添加使用示例和最佳实践
- 🔧 包含Session State使用指南

---

*本文档随代码更新而持续维护，确保与实际实现保持同步。*