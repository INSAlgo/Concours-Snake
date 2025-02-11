import random
import time

W, H = map(int, input().split())
G = int(input())
N, P = map(int, input().split())
j1 = tuple(map(int, input().split()))
j2 = tuple(map(int, input().split()))

t = 0
while True:
    time.sleep(0.08)
    if t % 2 == P - 1:
        print(random.choice(["up", "right", "down", "left"]))
    else:
        input()
    t += 1
