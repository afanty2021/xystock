# XY Stock 测试指南

> 更新时间：2025-12-07 22:59:00

## 概述

本目录包含了 XY Stock 项目的完整测试套件，包括单元测试、集成测试和端到端测试。测试覆盖率目标为 **80%**，确保代码质量和系统稳定性。

## 📁 目录结构

```
tests/
├── README.md                    # 本文件
├── requirements.txt             # 测试依赖
├── conftest.py                  # pytest配置和fixtures
├── run_tests.py                 # 测试运行脚本
├── fixtures/                    # 测试数据和工具
│   └── data_generator.py        # 测试数据生成器
├── unit/                        # 单元测试
│   └── ui/                      # UI组件单元测试
│       ├── test_page_common.py
│       ├── test_page_stock.py
│       ├── test_page_market_overview.py
│       ├── test_page_settings.py
│       └── test_page_export.py
├── integration/                 # 集成测试（待补充）
└── e2e/                        # 端到端测试（待补充）
```

## 🚀 快速开始

### 1. 安装测试依赖

```bash
pip install -r tests/requirements.txt
```

### 2. 运行所有测试

```bash
# 使用测试脚本（推荐）
python tests/run_tests.py --all

# 或直接使用pytest
pytest tests/
```

### 3. 查看测试覆盖率

```bash
# 生成覆盖率报告
python tests/run_tests.py --all --coverage --html

# 查看HTML报告
open htmlcov/index.html
```

## 📋 测试类型说明

### 单元测试 (Unit Tests)
- **位置**: `tests/unit/`
- **标记**: `@pytest.mark.unit`
- **特点**: 快速、独立、不依赖外部资源
- **覆盖范围**:
  - UI组件函数
  - 数据处理逻辑
  - 配置管理
  - 工具函数

### 集成测试 (Integration Tests)
- **位置**: `tests/integration/`
- **标记**: `@pytest.mark.integration`
- **特点**: 测试模块间协作
- **待补充内容**:
  - 数据流测试
  - API集成测试
  - 模块间接口测试

### 端到端测试 (E2E Tests)
- **位置**: `tests/e2e/`
- **标记**: `@pytest.mark.e2e`
- **特点**: 完整工作流测试
- **待补充内容**:
  - UI交互流程
  - 报告生成流程
  - 完整业务场景

## 🛠️ 测试命令

### 使用测试脚本

```bash
# 运行单元测试
python tests/run_tests.py --unit

# 运行集成测试
python tests/run_tests.py --integration

# 运行端到端测试
python tests/run_tests.py --e2e

# 运行所有测试
python tests/run_tests.py --all

# 生成覆盖率报告
python tests/run_tests.py --all --coverage

# 生成HTML覆盖率报告
python tests/run_tests.py --all --coverage --html

# 检查覆盖率是否达标（80%）
python tests/run_tests.py --check-coverage

# 详细输出
python tests/run_tests.py --all --verbose

# 包含慢速测试
python tests/run_tests.py --all --slow

# 生成测试数据
python tests/run_tests.py --generate-data
```

### 直接使用pytest

```bash
# 运行所有测试
pytest tests/

# 运行特定目录
pytest tests/unit/

# 运行特定文件
pytest tests/unit/ui/test_page_common.py

# 运行特定测试函数
pytest tests/unit/ui/test_page_common.py::TestDisplayTechnicalIndicators::test_display_with_valid_data

# 生成覆盖率报告
pytest --cov=ui --cov-report=html

# 并行运行
pytest -n auto

# 只运行失败的测试
pytest --lf

# 运行标记的测试
pytest -m "unit"  # 只运行单元测试
pytest -m "slow"  # 只运行慢速测试
```

## 📊 覆盖率目标

### 当前状态
- **单元测试覆盖率**: 目标 80%
- **集成测试覆盖率**: 目标 60%
- **关键路径覆盖率**: 100%

### 覆盖率配置

在 `pytest.ini` 中配置：
```ini
[coverage:run]
source = ui stock market llm utils
omit = */tests/* */test_* */__pycache__/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    raise AssertionError
    raise NotImplementedError
```

## 🎯 编写新测试

### 1. 单元测试模板

```python
#!/usr/bin/env python3
"""
测试 [模块名]
"""
import pytest
from unittest.mock import Mock, patch

class TestClassName:
    """测试类说明"""

    @pytest.mark.unit
    def test_method_name(self, mock_streamlit):
        """测试方法说明"""
        # Arrange - 准备测试数据
        test_data = {...}

        # Act - 执行测试
        result = function_under_test(test_data)

        # Assert - 验证结果
        assert result is not None
```

### 2. 使用Fixtures

```python
def test_function_with_fixture(sample_stock_data):
    """使用fixture的测试"""
    # 直接使用预定义的测试数据
    assert sample_stock_data is not None
    assert 'current_price' in sample_stock_data
```

### 3. Mock外部依赖

```python
@patch('module.external_function')
def test_with_mock(mock_external):
    """使用mock的测试"""
    mock_external.return_value = "mocked_value"
    result = function_using_external()
    mock_external.assert_called_once()
```

### 4. 参数化测试

```python
@pytest.mark.parametrize("input,expected", [
    ("A", 1),
    ("B", 2),
    ("C", 3)
])
def test_parametrized(input, expected):
    """参数化测试"""
    assert process_input(input) == expected
```

## 🔧 测试最佳实践

### 1. 测试命名
- 使用描述性的测试名
- 格式：`test_[功能]_[场景]_[期望结果]`
- 示例：`test_display_stock_info_with_valid_data`

### 2. AAA模式
```python
def test_example():
    # Arrange - 准备
    data = prepare_test_data()

    # Act - 执行
    result = function_under_test(data)

    # Assert - 验证
    assert result.success is True
```

### 3. 测试隔离
- 每个测试独立运行
- 不依赖测试执行顺序
- 使用fixture管理共享状态

### 4. Mock使用原则
- 只mock外部依赖
- 不mock被测试的代码
- 验证mock的调用

### 5. 断言清晰
- 使用有意义的断言
- 提供失败时的错误信息
- 每个测试一个主要断言

## 📈 持续集成

### GitHub Actions配置示例

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r tests/requirements.txt

    - name: Run tests
      run: |
        python tests/run_tests.py --all --coverage

    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## 🐛 常见问题

### Q: 测试运行很慢？
A:
- 使用 `pytest -m "not slow"` 跳过慢速测试
- 使用并行运行 `pytest -n auto`
- 检查是否有不必要的I/O操作

### Q: Mock不生效？
A:
- 确保mock路径正确
- 检查import顺序
- 使用 `patch.object` 对象方法

### Q: 覆盖率不准确？
A:
- 排除不需要测试的文件
- 检查 `exclude_lines` 配置
- 使用 `--cov-fail-under` 强制覆盖率

### Q: Session State相关问题？
A:
- 使用 `mock_session_state` fixture
- 确保key-value对的正确性
- 测试不同状态组合

## 📝 添加新测试

当添加新功能时，请同时添加对应的测试：

1. **单元测试**: 在 `tests/unit/` 对应目录下
2. **集成测试**: 如需要，在 `tests/integration/` 下添加
3. **更新Fixtures**: 如需新的测试数据，更新 `conftest.py`
4. **更新文档**: 在测试文件中添加清晰的文档字符串

## 🎉 贡献指南

1. 新增功能必须包含测试
2. 测试覆盖率不应降低
3. 遵循现有的测试命名和结构规范
4. 确保所有测试通过后提交PR

---

## 📞 获取帮助

- 查看pytest官方文档: https://docs.pytest.org/
- 查看pytest-cov文档: https://pytest-cov.readthedocs.io/
- 项目Issues: 提交问题或建议

---

*良好的测试是代码质量的保障，让我们一起努力提高测试覆盖率！*