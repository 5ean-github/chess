import time
import pygame
import copy

w_rook = pygame.image.load('w_rook.png')
w_rook = pygame.transform.scale(w_rook, (95,95))
b_rook = pygame.image.load('b_rook.png')
b_rook = pygame.transform.scale(b_rook, (95,95))
w_bishop = pygame.image.load('w_bishop.png')
w_bishop = pygame.transform.scale(w_bishop, (95,95))
b_bishop = pygame.image.load('b_bishop.png')
b_bishop = pygame.transform.scale(b_bishop, (95,95))
w_queen = pygame.image.load('w_queen.png')
w_queen = pygame.transform.scale(w_queen, (95,95))
b_queen = pygame.image.load('b_queen.png')
b_queen = pygame.transform.scale(b_queen, (95,95))
w_king = pygame.image.load('w_king.png')
w_king = pygame.transform.scale(w_king, (95,95))
b_king = pygame.image.load('b_king.png')
b_king = pygame.transform.scale(b_king, (95,95))
w_knight = pygame.image.load('w_knight.png')
w_knight = pygame.transform.scale(w_knight, (95,95))
b_knight = pygame.image.load('b_knight.png')
b_knight = pygame.transform.scale(b_knight, (95,95))
w_pawn = pygame.image.load('w_pawn.png')
w_pawn = pygame.transform.scale(w_pawn, (95,95))
b_pawn = pygame.image.load('b_pawn.png')
b_pawn = pygame.transform.scale(b_pawn, (95,95))

def setup_board(board):
    board = [['w_rook','w_knight','w_bishop','w_queen','w_king','w_bishop','w_knight','w_rook'],['w_pawn','w_pawn','w_pawn','w_pawn','w_pawn','w_pawn','w_pawn','w_pawn']]
    for i in range(4):
        board.append([' ',' ',' ',' ',' ',' ',' ',' '])
    board.append(['b_pawn','b_pawn','b_pawn','b_pawn','b_pawn','b_pawn','b_pawn','b_pawn'])
    board.append(['b_rook','b_knight','b_bishop','b_queen','b_king','b_bishop','b_knight','b_rook'])
    for i in range(len(board)):
        for j in range(i+1, len(board)):
            board[i][j],board[j][i] = board[j][i],board[i][j]
    return(board)

def coordToSquare(pos):
    square_x = int((pos[0] - 30)/95.3 + 1)
    square_y = int((769 - pos[1])/94.8 + 1)
    return square_x, square_y

def squareToCoord(square):
    pos_x = 30 + 95.3*square[0] - 95.3
    pos_y = 769 - 94.8*square[1]
    return pos_x,pos_y

def highlight(pos):
    s = pygame.Surface((95,95), pygame.SRCALPHA)   # per-pixel alpha
    s.fill((255,255,0,128))
    screen.blit(s, pos)

def color(piece):
    if 'b_' in piece:
        return 'black'
    if 'w_' in piece:
        return 'white'
    return 'empty'

def opposite(col):
    if col == 'black':
        return 'white'
    return 'black'

def pieceType(piece):
    if piece == ' ':
        return ' '
    return piece.split('_')[1]

def availableMoves(pieceType, col, square, bd, castle):
    moves = []
    if pieceType == 'pawn' and col == 'white':
        if square[1] == 2 and bd[square[0]-1][square[1]] == ' ' and bd[square[0]-1][square[1]+1] == ' ':
            moves.append((square[0],square[1]+2))
        if square[1] < 8 and bd[square[0]-1][square[1]] == ' ':
            moves.append((square[0],square[1]+1))
        if square[1] < 8 and square[0] < 8 and color(bd[square[0]][square[1]]) == 'black':
            moves.append((square[0]+1,square[1]+1))
        if square[1] < 8 and square[0] > 1 and color(bd[square[0]-2][square[1]]) == 'black':
            moves.append((square[0]-1,square[1]+1))
        if square[1] == 5 and len(ep) != 0 and ep[0][0] == 'black' and (ep[0][1] == square[0]+1 or ep[0][1] == square[0]-1):
            moves.append((ep[0][1],square[1]+1))
    if pieceType == 'pawn' and col == 'black':
        if square[1] == 7 and bd[square[0]-1][square[1]-2] == ' ' and bd[square[0]-1][square[1]-3] == ' ':
            moves.append((square[0],square[1]-2))
        if square[1] > 1 and bd[square[0]-1][square[1]-2] == ' ':
            moves.append((square[0],square[1]-1))
        if square[1] < 8 and square[0] < 8 and color(bd[square[0]][square[1]-2]) == 'white':
            moves.append((square[0]+1,square[1]-1))
        if square[1] < 8 and square[0] > 1 and color(bd[square[0]-2][square[1]-2]) == 'white':
            moves.append((square[0]-1,square[1]-1))
        if square[1] == 4 and len(ep) != 0 and ep[0][0] == 'white' and (ep[0][1] == square[0]+1 or ep[0][1] == square[0]-1):
            moves.append((ep[0][1],square[1]-1))
    if pieceType == 'king':
        for i in range(-2,1):
            for j in range(-2,1):
                if (i,j) != (-1,-1) and 0 <= square[0]+i <= 7 and 0 <= square[1]+j <= 7 and color(bd[square[0]+i][square[1]+j]) != col:
                    moves.append((square[0]+i+1, square[1]+j+1))
        if col == 'white' and w_king_moved == False and castle == False:
            if w_rook_l == False and board[1][0] == ' ' and board[2][0] == ' ' and board[3][0] == ' ' and not check(bd,'black',True):
                b1 = copy.deepcopy(bd)
                b2 = copy.deepcopy(bd)
                b1[2][0] = 'w_king'
                b2[3][0] = 'w_king'
                if not check(b1,'black', True) and not check(b2,'black', True):
                    moves.append((3,1))
            if w_rook_r == False and board[6][0] == ' ' and board[5][0] == ' ' and not check(bd,'black',True):
                b1 = copy.deepcopy(bd)
                b2 = copy.deepcopy(bd)
                b1[5][0] = 'w_king'
                b2[6][0] = 'w_king'
                if not check(b1,'black', True) and not check(b2,'black', True):
                    moves.append((7,1))
        if col == 'black' and b_king_moved == False and castle == False:
            if b_rook_l == False and board[1][7] == ' ' and board[2][7] == ' ' and board[3][7] == ' ' and not check(bd,'white',True):
                moves.append((3,8))
            if b_rook_r == False and board[6][7] == ' ' and board[5][7] == ' ' and not check(bd,'white',True):
                moves.append((7,8))


    if pieceType == 'knight':
        squares = [(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2)]
        for i in range(len(squares)):
            if 1 <= square[0]+squares[i][0] <= 8 and 1 <= square[1]+squares[i][1] <= 8 and color(bd[square[0]+squares[i][0]-1][square[1]+squares[i][1]-1]) != col:
                moves.append((square[0]+squares[i][0],square[1]+squares[i][1]))
    if pieceType == 'rook' or pieceType == 'queen':
        i,j = square[0],square[1]
        while i<=7:
            i += 1
            if color(bd[i-1][j-1]) == 'empty':
                moves.append((i,j))
            if color(bd[i-1][j-1]) == opposite(col):
                moves.append((i,j))
                break
            if color(bd[i-1][j-1]) == col:
                break
        i,j = square[0],square[1]
        while i>=2:
            i -= 1
            if color(bd[i-1][j-1]) == 'empty':
                moves.append((i,j))
            if color(bd[i-1][j-1]) == opposite(col):
                moves.append((i,j))
                break
            if color(bd[i-1][j-1]) == col:
                break
        i,j = square[0],square[1]
        while j<=7:
            j += 1
            if color(bd[i-1][j-1]) == 'empty':
                moves.append((i,j))
            if color(bd[i-1][j-1]) == opposite(col):
                moves.append((i,j))
                break
            if color(bd[i-1][j-1]) == col:
                break
        i,j = square[0],square[1]
        while j>=2:
            j -= 1
            if color(bd[i-1][j-1]) == 'empty':
                moves.append((i,j))
            if color(bd[i-1][j-1]) == opposite(col):
                moves.append((i,j))
                break
            if color(bd[i-1][j-1]) == col:
                break
    if pieceType == 'bishop' or pieceType == 'queen':
        i,j = square[0],square[1]
        while i<=7 and j<=7:
            i += 1
            j += 1
            if color(bd[i-1][j-1]) == 'empty':
                moves.append((i,j))
            if color(bd[i-1][j-1]) == opposite(col):
                moves.append((i,j))
                break
            if color(bd[i-1][j-1]) == col:
                break
        i,j = square[0],square[1]
        while i>=2 and j>=2:
            i -= 1
            j -= 1
            if color(bd[i-1][j-1]) == 'empty':
                moves.append((i,j))
            if color(bd[i-1][j-1]) == opposite(col):
                moves.append((i,j))
                break
            if color(bd[i-1][j-1]) == col:
                break
        i,j = square[0],square[1]
        while i<=7 and j>=2:
            i += 1
            j -= 1
            if color(bd[i-1][j-1]) == 'empty':
                moves.append((i,j))
            if color(bd[i-1][j-1]) == opposite(col):
                moves.append((i,j))
                break
            if color(bd[i-1][j-1]) == col:
                break
        i,j = square[0],square[1]
        while i>=2 and j<=7:
            i -= 1
            j += 1
            if color(bd[i-1][j-1]) == 'empty':
                moves.append((i,j))
            if color(bd[i-1][j-1]) == opposite(col):
                moves.append((i,j))
                break
            if color(bd[i-1][j-1]) == col:
                break
    return moves

def check(bd, col, castle):
    for i in range(len(bd)):
        for j in range(len(bd[i])):
            if color(bd[i][j]) == col:
                moves = availableMoves(pieceType(bd[i][j]),col,(i+1,j+1),bd,castle)
                for k in range(len(moves)):
                    if pieceType(bd[moves[k][0]-1][moves[k][1]-1]) == 'king' and color(bd[moves[k][0]-1][moves[k][1]-1]) == opposite(col):
                        return True
    return False

def legalMoves(pieceType, col, square, bd, castle):
    moves = availableMoves(pieceType, col, square, bd, castle)
    i = 0
    while(i<len(moves)):
        tempBoard = copy.deepcopy(bd)
        tempBoard[moves[i][0]-1][moves[i][1]-1] = tempBoard[square[0]-1][square[1]-1]
        tempBoard[square[0]-1][square[1]-1] = ' '
        
        if check(tempBoard,opposite(col),castle):
            moves.pop(i)
            i -= 1
            
        i += 1
    return moves

def insufficient(col):
    kb = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if color(board[i][j]) == col:
                if pieceType(board[i][j]) == 'pawn' or pieceType(board[i][j]) == 'queen' or pieceType(board[i][j]) == 'rook':
                    return False
                if pieceType(board[i][j]) == 'knight' or pieceType(board[i][j]) == 'bishop':
                    kb += 1
                    if kb == 2:
                        return False
    return True


def start():
    while True:
        global pieceSelected, squareSelected, turn, start_ticks, white_time, black_time, w_rook_l, w_rook_r, b_rook_l, b_rook_r, w_king_moved, b_king_moved, promote
        screen.fill((255,255,255))
        screen.blit(board_img, (0,0))
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 'b_pawn':
                    screen.blit(b_pawn, squareToCoord((i+1,j+1)))
                if board[i][j] == 'w_pawn':
                    screen.blit(w_pawn, squareToCoord((i+1,j+1)))
                if board[i][j] == 'b_rook':
                    screen.blit(b_rook, squareToCoord((i+1,j+1)))
                if board[i][j] == 'w_rook':
                    screen.blit(w_rook, squareToCoord((i+1,j+1)))
                if board[i][j] == 'b_knight':
                    screen.blit(b_knight, squareToCoord((i+1,j+1)))
                if board[i][j] == 'w_knight':
                    screen.blit(w_knight, squareToCoord((i+1,j+1)))
                if board[i][j] == 'b_bishop':
                    screen.blit(b_bishop, squareToCoord((i+1,j+1)))
                if board[i][j] == 'w_bishop':
                    screen.blit(w_bishop, squareToCoord((i+1,j+1)))
                if board[i][j] == 'b_queen':
                    screen.blit(b_queen, squareToCoord((i+1,j+1)))
                if board[i][j] == 'w_queen':
                    screen.blit(w_queen, squareToCoord((i+1,j+1)))
                if board[i][j] == 'b_king':
                    screen.blit(b_king, squareToCoord((i+1,j+1)))
                if board[i][j] == 'w_king':
                    screen.blit(w_king, squareToCoord((i+1,j+1)))
        timer_black = ''
        timer_white = ''
        if turn == 'white':
            mins_b, secs_b = divmod(int(black_time), 60)
            timer_black = '{:02d}:{:02d}'.format(mins_b, secs_b)
            t=int(white_time-(pygame.time.get_ticks()-start_ticks)/1000)
            mins_w, secs_w = divmod(t, 60)
            timer_white = '{:02d}:{:02d}'.format(mins_w, secs_w)
            if timer_white == '00:00':
                if not insufficient('black'):
                    print('black won by timeout')
                else:
                    print('drew by timeout vs insufficient material')
                break
        if turn == 'black':
            mins_w, secs_w = divmod(int(white_time), 60)
            timer_white = '{:02d}:{:02d}'.format(mins_w, secs_w)
            t=int(black_time-(pygame.time.get_ticks()-start_ticks)/1000)
            mins_b, secs_b = divmod(t, 60)
            timer_black = '{:02d}:{:02d}'.format(mins_b, secs_b)
            if timer_black == '00:00':
                if not insufficient('white'):
                    print('white won by timeout')
                else:
                    print('drew by timeout vs insufficient material')
                break
        text_white = font.render(timer_white, False, (0, 0, 0))
        text_black = font.render(timer_black, False, (0, 0, 0))
        screen.blit(text_white,(900,700))
        screen.blit(text_black,(900,100))
        if promote[0] == 'black':
            screen.blit(font.render('Promote to:', False, (0,0,0)),squareToCoord((10,6)))
            screen.blit(b_queen, squareToCoord((10,5)))
            screen.blit(b_rook, squareToCoord((11,5)))
            screen.blit(b_knight, squareToCoord((10,4)))
            screen.blit(b_bishop, squareToCoord((11,4)))
        if promote[0] == 'white':
            screen.blit(w_queen, squareToCoord((10,5)))
            screen.blit(w_rook, squareToCoord((11,5)))
            screen.blit(w_knight, squareToCoord((10,4)))
            screen.blit(w_bishop, squareToCoord((11,4)))
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                square = coordToSquare(pos)
                if (not 1<=square[0]<=8) or (not 1<=square[1]<=8):
                    if promote[0] == ' ':
                        pass
                    if promote[0] == 'black':
                        if square == (10,5):
                            board[promote[1][0]-1][promote[1][1]-1] = 'b_queen'
                        if square == (11,5):
                            board[promote[1][0]-1][promote[1][1]-1] = 'b_rook'
                        if square == (10,4):
                            board[promote[1][0]-1][promote[1][1]-1] = 'b_knight'
                        if square == (11,4):
                            board[promote[1][0]-1][promote[1][1]-1] = 'b_bishop'
                        promote = (' ', (' ',' '))
                        turn = 'white'
                    if promote[0] == 'white':
                        if square == (10,5):
                            board[promote[1][0]-1][promote[1][1]-1] = 'w_queen'
                        if square == (11,5):
                            board[promote[1][0]-1][promote[1][1]-1] = 'w_rook'
                        if square == (10,4):
                            board[promote[1][0]-1][promote[1][1]-1] = 'w_knight'
                        if square == (11,4):
                            board[promote[1][0]-1][promote[1][1]-1] = 'w_bishop'
                        promote = (' ', (' ',' '))
                        turn = 'black'
                elif color(board[square[0]-1][square[1]-1]) == turn and promote[0] == ' ':
                    pieceSelected = board[square[0]-1][square[1]-1]
                    squareSelected = square
                    boardCopy = board
                    lm = legalMoves(pieceType(pieceSelected), turn, squareSelected, boardCopy, False)
                elif pieceSelected != ' ' and lm.count(square) != 0 and promote[0] == ' ':
                    if turn == 'white':
                            if (square[0],square[1]) == (squareSelected[0]+1,squareSelected[1]+1) and board[square[0]-1][square[1]-1] == ' ':
                                board[square[0]-1][square[1]-2] = ' '
                            if (square[0],square[1]) == (squareSelected[0]-1,squareSelected[1]+1) and board[square[0]-1][square[1]-1] == ' ':
                                board[square[0]-1][square[1]-2] = ' '
                    if turn == 'black':
                            if (square[0],square[1]) == (squareSelected[0]-1,squareSelected[1]-1) and board[square[0]-1][square[1]-1] == ' ':
                                board[square[0]-1][square[1]] = ' '
                            if (square[0],square[1]) == (squareSelected[0]+1,squareSelected[1]-1) and board[square[0]-1][square[1]-1] == ' ':
                                board[square[0]-1][square[1]] = ' '
                    board[square[0]-1][square[1]-1] = pieceSelected
                    board[squareSelected[0]-1][squareSelected[1]-1] = ' '
                    if pieceType(pieceSelected) == 'pawn':
                        if square[1] == squareSelected[1] + 2 or square[1] == squareSelected[1] - 2:
                            ep.append((turn,square[0])) 
                        if square[1] == 1 and turn == 'black':
                            promote = ('black',square)
                            board[square[0]-1][square[1]-1] = ' '
                        if square[1]==8 and turn =='white':
                            promote = ('white',square)
                            board[square[0]-1][square[1]-1] = ' '
                    if pieceSelected == 'w_rook':
                        if squareSelected == (1,1):
                            w_rook_l = True
                        elif squareSelected == (8,1):
                            w_rook_r = True
                    if pieceSelected == 'b_rook':
                        if squareSelected == (1,8):
                            b_rook_l = True
                        elif squareSelected == (8,8):
                            b_rook_r = True
                    if pieceSelected == 'w_king':
                        w_king_moved = True
                        
                        if square == (3,1):
                            board[0][0] = ' '
                            board[3][0] = 'w_rook'
                        if square == (7,1):
                            board[7][0] = ' '
                            board[5][0] = 'w_rook'
                            
                    if pieceSelected == 'b_king':
                        b_king_moved = True
                        
                        if square == (3,8):
                            board[0][7] = ' '
                            board[3][7] = 'b_rook'
                        if square == (7,8):
                            board[7][7] = ' '
                            board[5][7] = 'b_rook'
                            
                    pieceSelected = ' '
                    squareSelected = (' ',' ')
                    if promote[0] == ' ':
                        turn = opposite(turn)
                        i = 0
                        while(i<len(ep)):
                            if ep[i][0] == turn:
                                ep.pop(i)
                                i -= 1
                            i += 1
                    if turn == 'black':
                        white_time = white_time-(pygame.time.get_ticks()-start_ticks)/1000
                    if turn == 'white':
                        black_time = black_time-(pygame.time.get_ticks()-start_ticks)/1000
                    start_ticks=pygame.time.get_ticks()
                    if insufficient('white') and insufficient('black'):
                        print('drew by insufficient material')
                    noLegalMoves = True
                    for i in range(len(board)):
                        for j in range(len(board[i])):
                            if color(board[i][j]) == turn:
                                lm = legalMoves(pieceType(board[i][j]),turn,(i+1,j+1),board,False)
                                if len(lm) > 0:
                                    noLegalMoves = False
                            if not noLegalMoves:
                                break
                        if not noLegalMoves:
                            break
                    if noLegalMoves:
                        if check(board,opposite(turn),False):
                            print(opposite(turn)+' won by checkmate')
                        else:
                            print('drew by stalemate')
                elif promote[0] == ' ':
                    pieceSelected = ' '
                    squareSelected = (' ',' ')
        if pieceSelected != ' ' and square[0] > 0 and square[0] < 9 and square[1] > 0 and square[1] < 9:
            highlight(squareToCoord(square))
        pygame.display.update()
        clock.tick(100)

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Times New Roman', 30)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1100,800))
board_img = pygame.image.load('board.png')
board_img = pygame.transform.scale(board_img, (800,800))


board = []
turn = 'white'
white_time = 600
black_time = 600
w_rook_l = False
w_rook_r = False
b_rook_l = False
b_rook_r = False
w_king_moved = False
b_king_moved = False


start_ticks=pygame.time.get_ticks()
board = setup_board(board)
pieceSelected = ' '
squareSelected = (' ',' ')
promote = (' ',squareSelected)
ep = []
start()

