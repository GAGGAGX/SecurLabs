#include <iostream>
#include <bitset>
#include <vector>


// polynom (8, 4, 3, 2, 0)
//const size_t bitsCnt = 8;
//std::bitset<bitsCnt>  reg;
//std::vector<int> bitsPositions{ 4, 3, 2, 0 };

// (59, 6, 5, 4, 3, 1, 0)
const size_t bitsCnt = 59;
std::bitset<bitsCnt>  reg;
std::vector<int> bitsPositions{ 6, 5, 4, 3, 1, 0 };

// (64, 4, 3, 1, 0)
//const size_t bitsCnt = 64;
//std::bitset<bitsCnt>  reg;
//std::vector<int> bitsPositions{ 4, 3, 1, 0 };


void findCodeKey() {
	bool xorValue = false;
	for (const auto& bit : bitsPositions) {
		xorValue ^= reg[bit];
	}
	reg >>= 1;
	reg[bitsCnt - 1] = xorValue;
}

std::string codeText(const std::string& str) 
{
	std::string output;
	for (const char& c : str) {
		findCodeKey();
		char codedSympol = c ^ static_cast<char>(reg.to_ullong());
		output += codedSympol;
	}
	return output;
}

int main() {
	
	std::string initialText = "ABC def 123 !@#";
	std::cout << "Initial text:  " << initialText << "\n";

	reg.set(); // all bits 1
	std::string codedText = codeText(initialText);
	std::cout << "Coded text:    " << codedText << "\n";

	reg.set(); // all bits 1
	std::string deCodeText = codeText(codedText);
	std::cout << "DeCoded text:  " << deCodeText << "\n";

	return 0;
}
