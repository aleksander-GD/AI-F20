def minmax_decision(state):
    def max_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = -infinity
        for e in successors_of(state):
            v = max(v, min_value(e))
        print('V: ' + str(v))
        return v

    def min_value(state):
        if is_terminal(state):
            return utility_of(state)
        v = infinity
        for e in successors_of(state):
            v = min(v, max_value(e))
        return v

    infinity = float('inf')
    action, state = argmax(successors_of(state), lambda a: min_value(a[1]))
    return action


def is_terminal(state):
    no_options = True
    for entry in state:
        if entry > 2 or state[1][len(state) - 1] > 2:  # hvis bunken er større end 2, kan man stadig dele bunken.
            no_options = False
            break

    if no_options:
        return True

    utility = utility_of(state)
    if utility == 1 or utility == 0:
        return True
    else:
        return False


def utility_of(state):
    for entry in state:
        if entry == 2 and len(state) % 2 == 1:
            return 1
        elif entry == 2 and len(state) % 2 == 0:
            return 0
    return -1

def successors_of(pile):
    total_pile = []
    pile_index = 0
    count = 0
    pile.sort()  # by sorting beforehand it makes it easy to clean up
    while pile_index < len(pile):
        single_pile = pile[pile_index]
        remainder = pile[:pile_index] + pile[pile_index + 1:]
        splitted_pile = single_split(single_pile)
        pile_index += 1
        for item in splitted_pile:
            for remains in remainder:
                item.append(remains)
            item.sort()
            total_pile.append((count, item))
            count += 1
    while pile in total_pile:
        total_pile.remove(pile)  # prevents duplicates of the pile in the new pile
    print(total_pile)
    return total_pile


def single_split(single_pile):
    # 6 returns [[1,3],[2,4]]
    # takes an int and returns possible states in list of lists form
    split_pile = []
    if single_pile < 3:
        split_pile.append([single_pile])
    else:
        first = 1
        last = single_pile - 1
        if single_pile % 2 == 0:
            mid = single_pile // 2
        else:
            mid = (single_pile // 2) + 1
        while first < mid:
            split_pile.append([first, last])
            first += 1
            last -= 1
    return split_pile


def display(state):
    print("-----")
    print(state)

    # for c in [0, 3, 6]:
    #    print(state[c + 0], state[c + 1], state[c + 2])


def main():
    starting_pile = [7]
    while not is_terminal(starting_pile):
        starting_pile[minmax_decision(starting_pile)]
        if not is_terminal(starting_pile):
            display(starting_pile)
            starting_pile[int(input('Your move? '))] = input("Enter your split number: " )
    display(starting_pile)


def argmax(iterable, func):
    return max(iterable, key=func)


if __name__ == '__main__':
    main()
