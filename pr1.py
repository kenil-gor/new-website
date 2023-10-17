import math
import random

class StateNode:
    def __init__(self, board, player):
        self.board = board
        self.player = player

    def get_score_value(self):
        if self.is_win():
            return -1 if self.player == 'X' else 1
        return 0

    def is_valid_move(self, pos):
        return self.board[pos] == ' '

    def is_game_over(self):
        return self.is_win() or self.is_draw()

    def draw_board(self):
        for i in range(0, 9, 3):
            print("|".join(self.board[i:i + 3]))
            if i < 6:
                print("-" * 5)

    def get_empty_cells(self):
        return [i for i in range(9) if self.is_valid_move(i)]

    def set_move(self, pos, player):
        self.board[pos] = player

    def is_win(self):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        for combination in winning_combinations:
            if self.board[combination[0]] == self.board[combination[1]] == self.board[combination[2]] != ' ':
                return True
        return False

    def is_draw(self):
        return len(self.get_empty_cells()) == 0


class TicTacToe:
    def __init__(self, player_marker, computer_marker, first_turn):
        self.state = StateNode([' ' for _ in range(9)], first_turn)
        self.player_marker = player_marker
        self.computer_marker = computer_marker

    def alphabeta(self, state, depth, alpha, beta, maximizing_player):
        if depth == 0 or state.is_game_over():
            return state.get_score_value(), None

        if maximizing_player:
            value, move = -math.inf, None
            for pos in state.get_empty_cells():
                state.set_move(pos, self.computer_marker)
                new_val, _ = self.alphabeta(StateNode(state.board, 'X'), depth - 1, alpha, beta, False)
                state.set_move(pos, ' ')
                if new_val > value:
                    value, move = new_val, pos
                    alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, move
        else:
            value, move = math.inf, None
            for pos in state.get_empty_cells():
                state.set_move(pos, self.player_marker)
                new_val, _ = self.alphabeta(StateNode(state.board, 'O'), depth - 1, alpha, beta, True)
                state.set_move(pos, ' ')
                if new_val < value:
                    value, move = new_val, pos
                    beta = min(beta, value)
                if alpha >= beta:
                    break
            return value, move

    def computer_move(self):
        if len(self.state.get_empty_cells()) == 9:
            pos = random.randint(0, 8)
        else:
            _, pos = self.alphabeta(self.state, 9, -math.inf, math.inf, True)
        self.state.set_move(pos, self.computer_marker)

    def player_move(self, pos):
        return self.state.is_valid_move(pos) and self.state.set_move(pos, self.player_marker) is None

    def execution(self):
        self.state.draw_board()

        while not self.state.is_game_over():
            if self.state.player == 'P':
                try:
                    pos = int(input("Enter your move (0-8): "))
                    if 0 <= pos <= 8 and self.player_move(pos):
                        self.state.draw_board()
                        if self.state.is_game_over():
                            break
                        self.state.player = 'C'
                except ValueError:
                    print("Invalid input, please enter a number between 0-8.")
            else:
                print("Computer's move:")
                self.computer_move()
                self.state.draw_board()
                if self.state.is_game_over():
                    break
                self.state.player = 'P'

        if self.state.is_win():
            winner = "Player" if self.state.player == 'C' else "Computer"
            print(f"{winner} ({self.player_marker if winner == 'Player' else self.computer_marker}) wins!")
        else:
            print("It's a draw!")

if __name__ == "__main__":
    player_marker = input("Choose your marker (X or O): ").upper()
    while player_marker not in {'X', 'O'}:
        player_marker = input("Invalid marker. Choose your marker (X or O): ").upper()
        computer_marker = 'O' if player_marker == 'X' else 'X'
        first_turn = input("Who goes first? (P for player, C for computer): ").upper()
    while first_turn not in {'P', 'C'}:
        first_turn = input("Invalid choice. Who goes first? (P for player, C for computer): ").upper()

    game = TicTacToe(player_marker, computer_marker, first_turn)
    game.execution()
