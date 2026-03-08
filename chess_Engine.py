

class GameState():
    def __init__(self):
        self.board = [
                ['bR', 'bN', 'bB', 'bK', 'bQ', 'bB', 'bN', 'bR'],
                ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                ['wR', 'wN', 'wB', 'wK', 'wQ', 'wB', 'wN', 'wR']]
        
        self.whiteToMove = True
        self.moveHistory = []

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
        self.board[move.endRow][move.endCol] = move.peice_moved
        self.moveHistory.append(move)
        self.whiteToMove = not self.whiteToMove
        #print(self.whiteToMove)


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

    def all_legal_moves(self): #sorts through all moves and returns moves that dont put king in danger
        pass

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
    def __init__(self, startSQ, endSQ, board):
        self.startRow = startSQ[0]
        self.startCol = startSQ[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.peice_moved = board[self.startRow][self.startCol]
        self.peice_captured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        #print(self.moveID)
        #print(self.peice_moved, self.peice_captured)

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    
    def __str__(self):
        return f"{self.peice_moved}: ({self.startRow},{self.startCol}) -> {self.peice_captured}: ({self.endRow},{self.endCol})"
