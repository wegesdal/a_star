import math

diagonals_allowed = False

print('diagonals allowed: {}'.format(diagonals_allowed))

grid = [
  [0,0,0,0,1,0,0,0,0],
  [0,0,0,0,1,0,0,0,0],
  [0,0,0,0,1,0,0,0,0],
  [0,0,0,0,1,0,0,0,0],
  [0,0,0,0,1,0,0,0,0],
  [0,0,0,0,1,0,0,0,0],
  [0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0]
]

class Node():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None
        self.H = 0
        self.G = 0

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return (hash(self.x) ^ hash(self.y))

start = Node(0, 0)
end = Node(7, 0)

# use this for 4-dir movement
def manhattan_distance(a, b):
  return abs(a.x - b.x) + abs(a.y - b.y)

# use this for 8-dir movement
def diagonal_distance(a, b):
    return max(abs(a.x - b.x), abs(a.y - b.y))

def walkable(n):
    if n.x >= 0 and n.y >= 0 and n.x < len(grid[0]) and n.y < len(grid):
        return grid[n.y][n.x] == 0
    else:
        return False

def retrace(node):
    path = []
    current = node
    while current.parent:
        path.append(current)
        current = current.parent
    return [(p.x, p.y) for p in path]

def astar(start, end, grid):
    open_set = set()
    closed_set = set()
    open_set.add(start)

    while open_set:
        # c is the node in openset with the minimum F value
        c = min(open_set, key=lambda o:o.G + o.H)
        if c.x == end.x and c.y == end.y:
            path = retrace(c)
            return path
        open_set.remove(c)
        closed_set.add(c)
        neighbors = [Node(c.x + 1, c.y), 
                     Node(c.x - 1, c.y + 1), 
                     Node(c.x, c.y + 1), 
                     Node(c.x, c.y - 1)]
        if diagonals_allowed:
            neighbors.extend([Node(c.x + 1, c.y + 1),
                             Node(c.x + 1, c.y - 1),
                             Node(c.x - 1, c.y + 1),
                             Node(c.x - 1, c.y - 1)])
        for n in neighbors:
            if not n in closed_set and walkable(n):
                if n in open_set:
                    new_G = c.G + 1
                    if n.G > new_G:
                        n.G = new_G
                        n.parent = c
                else:
                    n.G = c.G + 1
                    if diagonals_allowed:
                        n.H = diagonal_distance(n, end)
                    else:
                        n.H = manhattan_distance(n, end)
                    n.parent = c
                    open_set.add(n)
    print('No path found.')

# prints the whole path
print(astar(start, end, grid))

