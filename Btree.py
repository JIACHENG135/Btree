import bisect


class Node:
    def __init__(self, leaf=False):
        self.keys = []
        self.children = []
        self.leaf = leaf
        self.parent = (None, None)


class Btree:
    def __init__(self, t):
        self.t = t
        self.MIN = t - 1
        self.MAX = 2 * t - 1
        self.root = Node(True)

    def assign_parent(self, parent):
        # maintain not only who is my parent, and i'm which child of parent
        for ind, child in enumerate(parent.children):
            child.parent = (parent, ind)

    def split(self, x, ind):
        t = self.t
        y = x.children[ind]

        z = Node(y.leaf)
        x.children.insert(ind + 1, z)

        x.keys.insert(ind, y.keys[t-1])

        z.keys = y.keys[t: 2*t - 1]
        y.keys = y.keys[:t-1]
        if not y.leaf:
            z.children = y.children[t: 2*t]
            y.children = y.children[:t]

        self.assign_parent(x)
        self.assign_parent(y)
        self.assign_parent(z)

    def insert_to_node(self, node, key):
        t = self.t
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i+1] = node.keys[i]
                i -= 1
            node.keys[i+1] = key
        else:
            i = bisect.bisect_left(node.keys, key)
            if len(node.children[i].keys) == self.MAX:
                self.split(node, i)
                if key > node.keys[i]:
                    i += 1
            self.insert_to_node(node.children[i], key)

    def insert(self, key):
        t = self.t
        root = self.root

        if len(root.keys) == self.MAX:
            node = Node(False)
            self.root = node
            node.children.append(root)
            root.parent = (node, 0)
            self.split(node, 0)
            self.insert_to_node(node, key)
        else:
            self.insert_to_node(root, key)

    def search(self, key, node=None):
        node = self.root if not node else node
        ind = bisect.bisect_left(node.keys, key)
        length = len(node.keys)
        if ind < length and key == node.keys[ind]:
            return node
        elif node.leaf:
            return None
        else:
            return self.search(key, node.children[ind])

    def check_parent(self, node, handover_children=True):
        parent, index = node.parent

        if parent == None:
            # current node is root
            if len(node.keys) == 0:
                self.root = node.children[0]
        else:
            if len(node.keys) < self.MIN:
                children_length = len(parent.children)
                if index > 0 and index < children_length - 1:
                    ls = parent.children[index - 1]
                    rs = parent.children[index + 1]
                    if len(ls.keys) - 1 >= self.MIN:
                        node.keys = [parent.keys[index - 1]] + node.keys
                        parent.keys[index - 1] = ls.keys.pop()
                        if handover_children:
                            if len(ls.children) > 0:
                                node.children = [
                                    ls.children.pop()] + node.children
                                self.assign_parent(node)
                                self.assign_parent(ls)
                    elif len(rs.keys) - 1 >= self.MIN:
                        node.keys = node.keys + [parent.keys[index]]
                        parent.keys[index] = rs.keys.pop(0)
                        if handover_children:
                            if len(rs.children) > 0:
                                node.children = node.children + \
                                    [rs.children.pop(0)]
                                self.assign_parent(node)
                                self.assign_parent(rs)

                    else:
                        # both ls and rs not enough keys
                        # take the key from parent, ask parent handl
                        # itself
                        # merge left by default
                        ls.keys = ls.keys + \
                            [parent.keys.pop(index - 1)] + node.keys
                        poped = parent.children.pop(index)
                        self.assign_parent(parent)
                        if handover_children:
                            ls.children = ls.children + poped.children
                            self.assign_parent(node)
                            self.assign_parent(ls)

                        self.check_parent(parent, handover_children)
                elif index == 0:
                    rs = parent.children[index + 1]
                    if len(rs.keys) - 1 >= self.MIN:
                        node.keys = node.keys + [parent.keys[index]]
                        parent.keys[index] = rs.keys.pop(0)
                        if handover_children:
                            if len(rs.children) > 0:
                                node.children = node.children + \
                                    [rs.children.pop(0)]
                                self.assign_parent(node)
                                self.assign_parent(rs)
                    else:
                        rs.keys = node.keys + \
                            [parent.keys.pop(index)] + rs.keys
                        poped = parent.children.pop(index)
                        # print(
                        #     f"poped item: {poped.children[0].keys}", handover_children)
                        if handover_children:
                            rs.children = poped.children + rs.children
                            self.assign_parent(rs)
                        self.assign_parent(parent)
                        self.check_parent(parent, handover_children)

                elif index == children_length - 1:
                    ls = parent.children[index - 1]
                    if len(ls.keys) - 1 >= self.MIN:
                        # borrow key from ls
                        node.keys = [parent.keys[index - 1]] + node.keys
                        parent.keys[index - 1] = ls.keys.pop()
                        if handover_children:
                            if len(ls.children) > 0:
                                node.children = [
                                    ls.children.pop()] + node.children
                                self.assign_parent(node)
                        # since ls is leaf as well, children operation ignored
                    else:
                        ls.keys = ls.keys + \
                            [parent.keys.pop(index - 1)] + node.keys
                        poped = parent.children.pop(index)
                        self.assign_parent(parent)
                        if handover_children:
                            ls.children = ls.children + poped.children
                            self.assign_parent(ls)
                        self.check_parent(parent, handover_children)

    def pre(self, node):
        if len(node.children) == 0:
            return node
        else:
            return self.pre(node.children[-1])

    def suc(self, node):
        if len(node.children) == 0:
            return node
        else:
            return self.suc(node.children[0])

    def inorder(self, node):
        if not node.children:
            return node.keys
        res = []
        for i in range(len(node.keys)):
            res.extend(self.inorder(node.children[i]))
            res.append(node.keys[i])
        res.extend(self.inorder(node.children[i + 1]))
        return res

    def height(self, node):
        if not node.children:
            return 0
        return 1 + self.height(node.children[0])

    def delete(self, key):
        node = self.root

        while True:
            ind = bisect.bisect_left(node.keys, key)
            key_length = len(node.keys)
            if ind < key_length and node.keys[ind] == key:
                parent, index = node.parent
                if node.leaf and parent is not None:
                    if key_length - 1 >= self.MIN:
                        node.keys.pop(ind)
                        return
                    else:

                        children_length = len(parent.children)
                        if index > 0 and index < children_length - 1:
                            ls = parent.children[index - 1]
                            rs = parent.children[index + 1]
                            if len(ls.keys) - 1 >= self.MIN:
                                node.keys.pop(ind)
                                bisect.insort(
                                    node.keys, parent.keys[index - 1])
                                parent.keys[index - 1] = ls.keys.pop()
                            elif len(rs.keys) - 1 >= self.MIN:
                                node.keys.pop(ind)
                                bisect.insort(
                                    node.keys, parent.keys[index])
                                parent.keys[index] = rs.keys.pop(0)
                            else:
                                node.keys.pop(ind)
                                ls.keys = ls.keys + \
                                    [parent.keys.pop(index - 1)] + node.keys
                                parent.children.pop(index)
                                self.assign_parent(parent)
                                self.check_parent(parent)
                        elif index == 0:
                            rs = parent.children[index + 1]
                            if len(rs.keys) - 1 >= self.MIN:
                                node.keys.pop(ind)
                                bisect.insort(node.keys, parent.keys[index])
                                parent.keys[index] = rs.keys.pop(0)
                            else:
                                node.keys.pop(ind)
                                rs.keys = node.keys + \
                                    [parent.keys.pop(index)] + rs.keys
                                parent.children.pop(index)
                                self.assign_parent(parent)
                                self.check_parent(parent)
                        elif index == children_length - 1:
                            ls = parent.children[index - 1]
                            if len(ls.keys) - 1 >= self.MIN:
                                node.keys.pop(ind)
                                bisect.insort(
                                    node.keys, parent.keys[index - 1])
                                parent.keys[index - 1] = ls.keys.pop()
                            else:
                                node.keys.pop(ind)
                                ls.keys = ls.keys + \
                                    [parent.keys.pop(index - 1)] + node.keys
                                parent.children.pop(index)
                                self.assign_parent(parent)
                                self.check_parent(parent)
                        return
                else:
                    if len(node.children) > 0:
                        prenode = self.pre(node.children[ind])
                        sucnode = self.suc(node.children[ind + 1])
                        if len(prenode.keys) - 1 >= self.MIN:
                            node.keys.pop(ind)
                            bisect.insort(node.keys, prenode.keys.pop(-1))
                        elif len(sucnode.keys) - 1 >= self.MIN:
                            node.keys.pop(ind)
                            bisect.insort(node.keys, sucnode.keys.pop(0))
                        else:
                            node.keys.pop(ind)
                            bisect.insort(node.keys, prenode.keys.pop(-1))
                            self.check_parent(prenode, True)
                    else:
                        node.keys.pop(ind)
                    return
            elif ind < key_length and node.keys[ind] > key:
                if node.leaf:
                    return
                else:
                    node = node.children[ind]
            else:
                node = node.children[ind]

    def print_tree(self, x, level=0):
        print(f'Level {level}', end=": ")

        for i in x.keys:
            print(i, end=" ")

        print()
        level += 1

        if len(x.children) > 0:
            for i in x.children:
                self.print_tree(i, level)
