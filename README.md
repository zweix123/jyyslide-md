# jyyslide-md

❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗

该项目目前有一些亟需优化的地方，我已经有了方案，但是由于工作，暂时没有精力实现，请同好们敬请期待。
1. 支持通过`pip`下载并通过命令使用
    >并不是所有人都了解Python、Poetry
2. 命令支持检测文件修改并自动编译（甚至自动刷新浏览器）
    >就像前端相关命令一样自然
3. 优化架构，初版开发个人的软件工程水平一般（当前现在也一般但是有一定提高）
4. 拓展**渐变垂直幻灯片**的功能，用户常用渐变实现一张幻灯片的不同部分的先后出现，但是目前需要将不同部分作为多个页，很麻烦
5. 开发VSCode的插件
    >就像上面说的，并不是所有人都了解命令行

❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗❗

一款通过简约的Mardown方言生成具有[南大蒋炎岩老师幻灯片](http://jyywiki.cn/OS/2022/slides/1.slides#/)风格的Web幻灯片转换工具  
准确的说是一款基于Reveal.js的定制主题Web幻灯片框架（类似reveal-md，不过定制主题和蒋老师的一样）。

[Background](#background) | [Install](#install) | [Usage](#usage) | [Grammer](#grammer) | [Example](#example) | [Develop](#develop) | [Acknowledgement](#acknowledgement) | [License](#license)

## Background
>可以从奥卡姆剃刀（如无必要，勿增实体）的角度考虑我开发本项目的发心。

说起幻灯片，首先想到的是微软的PowerPoint，PPT几乎成了幻灯片的代名词。但是在使用过程中我们会发现，它提供的很多的功能，为了使用这些功能需要很高的学习成本，但大多数场景我们用不到这么多功能；同时在使用别人的PPT模板是因为我们对功能的不熟练而不能展现模板PPT的全部效果。在幻灯片领域有类似Markdown之于Word的框架嘛？

除了能量点这样的制作幻灯片的软件外，还有基于Web的幻灯片，我基本都[尝试](https://github.com/zweix123/CS-notes/blob/master/Missing-Semester/slide.md)了一下。但是并没有完全满足我的要求的。

[南京大学蒋炎岩老师](https://ics.nju.edu.cn/~jyy)开源了他的[操作系统课程](https://space.bilibili.com/202224425)，相信上过他的课的同学除了会被他深入浅出的授课所折服外，也一定对他的幻灯片感兴趣。他的幻灯片是基于[Reveal.js](https://revealjs.com/)这款Web幻灯片框架，但不清楚他具体是如何制作的，在经过他的同意下，我制作了这个将Markdown方言转换成和他一个风格的幻灯片的工具。

对于Markdown扩展语法的设计尽可能简单，有些功能不是不能提供，但是提供会导致语法没有性价比的扩张，所以舍弃。让设计尽可能足够且简约。

## Install

本项目使用Python开发，模块管理使用Poetry，请确保您的机器上有版本足够的Python（**3.10以上**）并安装有第三方模块Poetry，同时也得益于Python，本项目应该可以运行于任何系统上。
>关于Poetry可参考我的[笔记](https://github.com/zweix123/CS-notes/tree/master/Programing-Language/Python#poetry)，当然下面会提供足够的用法。

1. 克隆项目到本地并进入：
    ```bash
    git clone https://github.com/zweix123/jyyslide-md.git
    cd jyyslide-md
    ```
2. 利用Poetry下载第三方模块
    ```bash
    poetry install
    ```

>如果在win机器且出现乱码, 可以尝试下面的方案  
>`控制面板` -> `区域` -> `管理` -> `更改系统区域设置` -> 打开`Beta版`

## Usage
>请确保已经[Install](#install)好了

+ 使用Peotry管理的Python有两种运行方式
  1. 进入虚拟环境：
      ```bash
      poetry shell
      ```
      之后就可以正常的运行Python代码了
  2. 使用前缀：在运行Python代码的命令前添加`poetry run`
  
      比如[样例1](#example)中的命令应该是`poetry run python main.py example\jyy\操作系统概述.md`

命令格式如下
```bash
python main.py [Markdown文件]
```
在Markdown文件同级目录会出现一个`dist`文件夹，其下有一个index.html文件和一个static文件夹，前者即为生成的“Web幻灯片，static即为其相关静态文件。网页的title和Markdown文件同名、icon即为`static/img/favicon.png`，可通过替换这个文件修改icon。

+ PDF Export: [Manual](https://revealjs.com/pdf-export/)

### Grammer

[教程](https://zweix123.github.io/jyyslide-md/)：在这里可以结合效果来说明语法（**推荐**）
>这个幻灯片就是用jyyslide-md制作而成的

+ 水平幻灯片使用`\n---\n`（三个）分割
+ 垂直幻灯片使用`\n----\n`（四个）分割
+ 渐变垂直幻灯片使用`\n++++\n`(四个)分割
+ 在同一张幻灯片中依次出现的部分使用`\n--\n`(两个)分割
  + 具体分割方式是从分割符到下一个分隔符或者本张幻灯片末尾的位置
  + 更多样式见[reveal.js官网对Fragments的解释](https://revealjs.com/fragments/)
+ 作者信息使用`\n+++++\n`(五个)和正文分割，使用Json格式   
  这里主要指指的是这部分  

  <img src="./resource/author.png" width="456">  
 
  因为这部分是多个文字、图片、链接为一体，如果使用扩展Markdown语法的设置会让语法很凌乱。  
  实际上这样的页面只在第一页出现，即使不使用这样的语法，使用这样的形式  
  ```
  # Title

  >author
  ```
  <img src="./resource/example_of_author.png" width="456">  
  
  在大多数场景也足够，所以从设计上将这部分从主题抽离出来  
  
  这部分的格式如下，
  
  >在[例子](#example)中的jyy中的Markdown文件
  
  ```json
  {
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
  }
  ```

  现也支持YAML格式（建议）

  ```yaml
  author:
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
      img: ./img/ics-logo.png
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
          Markdown中的格式是流的形式，即图片是占位的，这里默认左对齐和居中的图片都是占位的，但是右对齐的图片不占位

      其他格式调整SFTW
    + 支持数学公式
    + 支持表格（表格的格式并不好看）
    + 关于Markdown的这个语法：大于三个的`-`是分割线`<hr>`，我们发现这和扩展语法冲突，所以这里是大于四个的`-`是分割线，且这里的分割线在HTML中是空行的效果

---

+ 调整主题：如果您有CSS基础，可以调整蒋老师主题（主要指字号、字间距、行间距之类的微调），关于蒋老师主题的CSS文件在`dist/static/jyy/jyy.css`中。

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

+ `example/jyy/操作系统概述.md`即为蒋老师2022年的第一节课

  ```bash
  python main.py example/jyy/操作系统概述.md
  ```
  
  打开`example\jyy\dist\index.html`即可查看

+ `example/Intro/slide.md`即为本项目介绍的幻灯片

  ```bash
  python main.py example/Intro/slide.md
  ```
  
  打开`example\Intro\dist\index.html`即可查看

## Develop

+ 根目录下的main.py是项目的入口，主体代码在src目录下，逻辑核心在converter.py，这个过程要维护很多配置信息和全局信息，所以我将其放在settings.py下，util目录则是些辅助函数
+ 不建议扩展标记，converter虽然不长，但是写的不是很优雅，可维护性低
+ 推荐从`src/util/md_util.py`入手，项目将Markdown转换成html的代码在这里，可以通过修改markdown模块相关来增加功能
  + 比如slidev的代码特定行高亮，这就是后续的开发计划
+ 格式化使用black，静态检查使用mypy
  + 依赖库中有很多用于静态检查的模块，如果想最小化本项目，可以重新加载依赖
    + 这个模块`pygments`，没有出现在代码的任何地方，但是在代码高亮中发挥重要作用，如果重新加载依赖，不要忘记它。

## Acknowledgement
+ 感谢[南京大学蒋炎岩老师](https://ics.nju.edu.cn/~jyy/)录制了如此优质的[操作系统课程](https://jyywiki.cn/)
+ 感谢[顾若水](https://github.com/ruoshui255)大佬提供的[思路和大量代码](./src/backup/rouv/ruoshui255.md.py)
+ 感谢[Jungle](https://github.com/Jungle430)对编码问题的提醒

## License

[MIT](LICENSE) © Richard Littauer
