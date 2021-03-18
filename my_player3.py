from copy import deepcopy
import json


class AlphaBeta:
    def _init_(self, board, previous_board, move, lastDiedPieces, pieceType):
        self.board = deepcopy(board)
        self.previous_board = previous_board
        self.diedPiece = []
        self.lastMove = move
        self.enemyPiecesDied = 0
        self.myPiecesDied = 0
        self.lastDiedPieces = lastDiedPieces
        self.pieceType = pieceType
        self.lastPreviousBoard = deepcopy(previous_board)

    def evaluationFunction(self, updatedBoard):
        myPoints = 0
        enemyPoints = 0
        group = []
        for i in range(0, 5):
            for j in range(0, 5):
                if updatedBoard[i][j] == piece_type:
                    # if (i, j) not in group:
                    #     stoneGroup, myLiberty = self.findNoOfLiberty(i, j, updatedBoard)
                    #     group.append(stoneGroup)
                    #     myPoints += myLiberty * 1
                    myPoints += 1
                if updatedBoard[i][j] == 3 - piece_type:
                    # if (i, j) not in group:
                    #     stoneGroup, enemyLiberty = self.findNoOfLiberty(i, j, updatedBoard)
                    #     group.append(stoneGroup)
                    #     myPoints += enemyLiberty * 1
                    enemyPoints += 1
        myPoints += self.enemyPiecesDied * 16
        enemyPoints += self.myPiecesDied * 10
        if piece_type == 1:
            enemyPoints += 2.5
        else:
            myPoints += 2.5
        return myPoints - enemyPoints

    def getPossibleMove(self, nBoard, diedPiece, pieceType):
        possibleMove = []
        for i in range(1,4):
            for j in range(1,4):
                if nBoard[i][j] == 0 and self.valid_place_check(i, j, pieceType, nBoard):
                    # d = self.getNearestOpponentPiece(i, j, pieceType, nBoard)
                    dist = abs(i - self.lastMove[0]) + abs(j - self.lastMove[1])
                    # dist = min(dist, d)
                    possibleMove.append((i, j, dist))
        for j in range(5):
            if nBoard[0][j] == 0 and self.valid_place_check(0, j, pieceType, nBoard):
                # d = self.getNearestOpponentPiece(i, j, pieceType, nBoard)
                dist = abs(0 - self.lastMove[0]) + abs(j - self.lastMove[1])
                # dist = min(dist, d)
                if (0, j, dist) not in possibleMove:
                    possibleMove.append((0, j, dist))
        for j in range(5):
            if nBoard[4][j] == 0 and self.valid_place_check(4, j, pieceType, nBoard):
                # d = self.getNearestOpponentPiece(i, j, pieceType, nBoard)
                dist = abs(4 - self.lastMove[0]) + abs(j - self.lastMove[1])
                # dist = min(dist, d)
                if (4, j, dist) not in possibleMove:
                    possibleMove.append((4, j, dist))
        for i in range(5):
            if nBoard[i][0] == 0 and self.valid_place_check(i, 0, pieceType, nBoard):
                # d = self.getNearestOpponentPiece(i, j, pieceType, nBoard)
                dist = abs(i - self.lastMove[0]) + abs(0 - self.lastMove[1])
                # dist = min(dist, d)
                if (i, 0, dist) not in possibleMove:
                    possibleMove.append((i, 0, dist))
        for i in range(5):
            if nBoard[i][4] == 0 and self.valid_place_check(i, 4, pieceType, nBoard):
                # d = self.getNearestOpponentPiece(i, j, pieceType, nBoard)
                dist = abs(i - self.lastMove[0]) + abs(4 - self.lastMove[1])
                # dist = min(dist, d)
                if (i, 4, dist) not in possibleMove:
                    possibleMove.append((i, 4, dist))
        if len(possibleMove) == 0:
            return possibleMove
        return sorted(possibleMove, key=lambda x: x[2])

    def getNearestOpponentPiece(self, x, y, pieceType, nboard):
        d = 10000
        for i in range(5):
            for j in range(5):
                if nboard[i][j] == pieceType:
                    dist = abs(i - x) + abs(j - y)
                    d = min(d, dist)
        return d

    def valid_place_check(self, i, j, pieceType, nBoard):

        if not (0 <= i < len(board)):
            return False
        if not (0 <= j < len(board)):
            return False

        if nBoard[i][j] != 0:
            return False

        test_board = deepcopy(nBoard)

        test_board[i][j] = pieceType
        if self.find_liberty(i, j, test_board):
            return True

        diedPiece, test_board = self.removediedpieces(3 - pieceType, test_board)
        if not self.find_liberty(i, j, test_board):
            return False

        else:
            if self.compare_board(self.lastPreviousBoard, test_board):
                return False
        return True

    def compare_board(self, board1, board2):
        for i in range(5):
            for j in range(5):
                if board1[i][j] != board2[i][j]:
                    return False
        return True

    def isGameEnd(self, n):
        if n >= 25:
            return True
        return False

    def amIWinner(self, board):
        myScore = 0
        enemyScore = 0
        if self.pieceType == 1:
            enemyScore += 2.5
        else:
            myScore += 2.5
        for i in range(5):
            for j in range(5):
                if board[i][j] == self.pieceType:
                    myScore += 1
                if board[i][j] == 3 - self.pieceType:
                    enemyScore += 1
        if myScore > enemyScore:
            return True
        return False

    def min_value(self, alpha, beta, depth, pieceType, board, n):
        enemyPieces = len(self.find_died_pieces(pieceType, board))
        self.enemyPiecesDied += enemyPieces
        diedPiece, newBoard = self.removediedpieces(pieceType, deepcopy(board))
        self.diedPiece = diedPiece

        if self.isGameEnd(n):
            self.enemyPiecesDied -= enemyPieces
            if self.amIWinner(newBoard):
                return 50, None, None
            else:
                return -60, None, None

        if depth == 0:
            value = self.evaluationFunction(newBoard), 0, 0
            self.enemyPiecesDied -= enemyPieces
            return value

        x_pos = None
        y_pos = None
        bestValue = 100000000
        moves = self.getPossibleMove(newBoard, diedPiece, pieceType)
        self.lastPreviousBoard = deepcopy(newBoard)
        counter = 0
        for move in moves:
            i = move[0]
            j = move[1]
            if counter > -1:
                counter += 1
                newBoard[i][j] = pieceType
                value = self.max_value(alpha, beta, depth - 1, 3 - pieceType, newBoard, n + 1)
                if bestValue > value[0]:
                    bestValue = value[0]
                    x_pos = i
                    y_pos = j
                beta = min(bestValue, beta)
                newBoard[i][j] = 0
                if beta <= alpha:
                    return bestValue, x_pos, y_pos
        return bestValue, x_pos, y_pos

    def max_value(self, alpha, beta, depth, pieceType, board, n):
        myPieces = len(self.find_died_pieces(pieceType, board))
        self.myPiecesDied += myPieces
        diedPiece, newBoard = self.removediedpieces(pieceType, deepcopy(board))
        self.diedPiece = diedPiece

        if self.isGameEnd(n):
            self.myPiecesDied -= myPieces
            if self.amIWinner(newBoard):
                return 50, None, None
            else:
                return -200, None, None

        if depth == 0:
            value = self.evaluationFunction(newBoard), 0, 0
            self.myPiecesDied -= myPieces
            return value

        x_pos = None
        y_pos = None
        bestValue = -100000000
        counter = 0
        allMoves = self.getPossibleMove(newBoard, diedPiece, pieceType)
        self.lastPreviousBoard = deepcopy(newBoard)
        for move in allMoves:
            i = move[0]
            j = move[1]
            if True:
                counter += 1
                newBoard[i][j] = pieceType
                value = self.min_value(alpha, beta, depth - 1, 3 - pieceType, newBoard, n + 1)
                if bestValue < value[0]:
                    bestValue = value[0]
                    x_pos = i
                    y_pos = j
                alpha = max(bestValue, alpha)
                newBoard[i][j] = 0
                if beta <= alpha:
                    return bestValue, x_pos, y_pos
        return bestValue, x_pos, y_pos

    def alphaBetaStart(self, moveNo):
        alpha, x_pos, y_pos = self.max_value(-100000000, 100000000, 2, piece_type, board, moveNo)
        return x_pos, y_pos

    def detect_neighbor(self, i, j, newBoard):
        board = newBoard
        neighbors = []
        # Detect borders and add neighbor coordinates
        if i > 0: neighbors.append((i - 1, j))
        if i < len(board) - 1: neighbors.append((i + 1, j))
        if j > 0: neighbors.append((i, j - 1))
        if j < len(board) - 1: neighbors.append((i, j + 1))
        return neighbors

    def detect_neighbor_ally(self, i, j, newBoard):
        board = newBoard
        neighbors = self.detect_neighbor(i, j, board)  # Detect neighbors
        group_allies = []
        # Iterate through neighbors
        for piece in neighbors:
            # Add to allies list if having the same color
            if board[piece[0]][piece[1]] == board[i][j]:
                group_allies.append(piece)
        return group_allies

    def ally_dfs(self, i, j, newBoard):
        stack = [(i, j)]  # stack for DFS serach
        ally_members = []  # record allies positions during the search
        while stack:
            piece = stack.pop()
            ally_members.append(piece)
            neighbor_allies = self.detect_neighbor_ally(piece[0], piece[1], newBoard)
            for ally in neighbor_allies:
                if ally not in stack and ally not in ally_members:
                    stack.append(ally)
        return ally_members

    def findNoOfLiberty(self, i, j, nBoard):
        board = nBoard
        count = 0
        ally_members = self.ally_dfs(i, j, board)
        for member in ally_members:
            neighbors = self.detect_neighbor(member[0], member[1], board)
            for piece in neighbors:
                # If there is empty space around a piece, it has liberty
                if board[piece[0]][piece[1]] == 0:
                    count += 1
        # If none of the pieces in a allied group has an empty space, it has no liberty
        return ally_members, count

    def find_liberty(self, i, j, newBoard):
        board = newBoard
        ally_members = self.ally_dfs(i, j, board)
        for member in ally_members:
            neighbors = self.detect_neighbor(member[0], member[1], board)
            for piece in neighbors:
                # If there is empty space around a piece, it has liberty
                if board[piece[0]][piece[1]] == 0:
                    return True
        # If none of the pieces in a allied group has an empty space, it has no liberty
        return False

    def find_died_pieces(self, piece_type, newBoard):
        board = newBoard
        died_pieces = []

        for i in range(len(board)):
            for j in range(len(board)):
                # Check if there is a piece at this position:
                if board[i][j] == piece_type:
                    # The piece die if it has no liberty
                    if not self.find_liberty(i, j, board):
                        died_pieces.append((i, j))
        return died_pieces

    def removediedpieces(self, piece_type, board):

        died_pieces = self.find_died_pieces(piece_type, board)
        if not died_pieces: return [], board
        updateBoard = self.remove_certain_pieces(died_pieces, board)
        return died_pieces, updateBoard

    def remove_certain_pieces(self, positions, newBoard):
        board = newBoard
        for piece in positions:
            board[piece[0]][piece[1]] = 0
        return board


def getLastMove(previousBoard, board):
    for i in range(5):
        for j in range(5):
            if previousBoard[i][j] != board[i][j]:
                return i, j
    return 2, 2


def getLastDiedPieces(previousBoard, board, pieceType):
    died = []
    for i in range(5):
        for j in range(5):
            if previousBoard[i][j] == pieceType and board[i][j] == 0:
                died.append((i, j))
    return died


def readInput(n, path="input.txt"):
    with open(path, 'r') as f:
        lines = f.readlines()

        piece_type = int(lines[0])

        previous_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:n + 1]]
        board = [[int(x) for x in line.rstrip('\n')] for line in lines[n + 1: 2 * n + 1]]

        return piece_type, previous_board, board


def writeOutput(result, path="output.txt"):
    res = ""
    if result == "PASS":
        res = "PASS"
    else:
        res += str(result[0]) + ',' + str(result[1])

    with open(path, 'w') as f:
        f.write(res)


def getMoves():
    with open('init/move_track.json', 'r') as f:
        file = json.load(f)
    return file


def updateMove(data):
    with open('init/move_track.json', 'w') as f:
        json.dump(data, f)


if _name_ == "_main_":
    N = 5
    piece_type, previous_board, board = readInput(N)
    dict = getMoves()

    if piece_type == dict["piece_type"]:
        dict["move_no"] = int(dict["move_no"]) + 2
    else:
        dict["piece_type"] = int(piece_type)
        dict["move_no"] = int(piece_type) + 2

    move_no = int(dict["move_no"]) - 2
    opponentLastMove = getLastMove(previous_board, board)
    lastDiedPieces = getLastDiedPieces(previous_board, board, piece_type)
    player = AlphaBeta(board, previous_board, opponentLastMove, lastDiedPieces, piece_type)
    possibleAction = player.alphaBetaStart(move_no)

    updateMove(dict)

    action = "PASS"
    if possibleAction[0] is not None:
        action = possibleAction
    #print(action)
    writeOutput(action)