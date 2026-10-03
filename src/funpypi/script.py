import argparse
from typing import Any

from farlog import getLogger
from funshell import run_shell

logger = getLogger("funpypi")


def install(*args: Any, **kwargs: Any) -> None:
    """升级组织内部发布包，任一步骤失败都会终止命令。

    Args:
        *args: 兼容 argparse 子命令分发，接收 `args.func(args)` 传入的
            `Namespace` 对象，函数体内不使用其内容。
        **kwargs: 预留的关键字参数占位，当前不使用。

    Returns:
        None。安装全部成功时无返回值；任一包安装失败会抛出 `RuntimeError`
        而不是返回错误状态。
    """
    packages = [
        "fardb",
        "funsecret",
        "farfuntask",
        "funbuild",
        "fundrive",
        "funread",
        "funfile",
    ]
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
