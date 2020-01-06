#pragma once
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <stdio.h>
#include <unistd.h>
using namespace std;

/**
  *
  *Class that receives data and stores it so it can be written on a file later or reads data from a file and returns it.
  */

class BitStream{
private:
    int accumulator;
    int bcount;
    FILE *fp;
    char matrix;
    int vb;
    vector<char> y;
    vector<char> u;
    vector<char> v;

public:
    void writeBit(int bit);
    void writeBits(int bits, int n);
    int readBit(FILE* fileName); 
    int readBits(int bits, FILE* fileName); 
    BitStream();
    void writeAll();
    void setMatrix(char matrix);
    void resetAll();
};

BitStream::BitStream(){
    this->accumulator = 0;
    this->bcount = 0;
    this->fp = NULL;
    this->matrix = ' ';
    this->vb = 0;
}

/**
  *
  *Function that writes a single bit Requires a 'bit' If bcount is 8 then all the information stored on the accumulator will be stored on the current matrix being used by the Encoder class, and both the bcount and accumulator will be reset back to 0 If the 'bit' is 1 it will 
  *be added to the accumulator bcount will be incremented every time this function is used.
  *@param bit: number to be added to the accumulator 
  */
void BitStream::writeBit(int bit){
    if(bcount == 8){
        if(this->matrix == 'y')
            this->y.push_back(this->accumulator);
        else if(this->matrix == 'u')
            this->u.push_back(this->accumulator);
        else if(this->matrix == 'v')
            this->v.push_back(this->accumulator);
        this->accumulator = 0;
        this->bcount = 0;
    }
    if(bit > 0)
        accumulator = accumulator |= 1 << 7-bcount;
    bcount++;
    
}

/**
  *
  *Function n bits This function requires a number and the number os bits that number has Transformes the number in bits to 1s or 0s Calls writeBits n times.
  *@param: number to be written
  *@param: number of bits the number in 'bits'
  */
void BitStream::writeBits(int bits, int n){
    while(n > 0){
        writeBit(bits & 1 << n-1);
        n--;
    }
}

int BitStream::readBits(int n, FILE* fileName){
    int v = 0;
    while(n > 0){
        v = (v << 1) | readBit(fileName);
        n--;
    }
    return v;
}

/**
  *
  *Function that reads a bit from a file and return it to who called it.
  *@param fileName: file pointer to the file that will be read
  */
int BitStream::readBit(FILE* fileName){
    if(this->bcount == 0){
        int a;
        fread(&a,sizeof(char),1,fileName);
        if(a != 0)
            this->accumulator = a;
        this->bcount = 8;
    }
    int rv = (this->accumulator & (1 << this->bcount-1)) >> this->bcount-1; 
    this->bcount--;
    return rv;
}

/**
  *
  *Function that determines which frame component it should store information.
  *@param matrix: char that represents the frame component that the Encoder is working on
  */
void BitStream::setMatrix(char matrix){
    this->matrix = matrix;
}

/**
  *
  *Function that writes all info stored on the BitStream All data is stored in 3 different matrixes, after a frame has been fully loaded this function is used to write everything on a file.
  */
void BitStream::writeAll(){
    ofstream WriteFile("OutFile.txt");
    for(int i = 0; i < this->y.size(); i++){
        WriteFile << this->y.at(i);
    }
    for(int i = 0; i < this->u.size(); i++)
        WriteFile << this->u.at(i);
    for(int i = 0; i < this->v.size(); i++)
        WriteFile << this->v.at(i);
    this->y.clear();
    this->u.clear();
    this->v.clear();
    if(this->accumulator != 0)
        WriteFile << this->accumulator;
    WriteFile.close();
}
/**
  *
  *Function that resets the information to prepare for the next frame.
  **/
void BitStream::resetAll(){
    this->accumulator = 0;
    this->bcount = 0;
}

