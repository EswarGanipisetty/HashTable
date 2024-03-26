class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class HashTable:
    def __init__(self, initial_capacity=16, load_factor=0.75, growth_factor=2, shrink_factor=0.25):
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.growth_factor = growth_factor
        self.shrink_factor = shrink_factor
        self.size = 0
        self.table = [None] * self.capacity

    def hash_function(self, key):
        # Multiplication method for hash function
        A = 0.61803398875  # The golden ratio
        hash_value = int(self.capacity * ((key * A) % 1))
        return hash_value

    def insert(self, key, value):
        index = self.hash_function(key)
        node = self.table[index]

        # Check if key already exists, if so, update value
        while node is not None:
            if node.key == key:
                node.value = value
                return
            node = node.next

        # Key doesn't exist, insert new node at the beginning of the chain
        new_node = Node(key, value)
        new_node.next = self.table[index]
        if self.table[index] is not None:
            self.table[index].prev = new_node
        self.table[index] = new_node
        self.size += 1

        # Check if resize is needed
        if self.size / self.capacity >= self.load_factor:
            self.resize(self.capacity * self.growth_factor)

    def remove(self, key):
        index = self.hash_function(key)
        node = self.table[index]

        # Search for the key and remove if found
        while node is not None:
            if node.key == key:
                if node.prev is None:
                    self.table[index] = node.next
                else:
                    node.prev.next = node.next
                if node.next is not None:
                    node.next.prev = node.prev
                self.size -= 1
                break
            node = node.next

        # Check if resize is needed
        if self.size / self.capacity <= self.shrink_factor and self.capacity > 16:
            self.resize(self.capacity // self.growth_factor)

    def get(self, key):
        index = self.hash_function(key)
        node = self.table[index]

        # Search for the key and return value if found
        while node is not None:
            if node.key == key:
                return node.value
            node = node.next

        return None

    def resize(self, new_capacity):
        new_table = [None] * new_capacity
        self.capacity = new_capacity

        # Re-hash all elements into the new table
        for node in self.table:
            while node is not None:
                next_node = node.next
                index = self.hash_function(node.key)
                node.next = new_table[index]
                if new_table[index] is not None:
                    new_table[index].prev = node
                new_table[index] = node
                node.prev = None
                node = next_node

        self.table = new_table

    def print_table(self):
        for i in range(self.capacity):
            print(f"Bucket {i}:", end=" ")
            node = self.table[i]
            while node is not None:
                print(f"({node.key}: {node.value})", end=" ")
                node = node.next
            print()


# Example usage
if __name__ == "__main__":
    hash_table = HashTable()
    hash_table.insert(1, 10)
    hash_table.insert(2, 20)
    hash_table.insert(3, 30)
    hash_table.insert(4, 40)
    hash_table.insert(5, 50)

    print("Hash Table with initial capacity:")
    hash_table.print_table()

    print("\nValue for key 3:", hash_table.get(3))

    hash_table.remove(3)
    print("\nHash Table after removing key 3:")
    hash_table.print_table()

    hash_table.insert(6, 60)
    hash_table.insert(7, 70)
    hash_table.insert(8, 80)
    hash_table.insert(9, 90)

    print("\nHash Table after resizing:")
    hash_table.print_table()
