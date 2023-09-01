from Btree import Btree
import random
import math


def find_height_upper_bound(n, t):
    return math.log((n + 1) / 2, t)


class TestBTree:

    def test_huge_insert(self):

        for _ in range(10000):
            t = random.sample(range(2, 20), 1)[0]
            ub = 3
            values_for_insertion = set(
                random.sample(range(1, 10 ** ub), 10 ** (ub - 1)))
            non_exist_values = [i for i in range(
                1, 10**ub) if i not in values_for_insertion]

            btree = Btree(t)
            count = 10**(ub - 1) - 1
            while count:
                value_for_insertion = values_for_insertion.pop()
                btree.insert(value_for_insertion)
                node = btree.search(value_for_insertion)
                assert node is not None
                non_exist_value = non_exist_values.pop()
                node = btree.search(non_exist_value)
                assert node is None
                count -= 1

    def test_huge_delete_root(self):

        for _ in range(10000):
            t = random.sample(range(2, 15), 1)[0]
            ub = 3
            values_for_insertion = set(
                random.sample(range(1, 10 ** ub), 10 ** (ub - 1)))
            non_exist_values = [i for i in range(
                1, 10**ub) if i not in values_for_insertion]

            btree = Btree(t)
            count = 10**(ub - 1) - 1

            inserted = set()
            while count:
                value_for_insertion = values_for_insertion.pop()
                inserted.add(value_for_insertion)

                btree.insert(value_for_insertion)
                node = btree.search(value_for_insertion)
                assert node is not None
                non_exist_value = non_exist_values.pop()
                node = btree.search(non_exist_value)
                assert node is None
                count -= 1
            btree.print_tree(btree.root)
            for key in btree.root.keys:
                inserted.remove(key)
                btree.delete(key)
                node = btree.search(key)
                assert node is None

    def test_huge_insert_and_delete(self):
        '''
        1. insert a value then query it, it should be found
        2. delete an inserted value, query it, it should not be found
        3. do an inorder traverse of the tree, the keys should be sorted
        '''

        for _ in range(1000):
            t = random.sample(range(2, 15), 1)[0]
            ub = 3
            values_for_insertion = set(
                random.sample(range(1, 10 ** ub), 10 ** ub // 2))
            non_exist_values = [i for i in range(
                1, 10**ub) if i not in values_for_insertion]

            btree = Btree(t)
            count = 10 ** ub // 2 - 1
            # count = 1000

            inserted = set()

            while count:
                value_for_insertion = values_for_insertion.pop()
                inserted.add(value_for_insertion)

                btree.insert(value_for_insertion)
                node = btree.search(value_for_insertion)
                assert node is not None
                non_exist_value = non_exist_values.pop()
                node = btree.search(non_exist_value)
                assert node is None
                count -= 1

                delOrNot = random.sample([0, 1], 1)[0]
                if delOrNot:
                    value_for_deletion = inserted.pop()
                    btree.delete(value_for_deletion)
                    node = btree.search(value_for_deletion)
                    assert node is None
                    keys = btree.inorder(btree.root)
                    sortedkeys = sorted(keys)
                    for k1, k2 in zip(keys, sortedkeys):
                        assert k1 == k2

    def test_huge_height_in_bound(self):
        '''
        1. Tree height should be always smaller than upper bound
        '''
        for _ in range(1000):
            t = random.sample(range(2, 15), 1)[0]
            ub = 4
            values_for_insertion = set(
                random.sample(range(1, 10 ** ub), 10 ** ub // 2))
            non_exist_values = [i for i in range(
                1, 10**ub) if i not in values_for_insertion]

            btree = Btree(t)
            count = 10 ** ub // 2 - 1
            # count = 1000

            inserted = set()

            while count:
                value_for_insertion = values_for_insertion.pop()
                inserted.add(value_for_insertion)
                btree.insert(value_for_insertion)
                count -= 1

                delOrNot = random.sample([0, 1], 1)[0]
                if delOrNot:
                    value_for_deletion = inserted.pop()
                    btree.delete(value_for_deletion)
                    h = btree.height(btree.root)
                    if len(inserted) > 0:
                        hb = find_height_upper_bound(len(inserted), t)
                        assert h <= hb
