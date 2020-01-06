#pragma once
#include "BitStream.h"
#include "Golomb.h"
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <time.h>
#include <unistd.h>
using namespace std;

class Encoder{
private:
	string fileName;
	string mode;
	int width;
	int height;
	int frameLen;

public:
	Encoder(string fileName);
	void encode();
	void compress(string text,BitStream &bs);
	void decode();
	void weirdTest();
	int predictor(char *p, int i, int j, int tipo);
};

Encoder::Encoder(string fileName){
	this->fileName = fileName;
}

/**
  *
  *Sub-function of read that uses Golomb to encode data and BitStream to write it on a file.
  *@param textRead: data read from the file to be encoded by golomb and written on a file by the bitstream
  */
void Encoder::compress(string textRead,BitStream &bs){
	Golomb gol(4);
	unsigned char frameSegment[this->height][this->width];
	for(int z = 0; z < 3; z++){
		if(z == 0)
			bs.setMatrix('y');
		else if(z == 1)
			bs.setMatrix('u');
		else
			bs.setMatrix('v');
		for(int i = 0; i < this->height; i++){
			for(int j = 0; j < this->width; j++){
				frameSegment[i][j] = textRead[z*this->height + i*this->width + j];
			}
		}
		int vb = 0;
		for(int i = 0; i < this->height; i++){
			for(int j = 0; j < this->width; j++){
				vb++;
				int x = (int)frameSegment[i][j];
				char *poi = (char*)frameSegment;
				int p = predictor(poi, i, j, 1);
				int e = x - p;
				if(e < 0){
					e = (-1*(e*2)) - 1;
				}
				else{
					e = e*2;
				}
				vector<int> enc = gol.encode(e);
				for(int c = 0; c < enc.size(); c++){
					bs.writeBits(enc.at(c), 1);
				}
			}
		}
		cout << vb << endl;
	}
}

/**
  *
  *Function that reads a video file, compresses it and writes it down.
  */
void Encoder::encode(){
	ifstream ReadFile(this->fileName);
	BitStream bs;
	string textRead;
	getline(ReadFile, textRead);
	cout << textRead << "\n";
	for(int i = 0; i < textRead.length(); i++){
		if(textRead[i-1] == ' ' && textRead[i] == 'W'){
			i++;
			string width = "";
			while(textRead[i] != ' '){
				width += textRead[i];
				i++;
			}
			this->width = stoi(width);
		}
		if(textRead[i-1] == ' ' && textRead[i] == 'H'){
			i++;
			string height = "";
			while(textRead[i] != ' '){
				height += textRead[i];
				i++;
			}
			this->height = stoi(height);
		}
	}
	getline(ReadFile, textRead);
	getline(ReadFile, textRead);
	compress(textRead, bs);
	bs.writeAll();
	ReadFile.close();
}
/**
  *
  *Function that reads a compressed file, decompresses it and shows each frame.
  */
void Encoder::decode(){
	BitStream bs;
	Golomb gol(4);
	char matrix[1280][720];
	FILE* fp = fopen("OutFile.txt", "rb");
	for(int i = 0; i < 720; i++){
		for(int j = 0; j < 1280; j++){
			vector<int> num;
			while(true){
				int nBit = bs.readBits(1, fp);
				num.push_back(nBit);
				if(nBit == 0){
					for(int r = 0; r < 2; r++){
						nBit = bs.readBits(1, fp);
						num.push_back(nBit);
					}
					break;
				}
			}
			int dec = gol.decode(num);
			int e;
			if(dec%2 == 0)
				e=dec/2;
			else
				e = -1*((dec+1)/2);
			char *poi = (char *)matrix;
			int p = (int)predictor(poi, i, j, 1);
			int x = e + p;
			cout << x << endl;
		}
	}
}

/**
  *
  *Function used to predict the next value of the image matrix, used by writeData and readData.
  *@param p: array with data on the frame
  *@param tipo: predictor type
  */
int Encoder::predictor(char *p, int i, int j, int tipo){
	int a = 0;
	int b = 0;
	int c = 0;
	if(tipo == 1){
		if(j > 0)
			return p[i*this->width+(j-1)];
		return 0;
	}
}