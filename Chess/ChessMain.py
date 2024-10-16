# driver file (user input and game state) and determining the valid move

import pygame as p
import ChessEngine
import SmartMoveFinder
from multiprocessing import Process, Queue

BOARD_WIDTH = BOARD_HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250
MOVE_LOGPANEL_HEIGHT = BOARD_HEIGHT
DIMENTION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENTION
MAX_FPS = 15
IMAGES = {}

def showStartButton(screen):
    font = p.font.SysFont("Arial", 46, True, False)
    text = font.render("Start", True, p.Color("white"))
    width, height = text.get_width(), text.get_height()
    button_rect = p.Rect(280,415, 200,50)
    p.draw.rect(screen, p.Color("green"), button_rect)
    screen.blit(text, (335,412))
    return button_rect

# Start screen
def showStartScreen(screen, playerOne, playerTwo): 
    
    screen.fill(p.Color("green"))
    font_options = p.font.SysFont("Arial", 24, True, False)

    font_title = p.font.SysFont("Arial", 80, True, False)
    text_title = font_title.render("CHESS", True, p.Color("white"))
    screen.blit(text_title, ((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH - text_title.get_width()) // 2.5, 50))

    illustration = p.image.load('Chess/images/wp.png')
    illustration = p.transform.scale(illustration, (85, 85))
    screen.blit(illustration, (BOARD_WIDTH / 2 - illustration.get_width() / 5 + 200, BOARD_HEIGHT / 8 - 10))

    font_options = p.font.SysFont("Arial", 24, True, False)

    text_p1 = font_options.render("Player 1:", True, p.Color("white"))
    screen.blit(text_p1, (130, 205))

    human_button_rect_p1 = p.Rect(230, 200, 100, 40)
    p.draw.rect(screen, p.Color("white") if playerOne else p.Color("black"), human_button_rect_p1)
    text_human_p1 = font_options.render("Human", True, p.Color("red"))
    screen.blit(text_human_p1, (245, 205)) 

    ai_button_rect_p1 = p.Rect(350, 200, 100, 40)
    p.draw.rect(screen, p.Color("white") if not playerOne else p.Color("black"), ai_button_rect_p1)
    text_ai_p1 = font_options.render("AI", True, p.Color("red"))
    screen.blit(text_ai_p1, (390, 205))

    text_p2 = font_options.render("Player 2:", True, p.Color("black"))
    screen.blit(text_p2, (130, 275))

    human_button_rect_p2 = p.Rect(230, 270, 100, 40)
    p.draw.rect(screen, p.Color("white") if playerTwo else p.Color("black"), human_button_rect_p2)
    text_human_p2 = font_options.render("Human", True, p.Color("red"))
    screen.blit(text_human_p2, (245, 277))

    ai_button_rect_p2 = p.Rect(350, 270, 100, 40)
    p.draw.rect(screen, p.Color("white") if not playerTwo else p.Color("black"), ai_button_rect_p2)
    text_ai_p2 = font_options.render("AI", True, p.Color("red"))
    screen.blit(text_ai_p2, (390, 277))


    return human_button_rect_p1, ai_button_rect_p1, human_button_rect_p2, ai_button_rect_p2
''' or board and pecies
'''
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("Chess/images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

# main driver for input and graphics 
def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white")) 
    moveLogFont = p.font.SysFont("Arial", 14, False, False)
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False # flag var for move made to save memory
    animate = False # flag var fro when we animate as we dont want to animate the undo
    loadImages() # only done once to save memory
    running = True
    sqSelected = () #innitally empty, keeps track of users last click as (r, c)
    playerClicks = [] # keeps track of player clicks as (r, c)
    gameOver = False # once over player can click they can still undo last move
    """changing player to false changes it to a AI if you want to do AI vs AI or test code"""
    playerOne = True # if human is white then true if AI is white its false
    playerTwo = True #same as before but black
    AIThinking = False
    moveFinderProcess = None
    moveUndone = False

    # UI 
    playerOne = True
    playerTwo = True

    human_button_rect_p1, ai_button_rect_p1, human_button_rect_p2, ai_button_rect_p2 = showStartScreen(screen, playerOne, playerTwo)
    start_button_rect = None
    selecting_players = True
    while selecting_players:
        for e in p.event.get():
            if e.type == p.QUIT:
                selecting_players = False
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if human_button_rect_p1.collidepoint(e.pos):
                    playerOne = True
                    ai_button_rect_p1 = showStartScreen(screen, playerOne, playerTwo)[1]
                elif ai_button_rect_p1.collidepoint(e.pos):
                    playerOne = False
                    ai_button_rect_p1 = showStartScreen(screen, playerOne, playerTwo)[1]
                elif human_button_rect_p2.collidepoint(e.pos):
                    playerTwo = True
                    ai_button_rect_p2 = showStartScreen(screen, playerOne, playerTwo)[3]
                elif ai_button_rect_p2.collidepoint(e.pos):
                    playerTwo = False
                    ai_button_rect_p2 = showStartScreen(screen, playerOne, playerTwo)[3]
                elif start_button_rect and start_button_rect.collidepoint(e.pos):
                    selecting_players = False

        start_button_rect = showStartButton(screen)

        p.display.flip()
        clock.tick(MAX_FPS)

    # Now that players are selected, proceed with the game
    if selecting_players:
        return

    # UI END GAME START!


    while running: # qeue is in order
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)# if white to move and player one is true its humans turn if not then player two
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handling/ clicks
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver: # can only mave moves is game not over. 
                    location = p.mouse.get_pos() #x,y location of mouse
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE 
                    if sqSelected == (row, col) or col>= 8:# if user clicks twice or clicks mouse log
                        sqSelected = () # reset click
                        playerClicks = [] # clears players click
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2 and humanTurn: # after second click which will move the piece while the first click selected the piece human turn so that human cannot play when ai is playing
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNoatation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = () # reset user clicks to not append leg of clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            
            #key input
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when u is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True
                if e.key == p.K_r: #r for reset board
                    # all changes to reset board and presvoius game
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking = False
                    moveUndone = True
        # AI move finder not in mouse clicks as we want ai to move on own
        if not gameOver and not humanTurn and not moveUndone:
            if not AIThinking: # AI turn and not thinking make turn
                AIThinking =True
                print("Thinking...")
                returnQueue = Queue() # to pass data between threds
                moveFinderProcess = Process(target=SmartMoveFinder.findBestMove, args=(gs, validMoves, returnQueue))
                moveFinderProcess.start() # calls find best move(..)
           
            if not moveFinderProcess.is_alive():
                print("Done Thinking")
                AIMove = returnQueue.get()
                if AIMove is None: # max sxore is checkmate so at checkmate it basicaly gives up so makes a random move as it exepts defete and cant find a way out
                    AIMove = SmartMoveFinder.findRandomMove(validMoves) # very rare
                gs.makeMove(AIMove)
                moveMade = True
                animate = True
                AIThinking =False

        

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock) # animate last move made
            validMoves = gs.getValidMoves()
            moveMade = False   
            animate = False    
            moveUndone = False
                    
        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

        if gs.checkMate: # if checkmate of stale mate end game
            gameOver = True
            if gs.whiteToMove:
                drawEndGameText(screen, "BLACK WINS BY CHECKMATE!")
            else:
                drawEndGameText(screen, "WHITE WINS BY CHECKMATE!")
        elif gs.staleMate:
            gameOver = True
            drawEndGameText(screen,"STALEMATE!")
        
        clock.tick(MAX_FPS)
        p.display.flip()
        


"""
draws everything in current game state
"""
def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)

def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            

"""highlight sq selected and moves possible"""
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): # sq selected is a valid piece
            s = p.Surface((SQ_SIZE, SQ_SIZE)) # surface
            s.set_alpha(100) # trasparency 
            s.fill(p.Color('blue'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # highlight moves possible 
            s. fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            piece = board[r][c]
            if piece != "--": 
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

""" draws the move log"""
def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOGPANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect )
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0 , len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i]) + " "
        if i + 1 < len(moveLog): #to check if black made a move
            moveString += str(moveLog[i+1]) + "  "
        moveTexts.append(moveString)
                                        
    movesPerRow = 3
    padding = 5
    lineSpacing = 2
    textY = padding + 40
    # movelog titel
    font_titleml = p.font.SysFont("Arial", 20, True, False)
    text_titleml = font_titleml.render("MOVE LOG", True, p.Color("white"))
    screen.blit(text_titleml, (580, 10))
    # move log 
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i+j]
        textObject = font.render(text, True, p.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing 

"""animating the pieces"""

def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSqare = 10 # frames to move one piece 
    frameCount = (abs(dR) + abs(dC)) * framesPerSqare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # erase piece from ending sq
        color = colors[(move.endRow + move.endCol) % 2] # colur or end sq
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # draw captured piece at rect
        if move.pieceCaptured != "--":
            if move.isEnpassantMove: 
                enpassantRow = move.endRow + 1 if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol*SQ_SIZE, enpassantRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)
    
# draw text on screen
def drawEndGameText(screen, text):
    font = p.font.SysFont("Arial", 32, True, False)
    textObject = font.render(text, 0 , p.Color("Red"))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2, BOARD_HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0 , p.Color("Black"))
    screen.blit(textObject, textLocation.move(2,2))

# runner
if __name__ == "__main__":
    main()
    