

class GameState():
    def __init__(self):
        self.board = [
                ['bR', 'bK', 'bB', 'bK', 'BQ', 'bB', 'bK', 'bR'],
                ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                ['wR', 'wK', 'wB', 'wK', 'wQ', 'wB', 'wK', 'wR']]
        
        self.whiteToMove = True
        self.moveHistory = []

    def makeMove(self, move):
        self.board[move.startCol][move.startRow] = '--'
        self.board[move.endCol][move.endRow] = move.peice_moved
        self.moveHistory.append(move)
        print(move)
        self.whiteToMove = not self.whiteToMove

class Move():
    def __init__(self, startSQ, endSQ, board):
        self.startCol = startSQ[0]
        self.startRow = startSQ[1]
        self.endCol = endSQ[0]
        self.endRow = endSQ[1]
        self.peice_moved = board[self.startCol][self.startRow]
        self.peice_captured = board[self.endCol][self.endRow]
        print(self.peice_moved, self.peice_captured)
