# -*- coding: utf-8 -*-
"""Add more idioms to data/idioms.json"""

import json

# Additional Daoist idioms
additional_idioms = [
    {
        "chapter": 34,
        "title": "道法自然",
        "meaning": "道的运行遵循自然规律，不需要人为干预",
        "source": "道德经·第二十五章",
        "keyword": "自然",
    },
    {
        "chapter": 41,
        "title": "上善若水",
        "meaning": "最高尚的品德像水一样滋润万物而不争",
        "source": "道德经·第八章",
        "keyword": "上善若水",
    },
    {
        "chapter": 42,
        "title": "大音希声",
        "meaning": "最大的声音反而听不到，意味着真正的伟大是无形无相",
        "source": "道德经·第四十一章",
        "keyword": "大音希声",
    },
    {
        "chapter": 43,
        "title": "无之以为用",
        "meaning": "把'没有'当作有用，实际上是不占有不执着的智慧",
        "source": "道德经·第十一章",
        "keyword": "无之以为用",
    },
    {
        "chapter": 60,
        "title": "治大国若烹小鲜",
        "meaning": "治理大国就像烹小鱼一样，不能急躁",
        "source": "道德经·第六十章",
        "keyword": "治大国若烹小鲜",
    },
    {
        "chapter": 61,
        "title": "大国者下流",
        "meaning": "大国的行为像水流向下一样，自然谦下",
        "source": "道德经·第六十一章",
        "keyword": "大国者下流",
    },
    {
        "chapter": 64,
        "title": "以道莅天下",
        "meaning": "用道的原则来统治天下，无为而治",
        "source": "道德经·第六十章",
        "keyword": "以道莅天下",
    },
    {
        "chapter": 76,
        "title": "柔弱胜刚强",
        "meaning": "柔软的反而能战胜刚强的，这是道家的重要观点",
        "source": "道德经·第七十六章",
        "keyword": "柔弱胜刚强",
    },
    {
        "chapter": 78,
        "title": "受国之垢",
        "meaning": "能承受国家的屈辱，体现宽容的胸襟",
        "source": "道德经·第七十八章",
        "keyword": "受国之垢",
    },
    {
        "chapter": 80,
        "title": "小国寡民",
        "meaning": "小国百姓少，更容易治理和管理",
        "source": "道德经·第八十章",
        "keyword": "小国寡民",
    },
    {
        "chapter": 81,
        "title": "信言不美",
        "meaning": "朴实的话语可能不华丽，但更可靠",
        "source": "道德经·第八十一章",
        "keyword": "信言不美",
    },
]

# Load existing
with open("data/idioms.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    existing_idioms = data.get("idioms", [])

# Append new idioms
existing_idioms.extend(additional_idioms)

# Update
data["idioms"] = existing_idioms

# Save
with open("data/idioms.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Updated idioms: {len(data['idioms'])} total")
print(f"Added: {len(additional_idioms)} new idioms")
