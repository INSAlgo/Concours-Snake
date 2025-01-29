import time

W, H = map(int, input().split())
N, P = map(int, input().split())
j1 = tuple(map(int, input().split()))
j2 = tuple(map(int, input().split()))

directions = ["up", "right", "down", "left"]
t = 0
while True:
	time.sleep(0.08)
	if t % 2 + 1 == P:
		print(directions[t % len(directions)])
	else:
		input()
	t = t + 1
