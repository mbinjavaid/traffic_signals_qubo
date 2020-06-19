from graph import graph
from graph import nearby_nodes_from_ordered_dict
import math
# from modes_to_signals import signal_state


graph_ordered_dict = {
    0: [3, 'False', 1, 'False'],
    1: [4, 'False', 2, 0],
    2: [5, 'False', 'False', 1],
    3: [6, 0, 4, 'False'],
    4: [7, 1, 5, 3],
    5: [8, 2, 'False', 4],
    6: ['False', 3, 7, 'False'],
    7: ['False', 4, 8, 6],
    8: ['False', 5, 'False', 7]
}

cost_lists = [[5, 20, 25, 30], [5, 20, 5, 30], [5, 20, 2, 2], [5, 4, 25, 30], [5, 4, 25, 30], [5, 4, 25, 30], [5, 20, 25, 30], [5, 20, 25, 30], [5, 20, 25, 30], [5, 20, 25, 30], [5, 20, 25, 30], [5, 20, 25, 30]]
print("cost_list: ", cost_lists)
f_list = [[0.7, 0.2], [0.7, 0.2], [0.7, 0.2], [0.7, 0.2], [0.7, 0.2], [0.7, 0.2]]

modes = [0, 0, 0, 0, 0, 0]


# for i in range(len(modes)):
#     modes[i] = 0


G = graph(graph_ordered_dict)


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
    right = math.ceil(f_list[1]*pass_cars)

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

    pass_cars = 0  # number of cars that will pass to the next segment, we return this number

    if signal_bool:  # the case when the signal is GREEN and cars can move

        pos_list = [x + distance for x in pos_list]  # every car moves a distance given as a function parameter


        # this loop checks how many cars move ahead (pass over) the weight and count the number in pass_cars
        for i in range(len(pos_list)):
            if pos_list[i] > weight:
                pass_cars += 1

        # straight represents number of cars to go straight and right represents no of cars to go right
        straight, right = f(f_list, pass_cars)
        # print("stright: ", straight)
        # print("right: ", right)

        # this loop pops the last cars that happen to pass over the edge. the idea is to return the number of passing
        # cars, so they can be added to the next edge ahead.

        pop_list_straight = []
        pop_list_right = []
        # pop_list_left = []

        pop_list = []

        for i in range(pass_cars):
            a = pos_list.pop(-1)
            pop_list.append(a-weight)

        # print("uh: ", pos_list)

        list.reverse(pop_list)


        for i in range(straight):
            pop_list_straight.append(pop_list[-i-1])

        list.reverse(pop_list_straight)

        pop_list_copy = [x for x in pop_list if x not in pop_list_straight]

        for i in range(right):
            pop_list_right.append(pop_list_copy[-i-1])

        list.reverse(pop_list_right)

        pop_union_list = pop_list_straight + pop_list_right
        pop_list_left = [x for x in pop_list if x not in pop_union_list]

        # print("pop list straight: ", pop_list_straight)
        # print("pop list copy: ", pop_list_copy)
        # print("pop list right ", pop_list_right)
        # print("left: ", pop_list_left)

        # border = weight - pos_list[-1]  # the distance from the the signal to the front most car
        # print("border: ", border)

        # pos_list = [x + border for x in pos_list]  # move all the cars border length ahead, so the front car is at the very edge

        return pass_cars, [pop_list_straight, pop_list_right, pop_list_left], pos_list  # the pos_list is now updated and returned along with the number of passing cars


    if not signal_bool:  # the case when cars can not pass, the signal is RED

        # find the fraction of cars that will turn left
        left_fraction = 1 - f_list[0] - f_list[1] # left number of cars needs to turn left, and we round that number upward

        pos_list_ = [x + distance for x in pos_list]

        pass_cars = 0
        for i in range(len(pos_list_)):
            if pos_list_[i] > weight:
                pass_cars += 1

        left = math.ceil(pass_cars*left_fraction)

        # this loop takes the left number of cars and moves them to the next list
        pop_list = []
        for i in range(left):
            a = pos_list.pop(-1)
            pop_list.append(a - weight)

        pop_list = [x + distance for x in pop_list]

        pos_list[-1] = move_car_limit(pos_list[-1], distance, weight)  # the last car has a limit of weight that it can not exceed, when the signal is red

        # this loop moves all the cars, except the one at the very front. The max_distance of a car is the position of
        # car ahead.
        for i in range(2, len(pos_list)+1):
            # print("i: ", i)
            # print("pos[-i] before", pos_list[-i])
            pos = pos_list[-i+1]
            # print("pos: ", pos)
            pos_list[-i] = move_car_limit(pos_list[-i], distance, pos - car_spacing)
            # print("pos[-i] after", pos_list[-i])
            # print("pos[-i+1] after", pos_list[-i+1])

        return left, pos_list, pop_list  # number of cars going to left, the updated pos list, cars hopped to the next edge


pos_list = [5, 13, 18, 23, 30, 35, 40, 45, 50]
print("move_cars: ", move_cars(pos_list, 50, 60, False, [.7,.2]))
print("updated pos list: ", pos_list)


def pos_list_gen(weight, number_of_cars, car_spacing):
    """This function generates the pos list from the cost list. It adds the cars from left to right of the segment."""

    pos_list = []
    for i in range(number_of_cars):
        pos_list.append(weight-i*car_spacing)

    list.reverse(pos_list)

    return pos_list

pos_list_gen_ = pos_list_gen(100, 5, 5)
# print("pos_list_gen: ", pos_list_gen_)




signal_state = [[False, False, True, True], [False, False, True, True], [False, False, True, True], [False, False, True, True], [False, False, True, True], [False, False, True, True]]


def traffic_init(graph_ordered_dict, G, cost_lists, car_spacing=5):
    """This function initializes the graph by adding position list and and effective length by using the cost_list."""

    """In this loop, we assign effective lengths of each segment based on cost lists. Assume each car in a cost_list 
        takes 5 meters of space."""
    # this loop adds the effective length on each segment by using the cost list
    """Adding cars in the position list. Take the number of cars from the cost list and add them in the position list"""

    nodes = list(G.nodes())

    for i in range(len(nodes)):
        node = nodes[i]

        up, down, right, left = nearby_nodes_from_ordered_dict(graph_ordered_dict, node)

        if not (up == 'False'):
            G[node][up]['pos_list'] = pos_list_gen(G[node][up]['weight'], cost_lists[up][0], car_spacing)
            G[up][node]['pos_list'] = pos_list_gen(G[up][node]['weight'], cost_lists[node][1], car_spacing)

            G[node][up]['effective'] = G[node][up]['weight'] - cost_lists[up][0] * car_spacing
            G[up][node]['effective'] = G[up][node]['weight'] - cost_lists[node][1] * car_spacing

        if not (down == 'False'):
            G[node][down]['pos_list'] = pos_list_gen(G[node][down]['weight'], cost_lists[down][1], car_spacing)
            G[down][node]['pos_list'] = pos_list_gen(G[down][node]['weight'], cost_lists[node][0], car_spacing)

            G[node][down]['effective'] = G[node][down]['weight'] - cost_lists[down][1] * car_spacing
            G[down][node]['effective'] = G[down][node]['weight'] - cost_lists[node][0] * car_spacing

        if not (right == 'False'):
            G[node][right]['pos_list'] = pos_list_gen(G[node][right]['weight'], cost_lists[right][2], car_spacing)
            G[right][node]['pos_list'] = pos_list_gen(G[right][node]['weight'], cost_lists[node][3], car_spacing)

            G[node][right]['effective'] = G[node][right]['weight'] - cost_lists[right][2] * car_spacing
            G[right][node]['effective'] = G[right][node]['weight'] - cost_lists[node][3] * car_spacing

        if not (left == 'False'):
            G[node][left]['pos_list'] = pos_list_gen(G[node][left]['weight'], cost_lists[left][3], car_spacing)
            G[left][node]['pos_list'] = pos_list_gen(G[left][node]['weight'], cost_lists[node][2], car_spacing)

            G[node][left]['effective'] = G[node][left]['weight'] - cost_lists[left][3] * car_spacing
            G[left][node]['effective'] = G[left][node]['weight'] - cost_lists[node][2] * car_spacing


def distance(speed, time_interval):
    return speed * time_interval


# def pos_list_push(pos_list, number_of_cars, distance):
#     """it adds cars at a start of pos_list"""


# print("f: ", f([.7, .2], [10, 20, 25, 30, 35, 40, 50]))

traffic_init(graph_ordered_dict, G, cost_lists, car_spacing=5)



def traffic_sim(graph_ordered_dict, G, cost_lists, fs, modes, time_interval, car_spacing=5):
    nodes = list(G.nodes())

    # for i in range(2, len(nodes)):
    for i in range(4,5):
        node = nodes[i]
        mode = modes[i]
        f = fs[i]

        up, down, right, left = nearby_nodes_from_ordered_dict(graph_ordered_dict, node)

        # move_cars(pos_list, distance, weight, signal_bool, f_list, car_spacing=5)
        # a = [pass_cars, [pop_list_straight, pop_list_right, pop_list_left], pos_list]   TRUE case
        # a = [left, pos_list, pop_list]   FALSE CASE

        if mode == 0:

            if G[node][up]['effective'] < 5:
                a = move_cars(G[down][node]['pos_list'], distance(G[down][node]['speed'], time_interval), G[down][node]['weight'], False, f)
                G[down][node]['pos_list'] = a[1]
                G[node][left]['pos_list'] = a[0] + G[node][left]['pos_list'] # handles cars going left


            else:
                a = move_cars(G[down][node]['pos_list'], distance(G[down][node]['speed'], time_interval), G[down][node]['weight'], True, f)
                G[down][node]['pos_list'] = a[2]
                G[node][up]['pos_list'] = a[1][0] + G[node][up]['pos_list']
                G[node][left]['pos_list'] = a[1][2] + G[node][left]['pos_list']    # handles cars going left



            if G[node][down]['effective']


            a = move_cars(G[up][node]['pos_list'], distance(G[up][node]['speed'], time_interval), G[up][node]['weight'], True, f)
            G[up][node]['pos_list'] = a[2]
            G[node][down]['pos_list'] = a[1][0] + G[node][down]['pos_list']

            a = move_cars(G[left][node]['pos_list'], distance(G[left][node]['speed'], time_interval), G[left][node]['weight'], False, f)
            # print(c)
            G[left][node]['pos_list'] = a[1]

            a = move_cars(G[right][node]['pos_list'], distance(G[right][node]['speed'], time_interval), G[right][node]['weight'], False, f)
            G[right][node]['pos_list'] = a[1]

            # print("G[node][up]['pos_list'] : ", G[node][up]['pos_list'])

        if mode == 1:

            a = move_cars(G[down][node]['pos_list'], distance(G[down][node]['speed'], time_interval), G[down][node]['weight'], True, f)
            G[node][up]['pos_list'] = a[1][0] + G[node][up]['pos_list']
            G[node][right]['pos_list'] = a[1][1] + G[node][right]['pos_list']


            # print("G[node][up]['pos_list'] : ", G[node][up]['pos_list'])


# traffic_init(graph_ordered_dict, G, cost_lists)

print("BB Before: ", G[1][4]['pos_list'])
print("BB Before[4][7]: ", G[4][7]['pos_list'])
print("BB Before[7][4]: ", G[7][4]['pos_list'])
print("BB weight[7][4]: ", G[7][4]['weight'])
print("BB weight: ", G[1][4]['weight'])
print("BB speed: ", G[1][4]['speed'])
traffic_sim(graph_ordered_dict, G, cost_lists, f_list, modes, 1, car_spacing=5)
print("AA after: ", G[1][4]['pos_list'])
print("AA after[7][4]: ", G[7][4]['pos_list'])


# traffic_init(graph_ordered_dict, G, cost_lists, 5)

# for node1, node2, data in G.edges(data=True):
#     print("Weight: ", data['weight'])
#     print("effective after: ", data['effective'])
#     print("pos after: ", data['pos_list'])
#     # print("Effective after: ", data['effective'])
