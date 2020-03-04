from typing import Any, Dict, Optional

import math


def float_or_none(value: Any) -> Optional[float]:
    """
    Get value as float. None if conversion fails.
    :param value: Any value
    :return: Value as float if successful; None otherwise
    """
    try:
        float_value = float(value)
        if not math.isnan(float_value):
            return float_value
        return None
    except (ValueError, TypeError):
        return None


def is_non_empty_forecast(forecast: Dict[str, float]) -> bool:
    """
    Check if forecast contains proper values
    :param forecast: Forecast dictionary
    :return: True if forecast contains values; False otherwise
    """
    for _, value in forecast.items():
        if not math.isnan(value):
            return True

    return False
