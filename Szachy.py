import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class ChessGameApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Chess - Game")
        self.configure_window()
        self.create_controls()
        self.setup_game()
        self.white_time = 0
        self.black_time = 0
        self.timer_running = False
        self.current_timer = None
        self.game_mode = None 
        self.player_names = {'white': 'White', 'black': 'Black'}

    def configure_window(self):
        self.BOARD_SIZE = 8
        self.SQUARE_SIZE = 70
        self.WIDTH = self.BOARD_SIZE * self.SQUARE_SIZE + 200
        self.HEIGHT = self.BOARD_SIZE * self.SQUARE_SIZE
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.resizable(False, False)

    def create_controls(self):
        self.menu_frame = tk.Frame(
            self.root,
            background="#333333"
        )
        self.menu_frame.pack(fill="both", expand=True)
        title = tk.Label(
            self.menu_frame,
            text="CHESS",
            font=("Arial", 40, "bold"),
            foreground="#FFFFFF",   
            background="#333333"   
        )
        title.pack(pady=30)
        btn_style = {
            "font": ("Arial", 18),
            "width": 20,
            "height": 2
        }
        tk.Button(self.menu_frame, text="Two Players", 
                  command=self.start_two_player_game, **btn_style).pack(pady=10)
        tk.Button(self.menu_frame, text="Play vs Computer", 
                  command=self.start_computer_game, **btn_style).pack(pady=10)
        tk.Button(self.menu_frame, text="Rules", 
                  command=self.show_rules, **btn_style).pack(pady=10)
        tk.Button(self.menu_frame, text="Exit", 
                  command=self.root.quit, **btn_style).pack(pady=10)
        chess_piece = tk.Label(
            self.menu_frame,
            text="Chess_Game",
            foreground="#FF0000",   
            background="#00FF00",    
            font=("Arial", 20)
        )
        chess_piece.pack(pady=20)
        
        self.canvas = tk.Canvas(
            self.root,
            width=self.BOARD_SIZE * self.SQUARE_SIZE,
            height=self.BOARD_SIZE * self.SQUARE_SIZE,
            background="#FFFFFF"
        )
        self.info_panel = tk.Frame(
            self.root,
            background="#F0F0F0",
            width=180,
            height=self.HEIGHT
        )
        self.info_label = tk.Label(
            self.info_panel,
            text="Turn: White",
            font=("Arial", 16),
            foreground="#000000",
            background="#F0F0F0"
        )
        self.info_label.pack(pady=20)
        self.timer_label = tk.Label(
            self.info_panel,
            text="White Time: 00:00",
            font=("Arial", 14),
            foreground="#222222",
            background="#F0F0F0"
        )
        self.timer_label.pack(pady=5)

    def setup_game(self):
        self.pieces = {
            'white': {'king': '♔', 'queen': '♕', 'rook': '♖', 'bishop': '♗', 'knight': '♘', 'pawn': '♙'},
            'black': {'king': '♚', 'queen': '♛', 'rook': '♜', 'bishop': '♝', 'knight': '♞', 'pawn': '♟'}
        }        
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.selected_piece = None
        self.selected_pos = None
        self.current_turn = 'white'
        self.game_running = False
        self._setup_pieces()       
        self.canvas.bind("<Button-1>", self.on_square_click)

    def _setup_pieces(self):
        order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']   
        for col in range(8):
            self.board[0][col] = ('black', order[col])
            self.board[1][col] = ('black', 'pawn')   
        for col in range(8):
            self.board[7][col] = ('white', order[col])
            self.board[6][col] = ('white', 'pawn')

    def start_two_player_game(self):
        self.game_mode = '2players'
        white_name = simpledialog.askstring("Player Names", "Enter name for White player:")
        black_name = simpledialog.askstring("Player Names", "Enter name for Black player:")
        if white_name and white_name.strip():
            self.player_names['white'] = white_name.strip()
        if black_name and black_name.strip():
            self.player_names['black'] = black_name.strip()
        self.start_new_game()

    def start_computer_game(self):
        self.game_mode = 'computer'
        white_name = simpledialog.askstring("Player Name", "Enter your name (you play as White):")
        if white_name and white_name.strip():
            self.player_names['white'] = white_name.strip()
        self.player_names['black'] = "Computer"
        self.start_new_game()

    def start_new_game(self):
        self.menu_frame.pack_forget()
        self.info_panel.pack(side="right", fill="y")
        self.canvas.pack(side="left")
        self.game_running = True      
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.selected_piece = None
        self.selected_pos = None
        self.current_turn = 'white'
        self.info_label.config(text=f"Turn: {self.player_names['white']}")
        self._setup_pieces()
        self.draw_board()
        self.white_time = 0
        self.black_time = 0
        self.update_timer_display()
        self.start_timer('white')

    def start_timer(self, player):
        self.timer_running = True
        self.current_timer = player
        self._count_time()

    def stop_timer(self):
        self.timer_running = False

    def _count_time(self):
        if not self.timer_running:
            return
        if self.current_timer == 'white':
            self.white_time += 1
        elif self.current_timer == 'black':
            self.black_time += 1
        self.update_timer_display()
        self.root.after(1000, self._count_time)

    def update_timer_display(self):
        w_min = self.white_time // 60
        w_sec = self.white_time % 60
        b_min = self.black_time // 60
        b_sec = self.black_time % 60
        if self.current_timer == 'white':
            self.timer_label.config(text=f"{self.player_names['white']} Time: {w_min:02d}:{w_sec:02d}")
        elif self.current_timer == 'black':
            self.timer_label.config(text=f"{self.player_names['black']} Time: {b_min:02d}:{b_sec:02d}")

    def draw_board(self):
        self.canvas.delete("all")        
        for row in range(8):
            for col in range(8):
                color = "#F0D9B5" if (row + col) % 2 == 0 else "#B58863"
                x1 = col * self.SQUARE_SIZE
                y1 = row * self.SQUARE_SIZE
                x2 = x1 + self.SQUARE_SIZE
                y2 = y1 + self.SQUARE_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                if self.selected_pos == (row, col):
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#82B1FF", outline="", stipple="gray50")              
                piece = self.board[row][col]
                if piece:
                    color, name = piece
                    symbol = self.pieces[color][name]
                    if color == "white":
                        for dx, dy in [(-0.8, 0), (0.8, 0), (0, -0.8), (0, 0.8)]:
                            self.canvas.create_text(
                                x1 + self.SQUARE_SIZE / 2 + dx,
                                y1 + self.SQUARE_SIZE / 2 + dy,
                                text=symbol,
                                font=("Arial", 36),
                                fill="#000000"
                            )
                        self.canvas.create_text(
                            x1 + self.SQUARE_SIZE / 2,
                            y1 + self.SQUARE_SIZE / 2,
                            text=symbol,
                            font=("Arial", 36),
                            fill="#FFFFFF"
                        )
                    else:
                        for dx, dy in [(-0.8, 0), (0.8, 0), (0, -0.8), (0, 0.8)]:
                            self.canvas.create_text(
                                x1 + self.SQUARE_SIZE / 2 + dx,
                                y1 + self.SQUARE_SIZE / 2 + dy,
                                text=symbol,
                                font=("Arial", 36),
                                fill="#FFFFFF"
                            )
                        self.canvas.create_text(
                            x1 + self.SQUARE_SIZE / 2,
                            y1 + self.SQUARE_SIZE / 2,
                            text=symbol,
                            font=("Arial", 36),
                            fill="#222222"
                        )

    def on_square_click(self, event):
        if not self.game_running:
            return
        if self.game_mode == 'computer' and self.current_turn == 'black':
            return       
        col = event.x // self.SQUARE_SIZE
        row = event.y // self.SQUARE_SIZE
        if self.selected_piece is None:
            piece = self.board[row][col]
            if piece and piece[0] == self.current_turn:
                self.selected_piece = piece
                self.selected_pos = (row, col)
        else:
            if self.selected_pos == (row, col):
                self.selected_piece = None
                self.selected_pos = None
            else:
                if self.is_valid_move(self.selected_pos, (row, col)):
                    self.move_piece(self.selected_pos, (row, col))
                    self.after_move()          
                self.selected_piece = None
                self.selected_pos = None
        self.draw_board()

    def after_move(self):
        """Actions after a move: switch turn, check game end, computer move"""
        self.stop_timer()
        if self.current_turn == 'white':
            self.current_turn = 'black'
            self.start_timer('black')
        else:
            self.current_turn = 'white'
            self.start_timer('white')
        self.info_label.config(text=f"Turn: {self.player_names[self.current_turn]}")                
        if self.is_checkmate():
            winner = self.player_names['black'] if self.current_turn == 'white' else self.player_names['white']
            messagebox.showinfo("Game Over", f"Checkmate! {winner} wins!")
            self.game_running = False
            self.stop_timer()
            return
        if self.game_mode == 'computer' and self.current_turn == 'black' and self.game_running:
            self.root.after(800, self.computer_move)

    def computer_move(self):
        """Simple computer AI: picks a random valid move"""
        all_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece[0] == 'black':
                    for to_row in range(8):
                        for to_col in range(8):
                            if self.is_valid_move((row, col), (to_row, to_col)):
                                all_moves.append( ((row, col), (to_row, to_col)) )
        if all_moves:
            from_pos, to_pos = random.choice(all_moves)
            self.move_piece(from_pos, to_pos)
            self.after_move()
            self.draw_board()

    def is_valid_move(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        piece = self.board[from_row][from_col]
        if not piece:
            return False
        color, ptype = piece
        target = self.board[to_row][to_col]   
        if target and target[0] == color:
            return False
        dr = to_row - from_row
        dc = to_col - from_col
        abs_dr = abs(dr)
        abs_dc = abs(dc)
        if ptype == 'pawn':
            direction = -1 if color == 'white' else 1         
            if dc == 0 and dr == direction and not target:
                return True         
            if dc == 0 and dr == 2 * direction and not target and \
               ((color == 'white' and from_row == 6) or (color == 'black' and from_row == 1)) and \
               not self.board[from_row + direction][from_col]:
                return True        
            if abs_dc == 1 and dr == direction and target:
                return True
        elif ptype == 'rook':
            if (dr == 0 or dc == 0) and self.is_path_clear(from_pos, to_pos):
                return True
        elif ptype == 'knight':
            if (abs_dr == 2 and abs_dc == 1) or (abs_dr == 1 and abs_dc == 2):
                return True
        elif ptype == 'bishop':
            if abs_dr == abs_dc and self.is_path_clear(from_pos, to_pos):
                return True
        elif ptype == 'queen':
            if (dr == 0 or dc == 0 or abs_dr == abs_dc) and self.is_path_clear(from_pos, to_pos):
                return True
        elif ptype == 'king':
            if abs_dr <= 1 and abs_dc <= 1:
                return True
        return False

    def is_path_clear(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        dr = 0 if to_row == from_row else (to_row - from_row) // abs(to_row - from_row)
        dc = 0 if to_col == from_col else (to_col - from_col) // abs(to_col - from_col)
        row, col = from_row + dr, from_col + dc
        while (row, col) != (to_row, to_col):
            if self.board[row][col] is not None:
                return False
            row += dr
            col += dc
        return True

    def move_piece(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = None

    def is_checkmate(self):
        kings = {'white': False, 'black': False}
        for row in self.board:
            for piece in row:
                if piece and piece[1] == 'king':
                    kings[piece[0]] = True
        return not kings['white'] or not kings['black']

    def show_rules(self):
        rules = """
        Basic Rules:
        - White moves first
        - Each piece moves according to its own rules
        - King: 1 square in any direction
        - Queen: any number of squares in any direction
        - Rook: straight (horizontal/vertical)
        - Bishop: diagonally
        - Knight: in L-shape (2 + 1)
        - Pawn: forward, captures diagonally
        Goal: Checkmate – trap the opponent's king so it cannot escape.
        """
        messagebox.showinfo("Game Rules", rules)


def main():
    root = tk.Tk()
    app = ChessGameApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()