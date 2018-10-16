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


def solve_chol(A, b, half_bandwidth=None):
    """
    This is the method implemented for solving the problem Ax = b,
    using Choleski Decomposition.

    Arguments:
        A: the matrix A, a real, S.P.D. (Symmetric positive definite) n * n matrix.
        b: Column vector with n rows.
        half_bandwidth: the half bandwidth of A.

    Returns:
        Column vector x with n rows.
    """
    if not A.is_symmetric():
        raise ValueError("Matrix must be symmetric to perform Choleski Decomposition.\n")

    if half_bandwidth is None:
        L = decomposition(A, half_bandwidth)

        # Now L and LT are all obtained, we can move to forward elimination
        y = forward_elimination(L, b, half_bandwidth)

        # Now perform back substitution to find x.
        v = backward_substitution(L, y, half_bandwidth)

    else:
        v = elimination(A, b, half_bandwidth)

    return v


def decomposition(A, half_bandwidth=None):
    n = A.rows
    empty_matrix = [[0 for _ in range(n)] for _ in range(n)]
    L = Matrix(empty_matrix, n, n)

    if half_bandwidth is None:
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
    else:
        for j in range(n):
            if A[j][j] <= 0:
                raise ValueError("Matrix is not positive definite.\n")

            temp_sum = 0
            k = j + 1 - half_bandwidth
            if k < 0:
                k = 0
            while k < j:
                temp_sum += math.pow(L[j][k], 2)
                k += 1

            if (A[j][j] - temp_sum) < 0:
                raise ValueError("Operand under the square root is not positive, matrix is not P.D. exiting")
            # Write the diagonal entry to matrix L
            L[j][j] = math.sqrt(A[j][j] - temp_sum)

            # Now we have found the diagonal entry
            # we move to calculate the entries below the diagonal entry, covered by HB.

            # Scenario 1: all entries below Ljj that are covered by HB are with the matrix bound.
            # However, some entries to the left covered by HB are out of bounds.
            # Scenario 2: all entries below and to the left of Ljj covered by HB are within the matrix bounds.
            # Scenario 3: some entries below Ljj are out of bounds,
            # but the entries to the left are within bounds.
            for i in range(j + 1, j + half_bandwidth):
                if i >= n:
                    break
                temp_sum = 0
                k = j + 1 - half_bandwidth
                if k < 0:
                    k = 0
                while k < j:
                    temp_sum += L[i][k] * L[j][k]
                    k += 1
                L[i][j] = (A[i][j] - temp_sum) / L[j][j]

    return L


def forward_elimination(L, b, half_bandwidth=None):
    n = L.rows
    y_vec = [[None for _ in range(1)] for _ in range(n)]
    y = Matrix(y_vec, n, 1)

    if half_bandwidth is None:
        for i in range(y.rows):
            temp_sum = 0
            if i > 0:
                for j in range(i):
                    temp_sum += L[i][j] * y[j][0]
                y[i][0] = (b[i][0] - temp_sum) / L[i][i]
            else:
                y[i][0] = b[i][0] / L[i][i]
    else:
        for i in range(y.rows):
            temp_sum = 0
            j = i + 1 - half_bandwidth
            if j < 0:
                j = 0
            while j < i:
                temp_sum += L[i][j] * y[j][0]
                j += 1

            y[j][0] = (b[j][0] - temp_sum) / L[i][i]

    return y


def elimination(A, b, half_bandwidth=None):
    n = A.rows
    for j in range(n):
        if A[j][j] <= 0:
            raise ValueError("Diagonal Entry is not positive, matrix is not P.D.")

        A[j][j] = math.sqrt(A[j][j])
        b[j][0] = b[j][0] / A[j][j]

        if half_bandwidth is None:
            finish_line = n
        else:
            if j + half_bandwidth <= n:
                finish_line = j + half_bandwidth
            else:
                finish_line = n

        for i in range(j + 1, finish_line):
            A[i][j] = A[i][j] / A[j][j]
            b[i][0] = b[i][0] - A[i][j] * b[j][0]

            for k in range(j + 1, i + 1):
                A[i][k] = A[i][k] - A[i][j] * A[k][j]

    x = backward_substitution(A, b, half_bandwidth)
    return x


def backward_substitution(L, y, half_bandwidth=None):
    n = L.rows
    x_vec = [[0 for _ in range(1)] for _ in range(n)]
    x = Matrix(x_vec, n, 1)

    for i in range(n - 1, -1, -1):
        temp_sum = 0
        for j in range(i + 1, n):
            temp_sum += L[j][i] * x[j][0]
        x[i][0] = (y[i][0] - temp_sum) / L[i][i]

    return x


if __name__ == "__main__":
    a_vec = [[6, 15, 55], [15, 55, 225], [55, 225, 979]]
    b_vec = [[0], [0.6667], [0]]

    A = Matrix(a_vec, 3, 3)
    b = Matrix(b_vec, 3, 1)

    x = solve_chol(A, b)
    if check_choleski(A, b, x):
        print("Correct")
    else:
        print("Incorrect")
