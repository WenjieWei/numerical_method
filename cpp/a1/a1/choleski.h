#ifndef CHOLESKI_H
#define CHOLESKI_H
#include "matrix.h"

bool checkCholeski(Matrix A, Matrix b, Matrix x);
Matrix solve_chol(Matrix A, Matrix b);

#endif
