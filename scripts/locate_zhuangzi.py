import os


def find_zhuangzi_files():
    root_dir = r"D:\AI_DATA\datasets\中华古籍文库"
    keywords = ["庄子", "南华"]
    commentators = ["郭象", "成玄英", "王夫之", "注", "疏", "解"]

    print(f"Searching in {root_dir}...")

    found_files = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if any(k in file for k in keywords):
                full_path = os.path.join(root, file)
                # Check if it looks like a commentary
                is_commentary = any(c in file for c in commentators)
                found_files.append((full_path, is_commentary))

    # Sort: Commentaries first
    found_files.sort(key=lambda x: x[1], reverse=True)

    for path, is_comm in found_files:
        print(f"{'[COMMENTARY]' if is_comm else '[TEXT]      '} {path}")


if __name__ == "__main__":
    find_zhuangzi_files()
