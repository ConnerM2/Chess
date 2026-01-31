

class GameState():
    def __init__(self):
        self.board = [
                ['bR', 'bN', 'bB', 'bK', 'BQ', 'bB', 'bN', 'bR'],
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
        if self.board[row][col][0] == 'w':
            if row == 6:
                moves.append(Move((row,col), (row-1,col), self.board))
                moves.append(Move((row,col), (row-2,col), self.board))
            else:
                moves.append(Move((row,col), (row-1,col), self.board))
        elif self.board[row][col][0] == 'b':
            if row == 1:
                moves.append(Move((row,col), (row+1,col), self.board))
                moves.append(Move((row,col), (row+2,col), self.board))
            else:
                moves.append(Move((row,col), (row+1,col), self.board))
        return moves
    
    def gen_rook_moves(self, row, col):
        return []
    def gen_knight_moves(self, row, col):
        return []
    def gen_bishop_moves(self, row, col):
        return []
    def gen_king_moves(self, row, col):
        return []
    def gen_queen_moves(self, row, col):
        return []
    



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
