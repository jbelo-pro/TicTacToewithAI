import random


class Player:

    def __init__(self, symbol):
        self.symbol = symbol
        self.opponent = 'O' if symbol == 'X' else 'X'

    def coor_is_number(self, coor):
        if len(coor) != 2 or not coor[0].isnumeric() or not coor[1].isnumeric():
            return False
        else:
            return True

    def coor_in_range(self, coor):
        if coor[0] not in ['1', '2', '3'] or coor[1] not in ['1', '2', '3']:
            return False
        else:
            return True

    def convert_coordinates(self, a_coor, b_coor):
        row = 2 - (b_coor - 1)
        pos = a_coor - 1
        return row, pos

    def check_available_coor(self, matrix, row, pos):
        if matrix[row][pos] == 'X' or matrix[row][pos] == 'O':
            return False
        else:
            return True


class PlayerUser(Player):

    def __init__(self, symbol):
        super().__init__(symbol)

    def play(self, matrix):
        while True:
            position = input('Enter the coordinates: ').split()
            if not self.coor_is_number(position):
                print('You should enter numbers!')
                continue
            if not self.coor_in_range(position):
                print("Coordinates should be from 1 to 3!")
                continue

            row, pos = self.convert_coordinates(int(position[0]), int(position[1]))

            if not self.check_available_coor(matrix, row, pos):
                print("This cell is occupied! Choose another one!")
            else:
                matrix[row][pos] = self.symbol
                break


class PlayerMachine(Player):
    def __init__(self, symbol, level):
        super().__init__(symbol)
        self.level = level
        self.fc = 0

    # returns the available spots on the board
    def emptyIndexies(self, board):
        # return board.filter(s= > s != "O" & & s != "X");}
        return [x for x in board if x != 'O' and x != 'X']

    # winning combinations using the board indexies
    # for instace the first win could be 3 xes in a row
    def winning(self, board, player):
        if board[0] == player and board[1] == player and board[2] == player or \
                board[3] == player and board[4] == player and board[
            5] == player or board[6] == player and board[7] == player and \
                board[8] == player or board[0] == player and board[
            3] == player and board[6] == player or board[1] == player and \
                board[4] == player and board[7] == player or board[
            2] == player and board[5] == player and board[8] == player or \
                board[0] == player and board[4] == player and board[
            8] == player or board[2] == player and board[4] == player and \
                board[6] == player:
            return True
        else:
            return False

    def minimax(self, newBoard, player):
        # add one to function calls
        # global fc # TODO do we need it?
        self.fc += 1

        # available spots
        availSpots = self.emptyIndexies(newBoard)


        # checks for the terminal states such as win, lose, and tie and returning a value accordingly
        if self.winning(newBoard, self.opponent):
            return {'score': -10}
        elif self.winning(newBoard, self.symbol):
            return {'score': 10}
        elif len(availSpots) == 0:
            return {'score': 0}

        # an array to collect all the objects
        moves = []

        # loop through available spots
        for i in range(len(availSpots)):
            # create an object for each and store the index of that spot that was stored as a number in the object's index key
            move = {'index': newBoard[availSpots[i]]}

            # set the empty spot to the current player
            newBoard[availSpots[i]] = player

            # if collect the score resulted from calling minimax on the opponent of the current player
            if player == self.symbol:
                result = self.minimax(newBoard, self.opponent)
                move['score'] = result['score']
            else:
                result = self.minimax(newBoard, self.symbol)
                move['score'] = result['score']

            # reset the spot to empty
            newBoard[availSpots[i]] = move['index']

            # push the object to the array
            moves.append(move)

            # if it is the computer's turn loop over the moves and choose the move with the highest score
            bestMove = None
            if player == self.symbol:
                bestScore = -10000
                for i in range(len(moves)):
                    if moves[i]['score'] > bestScore:
                        bestScore = moves[i]['score']
                        bestMove = i
            else:
                # else loop over the moves and choose the move with the lowest score
                bestScore = 10000
                for i in range(len(moves)):
                    if moves[i]['score'] < bestScore:
                        bestScore = moves[i]['score']
                        bestMove = i

            # return the chosen move(object) from the array to the higher depth
            return moves[bestMove]


    def complete_random(self, matrix):
        free = []
        for row_index in range(3):
            row = matrix[row_index]
            for column_index in range(3):
                column = row[column_index]
                if column == '_':
                    free.append([row_index, column_index])
        coor = None
        if len(free) == 1:
            coor = free[0]
        else:
            coor = free[random.randint(0, len(free)) - 1]
        matrix[coor[0]][coor[1]] = self.symbol


    def complete_horizontal(self, matrix, search_symbol, complete_symbol):
        row_index = 0
        for row in matrix:
            column_index = 0
            in_row = 0
            free = None
            for column in row:
                if column == search_symbol:
                    in_row += 1
                if column == '_':
                    free = [row_index, column_index]
                column_index += 1
            if in_row == 2 and free:
                matrix[free[0]][free[1]] = complete_symbol
                return True
            row_index += 1
        return False

    
    def complete_vertical(self, matrix, search_symbol, complete_symbol):

        for column_index in range(3):
            in_column = 0
            free = None
            for row_index in range(3):
                if matrix[row_index][column_index] == search_symbol:
                    in_column += 1
                if matrix[row_index][column_index] == '_':
                    free = [row_index, column_index]
            if in_column == 2 and free:
                matrix[free[0]][free[1]] = complete_symbol
                return True
        return False


    def complete_diagonal(self, matrix, search_symbol, complete_symbol):
        in_line = 0
        free = None
        for i in range(3):
            if matrix[i][i] == search_symbol:
                in_line += 1
            elif matrix[i][i] == '_':
                free = [i, i]
        if in_line == 2 and free:
            matrix[free[0]][free[1]] = complete_symbol
            return True
        in_line = 0
        free = None
        for i in range(3):
            if matrix[i][-(i + 1)] == search_symbol:
                in_line += 1
            elif matrix[i][-(i + 1)] == '_':
                free = [i, -(i + 1)]
        if in_line == 2 and free:
            matrix[free[0]][free[1]] = complete_symbol
            return True
        return False

    def medium_machine(self, matrix):

        if not self.complete_horizontal(matrix, self.symbol, self.symbol):
            if not self.complete_vertical(matrix, self.symbol, self.symbol):
                if not self.complete_diagonal(matrix, self.symbol, self.symbol):
                    if not self.complete_horizontal(matrix,
                                                    self.opponent, self.symbol):
                        if not self.complete_vertical(matrix, self.opponent,
                                                      self.symbol):
                            if not self.complete_diagonal(matrix,
                                                          self.opponent,
                                                          self.symbol):
                                self.complete_random(matrix)

    def hard_machine(self, matrix):
        flat_board = []
        position = 0
        for row in matrix:
            for column in row:
                if column != "_":
                    flat_board.append(column)
                else:
                    flat_board.append(position)
                position += 1
        # print(flat_board)
        best_spot = self.minimax(flat_board, self.symbol)

        target_row = best_spot['index'] // 3
        target_column = best_spot['index'] % 3
        # print(best_spot)
        # print('machine move to {} - {}'.format(target_row, target_column))
        # print('fc {}'.format(self.fc))
        matrix[target_row][target_column] = self.symbol




    def play(self, matrix):
        print('Making move level "{}"'.format(self.level))
        if self.level == 'easy':
            self.complete_random(matrix)
        elif self.level == 'medium':
            self.medium_machine(matrix)
        else:
            self.hard_machine(matrix)


def create_matrix(text):
    m = []
    for p in range(3, 10, 3):
        m.append([x for x in text[p - 3: p]])
    return m


def horizontal(symbol, matrix):
    winner = False
    for row in matrix:
        win = True
        for cell in row:
            if cell != symbol:
                win = False
                break
        if win:
            winner = True
            break
    return winner


def vertical(symbol, matrix):
    t_matrix = [[y for y in  x] for x in zip(*matrix)]
    return horizontal(symbol, t_matrix)


def diagonal(symbol, matrix):
    winner = True
    for i in range(3):
        if matrix[i][i] != symbol:
            winner = False
    if winner:
        return winner
    winner = True
    for i in range(3):
        if matrix[i][-(i + 1)] != symbol:
            winner = False
    return winner


def is_winner(symbol, matrix):
    if vertical(symbol, matrix) or \
       horizontal(symbol, matrix) or \
       diagonal(symbol, matrix):
        return True
    else:
        return False


def invalid_symbols(matrix):
    symbo_x = 0
    symbo_y = 0

    for row in matrix:
        for c in row:
            if c == 'X':
                symbo_x += 1
            elif c == 'O':
                symbo_y += 1
    if abs(symbo_y - symbo_x) >= 2:
        return True
    else:
        return False


def is_impossible(matrix):
    if is_winner('X', matrix) and is_winner('O', matrix) or invalid_symbols(matrix):
        return True
    else:
        return False


def has_space(matrix):
    counter = 0
    for row in matrix:
        for c in row:
            if c == '_':
                counter += 1
    if counter:
        return True
    else:
        return False


def print_matrix(matrix):
    print('---------')
    for row in matrix:
        line = '| {} {} {} |'.format(row[0], row[1], row[2])
        print(line)
    print('---------')


def active_player(matrix):
    x = 0
    o = 0
    for row in matrix:
        for cell in row:
            if cell == 'X':
                x += 1
                continue
            if cell == 'O':
                o += 1
    if x == o:
        return 'X'
    else:
        return 'X' if x < o else 'O'


def check_parameters(param, val_c):
    if 'start' in param and len(param) == 3 and \
            param[1] in val_c and param[2] in val_c:
        return True
    elif 'exit' in param and len(param) == 1:
        return True
    else:
        return False


valid_players = ['user', 'easy', 'medium', 'hard']

while True:
    parameters = input('Input command: ').split()
    if check_parameters(parameters, valid_players):
        if 'exit' in parameters:
            break
        else:
            matrix = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]
            print_matrix(matrix)
            player_x = PlayerUser('X') if parameters[1] == 'user' else \
                PlayerMachine('X', parameters[1])
            player_o = PlayerUser('O') if parameters[2] == 'user' else \
                PlayerMachine('O', parameters[2])
            player = None
            while True:
                if is_winner(player_x.symbol, matrix):
                    print('X wins')
                    break
                elif is_winner(player_o.symbol, matrix):
                    print('O wins')
                    break
                elif not has_space(matrix):
                    print('Draw')
                    break
                else:
                    player = player_x if not player or player.symbol == 'O' else \
                        player_o

                    player.play(matrix)
                    print_matrix(matrix)

    else:
        print('Bad parameters!')
