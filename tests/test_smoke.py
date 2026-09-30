"""funpypi 公开 API 和失败路径测试。"""

from unittest.mock import Mock, patch

import pytest

from funpypi.version import VersionManage


def test_version_manage_increment_and_write(tmp_path) -> None:
    """版本号应按三段式递增并写回文件。"""
    version = VersionManage(str(tmp_path / "version"))
    version.add()
    assert version.write() == "0.0.2"
    assert (tmp_path / "version").read_text() == "0.0.2"


def test_read_version_update_and_invalid_step(tmp_path) -> None:
    """read_version 应支持更新版本，并拒绝无效进位值。"""
    from funpypi.version import read_version

    version_path = tmp_path / "version"
    version_path.write_text("1.2.3")
    assert read_version(str(version_path), update=True) == "1.2.4"
    assert version_path.read_text() == "1.2.4"

    with pytest.raises(ValueError, match="step"):
        VersionManage(str(version_path), step=1).add()


def test_install_stops_on_failed_command() -> None:
    """任一包安装失败都应抛出错误而不是继续报告成功。"""
    from funpypi import script

    with patch.object(script, "run_shell", side_effect=["1"]) as run:
        with pytest.raises(RuntimeError, match="fundb"):
            script.install()
    run.assert_called_once()


def test_setup_defaults_name() -> None:
    """setuptools 辅助函数应提供默认包名和版本。"""
    from funpypi import setuptool

    with patch.object(setuptool, "setup2", return_value=Mock()) as setup2:
        setuptool.setup("demo")
    assert setup2.call_args.kwargs["name"] == "demo"


def test_import() -> None:
    """顶层包应可正常导入。"""
    import funpypi  # noqa: F401
