import pygame as pg, sys
from pygame.locals import  * 
import time
import math 
from collections import defaultdict

#initialize global variables
XO = 'x'
SIZE = 3
WINNER = None
DRAW = False
WIDTH = 400
HEIGHT = 400
BLACK = ( 0,  0,  0 ) 
WHITE = ( 255, 255, 255 ) 
RED = ( 250, 70, 70 )
CHOICE = 0
TABLE = {0 : "Welcome", 1 : "miniMax" , 2 : "alphaBetaPruning" }


#TicTacToe 3x3 board
TTT = [[None] * 3, [None] * 3, [None] * 3]

#initializing pygame window
pg.init() 
FPS = 30
CLOCK = pg.time.Clock() 
screen = pg.display.set_mode(( WIDTH,  HEIGHT + 100 ) , 0, 32 ) 
pg.display.set_caption( "Tic Tac Toe" ) 

#loading the images

X_IMG = pg.image.load( "X_image.png" ) 
O_IMG = pg.image.load( "O_image.png" ) 

#resizing images
X_IMG = pg.transform.scale( X_IMG,  ( 80, 80 )) 
O_IMG = pg.transform.scale( O_IMG,  ( 80, 80 )) 


def gameOpening() :
    # screen.blit( opening, ( 0, 0 )) 
    pg.display.update() 
    time.sleep( 1 ) 
    screen.fill( BLACK ) 
    
    for i in range( 1, SIZE ) :
        # Drawing vertical lines
        pg.draw.line( screen, WHITE, (int(( WIDTH / SIZE )  * i), 0 ) , (int(( WIDTH / SIZE )  * i),  HEIGHT ) , 5 ) 
        # Drawing horizontal lines
        pg.draw.line( screen, WHITE, ( 0, int(( HEIGHT / SIZE )  * i) ) , ( WIDTH,  int(( HEIGHT / SIZE )  * i )) , 5 ) 
    drawStatus() 
    

def drawStatus() :
    global DRAW, TABLE, CHOICE

    if WINNER is None:
        message = TABLE[CHOICE] + " : " + XO.upper()   +  "'s Turn"
    else:
        message = TABLE[CHOICE] + " : " + WINNER.upper()   +  " won!"
    if DRAW:
        message = 'Game Draw!'

    font = pg.font.SysFont( 'consolas',  30 ) 
    text = font.render( message,  1,  ( 0,  0,  0 )) 

    # copy the rendered message onto the board
    screen.fill (( 255,  255,  255 ) ,  ( 0,  400,  500,  100 )) 
    text_rect = text.get_rect( center=( int(WIDTH / 2) ,  500 - 50 )) 
    screen.blit( text,  text_rect ) 
    pg.display.update() 

def checkWinner( drawLine ) :
    global TTT, WINNER, DRAW, SIZE

    myDict  = { 'x' : -1, 'o' : 1 }
    winTable = { -SIZE : 'x', SIZE : 'o' }

    rowWin = 0
    colWin = 0
    diagonalWin = 0

    for row in range( SIZE ):
        rowWin=0
        for j in range( SIZE ):
            if TTT[row][j] is not None:
                rowWin += myDict[TTT[row][j]]
            else:
                break
        if rowWin == SIZE or rowWin == -SIZE:
            if(drawLine == True):
                pg.draw.line( screen,  ( 250, 0, 0 ) ,  ( 0,  ( row  +  1 )  * HEIGHT / 3  - HEIGHT / 6 ) , \
                              ( WIDTH,  ( row  +  1 )  * HEIGHT / 3  -  HEIGHT / 6  ) ,  4 )
                WINNER = winTable[rowWin]
                drawStatus()
            return winTable[rowWin]

    for col in range( SIZE ):
        colWin = 0
        for j in range( SIZE ):
            if TTT[j][col] is not None:
                colWin += myDict[TTT[j][col]]
            else:
                break
        if colWin == SIZE or colWin == -SIZE:
            if(drawLine == True):
                pg.draw.line ( screen,  ( 250, 0, 0 ) , (( col  +  1 )  *  WIDTH / 3  -  WIDTH / 6,  0 ) , \
                          (( col  +  1 )  *  WIDTH / 3  -  WIDTH / 6,  HEIGHT ) ,  4 )
                WINNER = winTable[colWin]
                drawStatus()
            return winTable[colWin]
    

    
    for i in range( SIZE ): 
        if TTT[i][i] is not None:
            diagonalWin += myDict[TTT[i][i]]
    
    if diagonalWin == SIZE or diagonalWin == -SIZE:
        if( drawLine == True ):
            WINNER = winTable[diagonalWin]
            pg.draw.line ( screen,  RED ,  ( 50,  50 ) ,  ( 350,  350 ) ,  4 ) 
            drawStatus()
        return winTable[diagonalWin]


    diagonalWin = 0
    
    for i in range( SIZE ): 
        if TTT[-i-1][i] is not None:
            diagonalWin += myDict[TTT[-i-1][i]]

    if diagonalWin == SIZE or diagonalWin == -SIZE:
        if(drawLine == True):
            WINNER = winTable[diagonalWin]
            pg.draw.line ( screen,  RED ,  ( 50,  50 ) ,  ( 50,  350 ) ,  4 ) 
            drawStatus()
        return winTable[diagonalWin]
    

    if( drawLine and all( [all( row )  for row in TTT] )  and WINNER is None ) :
        DRAW = True 

    if( drawLine ):
        drawStatus()
    return None
        

def bestMove() :
    global TTT, XO, DRAW
    bestScore = -math.inf
    move = [-2, -2]
    
    for i in range( SIZE ) :
        for j in range( SIZE ) :
            
            if( TTT[i][j] is None ) :
                TTT[i][j] =  'o'
                score = miniMax( 1, True,  -math.inf, math.inf ) 
                TTT[i][j] =   None
                if( score  >  bestScore ) :
                    bestScore = score
                    move = [i, j]
    XO = 'o'

    drawXO( move[0] + 1, move[1] + 1 ) 
    
    checkWinner( True ) 

    

def miniMax( depth, isMaximizing, alpha, beta ) :
    global TTT, CHOICE

    t = checkWinner( False ) 
    
    if ( t == 'x' ) :
        return -1
    elif ( t == 'o' ) :
        return 1
    elif ( t == 'd' ) :
        return 0
    

    if( isMaximizing ) :
        bestScore =  - math.inf
        for i in range( SIZE ) :
            for j in range( SIZE ) :
                if( TTT[i][j] is None ) :
                    TTT[i][j] =  'x'
                    score = miniMax( depth + 1, False, alpha, beta ) 
                    TTT[i][j] =  None
                    bestScore = max( score, bestScore ) 
                    if( TABLE[CHOICE] == "alphaBetaPruning" ) :
                        alpha = max( alpha, bestScore ) 
                        if beta  <=  alpha:
                            break
        return bestScore

    else:
        bestScore = math.inf 
        for i in range( SIZE ) :
            for j in range( SIZE ) :
                if( TTT[i][j] is None ) :

                    TTT[i][j] =  'o'
                    score = miniMax( depth + 1, True, alpha, beta ) 
                    TTT[i][j] =  None

                    bestScore = min( score, bestScore ) 
                    if( TABLE[CHOICE] == "alphaBetaPruning" ) :
                        beta = min( beta, bestScore ) 
                        if beta  <=  alpha:
                            break
        return bestScore



def heuristicAlphaBetaPruning( depth, isMaximizing, alpha, beta ) :

    global TTT
    # print( depth ) 
    t = checkWinner( False ) 
    if ( t == 'x' ) :
        return 1
    elif ( t == 'o' ) :
        return  - 1
    elif ( t == 'd' ) :
        return 0
    

    if( isMaximizing ) :
        bestScore =  - math.inf
        for i in range( 3 ) :
            for j in range( 3 ) :
                if( TTT[i][j] is None ) :
                    TTT[i][j] =  'x'
                    score = heuristicAlphaBetaPruning( depth - 1, False, alpha, beta ) 
                    # print( score ) 
                    TTT[i][j] =  None
                    bestScore = max( score, bestScore ) 
                    alpha = max( alpha, bestScore ) 
                    if beta  <=  alpha:
                        break
        return bestScore
    else:
        bestScore = math.inf 
        for i in range( 3 ) :
            for j in range( 3 ) :
                if( TTT[i][j] is None ) :
                    TTT[i][j] =  'o'
                    score = heuristicAlphaBetaPruning( depth - 1, True, alpha, beta ) 
                    TTT[i][j] =  None
                    bestScore = min( score, bestScore ) 
                    beta = min( beta, bestScore ) 
                    if beta  <=  alpha:
                        break
        return bestScore


def drawXO( row, col ) :
    # print( XO ) 
    posx = ( WIDTH / SIZE )  * ( row - 1 )  + 30
    posy = ( HEIGHT / SIZE )  * ( col - 1 )  + 30
    
    TTT[row - 1][col - 1] = XO
    if( XO == 'x' ) :
        screen.blit( X_IMG,( int(posy), int(posx) )) 
        # XO= 'o'
    else:
        screen.blit( O_IMG,( int(posy), int(posx) )) 
        # XO= 'x'
    pg.display.update() 
    
    

def userClick() :
    #get coordinates of mouse click
    x,y = pg.mouse.get_pos() 

    #get row, column of mouse click ( 1 - 3 ) 
    row = None
    col = None
    for i in range( 1,SIZE + 1 ) :
        if( x < ( WIDTH / SIZE )  * i ) :
            col = i
            break

        
    #get row of mouse click ( 1 - 3 ) 
    for i in range( 1,SIZE + 1 ) :
        if( y  <  ( HEIGHT / SIZE )  * i ) :
            row = i
            break
    
    if( row and col and TTT[row - 1][col - 1] is None ) :
        global XO
        XO = 'x'
        drawXO( row,col ) 
        checkWinner( True ) 

        

def resetGame() :
    global TTT,  WINNER, XO,  DRAW, CHOICE
    time.sleep( 2 ) 
    XO = 'x'
    CHOICE = 0
    DRAW = False
    gameOpening() 
    WINNER = None
    TTT = [[None] * 3, [None] * 3, [None] * 3]



def startGame() :

    resetGame() 

    # taking input
    print( "Please the CHOICE : " ) 
    print( "1.miniMax\n2.miniMax with alpha - beta pruning" ) 
    CHOICE = int( input()) 

    while( True ) :
        for event in pg.event.get() :
            if event.type  ==  QUIT:
                pg.quit() 
                sys.exit() 
            elif event.type is MOUSEBUTTONDOWN:
                # the user clicked; place an X or O
                XO = 'x'
                userClick() 
                
                if( WINNER or DRAW ) :
                    print("Reached1")
                    startGame() 
                # print(WINNER, DRAW)
                bestMove() 
                if( WINNER or DRAW ) :
                    # print(WINNER, DRAW)
                    startGame() 
                
        pg.display.update() 
        CLOCK.tick( FPS ) 
            

# Starting the game 
gameOpening() 
startGame() 
