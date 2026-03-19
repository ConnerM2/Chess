

class GameState():
    def __init__(self):
        self.board = [
                ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]
        
        self.whiteToMove = True
        self.moveHistory = []
        self.whiteKingLocation = (7,4)
        self.blackKingLocation = (0,4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = ()

        self.gen_move = {
            'p' : self.gen_pawn_moves,
            'R' : self.gen_rook_moves,
            'N' : self.gen_knight_moves,
            'B' : self.gen_bishop_moves,
            'K' : self.gen_king_moves,
            'Q' : self.gen_queen_moves,
        }

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.peiceMoved
        self.moveHistory.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.peiceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.peiceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
        
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.peiceMoved[0] + 'Q'

        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'

        if move.peiceMoved[1] == 'p' and abs(move.endRow-move.startRow) == 2:
            self.enpassantPossible = ((move.endRow + move.startRow) // 2, move.endCol)
        else:
            self.enpassantPossible = ()
    
    def undoMove(self):
        if len(self.moveHistory) != 0:
            move = self.moveHistory.pop()
            self.board[move.startRow][move.startCol] = move.peiceMoved
            self.board[move.endRow][move.endCol] = move.peiceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.peiceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.peiceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.peiceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)
            if move.peiceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

    def all_legal_moves(self): #sorts through all moves and returns moves that dont put king in danger
        tempEnpassantPossible = self.enpassantPossible
        moves = self.all_moves()
        for i in range(len(moves) - 1, -1, -1): #When removing elements from a list, go backwards to avoid bugs
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0: 
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        
        self.enpassantPossible = tempEnpassantPossible
        return moves

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.all_moves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False


    def all_moves(self): #finds every single possible move
        moves = []#stores all the moves and returns at end
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == '--':
                    continue
                color = self.board[row][col][0]
                peice = self.board[row][col][1]
                #print(color, peice)

                if (color == 'w' and self.whiteToMove) or (color == 'b' and not self.whiteToMove):
                    possible_moves = self.gen_move[peice](row, col)
                    moves.extend(possible_moves)

        return moves  

    def gen_pawn_moves(self, row, col):
        moves = []
        peice_color = self.board[row][col][0]

        if peice_color == 'w':
            direction = -1
            enemy = 'b'
            start_row = 6

        else:
            direction = 1
            enemy = 'w'
            start_row = 1

        #capture
        for capture in (-1, 1):
            r = row + direction
            c = col + capture
            if 0 <= r < 8 and 0 <= c < 8:
                if self.board[r][c][0] == enemy:
                    moves.append(Move((row, col), (r, c), self.board))
                elif (r, c) == self.enpassantPossible:
                    moves.append(Move((row, col), (r, c), self.board, isEnpassantMove=True))
                #check if diagnal square are en pasan

        #move forward
        oneforward = row + direction
        if 0 <= oneforward < 8 and self.board[oneforward][col] == '--':
            moves.append(Move((row, col), (oneforward, col), self.board))

            #move 2 forward if on starting row
            twoforward = row + direction * 2
            if 0 <= twoforward < 8 and row == start_row and self.board[twoforward][col] == '--':
                moves.append(Move((row, col), (twoforward, col), self.board))
                #declare that the square before is en pasan elegable

        return moves

    
    def gen_rook_moves(self, row, col):
        moves = []
        peice_color = self.board[row][col][0]

        if peice_color == 'w':
            enemy = 'b'
        else:
            enemy = 'w'

        for direction in (-1, 1):
            currentRow = row
            currentCol = col
            while 0 <= currentRow + 1 * direction < 8:
                currentRow += 1 * direction
                if self.board[currentRow][currentCol] == '--':
                    moves.append(Move((row,col), (currentRow, currentCol), self.board))
                elif self.board[currentRow][currentCol][0] == enemy:
                    moves.append(Move((row,col), (currentRow, currentCol), self.board))
                    break
                else:
                    break
            #think of it like a pawn move and loop until you are either ontop of a enemy or freindly
            #while in bounds, if move == -- append it, if move == enenmy append then break, if move == freindly break
        for direction in (-1, 1):
            currentRow = row
            currentCol = col
            while 0 <= currentCol + 1 * direction < 8:
                currentCol += 1 * direction
                if self.board[currentRow][currentCol] == '--':
                    moves.append(Move((row,col), (currentRow, currentCol), self.board))
                elif self.board[currentRow][currentCol][0] == enemy:
                    moves.append(Move((row,col), (currentRow, currentCol), self.board))
                    break
                else:
                    break #This break is for if the peice is block by thier own color peices
        return moves
    
    def gen_knight_moves(self, row, col):
        moves = []
        peice_color = self.board[row][col][0]

        if peice_color == 'w':
            enemy = 'b'
        else:
            enemy = 'w'

        for x_direction in (-1, 1):
            for y_direction in (-1, 1):
                r = row + 1 * y_direction
                c = col + 2 * x_direction
                if 0 <= r <= 7 and 0 <= c <= 7 and (self.board[r][c][0] == enemy or self.board[r][c] == '--'):
                    moves.append(Move((row, col), (r, c), self.board))

        for x_direction in (-1, 1):
            for y_direction in (-1, 1):
                r = row + 2 * y_direction
                c = col + 1 * x_direction
                if 0 <= r <= 7 and 0 <= c <= 7 and (self.board[r][c][0] == enemy or self.board[r][c] == '--'):
                    moves.append(Move((row, col), (r, c), self.board))

        return moves

    def gen_bishop_moves(self, row, col):
        moves = []
        peice_color = self.board[row][col][0]

        if peice_color == 'w':
            enemy = 'b'
        else:
            enemy = 'w'

        for row_direction in (-1, 1):
            for col_direction in (-1, 1):
                currentRow = row
                currentCol = col
                while 0 <= currentRow + 1 * row_direction < 8 and 0 <= currentCol + 1 * col_direction < 8:
                    currentRow += 1 * row_direction
                    currentCol += 1 * col_direction
                    if self.board[currentRow][currentCol] == '--':
                        moves.append(Move((row, col), (currentRow, currentCol), self.board))
                    elif self.board[currentRow][currentCol][0] == enemy:
                        moves.append(Move((row, col), (currentRow, currentCol), self.board))
                        break
                    else:
                        break #This break is for if the peice is block by thier own color peices

        return moves

    def gen_king_moves(self, row, col):
        moves = []
        peice_color = self.board[row][col][0]

        if peice_color == 'w':
            enemy = 'b'
        else:
            enemy = 'w'

        for row_direction in (-1, 1):
            for col_direction in (-1, 1):
                r = row + 1 * row_direction
                c = col + 1 * col_direction
                if 0 <= r <= 7 and 0 <= c <= 7 and (self.board[r][c][0] == enemy or self.board[r][c] == '--'):
                    moves.append(Move((row, col), (r, c), self.board))

        for x_direction in (-1, 1):
            c = col + 1 * x_direction
            if 0 <= c <= 7 and (self.board[row][c][0] == enemy or self.board[row][c] == '--'):
                moves.append(Move((row, col), (row, c), self.board))

        for y_direction in (-1, 1):
            r = row + 1 * y_direction
            if 0 <= r <= 7 and (self.board[r][col][0] == enemy or self.board[r][col] == '--'):
                moves.append(Move((row, col), (r, col), self.board))



        return moves

    def gen_queen_moves(self, row, col):
        moves = []
        peice_color = self.board[row][col][0]

        if peice_color == 'w':
            enemy = 'b'
        else:
            enemy = 'w'

        for row_direction in (-1, 1):
            for col_direction in (-1, 1):
                currentRow = row
                currentCol = col
                while 0 <= currentRow + 1 * row_direction < 8 and 0 <= currentCol + 1 * col_direction < 8:
                    currentRow += 1 * row_direction
                    currentCol += 1 * col_direction
                    if self.board[currentRow][currentCol] == '--':
                        moves.append(Move((row, col), (currentRow, currentCol), self.board))
                    elif self.board[currentRow][currentCol][0] == enemy:
                        moves.append(Move((row, col), (currentRow, currentCol), self.board))
                        break
                    else:
                        break 

        for direction in (-1, 1):
            currentRow = row
            currentCol = col
            while 0 <= currentRow + 1 * direction < 8:
                currentRow += 1 * direction
                if self.board[currentRow][currentCol] == '--':
                    moves.append(Move((row,col), (currentRow, currentCol), self.board))
                elif self.board[currentRow][currentCol][0] == enemy:
                    moves.append(Move((row,col), (currentRow, currentCol), self.board))
                    break
                else:
                    break

        for direction in (-1, 1):
            currentRow = row
            currentCol = col
            while 0 <= currentCol + 1 * direction < 8:
                currentCol += 1 * direction
                if self.board[currentRow][currentCol] == '--':
                    moves.append(Move((row,col), (currentRow, currentCol), self.board))
                elif self.board[currentRow][currentCol][0] == enemy:
                    moves.append(Move((row,col), (currentRow, currentCol), self.board))
                    break
                else:
                    break 
        return moves
    

'''
This class is used to store the two most reacent clicks
Start square; first click. Second square; second click
'''
class Move():
    def __init__(self, startSQ, endSQ, board, isEnpassantMove = False):
        self.startRow = startSQ[0]
        self.startCol = startSQ[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.peiceMoved = board[self.startRow][self.startCol]
        self.peiceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = False
        self.isEnpassantMove = False
        if (self.peiceMoved == 'wp' and self.endRow == 0) or (self.peiceMoved == 'bp' and self.endRow == 7):
            self.isPawnPromotion = True
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.peiceCaptured = 'wp' if self.peiceMoved == 'bp' else 'bp'

        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        #print(self.moveID)
        #print(self.peice_moved, self.peice_captured)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def __str__(self):
        return f"{self.peiceMoved}: ({self.startRow},{self.startCol}) -> {self.peiceCaptured}: ({self.endRow},{self.endCol})"
