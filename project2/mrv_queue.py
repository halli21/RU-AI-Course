

class MRV_Node:
    def __init__(self, value, ycord, xcord, next = None):
        self.value = value
        self.ycord = ycord
        self.xord = xcord
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

        return ret
    
    

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
    print()