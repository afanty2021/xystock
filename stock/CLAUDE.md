[根目录](../../CLAUDE.md) > **stock**

# stock 模块文档

## 模块职责

stock 模块是系统的核心模块之一，负责个股和ETF的数据获取、分析处理和AI智能分析。支持A股、港股和ETF基金，提供基本面、技术面、新闻面、筹码等多维度分析。

## 入口与启动

### 主要入口文件
- **`stock_data_fetcher.py`**：股票数据获取器
- **`stock_ai_analysis.py`**：股票AI分析引擎
- **`stock_report.py`**：股票分析报告生成器
- **`analysis_prompts.py`**：AI分析提示词模板
- **`etf_holdings_fetcher.py`**：ETF持仓数据获取
- **`chip_data_cache.py`**：筹码数据缓存

### 快速使用示例

```python
from stock.stock_data_fetcher import StockDataFetcher
from stock.stock_ai_analysis import generate_comprehensive_analysis
from stock.stock_report import generate_stock_report

# 获取股票数据
fetcher = StockDataFetcher()
stock_data = fetcher.get_stock_overview("000001", "平安银行")

# 生成AI分析
ai_analysis = generate_comprehensive_analysis(
    stock_code="000001",
    stock_name="平安银行",
    stock_data=stock_data
)

# 生成完整报告
report = generate_stock_report(
    stock_code="000001",
    stock_name="平安银行",
    market_type="A股",
    use_ai=True
)
```

## 对外接口

### StockDataFetcher 类

```python
class StockDataFetcher:
    def __init__(self):
        """初始化股票数据获取器"""

    def get_stock_overview(self,
                          stock_code: str,
                          stock_name: str) -> Dict[str, Any]
    """获取股票概览数据"""

    def get_fundamental_data(self,
                            stock_code: str) -> Dict[str, Any]
    """获取基本面数据"""

    def get_technical_data(self,
                          stock_code: str,
                          period: str = "daily") -> pd.DataFrame
    """获取技术面数据"""

    def get_chip_analysis(self,
                         stock_code: str) -> Dict[str, Any]
    """获取筹码分析数据"""

    def get_dividend_info(self,
                         stock_code: str) -> List[Dict[str, Any]]
    """获取分红信息"""
```

### ETF数据接口

```python
class ETFHoldingsFetcher:
    def get_etf_holdings(self,
                        etf_code: str) -> pd.DataFrame
    """获取ETF持仓明细"""

    def analyze_etf_composition(self,
                               etf_code: str) -> Dict[str, Any]
    """分析ETF构成"""

    def get_etf_performance(self,
                           etf_code: str) -> Dict[str, Any]
    """获取ETF业绩表现"""
```

### AI分析接口

```python
class StockAIAnalyzer:
    def __init__(self):
        """初始化AI分析器"""

    def analyze_technical(self,
                         technical_data: Dict[str, Any],
                         stock_info: Dict[str, Any]) -> AnalysisResult
    """技术面分析"""

    def analyze_fundamental(self,
                           fundamental_data: Dict[str, Any]) -> AnalysisResult
    """基本面分析"""

    def analyze_news(self,
                    news_data: List[Dict[str, str]]) -> AnalysisResult
    """新闻面分析"""

    def analyze_chip(self,
                    chip_data: Dict[str, Any]) -> AnalysisResult
    """筹码分析"""

    def generate_comprehensive_analysis(self,
                                       all_data: Dict[str, Any]) -> AnalysisResult
    """综合分析"""
```

## 关键依赖与配置

### 外部数据源
- **akshare**: A股基础数据
- **tushare**: 专业金融数据
- **baostock**: 历史数据补充
- **东方财富**: 实时行情数据
- **新浪财经**: 新闻资讯

### 内部依赖
- **llm模块**: AI分析能力
- **utils模块**: 数据处理和格式化
- **market模块**: 市场环境数据

### 支持的证券类型
```python
SUPPORTED_MARKETS = {
    "A股": {
        "prefix": ["00", "30", "60", "68", "83", "87"],
        "exchange": ["SZSE", "SSE", "STAR", "NEEQ"]
    },
    "港股": {
        "prefix": ["00", "02", "03", "04", "06", "08"],
        "exchange": ["HKEX"]
    },
    "ETF": {
        "prefix": ["15", "51", "52", "56", "58", "59"],
        "exchange": ["SZSE", "SSE"]
    }
}
```

## 数据模型

### StockData 股票基础数据
```python
@dataclass
class StockData:
    stock_code: str           # 股票代码
    stock_name: str           # 股票名称
    market: str               # 所属市场
    industry: str             # 所属行业
    current_price: float      # 当前价格
    change_percent: float     # 涨跌幅
    volume: float             # 成交量
    turnover: float           # 成交额
    market_cap: float         # 市值
    pe_ratio: float           # 市盈率
    pb_ratio: float           # 市净率
```

### FundamentalData 基本面数据
```python
@dataclass
class FundamentalData:
    revenue: float            # 营业收入
    net_profit: float         # 净利润
    eps: float               # 每股收益
    roe: float               # 净资产收益率
    roa: float               # 总资产收益率
    debt_ratio: float        # 资产负债率
    current_ratio: float     # 流动比率
    quick_ratio: float       # 速动比率
    gross_margin: float      # 毛利率
    net_margin: float        # 净利率
```

### ChipData 筹码数据
```python
@dataclass
class ChipData:
    concentration: float      # 筹码集中度
    main_cost: float         # 主力成本
    profit_ratio: float      # 盈利比例
    loss_ratio: float        # 亏损比例
    lock_ratio: float        # 锁仓比例
    distribution: List[float] # 成本分布
```

## 测试与质量

### 测试文件
- `../tests/test_stock_report.py`: 股票报告生成测试

### 测试覆盖
- ✅ 股票数据获取测试
- ✅ 报告生成测试
- ⏳ 各个分析模块的单元测试待补充
- ⏳ ETF分析测试待完善

### 质量保证
1. **数据验证**: 多源数据对比验证
2. **异常处理**: API失败时的容错机制
3. **缓存策略**: 智能缓存减少重复请求
4. **数据清洗**: 处理异常值和缺失值

## 使用场景

### 1. 个股深度分析
```python
# 生成完整的个股分析报告
def analyze_stock_deep(stock_code: str):
    # 获取所有维度的数据
    data = fetcher.get_comprehensive_data(stock_code)

    # AI分析各个维度
    tech_analysis = analyzer.analyze_technical(data['technical'])
    fund_analysis = analyzer.analyze_fundamental(data['fundamental'])
    news_analysis = analyzer.analyze_news(data['news'])
    chip_analysis = analyzer.analyze_chip(data['chip'])

    # 生成综合报告
    report = generate_stock_report(
        stock_code=stock_code,
        stock_name=data['basic']['name'],
        market_type=data['basic']['market'],
        technical_analysis=tech_analysis,
        fundamental_analysis=fund_analysis,
        news_analysis=news_analysis,
        chip_analysis=chip_analysis
    )

    return report
```

### 2. ETF投资分析
```python
# ETF投资组合分析
def analyze_etf_portfolio(etf_code: str):
    # 获取ETF持仓
    holdings = etf_fetcher.get_etf_holdings(etf_code)

    # 分析持仓集中度
    top10_holdings = holdings.nlargest(10, 'weight')
    concentration = top10_holdings['weight'].sum()

    # 分析行业分布
    industry_distribution = holdings.groupby('industry')['weight'].sum()

    # 分析个股表现
    stock_performance = []
    for _, holding in top10_holdings.iterrows():
        perf = get_stock_performance(holding['stock_code'])
        stock_performance.append(perf)

    return {
        'holdings': holdings,
        'concentration': concentration,
        'industry_distribution': industry_distribution,
        'top_performance': stock_performance
    }
```

### 3. 风险评估
```python
# 个股风险评估
def assess_stock_risk(stock_code: str):
    # 技术风险
    technical_risk = calculate_technical_risk(stock_code)

    # 基本面风险
    fundamental_risk = calculate_fundamental_risk(stock_code)

    # 集中度风险
    concentration_risk = calculate_concentration_risk(stock_code)

    # 综合风险评分
    risk_score = (
        technical_risk * 0.4 +
        fundamental_risk * 0.4 +
        concentration_risk * 0.2
    )

    return {
        'risk_score': risk_score,
        'risk_level': get_risk_level(risk_score),
        'risk_factors': {
            'technical': technical_risk,
            'fundamental': fundamental_risk,
            'concentration': concentration_risk
        }
    }
```

## 常见问题

### Q: 如何处理不同市场的股票代码？
A: 使用 `stock_code_map.py` 中的映射函数自动识别和转换代码格式。

### Q: 如何获取历史数据？
A: 通过 `get_technical_data` 方法指定时间范围，系统会自动获取历史K线数据。

### Q: ETF持仓数据多久更新一次？
A: 一般按季度更新，系统会缓存数据避免频繁请求。

### Q: 如何自定义AI分析提示词？
A: 修改 `analysis_prompts.py` 中的模板，支持针对不同类型的股票使用不同提示词。

## 相关文件清单

```
stock/
├── __init__.py                 # 模块初始化
├── stock_data_fetcher.py       # 数据获取器
├── stock_ai_analysis.py        # AI分析引擎
├── stock_report.py             # 报告生成器
├── stock_data_cache.py         # 数据缓存
├── stock_data_tools.py         # 数据工具
├── stock_utils.py              # 实用工具
├── stock_code_map.py           # 股票代码映射
├── analysis_prompts.py         # AI提示词
├── chip_data_cache.py          # 筹码缓存
└── etf_holdings_fetcher.py     # ETF持仓获取
```

## 变更记录

### 2025-12-07 22:48:54
- ✨ 创建模块文档
- 📊 定义股票数据模型
- 💡 提供分析场景示例

---

*该模块是股票分析的核心，为投资决策提供全面的数据和AI分析支持。*