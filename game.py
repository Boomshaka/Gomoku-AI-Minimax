class Game(object):

    def __init__(self):
        # board is a 15*15 array
        self.__size = 15

        #board is a representation of the current game board
        self.__board = [[0 for i in range(self.__size)] for j in range(self.__size)]

        '''
        Ghost board is any hypothetical board state.
        The AI searches for its optimal move using minimax algorithm, 
        and will modify the ghost board when doing so.
        This allows for the real board to remain unchanged until a move is actually made,
        making debugging easier :)
        '''
        self.__ghost_board = self.__board.copy()
        self.__player_turn = 2

        '''
            The following lists are the possible patterns of pieces and their respective scores.
            Values are formatted as:
                {player}_{length} where player = 1 || 2, length = 5 || 6 -> This is a combination of pieces
                score_{length} where length = 5 || 6 -> This is the score to be assigned for respective pattern
        '''
        self.one_6 = [  [0,1,1,1,1,1],#five
                        [1,1,1,1,1,0],#five
                        [0,1,1,1,1,0],#straight four
                        [0,1,0,1,1,1],#four
                        [1,1,1,0,1,0],#four
                        [0,1,1,0,1,1],#four
                        [1,1,0,1,1,0],#four
                        [0,1,1,1,0,1],#four
                        [1,0,1,1,1,0],#four
                        [0,1,1,1,0,0],#straight three
                        [0,0,1,1,1,0],#straight three
                        [0,1,0,1,1,0],#straight three
                        [0,1,1,0,1,0],#straight three
                        [2,1,1,1,0,0],#three
                        [0,0,1,1,1,2],#three
                        [2,1,1,0,1,0],#three
                        [0,1,0,1,1,2],#three
                        [0,1,1,0,1,2],#three
                        [2,1,0,1,1,0],#three
                        [0,0,1,1,0,0],#straight two
                        [0,1,0,0,1,0],#straight two
                        [0,0,0,1,1,2],#two
                        [2,1,1,0,0,0],#two
                        [0,0,1,0,1,2],#two
                        [2,1,0,1,0,0],#two
                        [0,1,0,0,1,2],#two
                        [2,1,0,0,1,0],#two
                        [0,0,1,0,0,0],#free one
                        [0,0,0,1,0,0],#free one
                        [2,1,1,1,1,2],#Deadfour
                    ]

        self.score_6 = [100000000,10000000,10000000,500000,500000,500000,500000,500000,500000,100000,100000,100000,100000,500,500,500,500,500,500,50,50,5,5,5,5,5,5,1,1,0]
        self.one_5 = [  [1,1,1,1,1], #win
                        [1,1,1,1,0],#four
                        [0,1,1,1,1],#four
                        [0,1,1,1,0],#straight three
                        [1,0,0,1,1],#three
                        [1,1,0,0,1],#three
                        [1,0,1,0,1],#three
                        [0,1,0,1,0], #two
                        [1,0,0,0,1],#two
                        [2,1,1,1,2],#deadthree
                        [2,1,1,2,0],#deadtwo
                        [0,2,1,1,2],#deadtwo
                    ]
        self.score_5 = [10000000,10000,10000,100000,500,500,500,5,5,0,0,0]

        self.two_6 = [  [0,2,2,2,2,2],
                        [2,2,2,2,2,0],
                        [0,2,2,2,2,0],#straight four
                        [0,2,0,2,2,2],#four
                        [2,2,2,0,2,0],#four
                        [0,2,2,0,2,2],#four
                        [2,2,0,2,2,0],#four
                        [0,2,2,2,0,2],#four
                        [2,0,2,2,2,0],#four
                        [0,1,1,1,0,0],#straight three
                        [0,0,1,1,1,0],#straight three
                        [0,2,0,2,2,0],#straight three
                        [0,2,2,0,2,0],#straight three
                        [1,2,2,2,0,0],#three
                        [0,0,2,2,2,1],#three
                        [1,2,2,0,2,0],#three
                        [0,2,0,2,2,1],#three
                        [0,2,2,0,2,1],#three
                        [1,2,0,2,2,0],#three
                        [0,0,2,2,0,0],#straight two
                        [0,2,0,0,2,0],#straight two
                        [0,0,0,2,2,1],
                        [1,2,2,0,0,0],
                        [0,0,2,0,2,1],
                        [1,2,0,2,0,0],
                        [0,2,0,0,2,1],
                        [1,2,0,0,2,0],
                        [0,0,2,0,0,0],#free one
                        [0,0,0,2,0,0],#free one
                        [1,2,2,2,2,1],#Deadfour
                    ]
        self.two_5 = [  [2,2,2,2,2],
                        [2,2,2,2,0],
                        [0,2,2,2,2],
                        [0,2,2,2,0],
                        [2,0,0,2,2],#three
                        [2,2,0,0,2],#three
                        [2,0,2,0,2],#three
                        [0,2,0,2,0], #two
                        [2,0,0,0,2],#two
                        [1,2,2,2,1],#deadthree
                        [1,2,2,1,0],#deadtwo
                        [0,1,2,2,1],#deadtwo
                    ]



    def get(self, row, col):
        '''
            Get the value at a given row,col position.
            Used to prevent accidental out of bounds access.
        '''
        if row < 0 or row >= self.__size or col < 0 or col >= self.__size:
            return 0
        return self.__board[row][col]

    def has_neighbor(self, row, col):
        '''Check whether a given row,col index has any neighboring game piece'''
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]
        if self.__board[row][col] != 0:
            return False
        for (xdirection, ydirection) in directions:
            if xdirection != 0 and ((col + xdirection) < 0 or (col + xdirection) >= self.__size):
                continue
            if ydirection != 0 and ((row + ydirection) < 0 or (row + ydirection) >= self.__size):
                continue
            if self.__board[row + ydirection][col + xdirection] != 0:
                # print(f"neighbor at [{row}][{col}]")
                return True
        return False

    def size(self):
        '''Return game board dimensions'''
        return self.__size

    def player_turn(self):
        '''Return player turn'''
        return self.__player_turn

    def board(self):
        '''Return the board array.'''
        return self.__board

    
    def window(self,iterable, size=5):
        '''sliding window to create a set of iterable vectors'''
        i = iter(iterable)
        window = []
        for j in range(0, size):
            window.append(next(i))
        yield window
        for j in i:
            window = window[1:] + [j]
            yield window

    #Window sliding algorithm
    def evaluate_vector(self, vector):
        '''
            Calculate the score of a sequence of gamepieces
            Returns: score values for both player 1 and player 2
        '''
        score = {'one': 0, 'two': 0}
        count_one = 0
        count_two = 0

        #Check through the combinations of 5 pieces, and determine the score of the vector
        if len(vector) == 5:
            for i in range(len(self.one_5)):
                if self.one_5[i] == vector:
                    score['one'] += self.score_5[i] * 1
                if self.two_5[i] == vector:
                    score['two'] += self.score_5[i] * 1
            return score

        mygenerator = list(self.window(vector,5))

        #check through the combinations of 5 consecutive pieces, and determine the score of the vector
        for i in mygenerator:
            for j in range(len(self.one_5)):
                if i==self.one_5[j]:
                    score['one'] += self.score_5[j] * len(mygenerator) + len(mygenerator)
                if i==self.two_5[j]:
                    score['two'] += self.score_5[j] * len(mygenerator) + len(mygenerator)

        mygenerator = list(self.window(vector, 6))

        #check through the combinations of 6 consecutive pieces, and determine the score of the vector
        for i in mygenerator:
            for j in range(len(self.one_6)):
                if i==self.one_6[j]:
                    score['one'] += self.score_6[j] * len(mygenerator) + len(mygenerator)
                if i==self.two_6[j]:
                    score['two'] += self.score_6[j] * len(mygenerator) + len(mygenerator)

        return score


    def evaluate_board_score(self):
        '''
            Given a boardstate, calculates the boardscore.
            Score is a numerical value to determine which player is in an advantageous state.
        '''
        vectors = []
        board_score = 0

        #Look through vertical and horizontal lines
        for i in range(self.__size):
            vectors.append(self.__ghost_board[i])
        for j in range(0,self.__size):
            vectors.append(list(self.__ghost_board[x][j] for x in range(self.__size)))


        #Look through the 2 diagonal lines extending from the corner
        vectors.append(list(self.__ghost_board[x][x] for x in range(self.__size)))
        vectors.append(list(self.__ghost_board[x][self.__size - x - 1] for x in range(self.__size)))

        #Look through the rest of the diagonal lines with length >= 5, if applicable
        if self.__size >= 6:
            for i in range(1, self.__size - 4):
                vectors.append(list(self.__ghost_board[row][row - i] for row in range (i, self.__size)))
                vectors.append(list(self.__ghost_board[col - i][col] for col in range(i, self.__size)))

            for i in range(4, self.__size - 1):
                vectors.append(list(self.__ghost_board[i - x][x] for x in range(i, -1, -1)))
                vectors.append(list(self.__ghost_board[self.__size - 1 - x][self.__size - 1 - (i - x)] for x in range(i, -1, -1)))


        for v in vectors:
            mygenerator = list(self.window(v))
            score = self.evaluate_vector(v)
            board_score += score['one'] - score['two']
        return board_score



    def find_choices(self):
        '''
            Returns list of moves the AI will consider.
            In order to reduce runtime, AI will only consider empty spots that are neighboring with a filled slot.
        '''
        choices = []
        for i in range(self.__size):
            for j in range(self.__size):
                if self.__board[i][j] != 0:
                    continue
                if not self.has_neighbor(i,j):
                    continue
                choices.append((i,j))
        return choices


    def add_new_choices(self, choice, existing_choices):
        '''
            Upon making a new move, returns a list of additional moves the AI may consider
        '''
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]
        additional_choices = []
        if choice is not None:
            for (xdirection, ydirection) in directions:
                if xdirection != 0 and ((choice[1] + xdirection) < 0 or (choice[1] + xdirection) >= self.__size):
                    continue
                if ydirection != 0 and ((choice[0] + ydirection) < 0 or (choice[0] + ydirection) >= self.__size):
                    continue
                if (self.__board[choice[0] + ydirection][choice[1] + xdirection] == 0) and (choice[0] + ydirection, choice[1] + xdirection) not in existing_choices:
                    additional_choices.append((choice[0] + ydirection, choice[1] + xdirection))
        return additional_choices



    def minimax(self,choices, depth, max_depth, alpha, beta, max_player, temp_choice = None, store_choice = None):
        '''
            Minimax algorithm with depth = 2 and alpha beta pruning to search for the ideal move to make.
            Recursively searches a game tree of possible board states, 
            and finds the board state that is most advantageous to the AI.
        '''

        #Grab list of possible choices to make
        new_choices = choices.copy()
        if max_player == 1:
            next_player = 2
        else:
            next_player = 1
        #Make a move into the ghost board
        self.make_ghost_move(temp_choice, next_player)

        #Once we reach the bottom of the search tree,
        #determine its board score along with the next choice the AI has to make to reach this score
        if depth == 0: #or win
            score = self.evaluate_board_score()
            self.remove_ghost_move(temp_choice)
            val = {'choice':store_choice, 'score':score}
            return val

        #Because we made a move in the ghost board at temp_choice, that block will no longer be available 
        if temp_choice is not None:
            new_choices.remove(temp_choice)
        new_choices.extend(self.add_new_choices(temp_choice, new_choices))
        new_choice = None

        #AI wants to maximize the gain
        if max_player == 1:
            maxVal = float("-inf")
            for choice in new_choices:
                #If we're at the top node, save our immediate next move into store_choice
                #so that we can retrieve it when the AI has decided its next move
                if depth == max_depth:
                    store_choice = choice
                #Traverse down a node of the search tree
                val = self.minimax(new_choices, depth - 1, max_depth, alpha, beta, 2, choice, store_choice)
                self.remove_ghost_move(temp_choice)

                #If we find a new maximum, update its value
                if val['score'] >= maxVal:
                    # print("")
                    # print("NEW MAX VAL", val['score'], maxVal)
                    # print("")
                    # print("larger choice taken between", val['score'], maxVal)
                    maxVal = val['score']
                    new_choice = val['choice']
                alpha = max(alpha, val['score'])

                #Alpha beta pruning states that all proceeding choices will be worse than the current best choice we have.
                #Therefore we stop evaluating this branch
                if beta <= alpha:
                    break
            # print(f"Final choice returned: ({new_choice}) score:{maxVal})")
            return {'choice':new_choice, 'score':maxVal}

        #Player wants to minimize the gain
        else:
            minVal = float("inf")
            for choice in new_choices:
                # new_choices.remove(choice)
                #Traverse down a node of the search tree
                val = self.minimax(new_choices, depth - 1, max_depth, alpha, beta, 1, choice, store_choice)
                if val['score'] <= minVal:
                    # print("smaller choice taken between", val['score'], minVal)
                    minVal = val['score']
                    new_choice = val['choice']
                beta = min(beta, val['score'])

                #Alpha beta pruning states that all proceeding choices will be worse than the current best choice we have.
                #Therefore we stop evaluating this branch
                if beta <= alpha:
                    self.remove_ghost_move(temp_choice)
                    break
            self.remove_ghost_move(temp_choice)
            # print(f"Smallest choice returned: ({new_choice}) score:{minVal})")
            return {'choice':new_choice, 'score':minVal}

    def make_move(self, row, col):
        '''
            Makes a move by filling in the slot at row,col
            Also resets ghost board to newest state of game board
        '''
        self.__board[row][col] = self.__player_turn
        self.__ghost_board = self.__board.copy()
        self.__player_turn = (self.__player_turn % 2) + 1

        self.printBoard()


    def make_ghost_move(self, choice, player_turn):
        '''
            Makes a move into the ghost_board
            Argument for player turn is required unlike make_move, 
            because minimax searches with depth = 2 meaning that ghost board can represent 
            board states up to 2 moves ahead.
        '''
        if choice is not None:
            self.__ghost_board[choice[0]][choice[1]] = player_turn

            # self.print_ghost_board()
 
            # print("")
            # print(f"GHOST MOVE: ({choice[0]}, {choice[1]})")


    def remove_ghost_move(self, choice):
        '''
            Erase a filled slot on the ghost board
        '''
        if choice is not None:
            self.__ghost_board[choice[0]][choice[1]] = 0

    def choose_move(self):
        '''
            Call onto minimax algorithm to find the optimal move for AI
        '''
        choices = self.find_choices()
        val = self.minimax(choices, depth=2, max_depth=2, alpha=-1000000000, beta=1000000000, max_player=1)
        return val

    def check(self):
        '''
            Check if there is a winner.
            Output: 0 if no winner, winning player's number (1,2) if there's a winner
        '''
        board = self.__board
        # check in 4 directions: down-left, down, down-right, right
        dirs = ((1, -1), (1, 0), (1, 1), (0, 1))
        for i in range(self.__size):
            for j in range(self.__size):
                if board[i][j] == 0:
                    continue
                player_num = board[i][j]
                # check if there exist 5 in a line
                for d in dirs:
                    x, y = i, j
                    count = 0
                    for _ in range(5):
                        if self.get(x, y) != player_num:
                            break
                        x += d[0]
                        y += d[1]
                        count += 1
                    # if 5 in a line, store positions of all stones, return value
                    if count == 5:
                        return player_num
        return 0


    def printBoard(self):
        '''
            Prints the board for debugging purposes
        '''
        val = '0'
        print("")
        print("A B C D E F G H I J K L M N O", end="")
        for i in range(self.__size):
            print("")
            for j in range(self.__size):
                if self.__board[i][j] == 0:
                    val = '0'
                elif self.__board[i][j] == 1:
                    val = '1'
                elif self.__board[i][j] == 2:
                    val = '2'
                print(f"{val}", end =" ")
            print(f" {i+1}", end="")

    # def print_ghost_board(self):
    #     val = '0'
    #     for i in range(self.__size):
    #         print("")
    #         for j in range(self.__size):
    #             if self.ghost_board[i][j] == 0:
    #                 val = '0'
    #             elif self.ghost_board[i][j] == 1:
    #                 val = '1'
    #             elif self.ghost_board[i][j] == 2:
    #                 val = '2'
    #             print(f"{val}", end =" ")
