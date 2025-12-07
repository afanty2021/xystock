[根目录](../../CLAUDE.md) > **backtesting**

# backtesting 模块文档

## 模块职责

backtesting 模块提供完整的策略回测框架，支持买卖策略验证、绩效计算和结果可视化。该模块帮助用户在历史数据上测试投资策略的有效性，为实盘交易提供参考依据。

## 入口与启动

### 主要入口文件
- **`backtest.py`**：核心回测引擎实现
- **`visualizer.py`**：回测结果可视化工具
- **`get_stock_data.py`**：回测用历史数据获取
- **`backtesting_demo.ipynb`**：Jupyter演示笔记本

### 快速使用示例

```python
from backtesting.backtest import SimpleBacktest

# 初始化回测引擎
backtest = SimpleBacktest(initial_cash=100000)

# 执行买入操作
backtest.buy(price=10.50, volume=1000, date='2024-01-01')

# 执行卖出操作
backtest.sell(price=12.00, volume=500, date='2024-01-15')

# 获取回测结果
results = backtest.get_results()
```

## 对外接口

### SimpleBacktest 类

#### 核心方法

```python
class SimpleBacktest:
    def __init__(self, initial_cash: float = 100000)

    def buy(self, price: float, volume: int, date: str) -> bool
    """买入操作"""

    def sell(self, price: float, volume: int, date: str) -> bool
    """卖出操作"""

    def update(self, price: float, date: str) -> None
    """更新持仓价值"""

    def get_results(self) -> Dict[str, Any]
    """获取回测结果统计"""

    def reset(self) -> None
    """重置回测状态"""
```

#### 返回指标

- `total_return`: 总收益率
- `max_drawdown`: 最大回撤
- `sharpe_ratio`: 夏普比率
- `win_rate`: 胜率
- `trade_count`: 交易次数

### 可视化接口

```python
from backtesting.visualizer import BacktestVisualizer

visualizer = BacktestVisualizer(backtest_results)
visualizer.plot_equity_curve()  # 绘制资金曲线
visualizer.plot_drawdown()      # 绘制回撤曲线
visualizer.plot_trades()        # 绘制交易点
```

## 关键依赖与配置

### 内部依赖
- **pandas**: 数据处理和分析
- **numpy**: 数值计算
- **matplotlib**: 基础绘图
- **plotly**: 交互式图表

### 外部数据依赖
- **stock模块**: 获取历史股价数据
- **utils模块**: 使用数据处理工具

### 配置参数
```python
# 回测参数配置
BACKTEST_CONFIG = {
    'initial_cash': 100000,      # 初始资金
    'commission': 0.001,         # 手续费率
    'slippage': 0.001,           # 滑点
    'position_limit': 0.95,      # 最大仓位限制
}
```

## 数据模型

### Trade 交易记录
```python
@dataclass
class Trade:
    date: str          # 交易日期
    action: str        # 交易类型 (buy/sell)
    price: float       # 交易价格
    volume: int        # 交易数量
    amount: float      # 交易金额
    commission: float  # 手续费
```

### BacktestResult 回测结果
```python
@dataclass
class BacktestResult:
    initial_cash: float
    final_value: float
    total_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    trades: List[Trade]
    equity_curve: pd.DataFrame
```

## 测试与质量

### 当前测试状态
- ✅ 基础回测流程验证
- ⏳ 策略测试用例待补充
- ⏳ 性能压力测试待实施

### 质量建议
1. 增加边界条件测试（极端行情、无交易等）
2. 添加性能基准测试（大数据量回测）
3. 实现策略回测的单元测试框架

## 使用场景

### 1. 策略验证
```python
# 验证均线策略
def ma_strategy(data, short_window=5, long_window=20):
    signals = []
    for i in range(len(data)):
        if data['MA5'][i] > data['MA20'][i]:
            signals.append('BUY')
        else:
            signals.append('SELL')
    return signals
```

### 2. 参数优化
```python
# 网格搜索最优参数
for short in range(5, 15):
    for long in range(20, 50):
        result = backtest_strategy(ma_strategy, short, long)
        results.append((short, long, result.total_return))
```

### 3. 风险评估
- 最大回撤分析
- 夏普比率计算
- 胜率统计
- 交易频率分析

## 常见问题

### Q: 如何处理停牌数据？
A: 使用 `get_stock_data.py` 中的数据清洗功能，自动填充或跳过停牌日期。

### Q: 如何加入手续费和滑点？
A: 在交易执行时自动计算，可在配置中调整费率。

### Q: 支持哪些类型的策略？
A: 目前支持简单策略，复杂策略需要继承 `SimpleBacktest` 类扩展。

## 相关文件清单

```
backtesting/
├── __init__.py              # 模块初始化
├── backtest.py              # 核心回测引擎
├── visualizer.py            # 可视化工具
├── get_stock_data.py        # 历史数据获取
└── backtesting_demo.ipynb   # Jupyter演示
```

## 变更记录

### 2025-12-07 22:48:54
- ✨ 创建模块文档
- 📝 定义回测接口和数据模型
- 🔧 提供使用示例和最佳实践

---

*该模块为投资策略验证提供基础框架，建议结合实际策略需求进行扩展。*