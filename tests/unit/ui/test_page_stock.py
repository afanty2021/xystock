#!/usr/bin/env python3
"""
测试个股分析页面 page_stock.py
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch, MagicMock
import streamlit as st
import sys
import os

# 添加项目路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.join(project_root, 'ui', 'components'))

try:
    from page_stock import (
        display_stock_info,
        display_basic_info,
        display_fundamental_analysis,
        display_technical_analysis,
        display_news_analysis,
        display_chips_analysis,
        display_company_analysis,
        display_comprehensive_analysis
    )
except ImportError as e:
    pytest.skip(f"无法导入 page_stock: {e}", allow_module_level=True)


class TestDisplayStockInfo:
    """测试股票信息主显示函数"""

    @pytest.mark.unit
    def test_display_with_valid_identity(self, mock_streamlit, mock_session_state):
        """测试有效股票标识"""
        stock_identity = {
            'code': '000001',
            'name': '平安银行',
            'market_name': 'A股'
        }

        # Mock 基本数据获取
        with patch('stock.stock_data_fetcher.get_stock_basic_info') as mock_basic:
            mock_basic.return_value = {
                'current_price': 12.50,
                'change_percent': 2.5,
                'volume': 10000000
            }

            # 调用函数
            display_stock_info(stock_identity)

            # 验证调用
            mock_basic.assert_called_once_with('000001')

    @pytest.mark.unit
    def test_display_without_market_name(self, mock_streamlit, mock_session_state):
        """测试没有市场名称的情况"""
        stock_identity = {
            'code': '000001',
            'name': '平安银行'
            # 没有 market_name
        }

        with patch('stock.stock_data_fetcher.get_stock_basic_info') as mock_basic:
            mock_basic.return_value = {}

            # 调用函数
            display_stock_info(stock_identity)

            # 应该使用默认值 "A股"
            mock_basic.assert_called_once_with('000001')

    @pytest.mark.unit
    def test_display_with_invalid_identity(self, mock_streamlit):
        """测试无效股票标识"""
        stock_identity = {}  # 空字典

        # 调用函数
        display_stock_info(stock_identity)

        # 应该显示错误信息
        mock_streamlit['error'].assert_called()

    @pytest.mark.unit
    def test_with_ai_analysis_enabled(self, mock_session_state):
        """测试启用AI分析的情况"""
        stock_identity = {
            'code': '000001',
            'name': '平安银行',
            'market_name': 'A股'
        }

        # 设置启用AI分析
        mock_session_state.get.side_effect = lambda key, default=None: {
            'use_cache': True,
            'include_ai_analysis': True,
            'ai_fundamental_report': {},
            'ai_market_report': {},
            'ai_news_report': {},
            'ai_chip_report': {},
            'ai_company_report': {},
            'ai_comprehensive_report': {}
        }.get(key, default)

        with patch('stock.stock_data_fetcher.get_stock_basic_info', return_value={}), \
             patch('stock.stock_ai_analysis.analyze_fundamental') as mock_ai:

            # 调用函数
            display_stock_info(stock_identity)

            # 验证AI分析被调用
            assert mock_ai.called


class TestDisplayBasicInfo:
    """测试基本信息展示"""

    @pytest.mark.unit
    def test_display_realtime_data(self, mock_streamlit):
        """测试实时数据显示"""
        stock_identity = {
            'code': '000001',
            'name': '平安银行',
            'market_name': 'A股'
        }

        # Mock 获取基本信息
        with patch('stock.stock_data_fetcher.get_stock_basic_info') as mock_basic:
            mock_basic.return_value = {
                'current_price': 12.50,
                'change_percent': 2.5,
                'change_amount': 0.30,
                'volume': 10000000,
                'turnover': 125000000,
                'amplitude': 3.2,
                'high': 12.80,
                'low': 12.20,
                'open': 12.30,
                'prev_close': 12.20
            }

            # 调用函数
            display_basic_info(stock_identity)

            # 验证数据显示
            assert mock_streamlit['metric'].call_count >= 8

    @pytest.mark.unit
    def test_display_with_missing_data(self, mock_streamlit):
        """测试部分数据缺失"""
        stock_identity = {
            'code': '000001',
            'name': '平安银行',
            'market_name': 'A股'
        }

        # Mock 部分数据
        with patch('stock.stock_data_fetcher.get_stock_basic_info') as mock_basic:
            mock_basic.return_value = {
                'current_price': 12.50,
                'change_percent': 2.5
                # 缺少其他数据
            }

            # 调用函数
            display_basic_info(stock_identity)

            # 应该不抛出异常
            assert True

    @pytest.mark.unit
    def test_display_error_handling(self, mock_streamlit):
        """测试错误处理"""
        stock_identity = {
            'code': '000001',
            'name': '平安银行',
            'market_name': 'A股'
        }

        # Mock 抛出异常
        with patch('stock.stock_data_fetcher.get_stock_basic_info') as mock_basic:
            mock_basic.side_effect = Exception("网络错误")

            # 调用函数
            display_basic_info(stock_identity)

            # 应该显示错误信息
            mock_streamlit['error'].assert_called()


class TestDisplayFundamentalAnalysis:
    """测试基本面分析"""

    @pytest.mark.unit
    def test_display_complete_metrics(self, mock_streamlit):
        """测试完整的财务指标"""
        stock_identity = {
            'code': '000001',
            'name': '平安银行',
            'market_name': 'A股'
        }

        # Mock 基本面数据
        with patch('stock.stock_data_fetcher.get_stock_fundamental_data') as mock_fundamental:
            mock_fundamental.return_value = {
                'pe_ratio': 8.5,
                'pb_ratio': 0.8,
                'roe': 12.3,
                'roa': 1.2,
                'eps': 2.5,
                'bps': 15.6,
                'market_cap': 2430.5,
                'dividend_yield': 3.2,
                'debt_ratio': 92.5,
                'current_ratio': 0.85,
                'revenue_growth': 5.2,
                'profit_growth': 15.3
            }

            # 调用函数
            display_fundamental_analysis(stock_identity)

            # 验证指标显示
            mock_fundamental.assert_called_once_with('000001')
            assert mock_streamlit['metric'].call_count >= 12

    @pytest.mark.unit
    def test_display_with_ai_analysis(self, mock_streamlit, mock_session_state):
        """测试包含AI分析"""
        stock_identity = {
            'code': '000001',
            'name': '平安银行',
            'market_name': 'A股'
        }

        # 设置AI报告已存在
        mock_session_state.get.side_effect = lambda key, default=None: {
            'ai_fundamental_report': {
                'success': True,
                'report': '这是AI生成的基本面分析报告'
            }
        }.get(key, default)

        with patch('stock.stock_data_fetcher.get_stock_fundamental_data', return_value={}):
            # 调用函数
            display_fundamental_analysis(stock_identity)

            # 验证AI报告显示
            assert mock_streamlit['success'].called or mock_streamlit['info'].called


class TestDisplayNewsAnalysis:
    """测试新闻分析"""

    @pytest.mark.unit
    def test_display_news_list(self, mock_streamlit):
        """测试新闻列表显示"""
        stock_identity = {
            'code': '000001',
            'name': '平安银行',
            'market_name': 'A股'
        }

        # Mock 新闻数据
        with patch('stock.stock_data_fetcher.get_stock_news') as mock_news:
            mock_news.return_value = [
                {
                    'title': '平安银行发布2024年业绩报告',
                    'content': '银行净利润同比增长...',
                    'publish_time': '2024-12-07 10:00:00',
                    'source': '财经网',
                    'sentiment': 'positive',
                    'impact_score': 8.5
                },
                {
                    'title': '平安银行股价创新高',
                    'content': '受利好消息影响...',
                    'publish_time': '2024-12-07 09:30:00',
                    'source': '证券时报',
                    'sentiment': 'positive',
                    'impact_score': 7.2
                }
            ]

            # 调用函数
            display_news_analysis(stock_identity)

            # 验证新闻获取
            mock_news.assert_called_once_with('000001', limit=20)

    @pytest.mark.unit
    def test_display_with_empty_news(self, mock_streamlit):
        """测试空新闻列表"""
        stock_identity = {
            'code': '000001',
            'name': '平安银行',
            'market_name': 'A股'
        }

        with patch('stock.stock_data_fetcher.get_stock_news', return_value=[]):
            # 调用函数
            display_news_analysis(stock_identity)

            # 应该显示提示信息
            mock_streamlit['info'].assert_called()


class TestDisplayChipsAnalysis:
    """测试筹码分析（仅A股）"""

    @pytest.mark.unit
    def test_display_a_stock_chips(self, mock_streamlit):
        """测试A股筹码分析"""
        stock_identity = {
            'code': '000001',
            'name': '平安银行',
            'market_name': 'A股'
        }

        # Mock 筹码数据
        with patch('stock.stock_data_fetcher.get_stock_chips_analysis') as mock_chips:
            mock_chips.return_value = {
                'concentration_ratio': 65.2,
                'main_holdings': 45.8,
                'institution_holdings': 32.5,
                'retail_holdings': 21.7,
                'chip_distribution': {
                    'low_cost': 30.5,
                    'medium_cost': 45.2,
                    'high_cost': 24.3
                },
                'change_10days': 2.5,
                'change_30days': 5.8
            }

            # 调用函数
            display_chips_analysis(stock_identity)

            # 验证数据获取
            mock_chips.assert_called_once_with('000001')

    @pytest.mark.unit
    def test_skip_non_a_stock(self):
        """测试跳过非A股的筹码分析"""
        stock_identity = {
            'code': '00700',
            'name': '腾讯控股',
            'market_name': '港股'
        }

        # 调用函数
        # 对于港股，应该跳过筹码分析
        result = display_chips_analysis(stock_identity)
        assert result is None

    @pytest.mark.unit
    def test_skip_etf(self):
        """测试跳过ETF的筹码分析"""
        stock_identity = {
            'code': '510300',
            'name': '沪深300ETF',
            'market_name': 'ETF'
        }

        # 调用函数
        result = display_chips_analysis(stock_identity)
        assert result is None


class TestDisplayCompanyAnalysis:
    """测试公司分析（仅A股）"""

    @pytest.mark.unit
    def test_display_a_stock_company(self, mock_streamlit):
        """测试A股公司分析"""
        stock_identity = {
            'code': '000001',
            'name': '平安银行',
            'market_name': 'A股'
        }

        # Mock 公司数据
        with patch('stock.stock_data_fetcher.get_stock_company_info') as mock_company:
            mock_company.return_value = {
                'company_name': '平安银行股份有限公司',
                'industry': '银行',
                'established_date': '1987-12-22',
                'listed_date': '1991-04-03',
                'registered_capital': 19405918198,
                'main_business': '商业银行业务',
                'scope': '吸收公众存款、发放贷款等',
                'profile': '中国领先的商业银行之一'
            }

            # 调用函数
            display_company_analysis(stock_identity)

            # 验证数据获取
            mock_company.assert_called_once_with('000001')

    @pytest.mark.unit
    def test_skip_non_a_stock_company(self):
        """测试跳过非A股的公司分析"""
        stock_identity = {
            'code': '00700',
            'name': '腾讯控股',
            'market_name': '港股'
        }

        # 调用函数
        result = display_company_analysis(stock_identity)
        assert result is None


class TestDisplayComprehensiveAnalysis:
    """测试综合分析"""

    @pytest.mark.unit
    def test_display_ai_comprehensive(self, mock_streamlit, mock_session_state):
        """测试AI综合分析"""
        stock_identity = {
            'code': '000001',
            'name': '平安银行',
            'market_name': 'A股'
        }

        # Mock AI综合报告
        mock_session_state.get.side_effect = lambda key, default=None: {
            'ai_comprehensive_report': {
                'success': True,
                'report': '## 综合分析报告\n\n该股票基本面稳健，技术面向好...'
            }
        }.get(key, default)

        # 调用函数
        display_comprehensive_analysis(stock_identity)

        # 验证报告显示
        assert mock_streamlit['info'].called or mock_streamlit['markdown'].called

    @pytest.mark.unit
    def test_display_without_ai_report(self, mock_streamlit, mock_session_state):
        """测试没有AI综合报告"""
        stock_identity = {
            'code': '000001',
            'name': '平安银行',
            'market_name': 'A股'
        }

        # Mock 没有AI报告
        mock_session_state.get.return_value = None

        # 调用函数
        display_comprehensive_analysis(stock_identity)

        # 应该显示提示
        mock_streamlit['info'].assert_called()


@pytest.mark.parametrize("market_name", ["A股", "港股", "ETF"])
def test_market_type_handling(market_name, mock_streamlit):
    """参数化测试不同市场类型的处理"""
    stock_identity = {
        'code': '000001',
        'name': '测试股票',
        'market_name': market_name
    }

    with patch('stock.stock_data_fetcher.get_stock_basic_info', return_value={}):
        # 调用主函数
        display_stock_info(stock_identity)

        # 验证函数正常执行
        assert True


@pytest.mark.parametrize("section", [
    "fundamental", "technical", "news", "chips", "company", "comprehensive"
])
def test_analysis_sections(section, mock_streamlit, mock_session_state):
    """参数化测试各个分析部分"""
    stock_identity = {
        'code': '000001',
        'name': '平安银行',
        'market_name': 'A股'
    }

    # 设置Session State
    mock_session_state.get.return_value = True

    # 根据部分选择函数
    functions = {
        'fundamental': display_fundamental_analysis,
        'technical': display_technical_analysis,
        'news': display_news_analysis,
        'chips': display_chips_analysis,
        'company': display_company_analysis,
        'comprehensive': display_comprehensive_analysis
    }

    with patch('stock.stock_data_fetcher.get_stock_basic_info', return_value={}):
        # 调用对应函数
        functions[section](stock_identity)
        assert True