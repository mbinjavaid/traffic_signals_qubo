import numpy as np
# import numpy.core._dtype_ctypes
from grid_graph import node_list
# import networkx as nx
from graph import nearby_nodes_from_ordered_dict
# from graph import graph

# from matplotlib import pyplot as plt



def I(i, j):
    if i == 'False':
        return "False"

    return (6 * i) + j


def q1_coeff(cost_list, f_list=(0.8, 0.8, 0.8, 0.8)):

    coeff_list = np.zeros(6)

    coeff_list[0] = -((cost_list[0] * f_list[0]) + (cost_list[1] * f_list[1]))
    coeff_list[1] = -cost_list[0]
    coeff_list[2] = -cost_list[1]
    coeff_list[3] = -((cost_list[2] * f_list[2]) + (cost_list[3] * f_list[3]))
    coeff_list[4] = -cost_list[2]
    coeff_list[5] = -cost_list[3]

    return coeff_list


# print("q1_coeff: ", q1_coeff(cost_lists))


def q1(cost_lists, dim):
    q1 = np.zeros((dim, dim))

    big_q1_coeff_flat = []

    for i in range(len(cost_lists)):
        q1_coeffs = q1_coeff(cost_lists[i])
        for j in range(6):
            big_q1_coeff_flat.append(q1_coeffs[j])

            # print("abc", len(big_q1_coeff_flat))

    for i in range(dim):
        q1[i][i] = big_q1_coeff_flat[i]

    return q1


# def q1_aug(cost_lists):
#
#     q1_dim = len(cost_lists) * 6
#     q1 = np.zeros((q1_dim, q1_dim))
#
#
#     for i in range(len(cost_lists)):


# q1 = q1(cost_lists, f_lists)


def q2(dim):
    # q2_dim = dim
    q2 = np.zeros((dim, dim))

    for i in range(dim):
        q2[i][i] = -1
        for j in range(i, 5):

            for k in range(int(dim / 6)):
                q2[i + (6 * k)][j + 1 + (6 * k)] = 2

    return 60 * q2
    # return 365 * q2


# q2 = q2(2, cost_lists)

# print(q1)
# print(q2)

# lembda = 100


def node_mode_table(j, node, graph_ordered_dict):
    # neighbors = nx.neighbors(G, node)

    # if node[0]

    up, down, right, left = nearby_nodes_from_ordered_dict(graph_ordered_dict, node)

    # print("up | down | right | left: ", up, down, right, left)

    if j == 0:
        return [I(up, 0), I(up, 1), I(down, 0), I(down, 2)], [up, down, right, left], [0, 1, 0, 2]
    if j == 1:
        return [I(up, 1), I(up, 0), I(right, 4), I(right, 3)], [up, down, right, left], [1, 0, 4, 3]
    if j == 2:
        return [I(down, 2), I(down, 0), I(left, 5), I(left, 3)], [up, down, right, left], [2, 0, 5, 3]
    if j == 3:
        return [I(right, 3), I(right, 4), I(left, 3), I(left, 5)], [up, down, right, left], [3, 4, 3, 5]
    if j == 4:
        return [I(right, 4), I(right, 3), I(down, 2), I(down, 0)], [up, down, right, left], [4, 3, 2, 0]
    if j == 5:
        return [I(left, 5), I(left, 3), I(up, 1), I(up, 0)], [up, down, right, left], [5, 3, 1, 0]


def q3(G, node_list, dim, graph_ordered_dict, runtime, run, cost_lists, lembda, lembda1=0.7, lembda2=0.3, buff=4):
    q3 = np.zeros((dim, dim))

    cutoff_speed = 0

    for i in range(len(node_list)):
        q1_coeff_ = q1_coeff(cost_lists[i])

        # q1_coeff_ = [1,1,1,1,1,1]
        node = node_list[i]

        up, down, right, left = nearby_nodes_from_ordered_dict(graph_ordered_dict, node)
        nearby_nodes_list = [up, down, right, left]



        distance_list = []
        speed_list = []
        # t_list = []

        runtime_list = []
        # print("RUNTIME: ", runtime)

        for k in range(len(nearby_nodes_list)):
            # print('Node', 'nearby_nodes_list', node, nearby_nodes_list[k])
            if nearby_nodes_list[k] == 'False':
                distance_list.append(0)
                speed_list.append(0)
                # t_list.append(0)
                runtime_list.append(0)
            else:
                distance_list.append(G[node][nearby_nodes_list[k]]['weight'])
                speed_list.append(G[node][nearby_nodes_list[k]]['speed'])
                # t_list.append(distance_list[k]/speed_list[k])
                runtime_list.append(int(round((distance_list[k] / speed_list[k]) / runtime)))


        for i_ in nearby_nodes_list:

            rel = nearby_nodes_list.index(i_)
            if i_ != 'False':
                nearby_nodes_x = nearby_nodes_from_ordered_dict(graph_ordered_dict, i_)

            x = nearby_nodes_x[rel]



            if i_ != 'False' and x != 'False':

                # if G[i][i_]['speed'] >= cutoff_speed:
                if G[i_][x]['speed'] >= cutoff_speed:

                    # print("ohahahajuuuu Allah uhhhhhhhh")

                    for j in range(6):
                        nm_table = node_mode_table(j, node, graph_ordered_dict)
                        nm_list = nm_table[0]
                        # nearby_nodes_list = nm_table[1]
                        j_prime = nm_table[2]

                        I_ = I(i, j)

                        # print("nm_table: ", nm_table)



                        # print("I_", I_)
                        # print("nm_list: ", nm_list)

                        # print("RUNTIME LIST UHHHHH: ", runtime_list)








                        if runtime_list[0] != 0 and run != 0:
                            # print("\nruntime_list[0]: ", runtime_list[0])
                            # print("run: ", run)
                            if runtime_list[0] > run:
                                if runtime_list[0] - run <= buff:
                                    # print("PERCOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ", abs(runtime_list[0] - run))
                                    if not (I_ == 'False' or nm_list[0] == 'False'):
                                        q3[I_][nm_list[0]] -= lembda1 * (q1_coeff_[j] + q1_coeff(cost_lists[nearby_nodes_list[0]])[j_prime[0]])

                            if runtime_list[0] <= run:
                                if run % runtime_list[0] <= buff:
                                    if not (I_ == 'False' or nm_list[0] == 'False'):
                                        q3[I_][nm_list[0]] -= lembda1 * (q1_coeff_[j] + q1_coeff(cost_lists[nearby_nodes_list[0]])[j_prime[0]])

                        if runtime_list[1] != 0 and run != 0:
                            # print("\nruntime_list[1]: ", runtime_list[1])
                            # print("run: ", run)
                            if runtime_list[1] > run:
                                if runtime_list[1] - run <= buff: # or run % runtime_list[1] <= 4:
                                    # print("PERCOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ", abs(runtime_list[1] - run))
                                    if not (I_ == 'False' or nm_list[1] == 'False'):
                                        q3[I_][nm_list[1]] -= lembda2 * (q1_coeff_[j] + q1_coeff(cost_lists[nearby_nodes_list[1]])[j_prime[1]])

                            if runtime_list[1] <= run:
                                if run % runtime_list[1] <= buff:
                                    # print("PERCOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ", abs(runtime_list[1] - run))
                                    if not (I_ == 'False' or nm_list[1] == 'False'):
                                        q3[I_][nm_list[1]] -= lembda2 * (q1_coeff_[j] + q1_coeff(cost_lists[nearby_nodes_list[1]])[j_prime[1]])

                        if runtime_list[2] != 0 and run != 0:
                            # print("\nruntime_list[2]: ", runtime_list[2])
                            # print("run: ", run)
                            if runtime_list[2] > run:
                                if runtime_list[2] - run <= buff:  # or run % runtime_list[2] <= 4:
                                    # print("PERCOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ", abs(runtime_list[2] - run))
                                    if not (I_ == 'False' or nm_list[2] == 'False'):
                                        q3[I_][nm_list[2]] -= lembda1 * (q1_coeff_[j] + q1_coeff(cost_lists[nearby_nodes_list[2]])[j_prime[2]])

                            if runtime_list[2] <= run:
                                if run % runtime_list[2] <= buff:
                                    # print("PERCOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ", abs(runtime_list[2] - run))
                                    if not (I_ == 'False' or nm_list[2] == 'False'):
                                        q3[I_][nm_list[2]] -= lembda1 * (q1_coeff_[j] + q1_coeff(cost_lists[nearby_nodes_list[2]])[j_prime[2]])

                        if runtime_list[3] != 0 and run != 0:
                            # print("\nruntime_list[3]: ", runtime_list[3])
                            # print("run: ", run)
                            if runtime_list[3] > run:
                                if runtime_list[3] - run <= buff: # run % runtime_list[3] <= 4:
                                    # print("PERCOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ", abs(runtime_list[3] - run))
                                    if not (I_ == 'False' or nm_list[3] == 'False'):
                                        q3[I_][nm_list[3]] -= lembda2 * (q1_coeff_[j] + q1_coeff(cost_lists[nearby_nodes_list[3]])[j_prime[3]])

                            if runtime_list[3] <= run:
                                if run % runtime_list[3] <= buff:
                                    # print("PERCOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO ", abs(runtime_list[3] - run))
                                    if not (I_ == 'False' or nm_list[3] == 'False'):
                                        q3[I_][nm_list[3]] -= lembda2 * (q1_coeff_[j] + q1_coeff(cost_lists[nearby_nodes_list[3]])[j_prime[3]])


    return lembda * q3


def Q(G, graph_ordered_dict, cost_lists, lembda, runtime, run, first_time):
    node_list_ = node_list(G)
    dim = len(node_list_) * 6

    q_1 = q1(cost_lists, dim)
    q_2 = q2(dim)

    if not first_time:
        q_3 = q3(G, node_list_, dim, graph_ordered_dict, runtime, run, cost_lists, lembda)


        return q_1 + q_2 + q_3

    else:
        return q_1 + q_2

