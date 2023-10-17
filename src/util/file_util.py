import os, shutil, uuid
from typing import Optional, Tuple
from . import str_util, net_util


def get_files_under_folder(
    folerpath: str, suffix_name: Optional[str] = None
) -> list[str]:
    """返回目录folderpath下后缀名为suffix_name的所有文件的绝对路径列表"""
    return [
        os.path.abspath(os.path.join(dirpath, filename))
        for dirpath, dirnames, filenames in os.walk(folerpath)
        for filename in filenames
        if suffix_name is None or str(filename).endswith("." + suffix_name)
    ]


def read(filepath: str) -> str:  # 读取文本文件内容
    if os.path.exists(filepath) is False:
        raise Exception("The path {} is not exists".format(filepath))
    with open(filepath, "r", encoding="utf-8") as f:
        return str(f.read())


def write(filepath: str, data: str) -> None:  # 向文件(覆)写内容
    dirpath = os.path.dirname(filepath)
    if os.path.exists(dirpath) is False:
        os.makedirs(dirpath)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(data)


def get_abspath(basefile: str, filepath: str) -> str:  # 从绝对路径变化成相对路径且符合当前的操作系统
    return os.path.normpath(os.path.join(os.path.dirname(basefile), filepath))


def get_image_to_target(
    link: str, from_filepath: str, target_foldpath: str
) -> Tuple[str, bool]:
    # 对于from_filepath(请使用其绝对地址)中的图床链接link, 它可能是url、绝对地址或相对地址, 我们会get它然后重命名并放到target_foldpath下, 并返回重命名后的名字
    # 这里对图片类型的判断是通过link的后缀名, 有些图片的url的末尾不是类型名, 就会有bug
    name = uuid.uuid4().hex + "." + link.split(".")[-1]
    if str_util.is_url(link):
        pass
    else:
        if os.path.isabs(link) is True:
            pass
        else:
            link = get_abspath(from_filepath, link)
            pass

    if str_util.is_url(link):
        net_util.down_image(link, os.path.join(target_foldpath, name))
    else:
        if os.path.exists(link) is False:
            print("The path is not exists: ", link)
            return "", True
        shutil.copyfile(link, os.path.join(target_foldpath, name))

    return name, False
