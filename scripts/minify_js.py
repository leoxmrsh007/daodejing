#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JavaScript文件压缩脚本
使用rjsmin压缩JavaScript文件，减小文件大小
"""

import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

import rjsmin


def compress_js_file(
    input_path: Path, output_path: Path = None
) -> Tuple[bool, int, int]:
    """
    压缩单个JavaScript文件

    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径（如果为None，则覆盖原文件）

    Returns:
        (是否成功, 原始大小, 压缩后大小)
    """
    try:
        # 读取原始文件
        with open(input_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        original_size = len(original_content.encode("utf-8"))

        # 压缩JavaScript
        minified_content = rjsmin.jsmin(original_content)

        minified_size = len(minified_content.encode("utf-8"))

        # 确定输出路径
        if output_path is None:
            output_path = input_path
        else:
            # 确保输出目录存在
            output_path.parent.mkdir(parents=True, exist_ok=True)

        # 写入压缩后的文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(minified_content)

        return True, original_size, minified_size
    except Exception as e:
        print(f"❌ 压缩失败: {input_path.name} - {e}")
        return False, 0, 0


def compress_js_directory(
    js_dir: Path, exclude_files: List[str] = None, create_backup: bool = True
) -> Dict[str, any]:
    """
    压缩目录中的所有JavaScript文件

    Args:
        js_dir: JavaScript目录
        exclude_files: 要排除的文件列表
        create_backup: 是否创建备份

    Returns:
        压缩结果统计
    """
    if exclude_files is None:
        exclude_files = []

    results = {
        "total_files": 0,
        "success_count": 0,
        "original_size": 0,
        "minified_size": 0,
        "files": [],
    }

    # 查找所有JavaScript文件
    js_files = list(js_dir.glob("**/*.js"))

    for js_file in js_files:
        # 跳过排除的文件
        if js_file.name in exclude_files:
            print(f"⏭️  跳过: {js_file.name}")
            continue

        results["total_files"] += 1

        # 创建备份
        if create_backup:
            backup_path = js_file.with_suffix(".js.backup")
            if not backup_path.exists():
                shutil.copy2(js_file, backup_path)

        # 压缩文件
        success, original_size, minified_size = compress_js_file(js_file)

        if success:
            results["success_count"] += 1
            results["original_size"] += original_size
            results["minified_size"] += minified_size

            reduction = original_size - minified_size
            reduction_pct = (
                (reduction / original_size * 100) if original_size > 0 else 0
            )

            results["files"].append(
                {
                    "name": str(js_file.relative_to(js_dir.parent)),
                    "original_size": original_size,
                    "minified_size": minified_size,
                    "reduction": reduction,
                    "reduction_pct": reduction_pct,
                }
            )

            print(
                f"✅ {js_file.name}: {original_size} -> {minified_size} bytes (-{reduction_pct:.1f}%)"
            )

    # 计算总体压缩率
    total_reduction = results["original_size"] - results["minified_size"]
    total_reduction_pct = (
        (total_reduction / results["original_size"] * 100)
        if results["original_size"] > 0
        else 0
    )

    results["total_reduction"] = total_reduction
    results["total_reduction_pct"] = total_reduction_pct

    return results


def restore_backup(js_dir: Path) -> int:
    """
    从备份恢复原始文件

    Args:
        js_dir: JavaScript目录

    Returns:
        恢复的文件数量
    """
    restored_count = 0
    backup_files = list(js_dir.glob("**/*.js.backup"))

    for backup_file in backup_files:
        original_file = backup_file.with_suffix("")  # 移除.backup
        if original_file.exists():
            shutil.copy2(backup_file, original_file)
            print(f"✅ 已恢复: {original_file.name}")
            restored_count += 1

    return restored_count


def main():
    """主函数"""
    import sys

    base_dir = Path(__file__).parent.parent
    js_dir = base_dir / "static" / "js"

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "compress":
            # 压缩JavaScript文件
            print("=" * 60)
            print("🚀 开始压缩JavaScript文件")
            print("=" * 60)

            # 排除一些不应该压缩的文件
            exclude_files = [
                # 可以添加需要排除的文件
            ]

            results = compress_js_directory(
                js_dir, exclude_files=exclude_files, create_backup=True
            )

            print("\n" + "=" * 60)
            print("📊 压缩结果")
            print("=" * 60)
            print(f"处理文件数: {results['total_files']}")
            print(f"成功压缩: {results['success_count']}")
            print(
                f"原始大小: {results['original_size']:,} bytes ({results['original_size'] / 1024:.1f} KB)"
            )
            print(
                f"压缩后大小: {results['minified_size']:,} bytes ({results['minified_size'] / 1024:.1f} KB)"
            )
            print(
                f"节省空间: {results['total_reduction']:,} bytes ({results['total_reduction'] / 1024:.1f} KB)"
            )
            print(f"压缩率: {results['total_reduction_pct']:.1f}%")

            # 显示每个文件的压缩结果
            print("\n详细结果:")
            for file_info in results["files"]:
                print(f"  {file_info['name']}: -{file_info['reduction_pct']:.1f}%")

        elif command == "restore":
            # 恢复备份
            print("=" * 60)
            print("🔄 恢复备份文件")
            print("=" * 60)

            restored_count = restore_backup(js_dir)
            print(f"\n✅ 已恢复 {restored_count} 个文件")

        else:
            print(f"❌ 未知命令: {command}")
            print("可用命令: compress, restore")

    else:
        print("用法: python scripts/minify_js.py [compress|restore]")
        print("  compress - 压缩所有JavaScript文件")
        print("  restore  - 从备份恢复原始文件")


if __name__ == "__main__":
    main()
