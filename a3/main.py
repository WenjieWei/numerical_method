from polynomial import Polynomial, LagrangePolynomial
from interpolation import lagrange_full_domain, cubit_hermite
import matplotlib.pyplot as plt
import csv, os


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

    return b_vec, h_vec

def calc_slope(X, Y, target):
    slope = []

    result = (Y[1] - Y[0]) / (X[1] - X[0])
    slope.append(result)
    for i in range(1, len(target) - 1):
        j = Y.index(target[i])
        result = (Y[j + 1] - Y[j - 1]) / (X[j + 1] - X[j - 1])

        slope.append(result)

    result = (Y[i + 1] - Y[i]) / (X[i + 1] - X[i])
    slope.append(result)

    return slope


def curve_plot(poly, filename, up):
    b_list = []
    h_list = []

    h = 0
    while h <= up:
        h_list.append(h)
        b_list.append(poly.calculate(h))
        h += 0.5

    plt.plot(h_list, b_list)

    plt.xlabel('H (A/m)')
    plt.ylabel('B (T)')
    plt.title('B vs. H')
    plt.grid(True)

    plt.savefig(filename)
    plt.close()
    print("Plot of the polynomial has been stored to " + os.getcwd() + filename)

if __name__ == "__main__":
    os.chdir('data')
    filename = 'M19_BH.csv'

    #B, H = read_BH_file(filename)

    print("This is the output log of assignment 3.")

    # ======= Part a =======
    print("Running (a) of Problem 1...")
    H = [0.0, 14.7, 36.5, 71.7, 121.4, 197.4]
    B = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    poly = lagrange_full_domain(H, B)

    print("The interpolated polynomial of the first six points is:")
    poly.toString()
    filename = "B_H_first_six.png"

    curve_plot(poly, filename, 200)

    # ====== Part b ======
    print("Running (b) of Problem 1...")
    H = [0.0, 540.6, 1062.8, 8687.4, 13924.3, 22650.2]
    B = [0.0, 1.3, 1.4, 1.7, 1.8, 1.9]
    poly = lagrange_full_domain(H, B)

    print("The interpolated polynomial of the second set of six points is:")
    poly.toString()
    filename = "B_H_second_six.png"
    curve_plot(poly, filename, 22651)

    # ====== Part c ======
    print("Running Part (c) of Problem 1...")
    print("The slope at the data points are calculated as follows:")

    B, H = read_BH_file("M19_BH.csv")
    for i in H:
        print(i, end=", ")

    print()
    slopes = calc_slope(H, B, B)
    for i in slopes:
        print(i, end=", ")

    filename = "Cubic Hermite.png"
    poly = cubit_hermite(H, B, slopes)
    print("The interpolated polynomial is:")
    poly.toString()

    print("test point" + str(540.6) + "=" + str(poly.calculate(540.6)))
    print("test point" + str(1062.8) + "=" + str(poly.calculate(1062.8)))
    print("test point" + str(8687.4) + "=" + str(poly.calculate(8687.4)))
    curve_plot(poly, filename, 22561)
