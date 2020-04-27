import random

from Lecture_6_Local_Search.Exercise4.Homework import queens_fitness

# import sys
# sys.path.insert(0, '/Lecture_6')


p_mutation = 4
num_of_generations = 30


def genetic_algorithm(population, fitness_fn, minimal_fitness):
    for generation in range(num_of_generations):
        print("Generation {}:".format(generation))
        print_population(population, fitness_fn)

        new_population = set()

        for i in range(len(population)):
            mother, father = random_selection(population, fitness_fn)
            child1, child2 = reproduce(mother, father)

            if random.uniform(1, 8) < p_mutation:
                child1 = mutate(child1)
                child2 = mutate(child2)

            new_population.add(child1)
            new_population.add(child2)

        # Add new population to population, use union to disregard
        # duplicate individuals
        population = population.union(new_population)

        fittest_individual = get_fittest_individual(population, fitness_fn)

        if minimal_fitness <= fitness_fn(fittest_individual):
            break

    print("Final generation {}:".format(generation))
    print_population(population, fitness_fn)

    return fittest_individual


def print_population(population, fitness_fn):
    for individual in population:
        fitness = fitness_fn(individual)
        print("{} - fitness: {}".format(individual, fitness))


def reproduce(mother, father):
    '''
    Reproduce two individuals with single-point crossover
    Return the child individual
    '''
    mother_list = list(mother)
    father_list = list(father)
    random_pointer = int(round(random.uniform(0, 7)))  # random pointer

    i = random_pointer

    while i < len(mother_list):
        mother_list[i], father_list[i] = father_list[i], mother_list[i]  # swap
        i += 1
    child1 = tuple(father_list)
    child2 = tuple(mother_list)
    children = []
    children.append(child1)
    children.append(child2)
    return children


def mutate(individual):
    '''
    Mutate an individual by randomly assigning one of its bits
    Return the mutated individual
    '''

    mutation = []
    numbers = list(range(1, 9))
    for number in individual:  # Remove duplicates
        if number not in mutation:  #
            mutation.append(number)  #

    for number in numbers:  # add the missing numbers
        if number not in mutation:  #
            mutation.append(number)  #
    random.shuffle(mutation)  # Shuffle

    return tuple(mutation)


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

    # https://en.wikipedia.org/wiki/Fitness_proportionate_selection
    fitness_of_each = {}
    sum_of_fitness = 0

    for member_of_population in ordered_population:
        fitness_of_each[member_of_population] = (fitness_fn(member_of_population))
        sum_of_fitness += fitness_of_each[member_of_population]
    percentage_of_each = {}
    parents = []

    for population, fitness in sorted(fitness_of_each.items(), key=lambda x: x[1],
                                      reverse=True):  # sort dict before loop, descending
        percentage_of_each[
            population] = fitness / sum_of_fitness * 100
    seen_population_list = []
    min_percent = 0
    max_percent = sum(percentage_of_each.values())

    while not len(parents) >= 2:
        if len(percentage_of_each) == 2:
            for population in percentage_of_each.keys():
                parents.append(population)
            return parents
        else:
            for population, percentage_of_population in percentage_of_each.items():
                pick_parents = random.uniform(min_percent, max_percent)
                if pick_parents >= percentage_of_population and not (len(parents) == 2) and population not in seen_population_list:
                    parents.append(population)
                    seen_population_list.append(population)
                    max_percent -= percentage_of_population

    return parents


def get_fittest_individual(iterable, func):
    return max(iterable, key=func)


def get_initial_population(n, count):
    '''
    Randomly generate count individuals of length n
    Note since its a set it disregards duplicate elements.
    '''
    return set([
        tuple(random.randint(1, 8) for _ in range(n))
        for _ in range(count)
    ])


def main():
    '''
    https://kushalvyas.github.io/gen_8Q.html
    The ideal case can yield upton 28 arrangements of non attacking pairs.
    Therefore max fitness = 28. if counting from 0 to 7, 36 if counting from 1 to 8
    '''
    minimal_fitness = 28

    # Curly brackets also creates a set, if there isn't a colon to indicate a dictionary
    initial_population = {
        (3, 1, 2, 6, 1, 7, 8, 5),
        (3, 1, 2, 6, 2, 7, 5, 8),
        (1, 2, 3, 4, 5, 6, 7, 8),
        (2, 7, 3, 6, 8, 5, 1, 4),

    }
    initial_population = get_initial_population(8, 4)

    fittest = genetic_algorithm(initial_population, queens_fitness.fitness_fn_positive, minimal_fitness)
    print('Fittest Individual: ' + str(fittest) + ' Fitness: ' + str(queens_fitness.fitness_fn_positive(fittest)))


if __name__ == '__main__':
    # pass
    main()
