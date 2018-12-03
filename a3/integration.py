import math
from math import log


def gauss_legendre_integration(function, lim_low, lim_high, n, real_value):
    width = (lim_high - lim_low) / n

    result = 0
    x = lim_low
    for i in range(n):
        result += function(x + width / 2) * width
        x += width

    error = abs(result - real_value)
    return result, error


def nested_integration(lim_low, lim_high, n, real_value):
    width = (lim_high - lim_low) / n

    result = 0
    x = lim_low
    for i in range(n):
        x_0 = x + width / 2
        result += (log(x_0) / math.sqrt(0.04 - x_0 ** 2)) * width
        x += width

    error = abs(result - real_value)
    return result, error
