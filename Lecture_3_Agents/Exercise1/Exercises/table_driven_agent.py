A = 'A'
B = 'B'

percepts = []

table = {
    ((A, 'Clean'),): 'Right',
    ((A, 'Dirty'),): 'Suck',
    ((B, 'Clean'),): 'Left',
    ((B, 'Dirty'),): 'Suck',
    ((A, 'Clean'), (A, 'Clean')): 'Right',
    ((A, 'Clean'), (A, 'Dirty')): 'Suck',
    # ...
    ((A, 'Clean'), (A, 'Clean'), (A, 'Clean')): 'Right',
    ((A, 'Clean'), (A, 'Clean'), (A, 'Dirty')): 'Suck',
    ((A, 'Clean'), (A, 'Dirty'), (B, 'Clean')): 'Left',
    # ...
    ((A, 'Clean'), (A, 'Dirty'), (B, 'Clean'), (B, 'Dirty')): 'Suck',
    ((A, 'Clean'), (A, 'Dirty'), (B, 'Clean'), (B, 'Clean')): 'Left',
    ((A, 'Clean'), (A, 'Dirty'), (B, 'Clean'), (B, 'Clean')): 'Left',

}


def LOOKUP(percepts, table):  # Lookup appropriate action for percepts
    action = table.get(tuple(percepts))
    return action


def TABLE_DRIVEN_AGENT(percept):  # Determine action based on table and percepts
    percepts.append(percept)  # add percept
    action = LOOKUP(percepts, table)  # Lookup appropriate action for percepts
    return action


def run():  # run agent on several sequential percepts
    print('Action\tPercepts')
    print(TABLE_DRIVEN_AGENT((A, 'Clean')), '\t', percepts)
    print(TABLE_DRIVEN_AGENT((A, 'Dirty')), '\t', percepts)
    print(TABLE_DRIVEN_AGENT((B, 'Clean')), '\t', percepts)
    print(TABLE_DRIVEN_AGENT((B, 'Clean')), '\t', percepts)


if __name__ == '__main__':
    run()
