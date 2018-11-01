from matrix import Matrix
from finite_difference import Node

HIGH_VOLTAGE = 110
LOW_VOLTAGE = 0
SPACING = 0.02
f = open('file.dat', 'w')


class two_element(object):
    def __init__(self, x, y):
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

if __name__ == "__main__":
    fe_vec = [[None for _ in range(5)] for _ in range(5)]
    fe_matrix = Matrix(fe_vec, 5, 5)

    y_coord = 0.08
    count = 0

    print("Creating the mesh of the finite elements...")
    for i in range(5):
        x_coord = 0
        for j in range(5):
            if x_coord >= 0.06 and y_coord == 0.08:
                break
            else:
                temp_two_element = two_element(x_coord, y_coord)
                fe_matrix[i][j] = temp_two_element
                count += 1

            x_coord += SPACING
        y_coord -= SPACING

    print("Finite elements created: " + str(count * 2))

    node_count = 1
    x_coord = 0
    y_coord = 0
    for i in range(4, -1, -1):
        for j in range(5):
            temp_two_element = fe_matrix[i][j]

            if temp_two_element is not None:
                pass
            else:
                break