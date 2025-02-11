#include <iostream>
#include <string>
#include <cmath>

using namespace std;

int main ()
{
    int W, H, G, N, P;
    string trash;
    cin >> W >> H >> G >> N >> P;
    cin >> trash >> trash >> trash >> trash;

    int i = 0;
    while (1)
    {
        if (i % N == P - 1)
        {
            cout << "right" << endl;
        }
        else
        {
            cin >> trash;
        }

        i++;
    }

    return 0;
}
