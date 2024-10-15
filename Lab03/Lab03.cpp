#include <iostream>
#include <fstream>
#include <vector>
#include <iomanip>
#include <string>
#include <cstring>
#include <chrono>

class LemerAlgr {
public:
    LemerAlgr() {
        current = std::chrono::system_clock::now().time_since_epoch().count();
    }

    void reset() {
        current = std::chrono::system_clock::now().time_since_epoch().count();
    }

    unsigned long next() {
        current = (a * current + c) % m;
        return current;
    }

private:
    static const unsigned long a = 1664525;
    static const unsigned long c = 1013904223;
    static const unsigned long m = 4294967295;
    unsigned long current;
};


std::vector<unsigned char> generateSessionKey(LemerAlgr& lcg, size_t keyBits) {
    size_t keyBytes = keyBits / 8;
    std::vector<unsigned char> key(keyBytes);

    for (size_t i = 0; i < keyBytes; ++i) {
        key[i] = static_cast<unsigned char>(lcg.next() % 256);
    }
    return key;
}


std::vector<unsigned long> generateControlVector(LemerAlgr& lcg, size_t vectorBits) {
    size_t vectorSize = vectorBits / 32;
    std::vector<unsigned long> controlVector(vectorSize);

    for (size_t i = 0; i < vectorSize; ++i) {
        controlVector[i] = lcg.next();
    }
    return controlVector;
}

std::vector<unsigned char> rxor(const std::vector<unsigned char>& data, const std::vector<unsigned char>& key) {
    std::vector<unsigned char> result(data.size());
    for (size_t i = 0; i < data.size(); ++i) {
        result[i] = data[i] ^ key[i % key.size()];
    }
    return result;
}

void saveToFile(const std::string& filename, const std::vector<unsigned char>& key) {
    std::ofstream file(filename, std::ios::binary);
    if (file.is_open()) {
        file.write(reinterpret_cast<const char*>(key.data()), key.size());
        file.close();
    }
    else {
        std::cerr << "Error: " << filename << std::endl;
    }
}


std::vector<unsigned char> encrypt(const std::vector<unsigned char>& data, const std::vector<unsigned char>& key) {
    return rxor(data, key);
}

int main() {

    size_t keyBits = 128;
    LemerAlgr lemerAlgr;

    std::vector<unsigned char> sessionKey = generateSessionKey(lemerAlgr, keyBits);
    for (unsigned char byte : sessionKey) {
        std::cout << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(byte) << " ";
    }
    std::cout << std::dec << std::endl;
    //saveToFile("s_key.txt", sessionKey);

    lemerAlgr.reset();
    size_t vectorBits = 128;
    std::vector<unsigned long> controlVector = generateControlVector(lemerAlgr, vectorBits);

    std::vector<unsigned char> hash(controlVector.size() * sizeof(unsigned long));
    std::memcpy(hash.data(), controlVector.data(), hash.size());
    std::vector<unsigned char> mKey = rxor(hash, sessionKey);
    for (unsigned char byte : mKey) {
        std::cout << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(byte) << " ";
    }
    std::cout << std::dec << std::endl;
   
    //saveToFile("m_key.txt", mKey);

    //std::ifstream inFile("s_key.txt", std::ios::binary);
    //std::vector<unsigned char> data((std::istreambuf_iterator<char>(inFile)), std::istreambuf_iterator<char>());
    // inFile.close();

    std::vector<unsigned char> encryptedData = encrypt(sessionKey, mKey);


    std::cout << "Encrypted data: ";
    for (unsigned char byte : encryptedData) {
        std::cout << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(byte) << " ";
    }
    std::cout << std::dec << std::endl;

    return 0;
}