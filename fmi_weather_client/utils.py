import math
from typing import Optional, Any

from fmi_weather_client.models import FMIObservation


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


def is_non_empty_observation(observation: FMIObservation) -> bool:
    """
    Validate if observation contains proper values
    :param observation: Observation
    :return: True if observation is not empty; False otherwise
    """
    for _, value in observation.variables.items():
        if value is not None:
            return True
    return False
