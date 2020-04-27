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
        ordered_fitness.append(fitness_fn(member))  # en liste af fitness værdier, i samme rækkefølge som populationen.
        sum_of_fitness += fitness_fn(member)  # læg alle fitness værdier sammen.

    i = 0
    for fitness in ordered_fitness:  # laver en liste med akkumlerede procent værdier.
        if (i != 0):
            ordered_fitness_percentage.append((fitness / sum_of_fitness * 100) + ordered_fitness_percentage[i - 1])
        else:
            ordered_fitness_percentage.append(fitness / sum_of_fitness * 100)
        i += 1

    seen = []  # For duplikerings purpose
    parents = []  # mor og far individer bliver tilføjet her, og returneret

    while not len(parents) >= 2:  # så længe vi ikke har fundet 2 individer

        pick_parents = random.uniform(min_percent, max_percent)  # Random number 0 - 100 (sum af procenter)
        if len(ordered_population) == 2:  # Hvis længden er 2, tilføj dem til parents og returner listen
            for member in ordered_population:
                parents.append(member)
            return parents
        else:  # gå igennem listen af procenter. Hvis random værdien er lavere end entry, tilføj individ til parents.
            for procent in ordered_fitness_percentage:
                if (pick_parents <= procent and ordered_population[
                    ordered_fitness_percentage.index(procent)] not in seen and ordered_fitness[
                    ordered_fitness_percentage.index(procent)] != 0):
                    parents.append(ordered_population[ordered_fitness_percentage.index(procent)])
                    seen.append(
                        ordered_population[ordered_fitness_percentage.index(procent)])  # for at undgå duplikerede nøgler
                    break

    print(parents)
    return parents  # Når loopet rammer false så har den fundet 2 værdier
