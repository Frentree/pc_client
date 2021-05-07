from collections import defaultdict


class TrieNode:
    def __init__(self):
        self.children = defaultdict()
        self.terminated = False
        self.parent = ""
        self.data = ""

    def deleteChildren(self, parent):
        del parent.parent.children[parent.data]


class Trie:
    def __init__(self):
        self.root = self.get_node()
        self.root.parent = self.root
        self.output = []

    def get_node(self):
        return TrieNode()

    def insert(self, word):
        root = self.root

        for path in word:
            if path not in root.children:
                root.children[path] = self.get_node()
                root.children[path].data = path
                root.children[path].parent = root
            keys = list(root.children.keys())
            for key in keys:
                if key == path:
                    root = root.children.get(key)
                    break

        root.terminated = True

    def dfs(self, node, prefix):
        if node.terminated:
            self.output.append((prefix + "\\" + node.data))
        for child in node.children.values():
            self.dfs(child, prefix + "\\" + node.data)

    def query(self):
        node = self.root
        self.dfs(node, "")
        return self.output

    def remove_node(self, parent, children):
        if parent == self.root:
            return True
        if len(parent.children) > 1:
            return parent.deleteChildren(parent)
        temp = parent.parent
        parent.children = defaultdict()
        self.remove_node(temp, parent)

    def delete(self, paths):
        root = self.root
        last = len(paths) - 1
        for path in paths:
            if path not in root.children and path != paths[last]:
                break

            keys = list(root.children.keys())
            for key in keys:
                if key == path:
                    root = root.children.get(key)
                    break

        if root.terminated and root.data == path:
            self.remove_node(root.parent, root)

    def search(self, paths):
        root = self.root

        for path in paths:
            if not root or not root.children:
                return False
            root = root.children.get(path)

        return True if root and root.terminated else False