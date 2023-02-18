import re
from src.settings import *

op_animate_pattern = "(?<=A).*?(?=B)"

s = """
A3123123B
## Grammer
总览效果见[样例](#Quickstart)
>互联网有多种构建网页幻灯片的框架，基本都有自己的Markdown方言，不过有一些习惯上的用法可循，jyyslide-md尽可能遵循这种习惯。
>功能上的设计从幻灯片的应用场景出发，在使用尽可能少的语法情况下提供尽可能足够的功能。

+ 水平幻灯片使用`\n---\n`（三个）分割
+ 垂直幻灯片使用`\n----\n`（四个）分割
+ 具有`data-fragment-index`属
<--[./illustrations]-->
<--./illustrations-->
dada
"""
print(op_animate_pattern)
print(s)

t = re.match(op_animate_pattern, s)

print(t)
