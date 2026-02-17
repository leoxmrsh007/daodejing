import os


def inspect_wang_file():
    path = r"D:\AI_DATA\datasets\中华古籍文库\01.中华十部古籍藏书\03道藏-1689部\09藏外-186种\09藏外-186种\庄子通-清-王船山.txt"
    try:
        with open(path, "r", encoding="gb18030") as f:
            content = f.read(3000)
            print(content)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    inspect_wang_file()
