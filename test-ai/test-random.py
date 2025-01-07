import random
import time

W, H = map(int, input().split())
N, P = map(int, input().split())
j1 = tuple(map(int, input().split()))
j2 = tuple(map(int, input().split()))

t = 0
while True:
    t = t % 2 + 1
    time.sleep(0.08)
    if t == P:
        print(random.choice(["U", "R", "D", "L"]))
    else:
        input()
