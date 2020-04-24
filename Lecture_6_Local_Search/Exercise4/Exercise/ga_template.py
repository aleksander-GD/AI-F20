import random
from Lecture_6.Exercise4.Exercise import random_selction_methods

p_mutation = 0.2
num_of_generations = 30


def genetic_algorithm(population, fitness_fn, minimal_fitness):
    for generation in range(num_of_generations):
        print("Generation {}:".format(generation))
        print_population(population, fitness_fn)

        new_population = set()

        for i in range(len(population)):
            mother, father = random_selection(population, fitness_fn)
            # mother, father = random_selction_methods.random_selection(population, fitness_fn)
            child = reproduce(mother, father)

            if random.uniform(0, 1) < p_mutation:
                child = mutate(child)

            new_population.add(child)

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
    random_pointer = int(round(random.uniform(0, 2)))  # random pointer

    i = random_pointer  # sæt i til random pointer, dvs lægden af tuplen er altid 3.
    # så kan det være man starter fra index 0, 1 eller 2 og så tager jeg og swapper de værdier fra det index.
    while i < len(mother_list):
        mother_list[i], father_list[i] = father_list[i], mother_list[i]  # swap
        i += 1  # det samme som for loop i++
    child1 = tuple(father_list)
    child2 = mother_list
    return child1
    # return random.choices(tuple(child1), tuple(child2))

    # return child


def mutate(individual):
    '''
    Mutate an individual by randomly assigning one of its bits
    Return the mutated individual
    '''
    mutation = [1 if random.random() > 0.3 else 0 for bit in
                individual]  # liste der indeholder bits baseret på en random ratio 0.3

    return tuple(mutation)  # returner muterede individ som tuple


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

    for member in ordered_population:
        fitness_of_each[member] = (fitness_fn(member))  # Lav dict hvor individ er key og fitness funktion er value
        sum_of_fitness += fitness_of_each[member]  # læg alle fitness værdier sammen.
    percentage_of_each = {}  # Ny dict med procenter, hvor individ stadig er key
    parents = []  # mor og far individer bliver tilføjet her, og returneret

    for key, value in sorted(fitness_of_each.items(), key=lambda x: x[1],
                             reverse=True):  # sortere dict inden loop, descending
        percentage_of_each[
            key] = value / sum_of_fitness * 100  # lav procenter som værdier og koble dem sammen med individ key
    seen = []  # For duplikerings purpose
    min_percent = 0
    max_percent = sum(percentage_of_each.values())

    while not len(parents) >= 2:  # så længe vi ikke har fundet 2 individer

        if len(percentage_of_each) == 2:  # Hvis længden er 2, tilføj dem til parents og returner listen
            for key in percentage_of_each.keys():  # de tre linjer tilføjer de to keys til parents, det kan sikkert gøres med list comprehension, men kan desværre ikke få det til at virke
                parents.append(key)
            return parents
        else:  # ellers for hver mulighed i dict, hvis random nummeret er mindre eller lig med værdien og længden ikk er 2 og at nøglen ikke er set i seen listen

            for key, value in percentage_of_each.items():
                pick_parents = random.uniform(min_percent, max_percent)  # Random number 0 - 100 (sum af procenter)
                if pick_parents >= value and not (len(parents) == 2) and key not in seen:
                    parents.append(key)
                    seen.append(key)  # for at undgå duplikerede nøgler
                    max_percent -= value


    return parents  # Når loopet rammer false så har den fundet 2 værdier


def fitness_function(individual):
    '''
    Computes the decimal value of the individual
    Return the fitness level of the individual

    Explanation:
    enumerate(list) returns a list of pairs (position, element):

    enumerate((4, 6, 2, 8)) -> [(0, 4), (1, 6), (2, 2), (3, 8)]

    enumerate(reversed((1, 1, 0))) -> [(0, 0), (1, 1), (2, 1)]
    '''
    liste = list(individual)

    fitness = int("".join(str(x) for x in liste), 2)

    return fitness


def get_fittest_individual(iterable, func):
    return max(iterable, key=func)


def get_initial_population(n, count):
    '''
    Randomly generate count individuals of length n
    Note since its a set it disregards duplicate elements.
    '''
    return set([
        tuple(random.randint(0, 1) for _ in range(n))
        for _ in range(count)
    ])


def main():
    minimal_fitness = 7

    # Curly brackets also creates a set, if there isn't a colon to indicate a dictionary
    initial_population = {
        (1, 1, 0),
        (0, 0, 0),
        (0, 1, 0),
        (1, 0, 0)
    }
    initial_population = get_initial_population(3, 4)

    fittest = genetic_algorithm(initial_population, fitness_function, minimal_fitness)
    print('Fittest Individual: ' + str(fittest) + ' Fitness: ' + str(fitness_function(fittest)))


if __name__ == '__main__':
    # pass
    main()
