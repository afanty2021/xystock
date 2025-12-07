#!/usr/bin/env python3
"""
测试运行脚本
提供便捷的测试执行和覆盖率报告生成
"""
import os
import sys
import subprocess
import argparse
import time
from pathlib import Path


# 获取项目根目录
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    print(f"执行命令: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        cwd=cwd or project_root,
        capture_output=True,
        text=True
    )
    return result


def run_unit_tests(verbose=False, coverage=False, html_report=False):
    """运行单元测试"""
    print("\n" + "="*50)
    print("🧪 运行单元测试")
    print("="*50)

    cmd = ["python", "-m", "pytest", "tests/unit/", "-m", "not slow"]

    if verbose:
        cmd.append("-v")

    if coverage:
        cmd.extend([
            "--cov=ui",
            "--cov=stock",
            "--cov=market",
            "--cov=llm",
            "--cov=utils",
            "--cov-report=term-missing"
        ])

        if html_report:
            cmd.append("--cov-report=html:htmlcov")

    result = run_command(cmd)

    if result.returncode == 0:
        print("\n✅ 单元测试通过")
    else:
        print("\n❌ 单元测试失败")
        print(result.stdout)
        print(result.stderr)

    return result.returncode == 0


def run_integration_tests(verbose=False):
    """运行集成测试"""
    print("\n" + "="*50)
    print("🔗 运行集成测试")
    print("="*50)

    cmd = ["python", "-m", "pytest", "tests/integration/", "-m", "not slow"]

    if verbose:
        cmd.append("-v")

    result = run_command(cmd)

    if result.returncode == 0:
        print("\n✅ 集成测试通过")
    else:
        print("\n❌ 集成测试失败")
        print(result.stdout)
        print(result.stderr)

    return result.returncode == 0


def run_e2e_tests(verbose=False):
    """运行端到端测试"""
    print("\n" + "="*50)
    print("🌐 运行端到端测试")
    print("="*50)

    cmd = ["python", "-m", "pytest", "tests/e2e/", "-m", "not slow"]

    if verbose:
        cmd.append("-v")

    result = run_command(cmd)

    if result.returncode == 0:
        print("\n✅ 端到端测试通过")
    else:
        print("\n❌ 端到端测试失败")
        print(result.stdout)
        print(result.stderr)

    return result.returncode == 0


def run_slow_tests(verbose=False):
    """运行慢速测试（需要网络或数据库）"""
    print("\n" + "="*50)
    print("🐌 运行慢速测试")
    print("="*50)

    cmd = ["python", "-m", "pytest", "-m", "slow"]

    if verbose:
        cmd.append("-v")

    result = run_command(cmd)

    if result.returncode == 0:
        print("\n✅ 慢速测试通过")
    else:
        print("\n❌ 慢速测试失败")
        print(result.stdout)
        print(result.stderr)

    return result.returncode == 0


def run_all_tests(verbose=False, coverage=False, html_report=False, include_slow=False):
    """运行所有测试"""
    print("\n🎯 开始运行所有测试...")

    start_time = time.time()
    results = []

    # 单元测试
    results.append(("单元测试", run_unit_tests(verbose, coverage, html_report)))

    # 集成测试
    results.append(("集成测试", run_integration_tests(verbose)))

    # 端到端测试
    results.append(("端到端测试", run_e2e_tests(verbose)))

    # 慢速测试（可选）
    if include_slow:
        results.append(("慢速测试", run_slow_tests(verbose)))

    # 统计结果
    end_time = time.time()
    duration = end_time - start_time

    print("\n" + "="*50)
    print("📊 测试结果汇总")
    print("="*50)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_type, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_type}: {status}")

    print(f"\n总计: {passed}/{total} 测试组通过")
    print(f"耗时: {duration:.2f} 秒")

    # 生成覆盖率报告
    if coverage and html_report:
        print(f"\n📈 HTML覆盖率报告已生成: {project_root}/htmlcov/index.html")

    return passed == total


def generate_test_data():
    """生成测试数据"""
    print("\n" + "="*50)
    print("📝 生成测试数据")
    print("="*50)

    result = run_command([
        "python", "tests/fixtures/data_generator.py"
    ])

    if result.returncode == 0:
        print("\n✅ 测试数据生成成功")
    else:
        print("\n❌ 测试数据生成失败")
        print(result.stderr)

    return result.returncode == 0


def check_coverage():
    """检查测试覆盖率"""
    print("\n" + "="*50)
    print("📊 检查测试覆盖率")
    print("="*50)

    cmd = [
        "python", "-m", "pytest",
        "tests/unit/",
        "--cov=ui",
        "--cov=stock",
        "--cov=market",
        "--cov=llm",
        "--cov=utils",
        "--cov-report=term-missing",
        "--cov-fail-under=80"  # 目标覆盖率80%
    ]

    result = run_command(cmd)

    # 解析覆盖率结果
    if result.stdout:
        lines = result.stdout.split('\n')
        for line in lines:
            if 'TOTAL' in line and '%' in line:
                coverage = line.split()[-1]
                print(f"\n当前覆盖率: {coverage}")

                # 判断是否达标
                coverage_value = int(coverage.rstrip('%'))
                if coverage_value >= 80:
                    print("✅ 覆盖率达到目标（≥80%）")
                else:
                    print(f"❌ 覆盖率未达标（目标80%，实际{coverage_value}%）")
                break

    return result.returncode == 0


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="XY Stock 测试运行脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 运行所有单元测试
  python run_tests.py --unit

  # 运行所有测试并生成覆盖率报告
  python run_tests.py --all --coverage --html

  # 运行特定测试
  python run_tests.py --unit --verbose

  # 检查覆盖率是否达标
  python run_tests.py --check-coverage

  # 生成测试数据
  python run_tests.py --generate-data
        """
    )

    parser.add_argument("--unit", action="store_true", help="运行单元测试")
    parser.add_argument("--integration", action="store_true", help="运行集成测试")
    parser.add_argument("--e2e", action="store_true", help="运行端到端测试")
    parser.add_argument("--slow", action="store_true", help="运行慢速测试")
    parser.add_argument("--all", action="store_true", help="运行所有测试")
    parser.add_argument("--coverage", action="store_true", help="生成覆盖率报告")
    parser.add_argument("--html", action="store_true", help="生成HTML覆盖率报告")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    parser.add_argument("--check-coverage", action="store_true", help="检查覆盖率是否达标（80%）")
    parser.add_argument("--generate-data", action="store_true", help="生成测试数据")

    args = parser.parse_args()

    # 检查依赖
    try:
        import pytest
        import pytest_cov
    except ImportError as e:
        print(f"❌ 缺少测试依赖: {e}")
        print("请运行: pip install pytest pytest-cov pytest-mock")
        sys.exit(1)

    # 如果没有指定任何选项，显示帮助
    if not any(vars(args).values()):
        parser.print_help()
        return

    success = True

    # 生成测试数据
    if args.generate_data:
        success &= generate_test_data()

    # 运行测试
    if args.all:
        success &= run_all_tests(
            verbose=args.verbose,
            coverage=args.coverage,
            html_report=args.html,
            include_slow=args.slow
        )
    else:
        if args.unit:
            success &= run_unit_tests(
                verbose=args.verbose,
                coverage=args.coverage,
                html_report=args.html
            )

        if args.integration:
            success &= run_integration_tests(verbose=args.verbose)

        if args.e2e:
            success &= run_e2e_tests(verbose=args.verbose)

        if args.slow:
            success &= run_slow_tests(verbose=args.verbose)

    # 检查覆盖率
    if args.check_coverage:
        success &= check_coverage()

    # 退出码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()