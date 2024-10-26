# unit test for function process_front_matter
# process_front_matter input is st.content
# process_front_matter output is st.author_template


import os
import sys
import unittest

from jinja2 import Template  # lib used in converter.py

# add project root to sys.path, otherwise, the import below will fail
sys.path = [os.environ["JYYSLICE_MD_PATH"]] + sys.path


import src.settings as st
from src.converter import process_front_matter

# 这里没有使用项目中的template, 而是针对其使用的模版变量专门测试
#! 假如未来模版内容修改, 当前单元测试无法感知, 导致作为回归测试的话会落后版本
AUTHOR_TEMPLATE_STRING = """
{{ author.name }}
{{ author.url }}
{% for department in departments %}
    {{ department.name }}
    {{ department.url }}
    {{ department.img }}
{% endfor %}
"""


class TestProcessFrontMatter(unittest.TestCase):
    def single_test(self, input: str, output: str):
        """
        单次测试
        Args:
            input (str): 要测试的markdown头
            output (str): 要测试的头部分的输出
        """
        st.content = input
        st.author_template = Template(AUTHOR_TEMPLATE_STRING)  # init st.author_template
        process_front_matter()
        self.assertEqual(st.author_template, output)

    def test_not_front_matter(self):
        self.single_test("", "")

    def test_common_json(self):
        author_info_md = (
            """{
    "author": {
        "name": "蒋炎岩",
        "url": "https://ics.nju.edu.cn/~jyy/"
    },
    "departments": [
        {
            "name": "  南京大学  ",
            "url": "https://www.nju.edu.cn/main.htm",
            "img": "./img/nju-logo.jpg"
        },
        {
            "name": "计算机科学与技术系",
            "url": "https://cs.nju.edu.cn/main.htm",
            "img": "./img/njucs-logo.jpg"
        },
        {
            "name": "计算机软件研究所",
            "url": "https://www.nju.edu.cn/main.htm",
            "img": "./img/ics-logo.png"
        }
    ]
}"""
            + st.op_front_matter
        )
        expected_output = """
蒋炎岩
https://ics.nju.edu.cn/~jyy/

    &#12288;&#12288;南京大学&#12288;&#12288;
    https://www.nju.edu.cn/main.htm
    ./img/nju-logo.jpg

    计算机科学与技术系
    https://cs.nju.edu.cn/main.htm
    ./img/njucs-logo.jpg

    计算机软件研究所
    https://www.nju.edu.cn/main.htm
    ./img/ics-logo.png
"""

        self.single_test(author_info_md, expected_output)

    def test_common_yaml(self):
        author_info_md = (
            """author:
    name: 蒋炎岩
    url: https://ics.nju.edu.cn/~jyy/

departments:
    - name: "  南京大学  "
      url: https://www.nju.edu.cn/main.htm,
      img: ./img/nju-logo.jpg

    - name: 计算机科学与技术系
      url: https://cs.nju.edu.cn/main.htm,
      img: ./img/njucs-logo.jpg

    - name: 计算机软件研究所
      url: https://www.nju.edu.cn/main.htm,
      img: ./img/ics-logo.png"""
            + st.op_front_matter
        )
        expected_output = """
蒋炎岩
https://ics.nju.edu.cn/~jyy/

    &#12288;&#12288;南京大学&#12288;&#12288;
    https://www.nju.edu.cn/main.htm,
    ./img/nju-logo.jpg

    计算机科学与技术系
    https://cs.nju.edu.cn/main.htm,
    ./img/njucs-logo.jpg

    计算机软件研究所
    https://www.nju.edu.cn/main.htm,
    ./img/ics-logo.png
"""

        self.single_test(author_info_md, expected_output)


if __name__ == "__main__":
    unittest.main()
