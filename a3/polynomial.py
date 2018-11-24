import math


class Polynomial(object):
    def __init__(self, coeff):
        self._coeff = coeff
        self._order = len(coeff) - 1

    def calculate(self, value):
        """
        This function calculates the result of the polynomial.

        :param value: value of x
        :return: value of y
        """
        result = 0
        for i in range(len(self._coeff)):
            result += self._coeff[i] * math.pow(value, i)

        return result

    def derive(self, der_order):
        result_coeff = []
        counter = 0

        for i in range(1, len(self._coeff)):
            result_coeff.append(i * self[i])
        result_poly = Polynomial(result_coeff)
        counter += 1

        if counter < der_order:
            return result_poly.derive(der_order - 1)
        else:
            return result_poly

    def __getitem__(self, item):
        return self._coeff[item]

    def __add__(self, other):
        self_has_higher_order = (max(self.order, other.order) == self.order)

        if self_has_higher_order:
            big_coeff = self.coefficient
            small_coeff = other.coefficient
        else:
            big_coeff = other.coefficient
            small_coeff = self.coefficient

        for i in range(len(small_coeff), len(big_coeff)):
            small_coeff.append(0)

        result_coeff = []
        for i in range(len(big_coeff)):
            result_coeff.append(small_coeff[i] + big_coeff[i])

        return Polynomial(result_coeff)

    def __sub__(self, other):
        self_has_higher_order = (max(self.order, other.order) == self.order)

        if self_has_higher_order:
            for i in range(len(other.coefficient), len(self.coefficient)):
                other.coefficient.append(0)
        else:
            for i in range(len(self.coefficient), len(other.coefficient)):
                self.coefficient.append(0)

        result_coeff = []
        for i in range(len(self.coefficient)):
            result_coeff.append(self.coefficient[i] - other.coefficient[i])

        return Polynomial(result_coeff)

    def __mul__(self, other):
        result_coefficients = []

        if isinstance(self, Polynomial) and isinstance(other, Polynomial):
            result_order = self.order + other.order

            for i in range(result_order + 1):
                coefficient = 0
                for j in range(self.order + 1):
                    for k in range(other.order + 1):
                        if j + k == i:
                            coefficient += self[j] * other[k]

                result_coefficients.append(coefficient)
        elif isinstance(self, Polynomial) and isinstance(other, int):
            for i in range(len(self._coeff)):
                result_coefficients.append(other * self[i])
        else:
            print("The format should be polynomial * polynomial or polynomial * constant.")

        return Polynomial(result_coefficients)

    def toString(self):
        print("y = ", end="")
        for i in range(self.order, 0, -1):
            if self[i] != 1 and self[i] != -1 and self[i] != 0:
                if self[i] >= 0:
                    print("+ " + str(self[i]) + "x^" + str(i), end=" ")
                else:
                    print("- " + str(-self[i]) + "x^" + str(i), end=" ")
            elif self[i] == 1:
                print("+ x^" + str(i), end=" ")
            elif self[i] == -1:
                print("- x^" + str(i), end=" ")
            else:
                pass

        if self[0] < 0:
            print("- " + str(-self[0]))
        else:
            print("+ " + str(self[0]))

    @property
    def order(self):
        return self._order

    @property
    def coefficient(self):
        return self._coeff


class LagrangePolynomial(object):
    def __init__(self, n, xr, j, xj):
        """
        Construct a Lagrange polynomial.

        :param n: how many points are on the x axis
        :param xr: the values of x
        :param j: the position of the current x
        :param xj: the value of x at position j
        """
        self._order = n
        self._j = j
        self._xr = []
        self._xj = xj

        self._x = 0

        for i in range(len(xr)):
            self._xr.append(-xr[i])

        self._numerator = self._create_numerator()
        self._denominator = self._create_denominator(xj)

    def _create_numerator(self):
        """
        This method creates the list of the parameters x_r.

        :return: no return value
        """
        i = 0
        result_numerator = Polynomial([1])

        while i < self._order:
            if i == self.j:
                i += 1

            if i >= self._order:
                break

            result_numerator *= Polynomial([self._xr[i], 1])
            i += 1

        return result_numerator

    def _create_denominator(self, x):
        """
        This method calculates the numerical result of the denominator.

        :return: the value in decimal of the denominator.
        """

        return self._numerator.calculate(x)

    def set_x(self, value):
        self._x = value

    @property
    def j(self):
        return self._j

    @property
    def xj(self):
        return self._xj

    @property
    def denominator(self):
        return self._denominator

    @property
    def numerator(self):
        return self._numerator


if __name__ == "__main__":
    coeff1 = Polynomial([2])
    coeff2 = Polynomial([4, 5, 7, 8])

    coeff2.toString()
    (coeff2 * 3).toString()
    coeff2.derive(3).toString()
