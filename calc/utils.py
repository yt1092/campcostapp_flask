from typing import Optional

def safe_int(value: Optional[str], default: int = 0) -> int:
    try:
        return int(float(value))
    except Exception:
        return default

def safe_float(value: Optional[str], default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default