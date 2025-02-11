import sys

W, H = map(int, input().split())
G = int(input())
N, P = map(int, input().split())
players = [tuple(map(int, input().split())) for _ in range(N)]

pos = players[P-1]
taken = set([pos])

dir = 1

def is_clear(x, y):
	return 0 <= x < W and 0 <= y < H and (x, y) not in taken


def handle_enemy():
	move = input()

t = 0
while True:
	if t % N == P-1:
		for d in (dir, -dir):
			nx, ny = pos[0] + d, pos[1]
			if is_clear(nx, ny):
				dir = d
				pos = (nx, ny)
				match dir:
					case 1:
						print('down')
					case -1:
						print('up')
				break
		else:
			nx, ny = pos[0], pos[1] + 1
			if is_clear(nx, ny):
				pos = (nx, ny)
				print('right')
			else:
				nx, ny = pos[0], pos[1] - 1
				pos = (nx, ny)
				print('left')
			dir = -dir

		taken.add(pos)
	else:
		handle_enemy()
	t = t + 1
	sys.stdout.flush()