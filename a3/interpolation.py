from matrix import Matrix
from polynomial import Polynomial
import matplotlib.pyplot as plt
import csv, math, os


def lagrange_full_domain():
    pass

def read_BH_file(filename):   
    """
    This method reads a csv file that contains the information about B and H for the M19 steel.
    :param: filename: the filename in a String to be read.
    :return: two matrices b_matrix and h_matrix
    """

    b_vec = []
    h_vec = []

    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')

        for row in csv_reader:
            b_vec.append(float(row[0]))
            h_vec.append(float(row[1]))
    
    b_matrix = Matrix([b_vec], 1, len(b_vec)).T
    h_matrix = Matrix([h_vec], 1, len(h_vec)).T

    return b_matrix, h_matrix

if __name__ == "__main__":
    os.chdir('data')
    filename = 'M19_BH.csv'

    b_matrix, h_matrix = read_BH_file(filename)
