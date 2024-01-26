from collections import deque
from consts import *

def shortest_path_binary_matrix(matrix, start, target):
    if not matrix or not matrix[0] or matrix[start[1]][start[0]] == 0 or matrix[target[1]][target[0]] == 0:
        # Invalid matrix or starting/ending point blocked
        return []

    rows, cols = len(matrix), len(matrix[0])

    # Directions for moving up, down, left, and right (no diagonals)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Initialize the queue with the starting point and path
    queue = deque([(start[1], start[0], [(start[1], start[0])])])  # (col, row, current path)
    #queue = ([(0,0 [(0,0)])])
    # the queue is able to store multiple current points and paths
    # meaning it can test all possibilities during one loop

    while queue:
        current_col, current_row, current_path = queue.popleft()
        #print(queue)

        # Check if reached the destination
        if current_row == target[1] and current_col == target[0]:
            return current_path

        # Explore neighbors
        for dr, dc in directions:
            new_row, new_col = current_row + dr, current_col + dc
            # changed the row and column to test if neighbours are moveable squares

            # Check if the neighbor is within bounds and is an open cell (1)
            if 0 <= new_row < rows and 0 <= new_col < cols and matrix[new_row][new_col] == 1:
                # Mark the cell as visited by setting it to 0
                matrix[new_row][new_col] = 0
                # Add the neighbor to the queue with an updated path
                queue.append((new_col, new_row, current_path + [(new_col, new_row)]))

    # If the queue is empty and destination is not reached, there is no path
    return []

start_square = (0, 0)
target_square = (2, 2)

shortest_path = shortest_path_binary_matrix(TRACK_GRID, start_square, target_square)
if shortest_path:
    print("Shortest path:", len(shortest_path))
    print(shortest_path)
else:
    print("No path found.")
