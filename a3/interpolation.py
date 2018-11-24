from polynomial import Polynomial, LagrangePolynomial


def lagrange_full_domain(xr, y, points=None):
    """
    This is the method for the lagrange full domain interpolation.
    X is the variable that varies.
    Y is the variable that varies with respect to X.

    :param X: X vector of type Matrix
    :param Y: Y vector of type Matrix
    :param points: select the range of data to be interpolated if needed.
    :return: Polynomial expression for y(x)
    """
    result_polynomial = Polynomial([0])

    if points is None:
        for j in range(len(xr)):
            xj = xr[j]
            aj = y[j]

            temp_lagrange_poly = LagrangePolynomial(len(xr), xr, j, xj)
            temp_poly = Polynomial([aj / temp_lagrange_poly.denominator])

            result_polynomial += temp_poly * temp_lagrange_poly.numerator

    else:
        pass

    return result_polynomial
