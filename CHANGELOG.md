# 更新日志

## [未发布]

### 修复

- 批量安装列表中的 `fundb` 改为组织真实发布名 `fundb-tau`：PyPI 上的 `fundb` 已被他人
  （Madhava-mng）占用，按旧名安装会装到别人的包。
- 删除历史遗留的 `script/__version__.md`，版本号统一以 `pyproject.toml` 为唯一来源。
- 补全 `setup`/`install` 公开 API 的参数、返回值与异常说明文档。

### 新增

- 补充 `setups`、CLI 子命令分发、`install` 成功路径、`setup` 默认值与缺 README 失败边界的测试。

## [0.2.2] - 2026-09-21

### 新增

- 增加版本管理和批量安装命令的公开 API 测试。

### 修复

- 使用 `funshell` 执行安装命令，失败时返回非零状态并统一使用 `farlog` 记录日志。

### 变更

- 迁移到 `src/funpypi` 布局并补齐类型标注、依赖下限和可复现锁文件。

### 废弃

- 无。
