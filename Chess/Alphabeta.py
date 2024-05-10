import math
import random

pieceScore = {
    'K': 0,
    'Q': 10,
    'R': 5,
    'B': 3.2,
    'N': 3,
    'p': 1
}

endgameMaterialStart = pieceScore['R'] * 2 + pieceScore['B'] + pieceScore['N']

knightScores = [[-50,-40,-30,-30,-30,-30,-40,-50],
			[-40,-20,  0,  0,  0,  0,-20,-40],
			[-30,  0, 10, 15, 15, 10,  0,-30],
			[-30,  5, 15, 20, 20, 15,  5,-30],
			[-30,  0, 15, 20, 20, 15,  0,-30],
			[-30,  5, 10, 15, 15, 10,  5,-30],
			[-40,-20,  0,  5,  5,  0,-20,-40],
			[-50,-40,-30,-30,-30,-30,-40,-50]]

bishopScores = [[-20,-10,-10,-10,-10,-10,-10,-20],
			[-10,  0,  0,  0,  0,  0,  0,-10],
			[-10,  0,  5, 10, 10,  5,  0,-10],
			[-10,  5,  5, 10, 10,  5,  5,-10],
			[-10,  0, 10, 10, 10, 10,  0,-10],
			[-10, 10, 10, 10, 10, 10, 10,-10],
			[-10,  5,  0,  0,  0,  0,  5,-10],
			[-20,-10,-10,-10,-10,-10,-10,-20]]

queenScores = [ [-20,-10,-10, -5, -5,-10,-10,-20],
			[-10,  0,  0,  0,  0,  0,  0,-10],
			[-10,  0,  5,  5,  5,  5,  0,-10],
			[-5,  0,  5,  5,  5,  5,  0, -5],
			[0,  0,  5,  5,  5,  5,  0, -5],
			[-10,  5,  5,  5,  5,  5,  0,-10],
			[-10,  0,  5,  0,  0,  0,  0,-10],
			[-20,-10,-10, -5, -5,-10,-10,-20]]

rookScores = [  [0,  0,  0,  0,  0,  0,  0,  0],
			[5, 10, 10, 10, 10, 10, 10,  5],
			[-5,  0,  0,  0,  0,  0,  0, -5],
			[-5,  0,  0,  0,  0,  0,  0, -5],
			[-5,  0,  0,  0,  0,  0,  0, -5],
			[-5,  0,  0,  0,  0,  0,  0, -5],
			[-5,  0,  0,  0,  0,  0,  0, -5],
			[0,  0,  0,  5,  5,  0,  0,  0]]

pawnScores = [ [0,  0,  0,  0,  0,  0,  0,  0],
			[50, 50, 50, 50, 50, 50, 50, 50],
			[10, 10, 20, 30, 30, 20, 10, 10],
			[5,  5, 10, 25, 25, 10,  5,  5],
			[0,  0,  0, 20, 20,  0,  0,  0],
			[5, -5,-10,  0,  0,-10, -5,  5],
			[5, 10, 10,-20,-20, 10, 10,  5],
			[0,  0,  0,  0,  0,  0,  0,  0]]

kingMiddle = [[-30,-40,-40,-50,-50,-40,-40,-30],
			[-30,-40,-40,-50,-50,-40,-40,-30],
			[-30,-40,-40,-50,-50,-40,-40,-30],
			[-30,-40,-40,-50,-50,-40,-40,-30],
			[-20,-30,-30,-40,-40,-30,-30,-20],
			[-10,-20,-20,-20,-20,-20,-20,-10],
			[20, 20,  0,  0,  0,  0, 20, 20],
			[20, 30, 10,  0,  0, 10, 30, 20]]

kingEnd = [[-50,-40,-30,-20,-20,-30,-40,-50],
			[-30,-20,-10,  0,  0,-10,-20,-30],
			[-30,-10, 20, 30, 30, 20,-10,-30],
			[-30,-10, 30, 40, 40, 30,-10,-30],
			[-30,-10, 30, 40, 40, 30,-10,-30],
			[-30,-10, 20, 30, 30, 20,-10,-30],
			[-30,-30,  0,  0,  0,  0,-30,-30],
			[-50,-30,-30,-30,-30,-30,-30,-50]]                

piecePositionScores =  {"wN": knightScores,
                        "bN": knightScores[::-1],
                        "wB": bishopScores,
                        "bB": bishopScores[::-1],
                        "wQ": queenScores,
                        "bQ": queenScores[::-1],
                        "wR": rookScores,
                        "bR": rookScores[::-1],
                        "wp": pawnScores,
                        "bp": pawnScores[::-1],
                        "wK": kingMiddle,
                        "bK": kingMiddle[::-1]}


CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3
hashfEXACT = 0
hashfALPHA = 1
hashfBETA = 2

class TranspositionEntry:
    def __init__(self, key, depth, flags, value, best_move):
        self.key = key
        self.depth = depth
        self.flags = flags
        self.value = value
        self.best_move = best_move

# Step 2: Initialize Transposition Table
transposition_table = {}

# Step 3: Implement Hash Function
def generate_key(gs, turnMultiple):
    # This key should be deterministic and unique for each position
    hash_key = 0
    piece_values = {
        'bR': 1, 'bN': 2, 'bB': 3, 'bQ': 4, 'bK': 5, 'wR': 6, 'wN': 7, 'wB': 8, 'wQ': 9, 'wp': 10, 'bp': 11, 'wK':12  # Assign unique values to pieces
    }
    board = gs.board
    for rank in range(8):
        for file in range(8):
            piece = board[rank][file]
            if piece != '--':  # Only consider squares with pieces
                hash_key ^= (piece_values[piece] << (rank * 4 + file))   # XOR with position-shifted piece value

    hash_key ^= turnMultiple
    return hash_key

# Step 4: Probe Transposition Table
def probe_transposition_table(key):
    if key in transposition_table:
        return transposition_table[key]
    else:
        return None

# Step 5: Record Entries in Transposition Table
def record_transposition_entry(key, depth, flags, value, best_move):
    transposition_table[key] = TranspositionEntry(key, depth, flags, value, best_move)

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove(gs, validMoves, returnQueue):
    global nextMove, counter
    counter = 0
    nextMove = None
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)

    print(counter)

    returnQueue.put(nextMove)

def findMoveNegaMax(gs, validMoves, depth, turnMultiple):
    global nextMove
    if depth == 0:
        return turnMultiple * scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiple)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore    


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiple):
    global nextMove, counter

    counter += 1

    if depth == 0:
        return turnMultiple * scoreBoard(gs)
    
    #move ordering
    orderMoves(gs, validMoves)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()

        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiple)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        
        if alpha >= beta:
            break

    return maxScore    

def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE
    score = scoreMaterial(gs)
    return score

def orderMoves(gs, validMoves):
    #move ordering
    moveScores = {}
    for move in validMoves:
        moveScore = 0
        movePieceType = move.pieceMoved[1]
        capturePieceType = move.pieceCaptured[1]
        if capturePieceType != '-':
            moveScore = 10 * pieceScore[capturePieceType] - pieceScore[movePieceType]
        if move.isPawnPromotion:
            moveScore += pieceScore['Q'] - 1
        if gs.squareUnderAttack(move.endRow, move.endCol):
            moveScore -= pieceScore[movePieceType]
        # Hashing
        moveScores[move.moveID] = moveScore
    
    # Order the moves based on their scores (higher scores first)
    validMoves.sort(key=lambda move: moveScores[move.moveID], reverse=True)

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiple):
    global nextMove, counter

    counter += 1

    hashf = hashfALPHA

    # Probe transposition table
    transposition_entry = probe_transposition_table(generate_key(gs,turnMultiple))
    if transposition_entry and transposition_entry.depth >= depth:
        flag, value = transposition_entry.flags, transposition_entry.value
        if flag == hashfEXACT:
            if depth == DEPTH:
                nextMove = transposition_entry.best_move
            return value
        elif flag == hashfALPHA:
            alpha = max(alpha, value)
        elif flag == hashfBETA:
            beta = min(beta, value)

        
        if alpha >= beta:
            if depth == DEPTH:
                nextMove = transposition_entry.best_move
            return transposition_entry.value
    if depth == 0:
        eval = turnMultiple * scoreBoard(gs) * ( 1 + 0.01 * depth)
        record_transposition_entry(generate_key(gs, turnMultiple), depth, hashfEXACT, eval, nextMove)
        return eval
    
    #move ordering
    orderMoves(gs, validMoves)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()

        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiple)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:
            hashf = hashfEXACT
            alpha = maxScore
        
        if score >= beta:
            record_transposition_entry(generate_key(gs,turnMultiple), depth, hashfBETA, beta, nextMove)
            break
    
    record_transposition_entry(generate_key(gs,turnMultiple), depth, hashf, maxScore, nextMove)

    return maxScore

def scoreMaterial(gs):
    
    whiteScore = 0
    blackScore = 0
    
    whiteScoreWithoutPawns = 0
    blackScoreWithoutPawns = 0

    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != '--':

                #score positionally
                piecePositionScore = 0
                if square[1] != 'K': # no position score table for king
                #other pieces
                    piecePositionScore = piecePositionScores[square][row][col]  
                

                if square[0] == 'w':
                    whiteScore += pieceScore[square[1]] + piecePositionScore * 0.01
                    if square[1] != 'p': whiteScoreWithoutPawns += pieceScore[square[1]]
                elif square[0] == 'b':
                    blackScore += pieceScore[square[1]] + piecePositionScore * 0.01
                    if square[1] != 'p': blackScoreWithoutPawns += pieceScore[square[1]]
                
    whiteEndgamePhaseWeight = EndgamePhaseWeight(whiteScoreWithoutPawns)
    blackEndgamePhaseWeight = EndgamePhaseWeight(blackScoreWithoutPawns)

    whiteScore += forceKingEndgameScore(gs.whiteKingLocation, gs.blackKingLocation, blackEndgamePhaseWeight)
    blackScore += forceKingEndgameScore(gs.blackKingLocation, gs.whiteKingLocation, whiteEndgamePhaseWeight)


    whiteKingRow, whiteKingCol = gs.whiteKingLocation
    blackKingRow, blackKingCol = gs.blackKingLocation
    whiteScore += piecePositionScores['wK'][whiteKingRow][whiteKingCol] * (1-blackEndgamePhaseWeight) * 0.01
    blackScore += piecePositionScores['bK'][blackKingRow][blackKingCol] * (1-whiteEndgamePhaseWeight) * 0.01
    
    score = whiteScore - blackScore

    return score

def EndgamePhaseWeight(scoreWithoutPawns):
    multiplier = 1 / endgameMaterialStart
    return 1 - min(1, scoreWithoutPawns * multiplier)

def forceKingEndgameScore(allyKingSquare, opponentKingSquare, endgameWeight):
    eval = 0

    opponentKingRow, opponentKingCol = opponentKingSquare

    opponentKingDstToCentreCol = max(3-opponentKingCol, opponentKingCol -4)
    opponentKingDstToCentreRow = max(3-opponentKingRow, opponentKingRow -4) 
    opponentKingDstToCentre = opponentKingDstToCentreCol+opponentKingDstToCentreRow
    
    eval += opponentKingDstToCentre

    allyKingRow, allyKingCol = allyKingSquare

    dstBetweenKingCol = abs(allyKingCol - opponentKingCol)
    dstBetweenKingRow = abs(allyKingRow - opponentKingRow)
    dstBetweenKing = dstBetweenKingCol + dstBetweenKingRow

    eval += 14 - dstBetweenKing

    return eval * 10 * endgameWeight

