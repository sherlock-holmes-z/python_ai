# python-ai

一个采用 `src` 布局的 Python 项目模板，适合脚本、库和服务类项目的起点。

## 快速开始

推荐使用项目根目录的 `environment.yml` 创建独立 Conda 环境：

```powershell
conda env create --file environment.yml
conda activate python-ai
python --version
python -m pip check
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m mypy
```

环境已经存在、配置发生变化时执行：

```powershell
conda env update --file environment.yml --prune
```

`--prune` 会删除不再声明的 Conda 包。执行上述命令时应位于项目根目录，
因为环境创建过程会以 editable 模式安装当前项目。

当前默认依赖只有 FastAPI、现有示例已使用的 aiohttp/NumPy 和开发工具。
后续学到数据库、LLM、RAG 或数据处理时，
按需安装 `pyproject.toml` 中已经准备好的可选依赖组：

```powershell
# FastAPI 数据库、配置和认证
python -m pip install -e ".[dev,backend]"

# 在 backend 基础上增加大模型 API 和 RAG
python -m pip install -e ".[dev,backend,llm,rag]"

# 增加 NumPy、pandas、scikit-learn 和 JupyterLab
python -m pip install -e ".[dev,data]"
```

可选组只是在配置中登记，默认不会下载和安装。正式启用某个分组后，应同步修改
`environment.yml` 中的 `.[dev]`，例如改成 `.[dev,backend]`，保证其他电脑也安装相同分组。

PyTorch 与 CUDA 和显卡驱动强相关，项目暂不进行通用自动安装；学习本地模型时，
应先根据 PyTorch 官方安装选择器安装与当前硬件匹配的版本，再启用 `local-ai` 依赖组。

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
- Python/Conda 环境入口维护在 `environment.yml`，项目统一使用 Python 3.12。
- `.env` 只用于本地环境，禁止提交真实密钥；请维护 `.env.example`。
- 提交前运行测试、Ruff 和 mypy。
