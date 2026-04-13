def is_safe(board, row, col, n):
    for i in range(col):
        if board[row][i] == "Q":
            return False

    for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[i][j] == "Q":
            return False

    for i, j in zip(range(row, n, 1), range(col, -1, -1)):
        if board[i][j] == "Q":
            return False

    return True

def solve_n_queens_util(board, col, n):
    if col >= n:
        return True

    for i in range(n):
        if is_safe(board, i, col, n):
            board[i][col] = "Q"

            if solve_n_queens_util(board, col + 1, n):
                return True

            board[i][col] = "-"

    return False

def solve_n_queens(n):
    board = [["-" for _ in range(n)] for _ in range(n)]
    if solve_n_queens_util(board, 0, n):
        for row in board:
            print(" ".join(row))
    else:
        print("No solution exists.")

n = 4
solve_n_queens(n)
