[根目录](../../CLAUDE.md) > **utils**

# utils 模块文档

## 模块职责

utils 模块提供系统的通用工具函数库，包括数据格式化、报告生成、风险计算、新闻处理、绘图工具等基础功能。作为支撑模块，为其他模块提供可复用的工具和服务。

## 入口与启动

### 主要工具文件
- **`data_formatters.py`**：数据格式化工具
- **`report_utils.py`**：报告生成工具
- **`risk_metrics.py`**：风险指标计算
- **`draw.py`**：绘图工具
- **`news_tools.py`**：新闻处理工具
- **`format_utils.py`**：通用格式化工具
- **`string_utils.py`**：字符串处理工具
- **`kline_cache.py`**：K线数据缓存
- **`report_utils.py`**：报告工具

### 快速使用示例

```python
from utils.data_formatters import StockDataFormatter
from utils.risk_metrics import RiskCalculator
from utils.report_utils import ReportGenerator

# 数据格式化
formatter = StockDataFormatter()
formatted_data = formatter.format_for_display(raw_data)

# 风险计算
calculator = RiskCalculator()
var_95 = calculator.calculate_var(returns, confidence=0.95)

# 报告生成
generator = ReportGenerator()
report = generator.generate_html_report(data, template="stock")
```

## 核心工具接口

### 数据格式化器 (`data_formatters.py`)

```python
class StockDataFormatter:
    """股票数据格式化器"""

    @staticmethod
    def format_price(value: float, precision: int = 2) -> str
    """格式化价格显示"""

    @staticmethod
    def format_percentage(value: float) -> str
    """格式化百分比"""

    @staticmethod
    def format_volume(value: float) -> str
    """格式化成交量"""

    @staticmethod
    def format_for_ai_analysis(data: Dict[str, Any]) -> str
    """格式化数据供AI分析"""

class MarketDataFormatter:
    """市场数据格式化器"""

    @staticmethod
    def format_market_data(market_data: Dict) -> str
    """格式化市场数据"""

    @staticmethod
    def format_indicators(indicators: Dict) -> str
    """格式化技术指标"""
```

### 风险指标计算 (`risk_metrics.py`)

```python
class RiskCalculator:
    """风险指标计算器"""

    def calculate_var(self,
                     returns: pd.Series,
                     confidence: float = 0.95) -> float
    """计算风险价值VaR"""

    def calculate_max_drawdown(self,
                              prices: pd.Series) -> Dict[str, float]
    """计算最大回撤"""

    def calculate_sharpe_ratio(self,
                              returns: pd.Series,
                              risk_free_rate: float = 0.02) -> float
    """计算夏普比率"""

    def calculate_beta(self,
                      stock_returns: pd.Series,
                      market_returns: pd.Series) -> float
    """计算Beta系数"""

    def calculate_volatility(self,
                           returns: pd.Series,
                           annualized: bool = True) -> float
    """计算波动率"""
```

### 报告生成器 (`report_utils.py`)

```python
class ReportGenerator:
    """报告生成器"""

    def generate_markdown_report(self,
                                data: Dict[str, Any],
                                template: str = "default") -> str
    """生成Markdown格式报告"""

    def generate_html_report(self,
                            data: Dict[str, Any],
                            template: str = "default") -> str
    """生成HTML格式报告"""

    def generate_pdf_report(self,
                           data: Dict[str, Any],
                           template: str = "default") -> bytes
    """生成PDF格式报告"""

    def export_to_excel(self,
                       data: Dict[str, Any],
                       filename: str) -> None
    """导出为Excel文件"""
```

### 绘图工具 (`draw.py`)

```python
class ChartDrawer:
    """图表绘制器"""

    @staticmethod
    def draw_kline_chart(data: pd.DataFrame,
                        title: str = "K线图") -> go.Figure
    """绘制K线图"""

    @staticmethod
    def draw_volume_chart(data: pd.DataFrame) -> go.Figure
    """绘制成交量图"""

    @staticmethod
    def draw_indicators_chart(data: pd.DataFrame,
                             indicators: List[str]) -> go.Figure
    """绘制技术指标图"""

    @staticmethod
    def draw_correlation_heatmap(corr_matrix: pd.DataFrame) -> go.Figure
    """绘制相关性热力图"""
```

## 关键依赖与配置

### 主要依赖
- **pandas**: 数据处理和分析
- **numpy**: 数值计算
- **matplotlib**: 基础绘图
- **plotly**: 交互式图表
- **pypandoc**: 文档格式转换
- **reportlab**: PDF生成

### 外部服务
- **新闻API**: 获取财经新闻
- **图表服务**: 在线图表生成
- **翻译API**: 多语言支持

### 配置参数

```python
# 格式化配置
FORMAT_CONFIG = {
    "price_precision": 2,
    "percentage_precision": 2,
    "volume_unit": "万手",
    "currency": "CNY"
}

# 风险计算参数
RISK_CONFIG = {
    "var_confidence": 0.95,
    "volatility_window": 252,  # 一年交易日
    "max_drawdown_window": None
}

# 报告配置
REPORT_CONFIG = {
    "template_dir": "templates",
    "output_dir": "reports",
    "default_format": "markdown"
}
```

## 工具函数详解

### 1. 数据清洗工具

```python
def clean_financial_data(df: pd.DataFrame) -> pd.DataFrame
    """清洗金融数据，处理异常值和缺失值"""

def normalize_data(data: np.ndarray, method: str = "minmax") -> np.ndarray
    """数据标准化"""

def detect_outliers(data: pd.Series, method: str = "iqr") -> pd.Series
    """异常值检测"""
```

### 2. 时间序列工具

```python
def resample_data(df: pd.DataFrame,
                 frequency: str = "D") -> pd.DataFrame
    """重采样时间序列数据"""

def calculate_returns(prices: pd.Series,
                     method: str = "simple") -> pd.Series
    """计算收益率"""

def decompose_time_series(series: pd.Series) -> Dict[str, pd.Series]
    """时间序列分解"""
```

### 3. 新闻处理工具

```python
def extract_keywords(text: str, top_k: int = 10) -> List[str]
    """提取关键词"""

def analyze_sentiment(text: str) -> Dict[str, float]
    """情感分析"""

def summarize_news(articles: List[Dict], max_length: int = 200) -> str
    """新闻摘要生成"""
```

### 4. 缓存管理工具

```python
class CacheManager:
    """缓存管理器"""

    def set(self, key: str, value: Any, ttl: int = 3600) -> None
    """设置缓存"""

    def get(self, key: str) -> Any
    """获取缓存"""

    def delete(self, key: str) -> None
    """删除缓存"""

    def clear_expired(self) -> None
    """清理过期缓存"""
```

## 使用示例

### 1. 创建自定义图表

```python
from utils.draw import ChartDrawer
import plotly.graph_objects as go

def create_custom_chart(stock_data: pd.DataFrame):
    # 创建K线图
    fig = ChartDrawer.draw_kline_chart(stock_data, "股价走势")

    # 添加移动平均线
    fig.add_trace(go.Scatter(
        x=stock_data.index,
        y=stock_data['MA20'],
        name="MA20",
        line=dict(color='orange')
    ))

    # 添加成交量
    fig.add_trace(go.Bar(
        x=stock_data.index,
        y=stock_data['Volume'],
        name="成交量",
        yaxis='y2'
    ))

    # 更新布局
    fig.update_layout(
        title="综合技术分析图",
        yaxis2=dict(
            title="成交量",
            overlaying='y',
            side='right'
        )
    )

    return fig
```

### 2. 生成定制报告

```python
from utils.report_utils import ReportGenerator
from utils.data_formatters import StockDataFormatter

def generate_analysis_report(stock_code: str, stock_data: Dict):
    formatter = StockDataFormatter()
    generator = ReportGenerator()

    # 格式化数据
    formatted_data = {
        "basic_info": formatter.format_basic_info(stock_data['basic']),
        "technical": formatter.format_technical(stock_data['technical']),
        "fundamental": formatter.format_fundamental(stock_data['fundamental'])
    }

    # 使用自定义模板
    template = """
    # {name}({code}) 分析报告

    ## 基本信息
    {basic_info}

    ## 技术分析
    {technical}

    ## 基本面分析
    {fundamental}
    """

    report = generator.generate_from_template(
        template=template,
        data=formatted_data
    )

    return report
```

### 3. 计算综合风险指标

```python
from utils.risk_metrics import RiskCalculator

def comprehensive_risk_analysis(returns: pd.Series,
                               market_returns: pd.Series):
    calculator = RiskCalculator()

    # 计算各类风险指标
    risk_metrics = {
        "var_95": calculator.calculate_var(returns, 0.95),
        "var_99": calculator.calculate_var(returns, 0.99),
        "max_dd": calculator.calculate_max_drawdown(returns)["max_drawdown"],
        "sharpe": calculator.calculate_sharpe_ratio(returns),
        "beta": calculator.calculate_beta(returns, market_returns),
        "volatility": calculator.calculate_volatility(returns)
    }

    # 风险评级
    risk_score = calculate_risk_score(risk_metrics)
    risk_level = categorize_risk(risk_score)

    return {
        "metrics": risk_metrics,
        "score": risk_score,
        "level": risk_level,
        "recommendation": get_risk_advice(risk_level)
    }
```

## 测试与质量

### 测试覆盖
- ⏳ 需要补充完整的单元测试
- ⏳ 集成测试待完善
- ⏳ 性能测试待实施

### 质量保证
1. **输入验证**: 所有函数都进行参数验证
2. **错误处理**: 完善的异常处理机制
3. **文档完整**: 详细的函数文档和示例
4. **性能优化**: 关键函数的性能优化

## 常见问题

### Q: 如何处理不同市场的数据格式差异？
A: 使用 `data_formatters.py` 中的格式化器，根据市场类型选择相应的格式化规则。

### Q: 如何添加新的风险指标？
A: 在 `risk_metrics.py` 中添加新的计算方法，确保符合现有的接口规范。

### Q: 报告模板如何自定义？
A: 在模板目录中创建新的模板文件，使用模板语法引用数据变量。

### Q: 如何优化大量数据的处理速度？
A: 使用向量化操作、并行处理、缓存机制等优化策略。

## 相关文件清单

```
utils/
├── __init__.py             # 模块初始化
├── data_formatters.py      # 数据格式化
├── report_utils.py         # 报告生成
├── risk_metrics.py         # 风险指标
├── draw.py                 # 绘图工具
├── news_tools.py           # 新闻处理
├── format_utils.py         # 格式化工具
├── string_utils.py         # 字符串工具
├── kline_cache.py          # K线缓存
└── report_utils.py         # 报告工具（备份）
```

## 变更记录

### 2025-12-07 22:48:54
- ✨ 创建模块文档
- 🛠️ 整理工具函数接口
- 📊 提供使用示例

---

*该模块是系统的基础支撑，良好的工具函数设计能显著提升开发效率。*