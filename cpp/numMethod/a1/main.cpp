#include <iostream>
#include <istream>
#include <vector>
#include <fstream>
#include <string>
#include "matrix.h"
#include "choleski.h"
#include "linearResistiveNetwork.h"

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

	Matrix x = solve_chol(A, b);

	if(checkCholeski(A, b, x)){
		cout << "Correct!" << endl;
	} else {
		cout << "Incorrect!" << endl;
	}
	
	cout << "Running circuit simulations for the five test circuits." << endl;
	for (int i = 1; i <= 5; i++) {
		string filename = "tc_" + to_string(i) + ".csv";
		string filepath = "./circuits/" + filename;

		cout << "Calculating node voltages for circuit " << i << "." << endl;

		std::filebuf fb;

		if (!fb.open(filepath, std::ios::in)) {
			cout << "unable to open file" << endl;
			exit(1);
		}
		else {
			istream in(&fb);
			vector<vector<string>> filetable = readCSV(in);

			for (int i = 0; i < filetable.size(); i++) {
				for (int j = 0; j < filetable[i].size(); j++) {
					cout << filetable[i][j] << ", ";
				}
				cout << endl;
			}
		}

		linearResistiveNetwork nwk = linearResistiveNetwork(filename);
		nwk.solveCircuit().printMatrix();
	}
	return 0;
}
