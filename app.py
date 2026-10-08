import random
import tkinter as tk

GRID_SIZE = 20
CELL_SIZE = 25
WINDOW_SIZE = GRID_SIZE * CELL_SIZE


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.configure(bg="#111827")
        self.root.resizable(False, False)

        self.score = 0
        self.running = True
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.snake = [(5, 10), (4, 10), (3, 10)]
        self.food = self.generate_food()

        self.canvas = tk.Canvas(
            root,
            width=WINDOW_SIZE,
            height=WINDOW_SIZE,
            bg="#0f172a",
            highlightthickness=0,
        )
        self.canvas.pack(padx=10, pady=10)

        self.score_label = tk.Label(
            root,
            text=f"Score: {self.score}",
            font=("Arial", 16, "bold"),
            fg="#f8fafc",
            bg="#111827",
        )
        self.score_label.pack()

        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.focus_set()
        self.tick()

    def generate_food(self):
        while True:
            food = (
                random.randint(0, GRID_SIZE - 1),
                random.randint(0, GRID_SIZE - 1),
            )
            if food not in self.snake:
                return food

    def on_key_press(self, event):
        if not self.running:
            return

        key = event.keysym.lower()
        moves = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0),
        }
        if key in moves:
            new_dir = moves[key]
            if new_dir != (-self.direction[0], -self.direction[1]):
                self.next_direction = new_dir

    def move(self):
        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if (
            new_head[0] < 0
            or new_head[0] >= GRID_SIZE
            or new_head[1] < 0
            or new_head[1] >= GRID_SIZE
            or new_head in self.snake[:-1]
        ):
            self.running = False
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.food = self.generate_food()
        else:
            self.snake.pop()

    def game_over(self):
        self.canvas.create_text(
            WINDOW_SIZE / 2,
            WINDOW_SIZE / 2,
            text="Game Over",
            fill="#f87171",
            font=("Arial", 28, "bold"),
        )
        self.canvas.create_text(
            WINDOW_SIZE / 2,
            WINDOW_SIZE / 2 + 35,
            text=f"Final Score: {self.score}",
            fill="#f8fafc",
            font=("Arial", 16, "bold"),
        )
        self.canvas.create_text(
            WINDOW_SIZE / 2,
            WINDOW_SIZE / 2 + 65,
            text="Press R to restart",
            fill="#93c5fd",
            font=("Arial", 12, "bold"),
        )
        self.root.bind("<KeyPress>", self.restart_if_needed)

    def restart_if_needed(self, event):
        if event.keysym.lower() == "r":
            self.root.unbind("<KeyPress>")
            self.root.bind("<KeyPress>", self.on_key_press)
            self.__init__(self.root)

    def draw(self):
        self.canvas.delete("all")

        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                self.canvas.create_rectangle(
                    col * CELL_SIZE,
                    row * CELL_SIZE,
                    (col + 1) * CELL_SIZE,
                    (row + 1) * CELL_SIZE,
                    fill="#0f172a",
                    outline="#1e293b",
                )

        food_x, food_y = self.food
        self.canvas.create_oval(
            food_x * CELL_SIZE + 5,
            food_y * CELL_SIZE + 5,
            (food_x + 1) * CELL_SIZE - 5,
            (food_y + 1) * CELL_SIZE - 5,
            fill="#ef4444",
            outline="#fca5a5",
            width=2,
        )

        for index, (x, y) in enumerate(self.snake):
            color = "#22c55e" if index == 0 else "#16a34a"
            self.canvas.create_rectangle(
                x * CELL_SIZE + 1,
                y * CELL_SIZE + 1,
                (x + 1) * CELL_SIZE - 1,
                (y + 1) * CELL_SIZE - 1,
                fill=color,
                outline="#14532d",
            )

    def tick(self):
        if self.running:
            self.move()
            self.draw()
        self.root.after(120, self.tick)


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
