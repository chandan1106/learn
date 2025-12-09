from typing import Optional, Any

class Node:
    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        # Dummy Head (MRU) and Tail (LRU)
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add(self, node: Node):
        # Always add right after Head
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.value
        return -1

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            node.value = value
            self._add(node)
        else:
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add(new_node)
            if len(self.cache) > self.capacity:
                lru = self.tail.prev # Victim is right before Tail
                print(f"[Cache] Capacity Full! Evicting Key: {lru.key}")
                self._remove(lru)
                del self.cache[lru.key]

# --- TEST HARNESS ---
print("--- INITIALIZING CACHE (Capacity=2) ---")
lru = LRUCache(2)

print("1. Put (1, 1)")
lru.put(1, 1)
print("2. Put (2, 2)")
lru.put(2, 2)

print("3. Get (1) -> This makes Key 1 the 'Most Recently Used'")
val = lru.get(1)
print(f"   Value: {val}")

print("4. Put (3, 3) -> Should evict Key 2 (because 1 was just used)")
lru.put(3, 3)

print("5. Check Status:")
if lru.get(2) == -1:
    print(" Key 2 was correctly evicted.")
else:
    print(" ERROR: Key 2 should be gone.")

if lru.get(1) != -1:
    print(" Key 1 is still safe.")