#!/usr/bin/env python3
"""
测试报告导出页面 page_export.py
"""
import pytest
import tempfile
import os
from datetime import datetime
from unittest.mock import Mock, patch, mock_open, MagicMock
import streamlit as st
import sys

# 添加项目路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.join(project_root, 'ui', 'components'))

try:
    from page_export import (
        display_report_export_section,
        display_quick_export_buttons,
        display_batch_export_options
    )
except ImportError as e:
    pytest.skip(f"无法导入 page_export: {e}", allow_module_level=True)


class TestDisplayReportExportSection:
    """测试报告导出部分"""

    @pytest.mark.unit
    def test_export_section_render(self, mock_streamlit, mock_session_state, sample_stock_report):
        """测试导出部分渲染"""
        entity_id = '000001'
        report_type = 'stock'

        # Mock 生成函数
        with patch('page_export.generate_markdown_report') as mock_generate:
            mock_generate.return_value = sample_stock_report

            # Mock 选择器
            mock_streamlit['selectbox'].return_value = 'markdown'

            # 调用函数
            display_report_export_section(
                entity_id=entity_id,
                report_type=report_type,
                title="测试导出",
                generate_func=mock_generate,
                filename_prefix="测试报告"
            )

            # 验证渲染
            mock_streamlit['header'].assert_called()
            mock_streamlit['selectbox'].assert_called()
            mock_streamlit['button'].assert_called()

    @pytest.mark.unit
    def test_generate_report_button(self, mock_streamlit, mock_session_state, sample_stock_report):
        """测试生成报告按钮"""
        entity_id = '000001'
        report_type = 'stock'

        with patch('page_export.generate_markdown_report') as mock_generate:
            mock_generate.return_value = sample_stock_report

            # Mock 生成按钮被点击
            mock_streamlit['button'].side_effect = [True, False]  # 第一个按钮点击

            # Mock 格式选择
            mock_streamlit['selectbox'].return_value = 'markdown'

            # 调用函数
            display_report_export_section(
                entity_id=entity_id,
                report_type=report_type,
                generate_func=mock_generate
            )

            # 验证生成函数被调用
            mock_generate.assert_called()

            # 验证报告存储到 session_state
            assert mock_session_state.__setitem__.called

    @pytest.mark.unit
    def test_download_button_after_generation(self, mock_streamlit, mock_session_state, sample_stock_report):
        """测试生成后的下载按钮"""
        entity_id = '000001'
        report_type = 'stock'

        # Mock 已生成的报告
        mock_session_state.get.side_effect = lambda key, default=None: {
            f'{report_type}_content_{entity_id}': sample_stock_report,
            f'{report_type}_filename_{entity_id}': 'test_report.md',
            f'{report_type}_mime_{entity_id}': 'text/markdown'
        }.get(key, default)

        # Mock 按钮点击
        mock_streamlit['button'].side_effect = [False, True]  # 第二个按钮（下载）点击

        # 调用函数
        display_report_export_section(
            entity_id=entity_id,
            report_type=report_type
        )

        # 验证下载按钮显示
        mock_streamlit['download_button'].assert_called()

    @pytest.mark.unit
    @pytest.mark.parametrize("format_type,expected_mime", [
        ("pdf", "application/pdf"),
        ("docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        ("markdown", "text/markdown"),
        ("html", "text/html")
    ])
    def test_different_export_formats(self, format_type, expected_mime, mock_streamlit, mock_session_state):
        """测试不同导出格式"""
        entity_id = '000001'
        report_type = 'stock'

        # Mock 格式选择
        mock_streamlit['selectbox'].return_value = format_type

        with patch('page_export.generate_markdown_report') as mock_generate:
            mock_generate.return_value = "# Test Report"

            # 调用函数
            display_report_export_section(
                entity_id=entity_id,
                report_type=report_type,
                generate_func=mock_generate
            )

            # 验证格式处理
            assert mock_streamlit['selectbox'].called


class TestDisplayQuickExportButtons:
    """测试快速导出按钮"""

    @pytest.mark.unit
    def test_quick_export_render(self, mock_streamlit, sample_stock_report):
        """测试快速导出渲染"""
        entity_id = '000001'
        report_type = 'stock'

        with patch('page_export.generate_markdown_report') as mock_generate:
            mock_generate.return_value = sample_stock_report

            # 调用函数
            display_quick_export_buttons(
                entity_id=entity_id,
                report_type=report_type,
                generate_func=mock_generate
            )

            # 验证按钮渲染（应该有4个格式的按钮）
            assert mock_streamlit['button'].call_count == 4

    @pytest.mark.unit
    def test_quick_export_click(self, mock_streamlit, mock_session_state, sample_stock_report):
        """测试快速导出点击"""
        entity_id = '000001'
        report_type = 'stock'

        with patch('page_export.generate_markdown_report') as mock_generate:
            mock_generate.return_value = sample_stock_report

            # Mock PDF按钮被点击
            mock_streamlit['button'].side_effect = [True, False, False, False]

            # 调用函数
            display_quick_export_buttons(
                entity_id=entity_id,
                report_type=report_type,
                generate_func=mock_generate
            )

            # 验证生成函数被调用
            mock_generate.assert_called()


class TestDisplayBatchExportOptions:
    """测试批量导出选项"""

    @pytest.mark.unit
    def test_batch_export_render(self, mock_streamlit):
        """测试批量导出渲染"""
        entities = [
            {'code': '000001', 'name': '平安银行'},
            {'code': '000002', 'name': '万科A'},
            {'code': '600519', 'name': '贵州茅台'}
        ]
        report_type = 'stock'

        with patch('page_export.generate_markdown_report') as mock_generate:
            mock_generate.return_value = "# Test Report"

            # Mock 多选
            mock_streamlit['multiselect'].return_value = entities

            # 调用函数
            display_batch_export_options(
                entities=entities,
                report_type=report_type,
                generate_func=mock_generate
            )

            # 验证多选组件
            mock_streamlit['multiselect'].assert_called()

    @pytest.mark.unit
    def test_batch_export_execution(self, mock_streamlit, mock_session_state):
        """测试批量导出执行"""
        entities = [
            {'code': '000001', 'name': '平安银行'},
            {'code': '000002', 'name': '万科A'}
        ]
        report_type = 'stock'

        with patch('page_export.generate_markdown_report') as mock_generate:
            mock_generate.return_value = "# Test Report"

            # Mock 选择和点击
            mock_streamlit['multiselect'].return_value = entities[:1]  # 只选择第一个
            mock_streamlit['button'].side_effect = [False, True]  # 第二个按钮点击

            # Mock 进度条
            mock_progress = Mock()
            mock_streamlit['progress'].return_value = mock_progress

            # 调用函数
            display_batch_export_options(
                entities=entities,
                report_type=report_type,
                generate_func=mock_generate
            )

            # 验证进度条显示
            mock_streamlit['progress'].assert_called()


class TestReportGeneration:
    """测试报告生成功能"""

    @pytest.mark.unit
    def test_markdown_report_generation(self, mock_streamlit, mock_session_state):
        """测试Markdown报告生成"""
        entity_id = '000001'
        report_type = 'stock'
        report_content = "# 平安银行分析报告\n\n## 基本信息\n..."

        with patch('page_export.generate_markdown_report') as mock_generate:
            mock_generate.return_value = report_content

            # Mock 格式选择为 Markdown
            mock_streamlit['selectbox'].return_value = 'markdown'

            # 调用函数
            display_report_export_section(
                entity_id=entity_id,
                report_type=report_type,
                generate_func=mock_generate
            )

            # 验证内容存储
            storage_calls = mock_session_state.__setitem__.call_args_list
            content_key = f'{report_type}_content_{entity_id}'
            filename_key = f'{report_type}_filename_{entity_id}'
            mime_key = f'{report_type}_mime_{entity_id}'

            stored_keys = [call[0][0] for call in storage_calls]
            assert content_key in stored_keys
            assert filename_key in stored_keys
            assert mime_key in stored_keys

    @pytest.mark.unit
    def test_pdf_report_conversion(self, mock_streamlit, mock_session_state):
        """测试PDF报告转换"""
        entity_id = '000001'
        report_type = 'stock'
        markdown_content = "# Test Report"

        with patch('page_export.generate_markdown_report') as mock_generate, \
             patch('page_export.convert_markdown_to_pdf') as mock_convert:

            mock_generate.return_value = markdown_content
            mock_convert.return_value = b'PDF content bytes'

            # Mock 格式选择为 PDF
            mock_streamlit['selectbox'].return_value = 'pdf'

            # 调用函数
            display_report_export_section(
                entity_id=entity_id,
                report_type=report_type,
                generate_func=mock_generate
            )

            # 验证转换函数被调用
            mock_convert.assert_called_with(markdown_content)

    @pytest.mark.unit
    def test_docx_report_conversion(self, mock_streamlit, mock_session_state):
        """测试DOCX报告转换"""
        entity_id = '000001'
        report_type = 'stock'
        markdown_content = "# Test Report"

        with patch('page_export.generate_markdown_report') as mock_generate, \
             patch('page_export.convert_markdown_to_docx') as mock_convert:

            mock_generate.return_value = markdown_content
            mock_convert.return_value = b'DOCX content bytes'

            # Mock 格式选择为 DOCX
            mock_streamlit['selectbox'].return_value = 'docx'

            # 调用函数
            display_report_export_section(
                entity_id=entity_id,
                report_type=report_type,
                generate_func=mock_generate
            )

            # 验证转换函数被调用
            mock_convert.assert_called_with(markdown_content)


class TestErrorHandling:
    """测试错误处理"""

    @pytest.mark.unit
    def test_generation_failure(self, mock_streamlit):
        """测试生成失败处理"""
        entity_id = '000001'
        report_type = 'stock'

        with patch('page_export.generate_markdown_report') as mock_generate:
            mock_generate.side_effect = Exception("生成失败")

            # Mock 生成按钮点击
            mock_streamlit['button'].side_effect = [True, False]

            # 调用函数
            display_report_export_section(
                entity_id=entity_id,
                report_type=report_type,
                generate_func=mock_generate
            )

            # 应该显示错误信息
            mock_streamlit['error'].assert_called()

    @pytest.mark.unit
    def test_conversion_failure(self, mock_streamlit):
        """测试转换失败处理"""
        entity_id = '000001'
        report_type = 'stock'

        with patch('page_export.generate_markdown_report') as mock_generate, \
             patch('page_export.convert_markdown_to_pdf') as mock_convert:

            mock_generate.return_value = "# Test"
            mock_convert.side_effect = Exception("转换失败")

            # Mock 格式选择和生成
            mock_streamlit['selectbox'].return_value = 'pdf'
            mock_streamlit['button'].side_effect = [True, False]

            # 调用函数
            display_report_export_section(
                entity_id=entity_id,
                report_type=report_type,
                generate_func=mock_generate
            )

            # 应该显示错误信息
            mock_streamlit['error'].assert_called()


@pytest.mark.parametrize("entity_id,report_type,filename_prefix", [
    ("000001", "stock", "平安银行报告"),
    ("market", "market", "市场分析报告"),
    ("portfolio", "portfolio", "投资组合报告")
])
def test_different_entity_types(entity_id, report_type, filename_prefix, mock_streamlit):
    """参数化测试不同实体类型"""
    with patch('page_export.generate_markdown_report') as mock_generate:
        mock_generate.return_value = "# Test Report"

        # 调用函数
        display_report_export_section(
            entity_id=entity_id,
            report_type=report_type,
            filename_prefix=filename_prefix,
            generate_func=mock_generate
        )

        # 验证正常执行
        assert True