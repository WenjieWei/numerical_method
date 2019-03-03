#include <iostream>
#include <vector>
#include <cmath>
#include "matrix.h"
#include "choleski.h"

using namespace std;


/**
 *  Perform the decomposition step of CD.
 *  Arguments:
 *      A: matrix A to be decomposed.
 *  Returns:
 *      L: matrix L which satisfies LL.transpose() = A.
 */
Matrix decomposite(Matrix A){
    int n = A.get_rows();
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
			throw "Operand in square root must be greater or equal to 0!";
		}
		else {
			L.setValueAt(entry, j, j);
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


}
