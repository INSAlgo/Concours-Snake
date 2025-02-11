import time

W, H = map(int, input().split())
G = int(input())
N, P = map(int, input().split())
j1 = tuple(map(int, input().split()))
j2 = tuple(map(int, input().split()))

directions = ["down", "right", "up", "left"]
t = 0
while True:
	time.sleep(0.08)
	if t % 2 == P - 1:
		print(directions[t % len(directions)])
	else:
		input()
	t += 1
