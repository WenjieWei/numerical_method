from matrix import Matrix
from polynomial import Polynomial
import matplotlib.pyplot as plt
import csv, math


def lagrange_full_domain():
    pass

if __name__ == "__main__":
    with open('./data/M19_BH.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        row = next(csv_reader)
        