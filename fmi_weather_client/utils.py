import math


def is_float(v):
    """
    Validate if value is float and not a NaN
    :param v: Any value
    :return: True if value is valid; False otherwise
    """
    try:
        f = float(v)
        return not math.isnan(f)
    except (ValueError, TypeError):
        return False


def is_non_empty_observation(observation):
    """
    Validate if observation contains proper values
    :param observation: Observation dictionary
    :return: True if observation is not empty; False otherwise
    """
    for _, value in observation.items():
        if not math.isnan(value):
            return True
    return False
