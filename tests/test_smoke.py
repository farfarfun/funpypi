"""funpypi 公开 API 和失败路径测试。"""

import sys
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


def test_install_succeeds_for_all_packages() -> None:
    """全部包安装成功时应逐个调用 pip，且批量安装列表只含组织自有包名。

    `fundb` 在 PyPI 上已被他人（Madhava-mng）占用，组织自有发布名是
    `fundb-tau`（见 NAMING.md），批量安装不能按仓库名直接装到别人的包。
    """
    from funpypi import script

    with patch.object(script, "run_shell", return_value="0") as run:
        script.install()
    installed_pkgs = [
        call.args[0].split("install -U ")[1].split(" ")[0] for call in run.call_args_list
    ]
    assert run.call_count == len(installed_pkgs) == 7
    assert "fundb-tau" in installed_pkgs
    assert "fundb" not in installed_pkgs


def test_setup_defaults_name() -> None:
    """setuptools 辅助函数应提供默认包名和版本。"""
    from funpypi import setuptool

    with patch.object(setuptool, "setup2", return_value=Mock()) as setup2:
        setuptool.setup("demo")
    assert setup2.call_args.kwargs["name"] == "demo"


def test_setup_defaults_full(tmp_path, monkeypatch) -> None:
    """未显式传参时，setup 应填充 author/url/package_data 等全部默认值。"""
    from funpypi import setuptool

    monkeypatch.chdir(tmp_path)
    (tmp_path / "README.md").write_text("demo readme")

    with patch.object(setuptool, "setup2", return_value=Mock()) as setup2:
        setuptool.setup("demo", version="1.2.3")

    kwargs = setup2.call_args.kwargs
    assert kwargs["author"] == "bingtao"
    assert kwargs["author_email"] == "1007530194@qq.com"
    assert kwargs["url"] == "https://github.com/farfarfun/demo"
    assert kwargs["description"] == "demo"
    assert kwargs["package_data"] == {"": ["*.js", "*.*"]}
    assert kwargs["install_requires"] == []
    assert kwargs["long_description"] == "demo readme"
    assert kwargs["version"] == "1.2.3"


def test_setup_missing_readme_raises(tmp_path, monkeypatch) -> None:
    """未传 long_description 且当前目录没有 README.md 时应失败而不是静默发布空描述。"""
    from funpypi import setuptool

    monkeypatch.chdir(tmp_path)

    with patch.object(setuptool, "setup2", return_value=Mock()):
        with pytest.raises(FileNotFoundError):
            setuptool.setup("demo", version="1.0.0")


def test_setups_picks_param_by_env_index(monkeypatch) -> None:
    """setups 应按 funbuild_multi_index 环境变量选中对应的参数字典。"""
    from funpypi import setuptool

    params = [
        {"name": "first", "version": "0.0.1", "long_description": "a"},
        {"name": "second", "version": "0.0.2", "long_description": "b"},
    ]
    monkeypatch.setenv("funbuild_multi_index", "1")

    with patch.object(setuptool, "setup2", return_value=Mock()) as setup2:
        setuptool.setups(params)

    assert setup2.call_args.kwargs["name"] == "second"
    assert setup2.call_args.kwargs["version"] == "0.0.2"


def test_funpypi_cli_dispatches_to_install(monkeypatch) -> None:
    """CLI 的 install 子命令应分发到 install 函数。"""
    from funpypi import script

    monkeypatch.setattr(sys, "argv", ["funpypi", "install"])
    with patch.object(script, "install") as install_mock:
        script.funpypi()
    install_mock.assert_called_once()


def test_funpypi_cli_requires_subcommand(monkeypatch) -> None:
    """不带子命令运行 CLI 时应报错退出，而不是静默什么都不做。"""
    from funpypi import script

    monkeypatch.setattr(sys, "argv", ["funpypi"])
    with pytest.raises(SystemExit):
        script.funpypi()


def test_import() -> None:
    """顶层包应可正常导入。"""
    import funpypi  # noqa: F401
