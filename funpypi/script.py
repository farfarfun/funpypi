import argparse
import subprocess


def install(*args, **kwargs):
    packages = ["fundb", "funsecret", "farfuntask", "funbuild", "fundrive", "funread"]
    for package in packages:
        subprocess.check_call(["pip", "install", package, "-U", " -i", "https://pypi.org/simple/", "-q"], shell=True)


def funpypi():
    parser = argparse.ArgumentParser(prog="PROG")
    subparsers = parser.add_subparsers(help="sub-command help")

    # 添加子命令
    build_parser = subparsers.add_parser("install", help="install farfarfun packages")
    build_parser.set_defaults(func=install)

    args = parser.parse_args()
    args.func(args)
