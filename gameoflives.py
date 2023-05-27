import pygame
import numpy as np
# import os
# os.environ['SDL_VIDEODRIVER']='dummy'


def set_up_grid(grid, coords_white, coords_red):
    for row, col in coords_white:
        grid[row, col] = 1
    for row, col in coords_red:
        grid[row, col] = 2
    return grid


def run_game(init_coords_white, init_coords_red, win_width=800,win_height=600,cell_col=80,cell_row=60):
    # Initialize pygame ------------------------------------------------------------------------------------------------

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (227, 116, 127)

    # Initialize Pygame
    pygame.init()

    # Set the width and height of the screen
    width, height = win_width,win_height
    screen = pygame.display.set_mode((width, height))

    # Set the number of cells
    cols, rows = cell_col,cell_row

    # Set the width and height of each cell
    cell_width = width // cols
    cell_height = height // rows

    # Create a 2D array for the grid
    grid = np.zeros((cols, rows), dtype=int)


    # Set up the initial state of the grid ---------------------------------------------------------------------------
    grid = set_up_grid(grid, init_coords_white, init_coords_red)

    
    iteration = 0
    # Game loop ------------------------------------------------------------------------------------------------------
    running = True
    while running:
        iteration += 1
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill(BLACK)

        # Draw the cells ---------------------------------------------------------------------------------------------
        for x in range(cols):
            for y in range(rows):
                # draw white
                if grid[x, y] == 1:
                    pygame.draw.rect(
                        screen,
                        WHITE,
                        (x * cell_width, y * cell_height, cell_width, cell_height),
                    )
                # draw red
                if grid[x, y] == 2:
                    pygame.draw.rect(
                        screen,
                        RED,
                        (x * cell_width, y * cell_height, cell_width, cell_height),
                    )    

        # Copy the grid to avoid modifying it while evaluating the next generation
        next_grid = grid.copy()

        # Calculate the next generation ------------------------------------------------------------------------------
        for x in range(cols):
            for y in range(rows):
                # get coords of neighbors
                neighbor_coords = [
                (x - 1, y),
                (x + 1, y),
                (x, y - 1),
                (x, y + 1),
                (x - 1, y - 1),
                (x + 1, y - 1),
                (x - 1, y + 1),
                (x + 1, y + 1)
                ]
                neighbors = [grid[nx, ny] for nx, ny in neighbor_coords if 0 <= nx < cols and 0 <= ny < rows]
                
                # count number of each color
                white_neighbors, red_neighbors = 0,0
                for n in neighbors:
                    if n==1:
                        white_neighbors+=1
                    if n==2:
                        red_neighbors+=1

                # Apply updated Conway's rules ------------------------------------------------------------------------------

                # if block was white
                if grid[x, y] == 1:
                    # "eaten"
                    if red_neighbors == 3:  
                        next_grid[x, y] = 2

                    # dies
                    elif (white_neighbors < 2 or white_neighbors > 3):
                        next_grid[x, y] = 0
                     
                    # lives
                    else:
                        next_grid[x, y] = 1

                # if block was red
                elif grid[x, y] == 2:
                    # "eaten"
                    if white_neighbors == 3:  
                        next_grid[x, y] = 1

                    # dies
                    elif (red_neighbors < 2 or red_neighbors > 3):
                        next_grid[x, y] = 0
                     
                    # lives
                    else:
                        next_grid[x, y] = 2

                # if block was empty                 
                else:
                    # turns white
                    if white_neighbors == 3 and red_neighbors !=3:
                        next_grid[x, y] = 1
                    # turns red
                    elif white_neighbors !=3 and red_neighbors == 3:
                        next_grid[x, y] = 2
                    
                    

        # Update the grid --------------------------------------------------------------------------------------------
        grid = next_grid


        # Update the screen
        pygame.display.flip()

        # Slow down game speed
        pygame.time.wait(20)
    # Quit the game
    pygame.quit()
    print(iteration)

# testing ------------------------------------------------------------------------------------------------------------------------
import random
from nn import calculate_reward
init_points_white, init_points_red = [],[]

for i in range(1000):
    y1, x1 = random.randint(0, 39), random.randint(0, 59)
    y2, x2 = random.randint(0, 39), random.randint(0, 59)
    init_points_white.append([y1, x1])
    init_points_red.append([y2 + 40, x2])
    print(calculate_reward(init_points_white, init_points_red, x1,y1))



run_game(init_points_white,init_points_red)