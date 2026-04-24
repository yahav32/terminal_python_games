#create me a tic tac toe game 

class TicTacToe:
    def __init__(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_over = False
    
    def print_board(self):
        for row in self.board:
            print("|".join(row))
    
    def check_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != " ":
                return row[0]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != " ":
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != " ":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != " ":
            return self.board[0][2]
        return None
    
    def make_move(self, row, col):
        if self.board[row][col] == " " and not self.game_over:
            self.board[row][col] = self.current_player
            winner = self.check_winner()
            if winner:
                print(f"Player {winner} wins!")
                self.game_over = True
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
        else:
            print("Invalid move!")
    
    def play(self):
        while not self.game_over:
            self.print_board()
            try:
                move = input(f"Player {self.current_player}, enter your move (row, col): ").split(",")
                row = int(move[0])
                col = int(move[1])
                self.make_move(row, col)
            except (ValueError, IndexError):
                print("Invalid input!")
            except KeyboardInterrupt:
                print("[CTRL+C] Game Over")
                break
        self.print_board()
        print("Game Over")

if __name__ == "__main__":
    game = TicTacToe()
    game.play()