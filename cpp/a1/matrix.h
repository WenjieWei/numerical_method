#ifndef MATRIX_H
#define MATRIX_H
#include <vector>

using namespace std;

class Matrix{
private:
    vector<vector<double>> mat_vec;
    int rows;
    int cols;

    bool symmetric; // Returns true if the matrix is symmetric.
    bool square; // Returns true if the matrix is square.

public:
    Matrix(vector<vector<double>> vec);

    //Matrix properties
    int get_rows(void); // Return the number of rows of the matrix.
    int get_cols(void); // Return the number of columns of the matrix.
    double value_at(int row, int col); // Return the specific value at one point.
    void set_value_at(double value, int row, int col);
    bool isSquare(void); // Returns true if the matrix is a square matrix.
    bool isSymmetric(void); // Returns true if the matrix is symmetric.

    // Matrix utilities
    Matrix plus(Matrix adder);
    Matrix subs(Matrix substractor);
    Matrix dot_product(Matrix multiplier);
    Matrix transpose(void);
    Matrix clone(void);

    // Debugging functions
    void printMatrix(void);
};

#endif
