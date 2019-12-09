#include "Golomb.h"
#include <vector>

using namespace std;

int main(){
    Golomb golomb(4);
    vector<int> l = golomb.encode(11);
    int x = golomb.decode(l);
    cout << "\n" << x;
    return 0;
}