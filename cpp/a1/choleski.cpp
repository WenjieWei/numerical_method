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
Matrix decomposition(Matrix A){
    int n = A.get_rows();
    vector<vector<double>> empty_vec(n);
    for(int i = 0; i < empty_vec.size(); i++){
        empty_vec[i].resize(1);
    }
    Matrix L = Matrix(empty_vec);

    for(int j = 0; j < n; j++){
        if(A.value_at(j, j) <= 0){
            throw "Matrix is not positive definite!\n";
        }

        double temp_sum = 0;
    }

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
