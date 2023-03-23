

class MRV_Node:
    def __init__(self, value, ycord, xcord, next = None):
        self.value = value
        self.ycord = ycord
        self.xcord = xcord
        self.next = next

class MRV_Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert(self, node):
        if self.head == None:
            self.head = node
            node.next = self.tail

        elif self.head.value > node.value:
            node.next = self.head
            self.head = node

        else:
            current = self.head
            while current.next != None and current.next.value < node.value:
                current = current.next

            node.next = current.next
            current.next = node
                    
        self.size += 1

    def pop(self):
        ret = self.head
        self.head = self.head.next
        self.size -= 1

        return ret
    

    def update_node(self, y, x, new_val):
        if self.head != None:
            current = self.head
            if current.ycord == y and current.xcord == x:
                self.head = self.head.next
                self.size -= 1
            else:
                while current.next != None:
                    if current.next.ycord == y and current.next.xcord == x:
                        current.next = current.next.next
                        self.size -= 1
                        break
                    current = current.next

        
        new_node = MRV_Node(new_val, y, x)
        self.insert(new_node)

    
    

if __name__ == "__main__":
    node1 = MRV_Node(3, 2, 2)
    node2 = MRV_Node(3, 1, 2)
    node3 = MRV_Node(1, 3, 2)
    node4 = MRV_Node(2, 4, 4)

    q = MRV_Queue()

    q.insert(node1)
    q.insert(node2)
    q.insert(node3)
    q.insert(node4)

    q.update_node(3, 2, 5)
    print()