from matrix import Matrix
from finite_difference import Node

EPSILON = 8.854188e-12
HIGH_VOLTAGE = 110
LOW_VOLTAGE = 0
SPACING = 0.02
s_vec = [[1, -0.5, 0, -0.5],[-0.5, 1, -0.5, 0],[0, -0.5, 1, -0.5],[-0.5, 0, -0.5, 1]]
S = Matrix(s_vec, 4, 4)
f = open('SIMPLE2Dinput.dat', 'w')


class two_element(object):
    def __init__(self, x, y, bl_node, id):
        """
        This is the constructor of a two-triangle finite element
        the vertices are numbered from 0 to 5, replacing 1 - 6 in question 1

        :param x: x coord for the bottom-left corner
        :param y: y coord for the bottom-left corner
        """

        # vertices are put in the array
        # vertices 2&5, vertices 0&4 have the same properties
        self._vertex_array = [Node(0) for _ in range(6)]
        self._vertex_array[5] = self._vertex_array[2]
        self._vertex_array[4] = self._vertex_array[0]
        self._bl_x = x
        self._bl_y = y

        self._bl_node = bl_node
        self._tl_node = bl_node + 6
        self._br_node = bl_node + 1
        self._tr_node = bl_node + 7

        self._id = id

        if (self._bl_x + SPACING) > 0.1 or (self._bl_y + SPACING) > 0.1:
            raise ValueError("The finite elements cannot exceed the third quadrant!")

        if self._bl_y == 0:
            # configure node 1
            self._vertex_array[1].set_fixed()
            self._vertex_array[1].set_value(LOW_VOLTAGE)

            # configure node 2 and 5
            self._vertex_array[2].set_fixed()
            self._vertex_array[2].set_value(LOW_VOLTAGE)

            # configure node 3
            self._vertex_array[3].set_free()

            if self._bl_x == 0:
                # configure node 0 and 4
                self._vertex_array[0].set_fixed()
                self._vertex_array[0].set_value(LOW_VOLTAGE)
            else:
                self._vertex_array[0].set_free()
        elif self._bl_x >= 0.06 and self._bl_y == 0.06:
            # configure node 1
            self._vertex_array[1].set_free()

            # configure node 2 and 5
            self._vertex_array[2].set_free()

            # configure node 0 and 4
            self._vertex_array[0].set_fixed()
            self._vertex_array[0].set_value(HIGH_VOLTAGE)

            # configure node 3
            self._vertex_array[3].set_fixed()
            self._vertex_array[3].set_value(HIGH_VOLTAGE)
        elif self._bl_x == 0.04 and self._bl_y == 0.06:
            # configure node 1
            self._vertex_array[1].set_free()

            # configure node 2 and 5
            self._vertex_array[2].set_free()

            # configure node 0 and 4
            self._vertex_array[0].set_free()

            # configure node 3
            self._vertex_array[3].set_fixed()
            self._vertex_array[3].set_value(HIGH_VOLTAGE)
        elif self._bl_x == 0.04 and self._bl_y == 0.08:
            # configure node 1
            self._vertex_array[1].set_free()

            # configure node 2 and 5
            self._vertex_array[2].set_fixed()
            self._vertex_array[2].set_value(HIGH_VOLTAGE)

            # configure node 0 and 4
            self._vertex_array[0].set_free()

            # configure node 3
            self._vertex_array[3].set_fixed()
            self._vertex_array[3].set_value(HIGH_VOLTAGE)
        elif self._bl_x == 0:
            # configure node 1
            self._vertex_array[1].set_fixed()
            self._vertex_array[1].set_value(LOW_VOLTAGE)

            # configure node 0 and 4
            self._vertex_array[0].set_fixed()
            self._vertex_array[0].set_value(LOW_VOLTAGE)

            # configure node 3
            self._vertex_array[3].set_free()

            # configure node 2 and 5
            self._vertex_array[2].set_free()
        else:
            for i in range(6):
                self._vertex_array[i].set_free()

    def print_two_element(self):
        for i in range(6):
            print("Vertex " + str(i) + " has value " + str(self._vertex_array[i].value) + ", free node: "
                  + str(self._vertex_array[i].is_free))

    @property
    def bl_x(self):
        return self._bl_x

    @property
    def bl_y(self):
        return self._bl_y

    @property
    def bl_node(self):
        return self._bl_node

    @property
    def tl_node(self):
        return self._tl_node

    @property
    def br_node(self):
        return self._br_node

    @property
    def tr_node(self):
        return self._tr_node

    @property
    def vertex(self, i):
        return self._vertex_array[i]

    @property
    def id(self):
        return self._id


def calc_energy(fe_matrix):
    file = open('potentials.dat', mode='r', encoding='utf-8-sig')
    lines = file.readlines()
    file.close()
    potentials = [0 for _ in range(len(lines))]

    energy = 0

    count = 0
    for line in lines:
        line = line.split(' ')
        line = [i.strip() for i in line]
        potentials[count] = line[3]
        count += 1

    for i in range(4, -1, -1):
        for j in range(5):
            temp_two_element = fe_matrix[i][j]

            if temp_two_element is not None:
                u_vec = [[0] for _ in range(4)]
                U = Matrix(u_vec, 4, 1)

                U[0][0] = float(potentials[temp_two_element.id])
                U[1][0] = float(potentials[temp_two_element.id + 1])
                U[2][0] = float(potentials[temp_two_element.id + 6])
                U[3][0] = float(potentials[temp_two_element.id + 7])

                energy += 0.5 * EPSILON * U.T.dot_product(S).dot_product(U)[0][0]

    return energy


if __name__ == "__main__":
    fe_vec = [[None for _ in range(5)] for _ in range(5)]
    fe_matrix = Matrix(fe_vec, 5, 5)

    y_coord = 0
    count = 0

    print("Creating the mesh of the finite elements...")
    node_count = 0
    for i in range(4, -1, -1):
        x_coord = 0
        for j in range(5):
            if x_coord >= 0.06 and y_coord == 0.08:
                break
            else:
                temp_two_element = two_element(x_coord, y_coord, node_count, node_count)
                fe_matrix[i][j] = temp_two_element
                node_count += 1
                count += 1

            x_coord += SPACING
        node_count += 1
        y_coord += SPACING

    print("Finite elements created: " + str(count * 2))

    # Now write the input file for SIMPLE2D.m
    print("Writing node information...")
    # write the bottom row
    i = 4
    for j in range(5):
        temp_two_element = fe_matrix[i][j]
        f.write('%d %.3f %.3f\n' % (temp_two_element.bl_node, temp_two_element.bl_x, temp_two_element.bl_y))
        if j == 4:
            f.write('%d %.3f %.3f\n' % (temp_two_element.br_node,
                                        temp_two_element.bl_x + SPACING, temp_two_element.bl_y))

    # write the general rows
    for i in range(4, -1, -1):
        for j in range(5):
            temp_two_element = fe_matrix[i][j]
            if temp_two_element is not None:
                if i != 0 and j != 4:
                    f.write('%d %.3f %.3f\n' %
                                  (temp_two_element.tl_node, temp_two_element.bl_x, temp_two_element.bl_y + SPACING))
                elif i != 0 and j == 4:
                    f.write('%d %.3f %.3f\n' %
                                  (temp_two_element.tl_node, temp_two_element.bl_x, temp_two_element.bl_y + SPACING))
                    f.write('%d %.3f %.3f\n' %
                                  (temp_two_element.tr_node, temp_two_element.bl_x + SPACING,
                                   temp_two_element.bl_y + SPACING))
                else:
                    if j != 2:
                        f.write('%d %.3f %.3f\n' %
                                  (temp_two_element.tl_node, temp_two_element.bl_x, temp_two_element.bl_y + SPACING))
                    else:
                        f.write('%d %.3f %.3f\n' %
                                      (temp_two_element.tl_node,
                                       temp_two_element.bl_x, temp_two_element.bl_y + SPACING))
                        f.write('%d %.3f %.3f\n' %
                                      (temp_two_element.tr_node, temp_two_element.bl_x + SPACING,
                                       temp_two_element.bl_y + SPACING))
            else:
                break

    f.write('\n')
    # Now write the triangle connection
    print("Writing triangle information...")
    for i in range(4, -1, -1):
        for j in range(5):
            temp_two_element = fe_matrix[i][j]
            if temp_two_element is not None:
                f.write('%d %d %d %.3f\n' %
                    (temp_two_element.bl_node, temp_two_element.br_node, temp_two_element.tl_node, 0))
            else:
                break
        for j in range(5):
            temp_two_element = fe_matrix[i][j]
            if temp_two_element is not None:
                f.write('%d %d %d %.3f\n' %
                    (temp_two_element.tr_node, temp_two_element.tl_node, temp_two_element.br_node, 0))
            else:
                break

    f.write('\n')

    print("Writing boundary conditions")
    for i in range(4, -1, -1):
        for j in range(5):
            temp_two_element = fe_matrix[i][j]
            if temp_two_element is not None:
                if i == 4 and j != 4:
                    f.write('%d %.3f\n' % (temp_two_element.bl_node, LOW_VOLTAGE))
                elif i == 4 and j == 4:
                    f.write('%d %.3f\n' % (temp_two_element.bl_node, LOW_VOLTAGE))
                    f.write('%d %.3f\n' % (temp_two_element.br_node, LOW_VOLTAGE))
                elif i == 3 and j == 0:
                    f.write('%d %.3f\n' % (temp_two_element.bl_node, LOW_VOLTAGE))
                    f.write('%d %.3f\n' % (temp_two_element.tl_node, LOW_VOLTAGE))
                elif j == 0 and i != 3 and i != 4:
                    f.write('%d %.3f\n' % (temp_two_element.tl_node, LOW_VOLTAGE))
                elif j >= 2 and i <= 1:
                    f.write('%d %.3f\n' % (temp_two_element.tr_node, HIGH_VOLTAGE))
            else:
                break

    energy = calc_energy(fe_matrix)
    print(energy)