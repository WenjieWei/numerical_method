from matrix import Matrix
import matplotlib.pyplot as plt


def lagrange_interpolate(x, y):
    pass

if __name__ == "__main__":    
    b_data = [[0, 1.3, 1.4, 1.7, 1.8, 1.9]]
    b_matrix = Matrix(b_data, 1, 6).T
    b_matrix.print_matrix()
