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

        result_vec = [[None for _ in range(other.cols)] for _ in range(self.rows)]
        result = matrix(result_vec, self.rows, other.cols)

        for i in range(self.rows):
            for j in range(other.cols):
                temp_sum = 0
                for k in range(other.rows):
                    temp_sum += self[i][k] * other[k][j]
                result[i][j] = temp_sum

        return result

    def choleski_decomposition(self, b):
        """
        This is the method implemented for solving the problem Ax = b,
        using Choleski Decomposition.

        Arguments:
            self: the matrix A, a real, S.P.D. (Symmetric positive definite) n * n matrix.
            b: Column vector with n rows.

        Returns:
            Column vector x with n rows.
        """
        if not self.is_symmetric():
            raise ValueError("Matrix must be symmetric to perform Choleski Decomposition.\n")

        n = self.rows
        sparse_matrix = [[0 for _ in range(n)] for _ in range(n)]
        L = matrix(sparse_matrix, n, n)

        for j in range(n):
            if self[j][j] <= 0:
                raise ValueError("Matrix is not positive definite.\n")

            temp_sum = 0
            for k in range(-1, j):
                temp_sum += math.pow(L[j][k], 2)
            if (self[j][j] - temp_sum) < 0:
                raise ValueError("Operand under square root is not positive. Matrix is not positive definite, exiting.")
            L[j][j] = math.sqrt(self[j][j] - temp_sum)

            temp_sum = 0
            for i in range(j + 1, n):
                for k in range(-1, j):
                    temp_sum += L[i][k] * L[j][k]
                L[i][j] = (self[i][j] - temp_sum) / L[j][j]
        # Now L and LT are all obtained, we can move to forward elimination

        y_vec = [[None for _ in range(1)] for _ in range(n)]
        y = matrix(y_vec, n, 1)
        for i in range(y.rows):
            temp_sum = 0
            if i > 0:
                for j in range(i):
                    temp_sum += L[i][j] * y[j][0]
                y[i][0] = (b[i][0] - temp_sum) / L[i][i]
            else:
                y[i][0] = b[i][0] / L[i][i]

        # Now perform back substitution to find x.
        x_vec = [[None for _ in range(1)] for _ in range(n)]
        x = matrix(x_vec, n, 1)

        for i in range(n - 1, -1, -1):
            temp_sum = 0
            for j in range(i + 1, n):
                temp_sum += L[j][i] * x[j][0]
            x[i][0] = (y[i][0] - temp_sum) / L[i][i]

        return x

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
