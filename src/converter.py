import os, re, json, shutil

from pyquery import PyQuery as pq
from jinja2 import Template

from . import settings as st
from src.util import *


def vertical_to_fragment(vertical: str) -> str:
    fragments = vertical.split(st.op_index_fragment)

    fragment_list = [md_util.md_to_html(fragments[0])]
    template = "<div class='fragment' data-fragment-index='{}'>{}</div>"

    for i in range(1, len(fragments)):
        fragment_list.append(template.format(i - 1, md_util.md_to_html(fragments[i])))

    return "\n".join(fragment_list)


def process_vertical(vertical: str) -> str:
    unit = str()
    if st.op_index_fragment in vertical:
        unit = vertical_to_fragment(vertical)
    else:
        unit = md_util.md_to_html(vertical)
    unit += st.author_template
    st.author_template = ""
    return unit


def horizontal_to_vertical(horizontal: str) -> str:
    verticals = horizontal.split(st.op_second_section)

    sections = list()
    template = "<section>{}</section>"

    for vertical in verticals:
        if vertical.isspace():
            continue
        fragmetns = process_vertical(vertical)
        html = template.format(fragmetns)
        sections.append(html)

    return "\n".join(sections)


def md_divide_to_horizontal(content: str):
    horizontals = content.split(st.op_first_section)

    sections = list()
    template = "<section>{}</section>"

    for horizontal in horizontals:
        if horizontal.isspace():
            continue
        html_second_sections = horizontal_to_vertical(horizontal)

        html = template.format(html_second_sections)
        sections.append(html)

    return "\n".join(sections)


def process_html_elements(e):
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


def get_body(content):
    html_first_sections = md_divide_to_horizontal(content)
    pre_html = "<html><body>{}</body></html>".format(html_first_sections)

    page = pq(pre_html)
    process_html_elements(page)

    items = page("body").children()
    return "\n".join([str(pq(e)) for e in items])


def process_image_link():
    def func(link):
        return os.path.join(
            st.images_foldpath,
            file_util.get_image_to_target(link, st.filepath, st.images_foldpath),
        )

    st.content = md_util.process_images(st.content, func)


def process_front_matter():
    if st.op_front_matter not in st.content:
        return

    parts = st.content.split(st.op_front_matter)

    front_matter = parts[0]
    st.content = "".join(parts[1:])

    data = json.loads(front_matter)

    for department in data["departments"]:
        department["img_url"] = os.path.join(
            st.images_foldpath,
            file_util.get_image_to_target(
                department["img_url"], st.filepath, st.images_foldpath
            ),
        )

    st.author_template = st.author_template.render(
        author=data["author"], departments=data["departments"]
    )


def process_static():
    if os.path.exists(st.output_foldpath) is True:
        shutil.rmtree(st.output_foldpath)
    os.mkdir(st.output_foldpath)
    shutil.copytree(st.static_path, st.static_foldpath)


def converter(MDfilepath):
    st.Init(MDfilepath)
    process_static()

    st.template = Template(file_util.read(st.template_from))
    st.author_template = Template(file_util.read(st.authortemp_from))

    st.content = file_util.read(st.filepath)
    process_front_matter()  # 解析markdown中的front_matter and render author_template(will change content)
    process_image_link()  # 处理Markdown文本中的图片链接, 将它们get到静态文件, 同时修改content

    st.title = "".join(st.filename.split(".")[:-1])
    st.body = get_body(st.content)

    st.template = st.template.render(title=st.title, body=st.body)
    file_util.write(st.output_filepath, st.template)
