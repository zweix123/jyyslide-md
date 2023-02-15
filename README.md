- [jyyslide-md](#jyyslide-md)
  - [Grammer](#grammer)
  - [Install](#install)
  - [Quickstart](#quickstart)
  - [Acknowledgement](#acknowledgement)
  - [Log](#log)


# jyyslide-md

一款通过Mardown方言生成[南大蒋炎岩老师的幻灯片](http://jyywiki.cn/OS/2022/slides/1.slides#/)主题的工具

## Grammer

+ 水平幻灯片使用`\n---\n`（三个）分割
+ 垂直幻灯片使用`\n----\n`（四个）分割
+ fragment使用`\n--\n`（两个）分割
    >更多样式见[reveal.js官网](https://revealjs.com/fragments/)
    >目前只支持次序出现，后续考虑通过`\n--x\n`的形式适配各种fragment

> 更多的`-`则是Mardown的`<br>`

+ Markdown原生语法适配：
    + 文字格式：
        + 加粗、斜体
        + 通过html实现删除线、高亮、标红
    + 注释
    + 列表
    + 代码和代码高亮
        >reveal-md和slidev支持的特定行高亮不支持
    + 引用
    + 数学公式
    + 表格（不够美观，后续修改）

## Install
>本项目使用Python3运行、使用poetry管理python虚拟环境，请确保本机有版本合适的Python和装有第三方Python库poetry。下面提供足够的使用方法，如果想进一步学习可尝试我的[poetry笔记](https://github.com/zweix123/CS-notes/blob/master/Programing-Language/Python/poetry.md)

1. 安装：`poetry install`

2. 使用：`poetry run python [file]`, 即为markdown文件生成对应的html文件（相同目录下）

## Quickstart

1. 安装：`poetry install`

+ win:
    ```bash
    poetry run python main.py .\test\slide.md
    ```
+ linux:
    ```bash
    poetry run python main.py ./test/slide.md
    ```
即可在`jyyslide-md/test/`目录下找到`slide.html`文件，打开查看效果

## Acknowledgement
+ 感谢[南京大学蒋炎岩老师](https://ics.nju.edu.cn/~jyy/)录制了如此优质的[操作系统课程](https://jyywiki.cn/)
+ 感谢[顾若水](https://github.com/ruoshui255)提供的模板

## Log

+ [ ] 完善对fragment支持的相关语句
+ [ ] 实现淡入淡出动画
+ [ ] 实现自动导出成完毕的网页