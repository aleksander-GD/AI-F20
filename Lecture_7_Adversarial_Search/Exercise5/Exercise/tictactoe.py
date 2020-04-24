def minmax_decision(state):
    def max_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = -infinity
        for (a, s) in successors_of(state):
            v = max(v, min_value(s))
        print('V: ' + str(v))
        return v

    def min_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = infinity
        for (a, s) in successors_of(state):
            v = min(v, max_value(s))
        return v

    infinity = float('inf')
    action, state = argmax(successors_of(state), lambda a: min_value(a[1]))
    return action


def is_terminal(state):
    board_is_full = True  # starter med at sætte et fuldt bræt
    for i in range(len(state)):  # looper igennem længden af state og hvis det ikke er fyldt med X eller O er det ikke fyldt
        if state[i] != 'O' and state[i] != 'X':
            board_is_full = False
            break

    if board_is_full:  # returnerer hvis brættet er fyldt
        return True

    utility = utility_of(state)  # bruger resultatet af utility_of(state) til at se om der er vundet eller tabt, ellers returneres false.
    if utility == 1 or utility == -1:
        return True
    else:
        return False


def utility_of(state):
    """
    returns +1 if winner is X (MAX player), -1 if winner is O (MIN player), or 0 otherwise
    :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
    :return:
    """

    if state[0] == state[1] == state[2]:
        if state[0] == 'X':
            return 1
        else:
            return -1
    if state[0] == state[4] == state[8]:
        if state[0] == 'X':
            return 1
        else:
            return -1

    if state[0] == state[3] == state[6]:
        if state[0] == 'X':
            return 1
        else:
            return -1
    if state[3] == state[4] == state[5]:
        if state[3] == 'X':
            return 1
        else:
            return -1
    if state[6] == state[7] == state[8]:
        if state[6] == 'X':
            return 1
        else:
            return -1
    if state[2] == state[4] == state[6]:
        if state[2] == 'X':
            return 1
        else:
            return -1
    if state[1] == state[4] == state[7]:
        if state[1] == 'X':
            return 1
        else:
            return -1
    if state[2] == state[5] == state[8]:
        if state[2] == 'X':
            return 1
        else:
            return -1
    return 0


def successors_of(state):
    """
   returns a list of tuples (move, state) as shown in the exercise slides
   :param state: State of the checkerboard. Ex: [0; 1; 2; 3; X; 5; 6; 7; 8]
   :return:
   """

    # Figure out whos' turn it is. if count uneven, X turn.
    count = 0
    for entry in state:
        if entry == 'O' or entry == 'X': # Hvis den finder et O eller X så springer den pladsen over
            continue
        count += 1
    max_turn = False
    if count % 2 == 1:
        max_turn = True

    # Generate valid moves:
    valid_moves = []
    for i in range(len(state)):
        if state[i] == 'O' or state[i] == 'X':
            continue
        new_state = state.copy()
        new_state[i] = 'X' if max_turn else 'O'
        valid_moves.append((i, new_state))



    return valid_moves


def display(state):
    print("-----")
    for c in [0, 3, 6]:
        print(state[c + 0], state[c + 1], state[c + 2])


def main():
    board = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while not is_terminal(board):
        board[minmax_decision(board)] = 'X'
        if not is_terminal(board):
            display(board)
            board[int(input('Your move? '))] = 'O'
    display(board)


def argmax(iterable, func):
    return max(iterable, key=func)


if __name__ == '__main__':
    main()