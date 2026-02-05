import heapq

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

def find_path(current_pos, target_pos, obstacles):
    """
    Returns the FULL list of steps (path) from start to target.
    """
    if current_pos == target_pos:
        return []

    start_node = Node(None, current_pos)
    end_node = Node(None, target_pos)

    open_list = []
    closed_list = []

    heapq.heappush(open_list, start_node)

    iterations = 0
    max_iterations = 200 # Increased for complex paths

    while len(open_list) > 0 and iterations < max_iterations:
        iterations += 1
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            curr = current_node
            while curr is not None:
                path.append(curr.position)
                curr = curr.parent
            # Return path reversed (Start -> End), excluding current position
            return path[::-1][1:] 

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] > 9 or node_position[0] < 0 or node_position[1] > 9 or node_position[1] < 0:
                continue

            if node_position in obstacles:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            if any(visited_child for visited_child in closed_list if visited_child == child):
                continue

            child.g = current_node.g + 1
            child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
            child.f = child.g + child.h

            if any(open_node for open_node in open_list if child == open_node and child.g > open_node.g):
                continue

            heapq.heappush(open_list, child)

    return [] # No path found