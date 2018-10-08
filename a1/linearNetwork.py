from matrix import Matrix
from choleski import solve_chol
import csv, math, time, os


class LinearResistiveNetwork(object):
    def __init__(self, num, branch, node, a, y, j, e, size):
        self._num = num
        self._branch_number = branch
        self._node_number = node
        self._curr_vec = j
        self._volt_vec = e
        self._red_ind_mat = a
        self._rev_res_mat = y
        self._size = size

    def solve_circuit_banded(self):
        return solve_chol(self.A, self.b, self.size + 1)

    def solve_circuit(self):
        return solve_chol(self.A, self.b)

    @property
    def size(self):
        return self._size

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
    def re_A(self):
        return self._red_ind_mat

    @property
    def A(self):
        return self.re_A.dot_product(self.Y.dot_product(self.re_A.T))

    @property
    def b(self):
        YE = self.Y.dot_product(self.E)
        J_YE = self.J.minus(YE)
        result = self.re_A.dot_product(J_YE)
        return result


def read_circuits(filename):
    """
    This is the method to read the circuit information that is contained in csv files in a directory.
    Upon success, the method will create the required calculation information such as J, E, vectors
    and reduced indices matrices.

    :return: a LinearResistiveNetwork object containing the key matrices for calculations.
    """
    with open(filename) as csv_file:
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
        size = int(math.sqrt(n_node))

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

        linear_network = LinearResistiveNetwork(circuit_id, n_branch, n_node, a_mat, y_mat, j_vec, e_vec, size)
        return linear_network


def network_constructor(size):
    """
    This method generates a linear resistive network.
    The size of the network is defined by the argument size, and it's an N*N square network.

    This method generates a new input .csv file, for future uses.

    :param size: a.k.a, N, the number of nodes in a row or in a column.
    :return: No return value.
    """
    n_node = int(math.pow(size, 2))
    n_branch = 2 * size * (size - 1) + 1
    resistance = 1000
    test_current = 10
    res_branch = 1000

    row_count = 0
    node_id = 0

    first_row = [str(size), 'B', str(n_branch), 'N', str(n_node)]
    first_branch = [str(n_node - 1), '0', str(test_current), str(res_branch), '0']
    general_branch = [None for _ in range(5)]

    with open('res_mesh' + str(size) + '.csv', 'w', newline='') as csv_file:
        row_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONE, escapechar=' ')

        if row_count == 0:
            row_writer.writerow(r for r in first_row)
            row_writer.writerow(r for r in first_branch)
            row_count += 2

        for row_count in range(row_count, n_branch):
            if node_id == n_node - 1:
                break

            elif (node_id + 1) % size == 0:
                general_branch[0] = str(node_id)
                general_branch[1] = str(node_id + size)
                general_branch[2] = '0'
                general_branch[3] = str(resistance)
                general_branch[4] = '0'
                row_writer.writerow(r for r in general_branch)

            elif (node_id + size) >= n_node:
                general_branch[0] = str(node_id)
                general_branch[1] = str(node_id + 1)
                general_branch[2] = '0'
                general_branch[3] = str(resistance)
                general_branch[4] = '0'
                row_writer.writerow(r for r in general_branch)

            else:
                general_branch[0] = str(node_id)
                general_branch[1] = str(node_id + 1)
                general_branch[2] = '0'
                general_branch[3] = str(resistance)
                general_branch[4] = '0'
                row_writer.writerow(r for r in general_branch)

                general_branch[0] = str(node_id)
                general_branch[1] = str(node_id + size)
                general_branch[2] = '0'
                general_branch[3] = str(resistance)
                general_branch[4] = '0'
                row_writer.writerow(r for r in general_branch)
            node_id += 1


if __name__ == "__main__":
    os.chdir('circuits')
    with open('result.csv', 'w', newline='') as csv_file:
        row_writer = csv.writer(csv_file, delimiter='\t', quoting=csv.QUOTE_NONE, escapechar=' ')
        first_row = ['size', '', 'Resistance', 'Time of Calculation']
        row_writer.writerow(r for r in first_row)
        for size in range(2, 16):
            print("Writing result of N = " + str(size) + ", banded = False")
            start_time_unbanded = time.time()

            network = read_circuits('res_mesh' + str(size) + '.csv')
            x_unbanded = network.solve_circuit()

            v = x_unbanded[x_unbanded.rows - 1][0]
            i1 = v / 1000
            i2 = 10 - i1
            resistance = v / i2
            finish_time_unbanded = time.time()
            result_arr = [str(size), 'unbanded', str(resistance), str(finish_time_unbanded - start_time_unbanded)]
            row_writer.writerow(r for r in result_arr)

            print("Writing result of N = " + str(size) + ", banded = True")
            start_time_banded = time.time()
            x_banded = network.solve_circuit_banded()

            v = x_banded[x_banded.rows - 1][0]
            i1 = v / 1000
            i2 = 10 - i1
            banded_resistance = v / i2
            finish_time_banded = time.time()
            result_arr = [str(size), 'banded', str(resistance), str(finish_time_banded - start_time_banded)]
            row_writer.writerow(r for r in result_arr)
    """
    size = 12
    print("N="+str(size))
    start_time_unbanded = time.time()

    network = read_circuits('res_mesh' + str(size) + '.csv')
    x_unbanded = network.solve_circuit()

    v = x_unbanded[x_unbanded.rows - 1][0]
    i1 = v / 1000
    i2 = 10 - i1
    resistance = v / i2
    finish_time_unbanded = time.time()
    print("R=" +str(resistance))
    print("t=" +str(finish_time_unbanded - start_time_unbanded))

    start_time_banded = time.time()
    x_banded = network.solve_circuit_banded()

    v = x_banded[x_banded.rows - 1][0]
    i1 = v / 1000
    i2 = 10 - i1
    banded_resistance = v / i2
    finish_time_banded = time.time()
    print("R=" +str(resistance))
    print("t=" +str(finish_time_banded - start_time_banded))
"""