# jyyslide-md

一款通过简单的Mardown方言生成类似[南大蒋炎岩老师的幻灯片](http://jyywiki.cn/OS/2022/slides/1.slides#/)的工具。

## Grammer
总览效果见[样例](#Quickstart)
>互联网有多种构建网页幻灯片的框架，基本都有自己的Markdown方言，不过有一些习惯上的用法可循，jyyslide-md尽可能遵循这种习惯。
>功能上的设计从幻灯片的应用场景出发，在使用尽可能少的语法情况下提供尽可能足够的功能。

+ 水平幻灯片使用`\n---\n`（三个）分割
+ 垂直幻灯片使用`\n----\n`（四个）分割
+ 具有`data-fragment-index`属性的Fragments使用`\n<!-- -->\n`分割
  + 语法对标`reveal-md`同时后续可能开发支持其他属性Fragments
  + 具体分割方式是从分割符到下一个分隔符或者本张幻灯片末尾的位置
  + 更多样式见[reveal.js官网对Fragments的解释](https://revealjs.com/fragments/)
<!-- + 渐变动画使用`\n<--[.?]-->\n`作为标记 -->
  <!-- >上面的fragment是依次出现，之前的不会消失，如果我们想一个个交替出现形成动画呢？ -->
  <!-- + 具体格式：`folderpath, "style"` -->
  <!-- + 限制：只支持图片且这样的tag只能放在一张幻灯片的末尾且和fragment冲突 -->

---

+ 对Markdown原生语法适配情况：
    + 文字格式：
        + 通过Markdown原生语法支持加粗、斜体
        + 通过插入html支持删除线、高亮、标红
    + 支持注释
    + 支持列表
    + 支持代码和代码高亮
        >reveal-md和slidev支持的代码特定行高亮和有序高亮不支持
    + 支持引用（链接和图片）
    + 支持数学公式
    + 支持表格（但蒋老师提供的CSS没有对表格的美化，所以建议不使用）


## Install
>本项目使用Python3开发，使用第三方库poetry进行库管理，请用户确保本机有**版本**合适的Python并装有poetry，下面提供足够的使用方法，如果像相对系统的学习，可尝试我的[poetry笔记](https://github.com/zweix123/CS-notes/blob/master/Programing-Language/Python/poetry.md)

0. 下载项目并进入项目根目录
1. 安装第三方库：`poetry install`

## Use

+ python/poetry的使用，有两种使用方式
  + 以`python3 -m poetry run python main.py`为前缀使用命令
  + 进入虚拟环境`python3 -m poetry shell`, 然后通过前缀`python main.py`为前缀使用命令

+ 命令解释：添加flag`--help`查看细节


## Quickstart

[下载后](#Install)运行命令
```
python3 -m poetry run python main.py test/slide.md
```

即可在`test/dist`目录下找到完整网页目录

## Develop
```
.
|----main.py: 项目入口, 主要是命令行配置
|----src
      |----settings.py: 配置信息，包括项目静态资源和设置的语法关键字
      |----lib.py: 包含一些辅助性函数
      ·----converter.py: 项目核心
```
程序中有大量的注释

## Acknowledgement
+ 感谢[南京大学蒋炎岩老师](https://ics.nju.edu.cn/~jyy/)录制了如此优质的[操作系统课程](https://jyywiki.cn/)
+ 感谢[顾若水](https://github.com/ruoshui255)提供的模板