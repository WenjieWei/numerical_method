from matrix import Matrix


class Polynomial():
    def __init__(self, coeff):
        self._coeff = coeff
        self._order = len(coeff) - 1

    @property
    def order(self):
        return self._order

    @property
    def coefficient(self):
        return self._coeff
