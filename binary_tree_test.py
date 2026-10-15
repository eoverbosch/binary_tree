import pytest
from binary_tree import BinaryNode

# Rudimentary test to see if the fixture is even capable of initialisation
def test_initialisation():
    root = BinaryNode.from_weight('A')
    assert root.weight == 'A'

    root.add_new_left('B')
    root.add_new_right('C')

    assert root.left.weight == 'B'
    assert root.left.parent.weight == 'A'

    assert root.right.weight == 'C'
    assert root.right.parent.weight == 'A'

@pytest.fixture
def pre_insert_example_tree():
    root = BinaryNode.from_weight('A')
    root.add_new_left('B')
    root.add_new_right('C')
    root.left.add_new_left('D')
    root.left.add_new_right('E')
    root.left.left.add_new_left('F')

    return root

@pytest.fixture
def example_tree():
    root = BinaryNode.from_weight('A')
    root.add_new_left('B')
    root.add_new_right('C')
    root.left.add_new_left('D')
    root.left.add_new_right('E')
    root.left.left.add_new_left('F')

    root.left.right.add_new_left('G')
    root.right.add_new_left('H')

    return root

def test_traversal_order(pre_insert_example_tree):
    correct_order = ['F', 'D', 'B', 'E', 'A', 'C']
    assert list(pre_insert_example_tree) == correct_order

def test_inorder_insertion(pre_insert_example_tree):
    root = pre_insert_example_tree
    node_E = root.left.right
    node_C = root.right

    node_E.insert_new_before('G')
    root.insert_new_after('H')

    assert node_E.left.weight == 'G'
    assert node_C.left.weight == 'H'

    correct_order = ['F', 'D', 'B', 'G', 'E', 'A', 'H', 'C']
    assert list(root) == correct_order

def test_inorder_deletion(example_tree):
    example_tree.delete()

    assert example_tree.is_root()
    assert example_tree.weight == 'E'

    correct_order = ['F', 'D', 'B', 'G', 'E', 'H', 'C']
    assert list(example_tree) == correct_order

def test_subtree_height(example_tree):
    assert example_tree.subtree_height() == 3
    assert example_tree.right.subtree_height() == 1
    assert example_tree.left.left.left.subtree_height() == 0

def test_subtree_first(example_tree):
    assert example_tree.subtree_first().weight == 'F'
    assert example_tree.left.subtree_first().weight == 'F'
    assert example_tree.right.subtree_first().weight == 'H'

def test_rotate_left(example_tree):
    traversal_order = list(example_tree)
    root = example_tree.subtree_rotate_left()

    assert root.is_root()
    assert root.weight == 'C'
    assert root.left.weight == 'A'
    assert root.left.right.weight == 'H'
    assert root.left.left.weight == 'B'
    assert root.right is None

    new_traversal_order = list(root)
    assert new_traversal_order == traversal_order 

def test_rotate_right(example_tree):
    traversal_order = list(example_tree)
    root = example_tree.subtree_rotate_right()

    assert root.is_root()
    assert root.weight == 'B'
    assert root.right.weight == 'A'
    assert root.right.left.weight == 'E'

    new_traversal_order = list(root)
    assert new_traversal_order == traversal_order 