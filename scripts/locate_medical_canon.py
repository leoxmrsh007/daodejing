import os


def find_files():
    root_dir = r"D:\AI_DATA"
    print(f"Searching in {root_dir}...")

    targets = ["马莳", "注证发微", "王冰", "类经", "张介宾", "素问", "灵枢"]
    found = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # Check for Ma Shi specifically
            if "马莳" in file or "注证发微" in file:
                print(f"FOUND MA SHI: {os.path.join(root, file)}")
                found.append(os.path.join(root, file))
            # Check for Wang Bing
            elif "王冰" in file and "素问" in file:
                print(f"FOUND WANG BING: {os.path.join(root, file)}")
            # Check for Zhang Jiebin
            elif "张介宾" in file or "类经" in file:
                # limit output for lei jing as there might be many
                if "素问" in file or "灵枢" in file or "类经" in file:
                    pass  # too many, maybe just print a few relevant ones?
                    # actually print all unique paths

    if not found:
        print("No Ma Shi files found.")


if __name__ == "__main__":
    find_files()
