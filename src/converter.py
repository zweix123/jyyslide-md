# 自下向上看
"""
算法比较简单
jyy的模板中, class为"slide"的div下, 
每个section都是一个水平幻灯片
每个水平幻灯片下的每个section都是垂直幻灯片 
"""
import os, shutil, re, json
from pyquery import PyQuery as pq
from jinja2 import Template
from src.settings import *
from src.util import *


def vertical_to_animate(vertical: str) -> str:
    folderpath = r"D:\Workspace\jyyslide-md\test\illustrations_queue"
    imgs = file_util.get_files_under_folder(
        folderpath, "jpg"
    ) + file_util.get_files_under_folder(folderpath, "png")
    animate_list = list()
    template = "<section data-auto-animate>{}</section>"
    for img in imgs:
        md = "![]({})".format(img)
        html = md_util.md_to_html(md)
        tmp = template.format(html)
        animate_list.append(tmp)

    return "\n".join(animate_list)


def vertical_to_fragment(vertical: str) -> str:
    fragments = vertical.split(op_index_fragment)

    fragment_list = [md_util.md_to_html(fragments[0])]
    template = "<div class='fragment' data-fragment-index='{}'> {} </div>"

    for i in range(1, len(fragments)):
        fragment_list.append(template.format(i - 1, md_util.md_to_html(fragments[i])))

    return "\n".join(fragment_list)


def process_vertical(vertical: str) -> str:
    if op_index_fragment in vertical:
        return vertical_to_fragment(vertical)
    else:
        if "[[]]" in vertical:
            return vertical_to_animate(vertical)
        else:
            return md_util.md_to_html(vertical)
        # if re.match(op_animate_pattern, vertical) is None:
        #     return md_to_html(vertical)
        # else:
        #     return vertical_to_animate(vertical)


first = True
auther = str()


def horizontal_to_vertical(horizontal: str) -> str:
    verticals = horizontal.split(op_second_section)

    sections = list()
    template = "\n<section>\n {} </section>"
    if len(verticals) == 1:  # 没有垂直幻灯片
        template = "{}"

    for vertical in verticals:
        if vertical.isspace():
            continue
        fragmetns = process_vertical(vertical)
        html = template.format(fragmetns)
        global first
        if first:
            html += auther
            first = False

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
    # 给标题添加属性
    for item in e("h1").parent():
        t = pq(item)
        t.wrap("<div style='width:100%'>")
        t.wrap("<div class='center middle'>")
    # 为各个属性插入tag
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
    # 插入到一个完整的HTML中
    pre_html = "<html>\n<body>\n{}\n</body>\n</html>".format(html_first_sections)

    # 为处理好的HTML中的各个元素插入对应的tag
    page = pq(pre_html)
    process_html_eles(page)
    # 拼接起来
    items = page("body").children()
    temp = "\n".join([str(pq(e)) for e in items])
    # 放到模板中
    result = pre_temp.replace("{}", temp)

    file_util.write(filepath, result)


def front_matter(content):
    match = re.search(op_front_matter, content, flags=re.MULTILINE)
    if match is None:
        return

    parts = re.split(op_front_matter, content, maxsplit=1, flags=re.MULTILINE)
    head = parts[0].strip()
    content = parts[1].strip()

    return json.loads(head), content


def converter(filepath):
    filename = os.path.basename(filepath)
    filepath = os.path.abspath(filepath)
    output_filename = "index.html"  # 习惯
    output_foldpath = os.path.join(filepath.split(filename)[0], "dist")
    output_filepath = os.path.join(output_foldpath, output_filename)

    # 转移静态文件
    if os.path.exists(output_foldpath):
        shutil.rmtree(output_foldpath)
    os.mkdir(output_foldpath)
    shutil.copytree(static_path, os.path.join(output_foldpath, "static"))

    # 预处理模板
    template_html = file_util.read(template_from)
    title = "".join(filename.split(".")[:-1])
    template_html = template_html.replace("{{ title }}", title)

    context = file_util.read(filepath)
    context = md_util.move_image(
        context, filepath, os.path.join(output_foldpath, "static", "img")
    )
    data, context = front_matter(context)
    # print(json.dumps(data["author"], sort_keys=True, indent=4, separators=(',', ':')))
    # print(json.dumps(data["departments"], sort_keys=True, indent=4, separators=(',', ':')))
    auther_template = Template(file_util.read(authortemp_from))
    auther_template = auther_template.render(
        author=data["author"], departments=data["departments"]
    )

    global auther
    auther = auther_template

    md_to_jyyhtml(context, output_filepath, template_html)
