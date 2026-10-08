# funpypi

`funpypi` 提供 farfarfun 组织包的批量升级命令，以及兼容旧项目的版本和 setuptools 辅助 API。

## 安装

```bash
pip install funpypi
```

支持 Python 3.10 及以上版本。

## 使用

```bash
funpypi install
```

Python API 示例：

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from funpypi.version import VersionManage

with TemporaryDirectory() as directory:
    version = VersionManage(str(Path(directory) / "version.txt"))
    version.add()
    print(version.write())  # 0.0.2
```

安装命令会按顺序升级组织包；任一包安装失败都会以非零状态退出。

## Python API

- `read_version(version_path=None, update=False)`：读取指定版本文件；传入
  `update=True` 时递增后写回。未指定路径时，为兼容旧项目会使用
  `script/__version__.md`。
- `setup(...)`：以组织默认值调用 `setuptools.setup`，未传入 `version` 时通过
  `read_version()` 读取版本文件。
- `setups(params)`：根据 `funbuild_multi_index` 环境变量，从多包配置中选择一个并调用
  `setup`。

`VersionManage` 和 `read_version` 管理的是独立的版本文本文件，不会读取或修改
`pyproject.toml` 中的项目发布版本。

## 开发与检查

在仓库根目录安装开发和构建工具后，可运行以下命令：

```bash
python -m pip install -e . pytest ruff build
python -m pytest
ruff check .
ruff format --check .
python -m build
```

---

## 关于 farfarfun

[farfarfun](https://github.com/farfarfun) 是一个专注于实用工具库的开源组织，
涵盖云存储、数据处理、AI、多媒体与开发工具链等方向。

- 🏠 组织主页：<https://github.com/farfarfun>
- 📦 PyPI：<https://pypi.org/user/niuliangtao/>
- 📧 联系：farfarfun@qq.com

本项目基于 [MIT](LICENSE) 协议开源。
