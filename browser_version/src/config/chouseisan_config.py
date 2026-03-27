"""
调整さん(chouseisan.com)网站配置文件。

默认从仓库根目录的 .env 读取配置，避免把个人账号信息提交到仓库。
"""

import os
from pathlib import Path

from dotenv import load_dotenv


REPO_ROOT = Path(__file__).resolve().parents[3]
load_dotenv(REPO_ROOT / ".env")


def _env_flag(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


CHOUSEISAN_CONFIG = {
    "url": os.getenv("CHOUSEISAN_URL", ""),
    "email": os.getenv("CHOUSEISAN_EMAIL", ""),
    "password": os.getenv("CHOUSEISAN_PASSWORD", ""),
    "headless": _env_flag("CHOUSEISAN_HEADLESS", default=False),
}
