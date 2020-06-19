import networkx as nx
import random
import copy
import numpy as np
# import numpy.core._dtype_ctypes


def ordered_dict_generator(n):

    keys = list(np.arange(0, n*n))

    ups_list = list(np.arange(n, (n*n)+n))

    for i in range(1, n+1):
        ups_list[-i] = 'False'

    downs_list = list(np.arange(0, (n*n)-n))

    for i in range(0, n):
        downs_list.insert(0, 'False')

    rights_list = list(np.arange(1, (n*n)+1))

    for index in range(n-1, len(rights_list), n):
        rights_list[index] = 'False'


    lefts_list = list(np.arange(-1, (n*n)-1))

    for index in range(0, len(lefts_list), n):
        lefts_list[index] = 'False'

    values = list(zip(ups_list, downs_list, rights_list, lefts_list))

    values_ = [list(elem) for elem in values]

    dictionary = dict(zip(keys, values_))

    # print(dictionary)
    return dictionary


# ordered_dict_generator(4)












def graph_unordered_dict(graph_ordered_dict):

    keys_list = list(graph_ordered_dict)

    values_list = list(graph_ordered_dict.values())

    # print(values_list)

    new_value_list = copy.deepcopy(values_list)

    # new_value_list = []
    #
    # for i in range(len(values_list)):
    #     new_value_list.append(values_list[i])

    # print("new_value_list: ", new_value_list)

    # new_value_list = []

    for i in range(len(values_list)):
        # a = []
        # for j in range(len(values_list[i])):
            # if values_list[i][j] != 'False':
            #     a.append(values_list[i][j])
        # new_value_list[i].remove('False')

        while 'False' in new_value_list[i]: new_value_list[i].remove('False')

        # print("new_value_list[i]: ", new_value_list[i])

        # new_value_list.append(a)

    # print("new value list: ", new_value_list)

    dict_list = zip(keys_list, new_value_list)

    graph_unordered_dict_ = dict(dict_list)

    # print("graph_unordered_dict_: ", graph_unordered_dict_)

    # graph_unordered_dict_ = graph_ordered_dict
    #
    # for i in graph_unordered_dict_.values():
    #     if 'False' in i:
    #         i.remove('False')

    # print("graph_unordered_dict_: ", graph_unordered_dict_)

    return graph_unordered_dict_

# graph_unordered_dict_ = graph_unordered_dict(graph_ordered_dict)


def graph(graph_ordered_dict_):

    random.seed(1)

    graph_unordered_dict_ = graph_unordered_dict(graph_ordered_dict_)

    print("graph unordered dict: ", graph_unordered_dict_)

    G = nx.DiGraph(graph_unordered_dict_)

    source_nodes_list = list(graph_unordered_dict_.keys())

    # print("source_nodes_list", source_nodes_list)

    speeds_list = [11, 17, 22, 28]

    for i in range(len(source_nodes_list)):
        for j in graph_unordered_dict_[i]:
            G[source_nodes_list[i]][j]['weight'] = 1000             #randomly generating lengths
            # G[source_nodes_list[i]][j]['weight'] = int(random.uniform(500, 1000))             #randomly generating lengths
            # G[source_nodes_list[i]][j]['speed'] = 10 * random.uniform(1,3.3) #random speed limits (40-100)
            G[source_nodes_list[i]][j]['speed'] = random.choice(speeds_list) #random speed limits (40-100)
            # G[source_nodes_list[i]][j]['speed'] = random.choice([10,20,30,40,50,150,160]) #random speed limits (40-100)
            # G[source_nodes_list[i]][j]['speed'] = random.uniform(0, 1)              #randomly speed limits
            # G[source_nodes_list[i]][j]['speed'] = 100        #randomly speed limits
            G[source_nodes_list[i]][j]['effective'] = 0
            G[source_nodes_list[i]][j]['pos_list'] = []
            G[source_nodes_list[i]][j]['pos_list_temp'] = []
            G[source_nodes_list[i]][j]['pos_list_stick'] = []
            G[source_nodes_list[i]][j]['color_list'] = []
            G[source_nodes_list[i]][j]['horizontal'] = False
            G[source_nodes_list[i]][j]['forward'] = False

            # G[source_nodes_list[i]][j]['cost_list'] = []


    # print("WEIGHT:", G.get_edge_data(1, 2))

    return G

# graph_from_unordered_dict(graph_unordered_dict_)


def nearby_nodes_from_ordered_dict(graph_ordered_dict, node):

    up, down, right, left = graph_ordered_dict[node]

    return up, down, right, left

# print("Nearby nodes: ", nearby_nodes_from_ordered_dict(graph_ordered_dict, 3))

