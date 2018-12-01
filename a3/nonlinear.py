from polynomial import Polynomial

TOLERANCE = 1e-6


def calc_newton_raphson(equation, data_x, data_y):
    """
    calculates the newton raphson
    :param equation: either a polynomial or a list of piecewise linear polynomials
    :param data_x: the list of data on the x axis
    :return: number of iterations and the final result
    """
    if isinstance(equation, list):
        """
            This condition will be taken if equation is a list of linear polynomials.
        """
        area = 1e-4
        flux_list = []
        coefficients = [3.9790e7, 0.3, -8000]
        first_iter = True

        # Calculate f(0)
        k = 0
        flux = 0
        convergent = False
        fk = -8000
        prev_fk = -8000

        while not convergent:
            if fk / prev_fk < TOLERANCE:
                break
            prev_fk = fk
            # Find the piecewise polynomial segment of the current flux
            for i in range(1, len(data_x)):
                if data_x[i - 1] <= (flux / area) < data_x[i]:
                    temp_poly = equation[i - 1]
                    start_H = data_y[i - 1]
                    break
                else:
                    temp_poly = equation[len(equation) - 1]
                    start_H = data_y[len(equation) - 1]

            # The polynomial segment is located at location i - 1
            # Calculating stuff at k
            slope = temp_poly[1]
            H = slope * flux / area + start_H
            fk = coefficients[0] * flux + coefficients[1] * H + coefficients[2]
            fk_prime = coefficients[0] + coefficients[1] * temp_poly[1] / area

            k += 1
            flux = flux - fk / fk_prime

        return k, flux_list
