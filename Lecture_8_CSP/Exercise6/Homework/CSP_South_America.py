from random import shuffle
import sys


class CSP:

    def __init__(self, variables, domains, neighbours, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbours = neighbours
        self.constraints = constraints

    def backtracking_search(self):
        return self.recursive_backtracking({})

    def recursive_backtracking(self, assignment):
        if self.is_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                results = self.recursive_backtracking(assignment)
                if results is not None:
                    return results
                assignment[var] = None
        return None

    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable

    def is_complete(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return False
        return True

    def order_domain_values(self, variable, assignment):
        all_values = self.domains[variable][:]
        # shuffle(all_values)
        return all_values

    def is_consistent(self, variable, value, assignment):
        if not assignment:
            return True

        for constraint in self.constraints.values():
            for neighbour in self.neighbours[variable]:
                if neighbour not in assignment:
                    continue

                neighbour_value = assignment[neighbour]
                if not constraint(variable, value, neighbour, neighbour_value):
                    return False
        return True


def create_australia_csp():
    wa, q, t, v, sa, nt, nsw = 'WA', 'Q', 'T', 'V', 'SA', 'NT', 'NSW'
    values = ['Red', 'Green', 'Blue']
    variables = [wa, q, t, v, sa, nt, nsw]
    domains = {
        wa: values[:],
        q: values[:],
        t: values[:],
        v: values[:],
        sa: values[:],
        nt: values[:],
        nsw: values[:],
    }
    neighbours = {
        wa: [sa, nt],
        q: [sa, nt, nsw],
        t: [],
        v: [sa, nsw],
        sa: [wa, nt, q, nsw, v],
        nt: [sa, wa, q],
        nsw: [sa, q, v],
    }

    def constraint_function(first_variable, first_value, second_variable, second_value):
        return first_value != second_value

    constraints = {
        wa: constraint_function,
        q: constraint_function,
        t: constraint_function,
        v: constraint_function,
        sa: constraint_function,
        nt: constraint_function,
        nsw: constraint_function,
    }

    return CSP(variables, domains, neighbours, constraints)


def create_south_america_csp():
    cri, pan, col, ven, guy, sur, guyfr, ecu, per, bol, pry, ury, bra, arg, chl = 'CRI', 'PAN', 'COL', 'VEN', 'GUY', 'SUR', 'GUYFR', 'ECU', 'PER', 'BOL', 'PRY', 'URY', 'BRA', 'ARG', 'CHL'
    values = ['Red', 'Green', 'Blue', 'Yellow']
    variables = [cri, pan, col, ven, guy, sur, guyfr, ecu, per, bol, pry, ury, bra, arg, chl]
    domains = {
        cri: values[:],
        pan: values[:],
        col: values[:],
        ven: values[:],
        guy: values[:],
        sur: values[:],
        guyfr: values[:],
        ecu: values[:],
        per: values[:],
        bol: values[:],
        pry: values[:],
        ury: values[:],
        bra: values[:],
        arg: values[:],
        chl: values[:],
    }
    neighbours = {
        # wa: [sa, nt],
        # t: [],
        cri: [pan],
        pan: [cri, col],
        col: [pan, ecu, per, ven, bra],
        ven: [col, guy, bra],
        guy: [ven, sur, bra],
        sur: [guy, guyfr, bra],
        guyfr: [sur, bra],
        ecu: [col, per],
        per: [ecu, col, bra, bol, chl],
        bol: [per, pry, arg, chl, bra],
        pry: [bol, arg, bra],
        ury: [arg, bra],
        arg: [chl, bol, pry, ury, bra],
        chl: [per, bol, arg],
        bra: [guyfr, sur, guy, ven, col, per, bol, pry, ury, arg],
    }

    def constraint_function(first_variable, first_value, second_variable, second_value):
        return first_value != second_value

    constraints = {
        cri: constraint_function,
        pan: constraint_function,
        col: constraint_function,
        ven: constraint_function,
        guy: constraint_function,
        sur: constraint_function,
        guyfr: constraint_function,
        ecu: constraint_function,
        per: constraint_function,
        bol: constraint_function,
        pry: constraint_function,
        ury: constraint_function,
        bra: constraint_function,
        arg: constraint_function,
        chl: constraint_function,
    }

    return CSP(variables, domains, neighbours, constraints)


if __name__ == '__main__':
    # sys.setrecursionlimit(100000)
    australia = create_australia_csp()
    result = australia.backtracking_search()
    print('\nCSP for australia: ')
    for area, color in sorted(result.items()):
        print("{}: {}".format(area, color))
    print('\nCSP for South America: ')
    south_america = create_south_america_csp()
    result = south_america.backtracking_search()
    for area, color in sorted(result.items()):
        print("{}: {}".format(area, color))

    # Check at https://mapchart.net/australia.html
