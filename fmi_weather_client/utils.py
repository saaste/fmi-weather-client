from typing import Any, Dict, Optional

import math


def float_or_none(v: Any) -> Optional[float]:
    """
    Get value as float. None if conversion fails.
    :param v: Any value
    :return: Value as float if successful; None otherwise
    """
    try:
        f = float(v)
        if not math.isnan(f):
            return f
        return None
    except (ValueError, TypeError):
        return None


def is_non_empty_forecast(forecast: Dict[str, float]) -> bool:
    for _, value in forecast.items():
        if not math.isnan(value):
            return True

    return False
