#pragma once
#include <math.h>
#include <vector>
#include <string>
#include <iostream>

using namespace std;

class Golomb{
private:
    int m;
    int b;

public:
    vector<int> encode(int number);
    int decode(vector<int> codigo);
    Golomb(int m);
};

Golomb::Golomb(int m){
    this->m=m;
    this->b=ceil(log2(m));
}

vector<int> Golomb::encode(int number){
    int q = number/m;
    int r = number%r;
    vector<int> ret;
    for(int i = 0; i < q; i++){
        ret.push_back(1);
    } 
    ret.push_back(0);
    for(int i = b - 1; i > -1; i-- ){
        int bit = (r >> i) & 1;
        ret.push_back(bit);
    }
    for(int i = 0; i < ret.size(); i++){
        cout << ret.at(i);
    }
    return ret;
}

int Golomb::decode(vector<int> codigo){
    int q = 0;
    while(codigo.size() > 0){
        int a = codigo.at(codigo.size() - 1);
        codigo.pop_back();
        if(a == 0){
            break;
        }
        q++;
    }
    int r = 0;
    for(int i = b-1; i > -1; i--){
        int bit = codigo.at(codigo.size() - 1);
        codigo.pop_back();
        r = r + bit << i;
    }
    return q*m + r;
    
    //return 0;
}

