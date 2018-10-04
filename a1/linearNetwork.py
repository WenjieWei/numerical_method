from matrix import Matrix
from choleski import choleski_decomposition, check_choleski
import os
import csv


class LinearResistiveNetwork(object):
    def __init__(self, num, b, n):
        self._num = num
        self._b = b
        self._n = n

        _j_vec = [[0] for _ in range(b)]
        self._J = Matrix(_j_vec, b, 1)
        _e_vec = [[0] for _ in range(b)]
        self._E = Matrix(_e_vec, b, 1)


def read_circuits():
    """
    This is the method to read the circuit information that is contained in csv files in a directory.
    Upon success, the method will create the required calculation information such as J, E, vectors
    and reduced indices matrices.

    :return: a LinearResistiveNetwork object containing the key matrices for calculations.
    """
    with open('tc_1.csv') as csv_file:
        # Use CSV reader to read from circuit files
        # row[0] = branch ID
        # row[1] = start node ID
        # row[2] = end node ID
        # row[3] = J value of a branch
        # row[4] = R value of a branch
        # row[5] = E value of a branch
        with open('tc_1.txt') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    circuit_id = int(row[0])
                    line_count += 1
                elif line_count == 1:



if __name__ == "__main__":
    pass
