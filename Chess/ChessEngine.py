# storing information about current state

class GameState():
    def __init__(self):
        # 8 x 8 board piece[0] = white [1] = black
        self.board = [ 
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"], 
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}               
                   
        self.whiteToMove = True # whites turn 
        self.moveLog = []
        self.whiteKingLocation = (7, 4) # for check
        self.blackKingLocation = (0, 4)
        self.checkMate = False # no valid moves king in check
        self.staleMate = False # no valid moves king not in check
        self.enpassantPossible = () # cord for sqr where enpessant is possible
        self.enpassantPossibleLog = [self.enpassantPossible] 
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.CastlingRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                               self.currentCastlingRight.wqs, self.currentCastlingRight.bqs,)]


    # takes move as parameter and dose it not working with castling at pawn promotion and passant
    def makeMove(self, move): #this will make the move EX move to n col
        self.board[move.startRow][move.startCol] = "--" # after move leave original spot blank on board
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move) # log the move to undo or display it
        self.whiteToMove = not self.whiteToMove # swap players turns # white starts
        # update king location to see if piece moved is white king if so update ir
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        # pawn promotion check if move is a pawn promtoion will always make pawn a queen
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
        
        # do enpassant
        if move.isEnpassantMove: # when empessant its just like normal pawn capture exept the piece is not on that sqare but on the row you started 
            self.board[move.startRow][move.endCol] = "--" # capture pawn
        
        # update empessand possible to always see if its possible....
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2: # only on 2 sq pawn advance move the sq in between the rows is the one removed
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol) 
        else: # any other move made
            self.enpassantPossible = ()

        # do the castle move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: # move to right so king side castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1] # move rook
                self.board[move.endRow][move.endCol + 1] = "--" # remove old rook
            else: # queen side
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = "--"

        self.enpassantPossibleLog.append(self.enpassantPossible) #debug/ for log

        # update catsle 
        self.updateCastleRights(move)
        self.CastlingRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                                   self.currentCastlingRight.wqs, self.currentCastlingRight.bqs,))


    def undoMove(self): # undos the last move using our movelog
        if len(self.moveLog) != 0: # check if there is atleast one move done that we can undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # after undo switch turns
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

            # undo empessant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--" # leave sq blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured

            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]
            
            # undo castling rights
            self.CastlingRightsLog.pop() # delete new castle rights from the move undid
            newRights = self.CastlingRightsLog[-1] # now make the last move done the move done before the undo to revert to orignal state
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
            # undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: #king side
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol - 1] = "--"
                else: # queen side
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "--"

            # AI debug
            self.checkMate = False;
            self.staleMate = False;

 # update castle rights if rook or king moves
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK': # if king is moved cant castle in game
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK': # if black moves king he cant castle anymore
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR': # white rook
            if move.startRow == 7:
                if move.startCol == 0: #left rook
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == 'bR': # black rook
            if move.startRow == 0:
                if move.startCol == 0: #left rook
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7: #right rook
                    self.currentCastlingRight.bks = False

        # for rook debug
        if move.pieceMoved == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False


    """ valid moves using two methods 1) all moves considring checks and 2) all moves not considering checks"""

    def getValidMoves(self): #considring checks Ex moving your pawn and letting king die is invalid 
        tempEmpessantPossible = self.enpassantPossible  # save values for when needed
        tempCastleRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, 
                                        self.currentCastlingRight.wqs, self.currentCastlingRight.bqs,) # copy current CR 
        # generate valid moves, then make the move, generate opp moves, then see for each opp moves if they attack king if they attack king move is invalid
        moves = self.getAllPossibleMoves()
        if self.whiteKingLocation: # kings castling moves
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves) # kings castling moves
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        # for each move make the move
        for i in range(len(moves)-1, -1, -1): #when removing from list go backwards
            self.makeMove(moves[i]) #first swap turn
            # swap turn again
            self.whiteToMove = not self.whiteToMove # switch the turn so we check if the person who just made the move is in check which is opposite of the person who made the move 
            if self.inCheck():
                moves.remove(moves[i]) # remove any moves that put you into a check
            self.whiteToMove = not self.whiteToMove # undo the player switch turn 
            self.undoMove() # back to players turn

        if len(moves) == 0: #checkmate or stale mate no valid moves
            if self.inCheck():
                self.checkMate = True # checkmate
            else:
                self.staleMate = True # stalemate
        else:
            self.checkMate = False 
            self.staleMate = False 

        self.enpassantPossible = tempEmpessantPossible 
        self.currentCastlingRight = tempCastleRights
        return moves

    def inCheck(self): # see if current player is in check
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove # switch turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove # switch turns back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #sq under attack
                return True
        return False

    def getAllPossibleMoves(self): # not consdering checks
        moves = [] # list of moves
        for r in range(len(self.board)): # num of rows
            for c in range(len(self.board[r])): # num of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove): # if its whites turn
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) # callc the correct move function based on peice

        return moves
    
    """all moves for all the picec"""

    def getPawnMoves(self, r, c, moves): # pawns only move forward and can move one step or two steps if its first move and can capture only diagonaly 
        if self.whiteToMove: # white pawn move
            if self.board[r-1][c] == "--": #check if sq infront of you is clear
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--": # 2 sq move only at start
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0: # capturing diagonally to left
                if self.board[r-1][c-1][0] == 'b': # check if there is a peice there to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible: # making enpessant move legal and having it execute on screen
                    moves.append(Move((r, c), (r-1, c-1), self.board, isEnpassantMove=True))
            if c+1 <= 7: # capturing to right
                if self.board[r-1][c+1][0] == 'b':
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, isEnpassantMove=True))
        
        else: # black pawn moves
            if self.board[r+1][c] == "--": # 1 sq move
                moves.append(Move((r, c), (r+1, c), self.board))
                if r==1 and self.board[r+2][c] == "--": # 2 sq move
                    moves.append(Move((r, c), (r+2, c), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c-1), self.board, isEnpassantMove=True))
            # capturing diagonally 
            if c - 1 >= 0: # left capture
                if self.board[r+1][c-1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c + 1 <= 7: #right capture
                if self.board[r+1][c+1][0] == 'w':
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c+1), self.board, isEnpassantMove=True))
                
    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8): #board is 8*8
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # rook on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": #empty space
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor: # target enemy piece
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else: #own piece invalid
                        break
                else: #off board
                    break


    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor: #empty or ememy can move
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = ((-1,-1), (-1, 1), (1,-1), (1,1)) 
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8): #can move max 7 sqs
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                        break
                    else:
                        break
                else:
                    break


    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1,-1), (-1,0), (-1,1), (0, -1), (0, 1), (1, -1), (1, 0), (1,1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r,c),(endRow,endCol),self.board))
        

    def getCastleMoves(self, r, c,  moves):
        if self.squareUnderAttack(r, c): #if king in check cant castle 
            return  
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)
    
    def getKingsideCastleMoves(self, r, c, moves):
        if c + 2 < 8 and self.board[r][c+1] == '--' and self.board[r][c+2] == '--': # see if square on king side are empty
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r,c), (r, c+2), self.board, isCastleMove=True))

    def getQueensideCastleMoves(self, r, c, moves):
         if c - 2 >= 0 and self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))


# casling 4 rules, space in row of king must be empty exept for rook,s king frist move of game and rooks first move if you want to caslte on its side, catle must not end is check.
# if castle on king side of board its king side castle ks and etc
class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():
    #mapping keys to values
    # key : value (format)
    # rank = rows, files = columns
    # the follwoing is rank file notation (chess notation)
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0 }
    rowstoRanks = {v: k for k, v in ranksToRows.items()} # reversing the dictionary ez method
    filestoCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colstoFiles = {v: k for k, v in filestoCols.items()} 

    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isCastleMove = False): #enpessant is a optional paramater where not every move should have a empessant possible only after a move is made where its possible do we pass this parameter in (it also has a default parameter of false)
        # all these only keep track of info no moves made yet
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        

        self.isPawnPromotion = False
        # pawn promotion
        if (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7): # 1) white pawn made it to black end row = 0 or black pawn made it to white end row = 7
            self.isPawnPromotion = True # pawn promotion for white
        # empessant
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'

        #castle moves
        self.isCastleMove = isCastleMove

        # capture move
        self.isCaptureMove = self.pieceCaptured != "--"

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
       


    """overiding a equals method"""
    def __eq__(self, other):
        # check if two objects are equal or not
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False



    def getChessNoatation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c): #helper method
        return self.colstoFiles[c] + self.rowstoRanks[r]
    
    def __str__(self): #overriding str function
        if self.isCastleMove: # for castle
            return "O-O" if self.endCol == 6 else "O-O-O"
        
        endSquare = self.getRankFile(self.endRow, self.endCol)
       # pawn moves
        if self.pieceMoved[1] == 'p':
            if self.isCaptureMove:
                return self.colstoFiles[self.startCol] + "x" + endSquare
            else:
                moveString = endSquare

            if self.isPawnPromotion:
                moveString += "=Q"  # Assuming promotion to queen, you can modify it based on your logic
            return moveString

        moveString = self.pieceMoved[1]
        if self.isCaptureMove:
            moveString += 'x'
        return moveString + endSquare