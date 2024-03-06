import heapq
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Cost from start node to current node
        self.h = 0  # Heuristic (estimated cost from current node to goal node)
        self.f = 0  # Total cost (g + h)

    def __lt__(self, other):
        return self.f < other.f

def heuristic(node, goal):
    # Manhattan distance heuristic
    return abs(node.position[0] - goal.position[0]) + abs(node.position[1] - goal.position[1])

def astar_search(start, goal, maze, ax):
    open_set = []
    closed_set = set()

    start_node = Node(start)
    goal_node = Node(goal)

    heapq.heappush(open_set, start_node)

    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node.position == goal_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Return reversed path

        closed_set.add(current_node.position)

        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # Adjacent positions
            new_position = (current_node.position[0] + move[0],
                            current_node.position[1] + move[1])

            if (new_position[0] < 0 or new_position[0] >= len(maze) or
                    new_position[1] < 0 or new_position[1] >= len(maze[0])):
                continue

            if maze[new_position[0]][new_position[1]] == 1:  # Check if obstacle
                continue

            if new_position in closed_set:
                continue

            neighbor_node = Node(new_position, current_node)
            neighbor_node.g = current_node.g + 1
            neighbor_node.h = heuristic(neighbor_node, goal_node)
            neighbor_node.f = neighbor_node.g + neighbor_node.h

            if any(neighbor_node.position == node.position and neighbor_node.f >= node.f
                   for node in open_set):
                continue

            heapq.heappush(open_set, neighbor_node)

            # Visualization
            ax.plot(neighbor_node.position[1], neighbor_node.position[0], 'yo')
            plt.pause(0.1)

    return None  # No path found

# Example usage:
maze = [
    [0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0]
]

gate_letter = input("Enter the gate letter you are departing from (A-G): ").upper()
gate_number = int(input("Enter the gate number you are departing from (1-7): "))
start = (0, 0)
goal = (gate_number, ord(gate_letter) - ord('A'))
#goal = (ord(gate_letter) - ord('A'), gate_number - 1)
#goal = (6, ord(gate_letter) - ord('A'))
#goal = (6, 6)

fig, ax = plt.subplots(figsize=(10, 8))  # Adjust the size here
ax.imshow(maze, cmap='gray')
ax.plot(start[1], start[0], 'go')  # Start point
ax.plot(goal[1], goal[0], 'ro')  # Goal point

# Set custom x-axis labels
ax.set_xticks(range(len(maze[0])))
ax.set_xticklabels(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
ax.yaxis.tick_right()  # Move y-axis labels to the right side


path = astar_search(start, goal, maze, ax)

if path:
    print("Shortest Path:", path)
    path_x = [pos[1] for pos in path]
    path_y = [pos[0] for pos in path]
    ax.plot(path_x, path_y, 'b-')  # Plot the path
    plt.title("A* Fastest Path for Departing Gate Visualization")
else:
    print("No path found")

plt.show()
