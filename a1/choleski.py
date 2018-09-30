import os
from matrix import matrix


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


def readCircuit(filename):
    direct = os.getcwd()

    f = open(direct + "/circuits/"+filename, 'r')
    for x in f:
        print(x)


if __name__ == "__main__":
    a_vec = [[15, -5, 0, -5], [-5, 12, -2, 0], [0, -2, 6, -2], [-5, 0, -2, 9]]
    b_vec = [[115], [22], [-51], [13]]

    A = matrix(a_vec, 4, 4)
    b = matrix(b_vec, 4, 1)

    x = A.choleski_decomposition(b)
    if check_choleski(A, b, x):
        print("Correct")
    else:
        print("Incorrect")

    """
    a_vec = [[2, -1, 0], [-1, 2, -1], [0, -1, 2]]
    b_vec = [[115], [22], [-51]]

    A = matrix(a_vec, 3, 3)
    b = matrix(b_vec, 3, 1)

    x = A.choleski_decomposition(b)
    if check_choleski(A, b, x):
        print("Correct")
    else:
        print("Incorrect")
    """

    readCircuit("circuit_org.txt")
