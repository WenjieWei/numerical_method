from polynomial import Polynomial, LagrangePolynomial
from interpolation import lagrange_full_domain, cubic_hermite, piecewise_linear_interpolate
from nonlinear import calc_newton_raphson, calc_successive_subs, calc_diode
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

    i = 0
    while i < len(target) - 1:
        j = Y.index(target[i])
        result = (Y[j + 1] - Y[j]) / (X[j + 1] - X[j])
        i += 1

        slope.append(result)

    result = (Y[j] - Y[j - 1]) / (X[j] - X[j - 1])
    slope.append(result)

    return slope


def curve_plot(poly, filename, up, data_x, data_y):
    b_list = []
    h_list = []

    h = 0
    while h <= up:
        h_list.append(h)
        b_list.append(poly.calculate(h))
        h += 0.5

    plt.plot(h_list, b_list)
    for i in range(len(data_x)):
        plt.plot(data_x[i], data_y[i], 'oC0')

    plt.xlabel('H (A/m)')
    plt.ylabel('B (T)')
    plt.title('B vs. H')
    plt.grid(True)

    plt.savefig(filename)
    plt.close()
    print("Plot of the polynomial has been stored to " + os.getcwd() + "/" + filename)


def plot_piecewise(filename, poly_list, data_x, data_y):
    b_list = []
    h_list = []

    for i in range(len(poly_list)):
        temp_poly = poly_list[i]
        h = data_x[i]
        while h < data_x[i + 1]:
            b = temp_poly.calculate(h)
            h_list.append(h)
            b_list.append(b)
            h += 0.01

    plt.plot(h_list, b_list)
    for i in range(len(data_x)):
        plt.plot(data_x[i], data_y[i], 'oC0')

    plt.ylabel('H (A/m)')
    plt.xlabel('B (T)')
    plt.title('H v.s. B')
    plt.grid(True)

    plt.savefig(filename)
    plt.close()
    print("Plot of the polynomial has been stored to " + os.getcwd() + "/" + filename)

if __name__ == "__main__":
    os.chdir('data')
    filename = 'M19_BH.csv'

    #B, H = read_BH_file(filename)

    print("This is the output log of assignment 3.")

    # ======= Part a =======
    print(" ====== Q1, Part a ======")
    H = [0.0, 14.7, 36.5, 71.7, 121.4, 197.4]
    B = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    poly = lagrange_full_domain(H, B)

    print("The interpolated polynomial of the first six points is:")
    poly.toString()
    filename = "B_H_first_six.png"

    curve_plot(poly, filename, 200, H, B)

    # ====== Part b ======
    print(" ====== Q1, Part b ======")
    H = [0.0, 540.6, 1062.8, 8687.4, 13924.3, 22650.2]
    B = [0.0, 1.3, 1.4, 1.7, 1.8, 1.9]
    poly = lagrange_full_domain(H, B)

    print("The interpolated polynomial of the second set of six points is:")
    poly.toString()
    filename = "B_H_second_six.png"
    curve_plot(poly, filename, 22651, H, B)

    # ====== Part c ======
    print(" ====== Q1, Part c ======")
    slopes = calc_slope(H, B, B)
    filename = "Cubic Hermite.png"
    poly = cubic_hermite(H, B, slopes)
    print("The interpolated polynomial is:")
    poly.toString()
    curve_plot(poly, filename, 22561, H, B)

    # ====== Part e ======
    print(" ====== Q1, Part e ======")
    # Find the piecewise interpolated polynomial
    filename = "Piecewise_Polynomial"
    B, H = read_BH_file('M19_BH.csv')
    piece_poly_list = piecewise_linear_interpolate(B, H)
    print("Printing the piecewise polynomials...")
    plot_piecewise(filename, piece_poly_list, B, H)

    # Calculate Newton Raphson
    iterations, flux_list = calc_newton_raphson(piece_poly_list, B, H)
    print("number of iterations = %d, final flux = %.8f" % (iterations, flux_list[len(flux_list) - 1]))

    # ====== Part f ======
    print(" ====== Q1, Part f ====== ")
    iterations, flux_list = calc_successive_subs(piece_poly_list, B, H)
    print("number of iterations = %d, final flux = %.8f" % (iterations, flux_list[len(flux_list) - 1]))

    # Start of Q2
    # ====== Part b ======
    print(" ====== Q2, Part b ====== ")
    calc_diode()
