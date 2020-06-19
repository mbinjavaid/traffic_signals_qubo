import networkx as nx
import random
# from matplotlib import pyplot as plt





def create_graph(dim_G=(3,3)):


    G = nx.grid_graph(dim_G)

    G = nx.DiGraph(G)

    # nx.draw(G)
    # node_list = list(nx.nodes(G))
    # print("node list: ", node_list)
    # edge_list = list(nx.edges(G))

    # x, y = node_list[0]
    # print("x, y: ", x, y)

    # no_of_edges = len(list(nx.edges(G)))

    return G


def node_list(G):
    return list(nx.nodes(G))



def random_density_list(no_of_edges, csv=False):

    random.seed(1)
    density_list = []

    for i in range(no_of_edges):
        density_list.append(random.randint(0, 20))

    return density_list


# density_list = density_list(no_of_edges)

# print("density Gen: ", density_list)


def node_index(node_list, node):

    try:
        index = node_list.index(node)
        return index
    except ValueError:
        return "False"


# node_index = node_index(node_list, (5,6))

# print("node_index: ", node_index)


def edge_index(edge_list, edge):
    return edge_list.index(edge)

# edge_index = edge_index(edge_list, edge_list[1])

# print("edge_number: ", edge_index)


def number_of_cars(density_list, edge_index):

    number_of_cars_on_edge = density_list[edge_index]

    return number_of_cars_on_edge


# print("no_of_cars: ", number_of_cars(density_list, edge_index))


def nearby_nodes_index(node_list, node):

    x, y = node

    # print("uh", x, y)

    up = node_index(node_list, (x, y + 1))

    down = node_index(node_list, (x, y - 1))

    right = node_index(node_list, (x + 1, y))

    left = node_index(node_list, (x - 1, y))

    # print("epep: ", up, down, right, left)

    return up, down, right, left


def two_nodes_relation(node_list, a, b, graph_ordered_dict):

    # check = nearby_nodes_index(node_list, a)
    check = graph_ordered_dict[a]

    pos = check.index(b)

    if pos == 0:
        return 'up'
    if pos == 1:
        return 'down'
    if pos == 2:
        return 'right'
    if pos == 3:
        return 'left'


# G = nx.grid_graph([1,2])
# node_list_ = list(nx.nodes(G))
#
# nearby_nodes_index = nearby_nodes_index(node_list_, (1,0))
# print(nearby_nodes_index)

# plt.show()

# print(G)