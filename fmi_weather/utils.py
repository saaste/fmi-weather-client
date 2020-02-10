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


def is_valid_observation(observations):
    """
    Validate if observation is valid
    :param observations: Observations
    :return: True if observation is valid; False otherwise
    """
    # Temperature is required
    if math.isnan(observations.get('t2m', 'nan')):
        return False

    valid_value_count = 0
    for k, v in observations.items():
        if not math.isnan(v):
            valid_value_count += 1

    return valid_value_count > 2
