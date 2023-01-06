# This will contain the connect 4 logic for detecting when a game is complete and which player has won.
# It will also store a copy of the board.


def initializeBoard(board):
    a = [0] * 7
    b = [0] * 7
    c = [0] * 7
    d = [0] * 7
    e = [0] * 7
    f = [0] * 7

    board = [a, b, c, d, e, f]

    return board


def checkForEmpty(board):
    for i in range(6):
        for j in range(7):
            if board[i][j] != 0:
                return False
    return True


def construct_board(newBoardString):
    newBoard = [[]]
    newBoard = initializeBoard(newBoard)
    for i in range(6):
        for j in range(7):
            # Get a character from the string
            char = newBoardString[i * 8 + j]
            if char == '#':
                newBoard[i][j] = 0
            elif char == 'X':
                newBoard[i][j] = -1
            elif char == 'O':
                newBoard[i][j] = 1
    return newBoard


def insertPiece(colLabel, player, board):
    for i, value in reversed(list(enumerate(board))):
        print("value of i: ", i)
        if board[i][colLabel] == 0:
            print(i, " ", colLabel)
            if player == 1:
                board[i][colLabel] = -1
            elif player == 2:
                board[i][colLabel] = 1
            break


def calculateNumberOfRedPieces(board):
    count = 0
    for i in range(6):
        for j in range(7):
            if board[i][j] == 1:
                count += 1
    return count


def calculateNumberOfYellowPieces(board):
    count = 0
    for i in range(6):
        for j in range(7):
            if board[i][j] == -1:
                count += 1
    return count


def checkVictory(board):
    # Check if there are 4 in a row horizontally
    for i in range(6):
        for j in range(4):
            if board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == -1:
                return True, 1
            elif board[i][j] == board[i][j + 1] == board[i][j + 2] == board[i][j + 3] == 1:
                return True, 2

    # Check if there are 4 in a row vertically
    for i in range(3):
        for j in range(7):
            if board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] == -1:
                return True, 1
            elif board[i][j] == board[i + 1][j] == board[i + 2][j] == board[i + 3][j] == 1:
                return True, 2

    # Check if there are 4 in a row diagonally
    for i in range(3):
        for j in range(4):
            if board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == -1:
                return True, 1
            elif board[i][j] == board[i + 1][j + 1] == board[i + 2][j + 2] == board[i + 3][j + 3] == 1:
                return True, 2

    # Check if there are 4 in a row diagonally
    for i in range(3, 6):
        for j in range(4):
            if board[i][j] == board[i - 1][j + 1] == board[i - 2][j + 2] == board[i - 3][j + 3] == -1:
                return True, 1
            elif board[i][j] == board[i - 1][j + 1] == board[i - 2][j + 2] == board[i - 3][j + 3] == 1:
                return True, 2

    return False, 0


def printBoard(board):
    for i in range(len(board)):
        print(i, end=' ')
        print(board[i])
    print("----------------------------")
    print("#", [0, 1, 2, 3, 4, 5, 6])


def gameEnd():
    pass
