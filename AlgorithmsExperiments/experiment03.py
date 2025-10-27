def cover_board(top_row, top_col, missing_row, missing_col, board_size):
    global tile_count
    if board_size == 1:
        return
    t = tile_count
    s = board_size // 2

    # 覆盖左上象限
    if missing_row < top_row + s and missing_col < top_col + s:
        cover_board(top_row, top_col, missing_row, missing_col, s)
    else:
        board[top_row + s - 1][top_col + s - 1] = t
        tile_count += 1
        cover_board(top_row, top_col, top_row + s - 1, top_col + s - 1, s)

    # 覆盖右上象限
    if missing_row < top_row + s and missing_col >= top_col + s:
        cover_board(top_row, top_col + s, missing_row, missing_col, s)
    else:
        board[top_row + s - 1][top_col + s] = t
        tile_count += 1
        cover_board(top_row, top_col + s, top_row + s - 1, top_col + s, s)

    # 覆盖左下象限
    if missing_row >= top_row + s and missing_col < top_col + s:
        cover_board(top_row + s, top_col, missing_row, missing_col, s)
    else:
        board[top_row + s][top_col + s - 1] = t
        tile_count += 1
        cover_board(top_row + s, top_col, top_row + s, top_col + s - 1, s)

    # 覆盖右下象限
    if missing_row >= top_row + s and missing_col >= top_col + s:
        cover_board(top_row + s, top_col + s, missing_row, missing_col, s)
    else:
        board[top_row + s][top_col + s] = t
        tile_count += 1
        cover_board(top_row + s, top_col + s, top_row + s, top_col + s, s)

def print_board(board_size):
    for i in range(board_size):
        for j in range(board_size):
            print(f"{board[i][j]:5}", end=" ")
        print()

# 初始化全局变量
tile_count = 1
n = 4  # 棋盘大小为 2^n x 2^n
board_size = 2 ** n
board = [[0 for _ in range(board_size)] for _ in range(board_size)]

# 假设残缺方格的位置
missing_row, missing_col = 1, 1

# 调用函数开始覆盖
cover_board(0, 0, missing_row, missing_col, board_size)

# 输出棋盘
print_board(board_size)