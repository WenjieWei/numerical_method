#ifndef LINEARNETWORK_H
#define LINEARNETWORK_H
#include <iostream>
#include <istream>
#include <vector>
#include "matrix.h"
#include "choleski.h"

using namespace std;

class linearResistiveNetwork {
private:
	int circuitId;
	int branchNumber;
	int nodeNumber;
	int size;

	Matrix currentVector;
	Matrix voltageVector;
	Matrix redResistanceMatrix;
	Matrix revResistanceMatrix;
	void readCircuit(std::string filename);
public:
	linearResistiveNetwork(std::string filename);
	
	int getSize(void);
	Matrix getMatJ(void);
	Matrix getMatE(void);
	Matrix getMatY(void);
	Matrix getMatA(void);
	Matrix reduceA(void);

	Matrix solveCircuit(void);
};

void constructNetwork(int size);
vector<vector<string>> readCSV(istream &in);

#endif