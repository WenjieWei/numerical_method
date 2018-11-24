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

            result_polynomial += Polynomial([aj]) * temp_lagrange_poly.poly

    else:
        pass

    return result_polynomial


def cubit_hermite(xr, y, slopes):
    result = Polynomial([0])

    for j in range(len(xr)):
        xj = xr[j]
        aj = y[j]
        bj = slopes[j]

        temp = LagrangePolynomial(len(xr), xr, j, xj).poly
        lagrange_backup = LagrangePolynomial(len(xr), xr, j, xj).poly

        # Calculate the polynomial u(x)
        temp = (temp.derive(1) * Polynomial([-xj, 1])) * Polynomial([-2])
        temp = temp + 1

        square = lagrange_backup * lagrange_backup
        uj = temp * square

        # Calculate the polynomial v(x)
        vj = Polynomial([-xj, 1]) * square

        aj_poly = Polynomial([aj])
        bj_poly = Polynomial([bj])

        result += uj * aj_poly + vj * bj_poly

    return result
