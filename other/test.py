tree = {'A': [['B', 1], ['C', 2], ['D', 4]],
               'B': [['F', 5], ['E', 4]],
               'C': [['E', 1]],
               'D': [['H', 1], ['I', 4], ['J', 2]],
               'E': [['G', 2], ['H', 3]],
               'F': [['G', 1]],
               'G': [['K', 6]],
               'H': [['K', 6], ['L', 5]],
               'I': [['L', 3]],
               'J': [],
               'K': [],
               'L': [],
               }

tree2 = {'S': [['A', 1], ['B', 2]],
         'A': [['S', 1]],
         'B': [['S', 2], ['C', 3], ['D', 4]],
         'C': [['B', 2], ['E', 5], ['F', 6]],
         'D': [['B', 4], ['G', 7]],
         'E': [['C', 5]],
         'F': [['C', 6]]
         }

heuristic = {'A': 6,
              'B': 5,
              'C': 5,
              'D': 2,
              'E': 4,
              'F': 5,
              'G': 4,
              'H': 1,
              'I': 2,
              'J': 1,
              'K': 0,
              'L': 0, }
heuristic2 = {'S': 0, 'A': 5000, 'B': 2, 'C': 3, 'D': 4, 'E': 5000, 'F': 5000, 'G': 0}

cost = {'A': 0}             # total cost for nodes visited


def AStarSearch():
    global tree, heuristic
    closed = []             # closed nodes
    opened = [['A', 6]]     # opened nodes

    '''find the visited nodes'''
    while True:
        fn = [i[1] for i in opened]     # fn = f(n) = g(n) + h(n)
        chosen_index = fn.index(min(fn))
        node = opened[chosen_index][0]  # current node
        closed.append(opened[chosen_index])
        del opened[chosen_index]
        if closed[-1][0] == 'K' or closed[-1][0] == 'L':        # break the loop if node G has been found
            break

        print(tree)
        for item in tree[node]:
            if item[0] in [closed_item[0] for closed_item in closed]:
                continue
            cost.update({item[0]: cost[node] + item[1]})            # add nodes to cost dictionary
            fn_node = cost[node] + heuristic[item[0]] + item[1]     # calculate f(n) of current node
            temp = [item[0], fn_node]
            opened.append(temp)                                     # store f(n) of current node in array opened

    '''find optimal sequence'''
    trace_node = 'K'                        # correct optimal tracing node, initialize as node G
    optimal_sequence = ['K']                # optimal node sequence
    for i in range(len(closed)-2, -1, -1):
        check_node = closed[i][0]           # current node
        if trace_node in [children[0] for children in tree[check_node]]:
            children_costs = [temp[1] for temp in tree[check_node]]
            children_nodes = [temp[0] for temp in tree[check_node]]

            '''check whether h(s) + g(s) = f(s). If so, append current node to optimal sequence
            change the correct optimal tracing node to current node'''
            if cost[check_node] + children_costs[children_nodes.index(trace_node)] == cost[trace_node]:
                optimal_sequence.append(check_node)
                trace_node = check_node
    optimal_sequence.reverse()              # reverse the optimal sequence

    return closed, optimal_sequence


if __name__ == '__main__':
    visited_nodes, optimal_nodes = AStarSearch()
    print('visited nodes: ' + str(visited_nodes))
    print('optimal nodes sequence: ' + str(optimal_nodes))