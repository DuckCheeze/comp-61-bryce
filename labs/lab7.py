import random
SHIPS = 1
OPEN = 0
HIT = -1
MISS = -2
def build_board():
    return [[OPEN for _ in range(10)] for _ in range(10)]

def board_show(board, show=False):
    print("   ", end="")
    for x in range(10):
        print(x, end=" ")
    print()
    for y in range(10):
        print(y, end="  ")
        for x in range(10):
            cell = board[y][x]
            if cell == HIT:
                print("H", end=" ")
            elif cell == MISS:
                print("M", end=" ")
            elif show and cell == SHIPS:
                print("S", end=" ")
            else:
                print("~", end=" ")
        print()

def put_ship(board, size):
    while True:
        orientation = random.choice(["long", "latit"])
        if orientation == "long":
            x = random.randint(0, 10 - size)
            y = random.randint(0, 9)
            if all(board[y][x+i] == OPEN for i in range(size)):
                for i in range(size):
                    board[y][x+i] = SHIPS
                break
        else:
            x = random.randint(0, 9)
            y = random.randint(0, 10 - size)
            if all(board[y+i][x] == OPEN for i in range(size)):
                for i in range(size):
                    board[y+i][x] = SHIPS
                break

def ships_left(board):
    return sum(cell == SHIPS for row in board for cell in row)

def main():
    board = build_board()

    for _ in range(2):
        put_ship(board, 2)
        put_ship(board, 3)
        put_ship(board, 5)
    print("This is Battleship!\n")
    print("Please enter the coordinates to attack there (x and y between 0 and 9); (Ex:  Type '4 3').\n")
    print("You can enter -1 -1 any time to reveal the whole board (cheating like a loser).\n")
    while ships_left(board) > 0:
        board_show(board)
        try:
            x, y = map(int, input("Please enter the x and y you want to see here:  ").split())
        except ValueError:
            print("That's an invalid input. Please enter two integers, just how I showed you to before. (Ex:  Type '1 2').")
            continue
        if x == -1 and y == -1:
            print("Well you cheated, hope you're happy with this. You suck at Battleship.\n")
            board_show(board, show=True)
            continue
        if not (0 <= x < 10 and 0 <= y < 10):
            print("The coords you entered are off the board, please enter working coords. (Ex:  Type '5 9')")
            continue
        if board[y][x] == HIT or board[y][x] == MISS:
            print("You already attacked that spot, come on now pal. Enter different coords")
            continue
        if board[y][x] == SHIPS:
            print("Thats a hit! (H)")
            board[y][x] = HIT
        else:
            print("Haha you missed! (M)")
            board[y][x] = MISS

    print("\nYippee! Yippee! You sunk all the battleships! You won!")
    board_show(board, show=True)

if __name__ == "__main__":
    main()