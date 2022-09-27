import pygame
from pprint import PrettyPrinter
import copy
import random

pygame.init()

p = PrettyPrinter()

WIDTH = 800
HEIGHT = 800

NUM_OF_COLS = 50
BLOCK_SIZE = WIDTH / NUM_OF_COLS
NUM_OF_ROWS = int(HEIGHT / BLOCK_SIZE)

buffer = 1

win = pygame.display.set_mode((WIDTH, HEIGHT))

# RGB COLORS
WHITE = (255, 255, 255)
LIGHT_GRAY = (150, 150, 150)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)

speed = 10


def setup_grid():
    grid = []

    for i in range(NUM_OF_ROWS):
        row = []
        for j in range(NUM_OF_COLS):
            row.append(0)
        grid.append(row)

    return grid


def is_valid(grid, previous, current):
    x, y = current
    pre_x, pre_y = previous

    if x == pre_x - 1:
        if x > 0 and y < NUM_OF_ROWS - 1 and grid[x - 1][y + 1] == 0:
            return False
        if x > 0 and y > 0 and grid[x - 1][y - 1] == 0:
            return False
        if x > 0 and grid[x - 1][y] == 0:
            return False
        if y < NUM_OF_ROWS - 1 and grid[x][y + 1] == 0:
            return False
        if y > 0 and grid[x][y - 1] == 0:
            return False

        return True

    if x == pre_x + 1:
        if x < NUM_OF_COLS - 1 and y < NUM_OF_ROWS - 1 and grid[x + 1][y + 1] == 0:
            return False
        if y > 0 and x < NUM_OF_COLS - 1 and grid[x + 1][y - 1] == 0:
            return False
        if x < NUM_OF_COLS - 1 and grid[x + 1][y] == 0:
            return False
        if y < NUM_OF_ROWS - 1 and grid[x][y + 1] == 0:
            return False
        if y > 0 and grid[x][y - 1] == 0:
            return False

        return True

    if y == pre_y - 1:
        if y > 0 and x < NUM_OF_COLS - 1 and grid[x + 1][y - 1] == 0:
            return False
        if x > 0 and y > 0 and grid[x - 1][y - 1] == 0:
            return False
        if y > 0 and grid[x][y - 1] == 0:
            return False
        if x > 0 and grid[x - 1][y] == 0:
            return False
        if x < NUM_OF_COLS - 1 and grid[x + 1][y] == 0:
            return False

        return True

    if y == pre_y + 1:
        if x < NUM_OF_COLS - 1 and y < NUM_OF_ROWS - 1 and grid[x + 1][y + 1] == 0:
            return False
        if x > 0 and y < NUM_OF_ROWS - 1 and grid[x - 1][y + 1] == 0:
            return False
        if y < NUM_OF_ROWS - 1 and grid[x][y + 1] == 0:
            return False
        if x > 0 and grid[x - 1][y] == 0:
            return False
        if x < NUM_OF_COLS - 1 and grid[x + 1][y] == 0:
            return False

        return True


def get_direction(previous, current):
    pre_x, pre_y = previous
    x, y = current

    print()
    print(previous)
    print(current)
    print()

    if x - 1 == pre_x:
        print("down")
        straight = (x + 1, y)
        left = (x, y - 1)
        right = (x, y + 1)
    elif x + 1 == pre_x:
        print("up")
        straight = (x - 1, y)
        left = (x, y + 1)
        right = (x, y - 1)
    elif y - 1 == pre_y:
        print("right")
        straight = (x, y + 1)
        left = (x + 1, y)
        right = (x - 1, y)
    elif y + 1 == pre_y:
        print("left")
        straight = (x, y - 1)
        left = (x - 1, y)
        right = (x + 1, y)
    else:
        return {(x + 1, y): "straight", (x - 1, y): "straight", (x, y + 1): "straight", (x, y - 1): "straight"}

    return {straight: "straight", right: "right", left: "left"}


def setup_maze_prims(grid, start=None):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j] = 1

    if start is None:
        first = 0, 0
    else:
        first = start

    queue = []

    first_x, first_y = first
    grid[first_x][first_y] = 0

    first_neighbors = get_neighbors(first_x, first_y, grid, inverted=True)
    for neighbor in first_neighbors:
        if is_valid(grid, first, neighbor):
            queue.append((neighbor, first))

    while len(queue) != 0:
        current, previous = queue.pop(random.randint(0, len(queue) - 1))
        x, y = current
        pre_x, pre_y = previous

        if is_valid(grid, (pre_x, pre_y), (x, y)) is False:
            continue

        grid[x][y] = 0
        update(grid)
        pygame.time.delay(speed)

        neighbors = get_neighbors(x, y, grid, inverted=True)
        for neighbor in neighbors:
            if is_valid(grid, (x, y), neighbor):
                queue.append((neighbor, (x, y)))

    return grid


def setup_maze(grid, start=None):
    print("setting up maze")
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j] = 1

    print("setting start")
    if start is None:
        first = 0, 0
    else:
        first = start

    queue = []
    temp_queue = []

    first_x, first_y = first
    grid[first_x][first_y] = 0

    first_neighbors = get_neighbors(first_x, first_y, grid, inverted=True)
    for neighbor in first_neighbors:
        if is_valid(grid, first, neighbor):
            temp_queue.append(neighbor)

    pre_x, pre_y = first_x, first_y
    x, y = first_x, first_y

    just_turned = False
    while len(queue) != 0 or len(temp_queue) != 0:
        if len(temp_queue) == 0:
            current, previous = queue.pop(len(queue) - 1)
            x, y = current
            pre_x, pre_y = previous
        else:
            directions = get_direction((pre_x, pre_y), (x, y))
            inv_directions = {v: k for k, v in directions.items()}

            if just_turned:
                if inv_directions["straight"] in temp_queue:
                    pre_x, pre_y = x, y
                    x, y = inv_directions["straight"]
                else:
                    pre_x, pre_y = x, y
                    x, y = temp_queue.pop(random.randint(0, len(temp_queue) - 1))
                just_turned = False
            else:
                pre_x, pre_y = x, y
                x, y = temp_queue.pop(random.randint(0, len(temp_queue) - 1))

                print(directions)
                print(x, y)

                if directions[x, y] != "straight":
                    just_turned = True

        if is_valid(grid, (pre_x, pre_y), (x, y)) is False:
            continue

        grid[x][y] = 0
        update(grid)
        pygame.time.delay(0)

        for node in temp_queue:
            queue.append((node, (pre_x, pre_y)))
        temp_queue = []

        neighbors = get_neighbors(x, y, grid, inverted=True)
        for neighbor in neighbors:
            if is_valid(grid, (x, y), neighbor):
                temp_queue.append(neighbor)

    return grid


def draw_block(win, row, col, color):
    pygame.draw.rect(win, color, (BLOCK_SIZE * col, BLOCK_SIZE * row, BLOCK_SIZE, BLOCK_SIZE))
    # pygame.draw.rect(win, color, (BLOCK_SIZE * col + buffer, BLOCK_SIZE * row + buffer,
                                  # BLOCK_SIZE - 2 * buffer, BLOCK_SIZE - 2 * buffer))


def get_neighbors(x, y, grid, inverted=False):
    neighbors = []

    value = 1
    if inverted:
        value = 0

    # RIGHT
    if x < NUM_OF_COLS - 1 and grid[x + 1][y] != value:
        neighbors.append((x + 1, y))
    # TOP
    if y > 0 and grid[x][y - 1] != value:
        neighbors.append((x, y - 1))
    # LEFT
    if x > 0 and grid[x - 1][y] != value:
        neighbors.append((x - 1, y))
    # BOTTOM
    if y < NUM_OF_ROWS - 1 and grid[x][y + 1] != value:
        neighbors.append((x, y + 1))

    return neighbors


def backtrack(start, end, key, grid):
    x, y = end
    grid[x][y] = 6
    update(grid)

    current = x, y
    while current != start:
        current = key[x, y]
        x, y = current
        grid[x][y] = 6

        update(grid)
        pygame.time.delay(speed)

    return grid


def breadth_first_search(grid, start, end):
    start_x, start_y = start
    solution = {(start_x, start_y): (start_x, start_y)}

    queue = get_neighbors(start_x, start_y, grid)
    visited = [start]

    for x, y in queue:
        solution[x, y] = start_x, start_y
        grid[x][y] = 4

    while len(queue) != 0:
        x, y = queue.pop(0)

        if (x, y) == end:
            return backtrack(start, end, solution, grid)

        visited.append((x, y))
        grid[x][y] = 5

        neighbors = get_neighbors(x, y, grid)

        for neighbor in neighbors:
            row, col = neighbor

            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)
                solution[row, col] = x, y
                grid[row][col] = 4

        update(grid)
        pygame.time.delay(speed)

    return grid


def depth_first_search(grid, start, end):
    start_x, start_y = start
    solution = {(start_x, start_y): (start_x, start_y)}

    queue = get_neighbors(start_x, start_y, grid)
    visited = [start]

    for x, y in queue:
        solution[x, y] = start_x, start_y
        grid[x][y] = 4

    while len(queue) != 0:
        x, y = queue.pop(len(queue) - 1)

        if (x, y) == end:
            return backtrack(start, end, solution, grid)

        visited.append((x, y))
        grid[x][y] = 5

        neighbors = get_neighbors(x, y, grid)

        for neighbor in neighbors:
            row, col = neighbor

            if neighbor not in visited and neighbor not in queue:
                queue.append(neighbor)
                solution[row, col] = x, y
                grid[row][col] = 4

        update(grid)
        pygame.time.delay(speed)

    return grid


def update(grid):
    win.fill(WHITE)

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 0:
                draw_block(win, row, col, WHITE)
            elif grid[row][col] == 1:
                draw_block(win, row, col, BLACK)
            elif grid[row][col] == 4:
                draw_block(win, row, col, YELLOW)
            elif grid[row][col] == 5:
                draw_block(win, row, col, ORANGE)
            elif grid[row][col] == 2:
                draw_block(win, row, col, GREEN)
            elif grid[row][col] == 6:
                draw_block(win, row, col, GREEN)
            else:
                draw_block(win, row, col, RED)

    pygame.display.update()


def main():
    running = True

    grid = setup_grid()
    copy_grid = copy.deepcopy(grid)
    copy_grid_maze = None

    start = None
    end = None

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                col = int(mouse_x // BLOCK_SIZE)
                row = int(mouse_y // BLOCK_SIZE)

                if start is None:
                    grid[row][col] = 2
                    start = (row, col)

                elif end is None:
                    grid[row][col] = 3
                    end = (row, col)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    grid = copy_grid
                    start = None
                    end = None
                if event.key == pygame.K_r and copy_grid_maze is not None:
                    grid = copy_grid_maze
                    start = None
                    end = None
                if event.key == pygame.K_m:
                    if start is None:
                        grid = setup_maze(grid)
                        copy_grid_maze = copy.deepcopy(grid)
                    else:
                        grid = setup_maze_prims(grid, start)
                        copy_grid_maze = copy.deepcopy(grid)

                        x, y = start
                        grid[x][y] = 2
                        end = None
                if event.key == pygame.K_d:
                    grid = depth_first_search(grid, start, end)
                if event.key == pygame.K_b:
                    grid = breadth_first_search(grid, start, end)

        update(grid)

    quit()


if __name__ == "__main__":
    main()
