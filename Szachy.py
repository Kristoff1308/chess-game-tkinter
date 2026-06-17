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
        self.difficulty = 'easy'
        self.player_names = {'white': 'White', 'black': 'Black'}
        self.piece_values = {'pawn': 1, 'knight': 3, 'bishop': 3, 'rook': 5, 'queen': 9, 'king': 100}
        self.piece_moved = {'white': {'king': False, 'rook_a': False, 'rook_h': False},
                            'black': {'king': False, 'rook_a': False, 'rook_h': False}}
        self.en_passant_target = None
        self.bg_image = None

    def configure_window(self):
        self.BOARD_SIZE = 8
        self.SQUARE_SIZE = 70
        self.WIDTH = self.BOARD_SIZE * self.SQUARE_SIZE + 200
        self.HEIGHT = self.BOARD_SIZE * self.SQUARE_SIZE
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.resizable(False, False)

    def create_controls(self):
        self.menu_frame = tk.Frame(self.root, bg="#1a1a2e")
        self.menu_frame.pack(fill="both", expand=True)
        title = tk.Label(
            self.menu_frame, text="CHESS", font=("Arial", 40, "bold"),foreground="#FFFFFF",background="#1a1a2e",borderwidth=0, relief="flat" )
        title.pack(pady=20)
        diff_frame = tk.Frame(self.menu_frame, bg="#1a1a2e", borderwidth=0, relief="flat")
        diff_frame.pack(pady=10)
        tk.Label(diff_frame, text="Difficulty Level:", font=("Arial", 14), fg="white", bg="#1a1a2e",borderwidth=0 ).grid(row=0, column=0, padx=5)
        self.diff_var = tk.StringVar(value="easy")
        tk.Radiobutton(diff_frame,text="Easy",variable=self.diff_var,value="easy",font=("Arial", 12),bg="#1a1a2e",fg="white",selectcolor="#33334e", borderwidth=0,relief="flat",activebackground="#1a1a2e").grid(row=0, column=1)
        tk.Radiobutton(diff_frame,text="Medium",variable=self.diff_var,value="medium",font=("Arial", 12),bg="#1a1a2e",fg="white",selectcolor="#33334e", borderwidth=0, relief="flat", activebackground="#1a1a2e" ).grid(row=0, column=2)
        tk.Radiobutton(diff_frame,text="Hard",variable=self.diff_var,value="hard",font=("Arial", 12),bg="#1a1a2e",fg="white",selectcolor="#33334e",borderwidth=0,relief="flat", activebackground="#1a1a2e").grid(row=0, column=3)
        btn_style = {"font": ("Arial", 18),"width": 20,"height": 2,"borderwidth": 0,"relief": "flat"}
        tk.Button(self.menu_frame, text="Two Players", command=self.start_two_player_game, **btn_style).pack(pady=10)
        tk.Button(self.menu_frame, text="Play vs Computer", command=self.start_computer_game, **btn_style).pack(pady=10)
        tk.Button(self.menu_frame, text="Rules",command=self.show_rules, **btn_style).pack(pady=10)
        tk.Button(self.menu_frame, text="Exit", command=self.root.quit, **btn_style).pack(pady=10)       
        self.canvas = tk.Canvas(
            self.root,
            width=self.BOARD_SIZE * self.SQUARE_SIZE,
            height=self.BOARD_SIZE * self.SQUARE_SIZE,
            background="#FFFFFF")
        self.info_panel = tk.Frame(
            self.root,background="#F0F0F0",width=180,height=self.HEIGHT)
        self.info_label = tk.Label(
            self.info_panel,text="Turn: White",font=("Arial", 16),foreground="#000000",background="#F0F0F0")
        self.info_label.pack(pady=20)
        self.timer_label = tk.Label(
            self.info_panel,text="White Time: 00:00",font=("Arial", 14),foreground="#222222",background="#F0F0F0")
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
        self.piece_moved = {'white': {'king': False, 'rook_a': False, 'rook_h': False},
                            'black': {'king': False, 'rook_a': False, 'rook_h': False}}
        self.en_passant_target = None

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
        self.difficulty = self.diff_var.get()
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
        self.piece_moved = {'white': {'king': False, 'rook_a': False, 'rook_h': False},
                            'black': {'king': False, 'rook_a': False, 'rook_h': False}}
        self.en_passant_target = None

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
                                text=symbol,font=("Arial", 36),fill="#000000")
                        self.canvas.create_text(
                            x1 + self.SQUARE_SIZE / 2,
                            y1 + self.SQUARE_SIZE / 2,
                            text=symbol,font=("Arial", 36),fill="#FFFFFF")
                    else:
                        for dx, dy in [(-0.8, 0), (0.8, 0), (0, -0.8), (0, 0.8)]:
                            self.canvas.create_text(
                                x1 + self.SQUARE_SIZE / 2 + dx,
                                y1 + self.SQUARE_SIZE / 2 + dy,
                                text=symbol,font=("Arial", 36),fill="#FFFFFF")
                        self.canvas.create_text(
                            x1 + self.SQUARE_SIZE / 2,
                            y1 + self.SQUARE_SIZE / 2,
                            text=symbol,font=("Arial", 36),fill="#222222")

    def get_king_position(self,color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece[0] == color and piece[1] == 'king':
                    return (row, col)
        return None

    def is_in_check(self, color):
        king_pos = self.get_king_position(color)
        if not king_pos:
            return False
        opponent = 'black' if color == 'white' else 'white'
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece[0] == opponent:
                    if self.is_valid_move((row, col), king_pos):
                        return True
        return False

    def would_be_in_check_after_move(self, from_pos, to_pos, color):
        from_r, from_c = from_pos
        to_r, to_c = to_pos
        original_target = self.board[to_r][to_c]
        original_en_passant = None
        if self.en_passant_target and (to_r, to_c) == self.en_passant_target:
            captured_row = from_r
            captured_col = to_c
            original_en_passant = self.board[captured_row][captured_col]
            self.board[captured_row][captured_col] = None
        self.board[to_r][to_c] = self.board[from_r][from_c]
        self.board[from_r][from_c] = None
        in_check = self.is_in_check(color)
        self.board[from_r][from_c] = self.board[to_r][to_c]
        self.board[to_r][to_c] = original_target
        if original_en_passant:
            self.board[captured_row][captured_col] = original_en_passant
        return in_check

    def has_any_valid_move(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece[0] == color:
                    for to_r in range(8):
                        for to_c in range(8):
                            if self.is_valid_move((row, col), (to_r, to_c)):
                              if not self.would_be_in_check_after_move((row, col), (to_r, to_c), color):
                                    return True
        return False

    def is_castling_valid(self, color, side):
        if self.piece_moved[color]['king']:
            return False
        if side == 'kingside':
            if self.piece_moved[color]['rook_h']:
                return False
            row = 7 if color == 'white' else 0
            if self.board[row][5] is not None or self.board[row][6] is not None:
                return False
            if self.is_in_check(color):
                return False
            temp_pos = [(row, 4), (row, 5), (row, 6)]
            for pos in temp_pos[1:]:
                if self.would_be_in_check_after_move(temp_pos[0], pos, color):
                    return False
            return True
        elif side == 'queenside':
            if self.piece_moved[color]['rook_a']:
                return False
            row = 7 if color == 'white' else 0
            if self.board[row][1] is not None or self.board[row][2] is not None or self.board[row][3] is not None:
                return False
            if self.is_in_check(color):
                return False
            temp_pos = [(row, 4), (row, 3), (row, 2)]
            for pos in temp_pos[1:]:
                if self.would_be_in_check_after_move(temp_pos[0], pos, color):
                    return False
            return True
        return False

    def perform_castling(self, color, side):
        row = 7 if color == 'white' else 0
        if side == 'kingside':
            self.board[row][6] = self.board[row][4]
            self.board[row][4] = None
            self.board[row][5] = self.board[row][7]
            self.board[row][7] = None
            self.piece_moved[color]['king'] = True
            self.piece_moved[color]['rook_h'] = True
        elif side == 'queenside':
            self.board[row][2] = self.board[row][4]
            self.board[row][4] = None
            self.board[row][3] = self.board[row][0]
            self.board[row][0] = None
            self.piece_moved[color]['king'] = True
            self.piece_moved[color]['rook_a'] = True

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
                from_r, from_c = self.selected_pos
                if self.selected_piece[1] == 'king':
                    color = self.selected_piece[0]
                    if from_c == 4 and row == (7 if color == 'white' else 0):
                        if col == 6 and self.is_castling_valid(color, 'kingside'):
                            self.perform_castling(color, 'kingside')
                            self.after_move()
                            self.selected_piece = None
                            self.selected_pos = None
                            self.draw_board()
                            return
                        elif col == 2 and self.is_castling_valid(color, 'queenside'):
                            self.perform_castling(color, 'queenside')
                            self.after_move()
                            self.selected_piece = None
                            self.selected_pos = None
                            self.draw_board()
                            return
                if self.is_valid_move(self.selected_pos, (row, col)):
                    if self.would_be_in_check_after_move(self.selected_pos, (row, col), self.current_turn):
                        messagebox.showwarning("Invalid Move", "You cannot make this move — your king would be in check!")
                    else:
                        if self.is_in_check(self.current_turn):
                            if not self.would_be_in_check_after_move(self.selected_pos, (row, col), self.current_turn):
                                self.move_piece(self.selected_pos, (row, col))
                                self.after_move()
                            else:
                                messagebox.showwarning("Invalid Move", "Your king is in check — you must get out of check first!")
                        else:
                            self.move_piece(self.selected_pos, (row, col))
                            self.after_move()          
                self.selected_piece = None
                self.selected_pos = None
        self.draw_board()

    def end_game_options(self, title, message):
        self.stop_timer()
        result = messagebox.askquestion(title, message + "\n\nBack to Menu? (Yes) / Exit? (No)", icon='info')
        if result == 'yes':
            self.go_back_to_menu()
        else:
            self.root.quit()

    def go_back_to_menu(self):
        self.game_running = False
        self.canvas.pack_forget()
        self.info_panel.pack_forget()
        self.menu_frame.pack(fill="both", expand=True)
        self.selected_piece = None
        self.selected_pos = None
        self.current_turn = 'white'

    def after_move(self):
        self.stop_timer()
        if self.current_turn == 'white':
            self.current_turn = 'black'
            self.start_timer('black')
        else:
            self.current_turn = 'white'
            self.start_timer('white')
        self.info_label.config(text=f"Turn: {self.player_names[self.current_turn]}")                
        if self.is_in_check(self.current_turn):
            if not self.has_any_valid_move(self.current_turn):
                winner = self.player_names['black'] if self.current_turn == 'white' else self.player_names['white']
                self.end_game_options("Checkmate!", f"Checkmate! {winner} wins!")
                return
            else:
                messagebox.showinfo("Check!", f"{self.player_names[self.current_turn]}, your king is in check! You must defend it.")
        elif not self.has_any_valid_move(self.current_turn):
            self.end_game_options("Stalemate!", "Stalemate! It's a draw!")
            return

        if self.game_mode == 'computer' and self.current_turn == 'black' and self.game_running:
            self.root.after(800, self.computer_move)

    def evaluate_move(self, from_pos, to_pos):
        to_r, to_c = to_pos
        score = 0
        target = self.board[to_r][to_c]
        if target and target[0] == 'white':
            score += self.piece_values[target[1]] * 10
        if self.is_square_attacked(to_pos, 'white'):
            score -= self.piece_values[self.board[from_pos[0]][from_pos[1]][1]] * 8
        king_pos = self.get_king_position('white')
        if self.is_valid_move(to_pos, king_pos):
            score += 5
        return score

    def is_square_attacked(self, pos, attacker_color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece[0] == attacker_color:
                    if self.is_valid_move((row, col), pos):
                        return True
        return False

    def computer_move(self):
        all_valid_moves = []
        capture_moves = []
        good_moves = []

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece[0] == 'black':
                    for to_row in range(8):
                        for to_col in range(8):
                            if self.is_valid_move((row, col), (to_row, to_col)):
                                if not self.would_be_in_check_after_move((row, col), (to_row, to_col), 'black'):
                                    move = ((row, col), (to_row, to_col))
                                    all_valid_moves.append(move)
                                    if self.board[to_row][to_col] and self.board[to_row][to_col][0] == 'white':
                                        capture_moves.append(move)

        if not all_valid_moves:
            if self.is_in_check('black'):
                self.end_game_options("Checkmate!", "Checkmate! You win!")
            else:
                self.end_game_options("Stalemate!", "Stalemate! It's a draw!")
            self.game_running = False
            self.stop_timer()
            return

        if self.difficulty == 'easy':
            from_pos, to_pos = random.choice(all_valid_moves)
        elif self.difficulty == 'medium':
            if capture_moves:
                from_pos, to_pos = random.choice(capture_moves)
            else:
                from_pos, to_pos = random.choice(all_valid_moves)
        elif self.difficulty == 'hard':
            best_score = -9999
            best_moves = []
            for move in all_valid_moves:
                score = self.evaluate_move(move[0], move[1])
                if score > best_score:
                    best_score = score
                    best_moves = [move]
                elif score == best_score:
                    best_moves.append(move)
            from_pos, to_pos = random.choice(best_moves)

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
            if abs_dc == 1 and dr == direction:
                if target:
                    return True
                elif self.en_passant_target == (to_row, to_col):
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
        color, ptype = self.board[from_row][from_col]
        if ptype == 'king':
            self.piece_moved[color]['king'] = True
        if ptype == 'rook':
            if from_col == 0:
                self.piece_moved[color]['rook_a'] = True
            elif from_col == 7:
                self.piece_moved[color]['rook_h'] = True
        self.en_passant_target = None
        if ptype == 'pawn' and abs(from_row - to_row) == 2:
            ep_row = (from_row + to_row) // 2
            self.en_passant_target = (ep_row, from_col)
        if ptype == 'pawn' and (to_row, to_col) == self.en_passant_target:
            captured_row = from_row
            captured_col = to_col
            self.board[captured_row][captured_col] = None
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = None

    def show_rules(self):
        rules = """
Basic Rules:
- White moves first
- Each piece moves according to its own rules
- King: 1 square in any direction; Castling: if king and rook haven't moved, path is clear, and king is not in check
- Queen: any number of squares in any direction
- Rook: straight (horizontal/vertical)
- Bishop: diagonally
- Knight: in L-shape (2 + 1)
- Pawn: forward 1 square, 2 squares on first move; captures diagonally; En Passant capture allowed
- Check: when the king is under attack — you must get out of check
- Checkmate: when the king is in check and there is no legal move to escape — game over
Goal: Checkmate the opponent's king.     
Difficulty Levels:
• Easy - random moves
• Medium - prioritizes capturing your pieces
• Hard - defends itself and attacks strategically
        """
        messagebox.showinfo("Game Rules", rules)

def main():
    root = tk.Tk()
    app = ChessGameApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()