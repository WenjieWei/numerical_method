#ifndef LINEARNETWORK_H
#define LINEARNETWORK_H
#include <iostream>
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
	Matrix solveCircuit(void);
	
	int size(void);
	Matrix J(void);
	Matrix E(void);
	Matrix Y(void);
	Matrix A(void);
	Matrix reduceA(void);
};

void constructNetwork(int size);

#endif