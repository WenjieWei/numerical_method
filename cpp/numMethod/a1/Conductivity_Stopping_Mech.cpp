/**
 *	This file is a try out of implementing trapezoidal integration in c++. 
 *	It will later be transfered to Arduino. 
 */

#include <iostream>
#include <string>
#include <fstream>
#include <istream>
#include <vector>

using namespace std;

/**
	Start of a custom csv parser.
*/
enum class CSVState {
	UnquotedField,
	QuotedField,
	QuotedQuote
};

vector<std::string> readCSVRow(const std::string& row) {
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

int main()
{
	string filepath = "./data/Nov22GxR3-020M.csv";
	cout << "Reading file " + filepath << endl;
	vector<vector<string>> filetable;

	std::filebuf fb;

	if (!fb.open(filepath, std::ios::in)) {
		cout << "unable to open file" << endl;
		exit(1);
	}
	else {
		istream in(&fb);
		filetable = readCSV(in);

		for (int i = 0; i < filetable.size(); i++) {
			for (int j = 0; j < filetable[i].size(); j++) {
				cout << filetable[i][j] << ", ";
			}
			cout << endl;
		}
	}

	// A glitch happened in (0, 0). Fix it. 
	filetable[0][0] = "0.1";
	vector<vector<float>> dataTable;
	vector<float> Y;

	for (int i = 0; i < filetable.size(); ++i) {
		std::string::size_type sz;     // alias of size_t
		float entry = std::stof(filetable[i][1], &sz);
		Y.push_back(entry);
	}
	int L = Y.size();

	vector<float> X;
	for (int i = 0; i < filetable.size(); ++i) {
		std::string::size_type sz;     // alias of size_t
		float entry = std::stof(filetable[i][0], &sz);
		X.push_back(entry);
	}
	vector<float> Ya;

	for (int i = 0; i < L - 4; ++i) {
		float total = 0.f;
		for (int j = 1; j <= 5; ++j) {
			total = total + Y[i + j - 1];
		}

		float avg = total / 5;
		Ya.push_back(avg);
	}

	vector<float> area;
	for (int i = 0; i < L - 5; ++i) {
		float prev = 0.f;
		if (i != 0) {
			prev = area[i - 1];
		}

		float a = (X[i + 1] - X[i]) * (Ya[i + 1] + Ya[i]) / 2;
		area.push_back(a);

		if (i > 0) {
			area[i] = area[i] + area[i - 1];
		}

		float diff = area[i] - prev;
		cout << "Current Integration value: " << area[i] << "\t";
		if (diff > 0) {
			cout << "+, ";
		}
		else {
			cout << "-, ";
		}
		cout << abs(diff) << endl;
	}

	return 0;
}

