import math
from matrix import Matrix


def check_choleski(A, b, x):
    """
    This method checks if the result of the choleski decomposition is correct.
    Precision is set to 0.001.

    :param A: n by n matrix A
    :param b: result vector, n by 1
    :param x: x vector, n by 1

    :return: True if the result is correct, other wise False
    """
    temp_result = A.dot_product(x)
    print("Matrix A is:")
    A.print_matrix()
    print("Vector b is:")
    b.print_matrix()
    print("Result vector x is:")
    x.print_matrix()

    for i in range(temp_result.rows):
        for j in range(temp_result.cols):
            if abs(temp_result[i][j] - b[i][j]) >= 0.001:
                return False
    return True


def choleski_decomposition(A, b):
    """
    This is the method implemented for solving the problem Ax = b,
    using Choleski Decomposition.

    Arguments:
        A: the matrix A, a real, S.P.D. (Symmetric positive definite) n * n matrix.
        b: Column vector with n rows.

    Returns:
        Column vector x with n rows.
    """
    if not A.is_symmetric():
        raise ValueError("Matrix must be symmetric to perform Choleski Decomposition.\n")

    n = A.rows
    sparse_matrix = [[0 for _ in range(n)] for _ in range(n)]
    L = Matrix(sparse_matrix, n, n)

    for j in range(n):
        if A[j][j] <= 0:
            raise ValueError("Matrix is not positive definite.\n")

        temp_sum = 0
        for k in range(-1, j):
            temp_sum += math.pow(L[j][k], 2)
        if (A[j][j] - temp_sum) < 0:
            raise ValueError("Operand under square root is not positive. Matrix is not positive definite, exiting.")
        L[j][j] = math.sqrt(A[j][j] - temp_sum)

        for i in range(j + 1, n):
            temp_sum = 0
            for k in range(-1, j):
                temp_sum += L[i][k] * L[j][k]
            L[i][j] = (A[i][j] - temp_sum) / L[j][j]
    # Now L and LT are all obtained, we can move to forward elimination

    y_vec = [[None for _ in range(1)] for _ in range(n)]
    y = Matrix(y_vec, n, 1)
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
    x = Matrix(x_vec, n, 1)

    for i in range(n - 1, -1, -1):
        temp_sum = 0
        for j in range(i + 1, n):
            temp_sum += L[j][i] * x[j][0]
        x[i][0] = (y[i][0] - temp_sum) / L[i][i]

    return x


if __name__ == "__main__":
    a_vec = [[0.1167, -0.0667, 0, -0.05, 0], [-0.0667, 0.2333, -0.1, 0, 0], [0, -0.1, 0.2667, -0.1, 0], [-0.05, 0, -0.1, 0.2, -0.05], [0, 0, 0, -0.05, 0.1167]]
    b_vec = [[0], [0.6667], [0], [0], [0]]

    A = Matrix(a_vec, 5, 5)
    b = Matrix(b_vec, 5, 1)

    x = choleski_decomposition(A, b)
    if check_choleski(A, b, x):
        print("Correct")
    else:
        print("Incorrect")
