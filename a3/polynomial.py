from matrix import Matrix


class Polynomial(object):
    def __init__(self, coeff):
        self._coeff = coeff
        self._order = len(coeff) - 1

    def __getitem__(self, item):
        return self._coeff[item]

    def __add__(self, other):
        large_order = max(self.order, other.order)
        small_order = min(self.order, other.order)
        result_coeff = [0 for _ in range(large_order + 1)]

        for i in range(small_order):
            result_coeff[i] = self[i] + other[i]

        for i in range(small_order, large_order + 1):
            if self.order >= other.order:
                result_coeff[i] = self[i]
            else:
                result_coeff[i] = other[i]

        result = Polynomial(result_coeff)
        return result

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
    