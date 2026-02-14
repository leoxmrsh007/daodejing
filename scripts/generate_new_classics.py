#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

import json
import os

# 新经典配置
NEW_CLASSICS = []

def create_classic_json(classic_config):
    """"创建经典数据文件"""
    data = {
        "title"": classic_config["title"],
        "chapters"：classic_config["chapters"],
        "commentators"：classic_config.get("commentators", []),
        "translators"：classic_config.get("translators", []),
        "variants"：classic_config.get("variants", [])
    }
    
    return data

def main():
    """"主函数"""
    base_dir = r"D:\项目文件\daodejing\data"
    
    print("开始生成数据文件...")
    
with open(r'D:\项目文件\daodejing\data\classics.json', 'r', encoding='utf-8') as f:
        all_classics = json.load(f)
        NEW_CLASSICS = [c for c in all_classics['classics'] if c['id'] not in ['ddj', 'zzj', 'hdnj']]
    
    print(f"找到 {len(NEW_CLASSICS)} 部新经典")
    
    # 为每部经典创建数据文件
    for classic in NEW_CLASSICS:
        dir_path = os.path.join(base_dir, classic["id"])
        os.makedirs(dir_path, exist_ok=True)
        
        file_path = os.path.join(dir_path, "chapters.json")
        
        data = create_classic_json(classic)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"创建 {classic['name']} 数据: {file_path}")
        print(f"章节数: {len(data['chapters'])}")
    
    print("
✓ 所有经典数据文件创建完成！")

if __name__ == "__main__":
    main()
