#include <iostream>
#include <vector>
#include "matrix.h"
#include "choleski.h"

using namespace std;

int main(int argc, char** argv) {
	cout << "**** Executing assignment 1 of ECSE 543 ****" << endl;
	cout << "**** Question 1: Choleski Decomposition ****" << endl;
	//cout << "Enter the A matrix. Separate row elements by ',' and separate rows by ';'." << endl;

	vector<vector<double>> matVec = {
		{38, 23, 31, 22, 29, 25, 31},
		{23, 44, 36, 27, 35, 24, 33},
		{31, 36, 65, 36, 45, 34, 45},
		{22, 27, 36, 46, 29, 15, 27},
		{29, 35, 45, 29, 52, 32, 39},
		{25, 24, 34, 15, 32, 37, 36},
		{31, 33, 45, 27, 39, 36, 65}};
	Matrix A = Matrix(matVec);
	A.printMatrix();

	vector<vector<double>> bVec = {
		{13},
		{4},
		{7},
		{23},
		{17},
		{5.8},
		{10}
	};
	Matrix b = Matrix(bVec);
	b.printMatrix();

	Matrix x = solve_chol(A, b);

	if(checkCholeski(A, b, x)){
		cout << "Correct!" << endl;
	} else {
		cout << "Incorrect!" << endl;
	}

	return 0;
}
