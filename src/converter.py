# 自下向上看
"""
算法比较简单
jyy的模板中, class为"slide"的div下, 
每个section都是一个水平幻灯片
每个水平幻灯片下的每个section都是垂直幻灯片 
"""
import os, shutil, re
from pyquery import PyQuery as pq
from src.settings import *
from src.lib import *


def vertical_to_fragment(vertical: str) -> str:
    fragment_sep = "\n<!-- -->\n"
    fragments = vertical.split(fragment_sep)

    template = "<div class='fragment' data-fragment-index='{}'> {} </div>"

    fragment_list = [md_to_html(fragments[0])]
    for i in range(1, len(fragments)):
        fragment_list.append(template.format(i - 1, md_to_html(fragments[i])))

    return "\n".join(fragment_list)


def vertical_to_animate(vertical: str, folder_path) -> str:
    source = "".join(vertical.split("\n[[" + folder_path + "]]\n"))
    "<section>\n {} \n</section>"
    pass


def process_verticalfragment(vertical: str) -> str:
    if "\n<!-- -->\n" in vertical:
        return vertical_to_fragment(vertical)
    else:
        t = re.math("\n[[.*]]\n", vertical)
        if t is None:
            return md_to_html(vertical)
        else:
            return vertical_to_animate(vertical)


def horizontal_to_vertical(horizontal: str) -> str:
    verticals = horizontal.split(op_second_section)

    sections = list()
    template = "\n<section>\n {} </section>"
    if len(verticals) == 1:  # 没有垂直幻灯片
        template = "{}"

    for vertical in verticals:
        if vertical.isspace():
            continue
        fragmetns = vertical_to_fragment(vertical)
        html = template.format(fragmetns)
        sections.append(html)

    return "\n".join(sections)


def md_divide_to_horizontal(context: str):
    horizontals = context.split(op_first_section)

    sections = list()
    template = "<section>\n {} \n</section>"

    for horizontal in horizontals:
        if horizontal.isspace():
            continue
        html_second_sections = horizontal_to_vertical(horizontal)
        html = template.format(html_second_sections)
        sections.append(html)

    return "\n".join(sections)


def process_html_eles(e):
    for item in e("h1").parent():
        t = pq(item)
        t.wrap("<div style='width:100%'>")
        t.wrap("<div class='center middle'>")
    class_data = {
        "ul": " list-disc font-serif",
        "li": " ml-8",
        "h2": " text-xl mt-2 pb-2 font-sans",
        "h1": " text-2xl mt-2 font-sans",
        "p": " font-serif my-1",
        "pre": " bg-gray-100 overflow-x-auto rounded p-2 mb-2 mt-2",
    }
    for k, v in class_data.items():
        for item in e(k):
            t = pq(item)
            t.add_class(v)


def md_to_jyyhtml(context: str, filepath: str, pre_temp: str):
    """
    将内容是Markdown的字符串转换成HTML并保存到对应路径下(静态文件已经在上层函数中处理好)

    Args:
        context (str): 内容是Markdown的字符串
        filepath (str): 保存生成的一系列文件的路径
        pre_temp (str): 预处理好title和icon的HTML模板
    """
    # 先将整个Mardown切成多个水平幻灯片
    html_first_sections = md_divide_to_horizontal(context)
    pre_html = "<html>\n<body>\n{}\n</body>\n</html>".format(html_first_sections)

    # 为填充好内容的html字符串中的各个块插入对应的tag, 并拼接放入模板中
    page = pq(pre_html)
    process_html_eles(page)

    items = page("body").children()
    result = pre_temp.replace("{}", "\n".join([str(pq(e)) for e in items]))

    write(filepath, result)
    pass


def converter(MDfile, title, icon, output_foldpath):
    """
    转换器, 用于将Markdown文件转换成HTML文件(并生成相关的静态文件)
    Args:
        MDfile (str): 要转换的Markdown文件路径
        title (str): 转换出的HTML网页的title, 默认同文件名
        icon (str): 转换出的HTML网页的icon, 默认zweix的logo
        folder (str): 转换出的一系列文件放在文件夹`dist`中, 该参数指明dist目录保存位置
    """
    # 相关路径的处理
    filename = os.path.basename(MDfile)
    filepath = os.path.abspath(MDfile)
    filepath_pre = filepath.split(filename)[0]
    output_filename = "index.html"  # 习惯
    if output_foldpath is None:
        output_foldpath = os.path.join(filepath_pre, "dist")
    else:
        output_foldpath = os.path.abspath(output_foldpath)
    output_filepath = os.path.join(output_foldpath, output_filename)
    if title is None:
        title = ".".join(filename.split(".")[:-1])
    if icon is None:
        icon = os.path.join(static_path, "img", "favicon.png")

    # 转移静态文件
    if os.path.exists(output_foldpath):
        shutil.rmtree(output_foldpath)
    os.mkdir(output_foldpath)
    shutil.copytree(static_path, os.path.join(output_foldpath, "static"))
    shutil.copy(icon, os.path.join(output_foldpath, "static", "img", "favicon.png"))

    # 预处理模板
    template_html = read(template_from)
    template_html = template_html.replace("{{title}}", title)

    context = read(filepath)
    md_to_jyyhtml(context, output_filepath, template_html)
