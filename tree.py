import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout


class TreeNode:
    def __init__(self, val, children, branch, col):
        self.val = val
        self.child = children
        self.br = branch
        self.col = col

    def value(self):
        return self.val

    def children(self):
        return self.child

    def branch(self):
        return self.br


def plot_tree(r, depth):
    plt.figure(3, figsize=((40) * (depth + 1), (40) * (depth + 1)), dpi=40)
    g = nx.DiGraph()
    g.add_node(0, value=r.value())
    node_labels = {0: r.value()}
    traverse((0, r), g, node_labels)
    pos = graphviz_layout(g, prog='twopi')
    nx.draw(g, pos, with_labels=False, arrows=True, node_size=6000, width=4)
    nx.draw_networkx_labels(g, pos, node_labels, font_size=20, font_color='yellow', font_weight='bold')
    nx.draw_networkx_edge_labels(g, pos, font_size=20, font_weight='bold')
    plt.savefig("tree", format="JPEG")
    plt.close()


def traverse(child, g, node_labels):
    if child[1].children() is None:
        return
    i = 1
    for n in child[1].children():
        g.add_node(child[0] * 10 + i, value=n.value())
        node_labels[child[0] * 10 + i] = n.value()
        g.add_weighted_edges_from([(child[0], child[0] * 10 + i, n.col + 1)], weight='col')
        traverse((child[0] * 10 + i, n), g, node_labels)
        i += 1


def check_row(board, window, col_pos, i, val):
    if not val and \
            (col_pos[window[1]] >= i or col_pos[window[1] + 1] >= i or col_pos[window[1] + 2] >= i or col_pos[window[1] + 3] >= i):
        return 0
    if board[i, window[1]] == val and board[i, window[1] + 1] == val and board[i, window[1] + 2] == val and board[i, window[1] + 3] == val:
        return 1
    return 0


def check_col(board, window, col_pos, j, val):
    if col_pos[window[1]] < window[0] - 4 and \
            board[window[1], j] == val and board[window[1] + 1, j] == val and board[window[1] + 2, j] == val and board[window[1] + 3, j] == val:
        return 1
    return 0


def check_diagonals(board, window, col_pos, val):
    pts = 0
    if window[0, 0] == val and window[1, 1] == val and window[2, 2] == val and window[3, 3] == val:
        pts += 1
    if window[0, 3] == val and window[1, 2] == val and window[2, 1] == val and window[3, 0] == val:
        pts += 1
    return pts


def calc_pts(board, val, all_cols=False):
    pts = 0
    for i in range(5, 2, -1):
        for j in range(4):
            pass


if __name__ == '__main__':
    print([i for i in range(3)])

