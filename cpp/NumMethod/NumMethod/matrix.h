#pragma once
#ifndef _MATRIX_H_
#define _MATRIX_H_

#include<stdexcept>

template <typename T>
class Matrix {
private:
	int _nCol, _nRow;
	T* _data = NULL;

public:
	// Constructors, copy constructor & destructor
	Matrix(int nCol = 1, int nRow = 1);
	Matrix(T* data, int nCol = 1, int nRow = sizeof(data) / sizeof(data[0]));
	Matrix(Matrix& mat);
	~Matrix();

	// Getter functions
	inline int getCol() const;
	inline int getRow() const;
	T getValue(int row, int col) const;

	// Matrix property functions
	inline bool isSquare() const;
	bool isSymmetric() const;
	void printMatrix() const;

	// Matrix operations
	Matrix<T> transpose();

	// Static functions

};

// ========== Constructors, copy constructor & destructor ========== 
// Constructors
template <typename T>
Matrix<T>::Matrix(int nCol, int nRow) :_nCol(nCol), _nRow(nRow) {
	this->_data = new T[nCol * nRow];
	for (int i = 0; i < nCol * nRow; ++i)
		this->_data[i] = rand() % 50;
}

template <typename T>
Matrix<T>::Matrix(T* data, int nCol, int nRow) {
	this->_nCol = nCol;
	this->_nRow = nRow;
	this->_data = new T[nCol * nRow];
}

// Copy constructor 
template <typename T>
Matrix<T>::Matrix(Matrix<T>& mat) {
	this->_nCol = mat._nCol;
	this->_nRow = mat._nRow;
	this->_data = mat._data;
}

// Destructor
template <typename T>
Matrix<T>::~Matrix() {
	delete [] this->_data;
}

// ========== Getter functions ========== 
template <typename T>
int Matrix<T>::getCol() const { return _nCol; }

template <typename T>
int Matrix<T>::getRow() const { return _nRow; }

/**
	Get the value of the matrix at (row, col)
 	Index at top left corner is (0, 0). 
 	@param:
 		row: row number, range: [0, this->_nRow]
 		col: column number, range: [0, this->_nCol]
 	@return:
 		The value at the indicated position
 */
template <typename T>
T Matrix<T>::getValue(int row, int col) const {
	if (row < this->_nRow && row >= 0 && col < this->_nCol && col >= 0)
		return this->_data[row * this->_nCol + col];
	else
		std::cout << "error!" << std::endl;
		//TODO: throw exception when out of bound.
		//throw std::runtime_error("Array index out of bound: trying to access matrix item at (%d, %d)", row, col);
}

// ========== Matrix property functions ========== 
template <typename T>
bool Matrix<T>::isSquare() const { return _nCol == _nRow; }

template <typename T>
bool Matrix<T>::isSymmetric() const {
	if (this->isSquare()) {
		if (this->_nRow > 1) {
			for (int i = 1; i < this->_nRow; ++i) {
				for (int j = 1; j < i; ++j) {
					if (this->getValue(i, j) == this->getValue(j, i)) continue;
					else return false;
				}
			}
		}
		return true;
	}
	else return false;
}

template <typename T>
void Matrix<T>::printMatrix() const {
	for (int i = 0; i < this->_nRow; ++i) {
		for (int j = 0; j < this->_nCol; ++j) {
			std::cout << this->getValue(i, j) << ",\t";
		}
		std::cout << "\n";
	}
}

// ========== Matrix operation functions ========== 
template <typename T>
Matrix<T> Matrix<T>::transpose() {

}
#endif
