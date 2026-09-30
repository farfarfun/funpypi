import os
import sys
from os import path


class VersionManage:
    """读写三段式版本号，并按步长递增。"""

    def __init__(self, version_path: str | None = None, step: int = 32) -> None:
        """初始化版本文件路径和进位步长。

        Args:
            version_path: 版本文件路径，默认是 script/__version__.md。
            step: 每一段版本号的进位值。
        """
        if step < 2:
            raise ValueError("step 必须大于 1")
        self.step = step
        self.version_path = version_path or "./script/__version__.md"
        self.version_arr = [0, 0, 1]
        self.read()

    @property
    def version(self) -> str:
        """返回当前版本字符串。"""
        return ".".join([str(i) for i in self.version_arr])

    def add(self) -> None:
        """将版本号递增一个版本。"""
        step = self.step
        version = self.version_arr
        version2 = version[0] * step * step + version[1] * step + version[2] + 1
        version[2] = version2 % step
        version[1] = int(version2 / step) % step
        version[0] = int(version2 / step / step)

        self.version_arr = version

    def read(self) -> None:
        """从版本文件读取版本号，不存在时使用初始版本。"""
        if path.exists(self.version_path):
            with open(self.version_path, "r") as f:
                self.version_arr = [int(i) for i in f.read().split(".")]
        else:
            self.version_arr = [0, 0, 1]

    def write(self) -> str:
        """将当前版本写回文件并返回版本字符串。"""
        with open(self.version_path, "w") as f:
            f.write(self.version)
        return self.version


def read_version(version_path: str | None = None, update: bool = False) -> str:
    """读取版本号，可选地递增并写回版本文件。

    Args:
        version_path: 版本文件路径。
        update: 是否递增并写回版本号。

    Returns:
        当前或更新后的三段式版本字符串。
    """
    manage = VersionManage(version_path=version_path)
    manage.read()
    if update or (
        len(sys.argv) >= 2
        and (os.environ.get("funbuild_multi_index", "0") == "0")
        and (sys.argv[1] == "build" or sys.argv[1] == "bdist_wheel")
    ):
        # print(sys.argv)
        manage.add()
        manage.write()
    return manage.version
