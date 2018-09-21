import math


class matrix(object):
    def __init__(self, vec, rows, cols):
        self._vec = vec
        self._rows = rows
        self._cols = cols

    def is_square(self):
        return self._rows == self._cols

    def is_symmetric(self):
        if not self.is_square():
            return False

        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    if self[i][j] != self.T[i][j]:
                        return False

        return True

    def transpose(self):
        vec_trans = [[None for _ in range(self.rows)] for _ in range(self.cols)]
        for x in range(self.cols):
            for y in range(self.rows):
                vec_trans[x][y] = self.vec[y][x]

        transposed_matrix = matrix(vec_trans, self.cols, self.rows)
        return transposed_matrix

    def dot_product(self, other):
        if self.cols != other.rows:
            raise ValueError("Incorrect dimension for vector multiplication.")

        result = 0
        for i in range(self.rows):
            for j in range(self.cols):
                result += (self.vec[i][j] * other.vec[j][i])

        return result

    def is_positive_definite(self):
        pass

    def __getitem__(self, item_number):
        if isinstance(item_number, int):
            return self._vec[item_number]

        if isinstance(item_number, tuple):
            x, y = item_number
            # use some "dummy entries" as a buffer to decrease the possibility of occurring out of boundary.
            if x < 0 or x >= self.rows or y < 0 or y >= self.cols:
                return 0
            else:
                return self._vec[x][y]

    def clone(self):
        cloned_matrix = matrix(self.vec, self.rows, self.cols)
        return cloned_matrix

    def print_matrix_property(self):
        print("The entered matrix is:\n")
        for i in range(self.rows):
            for j in range(self.cols):
                print("%d" % (self[i][j]), end=" ")
            print("\n")

        print("The transpose of the entered matrix is:\n")
        other = self.T
        for i in range(other.rows):
            for j in range(other.cols):
                print("%d" % (other[i][j]), end=" ")
            print("\n")

        if self.is_square():
            print("The entered matrix is square.\n")
        else:
            print("The entered matrix is not square.\n")

        if self.is_symmetric():
            print("The entered matrix is symmetric.\n")
        else:
            print("The entered matrix is not symmetric.\n")

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
