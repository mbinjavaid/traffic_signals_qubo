# from graph import graph_unordered_dict
# import networkx as nx
# from matplotlib import pyplot as plt
# import numpy as np
import random


# graph_ordered_dict = {
#     0: [3, 'False', 1, 'False'],
#     1: [4, 'False', 2, 0],
#     2: [5, 'False', 'False', 1],
#     3: [6, 0, 4, 'False'],
#     4: [7, 1, 5, 3],
#     5: [8, 2, 'False', 4],
#     6: ['False', 3, 7, 'False'],
#     7: ['False', 4, 8, 6],
#     8: ['False', 5, 'False', 7]
# }


def square_grid_coord(n, m, weight):
    coord_list = []

    for i in range(0, m):
        for j in range(0, n):
            coord_list.append((j * weight, i * weight))

    return coord_list


# coords = square_grid_coord(3, 3, 1000)
# print("coords:\n", coords)


# graph_unordered_dict_ = graph_unordered_dict(graph_ordered_dict)

# G = nx.DiGraph(graph_unordered_dict_)
# print("edges:\n", G.edges())

# def xy_edges(G, a, b, coords):
#
#     edges = G.edges()
#     return edges[a], edges[b]
#
# xy_edges_ = xy_edges(G, 0, 1, coords)
# print("xy_edges: ", xy_edges_)

def xy_edges_list_generator(G, coords):
    edges = list(G.edges())

    xy_list = []

    for i in range(len(edges)):
        start_xy = coords[edges[i][0]]
        end_xy = coords[edges[i][1]]

        xy_list.append([start_xy, end_xy])

    # print("xy_list:\n", xy_list)
    return xy_list


# xy_edges_list = xy_edges_list_generator(G, coords)


def xy_from_pos(G, node1, node2, weight, pos, n, m):
    coords = square_grid_coord(n, m, weight)

    edges = list(G.edges)

    edge_no = edges.index((node1, node2))

    edge_xy = xy_edges_list_generator(G, coords)[edge_no]

    a = edge_xy[0]
    b = edge_xy[1]

    s = pos / weight

    x = ((b[0] - a[0]) * s) + a[0]
    y = ((b[1] - a[1]) * s) + a[1]

    return x, y


# print(xy_from_pos(G, 0, 1, 1000, 500))


def xy_from_pos_list(G, node1, node2, weight, pos_list, n, m):
    xy_list = []

    for i in pos_list:
        xy = xy_from_pos(G, node1, node2, weight, i, n, m)

        xy_list.append(xy)

    return xy_list


# print("f0 ", xy_from_pos_list(G, 0, 1, 1000, [0, 100, 200, 300, 500, 1000]))
# print("f1 ", xy_from_pos_list(G, 1, 0, 1000, [0, 100, 200, 300, 500, 1000]))

# f0 = xy_from_pos_list(G, 1, 2, 1000, [0, 100, 200, 300, 500, 1000])
# f1 = xy_from_pos_list(G, 2, 1, 1000, [0, 100, 200, 300, 500, 1000])
# print("f0: ", f0)
# print("f1: ", f1)


def pos_shift(pos_list_xy, horizontal, forward, shift=100):
    # print("pos_list xy: ", pos_list_xy)

    if pos_list_xy == []:
        return []

    shift_list = []

    for i in range(len(pos_list_xy)):
        if horizontal:
            # if pos_list_xy[0][0] < pos_list_xy[1][0]:
            if forward:
                shift_list.append((pos_list_xy[i][0] - shift, pos_list_xy[i][1] + shift))
            else:
                shift_list.append(((pos_list_xy[i][0] - shift) / 1, pos_list_xy[i][1] - shift))

        else:
            # if pos_list_xy[0][1] < pos_list_xy[1][0]:
            if forward:
                shift_list.append((pos_list_xy[i][0] - shift, (pos_list_xy[i][1] + shift)))
            else:
                shift_list.append((pos_list_xy[i][0] + shift, (pos_list_xy[i][1] - shift)))

    return shift_list


# print(pos_shift(f0))
# print(pos_shift(f1))


# for i in np.linspace(0, 200, 1000):
#     y = np.sin(i)
#     # y = np.sqrt(np.abs(2500 - i*i))
#     # plt.scatter((i,i,-i,-i), (y,-y,y,-y))
#     plt.scatter((i), (y))
#
#     plt.pause(0.05)
#     # plt.clf()
#
#
# plt.show()


def x_y_from_xy(xy):
    if xy == []:
        return (), ()
    else:
        x = list(zip(*xy))[0]
        y = list(zip(*xy))[1]
        return x, y


def graph_topo(G, m, show=False):
    edges = list(G.edges())

    for i in range(len(edges)):

        a = edges[i][0]
        b = edges[i][1]

        if a - b == -1:
            G[a][b]['horizontal'] = True
            G[a][b]['forward'] = True

        if a - b == 1:
            G[a][b]['horizontal'] = True

        if a + m == b:
            G[a][b]['forward'] = True

    if show:

        for i in range(len(edges)):
            a = edges[i][0]
            b = edges[i][1]

            print("HORIZONTAL: ", a, "  ", b, "  ", G[a][b]['horizontal'])
            print("FORWARD: ", a, "  ", b, "  ", G[a][b]['forward'])


# edges = list(G.edges())
#
# graph_topo(G, 3)

# for i in range(len(edges)):
#
#     a = edges[i][0]
#     b = edges[i][1]
#
#     print("HORIZONTAL: ", G[a][b]['horizontal'])
#     print("FORWARD ", G[a][b]['forward'])


def color_gen(number_of_colors):
    random.seed = 6
    colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(number_of_colors)]

    return colors

# print(colors_gen(9))
