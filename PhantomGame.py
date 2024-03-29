from PhantomLogic import Board

class PhantomGame():
    """
    This class specifies the base Game class. To define your own game, subclass
    this class and implement the functions below. This works when the game is
    two-player, adversarial and turn-based.

    Use 1 for player1 and -1 for player2.

    See othello/OthelloGame.py for an example implementation.
    """
    def __init__(self):
        print("init")
        self.board = Board()

    def getInitBoard(self):
        """
        Returns:
            startBoard: a representation of the board (ideally this is the form
                        that will be the input to your neural network)
        """
        print("getInitBoard")
        player, pieces = self.board.get_next_question()
        return pieces

    def getBoardSize(self):
        """
        Returns:
            (x,y): a tuple of board dimensions
        """
        print("getBoardSize")
        return 9,9

    def getActionSize(self):
        """
        Returns:
            actionSize: number of all possible actions
        """
        print("getActionSize")
        return self.board.action_size

    def getNextState(self, board, player, action, first=False):
        """
        Input:
            board: current board
            player: current player (1 or -1)
            action: action taken by current player

        Returns:
            nextBoard: board after applying action
            nextPlayer: player who plays in the next turn (should be -player)
        """
        print("getNextState", player)
        if (first):
            self.board.set_answer(action, player)
            print("answered: ", action)
            ret = self.board.get_next_question()
            print(ret)
        else:
            ret = self.board.pieces, self.board.next_player
        return ret

    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        print("getValidMoves")
        return [1] * self.board.valid_actions + [0] * (self.board.action_size - self.board.valid_actions)

    def getGameEnded(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw.
               
        """
        print("getGameEnded")
        return self.board.has_game_ended()

    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """
        print("getCanonicalForm")
        return self.board.pieces

    def getSymmetries(self, board, pi):
        """
        Input:
            board: current board
            pi: policy vector of size self.getActionSize()

        Returns:
            symmForms: a list of [(board,pi)] where each tuple is a symmetrical
                       form of the board and the corresponding pi vector. This
                       is used when training the neural network from examples.
        """
        print("getSymmetries")
        return [(board, pi)]

    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        return '\n'.join('\t'.join('%0.3f' %x for x in y) for y in board)
