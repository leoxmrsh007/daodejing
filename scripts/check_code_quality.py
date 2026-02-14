#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码质量检查脚本
运行所有代码质量检查工具
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """运行命令并处理输出"""
    print(f"\n{'=' * 60}")
    print(f"运行: {description}")
    print(f"命令: {cmd}")
    print("=" * 60)

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        if result.returncode == 0:
            print("✅ 成功")
            if result.stdout.strip():
                print("输出:")
                print(result.stdout[:1000])  # 限制输出长度
        else:
            print("❌ 失败")
            print("标准输出:")
            print(result.stdout[:2000])
            print("\n标准错误:")
            print(result.stderr[:2000])

        return result.returncode == 0
    except Exception as e:
        print(f"❌ 执行错误: {e}")
        return False


def main():
    """主函数"""
    print("🚀 道德经平台 - 代码质量检查")
    print(f"工作目录: {Path(__file__).parent.parent}")

    all_passed = True

    # 1. 运行flake8
    flake8_passed = run_command(
        "python -m flake8 --config=.flake8 .", "Flake8代码风格检查"
    )
    all_passed = all_passed and flake8_passed

    # 2. 运行mypy
    mypy_passed = run_command("python -m mypy --config-file=mypy.ini .", "Mypy类型检查")
    all_passed = all_passed and mypy_passed

    # 3. 运行pytest测试
    pytest_passed = run_command("python -m pytest tests/ -v", "Pytest测试")
    all_passed = all_passed and pytest_passed

    # 4. 运行pytest覆盖率
    coverage_passed = run_command(
        "python -m pytest tests/ --cov=services --cov-report=term-missing",
        "测试覆盖率检查",
    )
    all_passed = all_passed and coverage_passed

    # 5. 检查导入排序（可选）
    try:
        import isort

        isort_passed = run_command(
            "python -m isort --check-only --profile=black .", "导入排序检查"
        )
        all_passed = all_passed and isort_passed
    except ImportError:
        print("\n⚠️  isort未安装，跳过导入排序检查")
        print("安装: pip install isort")

    # 6. 检查代码格式化（可选）
    try:
        import black

        black_passed = run_command(
            "python -m black --check --diff .", "Black代码格式化检查"
        )
        all_passed = all_passed and black_passed
    except ImportError:
        print("\n⚠️  black未安装，跳过格式化检查")
        print("安装: pip install black")

    # 总结
    print(f"\n{'=' * 60}")
    print("📊 检查总结")
    print("=" * 60)

    if all_passed:
        print("🎉 所有检查通过！代码质量优秀。")
        return 0
    else:
        print("⚠️  部分检查未通过，请修复上述问题。")
        print("\n建议修复步骤:")
        print("1. 运行 black . 自动格式化代码")
        print("2. 运行 isort . 自动排序导入")
        print("3. 修复flake8报告的问题")
        print("4. 修复mypy报告的类型错误")
        print("5. 添加缺失的测试")
        return 1


if __name__ == "__main__":
    sys.exit(main())
