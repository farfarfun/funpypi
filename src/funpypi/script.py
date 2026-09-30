import argparse
from typing import Any

from farlog import getLogger
from funshell import run_shell

logger = getLogger("funpypi")


def install(*args: Any, **kwargs: Any) -> None:
    """升级组织内部发布包，任一步骤失败都会终止命令。"""
    packages = ["fundb", "funsecret", "farfuntask", "funbuild", "fundrive", "funread", "funfile"]
    for package in packages:
        logger.info("安装 {} ...", package)
        result = run_shell(f"python -m pip install -U {package} -i https://pypi.org/simple/ -q")
        if result != "0":
            raise RuntimeError(f"安装 {package} 失败: {result}")
        logger.info("安装 {} 完成", package)


def funpypi() -> None:
    """运行 funpypi 命令行入口。"""
    parser = argparse.ArgumentParser(prog="funpypi")
    subparsers = parser.add_subparsers(help="sub-command help")

    # 添加子命令
    build_parser = subparsers.add_parser("install", help="安装 farfarfun 组织包")
    build_parser.set_defaults(func=install)

    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.error("必须指定子命令")
    args.func(args)
