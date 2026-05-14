import argparse
import subprocess
from functools import partial
import sys
import os
import logging
from livereload import Server
from pathlib import Path

def build(filepath: str):
    logging.info("Rebuilding...")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    build_script = os.path.join(current_dir, "build.py")
    try:
        result = subprocess.run(
            [sys.executable, build_script, filepath],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            logging.log(logging.WARNING, "编译出错，但监听继续：")
            logging.log(logging.WARNING, result.stdout)
            logging.log(logging.WARNING, result.stderr)
        else:
            logging.info("编译成功")
    except Exception as e:
        logging.error("执行build异常， 但监听继续：", e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="file path to target markdown file.", type=str)
    parser.add_argument("--host", default="0.0.0.0", help="host ip address", type=str)
    parser.add_argument("--port", default=5500, help="port", type=int)
    args = parser.parse_args()

    build(args.filepath)

    server = Server()
    server.watch(args.filepath, partial(build, args.filepath))
    server.serve(root=f'{Path(args.filepath).resolve().parent}/dist', open_url_delay=1, host=args.host, port=args.port)



if __name__ == "__main__":
    main()
