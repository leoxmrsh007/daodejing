#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新的静态站点生成器入口
使用重构后的模块化结构
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from generators import StaticSiteGenerator


def main():
    """主函数"""
    generator = StaticSiteGenerator()
    success = generator.generate()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
