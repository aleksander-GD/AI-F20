import functools
import random
from pprint import pformat


def multiply_vector_elements(vector):
    """ return the multiplication of the vector elements """

    def mult(x, y):
        return x * y

    return functools.reduce(mult, vector, 1)


class Variable(object):
    """ Node in the network. Represent a random Variable """

    def __init__(self, name, assignments, probability_table, parents=[], children=[], marginal=[]):
        print("Name: ", name)
        print("Assignments: ", assignments)
        print("Probability table: ", probability_table)
        print("Parents", parents)
        print("Children: ", children)

        """ Node initialization
            params:
            name: name of this random variable.
            assignments: possible values this variable can have.
            probability_table: the casual probability table of this variable.
            parents: list of references to this Node`s parents.
            children: list of references to this Node`s children.
        """

        # the name of this random variable
        self.name = name

        # holds the possible assignments of this random variable
        # assume certain order
        self.assignments = {}
        for i in range(len(assignments)):
            self.assignments[assignments[i]] = i

        # holds the distribution table of this random variable
        for key, val in probability_table.items():
            if len(val) != len(assignments):
                self = None
                raise ValueError(
                    'data in probability table is inconsistent with possible assignments')
        self.probability_table = probability_table

        # list of dependent variables
        self.children = children

        # list of variables which this variable depends upon
        self.parents = parents

        # holds the marginal, pre-calculated probability to obtain each
        # possible value
        # self.marginal_probabilities = self.calculate_marginal_probability()
        self.marginal_probabilities = []
        self.marginal = []

        # indicates whether this node is ready to use
        # true when the marginal probabilities were calculated
        self.ready = False

    def get_name(self):
        """ return the name of this random variable """
        return self.name

    def get_assignments(self):
        """ return the possible values this variable can have """
        return self.assignments

    def get_assignment_index(self, assignment):
        """ returns the index of a given possible assignment within the assignments list """
        return self.assignments[assignment]

    def get_probability(self, value, parents_values):
        """ read from the distribution table and return the probability of having a
            certain value (value) given the values of the parents.
        """
        return self.probability_table[parents_values][self.assignments[value]]

    def get_conditional_probability(self, value, parents_values):
        """ read from the distribution table and return the probability of having a
            certain value (value) given the values of the parents.
            here the parents assignments can be partial
            parent_vals is a dictionary: { parent: value }
        """
        res = 0
        given_parents_index = []
        marginal_parents_index = []
        for i, v in enumerate(self.parents):
            if v.name in parents_values:
                given_parents_index.append((i, parents_values[v.name]))
            else:
                marginal_parents_index.append(i)

        # go over the rows in the distribution table
        for row_key, row_val in self.probability_table.items():
            valid_row = 1

            # check if this row should count for the marginal conditional
            # probability
            for gpi in given_parents_index:
                if row_key[gpi[0]] != gpi[1]:
                    valid_row = 0
                    break

            # if this row is valid, add the corresponding conditional
            # probability
            if valid_row:
                parents_probability = 1
                for mpi in marginal_parents_index:
                    parents_probability *= self.parents[mpi].get_marginal_probability(row_key[mpi])

                res += row_val[self.assignments[value]] * parents_probability
        return res

    def calculate_marginal_probability(self):
        """
        calculates and stores the marginal probabilities of this node.
        this function should be call before any other calculation is done.

        """
        # return, if already done
        if self.ready:
            return

        # COMPLETE THIS FUNCTION
        # Set self.marginal_probabilities
        sumRow = 0
        sumColumn = 0
        sumColumn2 = 0
        probability_tuple_list = []
        current_probability_distribution_table = {}
        marginal_of_node = {}
        probability_list = []
        for assignment, probability_values in self.probability_table.items():
            # print(assignment)
            # print(probability_value)
            if not self.parents:
                probability_list = list(probability_values)
                self.marginal_probabilities = probability_list
                self.marginal.append(probability_list)
                return

            if self.parents:
                probability_tuple_list.append(probability_values)
                # for row_entry in probability_values:
                append_dict = {assignment[0]: probability_values}
                current_probability_distribution_table.update(append_dict)
        for parent in self.get_parents():
            for margin in list(parent.marginal):
                probability_list.append(margin)

        row_one_column_one = 0
        row_one_column_two = 0
        row_two_column_two = 0
        row_two_column_one = 0
        row_value_one = 0
        row_value_two = 0
        for value in probability_list:
            row_value_one = value[0]
            row_value_two = value[1]
        for assignment, probability in current_probability_distribution_table.items():
            if assignment.lower() == 'false':
                row_one_column_one = probability[0]
                row_one_column_two = probability[1]
            if assignment.lower() == 'true':
                row_two_column_two = probability[1]
                row_two_column_one = probability[0]


        false_sum = row_one_column_one * row_value_one + (row_two_column_one * row_value_two)
        true_sum = row_one_column_two * row_value_one + (row_two_column_two * row_value_two)

        self.marginal_probabilities = [false_sum, true_sum]
        self.marginal.append([false_sum, true_sum])
        self.ready = True

    def get_marginal_probability(self, val):
        """ returns the marginal probability, to have a certain value """
        return self.marginal_probabilities[self.assignments[val]]

    def add_child(self, node):
        """ add dependent Variable to this variable """
        self.children.append(node)

    def add_parent(self, node):
        """ add a parent to this Variable """
        self.parents.append(node)

    def get_children(self):
        """ returns the children list """
        return self.children

    def is_child_of(self, node):
        """ return boolean, indicating whether this Node is a child of a given
            Node
        """
        for var in self.parents:
            if var.name == node.name:
                return 1
        return 0

    def get_parents(self):
        '''
        Return list of parents
        '''
        return self.parents


class BayesianNetwork(object):
    """ Bayesian Network implementation. This implementation incorporates few
        assumptions (see comments).
    """

    def __init__(self):
        """ Initialize connectivity matrix. """
        self.variables = []  # list of variables (Nodes)
        self.varsMap = {}  # a mapping of variable name to the actual node, for easy access
        self.ready = False  # indication of this net state

    def calculate_marginal_probabilities(self):
        """ pre-calculate and stores the marginal probabilities of all the nodes """

        # iterate over the Nodes, from parents to children
        for var in self.variables:
            var.calculate_marginal_probability()
        self.ready = True

    def get_variables(self):
        """ returns the variables """

        return self.variables

    def get_variable(self, varName):
        """ returns the variable with the given name """

        return self.varsMap[varName]

    def add_variable(self, var, index=-1):  # len(variables)):
        """ add a single Node to the net """

        if index < 0:
            self.variables.append(var)
        else:
            self.variables.insert(index, var)

        self.varsMap[var.name] = var
        self.ready = False  # we need to re-calculate marginals

    def set_variables(self, varList):
        """ quick assignment: set the given Node list to be the Nodes of this
            net
        """

        self.variables = varList
        for var in self.variables:
            self.varsMap[var.name] = var
        self.ready = False  # we need to re-calculate marginals

    def get_marginal_probability(self, var, val):
        """ returns the marginal probability of a given node """

        return var.get_marginal_probability(val)

    # values is dictionary
    def get_joint_probability(self, values):
        """ return the joint probability of the Nodes """

        value_dict = {}

        for value in values:  # Itererer variabel listen som gives med i metoden (values)
            if value in self.varsMap:  # checker om nuværende variabel er i variabel dikten "self.varsMap"
                variable = self.varsMap[value]  # Gemmer variablen i en variabel så den kan arbejdes med.
                name = variable.get_name()  # Får navnet på variablen.
                index = variable.get_assignment_index(
                    values[value])  # får indexet på variablens assignment (true (1) eller false (0))
                parents = variable.get_parents()  # får variablens forældre.
                if parents:  # variablen har parents
                    for parent in parents:
                        probability = variable.probability_table
                        parentName = parent.get_name()
                        parentIndex = parent.get_assignment_index(values[parentName])
                        key = list(probability)[parentIndex]
                        numbers = probability[key]
                        prob = numbers[index]
                        value_dict[name] = prob
                else:

                    probability = variable.probability_table
                    key = list(probability)[()]
                    numbers = probability[key]
                    prob = numbers[index]
                    value_dict[name] = prob

        result = 1
        for value in value_dict:
            result = result * value_dict[value]

        return result

    def get_conditional_probability(self, values, evidents):
        """ returns the conditional probability.
            Here I do not introduce advanced algorithms for inference (e.g. junctions trees)
            this method implement only simple inference, namely: the joint probability of children given their parents
            or the probability of parents given their children.
            assumption: variables in each level are independent, or independent given their parents
            (i.e vars in values are independent, as well as vars in evidents
        """
        res = 1

        # when we want probability of children given their parents
        # if self.varsMap[list(values.keys())[0]].is_child_of(self.varsMap[list(evidents.keys())[0]]):
        if all(self.varsMap[list(values.keys())[0]].is_child_of(self.varsMap[evident]) for evident in evidents.keys()):
            # print('probability of children given their parents')
            for child, c_val in values.items():
                res *= self.varsMap[child].get_conditional_probability(c_val, evidents)

        # when we want probability of parents given their children
        # make use of Bayes rule
        # assumption: nodes in each level are independent, given their parents
        else:
            print('probability of parents given their children')

            joint_marginal_parents = 1
            joint_marginal_children = 1
            joint_conditional_children = 1
            marginal_of_evidents = 1

            # calculating the joint probability of the parents
            for parent, p_val in values.items():
                joint_marginal_parents *= self.varsMap[parent].get_marginal_probability(p_val)

            # calculating the joint probability of the children, and the joint joint probability
            # of the children given their parents
            for child, c_val in evidents.items():
                joint_marginal_children *= self.varsMap[child].get_marginal_probability(c_val)

                # children given their parents. here the values become the
                # evidents!
                joint_conditional_children *= self.varsMap[child].get_conditional_probability(c_val, values)

                k = list(values.keys())[0]
                complementary_conditional_values = values.copy()
                complementary_conditional_values[k] = 'false' if values[k] == 'true' else 'true'
                marginal_of_evidents = marginal_of_evidents * self.varsMap[child].get_conditional_probability(c_val,
                                                                                                              complementary_conditional_values)

                # print("Child: {}".format(child))
                # print("    Given: {}".format(complementary_conditional_values))

            # uses Bayes rule, for calculating the conditional probability
            res = (joint_conditional_children * joint_marginal_parents) / (
                    (joint_conditional_children * joint_marginal_parents) + marginal_of_evidents * (
                    1 - joint_marginal_parents))

        return res

    # helper method
    def sub_vals(self, var, values):
        """ return a tuple, contain all the relevant
            assignments for the given variable (i.e - the assignments
            pertaining to the variable`s parents."""
        sub = []
        for p in var.parents:
            sub.append(values[p.name])
        return tuple(sub)


def create_random_sample(network):
    """ creates random sample for the given network.
        the distribution of the samples follows the joint probability function.
        assumes binary variables. """
    sample = {}
    for var in network.variables:

        samp = random.random()
        assignment1 = list(var.assignments.keys())[0]
        assignment2 = list(var.assignments.keys())[1]

        parents_values = network.sub_vals(var, sample)
        prob = var.get_probability(assignment1, parents_values)

        if samp <= prob:
            sample[var.name] = assignment1
        else:
            sample[var.name] = assignment2
    return sample


def pad(string, pad=4):
    lines = string.split('\n')
    padded_lines = (' ' * pad + line for line in lines)
    return '\n'.join(padded_lines)


def print_conditional_probability(network, conditionals_vars, conditionals_evidents):
    print('Given')
    print(pad(pformat(conditionals_evidents)))
    print('conditional probability of')
    print(pad(pformat(conditionals_vars)))
    print("is {:f}".format(
        network.get_conditional_probability(
            conditionals_vars,
            conditionals_evidents
        )))


def print_joint_probability(network, values):
    print('Joint probability of')
    print(pad(pformat(values)))
    print("is {:f}".format(network.get_joint_probability(values)))


def print_marginal_probabilities(network):
    print("Marginal probabilities:")
    for variable in network.get_variables():
        print("    {}".format(variable.get_name()))
        for assignment in variable.get_assignments():
            print("        {}: {:f}".format(
                assignment,
                variable.get_marginal_probability(assignment))
            )


def car():
    # the values kept as dictionary
    t1 = {(): (0.7, 0.3)}
    t2 = {(): (0.8, 0.2)}
    t3 = {(): (0.7, 0.3)}
    t4 = {('false',): (0.9, 0.1), ('true',): (0.3, 0.7)}
    t5 = {
        ('false', 'false'): (0.3, 0.7),
        ('true', 'false'): (0.4, 0.6),
        ('false', 'true'): (0.7, 0.3),
        ('true', 'true'): (0.95, 0.05)
    }
    t6 = {
        ('false', 'false', 'false'): (0.99, 0.01),
        ('false', 'false', 'true'): (0.9, 0.1),
        ('false', 'true', 'false'): (0.5, 0.5),
        ('false', 'true', 'true'): (0.4, 0.6),
        ('true', 'false', 'false'): (0.8, 0.2),
        ('true', 'false', 'true'): (0.7, 0.3),
        ('true', 'true', 'false'): (0.2, 0.8),
        ('true', 'true', 'true'): (0.1, 0.9)
    }
    '''
 

 '''

    damaged_tire = Variable('Damaged Tire (DT)', ('false', 'true'), t1, [])
    electronics_malfunctioning = Variable('Electronics Malfunctioning (EM)', ('false', 'true'), t3, [])
    fuel_tank_leaking = Variable('Fuel Tank Leaking (FTL)', ('false', 'true'), t2, [])
    vibrations = Variable('Vibrations (V)', ('false', 'true'), t4, [damaged_tire])
    slow_max_speed = Variable('Slow Max Speed (SMS)', ('false', 'true'), t5, [damaged_tire, electronics_malfunctioning])
    high_consumption = Variable('High Consumption (HC)', ('false', 'true'), t6,
                                [damaged_tire, electronics_malfunctioning, fuel_tank_leaking])

    variables = [damaged_tire, electronics_malfunctioning, fuel_tank_leaking, vibrations, slow_max_speed,
                 high_consumption]
    # creation of Network
    network = BayesianNetwork()
    network.set_variables(variables)

    # pre-calculate marginals
    network.calculate_marginal_probabilities()

    print_marginal_probabilities(network)

    print('')

    joint_values = {
        'Damaged Tire (DT)': 'true',
        'Electronics Malfunctioning (EM)': 'false',
        'Fuel Tank Leaking (FTL)': 'true',
        'Vibrations (V)': 'true',
        'Slow Max Speed (SMS)': 'true',
        'High Consumption (HC)': 'false'
    }
    print_joint_probability(network, joint_values)

    print('')

    conditionals_vars = {'Damaged Tire (DT)': 'true', 'Electronics Malfunctioning (EM)': 'false',
                         'Fuel Tank Leaking (FTL)': 'true'}  # ?
    conditionals_evidents = {'Vibrations (V)': 'true', 'Slow Max Speed (SMS)': 'true', 'High Consumption (HC)': 'false'}

    print_conditional_probability(network, conditionals_vars, conditionals_evidents)

    print('')

    sample = create_random_sample(network)
    print_joint_probability(network, sample)


car()
