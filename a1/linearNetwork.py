from matrix import Matrix
from choleski import choleski_decomposition, check_choleski
import os
import csv


class LinearResistiveNetwork(object):
    def __init__(self, num, branch, node, a, y, j, e):
        self._num = num
        self._branch_number = branch
        self._node_number = node
        self._curr_vec = j
        self._volt_vec = e
        self._red_ind_mat = a
        self._rev_res_mat = y

    def solve_circuit(self):
        return choleski_decomposition(self.A, self.b)

    @property
    def J(self):
        return self._curr_vec

    @property
    def E(self):
        return self._volt_vec

    @property
    def Y(self):
        return self._rev_res_mat

    @property
    def A(self):
        return self._red_ind_mat.dot_product(self.Y.dot_product(self._red_ind_mat.T))

    @property
    def b(self):
        YE = self.Y.dot_product(self.E)
        J_YE = self.J.minus(YE)
        result = self.A.dot_product(J_YE)
        return result


def read_circuits():
    """
    This is the method to read the circuit information that is contained in csv files in a directory.
    Upon success, the method will create the required calculation information such as J, E, vectors
    and reduced indices matrices.

    :return: a LinearResistiveNetwork object containing the key matrices for calculations.
    """
    with open('tc_2.csv') as csv_file:
        # Use CSV reader to read from circuit files
        # row[0] = start node ID
        # row[1] = end node ID
        # row[2] = J value of a branch
        # row[3] = R value of a branch
        # row[4] = E value of a branch
        csv_reader = csv.reader(csv_file, delimiter=',')
        row = next(csv_reader)
        circuit_id = int(row[0])
        n_branch = int(row[2])
        n_node = int(row[4])

        branch_id = 0
        current_vec = [[0] for _ in range(n_branch)]
        volt_vec = [[0] for _ in range(n_branch)]
        rev_res_mat = [[0 for _ in range(n_branch)] for _ in range(n_branch)]
        incident_mat = [[0 for _ in range(n_branch)] for _ in range(n_node)]

        j_vec = Matrix(current_vec, n_branch, 1)
        e_vec = Matrix(volt_vec, n_branch, 1)
        y_mat = Matrix(rev_res_mat, n_branch, n_branch)
        a_mat = Matrix(incident_mat, n_node, n_branch)

        for row in csv_reader:
            j_vec[branch_id][0] = float(row[2])
            e_vec[branch_id][0] = float(row[4])
            if int(row[3]) != 0:
                y_mat[branch_id][branch_id] = 1 / float(row[3])
            else:
                print("The input resistance is 0.")

            # create un-reduced A matrix
            a_mat[int(row[0])][branch_id] = 1
            a_mat[int(row[1])][branch_id] = -1

            branch_id += 1

        # By default, Node 0 is grounded, remove node 0
        # and create new reduced incidence matrix
        a_mat = Matrix(a_mat.vec[1:], n_node - 1, n_branch)

        linear_network = LinearResistiveNetwork(circuit_id, n_branch, n_node, a_mat, y_mat, j_vec, e_vec)
        return linear_network


if __name__ == "__main__":
    network = read_circuits()
    x = network.solve_circuit()
    x.print_matrix()