import os, uuid, shutil, re

import markdown
from markdown import Extension
from markdown.blockprocessors import BlockProcessor

import xml.etree.ElementTree as etree

from src.util import str_util, net_util


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


def move_image(content, input_filepath, output_foldpath):
    def modify(match):
        tar = match.group()

        pre, mid, suf = str(), str(), str()  # 链接图片的代码, pre和suf是其他部分, mid是路径部分
        if tar[-1] == ")":
            pre = tar[: tar.index("(") + 1]
            mid = tar[tar.index("(") + 1 : -1]
            suf = tar[-1]
        else:
            pre = tar[: tar.index('"') + 1]
            tar = tar[tar.index('"') + 1 :]  # 转换一下, 并不是要使用
            mid = tar[: tar.index('"')]
            suf = tar[tar.index('"') :]

        name = uuid.uuid4().hex

        img_new_abspath = os.path.join(
            output_foldpath,
            name + "." + mid.split(".")[-1],
        )

        if str_util.is_url(mid):
            net_util.down(mid, img_new_abspath)
        else:
            mid_abspath = os.path.normpath(
                os.path.join(os.path.dirname(input_filepath), mid)
            )
            shutil.copy(mid_abspath, img_new_abspath)

        mid_new = os.path.join(".", "static", "img", name + "." + mid.split(".")[-1])

        return pre + mid_new + suf

    patten = r"!\[.*?\]\((.*?)\)|<img.*?src=[\'\"](.*?)[\'\"].*?>"
    return re.sub(patten, modify, content)
