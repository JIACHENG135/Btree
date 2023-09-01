# BTree Implementation in Python

This repository contains an implementation of the BTree data structure in Python. It also includes comprehensive tests to ensure the correctness and efficiency of the operations.

## Features

- Insertion
- Deletion
- Search
- In-order traversal
- Computation of height

## Getting Started

## Usage

```python
from Btree import Btree

# Create a Btree with a minimum degree of t
t = 3
btree = Btree(t)

# Insert values
btree.insert(1)
btree.insert(2)
btree.insert(3)

# Search for a value
node = btree.search(2)  # returns the node containing the value, None if not found

# Delete a value
btree.delete(2)

# Print the tree
btree.print_tree(btree.root)

```

## THIS IS ONLY FOR LEARNING PURPOSE

For more details, check here.
[BTree tutorail](!https://www.bilibili.com/video/BV1Y14y1y77X/?vd_source=367aed41a535ceffdb176c3ab1b4b146)

## Testing

This implementation comes with a suite of tests that verify the correctness of the BTree operations. These tests include:

- Huge Insert: Inserts a large number of values and ensures each inserted value can be found.
- Huge Delete Root: Inserts a large number of values, then deletes keys from the root.
- Huge Insert and Delete: Inserts a set of values, queries them, deletes some, and checks the in-order traversal of the tree.
- Huge Height In-Bound: Ensures that the tree's height is always within its expected bounds.

### To run the tests:

`pytest --log-cli-level=DEBUG BTreeTest.py`

## Contribute

Feel free to contribute to this repository by submitting pull requests. Any contributions, big or small, are greatly appreciated!

## License

MIT
