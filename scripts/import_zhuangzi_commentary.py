import json
import os
import re

# Configuration
DATA_DIR = r"d:\项目文件\daodejing\data"
ZZJ_DIR = os.path.join(DATA_DIR, "zhuangzi")
GUO_CHENG_PATH = r"D:\AI_DATA\datasets\中华古籍文库\01.中华十部古籍藏书\03道藏-1689部\01正统道藏洞神部-369部\01正统道藏洞神部-369部\正统道藏洞神部玉诀类-南华真经注疏-晋-郭象.txt"
WANG_PATH = r"D:\AI_DATA\datasets\中华古籍文库\01.中华十部古籍藏书\03道藏-1689部\09藏外-186种\09藏外-186种\庄子通-清-王船山.txt"


def load_chapters():
    with open(os.path.join(ZZJ_DIR, "chapters.json"), "r", encoding="utf-8") as f:
        return json.load(f)


def clean_text(text):
    return text.strip()


def parse_guo_cheng(chapters_data):
    print("Parsing Guo Xiang & Cheng Xuanying...")

    # Map title to chapter index
    # We use a mapping for Traditional/Variant titles found in the file
    title_map = {}
    title_regex_map = {}

    # Manual mapping for difficult titles (Simplified -> Regex for File)
    manual_map = {
        "逍遥游": r"逍[遥遙][游遊]",
        "齐物论": r"[齐齊]物[论論]",
        "养生主": r"[养養]生主",
        "人间世": r"人[间間問]世",  # Handle '問' typo
        "德充符": r"德充符",
        "大宗师": r"大宗[师師]",
        "应帝王": r"[应應]帝王",
        "骈拇": r"[骈駢]拇",
        "马蹄": r"[马馬]蹄",
        "胠箧": r"[胠肚][箧筐篋]",  # Inspect showed '肚筐'?
        "在宥": r"在宥",
        "天地": r"天地",
        "天道": r"天道",
        "天运": r"天[运運]",
        "刻意": r"刻意",
        "缮性": r"[缮繕]性",
        "秋水": r"秋水",
        "至乐": r"至[乐樂]",
        "达生": r"[达達]生",
        "山木": r"山木",
        "田子方": r"田子方",
        "知北游": r"知北[游遊]",
        "庚桑楚": r"庚桑楚",
        "徐无鬼": r"徐[无無]鬼",
        "则阳": r"[则則][阳陽]",
        "外物": r"外物",
        "寓言": r"寓言",
        "让王": r"[让讓]王",
        "盗跖": r"[盗盜][跖躡]",  # Inspect showed '盜躡'
        "说剑": r"[说說][剑劍]",
        "渔父": r"[渔漁]父",
        "列御寇": r"列御寇",
        "天下": r"天下",
    }

    for ch in chapters_data["chapters"]:
        title = ch["title"]
        idx = ch["chapter"]
        pattern = manual_map.get(title, title)
        title_regex_map[idx] = re.compile(pattern)

    try:
        with open(GUO_CHENG_PATH, "r", encoding="gb18030") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading Guo/Cheng file: {e}")
        return {}

    extracted = {}
    current_chapter = None

    # Regex for chapter header start
    # Matches: "內篇...", "外篇...", "雜篇..."
    header_start_pattern = re.compile(r"^(内|內|外|杂|雜)篇")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check for chapter header
        if header_start_pattern.match(line):
            # Check which chapter title matches this line
            for idx, pattern in title_regex_map.items():
                if pattern.search(line):
                    current_chapter = idx
                    if idx not in extracted:
                        extracted[idx] = {"guoxiang": [], "chengxuanying": []}
                    print(f"  Found Chapter {idx}: {line}")
                    break

        if current_chapter is not None:
            # Parse [註] and [疏]
            # Replace Traditional Markers if necessary?
            # The file uses 〔註〕 and 〔疏〕 (Unicode 3014, 8A3B/758F, 3015)
            # Or maybe just [註] ? Inspect output showed 〔註〕.

            parts = re.split(r"(〔註〕|〔疏〕|\[註\]|\[疏\])", line)

            current_type = None

            # If line doesn't start with marker, first part is original text (ignore)

            for part in parts:
                if part in ["〔註〕", "[註]"]:
                    current_type = "guoxiang"
                elif part in ["〔疏〕", "[疏]"]:
                    current_type = "chengxuanying"
                else:
                    if current_type == "guoxiang":
                        extracted[current_chapter]["guoxiang"].append(part)
                    elif current_type == "chengxuanying":
                        extracted[current_chapter]["chengxuanying"].append(part)

    # Join lists
    final_data = {}
    for idx, data in extracted.items():
        final_data[idx] = {
            "guoxiang": "\n".join([x.strip() for x in data["guoxiang"] if x.strip()]),
            "chengxuanying": "\n".join(
                [x.strip() for x in data["chengxuanying"] if x.strip()]
            ),
        }

    return final_data


def parse_wang_fuzhi(chapters_data):
    print("Parsing Wang Fuzhi...")

    title_regex_map = {}

    # Manual mapping for difficult titles (Simplified -> Regex for File)
    manual_map = {
        "逍遥游": r"逍[遥遙][游遊]",
        "齐物论": r"[齐齊]物[论論]",
        "养生主": r"[养養]生主",
        "人间世": r"人[间間]世",
        "德充符": r"德充符",
        "大宗师": r"大宗[师師]",
        "应帝王": r"[应應]帝王",
        "骈拇": r"[骈駢]拇",
        "马蹄": r"[马馬]蹄",
        "胠箧": r"[胠肚][箧筐篋]",  # Inspect showed '肚筐'?
        "在宥": r"在宥",
        "天地": r"天地",
        "天道": r"天道",
        "天运": r"天[运運]",
        "刻意": r"刻意",
        "缮性": r"[缮繕]性",
        "秋水": r"秋水",
        "至乐": r"至[乐樂]",
        "达生": r"[达達]生",
        "山木": r"山木",
        "田子方": r"田子方",
        "知北游": r"知北[游遊]",
        "庚桑楚": r"庚桑楚",
        "徐无鬼": r"徐[无無]鬼",
        "则阳": r"[则則][阳陽]",
        "外物": r"外物",
        "寓言": r"寓言",
        "让王": r"[让讓]王",
        "盗跖": r"[盗盜][跖躡]",  # Inspect showed '盜躡'
        "说剑": r"[说說][剑劍]",
        "渔父": r"[渔漁]父",
        "列御寇": r"列御寇",
        "天下": r"天下",
    }

    for ch in chapters_data["chapters"]:
        title = ch["title"]
        idx = ch["chapter"]
        pattern = manual_map.get(title, title)
        title_regex_map[idx] = re.compile(pattern)

    try:
        with open(WANG_PATH, "r", encoding="gb18030") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading Wang file: {e}")
        return {}

    extracted = {}
    current_chapter = None

    # Wang's file uses titles as headers

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if line IS a title (Exact or Regex match)
        # We need to iterate
        is_title = False
        line_clean = line.replace(" ", "")

        for idx, pattern in title_regex_map.items():
            if pattern.search(line_clean) and len(line_clean) < 10:
                current_chapter = idx
                extracted[idx] = []
                print(f"  Found Chapter {idx}: {line}")
                is_title = True
                break

        if is_title:
            continue

        if current_chapter is not None:
            extracted[current_chapter].append(line)

    # Join
    final_data = {}
    for idx, lines_list in extracted.items():
        final_data[idx] = "\n".join(lines_list)

    return final_data


def main():
    hdnj_data = load_chapters()

    guo_cheng_data = parse_guo_cheng(hdnj_data)
    wang_data = parse_wang_fuzhi(hdnj_data)

    count_updated = 0

    for chapter in hdnj_data["chapters"]:
        idx = chapter["chapter"]
        updated = False

        # Update Guo/Cheng
        if idx in guo_cheng_data:
            if guo_cheng_data[idx]["guoxiang"]:
                chapter["guoxiang_note"] = guo_cheng_data[idx]["guoxiang"]
                updated = True
            if guo_cheng_data[idx]["chengxuanying"]:
                chapter["chengxuanying_note"] = guo_cheng_data[idx]["chengxuanying"]
                updated = True

        # Update Wang
        if idx in wang_data:
            chapter["wangfuzhi_note"] = wang_data[idx]
            updated = True

        if updated:
            count_updated += 1

    # Save
    with open(os.path.join(ZZJ_DIR, "chapters.json"), "w", encoding="utf-8") as f:
        json.dump(hdnj_data, f, ensure_ascii=False, indent=2)

    print(f"Updated {count_updated} chapters.")


if __name__ == "__main__":
    main()
