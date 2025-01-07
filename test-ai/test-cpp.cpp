#include <iostream>
#include <string>
#include <cmath>

using namespace std;

int main ()
{
    int N, P, W, H;
    string trash;
    cin >> N >> P >> W >> H;
    cin >> trash >> trash >> trash >> trash;

    int i = 0;
    while (1)
    {
        if (i % N + 1 == P)
        {
            cout << "R" << endl;
        }
        else
        {
            cin >> trash;
        }

        i++;
    }

    return 0;
}
