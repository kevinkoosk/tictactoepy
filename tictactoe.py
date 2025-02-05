import tkinter as tk
from tkinter import messagebox

class ReversingTicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Reversing Tic Tac Toe")
        
        # Game state variables
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.move_history = []
        self.special_tokens = {'X': 3, 'O': 3}
        self.game_over = False
        
        # Configure grid weights for resizing
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create GUI elements
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        # Control frame
        control_frame = tk.Frame(self.root)
        control_frame.grid(row=0, column=0, sticky='ew')
        
        self.status_label = tk.Label(control_frame, text="", font=('Arial', 14))
        self.status_label.pack(side='left', padx=10)
        
        self.special_token_btn = tk.Button(control_frame, text="Use Special Token (3)", 
                                         command=self.use_special_token)
        self.special_token_btn.pack(side='right', padx=10)
        
        new_game_btn = tk.Button(control_frame, text="New Game", command=self.new_game)
        new_game_btn.pack(side='right', padx=10)
        
        # Game board
        self.board_frame = tk.Frame(self.root, bg='black')
        self.board_frame.grid(row=1, column=0, sticky='nsew')
        
        # Create buttons for the game board
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(self.board_frame, text='', font=('Arial', 40), 
                              command=lambda i=i, j=j: self.make_move(i, j),
                              width=3, height=1)
                btn.grid(row=i, column=j, sticky='nsew', padx=2, pady=2)
                row.append(btn)
            self.buttons.append(row)
            
        # Configure board grid weights for resizing
        for i in range(3):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)

    def update_display(self):
        self.status_label.config(text=f"Player {self.current_player}'s Turn")
        token_count = self.special_tokens[self.current_player]
        self.special_token_btn.config(
            text=f"Use Special Token ({token_count})",
            state=tk.NORMAL if token_count > 0 and not self.game_over else tk.DISABLED
        )

    def make_move(self, row, col):
        if self.board[row][col] == '' and not self.game_over:
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            self.move_history.append((row, col))
            
            if self.check_win():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.game_over = True
            elif self.check_tie():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.game_over = True
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.update_display()

    def use_special_token(self):
        if len(self.move_history) >= 2 and self.special_tokens[self.current_player] > 0:
            self.special_tokens[self.current_player] -= 1
            
            # Undo last two moves
            for _ in range(2):
                if self.move_history:
                    row, col = self.move_history.pop()
                    self.board[row][col] = ''
                    self.buttons[row][col].config(text='')
            
            self.update_display()

    def check_win(self):
        # Check rows, columns, and diagonals
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return True
        return False

    def check_tie(self):
        return all(cell != '' for row in self.board for cell in row)

    def new_game(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.move_history = []
        self.special_tokens = {'X': 3, 'O': 3}
        self.game_over = False
        
        for row in self.buttons:
            for btn in row:
                btn.config(text='')
                
        self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    game = ReversingTicTacToe(root)
    root.mainloop()
