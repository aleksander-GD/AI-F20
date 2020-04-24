class Node:  # Node has only PARENT_NODE, STATE, DEPTH
    def __init__(self, state, parent=None, depth=0):
        self.STATE = state
        self.PARENT_NODE = parent
        self.DEPTH = depth

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
        # node = REMOVE_FIRST(fringe) # lav en ny funktion som validere heuristics
        if node.STATE in GOAL_STATE:
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
    children = successor_fn(node.STATE)
    for child in children:
        s = Node(node)  # create node for each in state list
        s.STATE = child  # e.g. result = 'F' then 'G' from list ['F', 'G']
        s.PARENT_NODE = node
        s.DEPTH = node.DEPTH + 1
        successors = INSERT(s, successors)
    return successors


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
Removes and returns the best element from fringe based on heuristic value
'''


def REMOVE_BEST(queue):
    temp_key = None
    temp_value = None
    for entry in queue:
        if (temp_key == None and temp_value == None or temp_value > HEURISTICS.get(entry.STATE)):
            temp_key = entry
            temp_value = HEURISTICS.get(entry.STATE)
    return queue.pop(queue.index(temp_key))


'''
Successor function, mapping the nodes to its successors
'''


def successor_fn(state):  # Lookup list of successor states
    return STATE_SPACE[state]  # successor_fn( 'C' ) returns ['F', 'G']


INITIAL_STATE = ('A')
GOAL_STATE = [('K'), ('L')]
STATE_SPACE = {('A'): [('B'), ('C'), ('D')],
               ('B'): [('F'), ('E')],
               ('C'): [('E')],
               ('D'): [('I'), ('J'), ('H')],
               ('E'): [('G'), ('H')],
               ('F'): [('G')],
               ('G'): [('K')],
               ('H'): [('K'), ('L')],
               ('I'): [('L')],
               ('J'): [],
               'K': [],
               'L': [], }

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


if __name__ == '__main__':
    run()
