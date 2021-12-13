class TreeNode:
    def __init__(self, val, children, branch):
        self.val = val
        self.children = children
        self.branch = branch

    def value(self):
        return self.val

    def children(self):
        return self.children

    def branch(self):
        return self.branch
