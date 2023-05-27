import numpy as np
def set_up_grid(grid, coords_white, coords_red):
    for row, col in coords_white:
        grid[row, col] = 1
    for row, col in coords_red:
        grid[row, col] = 2
    return grid


def calculate_reward(init_coords_white,init_coords_red, x, y,win_width=800,win_height=600,cell_col=80,cell_row=60):
    reward = 0
   

    # Set the number of cells
    cols, rows = cell_col,cell_row
    width, height = win_width,win_height

    # Set the width and height of each cell
    cell_width = width // cols
    cell_height = height // rows

    # Create a 2D array for the grid
    grid = np.zeros((cols, rows), dtype=int)


    # Set up the initial state of the grid ---------------------------------------------------------------------------
    grid = set_up_grid(grid, init_coords_white, init_coords_red)

    # Check if the cell will survive in the next generation
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

    white_neighbors = sum(1 for n in neighbors if n == 1)
    red_neighbors = sum(1 for n in neighbors if n == 2)

    # Calculate the reward based on the cell survival
    if grid[x, y] == 1:
        if red_neighbors == 3 or white_neighbors < 2 or white_neighbors > 3:
            reward -= 1  # Penalize white cell if it won't survive
        else:
            reward += 1  # Encourage white cell survival
    elif grid[x, y] == 2:
        if white_neighbors == 3 or red_neighbors < 2 or red_neighbors > 3:
            reward -= 1  # Penalize red cell if it won't survive
        else:
            reward += 1  # Encourage red cell survival


    # Encourage pattern formation
    patterns = [
        {'pattern':[[1, 1, 1], [0, 0, 0], [0, 0, 0]],'reward':2},  # Example pattern: horizontal line
        # Add more patterns here
    ]

    for pattern in patterns:
        if is_pattern_present(grid, pattern['pattern']):
            reward += pattern['reward']

    return reward


def is_pattern_present(grid, pattern):
    height, width = grid.shape
    pattern_height, pattern_width = len(pattern), len(pattern[0])

    for i in range(height - pattern_height + 1):
        for j in range(width - pattern_width + 1):
            subgrid = grid[i:i+pattern_height, j:j+pattern_width]
            if np.array_equal(subgrid, pattern):
                return True

    return False
