from graph import graph
from graph import nearby_nodes_from_ordered_dict
import math
from itertools import repeat
from random import randint
from modes_to_signals import modes_to_signals

# from modes_to_signals import signal_state
# import copy

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

# cost_lists = [[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]]
# print("cost_list: ", cost_lists)
# f_list = [[0.7, 0.2], [0.7, 0.2], [0.7, 0.2], [0.7, 0.2], [0.7, 0.2], [0.7, 0.2], [0.7, 0.2], [0.7, 0.2]]
# f_list = [[0.2, 0.2], [0.2, 0.2], [0.2, 0.2], [0.2, 0.2], [0.2, 0.2], [0.2, 0.2]]

# modes = [0, 0, 0, 0, 0, 0, 0, 0]
# modes = [1, 1, 1, 1, 1, 1, 1, 1]
# modes = [2, 2, 2, 2, 2, 2, 2, 2]



# for i in range(len(modes)):
#     modes[i] = 0


# G = graph(graph_ordered_dict)


# print(G['effective'])
# print(G['weight'])


def move_car_limit(pos, distance, max_distance):
    """This function is to be used in the move_cars() function. It moves a car, by a distance, making sure it will
    not exceed the max_distance. If moving it by the distance increases the distance more than the max_distance, it
    just takes it to the max_distance. The car will never exceed the max_distance."""

    updated_pos = pos+distance

    if updated_pos <= max_distance:  # the condition when the car is behind the max_distance after update
        return updated_pos
    else:  # if updating the distance make the car go ahead of the max_distance
        return max_distance


def f(f_list, pass_cars):
    """This function takes one f list and a[1] which is the pos list of cars going into next segment
    and returns the number of cars which will go STRAIGHT or right in one go"""

    straight = math.ceil(f_list[0]*pass_cars)
    right = math.floor(f_list[1]*pass_cars)

    diff = (straight+right) - pass_cars
    # print("didididi: ", diff)

    # straight +=diff

    return straight, right


def move_cars(pos_list, distance, weight, signal_bool, f_list, car_spacing=5):
    """This function updates the pos list on an edge. It changes the position of cars by the distance it would move
    in one time_step.
    pos_list is the list that contains the position of cars on a segment.
    distance is the length moved my cars moving with average speed in a time_step.
    weight is the length of the segment.
    signal_bool is the state of the signal ahead of that segment, True for Green, False for Red.
    car_spacing is the length of a car plus the distance between it and the car behind"""

    # distance = speed * time_step

    # pos_list = error_corrector(pos_list, car_spacing)

    pass_cars = 0  # number of cars that will pass to the next segment, we return this number

    if signal_bool:  # the case when the signal is GREEN and cars can move

        # pos_list_ = pos_list_aut
        pos_list_aut = [x + distance for x in pos_list]  # every car moves a distance given as a function parameter
        # this is pos list autistic

        pos_list_straight = pos_list[:]
        # print("pos_list_straight", pos_list_straight)


        # this loop checks how many cars move ahead (pass over) the weight and count the number in pass_cars
        for i in range(len(pos_list_aut)):
            if pos_list_aut[i] > weight:
                pass_cars += 1

        # straight represents number of cars to go straight and right represents no of cars to go right
        straight, right = f(f_list, pass_cars)
        # left = pass_cars-straight-right

        left_fraction = 1 - f_list[0] - f_list[1]
        left = math.floor(pass_cars * left_fraction)


        # print("straight: ", straight)
        # print("right: ", right)
        # print("pAsS cArs: ", pass_cars)

        # this loop pops the last cars that happen to pass over the edge. the idea is to return the number of passing
        # cars, so they can be added to the next edge ahead.

        pop_list_straight = []
        pop_list_right = []
        # pop_list_left = []



        pop_list = []  # full pop list

        for i in range(pass_cars):
            a = pos_list_aut.pop(-1)
            pop_list.append(a-weight)

        # print("pos_list_straight", pos_list_straight)

        # print("uh: ", pos_list)



        list.reverse(pop_list)

        # Making pos_list_straight:
        for i in range(straight+left):
            # print("pos list straight: ", pos_list_straight)
            pos_list_straight.pop(-1)



        for i in range(1, len(pos_list_straight)+1):
            pos_list_straight[-i] = move_car_limit(pos_list_straight[-i], distance, weight-(i-1)*car_spacing)


        # print("crvtbt", pos_list_straight)


        for i in range(straight):
            pop_list_straight.append(pop_list[-i-1])

        list.reverse(pop_list_straight)

        pop_list_copy = [x for x in pop_list if x not in pop_list_straight]

        for i in range(right):
            pop_list_right.append(pop_list_copy[-i-1])

        list.reverse(pop_list_right)

        pop_union_list = pop_list_straight + pop_list_right
        pop_list_left = [x for x in pop_list if x not in pop_union_list]

        # pop_list_left = []

        # for i in range(left):
        #     pop_list_left.append(pop_list[-1-i])


        # print("pop list straight: ", pop_list_straight)
        # print("pop list copy: ", pop_list_copy)
        # print("pop list right ", pop_list_right)
        # print("left: ", pop_list_left)

        # border = weight - pos_list[-1]  # the distance from the the signal to the front most car
        # print("border: ", border)

        # pos_list = [x + border for x in pos_list]  # move all the cars border length ahead, so the front car is at the very edge


        return [pop_list_straight, pop_list_right, pop_list_left], [pos_list_straight, pos_list_aut], [straight, right, left]  # the pos_list is now updated and returned along with the number of passing cars


    if not signal_bool:  # the case when cars can not pass, the signal is RED

        # find the fraction of cars that will turn left
        left_fraction = 1 - f_list[0] - f_list[1] # left number of cars needs to turn left, and we round that number upward

        pos_list_ = [x + distance for x in pos_list]

        pass_cars = 0
        for i in range(len(pos_list_)):
            if pos_list_[i] > weight:
                pass_cars += 1

        # straight, right = f(f_list, pass_cars)
        # left = pass_cars - straight - right

        left = math.floor(pass_cars*left_fraction)

        # print("LEFT: ", left)

        # this loop takes the left number of cars and moves them to the next list
        pop_list = []
        for i in range(left):
            a = pos_list.pop(-1)
            pop_list.append(a - weight)

        pop_list = [x + distance for x in pop_list]

        if len(pos_list) != 0:
            pos_list[-1] = move_car_limit(pos_list[-1], distance, weight)  # the last car has a limit of weight that it can not exceed, when the signal is red

        # this loop moves all the cars, except the one at the very front. The max_distance of a car is the position of
        # car ahead.
        for i in range(2, len(pos_list) + 1):
            # print("i: ", i)
            # print("pos[-i] before", pos_list[-i])
            pos = pos_list[-i + 1]
            # print("pos: ", pos)
            pos_list[-i] = move_car_limit(pos_list[-i], distance, pos - car_spacing)
            # print("pos[-i] after", pos_list[-i])
            # print("pos[-i+1] after", pos_list[-i+1])



        return [[], [], pop_list], [pos_list, pos_list], [0, 0, left] # number of cars going to left, the updated pos list, cars hopped to the next edge


# pos_list = [5, 13, 18, 23, 30, 35, 40, 45, 50, 60, 70, 80, 90]
# print("move_cars: ", move_cars(pos_list, 100, 100, True, [.7,.2]))
# print("updated pos list: ", pos_list)


def pos_list_gen(weight, number_of_cars, car_spacing):
    """This function generates the pos list from the cost list. It adds the cars from left to right of the segment."""

    pos_list = []
    for i in range(number_of_cars):
        pos_list.append(weight-i*car_spacing)

    list.reverse(pos_list)

    return pos_list

# pos_list_gen_ = pos_list_gen(100, 5, 5)
# print("pos_list_gen: ", pos_list_gen_)


def color_hop(source_list, sink_list, n):
    """n colors are popped from the end of source_list and added to the beginning of sink_list"""

    if sink_list == "False":
        for i in range(n):
            if source_list != []:
                source_list.pop(-1)
    else:
        for i in range(n):
            if source_list != []:
                a = source_list.pop(-1)
                sink_list.insert(0, a)


# source_list = ["red", "blue", "green"]
# sink_list = ["yellow", "golden", "purple"]
#
# color_hop(source_list, sink_list, 2)
# print("source list: ", source_list)
# print("sink list: ", sink_list)


def color_list_gen(pos_list, color):
    number_of_cars = len(pos_list)
    color_list = []
    for i in range(number_of_cars):
        color_list.append(color)

    return color_list




# signal_state = [[False, False, True, True], [False, False, True, True], [False, False, True, True], [False, False, True, True], [False, False, True, True], [False, False, True, True]]


def traffic_init(graph_ordered_dict, G, cost_lists, color_list=(), car_spacing=5):
    """This function initializes the graph by adding position list and and effective length by using the cost_list."""

    """In this loop, we assign effective lengths of each segment based on cost lists. Assume each car in a cost_list 
        takes 5 meters of space."""
    # this loop adds the effective length on each segment by using the cost list
    """Adding cars in the position list. Take the number of cars from the cost list and add them in the position list"""

    nodes = list(G.nodes())

    c = 0

    for i in range(len(nodes)):
        node = nodes[i]
        # print("node: ", node)
        up, down, right, left = nearby_nodes_from_ordered_dict(graph_ordered_dict, node)


        if not (up == 'False'):
            G[node][up]['pos_list'] = pos_list_gen(G[node][up]['weight'], cost_lists[up][0], car_spacing)
            # G[up][node]['pos_list'] = pos_list_gen(G[up][node]['weight'], cost_lists[node][1], car_spacing)

            G[node][up]['color_list'] = color_list_gen(G[node][up]['pos_list'], color_list[c])
            c += 1
            # G[up][node]['color_list'] = color_list_gen(G[up][node]['pos_list'], color_list[c])
            # c += 1

            G[node][up]['effective'] = G[node][up]['weight'] - cost_lists[up][0] * car_spacing
            # G[up][node]['effective'] = G[up][node]['weight'] - cost_lists[node][1] * car_spacing

        if not (down == 'False'):
            G[node][down]['pos_list'] = pos_list_gen(G[node][down]['weight'], cost_lists[down][1], car_spacing)
            # G[down][node]['pos_list'] = pos_list_gen(G[down][node]['weight'], cost_lists[node][0], car_spacing)

            G[node][down]['color_list'] = color_list_gen(G[node][down]['pos_list'], color_list[c])
            c += 1
            # G[down][node]['color_list'] = color_list_gen(G[down][node]['pos_list'], color_list[c])
            # c += 1

            G[node][down]['effective'] = G[node][down]['weight'] - cost_lists[down][1] * car_spacing
            # G[down][node]['effective'] = G[down][node]['weight'] - cost_lists[node][0] * car_spacing

        if not (right == 'False'):
            G[node][right]['pos_list'] = pos_list_gen(G[node][right]['weight'], cost_lists[right][2], car_spacing)
            # G[right][node]['pos_list'] = pos_list_gen(G[right][node]['weight'], cost_lists[node][3], car_spacing)

            # print("c: ", c)
            G[node][right]['color_list'] = color_list_gen(G[node][right]['pos_list'], color_list[c])
            c += 1
            # G[right][node]['color_list'] = color_list_gen(G[right][node]['pos_list'], color_list[c])
            # c += 1

            G[node][right]['effective'] = G[node][right]['weight'] - cost_lists[right][2] * car_spacing
            # G[right][node]['effective'] = G[right][node]['weight'] - cost_lists[node][3] * car_spacing

        if not (left == 'False'):
            G[node][left]['pos_list'] = pos_list_gen(G[node][left]['weight'], cost_lists[left][3], car_spacing)
            # G[left][node]['pos_list'] = pos_list_gen(G[left][node]['weight'], cost_lists[node][2], car_spacing)

            G[node][left]['color_list'] = color_list_gen(G[node][left]['pos_list'], color_list[c])
            c += 1
            # G[left][node]['color_list'] = color_list_gen(G[left][node]['pos_list'], color_list[c])
            # c += 1

            G[node][left]['effective'] = G[node][left]['weight'] - cost_lists[left][3] * car_spacing
            # G[left][node]['effective'] = G[left][node]['weight'] - cost_lists[node][2] * car_spacing

        # print(c)

def distance(speed, time_interval):
    return speed * time_interval


# def pos_list_push(pos_list, number_of_cars, distance):
#     """it adds cars at a start of pos_list"""


# print("f: ", f([.7, .2], [10, 20, 25, 30, 35, 40, 50]))





def traffic_sim(graph_ordered_dict, G, fs, modes, time_interval):
    nodes = list(G.nodes())

    for j in range(0, len(nodes)):
        node = nodes[j]
        mode = modes[j]
        f = fs[j]

        up, down, right, left = nearby_nodes_from_ordered_dict(graph_ordered_dict, node)

        # move_cars(pos_list, distance, weight, signal_bool, f_list, car_spacing=5)
        # a = [pop_list_straight, pop_list_right, pop_list_left], [pos_list_straight, pos_list_aut], [straight, right, left]   TRUE case
        # [[], [], pop_list], [pos_list, pos_list], [0, 0, left]   FALSE CASE

        if mode == 0:

            sim_thanos_straight(G, node, time_interval, f, up, down, right, left)

        if mode == 1:

            sim_thanos_aut(G, node, time_interval, f, up, down, right, left)

        if mode == 2:

            sim_thanos_aut(G, node, time_interval, f, down, up, left, right)

        if mode == 3:

            sim_thanos_straight(G, node, time_interval, f, right, left, down, up)

        if mode == 4:

            sim_thanos_aut(G, node, time_interval, f, right, left, down, up)

        if mode == 5:

            sim_thanos_aut(G, node, time_interval, f, left, right, up, down)



    # current_signals = modes_to_signals(modes)
    # last_signals_list = []




    for i in list(G.edges):

        G[i[0]][i[1]]['pos_list'] = G[i[0]][i[1]]['pos_list_temp'] + G[i[0]][i[1]]['pos_list']



        # metric(last_signals_list[-1], current_signals[i][1], G[i[0]][i[1]]['pos_list_temp'])



        # last_signals_list.append(current_signals[:])


        G[i[0]][i[1]]['pos_list_stick'] = G[i[0]][i[1]]['pos_list_temp'][:]
        G[i[0]][i[1]]['pos_list_temp'] = []



        # print("G[i[0]][i[1]]['pos_list_temp']   ", G[i[0]][i[1]]['pos_list_temp'])




    for i in list(G.edges):
        error_corrector(G[i[0]][i[1]]['pos_list'])














def sim_thanos_straight(G, node, time_interval, f, p, q, r, s):
    if not (q == 'False'):
        a = move_cars(G[q][node]['pos_list'], distance(G[q][node]['speed'], time_interval), G[q][node]['weight'],
                      True, f)
        G[q][node]['pos_list'] = a[1][0]
        straight_cars, left_cars = a[2][0], a[2][2]

        if not (p == 'False'):
            G[node][p]['pos_list_temp'] = a[0][0]
            color_hop(G[q][node]['color_list'], G[node][p]['color_list'], straight_cars)
        else:
            color_hop(G[q][node]['color_list'], "False", straight_cars)

        if not (s == 'False'):
            G[node][s]['pos_list_temp'] = a[0][2]
            color_hop(G[q][node]['color_list'], G[node][s]['color_list'], left_cars)
        else:
            color_hop(G[q][node]['color_list'], "False", left_cars)

    if not (p == 'False'):
        a = move_cars(G[p][node]['pos_list'], distance(G[p][node]['speed'], time_interval), G[p][node]['weight'], True,
                      f)
        G[p][node]['pos_list'] = a[1][0]
        straight_cars, left_cars = a[2][0], a[2][2]

        if not (q == 'False'):
            G[node][q]['pos_list_temp'] = a[0][0]
            color_hop(G[p][node]['color_list'], G[node][q]['color_list'], straight_cars)
        else:
            color_hop(G[p][node]['color_list'], "False", straight_cars)

        if not (r == 'False'):
            G[node][r]['pos_list_temp'] = a[0][2]
            color_hop(G[p][node]['color_list'], G[node][r]['color_list'], left_cars)
        else:
            color_hop(G[p][node]['color_list'], "False", left_cars)

    if not (s == 'False'):
        a = move_cars(G[s][node]['pos_list'], distance(G[s][node]['speed'], time_interval), G[s][node]['weight'],
                      False, f)
        G[s][node]['pos_list'] = a[1][0]
        left_cars = a[2][2]

        if not (p == 'False'):
            G[node][p]['pos_list_temp'] = a[0][2] + G[node][p]['pos_list_temp']
            color_hop(G[s][node]['color_list'], G[node][p]['color_list'], left_cars)
        else:
            color_hop(G[s][node]['color_list'], "False", left_cars)

    if not (r == 'False'):
        a = move_cars(G[r][node]['pos_list'], distance(G[r][node]['speed'], time_interval),
                      G[r][node]['weight'], False, f)
        G[r][node]['pos_list'] = a[1][0]
        left_cars = a[2][2]

        if not (q == 'False'):
            G[node][q]['pos_list_temp'] = a[0][2] + G[node][q]['pos_list_temp']
            color_hop(G[r][node]['color_list'], G[node][q]['color_list'], left_cars)
        else:
            color_hop(G[r][node]['color_list'], "False", left_cars)



def sim_thanos_aut(G, node, time_interval, f, p, q, r, s):
    if not (q == 'False'):
        a = move_cars(G[q][node]['pos_list'], distance(G[q][node]['speed'], time_interval), G[q][node]['weight'],
                      True, f)
        G[q][node]['pos_list'] = a[1][1]
        straight_cars, r_cars, left_cars = a[2][0], a[2][1], a[2][2]

        if not (p == 'False'):
            G[node][p]['pos_list_temp'] = a[0][0]
            color_hop(G[q][node]['color_list'], G[node][p]['color_list'], straight_cars)
        else:
            color_hop(G[q][node]['color_list'], "False", straight_cars)

        if not (r == 'False'):
            G[node][r]['pos_list_temp'] = a[0][1]
            color_hop(G[q][node]['color_list'], G[node][r]['color_list'], r_cars)
        else:
            color_hop(G[q][node]['color_list'], "False", r_cars)

        if not (s == 'False'):
            G[node][s]['pos_list_temp'] = a[0][2]
            color_hop(G[q][node]['color_list'], G[node][s]['color_list'], left_cars)
        else:
            color_hop(G[q][node]['color_list'], "False", left_cars)

    if not (r == 'False'):
        a = move_cars(G[r][node]['pos_list'], distance(G[r][node]['speed'], time_interval),
                      G[r][node]['weight'], False, f)
        G[r][node]['pos_list'] = a[1][0]
        left_cars = a[2][2]

        if not (q == 'False'):
            G[node][q]['pos_list_temp'] = a[0][2]
            color_hop(G[r][node]['color_list'], G[node][q]['color_list'], left_cars)
        else:
            color_hop(G[r][node]['color_list'], "False", left_cars)

    if not (p == 'False'):
        a = move_cars(G[p][node]['pos_list'], distance(G[p][node]['speed'], time_interval), G[p][node]['weight'], False,
                      f)
        G[p][node]['pos_list'] = a[1][0]
        left_cars = a[2][2]

        if not (r == 'False'):
            G[node][r]['pos_list_temp'] = a[0][2] + G[node][r]['pos_list_temp']
            color_hop(G[p][node]['color_list'], G[node][r]['color_list'], left_cars)
        else:
            color_hop(G[p][node]['color_list'], "False", left_cars)

    if not (s == 'False'):
        a = move_cars(G[s][node]['pos_list'], distance(G[s][node]['speed'], time_interval), G[s][node]['weight'],
                      False, f)
        G[s][node]['pos_list'] = a[1][0]
        left_cars = a[2][2]

        if not (p == 'False'):
            G[node][p]['pos_list_temp'] = a[0][2] + G[node][p]['pos_list_temp']
            color_hop(G[s][node]['color_list'], G[node][p]['color_list'], left_cars)
        else:
            color_hop(G[s][node]['color_list'], "False", left_cars)








def error_corrector(pos_list, car_spacing=5):
    list.sort(pos_list)

    for i in range(len(pos_list)-1):
        diff = pos_list[i+1] - pos_list[i]

        if diff < 5:
            pos_list[i+1] = pos_list[i] + car_spacing

    return pos_list


# print("error correction: ", error_corrector([997, 1000])


def cost_list_from_pos_list(pos_list, weight, car_spacing=5):

    if len(pos_list) == 0:
        return 0


    if pos_list[-1] == weight:
        count = 1

        for i in range(1, len(pos_list)):
            diff = pos_list[-i] - pos_list[-i-1]

            if diff <= car_spacing:
                count += 1
        return count
    else:
        return 0


# print("cost_list_from_pos_list: ", cost_list_from_pos_list([980, 985, 990, 995, 1000], 1000))





def cost_list_generator(G, graph_ordered_dict, car_spacing=5):
    """This function takes updated pos_lists at the end of each iteration and converts them to cost_lists"""

    nodes = list(G.nodes())

    cost_lists = [[0,0,0,0] for i in repeat(None, len(nodes))]

    for i in range(len(nodes)):

        node = nodes[i]
        up, down, right, left = nearby_nodes_from_ordered_dict(graph_ordered_dict, node)

        if not (down == 'False'):
            cost_lists[i][0] = cost_list_from_pos_list(G[down][node]['pos_list'], G[down][node]['weight'], car_spacing)
        if not (up == 'False'):
            cost_lists[i][1] = cost_list_from_pos_list(G[up][node]['pos_list'], G[up][node]['weight'], car_spacing)
        if not (left == 'False'):
            cost_lists[i][2] = cost_list_from_pos_list(G[left][node]['pos_list'], G[left][node]['weight'], car_spacing)
        if not (right == 'False'):
            cost_lists[i][3] = cost_list_from_pos_list(G[right][node]['pos_list'], G[right][node]['weight'], car_spacing)

    return cost_lists



def cost_lists_init(number_of_nodes, min_number_of_cars=1, max_number_of_cars=10, repeat_list=[]):

    if repeat_list == []:
        cost_lists = []
        cost_list = []

        for i in range(number_of_nodes):
            for j in range(4):
                number_of_cars = randint(min_number_of_cars, max_number_of_cars)
                cost_list.append(number_of_cars)
            cost_lists.append(cost_list)
            cost_list = []

        return cost_lists

    else:
        cost_lists = []

        for i in range(number_of_nodes):
            cost_lists.append(repeat_list)

    return cost_lists


# print(cost_list_init(5, repeat_list=[5, 10, 5, 10]))


def f_lists_init(number_of_nodes, repeat_list=[0.7, 0.3]):

    f_lists = []

    for i in range(number_of_nodes):
        f_lists.append(repeat_list)

    return f_lists

# print(f_lists_init(5))


# print("bvhhd  ", G[4][5]['pos_list'])
# traffic_init(graph_ordered_dict, G, cost_lists, car_spacing=5)
# print("bvhhdfgg  ", G[0][1]['pos_list'])
# print("COST LISTS: ", cost_list_generator(G, graph_ordered_dict))











# traffic_init(graph_ordered_dict, G, cost_lists)

# print("BB Before: ", G[1][4]['pos_list'])
# print("BB Before[4][7]: ", G[4][7]['pos_list'])
# print("BB Before[7][4]: ", G[7][4]['pos_list'])
# print("BB weight[7][4]: ", G[7][4]['weight'])
# print("BB weight: ", G[1][4]['weight'])
# print("BB speed: ", G[1][4]['speed'])
# traffic_sim(graph_ordered_dict, G, cost_lists, f_list, modes, 1, car_spacing=5)
# print("AA after: ", G[1][4]['pos_list'])
# print("AA after[7][4]: ", G[7][4]['pos_list'])


# traffic_init(graph_ordered_dict, G, cost_lists, car_spacing=5)
# G[5][4]['pos_list'] = [995, 986, 970, 965, 960]


# print("\nBEFORE\n")
# print("G[1][4] ", G[1][4]['pos_list'])
# print("G[4][1] ", G[4][1]['pos_list'])
# print("G[4][3] ", G[4][3]['pos_list'])
# print("G[3][4] ", G[3][4]['pos_list'])
# print("G[4][5] ", G[4][5]['pos_list'])
# print("G[5][4] ", G[5][4]['pos_list'])
# print("G[4][7] ", G[4][7]['pos_list'])
# print("G[7][4] ", G[7][4]['pos_list'])


# traffic_sim(graph_ordered_dict, G, cost_lists, f_list, modes, 1, car_spacing=5)
# traffic_sim(graph_ordered_dict, G, f_list, modes, 1)

# print("\nAFTER\n")
# print("G[1][4] ", G[1][4]['pos_list'])
# print("G[4][1] ", G[4][1]['pos_list'])
# print("G[4][3] ", G[4][3]['pos_list'])
# print("G[3][4] ", G[3][4]['pos_list'])
# print("G[4][5] ", G[4][5]['pos_list'])
# print("G[5][4] ", G[5][4]['pos_list'])
# print("G[4][7] ", G[4][7]['pos_list'])
# print("G[7][4] ", G[7][4]['pos_list'])



# traffic_init(graph_ordered_dict, G, cost_lists, 5)

# for node1, node2, data in G.edges(data=True):
#     print("Weight: ", data['weight'])
#     print("effective after: ", data['effective'])
#     print("pos after: ", data['pos_list'])
#     # print("Effective after: ", data['effective'])
