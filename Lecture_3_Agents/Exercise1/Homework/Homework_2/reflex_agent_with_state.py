import random

A = 'A'
B = 'B'
C = 'C'
D = 'D'

state = {}
action = None
model = {A: None, B: None, C: None, D: None}  # Initially ignorant

RULE_ACTION = {
    1: 'Suck',
    2: 'Right',
    3: 'Left',
    4: 'Down',
    5: 'Up',
    6: 'NoOp'
}

rules = {
    ## Works
    (A, 'Dirty'): 1,
    (B, 'Dirty'): 1,
    (C, 'Dirty'): 1,
    (D, 'Dirty'): 1,

    (A, 'Clean'): 2,
    (B, 'Clean'): 3,

    (A, 'Clean'): 4,
    (C, 'Clean'): 5,

    (C, 'Clean'): 2,
    (D, 'Clean'): 3,

    (B, 'Clean'): 4,
    (D, 'Clean'): 5,

    (B, 'Clean'): 3,
    (C, 'Clean'): 2,
    ## Works until here

    # (D, 'Clean'): 3,
    # (C, 'Clean'): 2,

    # (C, 'Clean'): 5,
    # (A, 'Clean'): 4,

    # (D, 'Clean'): 5,
    # (B, 'Clean'): 4,

    # (B, 'Clean'): 3,
    # (C, 'Clean'): 2,
    # Also works until here after reversing the rule order

    (A, B, C, D, 'Clean'): 6
}
# Ex. rule (if location == A && Dirty then 1)

random_place = ['A', 'B', 'C', 'B']

Environment = {
    A: 'Dirty',
    B: 'Dirty',
    C: 'Dirty',
    D: 'Dirty',
    'Current': random.choice(random_place)  # Works for any random starting point
}


def INTERPRET_INPUT(input):  # No interpretation
    return input


def RULE_MATCH(state, rules):  # Match rule for a given state
    rule = rules.get(tuple(state))
    return rule


def UPDATE_STATE(state, action, percept):
    (location, status) = percept
    state = percept
    if model[A] == model[B] == model[C] == model[D] == 'Clean':
        state = (A, B, C, D, 'Clean')
        # Model consulted only for A and B Clean
    model[location] = status  # Update the model state
    return state


def REFLEX_AGENT_WITH_STATE(percept):
    global state, action
    state = UPDATE_STATE(state, action, percept)
    rule = RULE_MATCH(state, rules)
    action = RULE_ACTION[rule]
    return action


def Sensors():  # Sense Environment
    location = Environment['Current']
    return (location, Environment[location])


def Actuators(action):  # Modify Environment
    location = Environment['Current']
    if action == 'Suck':
        Environment[location] = 'Clean'
    elif action == 'Right' and location == A:
        Environment['Current'] = B
    elif action == 'Left' and location == B:
        Environment['Current'] = A
    elif action == 'Down' and location == A:
        Environment['Current'] = C
    elif action == 'Right' and location == C:
        Environment['Current'] = D
    elif action == 'Up' and location == D:
        Environment['Current'] = B
    elif action == 'Down' and location == B:
        Environment['Current'] = D
    elif action == 'Left' and location == D:
        Environment['Current'] = C
    elif action == 'Up' and location == C:
        Environment['Current'] = A


def run(n):  # run the agent through n steps
    print('     Current            New')
    print('location    status   action   location    status')
    for i in range(1, n):
        (location, status) = Sensors()  # Sense Environment before action
        print("{:12s}{:8s}".format(location, status), end='')
        action = REFLEX_AGENT_WITH_STATE(Sensors())
        Actuators(action)
        (location, status) = Sensors()  # Sense Environment after action
        print("{:8s}{:12s}{:8s}".format(action, location, status))


if __name__ == '__main__':
    run(20)
