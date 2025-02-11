import sys

W, H = map(int, input().split())
G = int(input())
N, P = map(int, input().split())
heads = [tuple(map(int, input().split())) for _ in range(N)]
players = [[heads[p]] for p in range(N)]
directions2deltas = {
    "up": (0, -1),
    "right": (1, 0),
    "down": (0, 1),
    "left": (-1, 0),
}


def update_position(player, direction, turn):
    x, y = heads[player]
    dx, dy = directions2deltas[direction]
    head = x + dx, y + dy
    heads[player] = head
    players[player].append(head)
    if (turn // N) % G != 0:
        players[player].pop(0)


def main():
    turn = 0

    while True:
        player = turn % N

        # Tour de notre IA
        if player == P - 1:
            direction = "right"
            update_position(player, direction, turn)
            print(direction)
            sys.stdout.flush()
        # Tour adversaire
        else:
            direction = input().split()[2]
            print(f"> {direction}")  # Debug
            update_position(player, direction, turn)
        
        turn += 1

if __name__ == "__main__":
    main()
