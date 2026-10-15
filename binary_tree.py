class BinaryNode:
    def __init__(self, weight=None, parent=None, left=None, right=None):
        self.weight = weight
        self.parent = parent
        self.left = left
        self.right = right

    @classmethod
    def from_weight(cls, weight, parent = None):
        return cls(weight, parent) 

    def add_new_left(self, weight):
        # Orphans previous entry before overwrite
        if self.left is not None:
            self.left.parent = None

        self.left = self.from_weight(weight, self)
        return self.left

    def add_new_right(self, weight):
        # Orphans previous entry before overwrite
        if self.right is not None:
            self.right.parent = None
        
        self.right = self.from_weight(weight, self)
        return self.right

    def replace_left_child(self, node):
        old_child = self.left

        if old_child is not None:
            old_child.orphan()

        if not node.is_root():
            node.orphan()

        self.left = node
        node.parent = self

        return old_child

    def replace_right_child(self, node):
        old_child = self.right

        if old_child is not None:
            old_child.orphan()

        if not node.is_root():
            node.orphan()

        self.right = node
        node.parent = self

        return old_child

    def orphan(self):
        if self.is_root():
            return

        if self.is_left_child():
            self.parent.left = None

        if self.is_right_child():
            self.parent.right = None

        self.parent = None

    def is_leaf(self):
        return self.left is None and self.right is None

    def is_root(self):
        return self.parent is None

    def is_left_child(self):
        if self.is_root():
            return False
        
        return self is self.parent.left

    def is_right_child(self):
        if self.is_root():
            return False
        
        return self is self.parent.right

    def n_children(self):
        if self.is_leaf():
            return 0
        elif self.left is not None and self.right is not None:
            return 2
        else:
            return 1

    def depth(self):
        count = 0
        node = self

        while not node.is_root():
            node = node.parent
            count += 1

        return count

    def subtree_height(self):
        # Initial value offset by -1 to compensate for guaranteed addition on return
        h_left  = -1 if self.left  is None else self.left.subtree_height()
        h_right = -1 if self.right is None else self.right.subtree_height()

        return max(h_left, h_right) + 1

    def subtree_skew(self):
        return self.right.subtree_height() - self.left.subtree_height()

    def subtree_first(self):
        if self.left is None:
            return self
        
        return self.left.subtree_first()

    def subtree_last(self):
        if self.right is None:
            return self

        return self.right.subtree_last()

    def subtree_size(self):
        left_size  = self.left.subtree_size() if self.left is not None else 0
        right_size  = self.right.subtree_size() if self.right is not None else 0
        
        return left_size + 1 + right_size
        
    def next(self):
        # If right child exists, next is the start of the subtree rooted by the right child
        if self.right is not None:
             return self.right.subtree_first()
        
        # If no right child, walk up the tree until we go up a parent's left branch
        else:
            node = self
            while 1:
                if node.is_root():
                    return None
                elif not node.is_left_child():
                    node = node.parent
                else:
                    return node.parent

    def prev(self):
        # If left child exists, prev is the last of the subtree rooted by the left child
        if self.left is not None:
            return self.left.subtree_last()

        # If no left child, walk up the tree until we go up a parent's right branch
        else: 
            node = self
            while 1:
                if node.is_root():
                    return None
                elif not node.is_right_child():
                    node = node.parent
                else:
                    return node.parent

    def find_node_by_weight(self, weight):
        node = self.subtree_first()

        while node is not None:
            if node.weight == weight:
                return node
            
            node = node.next()

        return None

    def insert_new_after(self, weight):
        if self.right is None:
            new_node = self.add_new_right(weight)

        else:
            new_node = self.right.subtree_first().add_new_left(weight)    

        return new_node
        
    def insert_new_before(self, weight):
        if self.left is None:
            new_node = self.add_new_left(weight)

        else:
            new_node = self.left.subtree_last().add_new_right(weight)

        return new_node

    def swap(self, node):
        current = self.weight

        self.weight = node.weight
        node.weight = current

        return node

    def subtree_detach(self):
        if self.is_left_child():
            self.parent.left = None

        elif self.is_right_child():
            self.parent.right = None

        self.parent = None

        return self

    def delete(self):
        if self.is_leaf():
           self.subtree_detach() 
           return

        elif self.left is not None:
            new_node = self.prev()

        elif self.right is not None:
            new_node = self.next()

        self.swap(new_node)
        new_node.delete()

    def subtree_rotate_left(self):
        if self.right is None:
            return self

        right_child = self.right
        right_child_left_subtree = self.right.left

        if self.is_left_child():
            self.parent.replace_left_child(right_child)

        elif self.is_right_child():
            self.parent.replace_right_child(right_child)

        else:
            right_child.orphan()

        right_child.replace_left_child(self)

        if right_child_left_subtree is not None:
            self.replace_right_child(right_child_left_subtree)
        
        return self.parent

    def subtree_rotate_right(self):
        if self.left is None:
            return self
        
        left_child = self.left
        left_child_right_subtree = self.left.right

        if self.is_left_child():
            self.parent.replace_left_child(left_child)

        elif self.is_right_child():
            self.parent.replace_right_child(left_child)

        else:
            left_child.orphan()

        left_child.replace_right_child(self)
        
        if left_child_right_subtree is not None:
            self.replace_left_child(left_child_right_subtree)

        return self.parent

class AVLNode(BinaryNode):
    def __init__(self, weight=None, parent=None, left=None, right=None):
        super().__init__(weight, parent, left, right)
        self.height = 0

    def subtree_height(self):
        return self.height

    def subtree_get_at(self, index):
        node = AVLNode()
        return node

    def subtree_insert_new_at(self, index, weight):
        next_node = self.subtree_get_at(index)
        next_node.insert_new_before(weight)
        next_node.height = 0
        
    def subtree_balance(self):
        match self.subtree_skew():
            case -1 | 0 | 1:
                pass

            case -2: # left-heavy
                self.balance_rightward()
            
            case 2: # right-heavy
                self.balance_leftward()

            case _:
                print("Tree balance error. Please reconstruct")

    def balance_leftward(self):
        if self.right.subtree_skew == -1:
            self.right.subtree_rotate_right()

        self.subtree_rotate_left()


    def balance_rightward(self):
        if self.left.subtree_skew == 1:
            self.left.subtree_rotate_left()

        self.subtree_rotate_right()

class BSTNode(BinaryNode):
    def insert_new(self, weight):
        return

    def insert_new_before(self, weight):
        return NotImplementedError

    def insert_new_after(self, weight):
        return NotImplementedError

    def find_node_by_weight(self, weight):
        raise NotImplementedError


if __name__ == "__main__":
    ## BUILD
    root = BinaryNode.from_weight('A')
    root.add_new_left('B')
    root.add_new_right('C')
    root.left.add_new_left('D')
    root.left.add_new_right('E')
    root.left.left.add_new_left('F')

    ## INSERTION
    root.left.right.insert_new_before('G')
    root.insert_new_after('H')

    ## TRAVERSAL ORDER
    first = root.subtree_first()
    print(first.weight)
    current = first.next()
    while current is not None:
        print(current.weight)
        current = current.next()

    print('done')