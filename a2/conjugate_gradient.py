from finite_difference import Node
from matrix import Matrix
from choleski import solve_chol
import math, csv, os, time

TOLERANCE = 1e-5

def third_quarter_node_gen():
    """
    This method generates a matrix for the nodes in the third quadrant

    :return: Matrix containing the nodes in the 3rd quadrant
    """
    temp_vec = [[None for _ in range(6)] for _ in range(6)]
    node_matrix = Matrix(temp_vec, 6, 6)
    counter = 0
    free_node_counter = 0
    fix_node_counter = 0

    for i in range(5, -1, -1):
        for j in range(6):
            temp_node = Node(0, counter)
            if i == 0 and j >= 4:
                pass
            elif j == 0 or i == 5:
                temp_node.set_fixed()
                node_matrix[i][j] = temp_node
                fix_node_counter += 1
            elif i <= 1 and j >= 3:
                temp_node.set_value(110)
                temp_node.set_fixed()
                node_matrix[i][j] = temp_node
                fix_node_counter += 1
            else:
                node_matrix[i][j] = temp_node
                free_node_counter += 1
            counter += 1

    return node_matrix, free_node_counter, fix_node_counter

def free_node_fd_gen(free_nodes_matrix, num_free_node):
    # remove the fixed nodes and change the id of the free nodes
    id = 0
    for i in range(5, -1, -1):
        for j in range(6):
            temp_node = free_nodes_matrix[i][j]
            if temp_node is not None:
                if not temp_node.is_free:
                    free_nodes_matrix[i][j] = None
                else:
                    temp_node.set_id(id)
                    id += 1

    # create the finite difference matrix for the free nodes
    fd_vec = [[0 for _ in range(num_free_node)] for _ in range(num_free_node)]
    fd_matrix = Matrix(fd_vec, num_free_node, num_free_node)

    for i in range(5, -1, -1):
        for j in range(6):
            temp_node = free_nodes_matrix[i][j]
            if temp_node is not None:
                k = temp_node.id
                fd_matrix[k][k] = -4

                # inspect the left node
                if j > 0:
                    if free_nodes_matrix[i][j - 1] is not None:
                        fd_matrix[k][k - 1] += 1

                # inspect the bottom node
                if i < 5:
                    if free_nodes_matrix[i + 1][j] is not None:
                        bottom_node = free_nodes_matrix[i + 1][j]
                        fd_matrix[bottom_node.id][k] += 1

                # inspect the right node
                if j < 5:
                    if free_nodes_matrix[i][j + 1] is not None:
                        fd_matrix[k][k + 1] += 1
                else:
                    fd_matrix[k][k - 1] += 1

                # inspect the top node
                if i > 0:
                    if free_nodes_matrix[i - 1][j] is not None:
                        top_node = free_nodes_matrix[i - 1][j]
                        fd_matrix[top_node.id][k] += 1
                else:
                    top_node = free_nodes_matrix[i + 1][j]
                    fd_matrix[k][top_node.id] += 1

    v_vec = [[0] for _ in range(num_free_node)]
    v_matrix = Matrix(v_vec, num_free_node, 1)

    v_matrix[18][0] = -110
    v_matrix[16][0] = -110
    v_matrix[14][0] = -110
    v_matrix[13][0] = -110
    v_matrix[12][0] = -110

    return fd_matrix, v_matrix

def solve_cg(A, b):
    x_vec = [[0] for _ in range(b.rows)]
    x = Matrix(x_vec, b.rows, 1)

    r = b.minus(A.dot_product(x))
    p = r.clone()

    r_list = []
    p_list = []
    x_list = []

    r_list.append(r)
    p_list.append(p)
    x_list.append(x)

    iteration = 0
    while True:
        iteration += 1
        alpha = p.T.dot_product(r)[0][0] / p.T.dot_product(A.dot_product(p))[0][0]

        ap = p.clone()
        for i in range(p.rows):
            ap[i][0] = alpha * p[i][0]
        x = x_list[iteration - 1].add(ap)
        x_list.append(x)

        r = b.minus(A.dot_product(x))
        if iteration != 1:
            r_list.append(r)
        else:
            pass

        pAr = p.T.dot_product(A.dot_product(r))
        pAp = p.T.dot_product(A.dot_product(p))
        beta = - pAr[0][0] / pAp[0][0]

        old_p = p.clone()
        for i in range(p.rows):
            old_p[i][0] = p[i][0] * beta
        p = r.add(old_p)
        p_list.append(p)

        residual = r.T.dot_product(r)[0][0]
        if math.sqrt(residual) < TOLERANCE:
            break

    return x, iteration, r_list

if __name__ == "__main__":
    os.chdir('outputs')
    node_matrix, free_node_counter, fix_node_counter = third_quarter_node_gen()

    free_nodes = node_matrix.clone()
    fd_matrix, v = free_node_fd_gen(free_nodes, free_node_counter)

    A = fd_matrix.T.dot_product(fd_matrix)
    b = fd_matrix.T.dot_product(v)

    x = solve_chol(A, b)
    x_cg, iterations, r_list = solve_cg(A, b)

    with open('cg_result.csv', 'w', newline='') as csv_file:
        row_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONE, escapechar=' ')
        row_writer.writerow(['$x$', '$y$', 'Choleski', 'CG'])

        x_coord = 0.02
        y_coord = 0.02

        for i in range(19):
            row_writer.writerow(['%.2f, %.2f' % (x_coord, y_coord), str(x[i][0]), str(x_cg[i][0])])
            x_coord += 0.02
            if y_coord == 0.08 and x_coord > 0.04:
                x_coord = 0.02
                y_coord += 0.02
            elif (i + 1) % 5 == 0 and i != 0:
                y_coord += 0.02
                x_coord = 0.02
    csv_file.close()

    with open('norm.csv', 'w', newline='') as csv_file:
        row_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONE, escapechar=' ')
        row_writer.writerow(['iterations', 'inf-norm', '2-norm'])

        count = 1
        for residual in r_list:
            max = 0
            two_norm = 0
            for i in range(residual.rows):
                if residual[i][0] > max:
                    max = residual[i][0]

                two_norm += residual[i][0] ** 2

            two_norm = math.sqrt(two_norm)
            row_writer.writerow([str(count), str(max), str(two_norm)])
            count += 1
    csv_file.close()
    print("File writing complete.")
