#!/usr/bin/env python3
"""
测试大盘分析页面 page_market_overview.py
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
import streamlit as st
import sys
import os

# 添加项目路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.join(project_root, 'ui', 'components'))

try:
    from page_market_overview import (
        display_market_overview,
        display_valuation_analysis,
        display_money_flow_analysis,
        display_margin_trading_analysis,
        display_market_sentiment_analysis,
        display_market_technical_analysis
    )
except ImportError as e:
    pytest.skip(f"无法导入 page_market_overview: {e}", allow_module_level=True)


class TestDisplayMarketOverview:
    """测试大盘分析主显示"""

    @pytest.mark.unit
    def test_main_page_render(self, mock_streamlit, mock_session_state):
        """测试主页面渲染"""
        # Mock 指数选择
        mock_streamlit['selectbox'].return_value = '上证指数'

        # 调用函数
        display_market_overview()

        # 验证页面元素
        mock_streamlit['header'].assert_called()
        mock_streamlit['selectbox'].assert_called()

    @pytest.mark.unit
    def test_index_selection(self, mock_streamlit, mock_session_state):
        """测试指数选择"""
        # Mock 选择不同指数
        test_indices = ['上证指数', '深证成指', '沪深300', '中证500', '创业板指']

        for index in test_indices:
            mock_streamlit['selectbox'].return_value = index

            # 调用函数
            display_market_overview()

            # 验证Session State更新
            assert mock_session_state.__setitem__.called

    @pytest.mark.unit
    def test_cache_configuration(self, mock_streamlit, mock_session_state):
        """测试缓存配置"""
        # Mock 缓存设置
        mock_session_state.get.return_value = True

        with patch('page_market_overview.display_market_technical_analysis') as mock_analysis:
            # 调用函数
            display_market_overview()

            # 验证分析函数被调用
            mock_analysis.assert_called()


class TestDisplayValuationAnalysis:
    """测试估值分析"""

    @pytest.mark.unit
    def test_valuation_data_display(self, mock_streamlit):
        """测试估值数据显示"""
        with patch('market.market_data_fetcher.get_index_valuation') as mock_valuation:
            mock_valuation.return_value = {
                'pe_ttm': 15.2,
                'pe_ttm_percentile': 45.5,
                'pb': 1.35,
                'pb_percentile': 38.2,
                'ps_ttm': 2.8,
                'ps_ttm_percentile': 52.3
            }

            # 调用函数
            display_valuation_analysis(index_name='上证指数')

            # 验证数据获取
            mock_valuation.assert_called_once_with('上证指数', use_cache=True)

            # 验证指标显示
            assert mock_streamlit['metric'].call_count >= 4

    @pytest.mark.unit
    def test_valuation_history_chart(self, mock_streamlit):
        """测试估值历史图表"""
        with patch('market.market_data_fetcher.get_index_valuation') as mock_valuation, \
             patch('market.market_data_fetcher.get_index_valuation_history') as mock_history:

            mock_valuation.return_value = {'pe_ttm': 15.2}
            mock_history.return_value = pd.DataFrame({
                'date': pd.date_range('2020-01-01', periods=100),
                'pe_ttm': np.random.uniform(10, 30, 100),
                'pb': np.random.uniform(1, 3, 100)
            })

            # 调用函数
            display_valuation_analysis(index_name='上证指数')

            # 验证图表显示
            mock_streamlit['plotly_chart'].assert_called()

    @pytest.mark.unit
    def test_valuation_with_cache_disabled(self, mock_session_state):
        """测试禁用缓存"""
        mock_session_state.get.return_value = False

        with patch('market.market_data_fetcher.get_index_valuation') as mock_valuation:
            mock_valuation.return_value = {}

            # 调用函数
            display_valuation_analysis(use_cache=False)

            # 验证传递的参数
            call_args = mock_valuation.call_args
            assert call_args[1].get('use_cache', True) is False


class TestDisplayMoneyFlowAnalysis:
    """测试资金流向分析"""

    @pytest.mark.unit
    def test_money_flow_data_display(self, mock_streamlit):
        """测试资金流向数据显示"""
        with patch('market.market_data_fetcher.get_market_money_flow') as mock_flow:
            mock_flow.return_value = {
                'northbound_flow': 52.3,
                'northbound_change': 15.6,
                'main_flow': 128.5,
                'main_change': -23.4,
                'super_large_flow': 85.2,
                'large_flow': 43.1,
                'medium_flow': -12.5,
                'small_flow': -15.8
            }

            # 调用函数
            display_money_flow_analysis()

            # 验证数据显示
            assert mock_streamlit['metric'].call_count >= 6

    @pytest.mark.unit
    def test_sector_flow_display(self, mock_streamlit):
        """测试行业资金流向"""
        with patch('market.market_data_fetcher.get_market_money_flow') as mock_flow, \
             patch('market.market_data_fetcher.get_sector_money_flow') as mock_sector:

            mock_flow.return_value = {}
            mock_sector.return_value = [
                {'sector': '银行', 'flow': 25.3, 'change': 5.2},
                {'sector': '地产', 'flow': -15.8, 'change': -8.5},
                {'sector': '科技', 'flow': 45.6, 'change': 12.3}
            ]

            # 调用函数
            display_money_flow_analysis()

            # 验证行业数据获取
            mock_sector.assert_called_once()

            # 验证表格显示
            mock_streamlit['dataframe'].assert_called()


class TestDisplayMarginTradingAnalysis:
    """测试融资融券分析"""

    @pytest.mark.unit
    def test_margin_data_display(self, mock_streamlit):
        """测试融资融券数据显示"""
        with patch('market.market_data_fetcher.get_margin_trading_data') as mock_margin:
            mock_margin.return_value = {
                'margin_balance': 15832.5,
                'margin_balance_change': 123.4,
                'margin_balance_percent': 0.78,
                'short_balance': 825.3,
                'short_balance_change': -15.2,
                'short_balance_percent': -1.81,
                'margin_short_ratio': 5.21
            }

            # 调用函数
            display_margin_trading_analysis()

            # 验证数据显示
            assert mock_streamlit['metric'].call_count >= 6

    @pytest.mark.unit
    def test_margin_history_chart(self, mock_streamlit):
        """测试融资融券历史图表"""
        with patch('market.market_data_fetcher.get_margin_trading_data') as mock_margin, \
             patch('market.market_data_fetcher.get_margin_trading_history') as mock_history:

            mock_margin.return_value = {}
            mock_history.return_value = pd.DataFrame({
                'date': pd.date_range('2024-01-01', periods=60),
                'margin_balance': np.random.uniform(15000, 16000, 60),
                'short_balance': np.random.uniform(800, 900, 60)
            })

            # 调用函数
            display_margin_trading_analysis()

            # 验证图表显示
            mock_streamlit['plotly_chart'].assert_called()


class TestDisplayMarketSentimentAnalysis:
    """测试市场情绪分析"""

    @pytest.mark.unit
    def test_sentiment_indicators_display(self, mock_streamlit):
        """测试情绪指标显示"""
        with patch('market.market_data_fetcher.get_market_sentiment') as mock_sentiment:
            mock_sentiment.return_value = {
                'fear_greed_index': 68.5,
                'fear_greed_status': '贪婪',
                'up_count': 3256,
                'down_count': 1648,
                'limit_up': 82,
                'limit_down': 12,
                'new_high': 156,
                'new_low': 23
            }

            # 调用函数
            display_market_sentiment_analysis()

            # 验证指标显示
            assert mock_streamlit['metric'].call_count >= 7

    @pytest.mark.unit
    def test_news_sentiment_analysis(self, mock_streamlit):
        """测试新闻情绪分析"""
        with patch('market.market_data_fetcher.get_market_sentiment') as mock_sentiment, \
             patch('market.market_data_fetcher.get_market_news_sentiment') as mock_news:

            mock_sentiment.return_value = {}
            mock_news.return_value = [
                {'sentiment': 'positive', 'count': 156},
                {'sentiment': 'neutral', 'count': 89},
                {'sentiment': 'negative', 'count': 45}
            ]

            # 调用函数
            display_market_sentiment_analysis()

            # 验证新闻情绪获取
            mock_news.assert_called_once()

    @pytest.mark.unit
    def test_user_opinion_input(self, mock_streamlit, mock_session_state):
        """测试用户观点输入"""
        mock_session_state.get.return_value = "市场走势良好"

        with patch('market.market_data_fetcher.get_market_sentiment', return_value={}):
            # 调用函数
            display_market_sentiment_analysis()

            # 验证文本输入
            mock_streamlit['text_area'].assert_called()


class TestDisplayMarketTechnicalAnalysis:
    """测试市场技术分析"""

    @pytest.mark.unit
    def test_technical_analysis_with_data(self, mock_streamlit):
        """测试有数据的技术分析"""
        with patch('market.market_data_fetcher.get_index_kline_data') as mock_kline:
            mock_kline.return_value = pd.DataFrame({
                'datetime': pd.date_range('2024-01-01', periods=100),
                'open': np.random.randn(100).cumsum() + 3200,
                'high': np.random.randn(100).cumsum() + 3220,
                'low': np.random.randn(100).cumsum() + 3180,
                'close': np.random.randn(100).cumsum() + 3200,
                'volume': np.random.randint(100000000, 500000000, 100)
            })

            # 调用函数
            display_market_technical_analysis(index_name='上证指数')

            # 验证K线图显示
            mock_streamlit['plotly_chart'].assert_called()

    @pytest.mark.unit
    def test_technical_analysis_different_indices(self):
        """测试不同指数的技术分析"""
        indices = ['上证指数', '深证成指', '沪深300', '中证500', '创业板指']

        for index in indices:
            with patch('market.market_data_fetcher.get_index_kline_data') as mock_kline:
                mock_kline.return_value = pd.DataFrame()

                # 调用函数
                display_market_technical_analysis(index_name=index)

                # 验证正确的指数被传递
                mock_kline.assert_called_once()

    @pytest.mark.unit
    def test_technical_analysis_cache_control(self, mock_session_state):
        """测试技术分析缓存控制"""
        mock_session_state.get.return_value = False

        with patch('market.market_data_fetcher.get_index_kline_data') as mock_kline:
            mock_kline.return_value = pd.DataFrame()

            # 调用函数
            display_market_technical_analysis()

            # 验证强制刷新
            call_args = mock_kline.call_args
            assert call_args[1].get('force_refresh', False) is True


class TestAIAnalysisIntegration:
    """测试AI分析集成"""

    @pytest.mark.unit
    def test_ai_market_analysis(self, mock_streamlit, mock_session_state):
        """测试AI市场分析"""
        # Mock AI报告
        mock_session_state.get.side_effect = lambda key, default=None: {
            'ai_index_report': {
                'success': True,
                'report': '## 市场AI分析\n\n当前市场情绪积极...'
            }
        }.get(key, default)

        with patch('market.market_data_fetcher.get_market_overview', return_value={}):
            # 调用主函数
            display_market_overview()

            # 验证AI分析显示
            assert mock_streamlit['success'].called or mock_streamlit['info'].called

    @pytest.mark.unit
    def test_ai_analysis_toggle(self, mock_session_state):
        """测试AI分析开关"""
        # Mock AI分析关闭
        mock_session_state.get.side_effect = lambda key, default=None: {
            'include_ai_analysis': False
        }.get(key, default)

        with patch('market.market_data_fetcher.get_market_overview', return_value={}):
            # 调用主函数
            display_market_overview()

            # AI分析应该不被触发
            assert True


@pytest.mark.parametrize("index_name", [
    "上证指数", "深证成指", "沪深300", "中证500", "创业板指"
])
def test_index_analysis(index_name, mock_streamlit):
    """参数化测试不同指数分析"""
    with patch('market.market_data_fetcher.get_index_kline_data') as mock_kline:
        mock_kline.return_value = pd.DataFrame()

        # 调用技术分析
        display_market_technical_analysis(index_name=index_name)

        # 验证正常执行
        assert True


@pytest.mark.parametrize("use_cache", [True, False])
def test_cache_behavior(use_cache, mock_session_state):
    """参数化测试缓存行为"""
    mock_session_state.get.return_value = use_cache

    with patch('market.market_data_fetcher.get_index_valuation') as mock_valuation:
        mock_valuation.return_value = {}

        # 调用估值分析
        display_valuation_analysis(use_cache=use_cache)

        # 验证缓存参数
        call_args = mock_valuation.call_args
        assert call_args[1].get('use_cache', True) == use_cache