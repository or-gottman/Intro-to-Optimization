import math
from random import randint
import time
from random import shuffle


def getNeighbors(state):
    return two_opt_swap(state)

def two_opt_swap(state):
    global neighborhood_size
    neighbors = []

    for i in range(neighborhood_size):
        node1 = 0
        node2 = 0

        while node1 == node2:
            node1 = randint(1, len(state) - 1)
            node2 = randint(1, len(state) - 1)

        if node1 > node2:
            swap = node1
            node1 = node2
            node2 = swap

        tmp = state[node1:node2]
        tmp_state = state[:node1] + tmp[::-1] + state[node2:]
        neighbors.append(tmp_state)

    return neighbors


def fitness(route, graph):
    path_length = 0

    for i in range(len(route)):
        if (i + 1 != len(route)):
            dist = weight_distance(route[i], route[i + 1], graph)
            if dist != -1:
                path_length = path_length + dist
            else:
                return max_fitness  # there is no  such path

        else:
            dist = weight_distance(route[i], route[0], graph)
            if dist != -1:
                path_length = path_length + dist
            else:
                return max_fitness  # there is no  such path

    return path_length


def euclidean_distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + ((city1[1] - city2[1]) ** 2))


def weight_distance(city1, city2, graph):
    global max_fitness

    neighbors = graph[str(city1)]

    for neighbor in neighbors:
        if neighbor[0] == int(city2):
            return neighbor[1]

    return -1


def scan(matrix):
    graph = dict()
    row_num = 0
    max_weight = 0
    for row in matrix:
        node_list = list()
        col_num = 0
        for col in row:
            if col_num != row_num:
                max_weight = max(col, max_weight)
                node_list.append([col_num, col])
            col_num += 1
        graph[str(row_num)] = node_list
        row_num += 1
    return graph, max_weight


def tabu_search(matrix):
    global max_fitness, start_node

    graph, max_weight = scan(matrix)

    ## Below, get the keys (node names) and shuffle them, and make start_node as start
    s0 = list(graph.keys())
    shuffle(s0)

    if int(s0[0]) != start_node:
        for i in range(len(s0)):
            if int(s0[i]) == start_node:
                swap = s0[0]
                s0[0] = s0[i]
                s0[i] = swap
                break

    # max_fitness will act like infinite fitness
    max_fitness = ((max_weight) * (len(s0))) + 1
    sBest = s0
    vBest = fitness(s0, graph)
    bestCandidate = s0
    tabuList = []
    tabuList.append(s0)
    stop = False
    best_keep_turn = 0

    start_time = time.time()
    while not stop:
        sNeighborhood = getNeighbors(bestCandidate)
        bestCandidate = sNeighborhood[0]
        for sCandidate in sNeighborhood:
            if (sCandidate not in tabuList) and ((fitness(sCandidate, graph) < fitness(bestCandidate, graph))):
                bestCandidate = sCandidate

        if (fitness(bestCandidate, graph) < fitness(sBest, graph)):
            sBest = bestCandidate
            vBest = fitness(sBest, graph)
            best_keep_turn = 0

        tabuList.append(bestCandidate)
        if (len(tabuList) > maxTabuSize):
            tabuList.pop(0)

        if best_keep_turn == stoppingTurn:
            stop = True

        best_keep_turn += 1

    exec_time = time.time() - start_time
    return sBest, vBest, exec_time


maxTabuSize = 400
neighborhood_size = 800
stoppingTurn = 200
max_fitness = 0
start_node = 0


def run(matrix):
    solution, value, exec_time = tabu_search(matrix)
    return solution, value
