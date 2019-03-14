#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cmath>
#include <Windows.h>
#include "matrix.h"
#include "choleski.h"
#include "linearResistiveNetwork.h"

using namespace std;

/**
	This is the constructor for the linear resistive network. 
	@param: input: the circuit filename to read from.
*/
linearResistiveNetwork::linearResistiveNetwork(string filename) {
	string filepath = "./circuits/" + filename;

	cout << filepath << endl;

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
		for (int i = 0; i < nodeNumber; i++) {
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

		for (tableRow; tableRow < filetable.size(); tableRow++) {
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
		// NEED TO CREATE REDUCED A MATRIX HERE!!!
	}
}


/**
	This function returns the current working directory. 

	@param: arg: void
	@param: return:string
*/
string getcwd(void) {
	char result[_MAX_PATH];
	return string(result, GetModuleFileName(NULL, result, MAX_PATH));
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

vector<vector<string>> readCSV(istream &in) {
	vector<vector<string>> table;
	string row;
	while (!in.eof()) {
		getline(in, row);
		if (in.bad() || in.fail()) {
			break;
		}

		auto fields = readCSVRow(row);
		table.push_back(fields);
	}

	return table;
}
