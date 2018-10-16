import math, csv
from matrix import Matrix


SHIELD_SIZE = 0.2
CORE_WIDTH = 0.08
CORE_HEIGHT = 0.04
CORE_VOLTAGE = 110
TOLERANCE = 0.00001

class Node(object):
    def __init__(self, value):
        self._value = value
        self._is_free = True

    def set_value(self, value):
        self._value = value

    def set_free(self):
        self._is_free = True

    def set_fixed(self):
        self._is_free = False

    @property
    def value(self):
        return self._value

    @property
    def is_free(self):
        return self._is_free

class UniformMesh(object):
    """
    This class generates a uniform mesh between the cable core and the outer shield.
    One of the corners of the mesh lies at the center of the core and the diagonal connects with a corner of the shield.
    This way we create a mesh with uniform spaced nodes with clear boundary conditions.
    """
    def __init__(self, width, height, x, y, h):
        self._width = width
        self._height = height
        self._node_distance = h

        # Coord of the bottom left corner
        self._bottom_left_x = x
        self._bottom_left_y = y

        # Coord of the bottom right
        self._bottom_right_x = x + width
        self._bottom_right_y = y

        # Coord of top left
        self._top_left_x = x
        self._top_left_y = y + height

        # Coord of top right
        self._top_right_x = x + width
        self._top_right_y = y + height

        # Calculate how many nodes are there in a row and a column.
        # Assume there is no remainder after the division.
        # Then construct a matrix for this mesh
        # The matrix has one extra row and one extra column
        # This addition can act as a buffer to the matrix, prevent out of bounds exceptions
        # Also makes use of the symmetry.
        self._row_nodes = int(width / h) + 1
        self._col_nodes = int(height / h) + 1

        self._mesh_vec = [[Node(0) for _ in range(self._row_nodes + 1)] for _ in range(self._col_nodes + 1)]
        self._mesh_matrix = Matrix(self._mesh_vec, self._row_nodes + 1, self._col_nodes + 1)

    def initialize_values_second_quadrant(self):
        """
        This method initializes a mesh in the second quadrant w.r.t. the core.
        The left most and top most boundaries are initialized and fixed to 0.
        The nodes lying on the edge of the cores are initialized to 110V.

        * Assume that width and height are completely divisible without remainder by h.
        :return: void
        """
        h = self._node_distance
        # Initialize the shield boundary conditions
        # Start from the top boundary
        i = 0
        for j in range(self.matrix.cols):
            node = self.matrix[i][j]
            node.set_value(0)
            node.set_fixed()

        # Now do the left side boundary
        j = 0
        for i in range(self.matrix.rows):
            node = self.matrix[i][j]
            node.set_value(0)
            node.set_fixed()

        # Now do the boundary of the core
        core_center_i = self.matrix.rows - 1
        core_center_j = self.matrix.cols - 1

        shift_j = int((CORE_WIDTH / 2) / h) + 1
        shift_i = int((CORE_HEIGHT / 2) / h) + 1

        core_boundary_i = core_center_i - shift_i
        core_boundary_j = core_center_j - shift_j

        for i in range(core_boundary_i, self.matrix.rows):
            for j in range(core_boundary_j, self.matrix.cols):
                node = self.matrix[i][j]
                node.set_value(CORE_VOLTAGE)
                node.set_fixed()


    def print_mesh(self):
        for i in range(self.matrix.rows):
            print("|", end=" ")
            for j in range(self.matrix.cols):
                node = self._mesh_matrix[i][j]
                print("%f" % node.value, end=" ")
            print("|")

    def copy_mesh(self):
        new_mesh = UniformMesh(self._width, self._height,
                               self._bottom_left_x, self._bottom_left_y, self._node_distance)
        for i in range(self.matrix.rows):
            for j in range(self.matrix.cols):
                new_node = new_mesh.matrix[i][j]
                old_node = self.matrix[i][j]
                new_node.set_value(old_node.value)
                if old_node.is_free:
                    new_node.set_free()
                else:
                    new_node.set_fixed()
        return new_mesh

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def bottom_left(self):
        return self._bottom_left_x, self._bottom_left_y

    @property
    def bottom_right(self):
        return self._bottom_right_x, self._bottom_right_y

    @property
    def top_left(self):
        return self._top_left_x, self._top_left_y

    @property
    def top_right(self):
        return self._top_right_x, self._top_right_y

    @property
    def matrix(self):
        return self._mesh_matrix

    @property
    def width_nodes(self):
        return self._row_nodes

    @property
    def height_nodes(self):
        return self._col_nodes

def successive_over_relaxation(mesh, omega, uni_spacing=True):
    iteration = 0
    new_mesh = mesh.copy_mesh()

    if uni_spacing:
        while not relaxation_succeeded(mesh, new_mesh):
            mesh = new_mesh.copy_mesh()
            new_mesh = mesh.copy_mesh()
            iteration += 1
            for i in range(mesh.width_nodes):
                for j in range(mesh.height_nodes):
                    if mesh.matrix[i][j].is_free:
                        sum = (new_mesh.matrix[i - 1][j].value +
                               new_mesh.matrix[i][j - 1].value +
                               mesh.matrix[i + 1][j].value +
                               mesh.matrix[i][j + 1].value)

                        temp_val = mesh.matrix[i][j].value
                        overwrite = (1 - omega) * temp_val + omega * sum * 0.25
                        new_mesh.matrix[i][j].set_value(overwrite)

                    # Deal with symmetry on y
                    if i == (mesh.matrix.rows - 3):
                        new_node = new_mesh.matrix[i + 2][j]
                        old_node = mesh.matrix[i][j]
                        new_node.set_value(old_node.value)
                        if not old_node.is_free:
                            new_node.set_fixed()

                    # Deal with symmetry on x
                    if j == (mesh.matrix.rows - 3):
                        new_node = new_mesh.matrix[i][j + 2]
                        old_node = mesh.matrix[i][j]
                        new_node.set_value(old_node.value)
                        if not old_node.is_free:
                            new_node.set_fixed()

                    # Deal with symmetry on the corner
                    if j == (mesh.matrix.rows - 3) and i == (mesh.matrix.rows - 3):
                        new_node = new_mesh.matrix[i + 2][j + 2]
                        old_node = mesh.matrix[i][j]
                        new_node.set_value(old_node.value)
                        if not old_node.is_free:
                            new_node.set_fixed()

    else:
        pass

    return iteration, mesh

def relaxation_succeeded(mesh, new_mesh):
    for i in range(mesh.width_nodes):
        for j in range(mesh.height_nodes):
            if mesh.matrix[i][j].is_free:
                residual = abs(new_mesh.matrix[i - 1][j].value
                               + new_mesh.matrix[i][j - 1].value
                               + new_mesh.matrix[i + 1][j].value
                               + new_mesh.matrix[i][j + 1].value
                               - 4 * new_mesh.matrix[i][j].value)
                if residual > TOLERANCE:
                    return False
    return True

if __name__ == "__main__":
    h = 0.02
    print("Now performing FD on a uniform spacing mesh with h = " + str(h))
    rect = UniformMesh(0.1, 0.1, 0, 0.1, h)
    rect.initialize_values_second_quadrant()

    omega_list = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]
    list_iteration = [0 for _ in range(10)]

    first_row = ['omega', 'value', 'iterations']
    row = [0 for _ in range(3)]

    with open('w_result.csv', 'w', newline='') as csv_file:
        row_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONE, escapechar=' ')
        row_writer.writerow(r for r in first_row)

        for i in range(10):
            omega = omega_list[i]
            iteration, result = successive_over_relaxation(rect, omega)
            list_iteration[i] = iteration
            print("Number of iterations with omega = " + str(omega) + " is " + str(iteration))

            target_node = result.matrix[3][2]

            row[0] = omega
            row[1] = target_node.value
            row[2] = iteration

            row_writer.writerow(r for r in row)