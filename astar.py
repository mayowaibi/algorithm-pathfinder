import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Algorithm Pathfinder")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row: int, col: int, width: int, total_rows: int) -> None:
        self.row = row
        self.col = col
        self.width = width
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.neighbors = []
        self.total_rows = total_rows
    
    # Function to get the position of the node (row, col)
    def get_pos(self):
        return self.row, self.col
    
    # The following functions check the state of the node using its colour
    def is_closed(self) -> bool:
        return self.colour == YELLOW
    
    def is_open(self) -> bool:
        return self.colour == BLUE
    
    def is_barrier(self) -> bool:
        return self.colour == BLACK
    
    def is_start(self) -> bool:
        return self.colour == ORANGE
    
    def is_end(self) -> bool:
        return self.colour == GREEN
    
    # Function to reset a node
    def reset(self) -> None:
        self.colour = WHITE

    # The following functions set the state of the node using its colour
    def set_closed(self) -> None:
        self.colour = YELLOW

    def set_open(self) -> None:
        self.colour = BLUE
    
    def set_barrier(self) -> None:
        self.colour = BLACK

    def set_start(self) -> None:
        self.colour = ORANGE

    def set_end(self) -> None:
        self.colour = GREEN

    def set_path(self) -> None:
        self.colour = RED

    # Function to draw the node in the given window
    def draw(self, win) -> None:
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    # Function to update the neighbors of the node in the given grid
    def update_neighbors(self, grid):
        self.neighbors = []
        # If any surrounding node is not a barrier, add it as a neighbor to the current node instance
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

    def __lt__(self, other) -> bool:
        return False
    
# Heuristic function to calculate the Manhattan distance between two given points
def h(p1, p2) -> int:
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Function to construct the shortest path found by the algorithm
def construct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.set_path()
        draw()

# Function to implement the A* algorithm
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    # G-Score
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    # F-Score
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        # Draw the path when the end node is found
        if current == end:
            construct_path(came_from, end, draw)
            end.set_end()
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.set_open()
        draw()
        if current != start:
            current.set_closed()

    return False


# Function to make a grid using the nodes
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

# Function to draw the gridlines for each node in the grid
def draw_gridlines(win, rows, width) -> None:
    gap = width // rows
    # Horizontal lines
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        # Vertical lines
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))

# Function to draw the entire grid containing the nodes and gridlines
def draw(win, grid, rows, width) -> None:
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)

    draw_gridlines(win, rows, width)
    pygame.display.update()

# Function to determine what node has been selected by a mouse click
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None
    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            # If user exits the window, quit the application
            if event.type == pygame.QUIT:
                run = False

            # If left mouse button is pressed, initialize the selected node 
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                # Start node
                if not start and node != end:
                    start = node
                    start.set_start()
                # End node
                elif not end and node != start:
                    end = node
                    end.set_end()
                # Barrier node
                elif node != start and node != end:
                    node.set_barrier()

            # If right mouse button is pressed, reset the selected node 
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
        
            if event.type == pygame.KEYDOWN:
                # If space bar is pressed, update neighbors and begin the algorithm
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                
                # If 'C' is pressed, clear the entire grid
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()

main(WIN, WIDTH)