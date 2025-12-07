#!/usr/bin/env python3
"""
pytest 配置文件
提供测试用的 fixtures 和配置
"""
import sys
import os
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
import streamlit as st

# 添加项目根路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)


@pytest.fixture(scope="session")
def project_root_path():
    """项目根路径"""
    return project_root


@pytest.fixture
def sample_stock_identity():
    """示例股票标识"""
    return {
        'code': '000001',
        'name': '平安银行',
        'market_name': 'A股'
    }


@pytest.fixture
def sample_kline_data():
    """示例K线数据"""
    days = 100
    dates = pd.date_range('2024-01-01', periods=days)

    # 生成模拟数据
    base_price = 10.0
    returns = np.random.normal(0.001, 0.02, days)
    prices = base_price * np.exp(np.cumsum(returns))

    df = pd.DataFrame({
        'datetime': dates,
        'open': prices * (1 + np.random.normal(0, 0.005, days)),
        'high': prices * (1 + np.abs(np.random.normal(0, 0.01, days))),
        'low': prices * (1 - np.abs(np.random.normal(0, 0.01, days))),
        'close': prices,
        'volume': np.random.randint(1000000, 10000000, days)
    })

    return df


@pytest.fixture
def sample_technical_data():
    """示例技术指标数据"""
    return {
        'MA5': 10.50,
        'MA10': 10.45,
        'MA20': 10.40,
        'MA60': 10.35,
        'RSI': 65.2,
        'MACD': 0.05,
        'Signal': 0.03,
        'Histogram': 0.02,
        'K': 75.3,
        'D': 70.1,
        'J': 85.7
    }


@pytest.fixture
def sample_risk_metrics():
    """示例风险指标"""
    return {
        'risk_level': '中',
        'volatility': 0.25,
        'max_drawdown': -0.15,
        'sharpe_ratio': 1.2,
        'var_95': -0.03
    }


@pytest.fixture
def mock_streamlit():
    """模拟 Streamlit 组件"""
    with patch('streamlit.set_page_config'), \
         patch('streamlit.sidebar'), \
         patch('streamlit.header') as mock_header, \
         patch('streamlit.subheader') as mock_subheader, \
         patch('streamlit.metric') as mock_metric, \
         patch('streamlit.columns') as mock_columns, \
         patch('streamlit.plotly_chart') as mock_chart, \
         patch('streamlit.spinner') as mock_spinner, \
         patch('streamlit.success') as mock_success, \
         patch('streamlit.error') as mock_error, \
         patch('streamlit.warning') as mock_warning:

        # 配置返回值
        mock_columns.return_value = [Mock(), Mock(), Mock()]

        yield {
            'header': mock_header,
            'subheader': mock_subheader,
            'metric': mock_metric,
            'columns': mock_columns,
            'chart': mock_chart,
            'spinner': mock_spinner,
            'success': mock_success,
            'error': mock_error,
            'warning': mock_warning
        }


@pytest.fixture
def mock_session_state():
    """模拟 session_state"""
    session_state = {}

    def get(key, default=None):
        return session_state.get(key, default)

    def __setitem__(key, value):
        session_state[key] = value

    def __getitem__(key):
        return session_state[key]

    mock_state = Mock()
    mock_state.get = get
    mock_state.__setitem__ = __setitem__
    mock_state.__getitem__ = __getitem__

    with patch.object(st, 'session_state', mock_state):
        yield mock_state


@pytest.fixture
def sample_stock_report():
    """示例股票报告"""
    return """# 平安银行(000001)分析报告

## 基本信息
- 当前价格: ¥12.50
- 涨跌幅: +2.50%
- 成交量: 1000万

## 技术分析
- MA5: 10.50
- MA20: 10.40
- RSI: 65.2

## AI分析
该股票近期表现稳健，建议关注...
"""


@pytest.fixture
def sample_market_report():
    """示例市场报告"""
    return """# 市场分析报告

## 市场概况
- 上证指数: 3200点 (+1.2%)
- 深证成指: 11000点 (+1.5%)
- 创业板指: 2100点 (+1.8%)

## 市场情绪
- 恐贪指数: 65 (贪婪)
- 涨停数: 50
- 跌停数: 10

## 资金流向
- 北向资金: +50亿
- 主力资金: +100亿
"""


@pytest.fixture
def mock_api_response():
    """模拟API响应"""
    return {
        'choices': [{
            'message': {
                'content': '这是AI生成的分析报告'
            }
        }],
        'usage': {
            'prompt_tokens': 100,
            'completion_tokens': 200,
            'total_tokens': 300
        }
    }


@pytest.fixture
def sample_config():
    """示例配置数据"""
    return {
        'LLM_OPENAI': {
            'API_KEY': 'test-key',
            'BASE_URL': 'https://api.openai.com/v1',
            'DEFAULT_MODEL': 'gpt-3.5-turbo',
            'TIMEOUT': 30,
            'MAX_RETRIES': 3,
            'DEFAULT_TEMPERATURE': 0.7
        },
        'LLM_CACHE': {
            'ENABLE_CACHE': True,
            'CACHE_TTL': 3600
        },
        'ANALYSIS': {
            'RISK_PREFERENCE': 'neutral',
            'CUSTOM_PRINCIPLES': '长期价值投资'
        },
        'USER_PROFILE': {
            'RAW': '测试用户',
            'MISTAKES': ['追涨杀跌', '频繁交易']
        }
    }


# 测试标记
def pytest_configure(config):
    """配置 pytest 标记"""
    config.addinivalue_line(
        "markers", "unit: 单元测试"
    )
    config.addinivalue_line(
        "markers", "integration: 集成测试"
    )
    config.addinivalue_line(
        "markers", "e2e: 端到端测试"
    )
    config.addinivalue_line(
        "markers", "slow: 慢速测试（需要网络或数据库）"
    )


# 测试收集钩子
def pytest_collection_modifyitems(config, items):
    """修改测试收集"""
    # 为没有标记的测试添加 unit 标记
    for item in items:
        if not any(item.iter_markers()):
            item.add_marker(pytest.mark.unit)