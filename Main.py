import tkinter as tk
import random
from tkinter import messagebox

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")
        self.difficulty = "Easy"  # Default difficulty
        self.grid_size = 4  # Default grid size
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.create_ui()
        self.start_game()

    def start_game(self):
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]  # Reset grid
        self.add_new_tile()
        self.add_new_tile()
        self.update_ui()
        self.selected_tile = None
        self.reset_timer()  # Start the timer for automatic increment

    def create_ui(self):
        # Dropdown menu for difficulty selection
        self.difficulty_var = tk.StringVar(value=self.difficulty)
        difficulty_menu = tk.OptionMenu(self.root, self.difficulty_var, "Easy", "Medium", "Hard", command=self.set_difficulty)
        difficulty_menu.grid(row=0, column=0, columnspan=4, pady=10)

        self.labels = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                label = tk.Label(self.root, text="", width=4, height=2, font=("Helvetica", 32), bg="lightgray", relief="solid")
                label.grid(row=i + 1, column=j, padx=5, pady=5)
                label.bind("<Button-1>", lambda event, r=i, c=j: self.select_tile(r, c))
                row.append(label)
            self.labels.append(row)

        # Restart Button
        restart_button = tk.Button(self.root, text="Restart Game", command=self.start_game, font=("Helvetica", 14), bg="lightblue")
        restart_button.grid(row=self.grid_size + 1, column=0, columnspan=4, pady=10)

        # Quit Button with confirmation
        quit_button = tk.Button(self.root, text="Quit", command=self.confirm_quit, font=("Helvetica", 14), bg="lightcoral")
        quit_button.grid(row=self.grid_size + 2, column=0, columnspan=4, pady=10)

        # Key bindings for movement
        self.root.bind("<Key>", self.handle_keypress)

    def set_difficulty(self, choice):
        if choice == "Easy":
            self.grid_size = 4
        elif choice == "Medium":
            self.grid_size = 5
        elif choice == "Hard":
            self.grid_size = 6
        
        self.start_game()  # Restart the game when difficulty is changed
        self.update_ui()

    def confirm_quit(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.root.quit()

    def select_tile(self, row, col):
        value = self.grid[row][col]

        if value == 0:
            return  # Skip empty tiles
        
        if self.selected_tile is None:
            # Select the first tile
            self.selected_tile = (row, col)
            self.labels[row][col].config(bg="yellow")  # Highlight the selected tile
        else:
            # Second tile clicked, perform merge check
            selected_row, selected_col = self.selected_tile
            selected_value = self.grid[selected_row][selected_col]

            if (selected_row, selected_col) != (row, col) and selected_value == value:
                # Merge the two tiles
                self.grid[row][col] = selected_value * 2
                self.grid[selected_row][selected_col] = 0

            # Reset the selection and update UI
            self.labels[selected_row][selected_col].config(bg="lightgray")
            self.selected_tile = None
            self.add_new_tile()  # Add a new random tile
            self.update_ui()

            # Check for Game Over
            if self.check_game_over():
                self.show_game_over()
            else:
                self.reset_timer()  # Reset the timer after a successful move

    def update_ui(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.grid[i][j]
                if value == 0:
                    self.labels[i][j].config(text="", bg="lightgray")
                else:
                    self.labels[i][j].config(text=str(value), bg=self.get_tile_color(value))

    def get_tile_color(self, value):
        colors = {
            2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
            128: "#edcf72", 256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }
        return colors.get(value, "#3c3a32")

    def add_new_tile(self):
        empty_tiles = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.grid[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.grid[i][j] = random.choice([2, 4])

    def handle_keypress(self, event):
        key = event.keysym
        if key == "Up":
            self.move_up()
        elif key == "Down":
            self.move_down()
        elif key == "Left":
            self.move_left()
        elif key == "Right":
            self.move_right()

        self.add_new_tile()
        self.update_ui()

        # Check for Game Over after every move
        if self.check_game_over():
            self.show_game_over()
        else:
            self.reset_timer()  # Reset the timer after a move

    def move_left(self):
        self.grid = [self.merge(row) for row in self.grid]

    def move_right(self):
        self.grid = [self.merge(row[::-1])[::-1] for row in self.grid]

    def move_up(self):
        self.grid = list(map(list, zip(*self.grid)))  # Transpose
        self.grid = [self.merge(row) for row in self.grid]
        self.grid = list(map(list, zip(*self.grid)))  # Transpose back

    def move_down(self):
        self.grid = list(map(list, zip(*self.grid)))  # Transpose
        self.grid = [self.merge(row[::-1])[::-1] for row in self.grid]
        self.grid = list(map(list, zip(*self.grid)))  # Transpose back

    def merge(self, row):
        non_zero = [x for x in row if x != 0]
        merged_row = []
        i = 0
        while i < len(non_zero):
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                merged_row.append(non_zero[i] * 2)
                i += 2
            else:
                merged_row.append(non_zero[i])
                i += 1
        return merged_row + [0] * (self.grid_size - len(merged_row))

    def check_game_over(self):
        # Check if there are any empty tiles
        if any(0 in row for row in self.grid):
            return False

        # Check if there are any moves left (adjacent tiles with the same value)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if i < self.grid_size - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
                if j < self.grid_size - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
        return True

    def show_game_over(self):
        # Create a new window for the Game Over message
        game_over_window = tk.Toplevel(self.root)
        game_over_window.title("Game Over")
        
        # Create a label with the game over message
        game_over_label = tk.Label(game_over_window, text="Game Over!", font=("Helvetica", 32))
        game_over_label.pack(pady=20)

        # Button to restart the game
        restart_button = tk.Button(game_over_window, text="Restart Game", command=self.start_game, font=("Helvetica", 14), bg="lightblue")
        restart_button.pack(pady=10)

        # Button to quit the game
        quit_button = tk.Button(game_over_window, text="Quit", command=self.confirm_quit, font=("Helvetica", 14), bg="lightcoral")
        quit_button.pack(pady=10)

    def reset_timer(self):
        self.timer_running = True
        if self.difficulty_var.get() == "Easy":
            self.timer_event = self.root.after(5000, self.auto_increment)
        elif self.difficulty_var.get() == "Medium":
            self.timer_event = self.root.after(3000, self.auto_increment)
        elif self.difficulty_var.get() == "Hard":
            self.timer_event = self.root.after(1000, self.auto_increment)
        self.timer_event = self.root.after(5000, self.auto_increment)

    def auto_increment(self):
        if not self.timer_running:
            return  # If timer is stopped, do nothing

        # Find a random empty tile and add a new number
        empty_tiles = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.grid[i][j] == 0]
        if empty_tiles:
            i, j = random.choice(empty_tiles)
            self.grid[i][j] = random.choice([2, 4])
            self.update_ui()  # Update UI after adding new tile

        # Check for Game Over after the auto-increment
        if self.check_game_over():
            self.show_game_over()
        else:
            # Schedule the next increment
            self.reset_timer()

    def stop_timer(self):
        self.timer_running = False
        if hasattr(self, 'timer_event'):
            self.root.after_cancel(self.timer_event)
            # Reset the timer event (if it exists) so that it doesn't try to call itself
            # after the timer has been stopped
if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
