from polynomial import Polynomial, LagrangePolynomial
from matrix import Matrix
from interpolation import lagrange_full_domain, cubic_hermite, piecewise_linear_interpolate
from nonlinear import calc_newton_raphson, calc_successive_subs
from nonlinear import calc_f1, calc_f2, calc_jacobian, calc_norm_vec
from integration import gauss_legendre_integration, nested_integration

from math import sin, log, log10
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


def plot_int_err(err_list, range_list, filename):
    print("Printing Error v.s. Segment Number.")
    err_list_log = []
    range_list_log = []
    for i in range(len(err_list)):
        err_list_log.append(log10(err_list[i]))
        range_list_log.append(log10(range_list[i]))

    plt.plot(range_list_log, err_list_log)
    plt.xlabel('log(N)')
    plt.ylabel('log(E)')
    plt.title('log(E) v.s. log(N)')
    plt.grid(True)

    plt.savefig(filename)
    plt.close()
    print("Plot has been saved to " + str(os.getcwd()) + "/" + filename)


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
    # This part calculates the nodal voltages specifically for this problem
    # r is the resistance of the resistor
    # e is the voltage provided by the source
    # isa is the reverse saturation current of diode A
    # isb is the reverse saturation current of diode B
    # ktq is the ratio of kT/q, which is 25mV.
    r = 512
    e = 0.2
    isa = 0.8e-6
    isb = 1.1e-6
    ktq = 0.025
    voltages = Matrix([[0], [0]], 2, 1)

    f1_list = [0]
    f2_list = [0]
    err_list = [0]
    epsilon = 1e-6

    iterations = 0
    f_mat = Matrix([[0], [0]], 2, 1)
    jacobian, inv_jacobian = calc_jacobian(voltages)

    f_mat[0][0] = calc_f1(voltages)
    f_mat[1][0] = calc_f2(voltages)
    f_0 = Matrix([[f_mat[0][0]], [f_mat[1][0]]], 2, 1)
    err = calc_norm_vec(f_mat) / calc_norm_vec(f_0)

    convergent = False
    with open("diode_circuit_NR.csv", 'w', newline='') as csv_file:
        row_writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_NONE, escapechar=' ')
        row_writer.writerow(['iter', '$V_1$', '$V_2$', '$f_1$', '$f_2$', 'err'])
        print("k\tV_1 \tV_2 \tf_1 \tf_2 \terr")

        while not convergent:
            err = calc_norm_vec(f_mat) / calc_norm_vec(f_0)
            err_list.append(err)
            row_writer.writerow([str(iterations), str(voltages[0][0]), str(voltages[1][0]),
                                 str(f_mat[0][0]), str(f_mat[1][0]), str(err)])
            print("%d %.8f %.8f %.8f %.8f %.8f"
                  % (iterations, voltages[0][0], voltages[1][0], f_mat[0][0], f_mat[1][0], err))
            iterations += 1
            voltages = voltages - jacobian.inv() * f_mat
            jacobian, inv_jacobian = calc_jacobian(voltages)
            f1 = calc_f1(voltages)
            f2 = calc_f2(voltages)

            v1 = voltages[0][0]
            v2 = voltages[1][0]

            f1_list.append(f1)
            f2_list.append(f2)
            f_mat[0][0] = f1
            f_mat[1][0] = f2

            if abs(calc_norm_vec(f_mat) / calc_norm_vec(f_0)) < epsilon:
                convergent = True

    # ====== Q3 ======
    print(" ====== Q3, Part a ====== ")
    filename = 'sine_err_int.png'
    real_value = 0.45970
    integral_list = []
    error_list = []
    segments = []
    for i in range(1, 21):
        integral, err = gauss_legendre_integration(sin, 0, 1, i, real_value)
        integral_list.append(integral)
        error_list.append(err)
        segments.append(i)

    plot_int_err(error_list, segments, filename)

    print(" ====== Q3, Part b ====== ")
    filename = 'ln_err_int.png'
    real_value = -1
    integral_list = []
    error_list = []
    segments = []
    for i in range(10, 200):
        integral, err = gauss_legendre_integration(log, 0, 1, i, real_value)
        integral_list.append(integral)
        error_list.append(err)
        segments.append(i)

    plot_int_err(error_list, segments, filename)

    print(" ====== Q3, Part c ====== ")
    filename = 'ln_sine_err_int.png'
    real_value = -2.666
    integral_list = []
    error_list = []
    segments = []
    upper_limit = 0.2 * sin(1)
    for i in range(10, 200):
        integral, err = nested_integration(0, upper_limit, i, real_value)
        integral_list.append(integral)
        error_list.append(err)
        segments.append(i)

    plot_int_err(error_list, segments, filename)

    print(" ====== Q3, Part d ====== ")
