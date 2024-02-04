# randome move from valid moves
import random

# piece rankings and numbers
pieceScores = {"K":0, "Q":10, "R":5, "B":3, "N":3, "p":1}
# what i do here is create a score based on the position of peiece 1-4 the higher the better position so this will help our ai better position its picec
# these are not my ranking but are pretty good
knightScores = [[1, 1, 1, 1, 1, 1, 1, 1], 
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4], 
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

queenScores =  [[1, 1, 1, 3, 1, 1, 1, 1], 
                [1, 2, 3, 3, 3, 1, 1, 1],
                [1, 4, 3, 3, 3, 4, 2, 1],
                [1, 2, 3, 3, 3, 2, 2, 1],
                [1, 2, 3, 3, 3, 2, 2, 1],
                [1, 4, 3, 3, 3, 4, 2, 1],
                [1, 1, 2, 3, 3, 1, 1, 1],
                [1, 1, 1, 3, 1, 1, 1, 1]]

rookScores =   [[4, 3, 4, 4, 4, 4, 3, 4], 
                [4, 4, 4, 4, 4, 4, 4, 4],
                [1, 1, 2, 3, 3, 2, 1, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 1, 2, 2, 2, 2, 1, 1],
                [4, 4, 4, 4, 4, 4, 4, 4],
                [4, 3, 4, 4, 4, 4, 3, 4]]

# pawns are diffrent based on color as there trying to get to diffrent location each oppisitie of one another
whitePawnScores =  [[8, 8, 8, 8, 8, 8, 8, 8], 
                    [8, 8, 8, 8, 8, 8, 8, 8],
                    [5, 6, 6, 7, 7, 6, 6, 5],
                    [2, 3, 3, 5, 5, 3, 3, 2],
                    [1, 2, 3, 4, 4, 3, 2, 1],
                    [1, 1, 2, 3, 3, 2, 1, 1],
                    [1, 1, 1, 0, 0, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores =  [[0, 0, 0, 0, 0, 0, 0, 0], 
                    [1, 1, 1, 0, 0, 1, 1, 1],
                    [1, 1, 2, 3, 3, 2, 1, 1],
                    [1, 2, 3, 4, 4, 3, 2, 1],
                    [2, 3, 3, 5, 5, 3, 3, 2],
                    [5, 6, 6, 7, 7, 6, 6, 5],
                    [8, 8, 8, 8, 8, 8, 8, 8],
                    [8, 8, 8, 8, 8, 8, 8, 8]]


piecePositionScores = {"N": knightScores, "Q": queenScores, "B": bishopScores, "R": rookScores, 
                       "bp": blackPawnScores, "wp": whitePawnScores}

CHECKMATE = 1000 # 1000 pts blk checkmate = -1000 wh = +1000
STALEMATE = 0 # better than losing (+ val = white winning, - val = black winning)
# can change to make better depth means how many moves to look ahead the higher the better but slower 
DEPTH = 2 # keep 1-3

def findRandomMove(validMoves):
    return validMoves[random.randint(0 ,len(validMoves)-1)]

# findbest move helps with find best move min max but is not called in the game
def findBestMoveMinMaxNoRecurtion(gs, validMoves): # greedy algrorithim/ minmax 
    # turn mulriplyer checks blacks turn of white turn to see if too maximise or minimize score
    turnMulriplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves) # adds verity to moves and picks a more randome move 
    for playerMove in validMoves: # goes through all off oppenent moves and picks the best move based on the players move 
        gs.makeMove(playerMove) # make a move
        opponentsMoves = gs.getValidMoves()
        if gs.staleMate:
            opponentMaxScore = STALEMATE
        elif gs.checkMate:
            opponentMaxScore = -CHECKMATE
        else: # if opp in check or stalemate no point in checking board for moves hence the for loop is indented in this
            opponentMaxScore = -CHECKMATE
            for opponentsMove in opponentsMoves: # try finding best move for opponent
                gs.makeMove(opponentsMove)
                gs.getValidMoves()
                if gs.checkMate:
                    score = CHECKMATE 
                elif gs.staleMate:
                    score = STALEMATE
                else:
                    score = -turnMulriplier * scoreMaterial(gs.board) # makes is so both black and white are trying to get a a high score from the algorithims perspective
                if score > opponentMaxScore:
                    opponentMaxScore = score
                gs.undoMove()
        if opponentMaxScore < opponentMinMaxScore: # minimum score part
            opponentMinMaxScore = opponentMaxScore
            bestPlayerMove = playerMove
        gs.undoMove() # debug 
    return bestPlayerMove
        
def findBestMove(gs, validMoves, returnQueue): #helper method to help us first call the recursiver funtion
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    # for testting other inferior algorithims 
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove) # prevoius code but if you want to go back to min max use this
    # findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    counter = 0
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    print(counter) # print how many times method is called ex how many states pos is runnign in
    returnQueue.put(nextMove)

def findMoveMinMax(gs, validMoves, depth, whiteToMove): # min max recurtion
    global nextMove 
    if depth == 0: #terminal node must return a move based on current board now
        return scoreMaterial(gs.board)
    
    if whiteToMove:
        maxScore = -CHECKMATE # worst score possible
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)# calling function recursively # depth -1 moves through layers
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:# at max depth im at first call of method that is the first move so i want best move i can curranly make, if i find a better move i change my move
                    nextMove = move 
            gs.undoMove()
        return maxScore # recurtion goes back up 

    else: # blk to move
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)  
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore

def findMoveNegaMax(gs, validMoves, depth, turnMulriplier): # nega max algorithim for move effecincy and effectiveness
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMulriplier * scoreBoard(gs) # wont need to check whos turn turn multiplyer will do that 
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMulriplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore

# given any board state if lets say we have a move that is the best move the AI can do, in that case why check all the other possible moves when we have the best one so this is where alpha beta pruning comes in and will speed up the AI chess bot
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMulriplier): # nega max algorithim with alpha beta pruning
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMulriplier * scoreBoard(gs) # wont need to check whos turn turn multiplyer will do that 
    
    # move ordering to make aplha beta pruning more effitient so we wont look at branches that our worse

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMulriplier) # for opponent alpha beta reversed as score is opposite for opp
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score)
        gs.undoMove()
        if maxScore > alpha: # pruning
            alpha = maxScore
        if alpha >= beta: #best case
            break
    return maxScore

def scoreBoard(gs): # a positive score from this is good for white and neg is good for black
    if gs.checkMate:
        if gs.whiteToMove:
            return - CHECKMATE # blk wins
        else:
            return CHECKMATE # wht wins    
    elif gs.staleMate:
        return STALEMATE

    score = 0 # if check or stale no point in scoring
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                # score based on position
                piecePositionScore = 0
                if square[1] != "K": # no king position
                    if square[1] == "p": # for pawn
                        piecePositionScore = piecePositionScores[square][row][col]
                    else: # for other picec
                        piecePositionScore = piecePositionScores[square[1]][row][col]

                if square[0] == 'w': # add score +
                    score += pieceScores[square[1]] + piecePositionScore * 0.1 # weight of position in 0.1 or 1/10 of a pawn# at sq 1 could be any piece there
                elif square[0] == 'b': # subtract score -
                    score -= pieceScores[square[1]]  + piecePositionScore * 0.1
    return score


"""Score the board based on picec"""
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w': # add score +
                score += pieceScores[square[1]] # at sq 1 could be any piece there
            elif square[0] == 'b': # subtract score -
                score -= pieceScores[square[1]]
    
    return score
