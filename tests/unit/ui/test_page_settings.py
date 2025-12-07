#!/usr/bin/env python3
"""
测试系统设置页面 page_settings.py
"""
import pytest
import configparser
import tempfile
import os
from unittest.mock import Mock, patch, mock_open
import streamlit as st
import sys

# 添加项目路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.join(project_root, 'ui', 'components'))

try:
    from page_settings import save_config, main
except ImportError as e:
    pytest.skip(f"无法导入 page_settings: {e}", allow_module_level=True)


class TestSaveConfig:
    """测试配置保存函数"""

    @pytest.mark.unit
    def test_save_new_config(self):
        """测试保存新配置"""
        # 使用临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as f:
            temp_path = f.name

        try:
            # Mock 文件操作
            with patch('builtins.open', mock_open()), \
                 patch('configparser.ConfigParser') as mock_config:

                mock_parser = Mock()
                mock_config.return_value = mock_parser
                mock_parser.read.return_value = []

                # 调用函数
                result = save_config('LLM_OPENAI', 'API_KEY', 'test-key-123')

                # 验证调用
                mock_parser.__setitem__.assert_called_with('LLM_OPENAI', {})
                mock_parser.set.assert_called_with('LLM_OPENAI', 'API_KEY', 'test-key-123')
                mock_parser.write.assert_called_once()

                # 验证返回值
                assert result is True

        finally:
            # 清理临时文件
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    @pytest.mark.unit
    def test_save_existing_config(self):
        """测试保存到已有配置"""
        # Mock 已存在的配置
        with patch('configparser.ConfigParser') as mock_config:
            mock_parser = Mock()
            mock_config.return_value = mock_parser
            mock_parser.read.return_value = ['config.ini']  # 已有配置文件

            # 调用函数
            result = save_config('LLM_OPENAI', 'TEMPERATURE', 0.7)

            # 验证调用
            mock_parser.set.assert_called_with('LLM_OPENAI', 'TEMPERATURE', '0.7')
            mock_parser.write.assert_called_once()

            # 验证返回值
            assert result is True

    @pytest.mark.unit
    def test_save_config_with_exception(self):
        """测试保存配置时的异常处理"""
        # Mock 抛出异常
        with patch('configparser.ConfigParser') as mock_config:
            mock_parser = Mock()
            mock_config.return_value = mock_parser
            mock_parser.write.side_effect = Exception("写入失败")

            # 调用函数
            result = save_config('LLM_OPENAI', 'API_KEY', 'test-key')

            # 验证返回值
            assert result is False

    @pytest.mark.unit
    @pytest.mark.parametrize("section,key,value,expected_type", [
        ('LLM_OPENAI', 'API_KEY', 'sk-12345', str),
        ('LLM_OPENAI', 'TIMEOUT', 30, str),
        ('LLM_OPENAI', 'DEFAULT_TEMPERATURE', 0.7, str),
        ('LLM_CACHE', 'ENABLE_CACHE', True, str),
        ('ANALYSIS', 'RISK_PREFERENCE', 'aggressive', str),
    ])
    def test_save_different_value_types(self, section, key, value, expected_type):
        """测试保存不同类型的值"""
        with patch('configparser.ConfigParser') as mock_config:
            mock_parser = Mock()
            mock_config.return_value = mock_parser
            mock_parser.read.return_value = []

            # 调用函数
            save_config(section, key, value)

            # 验证值被转换为字符串
            call_args = mock_parser.set.call_args
            assert call_args[0][2] == str(value)


class TestMainFunction:
    """测试主函数"""

    @pytest.mark.unit
    def test_main_page_render(self, mock_streamlit, mock_session_state):
        """测试主页面渲染"""
        # Mock 配置读取
        with patch('page_settings.load_config') as mock_load:
            mock_load.return_value = {
                'LLM_OPENAI': {
                    'API_KEY': 'sk-12345',
                    'DEFAULT_MODEL': 'gpt-3.5-turbo',
                    'TIMEOUT': 30,
                    'DEFAULT_TEMPERATURE': 0.7
                },
                'LLM_CACHE': {
                    'ENABLE_CACHE': True,
                    'CACHE_TTL': 3600
                },
                'ANALYSIS': {
                    'RISK_PREFERENCE': 'neutral'
                },
                'USER_PROFILE': {
                    'RAW': '测试用户',
                    'MISTAKES': ['追涨杀跌']
                }
            }

            # 调用主函数
            main()

            # 验证页面元素
            assert mock_streamlit['header'].called
            assert mock_streamlit['text_input'].call_count >= 2  # API Key, Base URL
            assert mock_streamlit['number_input'].call_count >= 2  # Timeout, Retries
            assert mock_streamlit['slider'].called  # Temperature
            assert mock_streamlit['toggle'].called  # Cache toggle

    @pytest.mark.unit
    def test_api_configuration_section(self, mock_streamlit, mock_session_state):
        """测试API配置部分"""
        with patch('page_settings.load_config') as mock_load:
            mock_load.return_value = {
                'LLM_OPENAI': {
                    'API_KEY': '',
                    'BASE_URL': 'https://api.openai.com/v1',
                    'DEFAULT_MODEL': 'gpt-3.5-turbo',
                    'INFERENCE_MODEL': 'gpt-3.5-turbo',
                    'TIMEOUT': 30,
                    'MAX_RETRIES': 3,
                    'DEFAULT_TEMPERATURE': 0.7
                }
            }

            # 调用主函数
            main()

            # 验证API配置输入框
            input_calls = mock_streamlit['text_input'].call_args_list
            api_key_input = any('API' in str(call) for call in input_calls)
            assert api_key_input

    @pytest.mark.unit
    def test_cache_configuration_section(self, mock_streamlit, mock_session_state):
        """测试缓存配置部分"""
        with patch('page_settings.load_config') as mock_load:
            mock_load.return_value = {
                'LLM_CACHE': {
                    'ENABLE_CACHE': True,
                    'CACHE_TTL': 3600
                }
            }

            # 调用主函数
            main()

            # 验证缓存配置
            mock_streamlit['toggle'].assert_called()
            mock_streamlit['number_input'].assert_called()

    @pytest.mark.unit
    def test_analysis_configuration_section(self, mock_streamlit, mock_session_state):
        """测试分析配置部分"""
        with patch('page_settings.load_config') as mock_load:
            mock_load.return_value = {
                'ANALYSIS': {
                    'RISK_PREFERENCE': 'neutral',
                    'CUSTOM_PRINCIPLES': '长期价值投资'
                }
            }

            # 调用主函数
            main()

            # 验证风险偏好选择
            mock_streamlit['selectbox'].assert_called()
            mock_streamlit['text_area'].assert_called()

    @pytest.mark.unit
    def test_user_profile_section(self, mock_streamlit, mock_session_state):
        """测试用户画像部分"""
        with patch('page_settings.load_config') as mock_load:
            mock_load.return_value = {
                'USER_PROFILE': {
                    'RAW': '保守型投资者',
                    'MISTAKES': ['追涨杀跌', '频繁交易', '情绪化']
                }
            }

            # 调用主函数
            main()

            # 验证用户画像输入
            mock_streamlit['text_area'].assert_called()
            mock_streamlit['multiselect'].assert_called()

    @pytest.mark.unit
    def test_save_button_functionality(self, mock_streamlit, mock_session_state):
        """测试保存按钮功能"""
        with patch('page_settings.load_config') as mock_load, \
             patch('page_settings.save_config') as mock_save:

            mock_load.return_value = {}
            mock_save.return_value = True

            # Mock 按钮点击
            mock_streamlit['button'].return_value = True

            # 调用主函数
            main()

            # 验证保存函数被调用
            assert mock_save.called

    @pytest.mark.unit
    def test_test_connection_button(self, mock_streamlit, mock_session_state):
        """测试连接测试按钮"""
        with patch('page_settings.load_config') as mock_load, \
             patch('llm.llm_client.test_connection') as mock_test:

            mock_load.return_value = {
                'LLM_OPENAI': {
                    'API_KEY': 'test-key',
                    'BASE_URL': 'https://api.openai.com/v1'
                }
            }
            mock_test.return_value = True

            # Mock 按钮点击
            mock_streamlit['button'].side_effect = [False, True]  # 第一个按钮不点，第二个按钮点击

            # 调用主函数
            main()

            # 验证测试连接被调用
            mock_test.assert_called()

    @pytest.mark.unit
    def test_reset_button_functionality(self, mock_streamlit, mock_session_state):
        """测试重置按钮功能"""
        with patch('page_settings.load_config') as mock_load, \
             patch('page_settings.reset_config_to_default') as mock_reset:

            mock_load.return_value = {}

            # Mock 重置按钮点击
            mock_streamlit['button'].side_effect = [False, False, True]  # 第三个按钮（重置）点击

            # 调用主函数
            main()

            # 验证重置函数被调用
            mock_reset.assert_called()


@pytest.mark.parametrize("config_section", [
    'LLM_OPENAI',
    'LLM_CACHE',
    'ANALYSIS',
    'USER_PROFILE'
])
def test_config_sections_render(config_section, mock_streamlit):
    """参数化测试各个配置部分的渲染"""
    with patch('page_settings.load_config') as mock_load:
        mock_load.return_value = {
            config_section: {
                'TEST_KEY': 'TEST_VALUE'
            }
        }

        # 调用主函数
        main()

        # 验证页面正常渲染
        assert True


@pytest.mark.parametrize("risk_preference", [
    'conservative',
    'neutral',
    'aggressive',
    'custom'
])
def test_risk_preference_options(risk_preference, mock_streamlit):
    """参数化测试风险偏好选项"""
    with patch('page_settings.load_config') as mock_load:
        mock_load.return_value = {
            'ANALYSIS': {
                'RISK_PREFERENCE': risk_preference
            }
        }

        # 调用主函数
        main()

        # 验证选项设置
        select_calls = mock_streamlit['selectbox'].call_args_list
        risk_select = any('RISK' in str(call) or '风险' in str(call) for call in select_calls)
        assert risk_select


class TestEdgeCases:
    """边界情况测试"""

    @pytest.mark.unit
    def test_empty_config_load(self, mock_streamlit):
        """测试加载空配置"""
        with patch('page_settings.load_config') as mock_load:
            mock_load.return_value = {}

            # 调用主函数
            main()

            # 应该正常渲染，使用默认值
            assert mock_streamlit['header'].called

    @pytest.mark.unit
    def test_missing_config_file(self, mock_streamlit):
        """测试配置文件不存在"""
        with patch('page_settings.load_config') as mock_load:
            mock_load.side_effect = FileNotFoundError("配置文件不存在")

            # 调用主函数
            main()

            # 应该显示错误信息
            mock_streamlit['error'].assert_called()

    @pytest.mark.unit
    def test_invalid_config_format(self, mock_streamlit):
        """测试无效的配置格式"""
        with patch('page_settings.load_config') as mock_load:
            mock_load.side_effect = configparser.Error("配置格式错误")

            # 调用主函数
            main()

            # 应该显示错误信息
            mock_streamlit['error'].assert_called()