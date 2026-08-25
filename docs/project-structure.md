# Python 项目目录与配置说明

## 推荐目录结构

```text
python-ai/
├── .github/
│   └── workflows/
│       └── ci.yml
├── configs/
│   └── settings.example.yaml
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   └── project-structure.md
├── scripts/
├── src/
│   └── python_ai/
│       ├── __init__.py
│       ├── __main__.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── .editorconfig
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── environment.yml
├── pyproject.toml
└── README.md
```

## 目录作用

| 目录 | 作用 | 常见内容 |
| --- | --- | --- |
| `src/` | 存放可安装的正式源码。使用 `src` 布局可以避免测试时误引用项目根目录下的源码。 | 一个或多个 Python 包 |
| `src/python_ai/` | 项目主包。包名应使用小写和下划线，按领域继续拆分模块。 | `api/`、`models/`、`services/`、`utils/`、`main.py` |
| `tests/` | 自动化测试，与源码目录结构尽量对应。 | 单元测试、集成测试、测试夹具 `conftest.py` |
| `docs/` | 面向开发者和使用者的文档。 | 架构说明、接口文档、部署手册、变更记录 |
| `configs/` | 不同环境的非敏感配置模板。 | `settings.example.yaml`、开发/生产配置示例 |
| `data/raw/` | 原始输入数据，只读保存，便于追溯。 | 下载数据、原始 CSV/JSON |
| `data/processed/` | 清洗、转换或特征工程后的数据。 | 中间数据、训练集、报表数据 |
| `scripts/` | 一次性或运维辅助脚本，不作为核心业务包导入。 | 初始化、数据处理、发布脚本 |
| `.github/workflows/` | CI/CD 自动化流程。 | 测试、检查、构建、发布 workflow |

小型项目可以暂时省略 `configs/`、`data/`、`docs/` 和 `scripts/`；随着项目变复杂再增加即可。

## 配置文件一般配置什么

### `pyproject.toml`

Python 项目的核心配置文件，通常集中配置：

- 项目元数据：名称、版本、作者、Python 版本、运行时依赖；
- 构建方式：setuptools、Hatch、Poetry 或 PDM；
- 命令行入口：安装后可执行的命令；
- 测试工具：测试目录、默认参数、覆盖率；
- 代码质量工具：Ruff、mypy、coverage 等规则；
- 可选开发依赖：测试、格式化、类型检查和提交钩子。

本模板选择标准 `pyproject.toml`，不额外拆出 `setup.py`、`setup.cfg`。

### `.gitignore`

声明不应进入 Git 的文件，例如虚拟环境、缓存、构建产物、覆盖率报告、本地数据和 IDE 文件。真实配置和密钥也应排除在外。

### `.env.example` 与 `.env`

`.env.example` 保存环境变量名称和示例值，供团队参考；`.env` 保存本机实际值并加入忽略列表。生产环境通常使用部署平台的环境变量或 Secret Manager，不把密码写进仓库。

### `.editorconfig`

统一不同编辑器的基础格式，例如编码、换行符、缩进和行尾空格，减少无意义的格式差异。

### `.pre-commit-config.yaml`

配置提交前自动执行的检查。本模板使用 Ruff 格式化和 lint，并检查 YAML/TOML 语法、文件结尾及合并冲突标记。

### `.python-version`

为 pyenv、部分 IDE 或版本管理工具指定默认 Python 版本。若团队使用 uv、Poetry 或 Conda，也可以把版本约束同步到对应配置中。

### `environment.yml`

定义可跨电脑创建的 Conda 环境入口，包括环境名、Python 3.12 和 pip 安装入口。Conda 负责解释器，pip 根据 `pyproject.toml` 安装项目依赖，避免重复维护两套业务依赖清单。默认安装 FastAPI、现有示例使用的 aiohttp/NumPy 与开发工具，其他 AI/数据库依赖通过 optional dependencies 按学习阶段启用。

### `configs/*.yaml` 或 `*.toml`

适合保存非敏感的业务配置，如日志级别、服务端口、超时时间和功能开关。不同环境可以使用不同文件，敏感值通过环境变量覆盖。

### `.github/workflows/ci.yml`

描述云端持续集成任务，通常包括：安装指定 Python 版本、安装依赖、运行测试、lint、格式检查、类型检查，以及构建分发包。

## 常见扩展

- Web API：增加 `routers/`、`schemas/`、`dependencies/`，并增加 FastAPI/Flask 配置；
- 数据科学：增加 `notebooks/`、`models/`、`data/`，并明确原始数据与生成数据边界；
- 数据库项目：增加 `alembic.ini` 和 `alembic/` 迁移目录；
- Docker 部署：增加 `Dockerfile`、`.dockerignore` 和 `compose.yaml`；
- 多环境部署：增加 CI/CD workflow、环境变量清单和部署文档。
