class GameState():
    #2d list string represent the board wwith black and white side
    def __init__(self) -> None:
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"],
        ]
        self.whiteToMove = True
        self.moveLog = []
    
    def makeMove(self,move):
        self.board[move.startRank][move.startFile] = "--"
        self.board[move.endRank][move.endFile] = move.pieceMoved
        self.moveLog.append(move) #store to able to undo
        self.whiteToMove = not self.whiteToMove #swap player

class Move():
    def __init__(self, startSQ, endSQ, board) -> None:
        self.startRank = startSQ[0]
        self.startFile = startSQ[1]
        self.endRank = endSQ[0]
        self.endFile = endSQ[1]
        self.pieceMoved = board[self.startRank][self.startFile]
        self.pieceCaptured = board[self.endRank][self.endFile]
    
    