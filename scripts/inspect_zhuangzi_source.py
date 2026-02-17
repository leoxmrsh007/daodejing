import os


def inspect_file():
    path = r"D:\AI_DATA\datasets\中华古籍文库\01.中华十部古籍藏书\03道藏-1689部\01正统道藏洞神部-369部\01正统道藏洞神部-369部\正统道藏洞神部玉诀类-南华真经注疏-晋-郭象.txt"
    try:
        with open(path, "r", encoding="gb18030") as f:
            content = f.read(2000)
            print(content)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    inspect_file()
