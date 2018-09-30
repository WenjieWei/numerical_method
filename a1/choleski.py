import math
from matrix import matrix


def choleski_decomposition(A, b):
    """
    This is the method implemented for solving the problem Ax = b,
    using Choleski Decomposition.

    Arguments:
        A: A real, S.P.D. (Symmetric positive definite) n * n matrix.
        b: Column vector with n rows.

    Returns:
        Column vector x with n rows.
    """
    if not A.is_symmetric():
        raise ValueError("Matrix must be symmetric to perform Choleski Decomposition.\n")

    n = A.rows
    sparse_matrix = [[0 for _ in range(n)] for _ in range(n)]
    L = matrix(sparse_matrix, n, n)

    for j in range(n):
        if A[j][j] <= 0:
            raise ValueError("Matrix is not positive definite.\n")

        temp_sum = 0
        for k in range(-1, j):
            temp_sum += math.pow(L[j][k], 2)
        if (A[j][j] - temp_sum) < 0:
            raise ValueError("Operand under square root is not positive. Matrix is not positive definite, exiting.")
        L[j][j] = math.sqrt(A[j][j] - temp_sum)

        temp_sum = 0
        for i in range(j + 1, n):
            for k in range(-1, j):
                temp_sum += L[i][k] * L[j][k]
            L[i][j] = (A[i][j] - temp_sum) / L[j][j]
    L.print_matrix_property()
    # Now L and L transpose are all obtained, we can move to forward elmination

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

    # y.print_matrix_property()
    # Now perform back substitution to find x.

    x_vec = [[0 for _ in range(1)] for _ in range(n)]
    x = matrix(x_vec, n, 1)

    for i in range(n - 1, -1, -1):
        temp_sum = 0
        for j in range(i + 1, n):
            temp_sum += L[j][i] * x[j][0]
        x[i][0] = (y[i][0] - temp_sum) / L[i][i]

    return x


if __name__ == "__main__":
    a_vec = [[15, -5, 0, -5], [-5, 12, -2, 0], [0, -2, 6, -2], [-5, 0, -2, 9]]
    b_vec = [[115], [22], [-51], [13]]

    # test matrix x = [12; 6; -5; 7]
    A = matrix(a_vec, 4, 4)
    b = matrix(b_vec, 4, 1)
    # A.print_matrix_property()
    x = choleski_decomposition(A, b)
    x.print_matrix_property()

    # matrix.print_matrix_property()
