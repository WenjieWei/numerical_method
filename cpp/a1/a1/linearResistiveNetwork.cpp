#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cmath>
#include "matrix.h"
#include "choleski.h"
#include "linearResistiveNetwork.h"

using namespace std;
const int MAX_PATH = 255;

/**
	This is the constructor for the linear resistive network.
	@param: input: the circuit filename to read from.
*/
linearResistiveNetwork::linearResistiveNetwork(string filename) {
	string filepath = "./circuits/" + filename;

	ifstream infile;
	infile.open(filepath);
	if (!infile) {
		cout << "unable to open file" << endl;
		exit(1);
	}
	else {
		vector<vector<string>> filetable = readCSV(infile);
		int tableRow = 0;

		// Create necessary vectors and matrices.
		circuitId = stoi(filetable[tableRow][0]);
		branchNumber = stoi(filetable[tableRow][2]);
		nodeNumber = stoi(filetable[tableRow][4]);
		size = int(sqrt(nodeNumber));
		tableRow++;

		int branchId = 0;
		vector<vector<double>> curVec(branchNumber);
		vector<vector<double>> volVec(branchNumber);
		vector<vector<double>> incVec(nodeNumber);
		for (int i = 0; i < nodeNumber; i++){
			curVec[i].resize(1);
			volVec[i].resize(1);
			incVec[i].resize(branchNumber);
		}
		vector<vector<double>> revResMat(branchNumber);
		for (int i = 0; i < branchNumber; i++) {
			revResMat[i].resize(branchNumber);
		}

		currentVector = Matrix(curVec); // -> equivalent to J
		voltageVector = Matrix(volVec); // -> equivalent to E
		revResistanceMatrix = Matrix(revResMat); // -> equivalent to y
		Matrix matA = Matrix(incVec); // -> equivalent to A

		for (tableRow = 1; tableRow < filetable.size(); tableRow++) {
			currentVector.setValueAt(stod(filetable[tableRow][2]), branchId, 0);
			voltageVector.setValueAt(stod(filetable[tableRow][4]), branchId, 0);

			if (stoi(filetable[tableRow][3]) != 0) {
				revResistanceMatrix.setValueAt((1 / stod(filetable[tableRow][3])), branchId, branchId);
			}
			else {
				cout << "Input resistance on branch " << tableRow << " is zero!" << endl;
				exit(1);
			}

			// Create un-reduced matrix A
			matA.setValueAt(1, stoi(filetable[tableRow][0]), branchId);
			matA.setValueAt(-1, stoi(filetable[tableRow][1]), branchId);

			branchId++;
		}
		
		// Node 0 is grounded by default.
		// Therefore, remove the first node, i.e. the first row of matrix A
		// and create a new reduced incidence matrix.
		vector<vector<double>> reduced_A_vector(nodeNumber - 1);
		for(int i = 0; i < reduced_A_vector.size(); i++){
			reduced_A_vector.resize(branchNumber);
			for(int j = 0; j < branchNumber; j++){
				reduced_A_vector[i][j] = matA.valueAt(i, j);
			}
		}
		redResistanceMatrix = Matrix(reduced_A_vector);
	}
}


int linearResistiveNetwork::getSize(void){
	return size;
}

Matrix linearResistiveNetwork::getMatJ(void){
	return currentVector;
}

Matrix linearResistiveNetwork::getMatE(void){
	return voltageVector;
}

Matrix linearResistiveNetwork::getMatY(void){
	return revResistanceMatrix;
}

Matrix linearResistiveNetwork::getMatA(void){
	return redResistanceMatrix;
}


/**
 *	Calculate the final solution of the circuit.
 *	Calculate matrices A and b based on the information above
 *	and solve Ax = b.
 */
Matrix linearResistiveNetwork::solveCircuit(void){
	// First calculate A.
	Matrix A = redResistanceMatrix.dotProduct(
		revResistanceMatrix.dotProduct(redResistanceMatrix.transpose()));

	// Calculate b
	Matrix YE = revResistanceMatrix.dotProduct(voltageVector);
	Matrix J_YE = currentVector.subs(YE);
	Matrix B = redResistanceMatrix.dotProduct(J_YE);

	return solve_chol(A, B);
}



/**
	Start of a custom csv parser.
*/
enum class CSVState{
	UnquotedField,
	QuotedField,
	QuotedQuote
};

vector<std::string> readCSVRow(const std::string &row) {
	CSVState state = CSVState::UnquotedField;
	std::vector<std::string> fields{ "" };
	size_t i = 0; // index of the current field.
	for (char c : row) {
		switch (state) {
		case CSVState::UnquotedField:
			switch (c) {
			case ',':	// end of the field
				fields.push_back("");
				i++;
				break;
			case '"':
				state = CSVState::QuotedField;
				break;
			default:
				fields[i].push_back(c);
				break;
			}
			break;

		case CSVState::QuotedField:
			switch (c) {
			case '"':
				state = CSVState::QuotedQuote;
				break;
			default:
				fields[i].push_back(c);
				break;
			}
			break;
		case CSVState::QuotedQuote:
			switch (c) {
			case ',': // , after closing quote
				fields.push_back("");
				i++;
				state = CSVState::UnquotedField;
				break;
			case '"': // "" -> "
				fields[i].push_back('"');
				state = CSVState::QuotedField;
				break;
			default:
				state = CSVState::UnquotedField;
				break;
			}
		}
	}

	return fields;
}

/// Read CSV file, Excel dialect. Accept "quoted fields ""with quotes"""
std::vector<std::vector<std::string>> readCSV(std::istream& in) {
    std::vector<std::vector<std::string>> table;
    std::string row;
    while (!in.eof()) {
        std::getline(in, row);
        if (in.bad() || in.fail()) {
            break;
        }
        auto fields = readCSVRow(row);
        table.push_back(fields);
    }
    return table;
}
