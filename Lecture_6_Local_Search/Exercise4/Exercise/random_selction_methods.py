import random

min_percent = 0
max_percent = 100


def random_selection(population, fitness_fn):
    """
  Compute fitness of each in population according to fitness_fn and add up
  the total. Then choose 2 from sequence based on percentage contribution to
  total fitness of population
  Return selected variable which holds two individuals that were chosen as
  the mother and the father
  """
    # Python sets are randomly ordered. Since we traverse the set twice, we
    # want to do it in the same order. So let's convert it temporarily to a
    # list.
    ordered_population = list(population)
    ordered_fitness = []
    ordered_fitness_percentage = []
    sum_of_fitness = 0
    fitness_of_each = {}

    for member in ordered_population:
        fitness_of_each[member] = (fitness_fn(member))

    for member in ordered_population:
        ordered_fitness.append(fitness_fn(member))
        sum_of_fitness += fitness_fn(member)

    i = 0
    for fitness in ordered_fitness:
        if (i != 0):
            ordered_fitness_percentage.append((fitness / sum_of_fitness * 100) + ordered_fitness_percentage[i - 1])
        else:
            ordered_fitness_percentage.append(fitness / sum_of_fitness * 100)
        i += 1

    seen = []
    parents = []

    while not len(parents) >= 2:

        pick_parents = random.uniform(min_percent, max_percent)
        if len(ordered_population) == 2:
            for member in ordered_population:
                parents.append(member)
            return parents
        else:
            for procent in ordered_fitness_percentage:
                if (pick_parents <= procent and ordered_population[
                    ordered_fitness_percentage.index(procent)] not in seen and ordered_fitness[
                    ordered_fitness_percentage.index(procent)] != 0):
                    parents.append(ordered_population[ordered_fitness_percentage.index(procent)])
                    seen.append(
                        ordered_population[ordered_fitness_percentage.index(procent)])
                    break

    print(parents)
    return parents
