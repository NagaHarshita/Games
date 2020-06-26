board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

def find_empty(board):
    for i in range(9):
        for j in range(9):
            if(board[i][j]==0):
                return [i,j]
    
    return None


def valid_position(board,num,pos):
    for j in range(9):
        if(board[pos[0]][j]==num and pos[1]!=j):
            return False
    for i in range(9):
        if(board[i][pos[1]]==num and pos[0]!=i):
            return False
    box_row = pos[0]//3
    box_col = pos[1]//3

    for i in range(box_row*3,box_row*3+3):
        for j in range(box_col*3,box_col*3+3):
            if(board[i][j]==num and [i,j]!=pos):
                return False

    return True

def print_board(board):
    for i in range(9):
        if(i%3==0 and i!=0):
            print("------------------------")
        for j in range(9):
            if(j%3==0 and j!=0):
                print(" | {} ".format(board[i][j]),end="")
            elif(j==8):
                print(board[i][j])
            else:
                print(board[i][j],end=" ")


def sudoku_solver(board):
    find = find_empty(board)

    if find is None:
        return True

    for i in range(1,10):
        if valid_position(board,i,find) is True:
            board[find[0]][find[1]] = i

            if sudoku_solver(board):
                return True
            
            board[find[0]][find[1]] = 0

print_board(board)
sudoku_solver(board)
print("__________________________________")
print_board(board)