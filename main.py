#! /usr/bin/python3
# pip3 install pyquery Markdown

import os
import sys
import xml.etree.ElementTree as etree


def run_help():
    txt = """
Usage: python3 md.py demo.md
request: pip3 install markdown pyquery  pygments

一些自定义解释标记
https://revealjs.com/fragments/
2个横线(--)  表示 fragment
3个横线(---) 表示 section
4个横线(----) 表示 vertical slides
5个横线以上 md 默认展示方式 <hr>
    
"""
    print(txt)
    exit(0)


try:
    from pyquery import PyQuery as pq
    import markdown
    from markdown import Extension
    from markdown.blockprocessors import BlockProcessor
except ImportError:
    run_help()


output_folder = "."

template_html = 


def write(data, filename):
    file = os.path.join(output_folder, filename)
    print("output name <{}>".format(file))

    with open(file, 'w+', encoding="utf-8") as f:
        s = f.write(data)


def get(filename):
    if os.path.exists(filename):
        with open(filename, 'r', encoding="utf-8") as f:
            s = f.read()
            return s
    else:
        print("{} not exist".format(filename))
        exit(-1)


def add_wrap(e):
    items = e('h1').parent()
    # items = e('h1')

    print("h1 {}".format(len(items)))
    for item in items:
        t = pq(item)
        t.wrap("<div style='width:100%'>")
        t.wrap("<div class='center middle'>")


class_data = {
    'ul': " list-disc font-serif",
    'li': " ml-8",
    "h2": " text-xl mt-2 pb-2 font-sans",
    "h1": " text-2xl mt-2 font-sans",
    "p": " font-serif my-1",
    "pre": " bg-gray-100 overflow-x-auto rounded p-2 mb-2 mt-2"
}


def add_class(e):
    for k, v in class_data.items():
        items = e(k)
        for item in items:
            t = pq(item)
            t.add_class(v)


def gen_html(md_html: str, output):
    # print(md_html)
    page = pq(md_html)
    add_wrap(page)
    add_class(page)

    items = page('body').children()
    print("div {}".format(len(items)))

    template = template_html
    sections = "\n".join([str(pq(e)) for e in items])
    res = template.replace("{}", sections)
    # res = template.replace("{}", str(e))

    write(res, output)


class BoxBlockProcessor(BlockProcessor):
    first = True

    def test(self, parent, block):
        return self.first

    def run(self, parent, blocks):
        if self.first:
            self.first = False

            e = etree.SubElement(parent, 'div')
            # e.set('style', 'display: inline-block; border: 1px solid red;')
            self.parser.parseBlocks(e, blocks)
            # remove used blocks
            for i in range(0, len(blocks)):
                blocks.pop(0)
            return True  # or could have had no return statement
        return False  # equivalent to our test() routine returning False


class BoxExtension(Extension):
    def extendMarkdown(self, md):
        md.parser.blockprocessors.register(BoxBlockProcessor(md.parser), 'box', 175)


def md_to_html(md: str) -> str:
    extensions = [
        BoxExtension(),
        'meta', 'fenced_code', "codehilite", 'attr_list'
    ]
    # html = markdown.markdown(text, extensions=[MyExtension()])
    res = markdown.markdown(md, extensions=extensions)
    return res


def print_list(identifier: str, lst: list):
    for t in lst:
        print("\n{}".format(identifier))
        print(t)
        print("{}".format(identifier))


def md_to_fragment(section: str):
    """
    2个横线
    class="fragment" data-fragment-index="2
    """

    fragment_delimiter = "\n--\n"
    fragments = section.split(fragment_delimiter)

    res = [md_to_html(fragments[0])]

    template = "<div class='fragment' data-fragment-index='{}'> {} </div>"
    for i in range(1, len(fragments)):
        t = template.format(i - 1, md_to_html(fragments[i]))
        res.append(t)
    return "\n".join(res)


def md_to_vertical_section(vertical_md: str) -> str:
    """
    4个横线
    表示section
    """
    md_delimiter = "\n----\n"
    vertical_sections = vertical_md.split(md_delimiter)

    template = "\n<section> {} </section>"
    if len(vertical_sections) == 1:
        template = "{}"

    section = []
    for t in vertical_sections:
        fragments = md_to_fragment(t)
        html = template.format(fragments)
        section.append(html)
    # print_list("--- section ---", section)

    res = "\n".join(section)
    return res


def md_parse(md: str, output_file):
    """
    3个横线
    表示 大 section

    5个横线
    表示 <hr>

    """
    big_section_delimiter = "\n---\n"
    mds = md.split(big_section_delimiter)
    print("mds[0] <{}>".format(mds[0]))

    sections = []
    template = "<section>\n {} \n</section>"
    for t in mds:
        if t.isspace():
            continue
        s = md_to_vertical_section(t)
        html = template.format(s)
        sections.append(html)
    # print_list("*** big sections ***", sections)

    # pq needs a parent
    md_html = "<html><body>{}</body></html>".format("\n".join(sections))
    gen_html(md_html, output_file)


def main():
    # if len(sys.argv) == 1:
    #     run_help()
    #     print("no input file")
    #     exit(0)
    #
    # print(sys.argv)
    # file = sys.argv[1]
    # # data = get(file)
    #
    #
    # name = file.split("/")[-1].split(".", 1)[0]
    # if not name:
    #     name = file.split("\\")[-1].split(".", 1)[0]
    # print(f'name {name}')
    #
    # output_filename = "{}.html".format(name)

    data = demo
    output_filename = "demo.html"

    md_parse(data, output_filename)


if __name__ == '__main__':
    main()
