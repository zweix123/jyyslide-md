```
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
```