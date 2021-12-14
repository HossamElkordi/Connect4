import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout


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


def plot_tree(r, depth):
    plt.figure(3, figsize=(40 * (depth + 1), 40 * (depth + 1)), dpi=40)
    g = nx.DiGraph()
    g.add_node(0, value=r.value())
    node_labels = {0: r.value()}
    traverse((0, r), g, node_labels)
    pos = graphviz_layout(g, prog='twopi')
    nx.draw(g, pos, with_labels=False, arrows=True, node_size=6000, width=4)
    nx.draw_networkx_labels(g, pos, node_labels, font_size=20, font_color='yellow', font_weight='bold')
    nx.draw_networkx_edge_labels(g, pos, font_size=20, font_weight='bold')
    plt.savefig("tree", format="JPEG")


def traverse(child, g, node_labels):
    if child[1].children() is None:
        return
    i = 1
    for n in child[1].children():
        g.add_node(child[0] * 10 + i, value=n.value())
        node_labels[child[0] * 10 + i] = n.value()
        g.add_weighted_edges_from([(child[0], child[0] * 10 + i, n.branch())], weight='col')
        traverse((child[0] * 10 + i, n), g, node_labels)
        i += 1


if __name__ == '__main__':
    root = TreeNode(1, [TreeNode(2, [TreeNode(4, None, -1), TreeNode(4, None, -1)], -1), TreeNode(2, [TreeNode(4, None, -1), TreeNode(4, None, -1)], -1), TreeNode(3, [TreeNode(4, [TreeNode(4, [TreeNode(4, None, -1), TreeNode(4, None, -1)], -1), TreeNode(4, None, -1)], -1)], -1), TreeNode(4, [TreeNode(4, None, -1), TreeNode(4, None, -1)], -1)], -1)
    root1 = TreeNode(7, [root, root, root, root], -1)
    plot_tree(root1)
