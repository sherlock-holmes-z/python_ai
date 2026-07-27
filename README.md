# python-ai

一个采用 `src` 布局的 Python 项目模板，适合脚本、库和服务类项目的起点。

## 快速开始

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m mypy
```

也可以直接运行示例命令：

```powershell
python -m python_ai
# 或安装后运行
python-ai
```

## 项目结构和配置说明

详细说明见 [docs/project-structure.md](docs/project-structure.md)。

## 开发约定

- 业务代码放在 `src/python_ai/`，测试代码放在 `tests/`。
- 依赖、工具和项目元数据统一维护在 `pyproject.toml`。
- `.env` 只用于本地环境，禁止提交真实密钥；请维护 `.env.example`。
- 提交前运行测试、Ruff 和 mypy。
