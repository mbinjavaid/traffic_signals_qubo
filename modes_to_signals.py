def solutions_to_modes(sliced_solution):


    mode_list = []
    for i in sliced_solution:
        index = i.index(1)
        # print("index:", index)

        mode_list.append(index)

    return mode_list


def modes_to_signals(mode_list):

    index_list = []

    for j in mode_list:

        # True means that particular segment going towards the node is DECREASED.

        # WHEN INCREASING, REMEMBER 0.8 AND 0.2

        # NEED TO INCLUDE UPDATE OF LEFT GOING CARS

        if j == 0:
            index_list.append([True, True, False, False])
        if j == 1:
            index_list.append([True, False, False, False])
        if j == 2:
            index_list.append([False, True, False, False])
        if j == 3:
            index_list.append([False, False, True, True])
        if j == 4:
            index_list.append([False, False, True, False])
        if j == 5:
            index_list.append([False, False, False, True])

    return index_list


def signal_state(sliced_solution):

    mode_list = solutions_to_modes(sliced_solution)

    signal_state_ = modes_to_signals(mode_list)

    return signal_state_


def sel_rules_to_mode_list(sliced_solution):

    mode_list = []

    for i in range(len(sliced_solution)):
        mode = sliced_solution[i].index(1)
        mode_list.append(mode)

    return mode_list