import math


class matrix(object):
    def __init__(self, vec, rows, cols):
        self._vec = vec
        self._rows = rows
        self._cols = cols

    def is_square(self):
        return self._rows == self._cols

    def is_symmetric(self):
        return self == self.T

    def transpose(self):
        vec_trans = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for x in range(self.cols):
            for y in range(self.rows):
                vec_trans[x, y] = self.vec[y, x]

        transposed_matrix = matrix(vec_trans, self.cols, self.rows)
        return transposed_matrix

    def clone(self):
        cloned_matrix = matrix(self.vec, self.rows, self.cols)

        return cloned_matrix


    @property
    def vec(self):
        return self._vec

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    @property
    def T(self):
        return self.transpose()
