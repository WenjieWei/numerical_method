import math
from matrix import matrix


def choleski_decomp(A, b):
    """
    This is the main class implemented for solving the problem Ax = b,
    using Cholesky Decomposition.

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
        if A[j][j] < 0:
            raise ValueError("Matrix is not positive definite.\n")

        temp_sum = 0
        for k in range(-1, j):
            temp_sum += math.pow(L[j][k], 2)
        if (A[j][j] - temp_sum) < 0:
            raise ValueError("Operand in sqrt must be positive at j = %d." % j)
        L[j][j] = math.sqrt(A[j][j] - temp_sum)
        temp_sum = 0
        for i in range(j+1, n):
            for k in range(-1, j-1):
                temp_sum += L[i][k] * L[j][k]
            L[i][j] = (A[i][j] - temp_sum) / L[j][j]



if __name__ == "__main__":
    a = [[15.0, -5.0, 0.0, -5.0], [-5.0, 12.0, -2.0, 0.0], [0.0, -2.0, 6.0, -2.0], [-5.0, 0.0, -2.0, 9.0]]
    b = [[1, 2, 3]]
    A = matrix(a, 4, 4)
    A.print_matrix_property()
    choleski_decomp(A, b)

    #matrix.print_matrix_property()