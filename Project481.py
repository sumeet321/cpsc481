import heapq
import matplotlib.pyplot as plt

# Node class representing a point in the grid for the current position, parent node, starting node, heuristic and the total cost
class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    # Less than comparison method for heapq
    def __lt__(self, other):
        return self.f < other.f

# Heuristic function used for Manhattan distance between two nodes
def heuristic(node, goal):
    return abs(node.position[0] - goal.position[0]) + abs(node.position[1] - goal.position[1])

# A* search algorithm to open set for nodes to get evaluated and closed set for the evaluated nodes
def astar_search(start, goal, maze, ax):
    open_set = []
    closed_set = set()

    # This is for the starting node and goal node and starting the node to open set
    start_node = Node(start)
    goal_node = Node(goal)
    heapq.heappush(open_set, start_node)

    # Getting the node with lowest f value from open set
    while open_set:
        current_node = heapq.heappop(open_set)

        # If current node is the goal then reconstruct and return the path
        if current_node.position == goal_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]
        closed_set.add(current_node.position)

        # Explore neighbors and the adjacent positions
        for move in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_position = (current_node.position[0] + move[0],
                            current_node.position[1] + move[1])

            # this if is to skip if out of bounds or obstacle
            if (new_position[0] < 0 or new_position[0] >= len(maze) or
                    new_position[1] < 0 or new_position[1] >= len(maze[0])):
                continue
            if maze[new_position[0]][new_position[1]] == 1:
                continue
            if new_position in closed_set:
                continue

            # Creating a neighbor node
            neighbor_node = Node(new_position, current_node)
            neighbor_node.g = current_node.g + 1
            neighbor_node.h = heuristic(neighbor_node, goal_node)
            neighbor_node.f = neighbor_node.g + neighbor_node.h

            # Skip if there's a better node in open set then adding neighbor to open set
            if any(neighbor_node.position == node.position and neighbor_node.f >= node.f
                   for node in open_set):
                continue
            heapq.heappush(open_set, neighbor_node)

            # Visualization
            ax.plot(neighbor_node.position[1], neighbor_node.position[0], 'yo')
            plt.pause(0.1)

    return None  # if no path found

# Example maze
maze = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
    [0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
    [0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
    [0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
    [0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
    [0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# This is where the user inputs for start and goal points and setting the start point to (0,0)
gate_letter = input("Enter the gate letter you are departing from (A-N): ").upper()
gate_number = int(input("Enter the gate number you are departing from (0-14): "))
start = (0, 0)
goal = (gate_number, ord(gate_letter) - ord('A'))

# These lines are to adjust the size, display the maze and showing the start and end points
fig, ax = plt.subplots(figsize=(10, 8))
ax.imshow(maze, cmap='gray')
ax.plot(start[1], start[0], 'go')
ax.plot(goal[1], goal[0], 'ro')

# Setting custom x-axis on the bottom and y-axis labels on the left
ax.set_xticks(range(len(maze[0])))
ax.set_xticklabels(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])
ax.yaxis.tick_left()

# Calling for A* search algorithm
path = astar_search(start, goal, maze, ax)

# Displaying result and plotting the path
if path:
    print("Shortest Path:", path)
    path_x = [pos[1] for pos in path]
    path_y = [pos[0] for pos in path]
    ax.plot(path_x, path_y, 'b-')
    plt.title("A* Fastest Path for Departing Gate Visualization")
else:
    print("No path found")

# Shows the plot
plt.show()
