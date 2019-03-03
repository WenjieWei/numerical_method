#include <iostream>
#include <vector>
#include "matrix.h"

using namespace std;

/**
 *  The constructor of the Matrix object.
 *  Input argument: vec: 2-D vector of doubles.
 *
 *  Initializes:
 *  The number of rows;
 *  The number of columns;
 *  A 2-D vector of doubles containing the matrix values.
 *  Two boolean values, indicating symmectricity and square information.
 */
Matrix::Matrix(vector<vector<double>> vec){
    rows = vec.size();
    if(rows > 0){
        cols = vec[0].size();
    }

    // Initialize the 2-D vector of the matrix object.
    mat_vec.resize(rows);
    for(int i = 0; i < rows; i++){
        mat_vec[i].resize(cols);
        for(int j = 0; j < cols; j++){
            mat_vec[i][j] = vec[i][j];
        }
    }

    // Check if the matrix is a square matrix.
    if(rows == cols){
        square = true;

        // Check symmetricity.
        symmetric = true;
        for(int i = 0; i < rows; i++){
            for(int j = 0; j < cols; j++){
                if(mat_vec[i][j] != mat_vec[j][i])
                    symmetric = false;
            }
        }
    } else {
        // If the matrix is not square,
        // Then it is 100% not symmetric.
        square = false;
        symmetric = false;
    }
}


/**
 *  Returns the number of rows of the matrix.
 *  Args: void.
 *  Returns: int value indicating the number of rows in the matrix.
 */
int Matrix::get_rows(void){
    return rows;
}


/**
 *  Returns the number of cols of the matrix.
 *  Args: void.
 *  Returns: int value indicating the number of columns in the matrix.
 */
int Matrix::get_cols(void){
    return cols;
}


/**
 *  Returns the value at the specified coordinate.
 *  Args: the row number and column number.
 *  Returns: double value indicating the number.
 */
double Matrix::valueAt(int row, int col){
    double value;

    try{
        value = mat_vec.at(row).at(col);
    } catch (const std::out_of_range& e){
        cout << "The indices passed in are out of bounds." << endl;
    }

    return value;
}


/**
 *  Returns true if the matrix is square.
 *  Args: void
 *  Retval: square
 */
bool Matrix::isSquare(void){
    return square;
}


/**
 * Returns true if the matrix is symmetric
 * Args: void
 * Retval: symmetric
 */
 bool Matrix::isSymmetric(void){
     return symmetric;
 }


 /**
  *  Set the value at the specific location
  *  Argument: value, row and column
  *  Return: void
  */
void Matrix::setValueAt(double value, int row, int col){
    try{
        mat_vec.at(row).at(col) = value;
    } catch (const std::out_of_range& e){
        cout << "The indicies passed in are out of bounds." << endl;
    }
}


/**
 *  Perform matrix addition.
 *  Args: the adder matrix.
 *  Retval: the result matrix.
 */
Matrix Matrix::plus(Matrix adder){
    vector<vector<double>> result_vec;
    if(adder.get_rows() != rows || adder.get_cols() != cols)
        throw "Matrix dimensions do not agree!\n";
    else{
        result_vec.resize(rows);
        for(int i = 0; i < rows; i++){
            result_vec[i].resize(cols);
        }
    }

    Matrix result = Matrix(result_vec);

    for(int i = 0; i < rows; i++){
        for(int j = 0; j < cols; j++){
            result.setValueAt((mat_vec[i][j] + adder.valueAt(i, j)), i, j);
        }
    }

    return result;
}


/**
 *  Perform matrix substraction.
 *  Args: the substractor matrix.
 *  Retval: the result matrix.
 */
Matrix Matrix::subs(Matrix substractor){
    vector<vector<double>> result_vec;
    if(substractor.get_rows() != rows || substractor.get_cols() != cols){
        throw "Matrix dimensions do not agree!\n";
    } else {
        result_vec.resize(rows);
        for(int i = 0; i < rows; i++){
            result_vec[i].resize(cols);
        }
    }

    Matrix result = Matrix(result_vec);

    for(int i = 0; i < rows; i++){
        for(int j = 0; j < cols; j++){
            result.setValueAt((mat_vec[i][j] - substractor.valueAt(i, j)), i, j);
        }
    }

    return result;
}


/**
 *  Perform matrix substraction.
 *  Args: the substractor matrix.
 *  Retval: the result matrix.
 */
Matrix Matrix::dot_product(Matrix multiplier){
    vector<vector<double>> result_vec;
    if(multiplier.get_rows() != cols || multiplier.get_cols() != rows){
        throw "Matrix dimensions do not agree!\n";
    } else {
        result_vec.resize(cols);
        for(int i = 0; i < cols; i++){
            result_vec[i].resize(multiplier.get_cols());
        }
    }

    Matrix result = Matrix(result_vec);

    for(int i = 0; i < rows; i++){
        for(int j = 0; j < multiplier.get_cols(); j++){
            double sum = 0;
            for(int k = 0; k < multiplier.get_rows(); k++){
                sum += mat_vec[i][k] * multiplier.valueAt(k, j);
            }

            result.setValueAt(sum, i, j);
        }
    }

    return result;
}


/**
 *  Perform the transpose of the matrix.
 *  Args: void
 *  Retval: The transpose of the matrix.
 */
Matrix Matrix::transpose(void){
    vector<vector<double>> result_vec(cols);
    for(int i = 0; i < cols; i++){
        result_vec[i].resize(rows);
    }

    Matrix result = Matrix(result_vec);

    for(int i = 0; i < rows; i++){
        for(int j = 0; j < cols; j++){
            result.setValueAt(mat_vec[i][j], j, i);
        }
    }

    return result;
}


/**
 *  Clone the current matrix.
 *  Retval: the clone of the current matrix.
 */
Matrix Matrix::clone(void){
    vector<vector<double>> result_vec(rows);
    for(int i = 0; i < rows; i++){
        result_vec[i].resize(cols);
        for(int j = 0; j < cols; j++){
            result_vec[i][j] = mat_vec[i][j];
        }
    }
    Matrix result = Matrix(result_vec);

    return result;
}


/**
 *  Print the matrix for debugging purpose.
 */
void Matrix::printMatrix(void){
    for(int i = 0; i < rows; i++){
        cout << "|\t";
        for(int j = 0; j < cols; j++){
            cout << mat_vec[i][j] << "\t";
        }
        cout << "|" << endl;
    }
}
