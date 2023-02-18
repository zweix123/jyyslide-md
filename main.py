import argparse
from src.converter import converter

if __name__ == "__main__":
    # 命令行, 清楚明了, 含义和默认值在--help中
    parser = argparse.ArgumentParser()
    parser.add_argument("MDfile", help="select a Markdown file to convert", type=str)
    parser.add_argument(
        "--title", help="select a title for your web slide, defult file name", type=str
    )
    parser.add_argument(
        "--icon",
        help="select a image as your web icon, default 'Z', or modify in dist folder",
        type=str,
    )
    parser.add_argument(
        "--folder", help="select a folder to save dist, default same to md", type=str
    )

    args = parser.parse_args()

    converter(args.MDfile, args.title, args.icon, args.folder)
