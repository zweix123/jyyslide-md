import os
import chardet


def get_files_under_folder(folerpath: str, suffix_name: str = None) -> list[str]:
    """返回目录folderpath下后缀名为suffix_name的所有文件的绝对路径列表"""
    return [
        os.path.abspath(os.path.join(dirpath, filename))
        for dirpath, dirnames, filenames in os.walk(folerpath)
        for filename in filenames
        if suffix_name is None or str(filename).endswith("." + suffix_name)
    ]


def get_file_code(filepath):
    """检测文件编码格式, 效率较低"""
    res = str()
    with open(filepath, "rb") as f:
        res = chardet.detect(f.read())["encoding"]
    return res


def read(filepath):  # 读取文本文件内容
    if os.path.exists(filepath):
        with open(filepath, "r", encoding=get_file_code(filepath)) as f:
            content = f.read()
            return content
    else:
        print("now in {}".format(os.getcwd()))
        print("the path {} is not exists".format(filepath))
        exit(-1)


def write(filepath, data):  # 向文件(覆)写入内容(这里保证file一定是创建好并被正确使用过的)
    if os.path.exists(filepath) is False:
        with open(filepath, "w") as f:
            f.write(data)
    else:
        with open(filepath, "w", encoding=get_file_code(filepath)) as f:
            f.write(data)
