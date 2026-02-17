import glob
import json
import os
import re

# Configuration
DATA_DIR = r"d:\项目文件\daodejing\data"
HDNJ_DIR = os.path.join(DATA_DIR, "huangdi_neijing")
SOURCE_ROOT = r"D:\AI_DATA\datasets\中华古籍文库"

# File Paths (Found via previous search)
FILES = {
    "wangbing": {
        "path": r"D:\AI_DATA\datasets\中华古籍文库\01.中华十部古籍藏书\03道藏-1689部\06正统道藏太玄部-113部\06正统道藏太玄部-113部\正统道藏太玄部-黄帝内经素问补注释文-唐-王冰.txt",
        "encoding_candidates": ["gb18030", "big5", "utf-16", "utf-8"],
        "name": "王冰补注",
    },
    "zhangzhicong": {
        "path": r"D:\AI_DATA\datasets\中华古籍文库\01.中华十部古籍藏书\09医藏-0869部\07素问-18本\07素问-18本\黄帝内经素问集注-清-张志聪.txt",
        "encoding_candidates": ["gb18030", "gbk", "big5", "utf-8"],
        "name": "张志聪集注",
    },
    "gaoshizong": {
        "path": r"D:\AI_DATA\datasets\中华古籍文库\01.中华十部古籍藏书\09医藏-0869部\07素问-18本\07素问-18本\黄帝素问直解-清-高士宗.txt",
        "encoding_candidates": ["gb18030", "gbk", "big5", "utf-8"],
        "name": "高士宗直解",
    },
}


def read_file_content(filepath, encodings):
    """Try reading file with multiple encodings."""
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None

    for enc in encodings:
        try:
            with open(filepath, "r", encoding=enc) as f:
                content = f.read()
                # Basic validation: check for common Chinese characters
                if "黄帝" in content or "素问" in content or "岐伯" in content:
                    print(f"Successfully read {os.path.basename(filepath)} using {enc}")
                    return content
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error reading {filepath} with {enc}: {e}")

    print(f"Failed to decode {filepath} with provided encodings.")
    return None


def normalize_title(title):
    """Normalize chapter title for matching."""
    # Remove "篇", "第一", punctuation, etc.
    # Wang Bing titles often have "○" or "篇第X"
    clean = re.sub(r"[○\s\d第篇]", "", title)
    return clean


def extract_chapters(content, classic_name):
    """
    Extract chapters from content based on common Su Wen chapter titles.
    Returns a dict: {chapter_index: content_text}
    """
    chapters_found = {}

    # Su Wen has 81 chapters. We need a list of titles to match.
    # We can load them from the existing chapters.json
    with open(os.path.join(HDNJ_DIR, "chapters.json"), "r", encoding="utf-8") as f:
        existing_data = json.load(f)

    chapter_map = {}  # Normalized Title -> Index
    chapter_titles = []
    for ch in existing_data["chapters"]:
        title = ch["title"]
        norm_title = normalize_title(title)
        chapter_map[norm_title] = ch["chapter"]
        chapter_titles.append((ch["chapter"], norm_title, title))

    # Regex strategies for different files
    # Wang Bing: ○上古天真论篇第一
    # Zhang Zhicong: 上古天真论篇第一
    # General pattern: (○)?\s*TITLE\s*篇?(第[一二三四五六七八九十]+)?

    # We will iterate through the text and look for these headers.
    # Since text order matches chapter order usually, we can scan sequentially.

    # Create a giant regex for all titles? Or scan line by line?
    # Scanning line by line is safer for large files.

    lines = content.split("\n")
    current_chapter = None
    buffer = []

    # Pre-compile regexes for titles
    # We look for lines that contain the title and "篇" or "第"

    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            if current_chapter:
                buffer.append(line)
            continue

        # Check if this line is a chapter header
        matched_chapter = None

        # Heuristic: Line is short (less than 30 chars) and contains a title
        if len(line_strip) < 40:
            norm_line = normalize_title(line_strip)
            for idx, norm_title, full_title in chapter_titles:
                # Check for exact match or strong containment
                # Wang Bing: "○上古天真论篇第一" -> norm "上古天真论"
                # But sometimes titles vary slightly.
                if norm_title in norm_line and len(norm_line) < len(norm_title) + 5:
                    matched_chapter = idx
                    break

        # Relaxed matching for Wang Bing (Title Only)
        if not matched_chapter and "王冰" in classic_name and len(line_strip) < 50:
            # Try matching title without "篇" or "第" constraints
            # Just check if the core title is in the line
            for idx, norm_title, full_title in chapter_titles:
                # norm_title is like "上古天真论"
                # line might be "○上古天真论篇"
                if norm_title in line_strip:
                    # Avoid false positives?
                    # Su Wen titles are quite unique.
                    matched_chapter = idx
                    break

        if matched_chapter:
            # Save previous chapter
            if current_chapter is not None:
                chapters_found[current_chapter] = "\n".join(buffer).strip()

            # Start new chapter
            current_chapter = matched_chapter
            buffer = [line]  # Keep the header
            print(f"Found Chapter {current_chapter} in {classic_name}: {line_strip}")
        else:
            if current_chapter is not None:
                buffer.append(line)

    # Save last chapter
    if current_chapter is not None:
        chapters_found[current_chapter] = "\n".join(buffer).strip()

    return chapters_found


def main():
    # 1. Load existing chapters
    json_path = os.path.join(HDNJ_DIR, "chapters.json")
    with open(json_path, "r", encoding="utf-8") as f:
        hdnj_data = json.load(f)

    # 2. Process each source
    sources_data = {}

    for key, info in FILES.items():
        print(f"Processing {info['name']}...")
        content = read_file_content(info["path"], info["encoding_candidates"])
        if content:
            extracted = extract_chapters(content, info["name"])
            sources_data[key] = extracted
            print(f"Extracted {len(extracted)} chapters for {info['name']}")
        else:
            print(f"Skipping {info['name']} due to read error.")
            sources_data[key] = {}

    # 3. Merge into JSON
    # We will map:
    # Wang Bing -> wangbing_note
    # Zhang Zhicong -> zhangzhicong_note
    # Gao Shizong -> gaoshizong_note

    count_updated = 0
    for chapter in hdnj_data["chapters"]:
        idx = chapter["chapter"]

        # Wang Bing
        if idx in sources_data["wangbing"]:
            chapter["wangbing_note"] = sources_data["wangbing"][idx]

        # Zhang Zhicong
        if idx in sources_data["zhangzhicong"]:
            chapter["zhangzhicong_note"] = sources_data["zhangzhicong"][idx]

        # Gao Shizong
        if idx in sources_data["gaoshizong"]:
            chapter["gaoshizong_note"] = sources_data["gaoshizong"][idx]

        count_updated += 1

    # 4. Save updated JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(hdnj_data, f, ensure_ascii=False, indent=2)

    print(f"Updated {count_updated} chapters in {json_path}")


if __name__ == "__main__":
    main()
