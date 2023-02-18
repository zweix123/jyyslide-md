# 自下向上看
"""
算法比较简单
jyy的模板中, class为"slide"的div下, 
每个section都是一个水平幻灯片
每个水平幻灯片下的每个section都是垂直幻灯片 
"""
import os, shutil, re

import xml.etree.ElementTree as etree
from pyquery import PyQuery as pq
import markdown
from markdown import Extension
from markdown.blockprocessors import BlockProcessor

from src.lib import *


# div处理
def add_wrap(e):
    for item in e("h1").parent():
        t = pq(item)
        t.wrap("<div style='width:100%'>")
        t.wrap("<div class='center middle'>")


def add_class(e):
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


# markdwon convert html
def md_to_html(md: str) -> str:
    # infrastructure
    class BoxBlockProcessor(BlockProcessor):
        first = True

        def test(self, parent, block):
            return self.first

        def run(self, parent, blocks):
            if self.first:
                self.first = False

                e = etree.SubElement(parent, "div")
                # e.set('style', 'display: inline-block; border: 1px solid red;')
                self.parser.parseBlocks(e, blocks)
                # remove used blocks
                for i in range(0, len(blocks)):
                    blocks.pop(0)
                return True  # or could have had no return statement
            return False  # equivalent to our test() routine returning False

    class BoxExtension(Extension):
        def extendMarkdown(self, md):
            md.parser.blockprocessors.register(BoxBlockProcessor(md.parser), "box", 175)

    extensions = [
        BoxExtension(),
        "meta",
        "fenced_code",
        "codehilite",
        "attr_list",
        "tables",
    ]
    return markdown.markdown(md, extensions=extensions)


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
    vertical_sep = "\n----\n"
    verticals = horizontal.split(vertical_sep)

    template = "\n<section>\n {} </section>"
    if len(verticals) == 1:
        template = "{}"

    sections = list()
    for vertical in verticals:
        if vertical.isspace():
            continue
        fragmetns = vertical_to_fragment(vertical)
        html = template.format(fragmetns)
        sections.append(html)

    return "\n".join(sections)


def md_divide_to_horizontal(context: str):
    horizontal_sep = "\n---\n"
    horizontals = context.split(horizontal_sep)

    sections = list()
    template = "<section>\n {} \n</section>"

    for horizontal in horizontals:
        if horizontal.isspace():
            continue
        second_sections = horizontal_to_vertical(horizontal)
        html = template.format(second_sections)
        sections.append(html)

    return "<html>\n<body>\n {} \t</body>\n</html>".format("\n".join(sections))


def md_to_jyyhtml(context: str, filepath: str, pre_temp: str):
    """
    将内容是Markdown的字符串转换成HTML, 并连同静态文件保存到对应路径下

    Args:
        context (str): 内容是Markdown的字符串
        filepath (str): 保存生成的一系列文件的路径
        pre_temp (str): 预处理好title和icon的HTML模板
    """
    # 先将整个Mardown切成多个水平幻灯片
    first_sectons = md_divide_to_horizontal(context)
    # first_sectons是多个secton块, 也就是多个html代码的列表

    # 为填充好内容的html字符串中的各个块插入对应的tag, 并拼接放入模板中
    page = pq(first_sectons)
    add_wrap(page)
    add_class(page)
    items = page("body").children()
    result = pre_temp.replace("{}", "\n".join([str(pq(e)) for e in items]))

    write(filepath, result)
    pass


def converter(MDfile, title, icon, output_foldpath):
    """
    转换器, 用于将Markdown文件转换成HTML文件(和其静态文件)
    Args:
        MDfile (str): 要转换的Markdown文件路径
        title (str): 转换出的HTML网页的title, 默认同文件名
        icon (str): 转换出的HTML网页的icon, 默认zweix的logo
        folder (str): 转换出的一系列文件放在文件夹`dist`中, 该参数指明dist目录保存位置
    """
    # 下面都是相关量的设置
    filename = os.path.basename(MDfile)
    filepath = os.path.abspath(MDfile)
    filepath_pre = filepath.split(filename)[0]
    output_filename = "index.html"  # 习惯
    if output_foldpath is None:
        output_foldpath = os.path.join(filepath_pre, "dist")
    else:
        output_foldpath = os.path.abspath(output_foldpath)

    # 将静态文件保存到路径下
    if os.path.exists(output_foldpath):
        shutil.rmtree(output_foldpath)
    os.mkdir(output_foldpath)
    shutil.copytree(
        os.path.join(os.getcwd(), "src", "static"),
        os.path.join(output_foldpath, "static"),
    )

    output_filepath = os.path.join(output_foldpath, output_filename)

    template_html = read(template_from)
    if title is None:
        title = ".".join(filename.split(".")[:-1])

    template_html = template_html.replace("{{title}}", title)

    if icon is None:
        icon = "./src/static/img/favicon.png"
        # icon = os.path.join(".", "src", "static", "img", "favicon.png")
    t = os.path.abspath(icon)
    shutil.copy(icon, os.path.join(output_foldpath, "static", "img", "favicon.png"))

    template_html = template_html.replace("{{icon}}", icon)

    context = read(filepath)

    md_to_jyyhtml(context, output_filepath, template_html)
