import random

A = 'A'
B = 'B'
C = 'C'
D = 'D'

## The grid of the vacuum world ##
##### #####
# A # # B #
##### #####

##### #####
# C # # D #
##### #####
random_place = ['A', 'B', 'C', 'B'] # Random place to start

Environment = {
    A: 'Dirty',
    B: 'Dirty',
    C: 'Dirty',
    D: 'Dirty',
    'Current': random.choice(random_place)  # Works for any random starting point
}


def REFLEX_VACUUM_AGENT(loc_st):  # Determine action
    if loc_st[1] == 'Dirty':
        return 'Suck'
    if loc_st[0] == A:
        actions = ['Right', 'Down']
        return random.choice(actions)  # It can choose between option 1 or 2, that is Randmized
    if loc_st[0] == B:
        actions = ['Left', 'Down']
        return random.choice(actions)
    if loc_st[0] == C:
        actions = ['Right', 'Up']
        return random.choice(actions)
    if loc_st[0] == D:
        actions = ['Left', 'Up']
        return random.choice(actions)


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


def run(n, make_agent):  # run the agent through n steps
    print('     Current            New')
    print('location    status  action  location    status')
    for i in range(1, n):
        (location, status) = Sensors()  # Sense Environment before action
        print("{:12s}{:8s}".format(location, status), end='')
        action = make_agent(Sensors())
        Actuators(action)
        (location, status) = Sensors()  # Sense Environment after action
        print("{:8s}{:12s}{:8s}".format(str(action), str(location), str(status)))


if __name__ == '__main__':
    run(20, REFLEX_VACUUM_AGENT)
