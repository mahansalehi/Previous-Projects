##Gomoku

def is_empty(board):
    for y in range (len(board)):
        for x in range(len(board[y])):
            if board [y][x]!= " ":
                return False
    return True
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):

    start_y = y_end - length*d_y
    start_x = x_end - length*d_x 
    final_y = y_end + d_y
    final_x = x_end + d_x
   
    open_start = in_board(start_y, start_x, board) \
    and board[start_y][start_x] == " " 
    open_final = in_board(final_y, final_x, board) \
    and board[final_y][final_x] == " "
    
    if (open_start and open_final):
        return "OPEN"
    elif open_start or open_final:
        return "SEMIOPEN"
    else:
        return "CLOSED"
    
            
def in_board(y, x, board): 
    return (y < len(board) and y >= 0) and (x < len(board) and x >= 0)
  
         
def test_is_bounded():
    
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 1, 0, 1, 2, "b")
    print_board(board)
    assert is_bounded(board, 0, 2, 2, 0, 1) == "OPEN"
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 0, 0, 1, 2, "b")
    print_board(board)
    assert is_bounded(board, 0, 1, 2, 0, 1) == "SEMIOPEN"
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 6, 1, 1, 2, "b")
    print_board(board)
    assert is_bounded(board, 1, 7, 2, 1, 1) == "CLOSED"
    board = make_empty_board(8)
    put_seq_on_board(board, 5, 5, 1, 1, 2, "b")
    print_board(board)
    assert is_bounded(board, 6, 6, 2, 1, 1) == "OPEN"
   
def detect_all_row_including_closed(board, colour, sy, sx, length, dy, dx):
    
    open_seq_count, semi_seq_count, closed_seq_count = 0, 0, 0
    y = sy
    x = sx
    prev_char = 0
    cur_len = 0
    
    while in_board(y, x, board):
        cur_char = board[y][x]
        
        if prev_char == cur_char:
            cur_len += 1
        else: #cur_char != prev_char
            if cur_char == colour:#start sequence
                cur_len = 1
            elif prev_char == colour and cur_len == length: #end sequence
            
                boundary = is_bounded(board, y-dy, x-dx, length, dy, dx) 
                if boundary == "OPEN":
                    open_seq_count += 1
                if boundary == "SEMIOPEN":
                    semi_seq_count += 1
                if boundary == "CLOSED":
                    closed_seq_count +=1
            else:
                cur_len = 0
        
        y += dy
        x += dx        
        prev_char = cur_char  
              
    if prev_char == colour and cur_len == length: #end sequence
            
        boundary = is_bounded(board, y-dy, x-dx, length, dy, dx) 
        if boundary == "OPEN":
            open_seq_count += 1
        if boundary == "SEMIOPEN":
            semi_seq_count += 1  
        if boundary == "CLOSED":
            closed_seq_count +=1                 
                
    return open_seq_count, semi_seq_count, closed_seq_count
    

def detect_row(board, colour, sy, sx, length, dy, dx):
    
    open_seq_count, semi_seq_count, closed_seq_count = \
    detect_all_row_including_closed(board, colour, sy, sx ,length, dy, dx)
    
    return open_seq_count, semi_seq_count
    
  
def test_detect_all_row_including_closed():
    
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 6, 0, 1, 2, "b")
    print_board(board)
    assert detect_all_row_including_closed\
    (board, "b", 0, 0, 2, 0,  1) == (0, 1, 0)
    
    #detect_row(board, col, y_start, x_start, length, d_y, d_x):
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 1, 0, 1, 2, "b")
    print_board(board)
    assert detect_all_row_including_closed\
    (board, "b", 0, 0, 2, 0,  1) == (1, 0, 0)
  
    board = make_empty_board(8)
    put_seq_on_board(board, 1, 1, 1, 1, 2, "b")
    print_board(board)
    assert detect_all_row_including_closed\
    (board, "b", 0, 0, 2, 1,  1) == (1, 0, 0)
    
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 0, 1, 1, 3, "b")
    print_board(board)
    assert detect_all_row_including_closed\
    (board, "b", 0, 0, 3, 1,  1) == (0, 1, 0)
    
    #detect row less than sequence length
    board = make_empty_board(8)
    put_seq_on_board(board, 1, 1, 1, 1, 3, "b")
    print_board(board)
    assert detect_all_row_including_closed\
    (board, "b", 0, 0, 2, 1,  1) == (0, 0, 0)
    
    #detect row greater than sequence length
    board = make_empty_board(8)
    put_seq_on_board(board, 1, 1, 1, 1, 2, "b")
    print_board(board)
    assert detect_all_row_including_closed\
    (board, "b", 0, 0, 3, 1,  1) == (0, 0, 0)
    
    board = make_empty_board(8)
    board[0][0] = "w"
    put_seq_on_board(board, 1, 1, 1, 1, 2, "b")
    print_board(board)
    assert detect_all_row_including_closed\
    (board, "b", 0, 0, 2, 1,  1) == (0, 1, 0)
    
    board = make_empty_board(8)
    board[3][3] = "w"
    put_seq_on_board(board, 1, 1, 1, 1, 2, "b")
    print_board(board)
    assert detect_all_row_including_closed\
    (board, "b", 0, 0, 2, 1,  1) == (0, 1, 0)
    
    board = make_empty_board(8)
    board[0][0] = "w"
    board[3][3] = "w"
    put_seq_on_board(board, 1, 1, 1, 1, 2, "b")
    print_board(board)
    assert detect_all_row_including_closed\
    (board, "b", 0, 0, 2, 1,  1) == (0, 0, 1)
    

def detect_all_rows_including_closed(board, colour, length):
    
    open_total, semi_total, closed_total = 0, 0, 0
 
    for dy, dx in [(0, 1),(1, 0), (1, 1), (1, -1)]:
    
        for sy, sx in get_start(board, dy, dx):
         
            open_seq_count, semi_seq_count, closed_seq_count = \
            detect_all_row_including_closed (board, colour, sy, \
            sx, length, dy, dx)
            
            open_total += open_seq_count
            semi_total += semi_seq_count
            closed_total += closed_seq_count
   
    return open_total, semi_total, closed_total

    
def detect_rows(board, colour, length):
    
    open_total, semi_total, closed_seq_count = \
    detect_all_rows_including_closed(board, colour, length)
    
    return open_total, semi_total


def test_detect_all_rows_including_closed():
    
    board = make_empty_board(8)
    put_seq_on_board(board, 1, 2, 0, 1, 4, "w")
    put_seq_on_board(board, 4, 2, 0, 1, 4, "w")
    put_seq_on_board(board, 2, 2, 1, 0, 2, "w")
    put_seq_on_board(board, 2, 5, 1, 0, 2, "w")
    put_seq_on_board(board, 2, 3, 0, 1, 2, "b")
    put_seq_on_board(board, 3, 3, 0, 1, 2, "b")
    print_board(board)
    assert detect_all_rows_including_closed(board, "b", 2) == (0, 0, 6)

    board = make_empty_board(8)
    board[5][5] = "b"
    board[5][6] = "b"
    board[6][6] = "b"
    board[6][5] = "b"
    print_board(board)
    assert detect_all_rows_including_closed(board, "b", 2) == (6, 0, 0)

    board = make_empty_board(8)
    board[5][7] = "b"
    board[6][7] = "b"
    board[5][6] = "b"
    board[6][6] = "b"
    print_board(board)
    assert detect_all_rows_including_closed(board, "b", 2) == (2, 4, 0)

    board = make_empty_board(8)
    board[7][7] = "b"
    board[6][7] = "b"
    board[7][6] = "b"
    board[6][6] = "b"
    print_board(board)
    assert detect_all_rows_including_closed(board, "b", 2) == (0, 5, 1)
    

def get_start(board, dy, dx):
    
    if dy == 0 and dx == 1:
        #return [(y, 0) for y in range (len(board))]
        a = []
        for y in range (len(board)):
            a.append((y, 0))
        return a
    
    if dy == 1 and dx == 0:
        a = []
        for x in range (len(board)):
            a.append((0, x))
        return a
        
    if dy == 1 and dx == 1:
        a = []
        for y in range (len(board)):
            a.append((y, 0))
        for x in range (1,len(board)):
            a.append((0, x))
        return a
    
    if dy == 1 and dx == -1:
        a = []
        for x in range (len(board)):
            a.append((0, x))
        for y in range (1,len(board)):
            a.append((y, 7))
        return a
        
            
def test_get_start():
    board = make_empty_board(8)
    print(get_start(board, 1, -1))
    
def search_max(board):
    
    max_score = -100001
    move_y = 0 
    move_x = 0
  
    for y in range (len(board)):
        for x in range(len(board[y])):
                if board[y][x] == " ":
                    board[y][x] = "b"
                    cur_score = score(board)
                    win = is_win(board)
                    if win == "Black won":
                        cur_score = 100000
                        board[y][x] = " "
                        move_y = y
                        move_x = x
                        return move_y, move_x
                    if cur_score > max_score:
                        max_score = cur_score
                        move_y = y
                        move_x = x
                    
                    board[y][x] = " "
                    
    return move_y, move_x
    

def test_search_max():
    
    board = make_empty_board(8)
    board[2][4], board[3][3], board[4][2], board[6][4] = "w", "w", "w", "w"
    board[3][4], board[4][4], board[5][4], board[4][3] = "b", "b", "b", "b"
    assert search_max(board) == (1, 5)
    board[1][5] = "b"
    board[5][1] = "w"
    assert search_max(board) == (6,  0)
    
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 1, 0, 1, 4, "b")
    print_board(board)
    assert search_max(board) == (0, 0) 

    board = make_empty_board(8)
    put_seq_on_board(board, 0, 0, 0, 1, 2, "b")
    print_board(board)
    assert search_max(board) == (0, 2)   

    board = make_empty_board(8)
    put_seq_on_board(board, 0, 0, 0, 1, 4, "b")
    put_seq_on_board(board, 1, 4, 1, 0, 2, "b")
    print_board(board)
    assert search_max(board) == (0, 4) 
    
    board = make_empty_board(8)
    put_seq_on_board(board, 3, 3, 0, 1, 3, "b")
    put_seq_on_board(board, 4, 2, 1, 0, 3, "b")
    put_seq_on_board(board, 4, 3, 1, 0, 3, "b")
    put_seq_on_board(board, 4, 4, 1, 0, 3, "b")
    put_seq_on_board(board, 4, 5, 1, 0, 3, "b")
    print_board(board)
    assert search_max(board) == (2, 3) 

    

def score(board):
    
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

    
def is_win(board):
   
    open_b = {}
    semi_open_b = {}
    closed_b = {}
    open_w = {}
    semi_open_w = {}
    closed_w = {}
    
    i = 5
    
    open_b[i], semi_open_b[i], closed_b[i] = \
    detect_all_rows_including_closed(board, "b", i)
    open_w[i], semi_open_w[i], closed_w[i] = \
    detect_all_rows_including_closed(board, "w", i)
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1 or closed_b[5]>=1:
        return "Black won"
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1 or closed_w[5]>=1:
        return "White won"
    
    elif is_full(board):
        return "Draw"
    
    return "Continue playing"

def test_is_win():
    
    board = make_empty_board(8)
    y = 0; x = 2; d_x = 1; d_y = 0; length = 4
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    assert (0, 1) == search_max(board)
    board[0][1] = "b"
    assert is_win(board) == "Black won"
    print_board(board)
    
def is_full(board):

    for y in range (len(board)):
        for x in range(len(board[y])):
            if board [y][x] == " ":
                return False
    return True


def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
        
    
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

            
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x
        
def some_tests():
    board = make_empty_board(8)
    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


  
            
if __name__ == '__main__':
    
    play_gomoku(8)
    # test_is_win()
    # test_is_bounded()
    # test_detect_all_row_including_closed()
    # test_detect_all_rows_including_closed()
    # some_tests()
    # test_search_max()
    