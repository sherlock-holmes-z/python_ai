"""测试启动配置：只为导入应用提供占位密码，单元测试不会连接真实数据库。"""

import os
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

os.environ.setdefault("CUSTOMER_SERVICE_DB_PASSWORD", "unit-test-placeholder")
