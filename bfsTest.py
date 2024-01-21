from collections import deque
from consts import *

def shortest_path_binary_matrix(matrix, start, target):
    if not matrix or not matrix[0] or matrix[start[0]][start[1]] == 0 or matrix[target[0]][target[1]] == 0:
        # Invalid matrix or starting/ending point blocked
        return []

    rows, cols = len(matrix), len(matrix[0])

    # Directions for moving up, down, left, and right (no diagonals)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Initialize the queue with the starting point and path
    queue = deque([(start[0], start[1], [(start[0], start[1])])])  # (row, col, current path)

    while queue:
        current_row, current_col, current_path = queue.popleft()

        # Check if reached the destination
        if current_row == target[0] and current_col == target[1]:
            return current_path

        # Explore neighbors
        for dr, dc in directions:
            new_row, new_col = current_row + dr, current_col + dc

            # Check if the neighbor is within bounds and is an open cell (1)
            if 0 <= new_row < rows and 0 <= new_col < cols and matrix[new_row][new_col] == 1:
                # Mark the cell as visited by setting it to 0
                matrix[new_row][new_col] = 0
                # Add the neighbor to the queue with an updated path
                queue.append((new_row, new_col, current_path + [(new_row, new_col)]))

    # If the queue is empty and destination is not reached, there is no path
    return []

# Example usage:
binary_matrix = [
    [1, 0, 1, 1, 1],
    [1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1],
    [0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
]

start_square = (0, 0)
target_square = (6, 4)

shortest_path = shortest_path_binary_matrix(TRACK_GRID, start_square, target_square)
if shortest_path:
    print("Shortest path:", len(shortest_path))
    print(shortest_path)
else:
    print("No path found.")
