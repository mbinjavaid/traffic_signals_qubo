import numpy as np
import pandas as pd
from Q_proper import Q
from graph import graph, ordered_dict_generator, nearby_nodes_from_ordered_dict
from grid_graph import two_nodes_relation
from modes_to_signals import sel_rules_to_mode_list, modes_to_signals
from qbsolv import QBSolve_classical_solution, solution_slicer, QBSolve_quantum_solution
from simulation_under_hood import traffic_init, traffic_sim, cost_list_generator, cost_lists_init, f_lists_init
from visualization import graph_topo, color_gen



def modes_from_Q(G, times_list, token, graph_ordered_dict, cost_lists, lembda, runtime, run, annealing_time,
                 first_time):
    Q_ = Q(G, graph_ordered_dict, cost_lists, lembda, runtime, run, first_time)

    if token == "":  # Solve classically if no token given, otherwise send to QC using the entered token.
        sol = QBSolve_classical_solution(Q_, times_list)
    else:
        sol = QBSolve_quantum_solution(Q_, times_list, token, annealing_time)

    sliced_sol = solution_slicer(sol)
    print("Sliced Sol: ", sliced_sol)

    error = 0

    for i in sliced_sol:
        counter = 0
        for j in i:
            if j == 1:
                counter += 1
            if counter > 1:
                error += 1
                break

    mode_list = sel_rules_to_mode_list(sliced_sol)

    return mode_list, error


def modes_from_cycle(G, last_signal_list):
    no_of_nodes = len(list(G.nodes()))

    if last_signal_list[0] == 0:
        return [1] * no_of_nodes

    if last_signal_list[0] == 1:
        return [2] * no_of_nodes

    if last_signal_list[0] == 2:
        return [3] * no_of_nodes

    if last_signal_list[0] == 3:
        return [4] * no_of_nodes

    if last_signal_list[0] == 4:
        return [5] * no_of_nodes

    if last_signal_list[0] == 5:
        return [0] * no_of_nodes


def metric_q3(last_signal_list_, temp_list, first_time=False):
    """This function returns a parameter that quantifies how well Q3 is working - namely, how many cars pass
    through signals unhindered"""

    for item in last_signal_list_:
        if not item:
            return 0

    return len(temp_list)


def metric_q3_bad(G, graph_ordered_dict_, mode, cost_list, b):
    """This function returns a parameter that quantifies how well Q3 is working - namely, how many cars pass
    through signals unhindered"""

    badness = 0
    up, down, right, left = nearby_nodes_from_ordered_dict(graph_ordered_dict_, b)

    if mode == 0:
        if right != 'False':
            badness += G[b][right]['speed'] * 0.7 * cost_list[2]
        if down != 'False':
            badness += G[b][down]['speed'] * 0.3 * cost_list[2]

        if left != 'False':
            badness += G[b][left]['speed'] * 0.7 * cost_list[3]
        if up != 'False':
            badness += G[b][up]['speed'] * 0.3 * cost_list[3]

    if mode == 1:
        if down != 'False':
            badness += G[b][down]['speed'] * 0.7 * cost_list[1]
            badness += G[b][down]['speed'] * 0.3 * cost_list[2]
        if left != 'False':
            badness += G[b][left]['speed'] * 0.3 * cost_list[1]
            badness += G[b][left]['speed'] * 0.7 * cost_list[3]

        if right != 'False':
            badness += G[b][right]['speed'] * 0.7 * cost_list[2]

        if up != 'False':
            badness += G[b][up]['speed'] * 0.3 * cost_list[3]

    if mode == 2:
        if up != 'False':
            badness += G[b][up]['speed'] * 0.7 * cost_list[0]
            badness += G[b][up]['speed'] * 0.3 * cost_list[3]
        if right != 'False':
            badness += G[b][right]['speed'] * 0.3 * cost_list[0]
            badness += G[b][right]['speed'] * 0.7 * cost_list[2]
        if down != 'False':
            badness += G[b][down]['speed'] * 0.3 * cost_list[2]
        if left != 'False':
            badness += G[b][left]['speed'] * 0.7 * cost_list[3]

    if mode == 3:
        if up != 'False':
            badness += G[b][up]['speed'] * 0.7 * cost_list[0]
        if right != 'False':
            badness += G[b][right]['speed'] * 0.3 * cost_list[0]
        if down != 'False':
            badness += G[b][down]['speed'] * 0.7 * cost_list[1]
        if left != 'False':
            badness += G[b][left]['speed'] * 0.3 * cost_list[1]

    if mode == 4:
        if up != 'False':
            badness += G[b][up]['speed'] * 0.7 * cost_list[0]
            badness += G[b][up]['speed'] * 0.3 * cost_list[3]
        if right != 'False':
            badness += G[b][right]['speed'] * 0.3 * cost_list[0]
        if down != 'False':
            badness += G[b][down]['speed'] * 0.7 * cost_list[1]
        if left != 'False':
            badness += G[b][left]['speed'] * 0.3 * cost_list[1]
            badness += G[b][left]['speed'] * 0.7 * cost_list[3]

    if mode == 5:
        if up != 'False':
            badness += G[b][up]['speed'] * 0.7 * cost_list[0]
        if right != 'False':
            badness += G[b][right]['speed'] * 0.3 * cost_list[0]
            badness += G[b][right]['speed'] * 0.7 * cost_list[2]
        if down != 'False':
            badness += G[b][down]['speed'] * 0.7 * cost_list[1]
            badness += G[b][down]['speed'] * 0.3 * cost_list[2]
        if left != 'False':
            badness += G[b][left]['speed'] * 0.3 * cost_list[1]

    return badness


def metric_q1(cost_lists_):
    """This function returns a parameter that quantifies how well Q1 is working -- namely, how many cars at any given
    time are stopped / are positioned bumper to bumper"""

    num = 0

    for item in cost_lists_:
        for j in item:
            num += j

    return num


main_badness_list = []


def Main(token, annealing_time, lembda):

    nu = pd.read_csv('skeli.csv', dtype=object)  # Dataframe to export values in csv format

    dim = 6

    times_list = []

    graph_ordered_dict = ordered_dict_generator(dim)
    print("graph_ordered_dict", graph_ordered_dict)

    G = graph(graph_ordered_dict)

    cost_lists = cost_lists_init(G.number_of_nodes(), repeat_list=[30, 30, 30, 30])

    f_lists = f_lists_init(G.number_of_nodes())



    edges = list(G.edges())
    nodes = list(G.nodes())

    color_list = color_gen(len(edges))

    traffic_init(graph_ordered_dict, G, cost_lists, color_list)

    runtime_list = []

    goodness = 0
    badness = 0


    run = 0

    error = 0

    mode_list_ = modes_from_Q(G, times_list, token, graph_ordered_dict, cost_lists, lembda, 1, run, annealing_time,
                              first_time=True)

    mode_list = mode_list_[0]


    signals = modes_to_signals(mode_list)


    print("MODES:\n\n", mode_list)

    graph_topo(G, dim)



    stopped_list = []
    stopped = metric_q1(cost_lists)
    stopped_list.append(stopped)

    buff = 4

    last_signal_list = []
    signal_list = []


    while run < 150:


        avg_stopped = np.mean(stopped_list)  # quantifies how much q1 is dominant

        if run % 5 == 0 and run != 0:

            mode_list_ = modes_from_Q(G, times_list, token, graph_ordered_dict, cost_lists, lembda, 1, run,
                                      annealing_time, first_time=False)  # 1 is the avg runtime

            mode_list = mode_list_[0]

            error += mode_list_[1]


            signals = modes_to_signals(mode_list)


        signal_list.append(signals)

        for i in range(len(edges)):


            a = edges[i][0]
            b = edges[i][1]

            pos_list_stick = G[a][b]['pos_list_stick']

            relation = two_nodes_relation(nodes, a, b, graph_ordered_dict)

            mode = mode_list[b]
            cost_list = cost_lists[b]

            if run >= buff:

                for i in range(1, buff + 1):

                    if relation == 'up':
                        current_signal = signal_list[-i][a][0]

                    if relation == 'down':
                        current_signal = signal_list[-i][a][1]

                    if relation == 'right':
                        current_signal = signal_list[-i][a][2]

                    if relation == 'left':
                        current_signal = signal_list[-i][a][3]

                    last_signal_list.append(current_signal)

            goodness += metric_q3(last_signal_list, pos_list_stick)
            badness += metric_q3_bad(G, graph_ordered_dict, mode, cost_list, b)

            last_signal_list = []

        traffic_sim(graph_ordered_dict, G, f_lists, mode_list, 1)
        cost_lists = cost_list_generator(G, graph_ordered_dict)

        stopped = metric_q1(cost_lists)
        stopped_list.append(stopped)

        run += 1

        counter = 0

        for i in range(len(edges)):
            a = edges[i][0]
            b = edges[i][1]

            counter += len(G[a][b]['pos_list'])

    nu.to_csv('Output/results_' + str(annealing_time) + '.csv', index=False)
    nu.to_pickle('Output/results_' + str(annealing_time) + '.pkl')

    print("\nStoppedness: ", avg_stopped)
    print("Goodness: ", goodness)
    print("Badness: ", badness)
    main_badness_list.append(badness)
    print("\nNumber of errors related to lambda: ", error)

    print("PROBLEM 1 DONEEEE")

    print("\n\n\n\n")
    return 0


Main(token="", annealing_time=20, lembda=60)


print("Badness List:", main_badness_list)
