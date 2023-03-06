# jyyslide-md

一款通过简约的Mardown方言生成具有[南大蒋炎岩老师幻灯片](http://jyywiki.cn/OS/2022/slides/1.slides#/)风格的工具  
准确的说应该是一款Reveal.js的定制化前端框架。

[Background](#background) | [Install](#install) | [Usage](#usage) | [Grammer](#grammer) | [Example](#example) | [Acknowledgement](#acknowledgement) | [License](#license)

## Background
>可以从奥卡姆剃刀（如无必要，勿增实体）的角度考虑我开发本项目的发心。

说起幻灯片，首先想到的是微软的PowerPoint，PPT几乎成了幻灯片的代名词。但是在使用过程中我们会发现，它提供的很多的功能，为了使用这些功能需要很高的学习成本，但大多数场景我们用不到这么多功能；同时在使用别人的PPT模板是因为我们对功能的不熟练而不能展现模板PPT的全部效果。在幻灯片领域有类似Markdown之于Word的框架嘛？

除了能量点这样的制作幻灯片的软件外，还有基于Web的幻灯片，我基本都[尝试](https://github.com/zweix123/CS-notes/blob/master/Missing-Semester/slide.md)了一下。但是并没有完全满足我的要求的。

[南京大学蒋炎岩老师](https://ics.nju.edu.cn/~jyy)开源了他的[操作系统课程](https://space.bilibili.com/202224425)，相信上过他的课的同学除了会被他深入浅出的授课所折服外，也一定对他的幻灯片感兴趣。他的幻灯片是基于[Reveal.js](https://revealjs.com/)这款Web幻灯片框架，但不清楚他具体是如何制作的，在经过他的同意下，我制作了这个将Markdown方言转换成和他一个风格的幻灯片的工具。

对于Markdown扩展语法的设计尽可能简单，有些功能不是不能提供，但是提供会导致语法没有性价比的扩张，所以舍弃。让设计尽可能足够且简约。

## Install

本项目使用Python开发，模块管理使用Poetry，请确保您的机器上有版本足够的Python（3.10以上）并安装有第三方模块Poetry，同时也得益于Python，本项目应该可以运行于任何系统上。
>关于Poetry可参考我的[笔记](https://github.com/zweix123/CS-notes/blob/master/Programing-Language/Python/poetry.md)，当然下面会提供足够的用法。

1. 克隆项目到本地并进入：
    ```bash
    git clone https://github.com/zweix123/jyyslide-md.git
    cd jyyslide-md
    ```
2. 利用Poetry下载第三方模块
    ```bash
    python3 -m poetry install
    # 或者 poetry install
    ```

>在windows下可能出现编码问题：`控制面板` -> `区域` -> `管理` -> `更改系统区域设置` -> 打开`Beta版`

## Usage
>请确保已经[Install](#install)好了

+ 使用Peotry管理的Python有两种运行方式
  1. 进入虚拟环境：
      ```bash
      python3 -m poetry shell
      # 或者 poetry shell
      ```
      之后就可以正常的运行Python代码了
  2. 使用前缀：在运行Python代码的命令前添加`python3 -m poetry run`（或者`poetry run`）

命令格式如下
```bash
python main.py [Markdown文件]
```
在Markdown文件同级目录会出现一个`dist`文件夹，其下有一个index.html文件和一个static文件夹，前者即为生成的“Web幻灯片，static即为其相关静态文件。网页的title和Markdown文件同名、icon即为`static/img/favicon.png`，可通过替换这个文件修改icon。

+ PDF Export: [Manual](https://revealjs.com/pdf-export/)

### Grammer
>在[例子](#example)的Intro中的幻灯片有更形象的说明

+ 水平幻灯片使用`\n---\n`（三个）分割
+ 垂直幻灯片使用`\n----\n`（四个）分割
+ 渐变垂直幻灯片使用`\n++++\n`(四个)分割
+ 在同一张幻灯片中依次出现的部分使用`\n--\n`(两个)分割
  + 具体分割方式是从分割符到下一个分隔符或者本张幻灯片末尾的位置
  + 更多样式见[reveal.js官网对Fragments的解释](https://revealjs.com/fragments/)
+ 作者信息使用`\n+++++\n`(五个)和正文分割，使用Json格式   
  这里主要指指的是这部分  
  ![](./img/author.png)  
  因为这部分是多个文字、图片、链接为一体，如果使用扩展Markdown语法的设置会让语法很凌乱。  
  实际上这样的页面只在第一页出现，即使不使用这样的语法，使用这样的形式  
  ```
  # Title

  >author
  ```
  ![](./img/example_of_author.png)  
  也能够实现差不多的意思，所以从设计上将这部分从主题抽离出来  
  这部分的格式如下，
  >在[例子](#example)中的jyy中的Markdown文件
  ```
  {
      "author": {
          "name": "蒋炎岩",
          "url": "https://ics.nju.edu.cn/~jyy/"
      },
      "departments": [
          {
              "name": "  南京大学  ",
              "url": "https://www.nju.edu.cn/main.htm",
              "img_url": "./img/nju-logo.jpg"
          },
          {
              "name": "计算机科学与技术系",
              "url": "https://cs.nju.edu.cn/main.htm",
              "img_url": "./img/njucs-logo.jpg"
          },
          {
              "name": "计算机软件研究所",
              "url": "https://www.nju.edu.cn/main.htm",
              "img_url": "./img/ics-logo.png"
          }
      ]
  }
  ```

---

+ 对Markdown原生语法适配情况：
  >这里使用的Markdown语法使用的是**严格**语法。
    + 文字格式：
        + 通过Markdown原生语法支持**加粗**、*斜体*
        + 通过插入html支持<del>删除线</del>、<mark>高亮</mark>、<red>标红</red>
    + 支持注释
    + 支持列表
    + 支持代码和代码高亮
        >Reveal-md和Slidev支持的代码特定行高亮暂时不支持
    + 支持引用（链接和图片），图片推荐以插入HTML的方式使用
      ```html
      <img src="图片地址">
      ```
      这里的src支持URL，相对地址和绝对地址，程序会将其down或者copy到dist下的img中
      >这里使用的爬虫是非常简单的爬虫，建议自己下载到本地使用。
      
      + 图片居中：
          ```html
          <img class="float-right" src="图片地址">
          ```
      + 图片右对齐：
          ```html
          <img class="float-right" src="图片地址">
          ```
          Markdown中的格式是流的形式，即图片是占位的，这里默认左对齐和居中的图片都是占位的，但是右对齐的图片不居中
      其他格式调整SFTW
    + 支持数学公式
    + 支持表格
    + 关于Markdown的这个语法：大于三个的`-`是分割线`<hr>`，我们发现这和扩展语法冲突，所以这里是大于四个的`-`是分割线，且这里的分割线在HTML中是空行的效果

---

蒋老师有而未设置专门语法的部分
+ 多个幻灯片并列
  ```
  <center>
  <img class="inline" ...>
  <img class="inline" ...>
  <img class="inline" ...>
  </center>
  ```
  如果你想，你可以直接在Markdown中插入类似上面的代码

+ 插入B站

## Example

+ `test/jyy/操作系统概述.md`即为蒋老师2022年的第一节课
  ```bash
  python main.py test\jyy\操作系统概述.md
  ```
  打开`test\jyy\dist\index.html`即可查看

+ `test/Intro/slide.md`即为本项目介绍的幻灯片
  ```bash
  python main.py test\Intro\slide.md
  ```
  打开`test\Intro\dist\index.html`即可查看

## Acknowledgement
+ 感谢[南京大学蒋炎岩老师](https://ics.nju.edu.cn/~jyy/)录制了如此优质的[操作系统课程](https://jyywiki.cn/)
+ 感谢[顾若水](https://github.com/ruoshui255)大佬提供的[思路和大量代码](./src/backup/rouv/ruoshui255.md.py)
+ 感谢[Jungle](https://github.com/Jungle430)对编码问题的提醒

## License

[MIT](LICENSE) © Richard Littauer
