#include <iostream>
#include <vector>
#include <cmath>
#include "matrix.h"
#include "choleski.h"

using namespace std;


/**
 *  Perform the back substitution step of CD.
 *  Arguments:
 *      L: The decomposited matrix.
 *      y: The eliminated vector.
 *  Returns:
 *      x: Final result vector.
 */
Matrix bwdSubstitution(Matrix L, Matrix y){
    int n = L.getRows();
    vector<vector<double>> xVec(n);
    for(int i = 0; i < n; i++){
        xVec[i].resize(1);
    }
    Matrix x = Matrix(xVec);

    for(int i = (n - 1); i >= 0; i--){
        double tempSum = 0;
        double entry = 0;
        for(int j = (i + 1); j < n; j++){
            tempSum += (L.valueAt(j, i) * x.valueAt(j, 0));
        }

        entry = (y.valueAt(i, 0) - tempSum) / L.valueAt(i, i);
        x.setValueAt(entry, i, 0);
    }

    return x;
}


/**
 *  Perform the forward elemination step of CD.
 *  Arguments:
 *      L: The decomposited matrix.
 *      b: The result vector.
 *  Returns:
 *      y: the eliminated vector.
 */
Matrix fwdElimination(Matrix L, Matrix b){
    int n = L.getRows();
    vector<vector<double>> yVec(n);
    for(int i = 0; i < n; i++){
        yVec[i].resize(1);
    }
    Matrix y = Matrix(yVec);

    for(int i = 0; i < y.getRows(); i++){
        double tempSum = 0;
        double tempProd = 0;
        double entry = 0;

        if (i > 0){
            for(int j = 0; j < i; j++){
                tempProd = L.valueAt(i, j) * y.valueAt(j, 0);
                tempSum += tempProd;
            }
            entry = (b.valueAt(i, 0) - tempSum) / L.valueAt(i, i);
            y.setValueAt(entry, j, 0);
        }
    }

    return y;
}


/**
 *  Perform the decomposition step of CD.
 *  Arguments:
 *      A: matrix A to be decomposed.
 *  Returns:
 *      L: matrix L which satisfies LL.transpose() = A.
 */
Matrix decomposite(Matrix A){
    int n = A.getRows();
	// Obtain the number of rows in the matrix.

    vector<vector<double>> empty_vec(n);
    for(int i = 0; i < empty_vec.size(); i++){
        empty_vec[i].resize(1);
    }
    Matrix L = Matrix(empty_vec);

	// Loop through every row in the matrix. j is the row number.
    for(int j = 0; j < n; j++){
        double tempSum = 0;
		// Loop through every column until the diagonal. k is the column number.
		for (int k = 0; k < j; k++) {
			// Obtain Ljj.
			tempSum += pow(A.valueAt(k, j), 2);
		}

		double entry = A.valueAt(j, j) - tempSum;
		if (entry < 0) {
            cout << "Warning: Matrix is not positive definite." << endl;
			throw "Operand in square root must be greater or equal to 0!";
		}
		else {
			L.setValueAt(sqrt(entry), j, j);
		}

        for(int i = j + 1; i < n; i++){
            tempSum = 0;
            for(int k = 0; k < j; k++){
                tempSum += L.valueAt(i, k) * L.valueAt(j, k);
            }

            entry = (A.valueAt(i, j) - tempSum) / L.valueAt[j][j];
            L.setValueAt(entry, i, j);
        }
    }

	return L;
}


/**
 *  This is the function implemented for solving the problem Ax = b,
 *  using Choleski decomposition.
 *
 *  Arguments:
 *      A: matrix A, a real, S.P.D. nxn matrix.
 *      b: Column vector with n rows.
 *
 *  Returns:
 *      Column vector x with n rows.
 */
Matrix solve_chol(Matrix A, Matrix b){
    // Check SPD
    if (!A.isSymmetric()){
        throw "Matrix must be symmetric to perform Choleski Decomposition!\n";
    }

    Matrix L = decomposite(A);
    Matrix y = fwdElimination(L, b);
    Matrix x = bwdSubstitution(L, y);

    return x;
}


/**
 *  Check if Choleski returns the correct result.
 *  Arguments:
 *      A: nxn matrix
 *      b: result vector.
 *      x: nx1 vector.
 *  Returns:
 *      True if correct.
 */
bool checkCholeski(Matrix A, Matrix b, Matrix x){
    Matrix result = A.dotProduct(x);
    cout << "Matrix A is:" << endl;
    A.printMatrix();
    cout << endl << "Vector b is:" << endl;
    b.printMatrix();
    cout << endl << "Result vector x is:" << endl;
    x.printMatrix();

    for(int i = 0; i < result.getRows(); i++){
        for(int j = 0; j < result.getCols(); j++){
            if(abs(result.valueAt(i, j) - b.valueAt(i, j)) >= 0.001){
                return false;
            }
        }
    }

    return true;
}
