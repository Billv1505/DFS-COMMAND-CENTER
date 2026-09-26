import json
import os
import pandas as pd
from typing import Optional

CACHE_DIR = ".cache"


def _ensure_dir():
    os.makedirs(CACHE_DIR, exist_ok=True)


def _path(slate_name: str) -> str:
    safe = slate_name.replace(" ", "_").replace("(", "").replace(")", "").lower()
    return os.path.join(CACHE_DIR, f"{safe}.json")


def save_slate(slate_name: str, df: Optional[pd.DataFrame]):
    _ensure_dir()
    if df is None:
        if os.path.exists(_path(slate_name)):
            os.remove(_path(slate_name))
        return
    df.to_json(_path(slate_name), orient="records")


def load_slate(slate_name: str) -> Optional[pd.DataFrame]:
    p = _path(slate_name)
    if not os.path.exists(p):
        return None
    try:
        return pd.read_json(p, orient="records")
    except Exception:
        return None
