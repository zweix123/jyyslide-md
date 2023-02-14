一个通过Mardown方言生成像[这样的幻灯片](http://jyywiki.cn/OS/2022/slides/1.slides#/)的工具

## Grammer
+ 水平幻灯片使用`\n---\n`（三个）分割
+ 垂直幻灯片使用`\n----\n`（四个）分割
+ fragment使用`\n--\n`（两个）分割
    >更多样式见[reveal.js官网](https://revealjs.com/fragments/)
    >其实又想通过`\n--x\n`的形式适配各种fragment，但是后来发现没有必要

> 更多的`-`则是Mardown的`<br>`

+ Markdown原生语法适配：
    + 注释
    + 列表
    + 代码和代码高亮
        >reveal-md和slidev支持的特定行高亮不支持
    + 引用
    + 数学公式
    + 表格（不够美观，后续修改）

## Install

>需要使用Python3和Python3虚拟环境管理库poetry

+ 安装：`poetry install`

+ 使用：`poetry run python [${file}]`, 即为markdown文件生成对应的html文件（相同目录下）

## Quickstart

安装后在项目目录下运行：
+ win:
    ```bash
    poetry run python main.py .\test\slide.md
    ```
+ linux:
    ```bash
    poetry run python main.py ./test/slide.md
    ```

## 鸣谢
+ 感谢[南京大学蒋炎岩老师](https://ics.nju.edu.cn/~jyy/)录制了如此优质的[操作系统课程](https://jyywiki.cn/)
+ 感谢[顾若水](https://github.com/ruoshui255)提供的模板