pieceScore = {
    'K': 0,
    'Q': 900,
    'R': 500,
    'B': 320,
    'N': 300,
    'p': 100
}

endgameMaterialStart = pieceScore['R'] * 2 + pieceScore['B'] + pieceScore['N']

passedPawnBonuses = [ 0, 120, 80, 50, 30, 15, 15 ]
isolatedPawnPenaltyByCount = [ 0, -10, -25, -50, -75, -75, -75, -75, -75 ]

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

pawnEndScores = [ [0,   0,   0,   0,   0,   0,   0,   0],
			[80,  80,  80,  80,  80,  80,  80,  80],
			[50,  50,  50,  50,  50,  50,  50,  50],
			[30,  30,  30,  30,  30,  30,  30,  30],
			[20,  20,  20,  20,  20,  20,  20,  20],
			[10,  10,  10,  10,  10,  10,  10,  10],
			[10,  10,  10,  10,  10,  10,  10,  10],
			 [0,   0,   0,   0,   0,   0,   0,   0]]

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
                        "wpE": pawnEndScores,
                        "bpE": pawnEndScores[::-1],
                        "wK": kingMiddle,
                        "bK": kingMiddle[::-1],
                        "wKE": kingEnd,
                        "bKE": kingEnd[::-1]}

CHECKMATE = 9999999
STALEMATE = 0

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

def scoreMaterial(gs):
    
    # Total Score
    whiteScore = 0
    blackScore = 0

    # Score based on number and type of pieces
    whiteMaterialScore = 0
    blackMaterialScore = 0

    # Pawn score
    whitePawnEarly = 0
    blackPawnEarly = 0
    whitePawnEnd = 0
    blackPawnEnd = 0


    # Weight to determine endgame transition
    queenEndgameWeight = 45
    rookEndgameWeight = 20
    bishopEndgameWeight = 10
    knightEndgameWeight = 10

    # number of queens and minors
    numWQueens = 0
    numWRooks = 0
    numWBishops = 0
    numWKnights = 0

    numBQueens = 0
    numBRooks = 0
    numBBishops = 0
    numBKnights = 0

    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != '--':

                if square[1] == 'wQ':
                    numWQueens += 1
                elif square[1] == 'wR':
                    numWRooks += 1
                elif square[1] == 'wB':
                    numWBishops += 1
                elif square[1] == 'wN':
                    numWKnights += 1

                if square[1] == 'bQ':
                    numBQueens += 1
                elif square[1] == 'bR':
                    numBRooks += 1
                elif square[1] == 'bB':
                    numBBishops += 1
                elif square[1] == 'bN':
                    numBKnights += 1

                #score positionally
                piecePositionScore = 0
                if square[1] != 'K': # no position score table for king
                #other pieces
                    if square[1] == 'p':
                        if square[0] == 'w':
                            whitePawnEarly += piecePositionScores["wp"][row][col]
                            whitePawnEnd += piecePositionScores["wpE"][row][col]
                                

                        else:
                            blackPawnEarly += piecePositionScores["bp"][row][col]
                            blackPawnEnd += piecePositionScores["bpE"][row][col]

                    else:
                        piecePositionScore = piecePositionScores[square][row][col]  
                

                if square[0] == 'w':
                    whiteScore += pieceScore[square[1]] + piecePositionScore 
                    whiteMaterialScore += pieceScore[square[1]]
        
                elif square[0] == 'b':
                    blackScore += pieceScore[square[1]] + piecePositionScore 
                    blackMaterialScore += pieceScore[square[1]]
                    

    # calculate engameWeight(0 -> 1)
    endgameStartWeight = 2 * rookEndgameWeight + 2 * bishopEndgameWeight + 2 * knightEndgameWeight + queenEndgameWeight
    
    whiteEndgameWeightSum = numWQueens * queenEndgameWeight + numWRooks * rookEndgameWeight + numWBishops * bishopEndgameWeight + numWKnights * knightEndgameWeight
    blackEndgameWeightSum = numBQueens * queenEndgameWeight + numBRooks * rookEndgameWeight + numBBishops * bishopEndgameWeight + numBKnights * knightEndgameWeight

    whiteEndgameR = 1 - min(1, whiteEndgameWeightSum / endgameStartWeight)
    blackEndgameR = 1 - min(1, blackEndgameWeightSum / endgameStartWeight)

    # force king to edge
    whiteScore += forceKingEndgameScore(gs.whiteKingLocation, gs.blackKingLocation, whiteMaterialScore, blackMaterialScore, blackEndgameR)
    blackScore += forceKingEndgameScore(gs.blackKingLocation, gs.whiteKingLocation, blackMaterialScore, whiteMaterialScore, whiteEndgameR)

    # pawn early and pawn late 
    whiteScore += (int)(whitePawnEarly * (1 - blackEndgameR) + whitePawnEnd * blackEndgameR)
    blackScore += (int)(blackPawnEarly * (1 - whiteEndgameR) + blackPawnEnd * whiteEndgameR)


    whiteKingRow, whiteKingCol = gs.whiteKingLocation
    blackKingRow, blackKingCol = gs.blackKingLocation

    # king early phase
    whiteScore += (int)(piecePositionScores['wK'][whiteKingRow][whiteKingCol] * (1-blackEndgameR))
    blackScore += (int)(piecePositionScores['bK'][blackKingRow][blackKingCol] * (1-whiteEndgameR))
    
    # king late phase
    whiteScore += (int)(piecePositionScores['wKE'][whiteKingRow][whiteKingCol] * (blackEndgameR)) 
    blackScore += (int)(piecePositionScores['bKE'][blackKingRow][blackKingCol] * (whiteEndgameR))

    score = whiteScore - blackScore

    return score

def EndgamePhaseWeight(scoreWithoutPawns):
    multiplier = 1 / endgameMaterialStart
    return 1 - min(1, scoreWithoutPawns * multiplier)

def forceKingEndgameScore(allyKingSquare, opponentKingSquare, myScore, opponentScore, endgameWeight):
    eval = 0

    if (myScore > opponentScore + 2 * pieceScore['p'] and endgameWeight > 0):
        opponentKingRow, opponentKingCol = opponentKingSquare

        opponentKingDstToCentreCol = max(3-opponentKingCol, opponentKingCol -4)
        opponentKingDstToCentreRow = max(3-opponentKingRow, opponentKingRow -4) 
        opponentKingDstToCentre = opponentKingDstToCentreCol + opponentKingDstToCentreRow
        
        eval += opponentKingDstToCentre * 10

        allyKingRow, allyKingCol = allyKingSquare

        dstBetweenKingCol = abs(allyKingCol - opponentKingCol)
        dstBetweenKingRow = abs(allyKingRow - opponentKingRow)
        dstBetweenKing = dstBetweenKingCol + dstBetweenKingRow

        eval += (14 - dstBetweenKing) * 4

        return eval * endgameWeight
    return 0
