

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