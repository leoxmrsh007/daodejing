#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片优化脚本
压缩和优化图片文件，减少文件大小
"""

import io
import os
from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image


def optimize_image(
    input_path: Path,
    output_path: Path = None,
    quality: int = 85,
    max_width: int = None,
    format: str = None,
    create_backup: bool = True,
) -> Tuple[bool, int, int]:
    """
    优化单个图片文件

    Args:
        input_path: 输入文件路径
        output_path: 输出文件路径（如果为None，则覆盖原文件）
        quality: 图片质量 (1-100)
        max_width: 最大宽度（保持比例）
        format: 输出格式（如果为None，则保持原格式）
        create_backup: 是否创建备份

    Returns:
        (是否成功, 原始大小, 优化后大小)
    """
    try:
        # 读取原始图片
        img = Image.open(input_path)

        # 确定输出格式
        if format is None:
            format = img.format

        # 调整大小（如果需要）
        if max_width and img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

        # 确定输出路径
        if output_path is None:
            output_path = input_path
        else:
            # 确保输出目录存在
            output_path.parent.mkdir(parents=True, exist_ok=True)

        # 创建备份
        if create_backup and output_path == input_path:
            backup_path = input_path.with_suffix(f".{format.lower()}.backup")
            if not backup_path.exists():
                import shutil

                shutil.copy2(input_path, backup_path)

        # 保存优化后的图片
        original_size = input_path.stat().st_size

        # 根据格式优化
        if format.lower() in ["jpg", "jpeg"]:
            img.save(output_path, "JPEG", quality=quality, optimize=True)
        elif format.lower() == "png":
            img.save(output_path, "PNG", optimize=True)
        elif format.lower() == "webp":
            img.save(output_path, "WEBP", quality=quality, method=6)
        else:
            img.save(output_path, optimize=True)

        # 获取优化后的大小
        optimized_size = output_path.stat().st_size

        return True, original_size, optimized_size
    except Exception as e:
        print(f"❌ 优化失败: {input_path.name} - {e}")
        return False, 0, 0


def optimize_images_directory(
    images_dir: Path,
    quality: int = 85,
    max_width: int = None,
    convert_to_webp: bool = False,
) -> Dict[str, any]:
    """
    优化目录中的所有图片文件

    Args:
        images_dir: 图片目录
        quality: 图片质量 (1-100)
        max_width: 最大宽度
        convert_to_webp: 是否转换为WebP格式

    Returns:
        优化结果统计
    """
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    results = {
        "total_files": 0,
        "success_count": 0,
        "original_size": 0,
        "optimized_size": 0,
        "files": [],
    }

    # 查找所有图片文件
    image_files = []
    for ext in image_extensions:
        image_files.extend(images_dir.glob(f"**/*{ext}"))

    for img_file in image_files:
        results["total_files"] += 1

        # 确定输出格式
        output_format = "webp" if convert_to_webp else None
        output_path = img_file

        if convert_to_webp:
            # 转换为WebP
            output_path = img_file.with_suffix(".webp")

        # 优化图片
        success, original_size, optimized_size = optimize_image(
            img_file,
            output_path=output_path,
            quality=quality,
            max_width=max_width,
            format=output_format,
            create_backup=True,
        )

        if success:
            results["success_count"] += 1
            results["original_size"] += original_size
            results["optimized_size"] += optimized_size

            reduction = original_size - optimized_size
            reduction_pct = (
                (reduction / original_size * 100) if original_size > 0 else 0
            )

            results["files"].append(
                {
                    "name": str(img_file.relative_to(images_dir.parent)),
                    "original_size": original_size,
                    "optimized_size": optimized_size,
                    "reduction": reduction,
                    "reduction_pct": reduction_pct,
                    "format": output_format or img_file.suffix[1:],
                }
            )

            print(
                f"✅ {img_file.name}: {original_size:,} -> {optimized_size:,} bytes (-{reduction_pct:.1f}%)"
            )

    # 计算总体压缩率
    total_reduction = results["original_size"] - results["optimized_size"]
    total_reduction_pct = (
        (total_reduction / results["original_size"] * 100)
        if results["original_size"] > 0
        else 0
    )

    results["total_reduction"] = total_reduction
    results["total_reduction_pct"] = total_reduction_pct

    return results


def restore_backup(images_dir: Path) -> int:
    """
    从备份恢复原始图片

    Args:
        images_dir: 图片目录

    Returns:
        恢复的文件数量
    """
    import shutil

    restored_count = 0
    backup_extensions = [".jpg.backup", ".jpeg.backup", ".png.backup", ".webp.backup"]

    for ext in backup_extensions:
        backup_files = list(images_dir.glob(f"**/*{ext}"))
        for backup_file in backup_files:
            # 移除.backup扩展名
            original_file = backup_file.with_suffix("")
            if original_file.exists():
                shutil.copy2(backup_file, original_file)
                print(f"✅ 已恢复: {original_file.name}")
                restored_count += 1

    return restored_count


def main():
    """主函数"""
    import sys

    base_dir = Path(__file__).parent.parent
    images_dir = base_dir / "static" / "images"

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "optimize":
            # 优化图片
            print("=" * 60)
            print("🖼️  开始优化图片")
            print("=" * 60)

            quality = 85  # 默认质量
            max_width = None  # 默认不限制宽度
            convert_to_webp = False  # 默认不转换格式

            # 解析参数
            for arg in sys.argv[2:]:
                if arg.startswith("--quality="):
                    quality = int(arg.split("=")[1])
                elif arg.startswith("--max-width="):
                    max_width = int(arg.split("=")[1])
                elif arg == "--webp":
                    convert_to_webp = True

            results = optimize_images_directory(
                images_dir,
                quality=quality,
                max_width=max_width,
                convert_to_webp=convert_to_webp,
            )

            print("\n" + "=" * 60)
            print("📊 优化结果")
            print("=" * 60)
            print(f"处理文件数: {results['total_files']}")
            print(f"成功优化: {results['success_count']}")
            print(
                f"原始大小: {results['original_size']:,} bytes ({results['original_size'] / 1024:.1f} KB)"
            )
            print(
                f"优化后大小: {results['optimized_size']:,} bytes ({results['optimized_size'] / 1024:.1f} KB)"
            )
            print(
                f"节省空间: {results['total_reduction']:,} bytes ({results['total_reduction'] / 1024:.1f} KB)"
            )
            print(f"压缩率: {results['total_reduction_pct']:.1f}%")

            # 显示每个文件的优化结果
            print("\n详细结果:")
            for file_info in results["files"]:
                print(
                    f"  {file_info['name']}: -{file_info['reduction_pct']:.1f}% ({file_info['format']})"
                )

        elif command == "restore":
            # 恢复备份
            print("=" * 60)
            print("🔄 恢复备份图片")
            print("=" * 60)

            restored_count = restore_backup(images_dir)
            print(f"\n✅ 已恢复 {restored_count} 个文件")

        else:
            print(f"❌ 未知命令: {command}")
            print("可用命令: optimize, restore")
            print("\noptimize命令选项:")
            print("  --quality=N     设置图片质量 (1-100, 默认85)")
            print("  --max-width=N   设置最大宽度")
            print("  --webp          转换为WebP格式")

    else:
        print("用法: python scripts/optimize_images.py [optimize|restore]")
        print("  optimize - 优化所有图片")
        print("  restore  - 从备份恢复原始图片")
        print("\noptimize命令选项:")
        print("  --quality=N     设置图片质量 (1-100, 默认85)")
        print("  --max-width=N   设置最大宽度")
        print("  --webp          转换为WebP格式")


if __name__ == "__main__":
    main()
