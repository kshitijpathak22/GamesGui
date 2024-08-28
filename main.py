import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import heapq

# Define the goal state for 8 Puzzle
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)  # 0 represents the empty space

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic-Tac-Toe")
        self.master.geometry("400x400")  # Adjust the window size

        self.current_player = "X"
        self.board = ["-" for _ in range(9)]

        self.buttons = []
        self.create_board()

    def create_board(self):
        for i in range(3):
            for j in range(3):
                button = tk.Button(self.master, text="", font=("Arial", 30), width=4, height=2,
                                   command=lambda row=i, col=j: self.make_move(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(button)

    def make_move(self, row, col):
        position = row * 3 + col
        if self.board[position] == "-":
            self.board[position] = self.current_player
            self.buttons[position].config(text=self.current_player)
            game_result = self.check_game_over()
            if game_result == "win":
                messagebox.showinfo("Game Over", f"{self.current_player} wins!")
                self.reset_game()
            elif game_result == "tie":
                messagebox.showinfo("Game Over", "It's a tie!")
                self.reset_game()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                if self.current_player == "O":
                    self.make_computer_move()

    def make_computer_move(self):
        available_positions = [i for i in range(9) if self.board[i] == "-"]
        position = random.choice(available_positions)
        self.make_move(position // 3, position % 3)

    def check_game_over(self):
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != "-":
                return "win"
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != "-":
                return "win"
        if self.board[0] == self.board[4] == self.board[8] != "-":
            return "win"
        if self.board[2] == self.board[4] == self.board[6] != "-":
            return "win"
        if "-" not in self.board:
            return "tie"
        return "play"

    def reset_game(self):
        self.board = ["-" for _ in range(9)]
        self.current_player = "X"
        for button in self.buttons:
            button.config(text="")

class WaterJugSolverGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Water Jug Solver")
        self.master.geometry("400x200")  # Adjust the window size

        self.jug1_capacity = 4
        self.jug2_capacity = 3
        self.target_amount = 2

        self.create_widgets()

    def create_widgets(self):
        self.label_jug1_capacity = tk.Label(self.master, text="Jug 1 Capacity:")
        self.label_jug1_capacity.grid(row=0, column=0)
        self.entry_jug1_capacity = tk.Entry(self.master)
        self.entry_jug1_capacity.insert(0, str(self.jug1_capacity))
        self.entry_jug1_capacity.grid(row=0, column=1)

        self.label_jug2_capacity = tk.Label(self.master, text="Jug 2 Capacity:")
        self.label_jug2_capacity.grid(row=1, column=0)
        self.entry_jug2_capacity = tk.Entry(self.master)
        self.entry_jug2_capacity.insert(0, str(self.jug2_capacity))
        self.entry_jug2_capacity.grid(row=1, column=1)

        self.label_target_amount = tk.Label(self.master, text="Target Amount:")
        self.label_target_amount.grid(row=2, column=0)
        self.entry_target_amount = tk.Entry(self.master)
        self.entry_target_amount.insert(0, str(self.target_amount))
        self.entry_target_amount.grid(row=2, column=1)

        self.solve_button = tk.Button(self.master, text="Solve", command=self.solve)
        self.solve_button.grid(row=3, columnspan=2)

        self.result_label = tk.Label(self.master, text="")
        self.result_label.grid(row=4, columnspan=2)

    def solve(self):
        self.jug1_capacity = int(self.entry_jug1_capacity.get())
        self.jug2_capacity = int(self.entry_jug2_capacity.get())
        self.target_amount = int(self.entry_target_amount.get())

        result = self.water_jug_a_star(self.jug1_capacity, self.jug2_capacity, self.target_amount)

        if result:
            self.result_label.config(text=f"Solution: {result}")
        else:
            self.result_label.config(text="No solution found!")

    def water_jug_a_star(self, jug1_capacity, jug2_capacity, target_amount):
        start_state = (0, 0)
        open_list = [(0, start_state)]  # (f-value, state)
        closed_set = set()

        while open_list:
            current_cost, current_state = heapq.heappop(open_list)

            if current_state == (target_amount, 0) or current_state == (0, target_amount):
                # Goal reached
                return current_state

            closed_set.add(current_state)

            # Generate successor states
            successors = self.generate_successors(current_state, jug1_capacity, jug2_capacity)

            if successors is not None:
                for successor in successors:
                    if successor not in closed_set:
                        # Calculate f-value (cost + heuristic)
                        cost = current_cost + 1  # Assuming each step has a cost of 1
                        heuristic = self.calculate_heuristic(successor, target_amount)
                        f_value = cost + heuristic
                        heapq.heappush(open_list, (f_value, successor))

        # No solution found
        return None

    def generate_successors(self, state, jug1_capacity, jug2_capacity):
        jug1, jug2 = state
        successors = []

        # Fill jug 1
        successors.append((jug1_capacity, jug2))
        # Fill jug 2
        successors.append((jug1, jug2_capacity))
        # Empty jug 1
        successors.append((0, jug2))
        # Empty jug 2
        successors.append((jug1, 0))
        # Pour water from jug 1 to jug 2
        pour = min(jug1, jug2_capacity - jug2)
        successors.append((jug1 - pour, jug2 + pour))
        # Pour water from jug 2 to jug 1
        pour = min(jug2, jug1_capacity - jug1)
        successors.append((jug1 + pour, jug2 - pour))

        return successors

    def calculate_heuristic(self, state, target_amount):
        return abs(sum(state) - target_amount)


class RatInMazeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Rat in a Maze Solver")
        self.master.geometry("500x500")  # Adjust the window size

        # Set initial maze parameters
        self.rows = 5
        self.columns = 5
        self.cell_size = 30

        # Create the canvas for the maze
        self.canvas = tk.Canvas(self.master, width=self.columns * self.cell_size, height=self.rows * self.cell_size)
        self.canvas.pack()

        # Create cells in the maze
        self.cells = []
        self.walls = set()
        self.draw_maze()

        # Add event binding to toggle walls
        self.canvas.bind("<Button-1>", self.toggle_wall)

        # Create entry fields for maze size
        self.row_label = tk.Label(self.master, text="Rows:")
        self.row_label.pack()
        self.row_entry = tk.Entry(self.master)
        self.row_entry.pack()

        self.column_label = tk.Label(self.master, text="Columns:")
        self.column_label.pack()
        self.column_entry = tk.Entry(self.master)
        self.column_entry.pack()

        # Create a button to update maze size
        self.update_button = tk.Button(self.master, text="Update Maze Size", command=self.update_maze_size)
        self.update_button.pack()

        # Create solve button
        self.solve_button = tk.Button(self.master, text="Solve Maze", command=self.solve_maze)
        self.solve_button.pack()

    def find_path(self, maze, start, goal):
        def dfs(current, path):
            if current == goal:
                return path + [current]

            x, y = current
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_x, next_y = x + dx, y + dy
                if (0 <= next_x < len(maze) and 0 <= next_y < len(maze[0]) and
                    maze[next_x][next_y] == 0 and (next_x, next_y) not in path):
                    result = dfs((next_x, next_y), path + [current])
                    if result:
                        return result
            return None

        return dfs(start, [])

    def create_maze(self):
        maze = []
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                if (i, j) in self.walls:
                    row.append(1)  # 1 represents an obstacle
                else:
                    row.append(0)  # 0 represents an empty cell
            maze.append(row)
        return maze

    def update_maze_size(self):
        try:
            new_rows = int(self.row_entry.get())
            new_columns = int(self.column_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer values for rows and columns.")
            return

        if new_rows <= 0 or new_columns <= 0:
            messagebox.showerror("Error", "Rows and columns must be positive integers.")
            return

        self.rows, self.columns = new_rows, new_columns
        self.canvas.config(width=self.columns * self.cell_size, height=self.rows * self.cell_size)
        self.canvas.delete("all")
        self.draw_maze()

    def draw_maze(self):
        self.cells = []
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                fill_color = "black" if (i, j) in self.walls else "white"
                cell = self.canvas.create_rectangle(
                    j * self.cell_size, i * self.cell_size,
                    (j + 1) * self.cell_size, (i + 1) * self.cell_size,
                    fill=fill_color, outline="gray"
                )
                row.append(cell)
            self.cells.append(row)

    def solve_maze(self):
        maze = self.create_maze()
        start = (0, 0)
        goal = (self.rows - 1, self.columns - 1)
        path = self.find_path(maze, start, goal)
        if path:
            path_str = " -> ".join(str(cell) for cell in path)
            messagebox.showinfo("Path found", f"Path: {path_str}")
        else:
            messagebox.showinfo("No path found", "No path found")

    def toggle_wall(self, event):
        x, y = event.y // self.cell_size, event.x // self.cell_size
        if (x, y) in self.walls:
            self.walls.remove((x, y))
        else:
            self.walls.add((x, y))
        self.draw_maze()

class GamePlatform:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Platform")
        self.master.geometry("500x900")  # Adjust the window size
        self.create_widgets()
        self.master.configure(bg="light blue")

    def create_widgets(self):

        heading_label = tk.Label(self.master, text="Games GUI", font=("Helvetica", 30), bg="light green", fg="blue"
                                                                                                             ""
                                                                                                             "")
        heading_label.grid(row=0, column=0, columnspan=900, pady=10)
        # Load images
        tic_tac_toe_image = Image.open("tic_tac_toe.png")
        water_jug_solver_image = Image.open("water_jug.png")
        rat_in_maze_image = Image.open("rat_in_maze.png")
        eight_puzzle_image = Image.open("eigth_puzzle.png")
        find_s_image = Image.open("find_s.jpeg")

        # Resize images
        image_size = (200, 200)  # Adjust the size as needed
        tic_tac_toe_image = tic_tac_toe_image.resize(image_size, Image.LANCZOS)
        water_jug_solver_image = water_jug_solver_image.resize(image_size, Image.LANCZOS)
        rat_in_maze_image = rat_in_maze_image.resize(image_size, Image.LANCZOS)
        eight_puzzle_image = eight_puzzle_image.resize(image_size, Image.LANCZOS)
        find_s_image = find_s_image.resize(image_size, Image.LANCZOS)

        # Convert images to PhotoImage objects
        self.tic_tac_toe_photo = ImageTk.PhotoImage(tic_tac_toe_image)
        self.water_jug_solver_photo = ImageTk.PhotoImage(water_jug_solver_image)
        self.rat_in_maze_photo = ImageTk.PhotoImage(rat_in_maze_image)
        self.eight_puzzle_photo = ImageTk.PhotoImage(eight_puzzle_image)
        self.find_s_photo = ImageTk.PhotoImage(find_s_image)

        # Create labels for images
        self.tic_tac_toe_label = tk.Label(self.master, image=self.tic_tac_toe_photo)
        self.tic_tac_toe_label.grid(row=1, column=0, padx=10, pady=10)

        self.water_jug_solver_label = tk.Label(self.master, image=self.water_jug_solver_photo)
        self.water_jug_solver_label.grid(row=1, column=1, padx=10, pady=10)

        self.rat_in_maze_label = tk.Label(self.master, image=self.rat_in_maze_photo)
        self.rat_in_maze_label.grid(row=3, column=0, padx=10, pady=10)

        self.eight_puzzle_label = tk.Label(self.master, image=self.eight_puzzle_photo)
        self.eight_puzzle_label.grid(row=3, column=1, padx=10, pady=10)

        self.find_s_label = tk.Label(self.master, image=self.find_s_photo)
        self.find_s_label.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Buttons
        tic_tac_toe_button = tk.Button(self.master, text="Tic Tac Toe", command=self.open_tic_tac_toe, borderwidth=1, highlightbackground="light blue")
        tic_tac_toe_button.grid(row=2, column=0, padx=10, pady=10)

        water_jug_solver_button = tk.Button(self.master, text="Water Jug Solver", command=self.open_water_jug_solver, borderwidth=1, highlightbackground="light blue")
        water_jug_solver_button.grid(row=2, column=1, padx=10, pady=10)

        rat_in_maze_button = tk.Button(self.master, text="Rat in Maze", command=self.open_rat_in_maze, borderwidth=0, highlightbackground="light blue")
        rat_in_maze_button.grid(row=4, column=0, padx=10, pady=10)

        eight_puzzle_button = tk.Button(self.master, text="8 Puzzle", command=self.open_eight_puzzle, borderwidth=0, highlightbackground="light blue")
        eight_puzzle_button.grid(row=4, column=1, padx=10, pady=10)

        find_s_button = tk.Button(self.master, text="Find-S Algorithm", command=self.open_find_s, borderwidth=0, highlightbackground="light blue")
        find_s_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def open_tic_tac_toe(self):
        root = tk.Toplevel(self.master)
        app = TicTacToeGUI(root)

    def open_water_jug_solver(self):
        root = tk.Toplevel(self.master)
        app = WaterJugSolverGUI(root)

    def open_rat_in_maze(self):
        root = tk.Toplevel(self.master)
        app = RatInMazeGUI(root)

    def solve_puzzle(initial_state, goal_state):
        # Define the goal state for 8 Puzzle
        GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)  # 0 represents the empty space

        def calculate_heuristic(state):
            # Manhattan distance heuristic
            h = 0
            for i in range(3):
                for j in range(3):
                    value = state[i * 3 + j]
                    if value != 0:
                        goal_row = (value - 1) // 3
                        goal_col = (value - 1) % 3
                        h += abs(i - goal_row) + abs(j - goal_col)
            return h

        def generate_successors(state):
            successors = []
            empty_index = state.index(0)
            row, col = empty_index // 3, empty_index % 3

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 3 and 0 <= new_col < 3:
                    new_index = new_row * 3 + new_col
                    new_state = list(state)
                    new_state[empty_index], new_state[new_index] = new_state[new_index], new_state[empty_index]
                    successors.append(new_state)

            return successors

        open_list = [(0 + calculate_heuristic(initial_state), 0, initial_state)]  # (f-value, g-value, state)
        closed_set = set()

        while open_list:
            f_value, g_value, current_state = heapq.heappop(open_list)

            if current_state == goal_state:
                # Goal reached
                return ["Goal reached"]

            closed_set.add(current_state)

            # Generate successor states
            successors = generate_successors(current_state)

            for successor in successors:
                if successor not in closed_set:
                    # Calculate f-value and g-value
                    successor_g_value = g_value + 1
                    successor_f_value = successor_g_value + calculate_heuristic(successor)
                    heapq.heappush(open_list, (successor_f_value, successor_g_value, successor))

        # No solution found
        return ["No solution found"]

    def open_eight_puzzle(self):
        window = tk.Toplevel(self.master)
        window.title("8 Puzzle")

        # Function to handle solving the puzzle
        def solve():
            # Get initial state and goal state from entry fields
            initial_state = [int(entry.get()) for entry in initial_state_entries]
            goal_state = [int(entry.get()) for entry in goal_state_entries]

            # Call solve_puzzle function to solve the puzzle
            steps = solve_puzzle(initial_state, goal_state)
            if steps:
                # If steps are found, display them
                messagebox.showinfo("Solution", "\n".join(steps))
            else:
                # If no solution is found, display a message
                messagebox.showinfo("No Solution", "No solution found.")

        # Create entry fields for initial state
        initial_state_label = tk.Label(window, text="Initial State:")
        initial_state_label.grid(row=0, column=0, padx=10, pady=5)
        initial_state_entries = []
        for i in range(3):
            for j in range(3):
                entry = tk.Entry(window, width=5)
                entry.grid(row=i + 1, column=j, padx=2, pady=2)
                initial_state_entries.append(entry)

        # Create entry fields for goal state
        goal_state_label = tk.Label(window, text="Goal State:")
        goal_state_label.grid(row=4, column=0, padx=10, pady=5)
        goal_state_entries = []
        for i in range(3):
            for j in range(3):
                entry = tk.Entry(window, width=5)
                entry.grid(row=i + 5, column=j, padx=2, pady=2)
                goal_state_entries.append(entry)

        # Create solve button
        solve_button = tk.Button(window, text="Solve", command=solve)
        solve_button.grid(row=8, columnspan=3, padx=10, pady=10)


    def open_find_s(self):
        root = tk.Toplevel(self.master)
        app = FindSAlgorithmGUI(root)

class FindSAlgorithmGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Find-S Algorithm")
        self.master.geometry("500x400")  # Adjust the window size

        self.attributes = ["Attribute1:", "Attribute2:", "Attribute3:", "Attribute4:"]
        self.training_data = []

        self.create_widgets()

    def create_widgets(self):
        self.attribute_labels = []
        self.attribute_entry_fields = []
        for i, attribute in enumerate(self.attributes):
            label = tk.Label(self.master, text=attribute)
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            self.attribute_labels.append(label)

            entry_field = tk.Entry(self.master)
            entry_field.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            self.attribute_entry_fields.append(entry_field)

        self.train_button = tk.Button(self.master, text="Train", command=self.train)
        self.train_button.grid(row=len(self.attributes), columnspan=2, padx=10, pady=10)

        self.output_label = tk.Label(self.master, text="")
        self.output_label.grid(row=len(self.attributes) + 1, columnspan=2, padx=10, pady=5)

    def train(self):
        training_example = {}
        for attribute, entry_field in zip(self.attributes, self.attribute_entry_fields):
            value = entry_field.get()
            if value:
                training_example[attribute] = value

        if training_example:
            self.training_data.append(training_example)
            self.find_s_algorithm()
        else:
            self.output_label.config(text="No training example provided.")

    def find_s_algorithm(self):
        hypothesis = {}
        for example in self.training_data:
            for attribute, value in example.items():
                if attribute not in hypothesis:
                    hypothesis[attribute] = value
                elif hypothesis[attribute] != value:
                    hypothesis[attribute] = "?"

        self.display_hypothesis(hypothesis)

    def display_hypothesis(self, hypothesis):
        output_text = "Hypothesis (Find-S Algorithm):\n"
        for attribute, value in hypothesis.items():
            output_text += f"{attribute}: {value}\n"
        self.output_label.config(text=output_text)



def main():
    root = tk.Tk()
    app = GamePlatform(root)
    root.mainloop()



if __name__ == "__main__":
    main()
