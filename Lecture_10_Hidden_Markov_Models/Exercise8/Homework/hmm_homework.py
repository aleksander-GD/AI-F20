import numpy as np

"""
Hidden Markov Model using Viterbi algorithm to find most
likely sequence of hidden states.

The problem is to find out the most likely sequence of states
of the weather (hot, cold) from a describtion of the number
of ice cream eaten by a boy in the summer.
"""


def main():
    np.set_printoptions(suppress=True)

    states = np.array(["initial", "hot", "cold", "final"])

    # To simulate starting from index 1, we add a dummy value at index 0
    observationss = [
        [None, 3, 1, 3],
        [None, 3, 3, 1, 1, 2, 2, 3, 1, 3],
        [None, 3, 3, 1, 1, 2, 3, 3, 1, 2],
    ]

    # Markov transition matrix
    # transitions[start, end]
    transitions = np.array([[.0, .8, .2, .0],  # Initial state
                            [.0, .6, .3, .1],  # Hot state
                            [.0, .4, .5, .1],  # Cold state
                            [.0, .0, .0, .0],  # Final state
                            ])

    # P(v|q)
    # emission[state, observation]
    emissions = np.array([[.0, .0, .0, .0],  # Initial state
                          [.0, .2, .4, .4],  # Hot state
                          [.0, .5, .4, .1],  # Cold state
                          [.0, .0, .0, .0],  # Final state
                          ])

    for observations in observationss:
        print("Observations: {}".format(' '.join(map(str, observations[1:]))))

        probability = compute_forward(states, observations, transitions, emissions)
        print("Probability: {}".format(probability))

        path = compute_viterbi(states, observations, transitions, emissions)
        print("Path: {}".format(' '.join(path)))

        print('')


def inclusive_range(a, b):
    return range(a, b + 1)


def compute_forward(states, observations, transitions, emissions):
    n = len(states) - 2
    t = len(observations) - 1

    final_state = n + 1
    size_of_observations = t

    forward = 5 * np.ones((n + 2, t + 1))

    for state in inclusive_range(1, n):
        ob1 = observations[1]
        trans = transitions[0, state]
        emis = emissions[state, ob1]
        forward[state, 1] = trans * emis

    for time_step in inclusive_range(2, t):
        for state in inclusive_range(1, n):
            result = 0
            for s_prime in inclusive_range(1, n):
                result += forward[s_prime, time_step - 1] * transitions[s_prime, state] * emissions[
                    state, observations[time_step]]
            forward[state, time_step] = result

    computed_forward_probability = 0
    for inner_state in inclusive_range(1, n):
        computed_forward_probability += (
                    forward[inner_state, size_of_observations] * transitions[inner_state, final_state])

    return computed_forward_probability


def compute_viterbi(states, observations, transitions, emissions):
    n = len(states) - 2
    t = len(observations) - 1

    viterbi = 5 * np.ones((n + 2, t + 1))

    for state in inclusive_range(1, n):
        ob1 = observations[1]
        trans = transitions[0, state]
        emis = emissions[state, ob1]
        viterbi[state, 1] = trans * emis

    for time_step in inclusive_range(2, t):
        for state in inclusive_range(1, n):
            result = 0
            for s_prime in inclusive_range(1, n):
                result += viterbi[s_prime, time_step - 1] * transitions[s_prime, state] * emissions[
                    state, observations[time_step]]
            viterbi[state, time_step] = result

    path = []
    probability_list = []
    take_path_list = []
    for time_step in inclusive_range(1, t):
        probability = 0
        for_argmax = None
        maxi = 0
        for state in inclusive_range(1, n):
            for_argmax = viterbi[state, time_step]
            if time_step > 1:
                ob1 = observations[1]
                trans = transitions[0, state]
                emis = emissions[state, ob1]
                probability = trans * emis
                maxi += probability * for_argmax

            for_argmax = viterbi[state, time_step]
            take_path_list.append(state)
            probability_list.append(for_argmax)

            if len(probability_list) > 1 and len(take_path_list) > 1:
                max_value = argmax(probability_list)
                state_pos = take_path_list.pop(max_value)
                path.append(states[state_pos])
                probability_list.clear()
                take_path_list.clear()
    return path


def argmax(sequence):
    # Note: You could use np.argmax(sequence), but only if sequence is a list.
    # If it is a generator, first convert it: np.argmax(list(sequence))
    return max(enumerate(sequence), key=lambda x: x[1])[0]


if __name__ == '__main__':
    main()
