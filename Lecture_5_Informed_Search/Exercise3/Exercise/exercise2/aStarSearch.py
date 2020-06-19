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
        if entry.STATE[0] in [closed_item[0] for closed_item in
                              VISITED]:  # hvis noden har været besøgt, ignorer og fortsæt
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
        # udregner hvad noden koster, med rute og heuristic.
        fn_node = COST[entry.STATE[0]] + HEURISTICS[entry.STATE[0]]
        fn.append(fn_node)
    # finder den minimale cost i listen af noder.
    chosen_index = fn.index(min(fn))
    # tilføjer den valgte til den besøgte liste
    VISITED.append(queue[chosen_index].STATE)
    # returnere og fjerner den valgte node fra fringe
    return queue.pop(chosen_index)


# '''


'''
Successor function, mapping the nodes to its successors
'''


def successor_fn(state):  # Lookup list of successor states
    return STATE_SPACE[state[0]]  # successor_fn( 'C' ) returns ['F', 'G']


VISITED = []
COST = {'A': 0}
INITIAL_STATE = ('A', 6)
GOAL_STATE = [('K'), ('L')]
STATE_SPACE = {('A'): [('B', 1), ('C', 2), ('D', 4)],
               ('B'): [('F', 5), ('E', 4)],
               ('C'): [('E', 1)],
               ('D'): [('H', 1), ('I', 4), ('J', 2)],
               ('E'): [('G', 2), ('H', 3)],
               ('F'): [('G', 1)],
               ('G'): [('K', 6)],
               ('H'): [('K', 6), ('L', 5)],
               ('I'): [('L', 3)],
               ('J'): [],
               ('K'): [],
               ('L'): [], }

HEURISTICS = {'A': 6,
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
