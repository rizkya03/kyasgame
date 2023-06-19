import pygame
import random
import tkinter as tk
import threading

# Set the dimensions of the screen
WIDTH = 1000
HEIGHT = 700

# Set the dimensions of the maze grid
CELL_SIZE = 50
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Define Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define Button Colors
BUTTON_NORMAL = (150, 150, 150)
BUTTON_HOVER = (200, 200, 200)
BUTTON_CLICKED = (100, 100, 100)

# Define Button Dimensions
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 50
BUTTON_PADDING = 20
BUTTON_MARGIN = 10

# Initialize Pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Seek and Hide")
clock = pygame.time.Clock()

# Create the maze grid
grid = [[1] * GRID_HEIGHT for _ in range(GRID_WIDTH)]

# Define the directions for movement: UP, RIGHT, DOWN, LEFT
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

# Generate the maze using the Recursive Backtracking algorithm
def generate_maze(x, y):
    grid[x][y] = 0

    # Shuffle the directions randomly
    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + 2 * dx, y + 2 * dy

        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[nx][ny] == 1:
            grid[x + dx][y + dy] = 0
            generate_maze(nx, ny)

# Generate the maze starting from the top-left corner
generate_maze(0, 0)

class SeekAndHide:
    def __init__(self):
        
        self.maze_surface = pygame.Surface((WIDTH, HEIGHT))
        self.maze_surface.set_colorkey((0, 0, 0))

        # Initialize the game        
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.droids = []
        self.movement_enabled = False
        self.green_droid_visibility = 5

        # Create the GUI
        self.create_gui()
        self.gui_update_interval = 100  # GUI update interval in milliseconds
        
        # Create a separate thread for tkinter main loop
        self.gui_thread = threading.Thread(target=self.run_gui)
        self.gui_thread.daemon = True  # Set the thread as a daemon, so it terminates when the main thread ends

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("Seek and Hide")
        self.root.geometry("400x250")

        self.start_stop_button = tk.Button(self.root, text="Start/Stop", command=self.toggle_movement)
        self.start_stop_button.pack(pady=10)

        self.randomize_map_button = tk.Button(self.root, text="Randomize Map", command=self.randomize_map)
        self.randomize_map_button.pack()

        self.randomize_red_droid_button = tk.Button(self.root, text="Randomize Red Droid", command=self.randomize_red_droid)
        self.randomize_red_droid_button.pack()

        self.randomize_green_droid_button = tk.Button(self.root, text="Randomize Green Droid", command=self.randomize_green_droid)
        self.randomize_green_droid_button.pack()

        self.increase_red_droids_button = tk.Button(self.root, text="Increase Red Droids", command=self.increase_red_droids)
        self.increase_red_droids_button.pack()

        self.green_droid_visibility_label = tk.Label(self.root, text="Green Droid Visibility")
        self.green_droid_visibility_label.pack()

        self.green_droid_visibility_slider = tk.Scale(self.root, from_=1, to=GRID_WIDTH, orient="horizontal", length=200)
        self.green_droid_visibility_slider.set(self.green_droid_visibility)
        self.green_droid_visibility_slider.pack()

        self.red_droid_view_button = tk.Button(self.root, text="Show Red Droid View", command=self.show_red_droid_view)
        self.red_droid_view_button.pack()

        self.green_droid_view_button = tk.Button(self.root, text="Show Green Droid View", command=self.show_green_droid_view)
        self.green_droid_view_button.pack()

    def update_gui(self):
        self.root.update()

    def run_gui(self):
        self.root.mainloop()

    def toggle_movement(self):
        self.movement_enabled = not self.movement_enabled

    def randomize_map(self):
        global grid
        grid = [[1] * GRID_HEIGHT for _ in range(GRID_WIDTH)]
        generate_maze(0, 0)

    def randomize_red_droid(self):
        self.droids[0] = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def randomize_green_droid(self):
        self.droids[1] = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def increase_red_droids(self):
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        self.droids.append((x, y))

    def draw_map(self):
        self.maze_surface.fill((0, 0, 0))
        for i in range(GRID_WIDTH):
            for j in range(GRID_HEIGHT):
                if grid[i][j] == 1:
                    pygame.draw.rect(self.maze_surface, WHITE, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def draw_droids(self):
        self.screen.blit(self.maze_surface, (0, 0))

        for droid in self.droids:
            x = droid[0] * CELL_SIZE + CELL_SIZE // 2
            y = droid[1] * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(self.screen, RED, (x, y), CELL_SIZE // 3)

        # Adjust the size of the green droid by changing the radius value
        radius = CELL_SIZE // 4

        pygame.draw.circle(self.screen, GREEN, (self.droids[1][0] * CELL_SIZE + CELL_SIZE // 2, self.droids[1][1] * CELL_SIZE + CELL_SIZE // 2), radius)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.root.destroy()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.toggle_movement()

    def move_droids(self):
        if self.movement_enabled:
            red_droid_pos = self.droids[0]
            green_droid_pos = self.droids[1]
            
            # Calculate the distance between the red and green droids
            dx = green_droid_pos[0] - red_droid_pos[0]
            dy = green_droid_pos[1] - red_droid_pos[1]
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance <= self.green_droid_visibility:
                # The red droid sees the green droid, so it chases it
                if dx != 0:
                    dx //= abs(dx)
                if dy != 0:
                    dy //= abs(dy)
                nx, ny = red_droid_pos[0] + dx, red_droid_pos[1] + dy
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[nx][ny] != 1:
                    self.droids[0] = (nx, ny)
                else:
                    # Game over condition: Green droid caught by the red droid
                    self.game_over()
                    return  # Exit the method to stop further droid movement

            else:
                # The red droid doesn't see the green droid, so it moves randomly
                for i in range(len(self.droids)):
                    droid = self.droids[i]
                    dx, dy = random.choice(directions)
                    nx, ny = droid[0] + dx, droid[1] + dy
                    if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[nx][ny] != 1:
                        self.droids[i] = (nx, ny)

            # The green droid sees the red droid, so it runs away
            dx = red_droid_pos[0] - green_droid_pos[0]
            dy = red_droid_pos[1] - green_droid_pos[1]
            distance = (dx ** 2 + dy ** 2) ** 0.5

            if distance <= self.green_droid_visibility:
                if dx != 0:
                    dx //= abs(dx)
                if dy != 0:
                    dy //= abs(dy)
                nx, ny = green_droid_pos[0] - dx, green_droid_pos[1] - dy
                if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and grid[nx][ny] != 1:
                    self.droids[1] = (nx, ny)
                
    def show_red_droid_view(self):
        self.screen.blit(self.maze_surface, (0, 0))
        red_droid_pos = self.droids[0]
        for dx, dy in directions:
            x, y = red_droid_pos
            while 0 <= x + dx < GRID_WIDTH and 0 <= y + dy < GRID_HEIGHT and grid[x + dx][y + dy] == 0:
                x += dx
                y += dy
                pygame.draw.rect(self.screen, BLUE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.display.flip()
                pygame.time.delay(10)  # Add delay to slow down the drawing
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        self.root.destroy()


    def show_green_droid_view(self):
        self.screen.blit(self.maze_surface, (0, 0))
        green_droid_pos = self.droids[1]
        radius = self.green_droid_visibility_slider.get()
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                x, y = green_droid_pos
                if 0 <= x + dx < GRID_WIDTH and 0 <= y + dy < GRID_HEIGHT and grid[x + dx][y + dy] == 0:
                    pygame.draw.rect(self.screen, BLUE, ((x + dx) * CELL_SIZE, (y + dy) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    pygame.display.flip()
                    pygame.time.delay(10)  # Add delay to slow down the drawing
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            self.root.destroy()

    def run(self):
        self.create_droids(2)
        gui_last_update = pygame.time.get_ticks()

        while True:
            self.screen.fill(BLACK)

            self.handle_events()
            self.move_droids()

            self.draw_map()
            self.draw_droids()

            pygame.display.flip()
            self.clock.tick(60)

            # Update the GUI periodically
            current_time = pygame.time.get_ticks()
            if current_time - gui_last_update >= self.gui_update_interval:
                gui_last_update = current_time
                self.update_gui()

    def create_droids(self, num_droids):
        self.droids = []
        for _ in range(num_droids):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            self.droids.append((x, y))
            
    def game_over(self):
        # Game over logic
        print("Game Over")
        pygame.quit()
        self.root.destroy()



if __name__ == "__main__":
    seek_and_hide = SeekAndHide()
    seek_and_hide.run()
