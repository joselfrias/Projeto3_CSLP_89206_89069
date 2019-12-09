#pragma once
#include <iostream>
#include <fstream>
#include <string>
using namespace std;

class BitStream{
private:
    int accumulator;
    int bcount;
    FILE *fp;

public:
    void writeBit(int bit);
    void writeBits(int bit, int n, string f);
    //int readBit(); implementar depois
    //int readBits(); implementar depois
    BitStream();
};

BitStream::BitStream(){
    this->accumulator = 0;
    this->bcount = 0;
    this->fp = NULL;
}

void BitStream::writeBit(int bit){
    if(bcount == 7){
        cout << accumulator << "\n";
        accumulator = 0;
        bcount = 0;
    }
    if(bit > 0)
        accumulator = accumulator |= 1 << 7-bcount;
    bcount++;
    
}

void BitStream::writeBits(int bits, int n, string f){
    ofstream fp(f);
    while(n > 0){
        writeBit(bits & 1 << n-1);
        n--;
    }
}


