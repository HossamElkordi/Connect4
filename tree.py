class TreeNode:
    def __init__(self, val, children, branch):
        self.val = val
        self.child = children
        self.br = branch

    def value(self):
        return self.val

    def children(self):
        return self.child

    def branch(self):
        return self.br
