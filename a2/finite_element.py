from matrix import Matrix
import csv


LOW_VOLTAGE = 0
HIGH_VOLTAGE = 110
TOTAL_WIDTH = 0.2
TOTAL_HEIGHT = 0.2

class Node(object):
    def __init__(self, x, y, value):
        self._x = x
        self._y = y
        self._value = value
        self._is_free = True

    def set_free(self):
        self._is_free = True

    def set_fixed(self):
        self._is_free = False

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y

    def set_value(self, value):
        self._value = value

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def value(self):
        return self._value

    @property
    def is_free(self):
        return self._is_free


class TriangleGroup(object):
    def __init__(self, tl_x, tl_y, spacing):
        self._node_list = [None for _ in range(6)]
        self._tl_x = tl_x
        self._tl_y = tl_y
        self._spacing = spacing

    def construct_group(self):
        spacing = self._spacing
        temp_node = Node(self._tl_x, self._tl_y, 0)
        if self._tl_x == 0:
            # Set vertex 0
            temp_node.set_fixed()
            self._node_list[0] = temp_node

            # Set vertex 1
            temp_node.set_x(self._tl_x + spacing)
            if self._tl_y != 0:
                temp_node.set_free()
            else:
                temp_node.set_fixed()
            self._node_list[1] = temp_node

            # Set vertex 2
            temp_node.set_free()
            temp_node.set_y(self._tl_y + spacing)
            self._node_list[2] = temp_node

            # Set vertex 3
            temp_node.set_fixed()
            temp_node.set_x(self._tl_x)
            self._node_list[3] = temp_node

            # Set vertices 4 and 5
            self._node_list[4] = self._node_list[0]
            self._node_list[5] = self._node_list[2]

        elif (self._tl_x + spacing) == 0.08:
            # Set vertex 0
            temp_node.set_free()
            temp_node.set_value(0)
            self._node_list[0] = temp_node

            # Set vertex 1
            temp_node.set_x(self._tl_x + spacing)
            if self._tl_y == 0:
                temp_node.set_fixed()
                self._node_list[1] = temp_node
            elif self._tl_y >= 0.06:
                temp_node.set_fixed()
                temp_node.set_value(HIGH_VOLTAGE)
                self._node_list[1] = temp_node
            else:
                temp_node.set_free()
                self._node_list[1] = temp_node

            # Set vertex 2
            temp_node.set_y(self._tl_y + spacing)
            if self._tl_y == 0:
                temp_node.set_free()
                self._node_list[2] = temp_node
            elif self._tl_y >= 0.04:
                temp_node.set_fixed()
                temp_node.set_value(HIGH_VOLTAGE)
                self._node_list[2] = temp_node
            else:
                temp_node.set_free()
                self._node_list[2] = temp_node

            # Set vertex 3
            temp_node.set_x(self._tl_x)
            temp_node.set_free()
            temp_node.set_value(0)
            self._node_list[3] = temp_node

            # Set vertex 4 and 5
            self._node_list[4] = self._node_list[0]
            self._node_list[5] = self._node_list[2]


class TwoElementMesh(object):
    def __init__(self, spacing, quarter, width, height):
        self._spacing = spacing
        self._quarter = quarter
        self._width = width / 2
        self._height = height / 2

    def construct_mesh(self):
        spacing = self._spacing

        if self._quarter == 2:
            # if width % spacing != 0 or height % spacing != 0:
            #    raise ValueError("Width or height must be divisible by spacing.")

            num_tri_group_row = self._width / spacing
            num_tri_group_col = self._height / spacing

    def print_mesh(self):
        pass

    def write_input_to_csv(self):
        pass

if __name__ == "__main__":
    spacing = 0.02
    quarter = 2

    mesh = TwoElementMesh(spacing, quarter)