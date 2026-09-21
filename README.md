# funpypi

`funpypi` 提供 farfarfun 组织包的批量升级命令，以及兼容旧项目的版本和 setuptools 辅助 API。

## 安装

```bash
pip install funpypi
```

## 使用

```bash
funpypi install
```

Python API 示例：

```python
from funpypi.version import VersionManage

version = VersionManage("script/__version__.md")
version.add()
print(version.write())
```

安装命令会按顺序升级组织包；任一包安装失败都会以非零状态退出。

---

## 关于 farfarfun

[farfarfun](https://github.com/farfarfun) 是一个专注于实用工具库的开源组织，
涵盖云存储、数据处理、AI、多媒体与开发工具链等方向。

- 🏠 组织主页：<https://github.com/farfarfun>
- 📦 PyPI：<https://pypi.org/user/niuliangtao/>
- 📧 联系：farfarfun@qq.com

本项目基于 [MIT](LICENSE) 协议开源。
