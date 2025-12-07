#!/usr/bin/env python3
"""
测试通用UI组件 page_common.py
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import plotly.graph_objects as go
import sys
import os

# 添加项目路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.join(project_root, 'ui', 'components'))

try:
    from page_common import (
        display_technical_indicators,
        display_technical_analysis_tab,
        display_risk_analysis,
        display_kline_charts
    )
except ImportError as e:
    pytest.skip(f"无法导入 page_common: {e}", allow_module_level=True)


class TestDisplayTechnicalIndicators:
    """测试技术指标展示函数"""

    @pytest.mark.unit
    def test_display_with_valid_data(self, mock_streamlit):
        """测试有效数据的显示"""
        tech_data = {
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

        # 调用函数
        display_technical_indicators(tech_data)

        # 验证调用
        assert mock_streamlit['metric'].call_count >= 11  # 至少11个指标
        assert mock_streamlit['columns'].call_count >= 3   # 至少3列布局

    @pytest.mark.unit
    def test_display_with_partial_data(self, mock_streamlit):
        """测试部分数据的显示"""
        tech_data = {
            'MA5': 10.50,
            'MA10': 10.45,
            'RSI': 65.2
        }

        # 调用函数
        display_technical_indicators(tech_data)

        # 验证调用
        assert mock_streamlit['metric'].call_count >= 3

    @pytest.mark.unit
    def test_display_with_empty_data(self, mock_streamlit):
        """测试空数据的处理"""
        tech_data = {}

        # 调用函数
        display_technical_indicators(tech_data)

        # 应该不会抛出异常
        assert True

    @pytest.mark.unit
    def test_display_with_none_data(self, mock_streamlit):
        """测试 None 数据的处理"""
        tech_data = None

        # 调用函数
        with pytest.raises(Exception):
            display_technical_indicators(tech_data)


class TestDisplayTechnicalAnalysisTab:
    """测试技术分析标签页函数"""

    @pytest.mark.unit
    def test_display_stock_analysis(self, mock_streamlit, mock_session_state):
        """测试个股技术分析"""
        stock_identity = {
            'code': '000001',
            'name': '平安银行',
            'market_name': 'A股'
        }

        # Mock 获取K线数据
        with patch('stock.stock_data_fetcher.get_stock_kline_data') as mock_kline:
            mock_kline.return_value = pd.DataFrame({
                'datetime': pd.date_range('2024-01-01', periods=100),
                'open': np.random.randn(100).cumsum() + 100,
                'high': np.random.randn(100).cumsum() + 102,
                'low': np.random.randn(100).cumsum() + 98,
                'close': np.random.randn(100).cumsum() + 100,
                'volume': np.random.randint(1000000, 10000000, 100)
            })

            # 调用函数
            display_technical_analysis_tab(stock_identity=stock_identity)

            # 验证调用
            mock_kline.assert_called_once()

    @pytest.mark.unit
    def test_display_index_analysis(self, mock_streamlit, mock_session_state):
        """测试指数技术分析"""
        index_name = '上证指数'

        # Mock 获取指数数据
        with patch('market.market_data_fetcher.get_index_kline_data') as mock_kline:
            mock_kline.return_value = pd.DataFrame({
                'datetime': pd.date_range('2024-01-01', periods=100),
                'open': np.random.randn(100).cumsum() + 3000,
                'high': np.random.randn(100).cumsum() + 3020,
                'low': np.random.randn(100).cumsum() + 2980,
                'close': np.random.randn(100).cumsum() + 3000,
                'volume': np.random.randint(100000000, 500000000, 100)
            })

            # 调用函数
            display_technical_analysis_tab(index_name=index_name)

            # 验证调用
            mock_kline.assert_called_once()

    @pytest.mark.unit
    def test_with_cache_disabled(self, mock_session_state):
        """测试禁用缓存的情况"""
        mock_session_state.get.return_value = False

        with patch('stock.stock_data_fetcher.get_stock_kline_data') as mock_kline:
            mock_kline.return_value = pd.DataFrame()
            display_technical_analysis_tab(stock_identity={'code': '000001'})

            # 验证强制刷新参数
            call_args = mock_kline.call_args
            assert call_args[1].get('force_refresh', False) == True


class TestDisplayRiskAnalysis:
    """测试风险分析展示函数"""

    @pytest.mark.unit
    def test_display_risk_metrics(self, mock_streamlit):
        """测试风险指标显示"""
        risk_metrics = {
            'risk_level': '中',
            'volatility': 0.25,
            'max_drawdown': -0.15,
            'sharpe_ratio': 1.2,
            'var_95': -0.03
        }

        # 调用函数
        display_risk_analysis(risk_metrics)

        # 验证调用
        mock_streamlit['metric'].call_count >= 4

    @pytest.mark.unit
    def test_display_high_risk(self, mock_streamlit):
        """测试高风险显示"""
        risk_metrics = {
            'risk_level': '高',
            'volatility': 0.45,
            'max_drawdown': -0.35,
            'sharpe_ratio': 0.5,
            'var_95': -0.08
        }

        # 调用函数
        display_risk_analysis(risk_metrics)

        # 验证调用
        mock_streamlit['warning'].assert_called()

    @pytest.mark.unit
    def test_display_low_risk(self, mock_streamlit):
        """测试低风险显示"""
        risk_metrics = {
            'risk_level': '低',
            'volatility': 0.15,
            'max_drawdown': -0.05,
            'sharpe_ratio': 2.0,
            'var_95': -0.01
        }

        # 调用函数
        display_risk_analysis(risk_metrics)

        # 验证调用
        mock_streamlit['success'].assert_called()


class TestDisplayKlineCharts:
    """测试K线图渲染函数"""

    @pytest.mark.unit
    def test_display_stock_chart(self, mock_streamlit, sample_kline_data):
        """测试股票K线图"""
        # 调用函数
        display_kline_charts(
            sample_kline_data,
            chart_type="stock",
            title_prefix="平安银行"
        )

        # 验证调用
        mock_streamlit['chart'].assert_called()

        # 验证图表配置
        call_args = mock_streamlit['chart'].call_args[0][0]
        assert isinstance(call_args, go.Figure)

    @pytest.mark.unit
    def test_display_index_chart(self, mock_streamlit, sample_kline_data):
        """测试指数K线图"""
        # 调用函数
        display_kline_charts(
            sample_kline_data,
            chart_type="index",
            title_prefix="上证指数"
        )

        # 验证调用
        mock_streamlit['chart'].assert_called()

    @pytest.mark.unit
    def test_with_invalid_dataframe(self):
        """测试无效DataFrame的处理"""
        # 缺少必要列的DataFrame
        invalid_df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=10),
            'price': np.random.randn(10)
        })

        # 调用函数应该抛出异常
        with pytest.raises(KeyError):
            display_kline_charts(invalid_df)

    @pytest.mark.unit
    def test_with_empty_dataframe(self, mock_streamlit):
        """测试空DataFrame的处理"""
        empty_df = pd.DataFrame()

        # 调用函数
        display_kline_charts(empty_df)

        # 应该显示错误信息
        mock_streamlit['error'].assert_called()

    @pytest.mark.unit
    def test_chart_configuration(self, mock_streamlit, sample_kline_data):
        """测试图表配置"""
        # 调用函数
        display_kline_charts(
            sample_kline_data,
            chart_type="stock",
            title_prefix="平安银行"
        )

        # 获取图表对象
        fig = mock_streamlit['chart'].call_args[0][0]

        # 验证图表标题
        assert "平安银行" in fig.layout.title.text

        # 验证坐标轴标题
        assert fig.layout.yaxis.title.text
        assert fig.layout.xaxis.title.text

        # 验证图表高度
        assert fig.layout.height == 600


class TestIntegration:
    """集成测试"""

    @pytest.mark.integration
    def test_complete_technical_analysis(self, mock_streamlit, mock_session_state):
        """测试完整的技术分析流程"""
        # 准备测试数据
        stock_identity = {
            'code': '000001',
            'name': '平安银行',
            'market_name': 'A股'
        }

        kline_data = pd.DataFrame({
            'datetime': pd.date_range('2024-01-01', periods=100),
            'open': np.random.randn(100).cumsum() + 100,
            'high': np.random.randn(100).cumsum() + 102,
            'low': np.random.randn(100).cumsum() + 98,
            'close': np.random.randn(100).cumsum() + 100,
            'volume': np.random.randint(1000000, 10000000, 100)
        })

        tech_data = {
            'MA5': 10.50,
            'MA10': 10.45,
            'MA20': 10.40,
            'RSI': 65.2,
            'MACD': 0.05
        }

        # Mock 外部依赖
        with patch('stock.stock_data_fetcher.get_stock_kline_data', return_value=kline_data), \
             patch('utils.calculate_technical_indicators', return_value=tech_data):

            # 调用函数
            display_technical_analysis_tab(stock_identity=stock_identity)

            # 验证组件协同工作
            assert mock_streamlit['header'].called
            assert mock_streamlit['chart'].called


@pytest.mark.parametrize("chart_type", ["stock", "index"])
@pytest.mark.parametrize("title_prefix", ["平安银行", "上证指数", ""])
def test_kline_chart_parameters(chart_type, title_prefix, mock_streamlit, sample_kline_data):
    """参数化测试K线图的不同参数组合"""
    display_kline_charts(
        sample_kline_data,
        chart_type=chart_type,
        title_prefix=title_prefix
    )

    # 验证函数被调用
    mock_streamlit['chart'].assert_called_once()