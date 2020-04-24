class Node:  # Node has only PARENT_NODE, STATE, DEPTH
    def __init__(self, state, parent=None, depth=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth
        self.TOTAL_COST = None

    def path(self):  # Create a list of nodes from the root to this node.
        current_node = self
        path = [self]
        while current_node.PARENT_NODE:  # while current node has parent
            current_node = current_node.PARENT_NODE  # make parent the current node
            path.append(current_node)  # add current node to path
        return path

    def display(self):
        print(self)

    def __repr__(self):
        return 'State: ' + str(self.STATE) + ' - Depth: ' + str(self.DEPTH)


'''
Search the tree for the goal state and return path from initial state to goal state
'''


def TREE_SEARCH():
    fringe = []
    initial_node = Node(INITIAL_STATE)
    fringe = INSERT(initial_node, fringe)
    while fringe is not None:
        node = REMOVE_BEST(fringe)
        if node.STATE[0] in GOAL_STATE:
            return node.path()
        children = EXPAND(node)
        fringe = INSERT_ALL(children, fringe)
        print("fringe: {}".format(fringe))


'''
Expands node and gets the successors (children) of that node.
Return list of the successor nodes.
'''


def EXPAND(node):
    successors = []
    calculatedlist = []
    children = successor_fn(node.STATE)
    children.append(node.STATE)  # tilføjer også den vi kommer fra til child listen
    for child in children:
        s = Node(node)  # create node for each in state list
        s.STATE = child  # e.g. result = 'F' then 'G' from list ['F', 'G']
        s.PARENT_NODE = node
        s.DEPTH = node.DEPTH + 1
        successors = INSERT(s, successors)
    for entry in successors:
        # if (entry.STATE[0] in [closed_item for closed_item in VISITED]):  # hvis noden har været besøgt, ignorer og fortsæt
        if (entry.STATE[0] in VISITED):
            continue
        COST.update({entry.STATE[0]: COST[node.STATE[0]] + entry.STATE[
            1]})  # opdatere node costen (kun med rute cost op til noden)
        calculatedlist.append(entry)  # tilføjer noden til fringe
    return calculatedlist


# FIFO
def INSERT(node, queue):
    queue.append(node)
    return queue


'''
#LIFO
def INSERT(node, queue):
    queue.insert(0, node)
    return queue
'''

'''
Insert list of nodes into the fringe
'''


def INSERT_ALL(list, queue):
    for e in list:
        queue.append(e)
    return queue


'''
Removes and returns the best element from fringe
'''


# '''
def REMOVE_BEST(queue):
    fn = []
    for entry in queue:
        fn_node = COST[entry.STATE[0]] + HEURISTICS[
            entry.STATE[0]]  # udregner hvad noden koster, med rute og heuristic. fn = gn + hn
        fn.append(fn_node)
    chosen_index = fn.index(min(fn))  # finder den minimale cost i listen af noder.
    VISITED.append(queue[chosen_index].STATE[0])  # tilføjer den valgte til den besøgte liste
    return queue.pop(chosen_index)  # returnere og fjerner den valgte node fra fringe


# '''


'''
Successor function, mapping the nodes to its successors
'''


def successor_fn(state):  # Lookup list of successor states
    return STATE_SPACE[state[0]]  # successor_fn( 'C' ) returns ['F', 'G']


VISITED = []
COST = {('A', 'Dirty', 'Dirty'): 0}
INITIAL_STATE = (('A', 'Dirty', 'Dirty'), 0)
GOAL_STATE = [('A', 'Clean', 'Clean'), ('B', 'Clean', 'Clean')]
STATE_SPACE = {
    (('A', 'Dirty', 'Dirty')):
        [(('A', 'Clean', 'Dirty'), 1), (('B', 'Dirty', 'Dirty'), 2)],
    (('B', 'Dirty', 'Dirty')):
        [(('B', 'Dirty', 'Clean'), 1), (('A', 'Dirty', 'Dirty'), 2)],

    (('B', 'Dirty', 'Clean')):
        [(('B', 'Dirty', 'Clean'), 2), (('A', 'Dirty', 'Clean'), 1)],
    (('A', 'Dirty', 'Clean')):
        [(('A', 'Clean', 'Clean'), 1), (('B', 'Dirty', 'Clean'), 2)],
    (('A', 'Clean', 'Clean')):
        [(('A', 'Clean', 'Clean'), 3), (('B', 'Clean', 'Clean'), 3)],

    (('A', 'Clean', 'Dirty')):
        [(('A', 'Clean', 'Dirty'), 2), (('B', 'Clean', 'Dirty'), 1)],
    (('B', 'Clean', 'Dirty')):
        [(('B', 'Clean', 'Clean'), 1), (('A', 'Clean', 'Dirty'), 2)],
    (('B', 'Clean', 'Clean')):
        [(('B', 'Clean', 'Clean'), 3), (('A', 'Clean', 'Clean'), 3)],
}

'''
STATE_SPACE = {
    (('A', 'Dirty', 'Dirty')):
        [(('A', 'Dirty', 'Dirty'), 3), (('A', 'Clean', 'Dirty'), 1), (('B', 'Dirty', 'Dirty'), 2)],
    (('B', 'Dirty', 'Dirty')):
        [(('B', 'Dirty', 'Dirty'), 3), (('B', 'Dirty', 'Clean'), 1), (('A', 'Dirty', 'Dirty'), 2)],

    (('B', 'Dirty', 'Clean')):
        [(('B', 'Dirty', 'Clean'), 3), (('B', 'Dirty', 'Clean'), 2), (('A', 'Dirty', 'Clean'), 1)],
    (('A', 'Dirty', 'Clean')):
        [(('A', 'Dirty', 'Clean'), 3), (('A', 'Clean', 'Clean'), 1), (('B', 'Dirty', 'Clean'), 2)],
    (('A', 'Clean', 'Clean')):
        [(('A', 'Clean', 'Clean'), 1), (('A', 'Clean', 'Clean'), 3), (('B', 'Clean', 'Clean'), 3)],

    (('A', 'Clean', 'Dirty')):
        [(('A', 'Clean', 'Dirty'), 3), (('A', 'Clean', 'Dirty'), 2), (('B', 'Clean', 'Dirty'), 1)],
    (('B', 'Clean', 'Dirty')):
        [(('B', 'Clean', 'Dirty'), 3), (('B', 'Clean', 'Clean'), 1), (('A', 'Clean', 'Dirty'), 2)],
    (('B', 'Clean', 'Clean')):
        [(('B', 'Clean', 'Clean'), 1), (('B', 'Clean', 'Clean'), 3), (('A', 'Clean', 'Clean'), 3)],
}
'''
HEURISTICS = {('A', 'Dirty', 'Dirty'): 3,
              ('B', 'Dirty', 'Dirty'): 3,
              ('B', 'Dirty', 'Clean'): 2,
              ('A', 'Dirty', 'Clean'): 1,
              ('A', 'Clean', 'Dirty'): 2,
              ('B', 'Clean', 'Dirty'): 1,
              ('A', 'Clean', 'Clean'): 0,
              ('B', 'Clean', 'Clean'): 0, }

'''
Run tree search and display the nodes in the path to goal node
'''


def run():
    path = TREE_SEARCH()
    print('Solution path:')
    for node in path:
        node.display()
    for costKey, costValue in COST.items():
        print(costKey, costValue)


if __name__ == '__main__':
    run()
