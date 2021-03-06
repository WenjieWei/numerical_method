import math


class Matrix(object):
    def __init__(self, vec, rows, cols):
        self._vec = vec
        self._rows = rows
        self._cols = cols

    def set_row(self, n_rows):
        self._rows = n_rows

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
        vec_trans = [[0 for _ in range(self.rows)] for _ in range(self.cols)]
        for x in range(self.cols):
            for y in range(self.rows):
                vec_trans[x][y] = self.vec[y][x]

        transposed_matrix = Matrix(vec_trans, self.cols, self.rows)
        return transposed_matrix

    def __add__(self, other):
        if self.cols != other.cols or self.rows != other.rows:
            raise ValueError("Incorrect dimension for matrix subtraction.")

        result_vec = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        result = Matrix(result_vec, self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result[i][j] = self[i][j] + other[i][j]

        return result

    def __sub__(self, other):
        if self.cols != other.cols or self.rows != other.rows:
            raise ValueError("Incorrect dimension for matrix subtraction.")

        result_vec = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        result = Matrix(result_vec, self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                result[i][j] = self[i][j] - other[i][j]

        return result

    def minus(self, other):
        return self - other

    def __mul__(self, other):
        if self.cols != other.rows:
            raise ValueError("Incorrect dimension for matrix multiplication.")

        result_vec = [[None for _ in range(other.cols)] for _ in range(self.rows)]
        result = Matrix(result_vec, self.rows, other.cols)

        for i in range(self.rows):
            for j in range(other.cols):
                temp_sum = 0
                for k in range(other.rows):
                    temp_sum += self[i][k] * other[k][j]
                result[i][j] = temp_sum

        return result

    def dot_product(self, other):
        return self * other

    def det(self):
        if self.cols > 2 or self.rows > 2:
            raise ValueError("I cannot calculate determinants with dimensions over 2!")

        if self.cols != self.rows:
            raise ValueError("The matrix must be square to calculate the determinant!")

        return 1 / (self[0][0] * self[1][1] - self[0][1] * self[1][0])

    def inv(self):
        """

        :rtype: Matrix
        """
        if self.cols > 2 or self.rows > 2:
            raise ValueError("I cannot calculate inverse with dimensions over 2!")

        if self.cols != self.rows:
            raise ValueError("The matrix must be square to calculate the inverse!")

        result_mat = Matrix([[0, 0], [0, 0]], 2, 2)
        det = self.det()
        result_mat[0][0] = self[1][1] * det
        result_mat[1][1] = self[0][0] * det
        result_mat[0][1] = -self[0][1] * det
        result_mat[1][0] = -self[1][0] * det

        return result_mat

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
        cloned_vec = []
        for i in range(len(self.vec)):
            cloned_vec.append(self.vec[i])

        cloned_matrix = Matrix(cloned_vec, self.rows, self.cols)
        return cloned_matrix

    def print_matrix(self):
        for i in range(self.rows):
            print("|", end=" ")
            for j in range(self.cols):
                print("%f" % self[i][j], end=" ")
            print("|")

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
