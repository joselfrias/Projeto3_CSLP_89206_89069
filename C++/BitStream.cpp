#include "BitStream.h"
#include <string>
using namespace std;

int main(){

    BitStream bs;
    string ch = "001100101";
    string outFile = "out";
    for(int c = 0; c < ch.length(); c++){
        int asc = ch[c];
        bs.writeBits(asc,1, outFile);
    }
    return 0;
}