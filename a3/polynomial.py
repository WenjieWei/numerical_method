from matrix import Matrix


class Polynomial():
    def __init__(self, order, coeff):
        self._order = order
        self._coeff = coeff

    @property
    def order(self):
        return self._order

    @property
    def coefficient(self):
        return self._coeff
