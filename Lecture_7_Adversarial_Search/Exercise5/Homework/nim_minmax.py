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
    return state


def is_terminal(state):
    no_options = True
    for entry in state:
        if entry > 2:
            no_options = False
            break

    if no_options:
        return True

    utility = utility_of(state)
    if utility == 0 or utility == 1:
        return True
    else:
        return False


def utility_of(state):
    '''
   Checks who wins. if 0 min if 1 max
   the check works, because we are sorting the state space to have the biggest number first.
   If the first number in the state space is two, we cannot split the pile anymore.

   If the entry is 2 and modulo is 1, we are on a minimum level,
   minimum cannot divide the piles anymore, and max wins.
   '''
    for entry in state:
        if state[0] == 2 and len(state) % 2 == 1:
            return 1
        elif state[0] == 2 and len(state) % 2 == 0:
            return 0

    return -1


def successors_of(state):
    """
   The successor seems to create the correct tree
   """

    # Generate valid moves
    valid_moves = []
    for i in range(len(state)):
        if state[i] == 1 or state[i] == 2:
            continue
        count = 1
        while count < state[i] / 2:
            new_state = state.copy()
            new_state[i] = new_state[i] - count
            new_state.append(count)
            new_state.sort(reverse=True)
            valid_moves.append((count, new_state))
            count += 1

    print(valid_moves)

    return valid_moves


def display(state):
    print("-----")
    print(state)
    '''
   for c in [0, 3, 6]:
       print(state[c + 0], state[c + 1], state[c + 2])
   '''


def main():
    board = [15]
    # board = [20]
    while not is_terminal(board):
        board = computer_select_pile(board)
        if not is_terminal(board):
            display(board)
            board = user_select_pile(board)
    print("    Final state is {}".format(board))


def argmax(iterable, func):
    return max(iterable, key=func)


def computer_select_pile(state):
    new_state = minmax_decision(state)
    return new_state


def user_select_pile(list_of_piles):
    '''
    Given a list of piles, asks the user to select a pile and then a split.
    Then returns the new list of piles.
    '''
    print("\n    Current piles: {}".format(list_of_piles))

    i = -1
    while i < 0 or i >= len(list_of_piles) or list_of_piles[i] < 3:
        print("Which pile (from 1 to {}, must be > 2)?".format(len(list_of_piles)))
        i = -1 + int(input())

    print("Selected pile {}".format(list_of_piles[i]))

    max_split = list_of_piles[i] - 1

    j = 0
    while j < 1 or j > max_split or j == list_of_piles[i] - j:
        if list_of_piles[i] % 2 == 0:
            print(
                'How much is the first split (from 1 to {}, but not {})?'.format(
                    max_split,
                    list_of_piles[i] // 2
                )
            )
        else:
            print(
                'How much is the first split (from 1 to {})?'.format(max_split)
            )
        j = int(input())

    k = list_of_piles[i] - j

    new_list_of_piles = list_of_piles[:i] + [j, k] + list_of_piles[i + 1:]

    print("    New piles: {}".format(new_list_of_piles))

    return new_list_of_piles


if __name__ == '__main__':
    main()
