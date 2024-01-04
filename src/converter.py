import json
import os
import shutil

import yaml
from jinja2 import Template
from pyquery import PyQuery  # type: ignore

from src.util import *

from . import settings as st


def process_html_elements(before_html):
    temp_html = "<html><body>{}</body></html>".format(before_html)
    page = PyQuery(temp_html)
    e = page
    for item in e("h1").parent():
        t = PyQuery(item)
        t.wrap("<div style='width:100%'>")
        t.wrap("<div class='center middle'>")
    class_data = {
        "ul": "list-disc font-serif",
        "li": "ml-8",
        "h2": "text-xl mt-2 pb-2 font-sans",
        "h1": "text-2xl mt-2 font-sans",
        "p": "font-serif my-1",
        "pre": "bg-gray-100 overflow-x-auto rounded p-2 mb-2 mt-2",
        # "img": "center",  # 设置图片是否默认居中
    }
    for k, v in class_data.items():
        for item in e(k):
            t = PyQuery(item)
            t.add_class(v)
    page = e
    items = page("body").children()
    return "".join([str(PyQuery(e)) for e in items])


def process_terminal(semi_html):
    semi_html += st.author_template
    st.author_template = ""
    temp = "<div>" + semi_html + "</div>"
    semi_html = process_html_elements(temp)
    return semi_html


def vertical_to_fragment(vertical: str) -> str:
    fragments = vertical.split(st.op_index_fragment)

    fragment_list = [md_util.md_to_html(fragments[0])]
    template = "<div class='fragment' data-fragment-index='{}'>{}</div>"

    for i in range(1, len(fragments)):
        fragment_list.append(template.format(i, md_util.md_to_html(fragments[i])))

    return "".join(fragment_list)


def vertical_to_animate(vertical: str) -> str:
    animates = vertical.split(st.op_animate_section)

    animate_list = list()
    template = "{}"

    for i in range(len(animates)):
        animate_list.append(template.format(md_util.md_to_html(animates[i])))

    return "".join(animate_list)


def horizontal_to_vertical(horizontal: str) -> str:
    verticals_divided_by_second = horizontal.split(st.op_second_section)

    sections = list()
    template_second = "<section>{}</section>"

    for vertical_divided_by_second in verticals_divided_by_second:
        if vertical_divided_by_second.isspace():
            continue
        if st.op_animate_section in vertical_divided_by_second:
            verticals_divided_by_animate = vertical_divided_by_second.split(
                st.op_animate_section
            )
            template_animate = "<section data-auto-animate>{}</section>"
            for vertical_divided_by_animate in verticals_divided_by_animate:
                if vertical_divided_by_animate.isspace():
                    continue
                sections.append(
                    template_animate.format(
                        process_terminal(
                            vertical_to_animate(vertical_divided_by_animate)
                        )
                    )
                )
        elif st.op_index_fragment in vertical_divided_by_second:
            sections.append(
                template_second.format(
                    process_terminal(vertical_to_fragment(vertical_divided_by_second))
                )
            )
        else:
            sections.append(
                template_second.format(
                    process_terminal(md_util.md_to_html(vertical_divided_by_second))
                )
            )

    return "".join(sections)


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

    return "".join(sections)


def get_body(content):
    html_first_sections = md_divide_to_horizontal(content)
    return html_first_sections


def process_image_link():
    def func(link):
        new_name, err = file_util.get_image_to_target(
            link, st.filepath, st.images_foldpath
        )

        return (
            os.path.join(".", "static", st.images_foldname, new_name)
            if err is False
            else ""
        ), err

    st.content = md_util.process_images(st.content, func)


def process_front_matter():
    if st.op_front_matter not in st.content:
        st.author_template = ""
        return

    parts = st.content.split(st.op_front_matter)

    front_matter = parts[0]
    st.content = "".join(parts[1:])

    try:
        data = json.loads(front_matter)
    except Exception as e:
        data = yaml.load(front_matter, Loader=yaml.SafeLoader)

    for department in data["departments"]:
        new_name, err = file_util.get_image_to_target(
            department["img"], st.filepath, st.images_foldpath
        )
        if err is False:
            department["img"] = os.path.join(
                ".", "static", st.images_foldname, new_name
            )
        department["name"] = department["name"].replace(" ", "&#12288;")

    st.author_template = st.author_template.render(author=data["author"], departments=data["departments"])  # type: ignore


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
