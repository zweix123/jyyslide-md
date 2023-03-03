from urllib.parse import urlparse


import markdown
from markdown import Extension
from markdown.blockprocessors import BlockProcessor

import xml.etree.ElementTree as etree

# 分辨URL和路径: 判断一个字符串是否为URL
def is_url(string):
    result = urlparse(string)
    return all([result.scheme, result.netloc])


# 分辨URL和路径: 判断一个字符串是否为路径
def is_path(string):
    result = urlparse(string)
    return not all([result.scheme, result.netloc])

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
