from graph import nearby_nodes_from_ordered_dict


# graph_ordered_dict = {
#     0: [3, 'False', 1, 'False'],
#     1: [4, 'False', 2, 0],
#     2: [5, 'False', 'False', 1],
#     3: ['False', 0, 4, 'False'],
#     4: ['False', 1, 5, 3],
#     5: ['False', 2, 'False', 4]
# }
#
# cost_lists = [[5, 20, 25, 30], [5, 20, 25, 30], [5, 20, 25, 30], [5, 20, 25, 30], [5, 20, 25, 30], [5, 20, 25, 30]]
# f_list = [[0.7, 0.2], [0.7, 0.2], [0.7, 0.2], [0.7, 0.2], [0.7, 0.2], [0.7, 0.2]]
#
# modes = [3, 3, 0, 3, 3, 3]

# def spill_cars(cost_list_a, cost_list_b, mode):

# print(cost_lists)

def cost_list_updater(cost_lists, modes, graph_ordered_dict, rate, fs):

    nodes = list(graph_ordered_dict.keys())
    # print(nodes)

    for i in range(len(nodes)):

        node = nodes[i]
        mode = modes[i]
        f = fs[i]

        up, down, right, left = nearby_nodes_from_ordered_dict(graph_ordered_dict, node)

        if mode == 0:
            cost_lists[node][0] -= rate*f[0]

            if not (up == 'False'):
                cost_lists[up][0] += rate*f[0]

            cost_lists[node][1] -= rate*f[0]

            if not (down == 'False'):
                cost_lists[down][1] += rate*f[0]


        if mode == 1:
            # print("OOOOOOOOOOOH")
            cost_lists[node][0] -= rate*f[0]
            if not (up == 'False'):
                cost_lists[up][0] += rate*f[0]

            cost_lists[node][0] -= rate*f[1]
            if not (right == 'False'):
                cost_lists[right][2] += rate*f[1]


        if mode == 2:
            cost_lists[node][1] -= rate*f[1]
            if not (left == 'False'):
                cost_lists[left][3] += rate*f[1]

            cost_lists[node][1] -= rate*f[0]
            if not (down == 'False'):
                cost_lists[down][1] += rate*f[0]


        if mode == 3:
            # print("uhhhhhHhhHHhHhhH")
            cost_lists[node][2] -= rate*f[0]
            if not (right == 'False'):
                # print("uhhhh")
                cost_lists[right][2] += rate*f[0]

            cost_lists[node][3] -= rate*f[0]
            if not (left == 'False'):
                # print("uhhhh")
                cost_lists[left][3] += rate*f[0]


        if mode == 4:
            cost_lists[node][2] -= rate*f[0]
            if not (right == 'False'):
                cost_lists[right][2] += rate*f[0]

            cost_lists[node][2] -= rate*f[1]
            if not (down == 'False'):
                cost_lists[down][1] += rate*f[1]


        if mode == 5:
            cost_lists[node][3] -= rate*f[0]
            if not (left == 'False'):
                cost_lists[left][3] += rate*f[0]

            cost_lists[node][3] -= rate*f[1]
            if not (up == 'False'):
                cost_lists[up][0] += rate*f[1]


# for i in range(500):
# cost_list_updater(cost_lists, modes, graph_ordered_dict, 1, f_list)


# func = lambda x: max(0, int(round(x,0)))

# b =[[1.234,2.454],[2.352,9.873]]
# cost_lists = [list(map(func, i)) for i in cost_lists]
#
# print(cost_lists)