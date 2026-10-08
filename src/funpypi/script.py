import typer
from farlog import getLogger
from funshell import run_shell

logger = getLogger("funpypi")
app = typer.Typer(help="farfarfun 组织包管理工具")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit(2)


@app.command()
def install() -> None:
    """升级组织内部发布包，任一步骤失败都会终止命令。

    任一包安装失败会抛出 `RuntimeError`，命令以非零状态退出。
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
    app()
