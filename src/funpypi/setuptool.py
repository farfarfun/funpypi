import os
from typing import Any

from setuptools import find_packages
from setuptools import setup as setup2

from .version import read_version


def setup(
    name: str,
    package_name: str | None = None,
    version: str | None = None,
    description: str | None = None,
    author: str | None = None,
    author_email: str | None = None,
    url: str | None = None,
    packages: list[str] | None = None,
    package_data: dict[str, list[str]] | None = None,
    install_requires: list[str] | None = None,
    long_description: str | None = None,
    *args: object,
    **kwargs: Any,
) -> Any:
    """按组织默认值调用 setuptools.setup。

    Args:
        name: 项目名称，同时作为 package_name、description、url 的默认取值来源。
        package_name: 发布到 PyPI 的包名，默认使用 name。
        version: 版本号，未提供时通过 `read_version()` 从版本文件读取。
        description: 包描述，默认使用 name。
        author: 作者名，默认 "bingtao"。
        author_email: 作者邮箱，默认 "1007530194@qq.com"。
        url: 项目主页，默认 `https://github.com/farfarfun/{name}`。
        packages: 要发布的包列表，默认使用 `setuptools.find_packages()` 自动发现。
        package_data: 包含的非 Python 文件规则，默认 `{"": ["*.js", "*.*"]}`。
        install_requires: 运行时依赖列表，默认空列表。
        long_description: 长描述正文，默认读取当前目录下的 `README.md`；
            该文件不存在时会抛出 `FileNotFoundError`。
        *args: 透传给 `setuptools.setup` 的位置参数。
        **kwargs: 透传给 `setuptools.setup` 的关键字参数。

    Returns:
        `setuptools.setup` 的返回值。

    Raises:
        FileNotFoundError: 未显式传入 `long_description` 且当前目录缺少
            `README.md` 时。
    """
    version = version or read_version()
    return setup2(
        name=package_name or name,
        version=version,
        description=description or name,
        author=author or "bingtao",
        author_email=author_email or "1007530194@qq.com",
        url=url or f"https://github.com/farfarfun/{name}",
        packages=packages or find_packages(),
        package_data=package_data or {"": ["*.js", "*.*"]},
        install_requires=install_requires or [],
        long_description=long_description or open("README.md").read(),
        long_description_content_type="text/markdown",
        *args,
        **kwargs,
    )


def setups(params: list[dict[str, Any]] | None = None) -> Any:
    """根据 funbuild 多包索引选择并调用 setup。

    Args:
        params: 多包配置列表；为空时使用空列表。

    Returns:
        setup 的返回值。
    """
    params = params or []
    return setup(**params[int(os.environ.get("funbuild_multi_index", "0"))])
