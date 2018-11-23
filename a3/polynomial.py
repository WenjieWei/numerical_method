from matrix import Matrix


class Polynomial(object):
    def __init__(self, coeff):
        self._coeff = coeff
        self._order = len(coeff) - 1

    def __getitem__(self, item):
        return self._coeff[item]

    def __add__(self, other):
        self_has_higher_order = (max(self.order, other.order) == self.order)

        if(self_has_higher_order):
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
        pass

    def __mul__(self, other):
        pass

    def toString(self):
        print("y = ", end="")
        for i in range(self.order, 0, -1):
            if self[i] != 1 and self[i] != 0:
                print(str(self[i]) + "x^" + str(i) + " + ", end="")
            elif self[i] == 1:
                print("x^" + str(i) + " + ", end="")
            else:
                pass

        print(str(self[0]))

    @property
    def order(self):
        return self._order

    @property
    def coefficient(self):
        return self._coeff

class LagrangePolynomial(object):
    def __init__(self, n, xr):
        self._order = n
        self._xr = []
        self._L_list = [None for _ in range(n)]
        self._numerator = [None for _ in range(n - 1)]

        for i in range(len(xr)):
            self._xr.append(-xr[i])

        for j in range(n):
            counter = 0
            skipped = False
            for r in range(n):
                if counter == j:
                    counter += 1
                    skipped = True

                if not skipped:
                    temp_poly = Polynomial([xr[counter], 1])
                    self._numerator[counter] = temp_poly
                else:
                    temp_poly = Polynomial([xr[counter], 1])
                    self._numerator[counter - 1] = temp_poly

                temp_poly.toString()

if __name__ == "__main__":
    coeff = [1,2,3]
    l = LagrangePolynomial(3, coeff)
