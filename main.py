#! /usr/bin/python3
# coding=utf-8

import os
import chardet
import xml.etree.ElementTree as etree
from pyquery import PyQuery as pq
import markdown
from markdown import Extension
from markdown.blockprocessors import BlockProcessor

# settings
template_html = str()
template_html_from = "./static/template/template_c.html"


# infrastructure
def get_file_code(file_path):  # 检测文件编码格式, 效率较低
    res = str()
    with open(file_path, "rb") as f:
        res = chardet.detect(f.read())["encoding"]
    return res


def read(filepath):  # 读取文本文件内容
    if os.path.exists(filepath):
        with open(filepath, "r", encoding=get_file_code(filepath)) as f:
            content = f.read()
            return content
    else:
        print("{} is not exists".format(filepath))
        exit(-1)


def write(filepath, data):  # 向文本文件(覆)写入内容
    # with open(filepath, "wb") as f:
    #     f.write(b"Hello World!")
    # with open(filepath, "w", encoding=get_file_code(filepath)) as f:
    #     f.write(data)
    with open(filepath, "w", encoding="UTF-8") as f:
        f.write(data)


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
    fragment_sep = "\n--\n"
    fragments = vertical.split(fragment_sep)

    template = "<div class='fragment' data-fragment-index='{}'> {} </div>"
    fragment_list = [md_to_html(fragments[0])]

    for i in range(1, len(fragments)):
        fragment_list.append(template.format(i - 1, md_to_html(fragments[i])))

    return "\n".join(fragment_list)


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


def md_to_jyyhtml(context: str, filepath):
    subject = md_divide_to_horizontal(context)

    page = pq(subject)
    add_wrap(page)
    add_class(page)

    items = page("body").children()

    global template_html
    template = template_html
    sections = "\n".join([str(pq(e)) for e in items])

    result = template.replace("{}", sections)
    write(filepath, result)
    pass


def process(file="./slide.md"):
    filename = os.path.basename(file)
    filepath = os.path.abspath(file)
    output_filename = os.path.splitext(filename)[0] + ".html"
    output_foldpath = filepath.split(filename)[0]
    output_filepath = os.path.join(output_foldpath, output_filename)

    global template_html
    template_html = read(template_html_from)
    title = ".".join(filename.split(".")[:-1])
    template_html = template_html.replace("{{title}}", title)

    context = read(filepath)
    md_to_jyyhtml(context, output_filepath)
    pass


if __name__ == "__main__":
    # process()
    import sys

    for file in sys.argv[1:]:
        print("working in {}".format(file), end=" ")
        process(file)
        print(" done")
    pass
