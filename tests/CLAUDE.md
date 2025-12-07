[根目录](../../CLAUDE.md) > **tests**

# tests 模块文档

## 模块职责

tests 模块负责系统的测试工作，包括单元测试、集成测试和端到端测试。确保各个模块功能的正确性、系统的稳定性和数据的准确性。

## 测试文件结构

### 当前测试文件
- **`test_stock_report.py`**：股票报告生成测试
- **`test_market_report.py`**：市场报告生成测试

### 建议的测试目录结构
```
tests/
├── unit/                   # 单元测试
│   ├── test_stock/
│   │   ├── test_data_fetcher.py
│   │   ├── test_ai_analysis.py
│   │   └── test_report.py
│   ├── test_market/
│   │   ├── test_data_fetcher.py
│   │   └── test_analysis.py
│   ├── test_llm/
│   │   └── test_openai_client.py
│   └── test_utils/
│       ├── test_formatters.py
│       └── test_risk_metrics.py
├── integration/            # 集成测试
│   ├── test_data_flow.py
│   └── test_api_integration.py
├── e2e/                   # 端到端测试
│   ├── test_ui_flow.py
│   └── test_complete_workflow.py
├── fixtures/              # 测试数据
│   ├── sample_stock_data.json
│   ├── sample_market_data.json
│   └── mock_responses.json
└── conftest.py            # pytest配置
```

## 测试框架与工具

### 主要测试框架
- **pytest**: 主要测试框架
- **unittest**: Python内置测试框架
- **mock**: 模拟对象和函数
- **parameterized**: 参数化测试

### 测试工具
- **pytest-cov**: 代码覆盖率
- **pytest-mock**: Mock支持
- **pytest-asyncio**: 异步测试
- **pytest-xdist**: 并行测试

### 配置示例

```python
# conftest.py
import pytest
import pandas as pd
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def sample_stock_data():
    """提供示例股票数据"""
    return {
        "stock_code": "000001",
        "stock_name": "平安银行",
        "current_price": 12.50,
        "change_percent": 2.5,
        "volume": 1000000,
        "pe_ratio": 8.5,
        "pb_ratio": 0.8
    }

@pytest.fixture
def mock_api_response():
    """模拟API响应"""
    return {
        "choices": [{
            "message": {
                "content": "这是一个测试分析报告"
            }
        }]
    }
```

## 现有测试示例

### test_stock_report.py

```python
#!/usr/bin/env python3
"""
股票报告测试
"""
import sys
import os
import argparse

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from stock.stock_report import generate_stock_report
from stock.stock_code_map import get_stock_identity

def test_stock_report(stock_code="600519", stock_name="贵州茅台", market_type="A股",
                     format_type="markdown", use_ai=False):
    """测试生成股票报告"""
    print(f"🧪 测试股票报告生成 - {stock_name}({stock_code})...")

    try:
        # 生成报告
        success, message = generate_stock_report(
            stock_code=stock_code,
            stock_name=stock_name,
            market_type=market_type,
            format_type=format_type,
            use_ai=use_ai
        )

        if success:
            print(f"✅ 报告生成成功")
            print(f"📄 报告长度: {len(message)} 字符")
            print(f"💾 已保存至: {message}")
        else:
            print(f"❌ 报告生成失败: {message}")

    except Exception as e:
        print(f"💥 测试异常: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="测试股票报告生成")
    parser.add_argument("--stock-code", default="600519", help="股票代码")
    parser.add_argument("--stock-name", default="贵州茅台", help="股票名称")
    parser.add_argument("--market-type", default="A股", help="市场类型")
    parser.add_argument("--format", default="markdown", help="报告格式")
    parser.add_argument("--use-ai", action="store_true", help="使用AI分析")

    args = parser.parse_args()

    test_stock_report(
        stock_code=args.stock_code,
        stock_name=args.stock_name,
        market_type=args.market_type,
        format_type=args.format,
        use_ai=args.use_ai
    )
```

## 测试用例建议

### 1. 单元测试用例

```python
# tests/unit/test_utils/test_risk_metrics.py
import pytest
import numpy as np
from utils.risk_metrics import RiskCalculator

class TestRiskCalculator:
    """风险指标计算测试"""

    def setup_method(self):
        """测试前置设置"""
        self.calculator = RiskCalculator()
        self.returns = np.random.normal(0.001, 0.02, 252)  # 一年日收益率

    def test_calculate_var(self):
        """测试VaR计算"""
        var = self.calculator.calculate_var(self.returns, 0.95)
        assert var < 0  # VaR应该是负值
        assert isinstance(var, float)

    def test_calculate_sharpe_ratio(self):
        """测试夏普比率计算"""
        sharpe = self.calculator.calculate_sharpe_ratio(self.returns)
        assert isinstance(sharpe, float)

    def test_calculate_max_drawdown(self):
        """测试最大回撤计算"""
        prices = 100 * np.exp(np.cumsum(self.returns))
        dd_info = self.calculator.calculate_max_drawdown(prices)
        assert "max_drawdown" in dd_info
        assert dd_info["max_drawdown"] <= 0
```

### 2. 集成测试用例

```python
# tests/integration/test_data_flow.py
import pytest
from stock.stock_data_fetcher import StockDataFetcher
from stock.stock_ai_analysis import StockAIAnalyzer

class TestDataFlow:
    """数据流集成测试"""

    def test_stock_analysis_workflow(self):
        """测试完整的股票分析流程"""
        # 1. 获取数据
        fetcher = StockDataFetcher()
        stock_data = fetcher.get_stock_overview("000001", "平安银行")

        assert stock_data is not None
        assert "current_price" in stock_data

        # 2. AI分析
        analyzer = StockAIAnalyzer()
        result = analyzer.analyze_technical(stock_data)

        assert result.success
        assert len(result.report) > 0
```

### 3. 端到端测试用例

```python
# tests/e2e/test_complete_workflow.py
import pytest
import subprocess
import time

class TestCompleteWorkflow:
    """完整工作流测试"""

    def test_report_generation_pipeline(self):
        """测试报告生成管道"""
        # 运行报告生成脚本
        cmd = [
            "python", "tests/test_stock_report.py",
            "--stock-code", "000001",
            "--stock-name", "平安银行",
            "--format", "markdown"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        assert result.returncode == 0
        assert "报告生成成功" in result.stdout

    def test_ui_loading(self):
        """测试UI加载"""
        # 启动Streamlit应用
        import streamlit as st

        # 模拟UI组件加载
        from ui.components.page_stock import display_stock_info

        # 验证组件可以正常初始化
        assert callable(display_stock_info)
```

## 测试数据管理

### 测试数据准备

```python
# tests/fixtures/data_generator.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_stock_data(days=252):
    """生成模拟股票数据"""
    dates = [datetime.now() - timedelta(days=i) for i in range(days)]
    dates.reverse()

    # 生成随机价格序列
    returns = np.random.normal(0.001, 0.02, days)
    prices = 100 * np.exp(np.cumsum(returns))

    data = pd.DataFrame({
        'Date': dates,
        'Open': prices * (1 + np.random.normal(0, 0.005, days)),
        'High': prices * (1 + np.abs(np.random.normal(0, 0.01, days))),
        'Low': prices * (1 - np.abs(np.random.normal(0, 0.01, days))),
        'Close': prices,
        'Volume': np.random.randint(1000000, 10000000, days)
    })

    return data

def generate_market_sentiment_data():
    """生成模拟市场情绪数据"""
    sentiments = ['positive', 'neutral', 'negative']
    news_data = []

    for i in range(100):
        news_data.append({
            'title': f'新闻标题 {i}',
            'content': f'这是第{i}条新闻内容',
            'sentiment': np.random.choice(sentiments),
            'impact_score': np.random.uniform(0, 10)
        })

    return news_data
```

## 测试运行指南

### 运行所有测试

```bash
# 运行所有测试
pytest tests/

# 运行特定目录的测试
pytest tests/unit/

# 运行特定文件
pytest tests/test_stock_report.py

# 运行特定测试函数
pytest tests/unit/test_stock/test_data_fetcher.py::TestStockDataFetcher::test_get_stock_overview
```

### 测试配置选项

```bash
# 生成覆盖率报告
pytest --cov=stock --cov-report=html

# 并行运行测试
pytest -n auto

# 显示详细输出
pytest -v

# 只运行失败的测试
pytest --lf

# 运行标记的测试
pytest -m "slow"  # 运行标记为slow的测试
```

## 持续集成建议

### GitHub Actions 配置

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run tests
      run: |
        pytest --cov=./ --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## 质量保证

### 测试覆盖率目标
- **单元测试覆盖率**: > 80%
- **集成测试覆盖率**: > 60%
- **关键路径覆盖率**: 100%

### 测试最佳实践
1. **AAA模式**: Arrange-Act-Assert
2. **独立性**: 测试之间不应相互依赖
3. **可重复**: 测试结果应该是一致的
4. **快速执行**: 单元测试应该快速完成
5. **清晰的描述**: 测试名称应该清楚表达测试内容

## 常见问题

### Q: 如何测试需要API密钥的功能？
A: 使用Mock对象模拟API响应，或使用测试专用的API密钥。

### Q: 如何测试数据库操作？
A: 使用内存数据库或测试数据库，确保测试环境独立。

### Q: 如何处理异步代码测试？
A: 使用pytest-asyncio插件，或使用同步包装器。

### Q: 如何优化慢速测试？
A: 使用fixture缓存数据、并行测试、标记慢速测试。

## 相关文件清单

```
tests/
├── __init__.py                # 测试包初始化
├── test_stock_report.py       # 股票报告测试
├── test_market_report.py      # 市场报告测试
├── conftest.py               # pytest配置
└── fixtures/                 # 测试数据目录
    └── data_generator.py      # 测试数据生成器
```

## 变更记录

### 2025-12-07 22:48:54
- ✨ 创建模块文档
- 🧪 整理现有测试用例
- 📋 提供测试框架建议

---

*良好的测试是代码质量的保障，建议持续完善测试覆盖率。*