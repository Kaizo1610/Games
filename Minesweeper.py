import tkinter as tk
import random
from tkinter import messagebox

class Minesweeper:
    def __init__(self, master, rows=10, cols=10, mines=10):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.buttons = []
        self.mine_locations = set()
        self.is_game_over = False

        self.create_widgets()
        self.place_mines()

    def create_widgets(self):
        self.frame = tk.Frame(self.master)
        self.frame.grid()
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                button = tk.Button(self.frame, width=2, height=1, command=lambda r=r, c=c: self.reveal(r, c))
                button.bind('<Button-3>', lambda event, r=r, c=c: self.flag(r, c))
                button.grid(row=r, column=c)
                row.append(button)
            self.buttons.append(row)

    def reset_game(self):
        self.mine_locations.clear()
        self.is_game_over = False
        for row in self.buttons:
            for button in row:
                button.config(text="", state="normal", bg="SystemButtonFace")
        self.place_mines()

    def place_mines(self):
        mine_count = 0
        while mine_count < self.mines:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if (r, c) not in self.mine_locations:
                self.mine_locations.add((r, c))
                mine_count += 1

    def reveal(self, r, c):
        if self.is_game_over or self.buttons[r][c]['state'] == 'disabled':
            return

        if (r, c) in self.mine_locations:
            self.buttons[r][c].config(text="*", bg="red")
            self.game_over(False)
        else:
            mines_count = self.count_adjacent_mines(r, c)
            self.buttons[r][c].config(text=str(mines_count), state='disabled')
            if mines_count == 0:
                self.reveal_adjacent(r, c)

        if self.check_win():
            self.game_over(True)

    def reveal_adjacent(self, r, c):
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if 0 <= r + dr < self.rows and 0 <= c + dc < self.cols:
                    if self.buttons[r + dr][c + dc]['state'] != 'disabled':
                        self.reveal(r + dr, c + dc)

    def count_adjacent_mines(self, r, c):
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if (r + dr, c + dc) in self.mine_locations:
                    count += 1
        return count

    def flag(self, r, c):
        if self.is_game_over or self.buttons[r][c]['state'] == 'disabled':
            return

        if self.buttons[r][c]['text'] == 'F':
            self.buttons[r][c].config(text="")
        else:
            self.buttons[r][c].config(text="F")

    def check_win(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in self.mine_locations and self.buttons[r][c]['state'] != 'disabled':
                    return False
        return True

    def game_over(self, won):
        self.is_game_over = True
        if won:
            msg = "You win!"
        else:
            msg = "Game over!"
            for r, c in self.mine_locations:
                self.buttons[r][c].config(text="*", bg="red")

        play_again = messagebox.askyesno("Minesweeper", f"{msg} Do you want to play again?")
        if play_again:
            self.reset_game()
        else:
            self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    game = Minesweeper(root)
    root.mainloop()
