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
        node = REMOVE_FIRST(fringe)
        if node.STATE == GOAL_STATE:
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


'''
Insert node in to the queue (fringe).
'''


def INSERT(node, queue):
    queue.insert(0, node)
    return queue


'''
Insert list of nodes into the fringe
'''


def INSERT_ALL(list, queue):
    for l in list:
        queue.append(l)
    return queue


'''
Removes and returns the first element from fringe
'''


def REMOVE_FIRST(queue):
    return queue.pop(0)


'''
Successor function, mapping the nodes to its successors
'''


def successor_fn(state):  # Lookup list of successor states
    if state not in ILLEGAL_STATE:
        return STATE_SPACE[state]
    return []  # successor_fn( 'C' ) returns ['F', 'G']


# INITIAL_STATE = 'A'
# GOAL_STATE = 'J'
# STATE_SPACE = {'A': ['B', 'C'],
#               'B': ['D', 'E'], 'C': ['F', 'G'],
#               'D': [], 'E': [], 'F': [], 'G': ['H', 'I', 'J'],
#               'H': [], 'I': [], 'J': [], }

# ('Farmer', 'Wolf', 'Goat', 'Cabbage')
'''
Take the goat over
Return
Take the wolf (cabbage) over
Return with the goat
Take the cabbage (wolf) over
Return
Take goat over
'''
ILLEGAL_STATE = (
    ('E', 'W', 'W', 'E'), ('E', 'E', 'W', 'W'), ('E', 'W', 'W', 'E'), ('W', 'W', 'E', 'E'), ('W', 'E', 'E', 'W'), ('E', 'W', 'W', 'W'))
INITIAL_STATE = ('W', 'W', 'W', 'W')
GOAL_STATE = ('E', 'E', 'E', 'E')
STATE_SPACE = {
    ('W', 'W', 'W', 'W'):
        [('W', 'W', 'W', 'W'), ('E', 'W', 'W', 'W'), ('E', 'E', 'W', 'W'), ('E', 'W', 'E', 'W'), ('E', 'W', 'W', 'E')],
    #('E', 'W', 'W', 'W'):  # Illegal state
    #    [('E', 'W', 'W', 'W')],
    #('E', 'E', 'W', 'W'):  # Illegal state
    #    [('E', 'E', 'W', 'W')],
    #('E', 'W', 'W', 'E'):  # Illegal state
     #   [('E', 'W', 'W', 'E')],

    ('E', 'W', 'E', 'W'):
        [('E', 'W', 'E', 'W'), ('W', 'W', 'E', 'W'), ('W', 'W', 'W', 'W')],
    ('W', 'W', 'E', 'W'):
        [('W', 'W', 'E', 'W'), ('E', 'W', 'E', 'W'), ('E', 'E', 'E', 'W'), ('E', 'W', 'E', 'E')],

    ('E', 'W', 'E', 'E'):
        [('E', 'W', 'E', 'E'), ('W', 'W', 'E', 'E'), ('W', 'W', 'W', 'E'), ('W', 'W', 'E', 'W')],
    #('W', 'W', 'E', 'E'):  # Illegal state
    #    [('W', 'W', 'E', 'E')],
    #('W', 'W', 'E', 'E'):
    #    [('W', 'W', 'E', 'E')],
    ('W', 'W', 'W', 'E'):
        [('W', 'W', 'W', 'E'), ('E', 'W', 'W', 'E'), ('E', 'E', 'W', 'E'), ('E', 'W', 'E', 'E')],
    #('E', 'W', 'W', 'E'):  # Illegal state
     #   [('E', 'W', 'W', 'E')],

    ('E', 'E', 'E', 'W'):
        [('E', 'E', 'E', 'W'), ('W', 'E', 'E', 'W'), ('W', 'W', 'E', 'W'), ('W', 'E', 'W', 'W')],
   #('W', 'E', 'E', 'W'):  # Illegal state
   #     [('W', 'E', 'E', 'W')],
    ('W', 'E', 'W', 'W'):
        [('W', 'E', 'W', 'W'), ('E', 'E', 'W', 'W'), ('E', 'E', 'E', 'W'), ('E', 'E', 'W', 'E')],
    #('E', 'E', 'W', 'W'):  # Illegal state
     #   [('E', 'E', 'W', 'W')],
    ('E', 'E', 'E', 'W'):
        [('E', 'E', 'E', 'W')],

    ('E', 'E', 'W', 'E'):
        [('E', 'E', 'W', 'E'), ('W', 'E', 'W', 'E'), ('W', 'W', 'W', 'E'), ('W', 'E', 'W', 'W')],
    ('W', 'E', 'W', 'W'):
        [('W', 'E', 'W', 'W')],

    ('W', 'E', 'W', 'E'):
        [('W', 'E', 'W', 'E'), ('E', 'E', 'W', 'E'), ('E', 'E', 'E', 'E')],
    ('E', 'E', 'E', 'E'):
        [('E', 'E', 'E', 'E')]
}

''' OUTPUT ''''''
(Route to find solution, to large to put in here)
......
Solution path:
State: ('E', 'E', 'E', 'E') - Depth: 7
State: ('W', 'E', 'W', 'E') - Depth: 6
State: ('E', 'E', 'W', 'E') - Depth: 5
State: ('W', 'W', 'W', 'E') - Depth: 4
State: ('E', 'W', 'E', 'E') - Depth: 3
State: ('W', 'W', 'E', 'W') - Depth: 2
State: ('E', 'W', 'E', 'W') - Depth: 1
State: ('W', 'W', 'W', 'W') - Depth: 0
'''

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
