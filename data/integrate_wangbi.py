# -*- coding: utf-8 -*-
"""
整合王弼《老子注》完整注释到主数据文件
"""

import json

# 数据文件路径
DATA_DIR = r'D:\项目文件\daodejing\data'
WANGBI_FILE = f'{DATA_DIR}\\wangbi_full_notes.json'
MAIN_DATA_FILE = f'{DATA_DIR}\\daodejing.json'
OUTPUT_FILE = f'{DATA_DIR}\\daodejing.json'

# 加载王弼完整注释
with open(WANGBI_FILE, 'r', encoding='utf-8') as f:
    wangbi_notes = json.load(f)

# 加载主数据文件
with open(MAIN_DATA_FILE, 'r', encoding='utf-8') as f:
    main_data = json.load(f)

print(f"王弼注释文件包含 {len(wangbi_notes)} 章")
print(f"主数据文件包含 {len(main_data['chapters'])} 章")

# 找出缺失的章节
existing_chapters = set(wangbi_notes.keys())
missing_chapters = []
for i in range(1, 82):
    if str(i) not in existing_chapters:
        missing_chapters.append(i)

if missing_chapters:
    print(f"王弼注释中缺失的章节: {missing_chapters}")

# 更新主数据文件中的王弼注释
updated_count = 0
kept_count = 0
for chapter in main_data['chapters']:
    chapter_num = str(chapter['chapter'])
    if chapter_num in wangbi_notes:
        # 使用完整的王弼注释
        new_note = wangbi_notes[chapter_num]
        if new_note != chapter.get('wangbi_note', ''):
            chapter['wangbi_note'] = new_note
            updated_count += 1
        else:
            kept_count += 1
    else:
        # 保持原有注释（缺失章节）
        print(f"第{chapter['chapter']}章保持原有注释")
        kept_count += 1

print(f"\n更新完成:")
print(f"- 更新了 {updated_count} 章的王弼注释")
print(f"- 保持了 {kept_count} 章的原有注释")

# 保存更新后的数据
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(main_data, f, ensure_ascii=False, indent=2)

print(f"\n已保存更新后的数据到: {OUTPUT_FILE}")

# 显示一些示例更新
print("\n示例更新:")
for chapter in main_data['chapters'][:3]:
    print(f"\n第{chapter['chapter']}章:")
    note_preview = chapter['wangbi_note'][:100] + "..." if len(chapter['wangbi_note']) > 100 else chapter['wangbi_note']
    print(f"  {note_preview}")
