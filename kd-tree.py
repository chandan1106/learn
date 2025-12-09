from typing import List, Tuple, Optional
import pprint

# --- DATA STRUCTURES ---
class Node:
    def __init__(self, point: Tuple[int, int], left=None, right=None):
        self.point = point
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"Node({self.point})"

# --- ALGORITHMS ---
def build_kdtree(points: List[Tuple[int, int]], depth: int = 0) -> Optional[Node]:
    if not points:
        return None
    
    k = 2 # 2 Dimensions (x, y)
    axis = depth % k
    
    # 1. Sort by current axis (x or y)
    points.sort(key=lambda x: x[axis])
    
    # 2. Find Median
    median = len(points) // 2
    
    # 3. Create Node and Recursefrom typing import List, Tuple, Optional
import pprint

# --- DATA STRUCTURES ---
class Node:
    def __init__(self, point: Tuple[int, int], left=None, right=None):
        self.point = point
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"Node({self.point})"

# --- ALGORITHMS ---
def build_kdtree(points: List[Tuple[int, int]], depth: int = 0) -> Optional[Node]:
    if not points:
        return None
    
    k = 2 # 2 Dimensions (x, y)
    axis = depth % k
    
    # 1. Sort by current axis (x or y)
    points.sort(key=lambda x: x[axis])
    
    # 2. Find Median
    median = len(points) // 2
    
    # 3. Create Node and Recurse
    return Node(
        point=points[median],
        left=build_kdtree(points[:median], depth + 1),
        right=build_kdtree(points[median + 1:], depth + 1)
    )

def search_kdtree(node: Optional[Node], target: Tuple[int, int], depth: int = 0) -> bool:
    if node is None:
        return False
    if node.point == target:
        return True
        
    axis = depth % 2
    
    # Visualizing the path taken
    print(f"Checking {node.point} at depth {depth} (Axis {'X' if axis==0 else 'Y'})...")
    
    if target[axis] < node.point[axis]:
        return search_kdtree(node.left, target, depth + 1)
    else:
        return search_kdtree(node.right, target, depth + 1)

# --- SIMULATION ---
print("--- BUILDING VECTOR INDEX (KD-TREE) ---")
# These represent document vectors in 2D space
vectors = [(3, 6), (17, 15), (13, 15), (6, 12), (9, 1), (2, 7), (10, 19)]

# Build the tree
index_root = build_kdtree(vectors)
print("Tree Built Successfully.")

print("\n--- SEARCHING FOR VECTOR (9, 1) ---")
# We want to find the vector (9, 1). 
# A linear search would check 7 items. The tree should check fewer.
found = search_kdtree(index_root, (9, 1))

if found:
    print(" TARGET FOUND")
else:
    print("TARGET NOT FOUND")

print("\n--- SEARCHING FOR MISSING VECTOR (99, 99) ---")
found_missing = search_kdtree(index_root, (99, 99))
if not found_missing:
    print(" MISSING VECTOR CORRECTLY NOT FOUND")
    return Node(
        point=points[median],
        left=build_kdtree(points[:median], depth + 1),
        right=build_kdtree(points[median + 1:], depth + 1)
    )

def search_kdtree(node: Optional[Node], target: Tuple[int, int], depth: int = 0) -> bool:
    if node is None:
        return False
    if node.point == target:
        return True
        
    axis = depth % 2
    
    # Visualizing the path taken
    print(f"Checking {node.point} at depth {depth} (Axis {'X' if axis==0 else 'Y'})...")
    
    if target[axis] < node.point[axis]:
        return search_kdtree(node.left, target, depth + 1)
    else:
        return search_kdtree(node.right, target, depth + 1)

# --- SIMULATION ---
print("--- BUILDING VECTOR INDEX (KD-TREE) ---")
# These represent document vectors in 2D space
vectors = [(3, 6), (17, 15), (13, 15), (6, 12), (9, 1), (2, 7), (10, 19)]

# Build the tree
index_root = build_kdtree(vectors)
print("Tree Built Successfully.")

print("\n--- SEARCHING FOR VECTOR (9, 1) ---")
# We want to find the vector (9, 1). 
# A linear search would check 7 items. The tree should check fewer.
found = search_kdtree(index_root, (9, 1))

if found:
    print(" TARGET FOUND")
else:
    print(" TARGET NOT FOUND")

print("\n--- SEARCHING FOR MISSING VECTOR (99, 99) ---")
found_missing = search_kdtree(index_root, (99, 99))
if not found_missing:
    print("MISSING VECTOR CORRECTLY NOT FOUND")