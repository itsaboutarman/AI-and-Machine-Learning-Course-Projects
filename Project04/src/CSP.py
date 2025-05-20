from collections import deque
from typing import Callable, List, Tuple


class CSP(object):

    def __init__(self, *args, **kwargs) -> None:
        self.variables = {}
        self.constraints = []
        self.unassigned_var = []
        self.var_constraints = {}
        self.assignments = {}
        self.assignments_number = 0

    def add_constraint(self, constraint_func: Callable, variables: List[str]) -> None:
        variable = variables[0]
        if variable not in self.var_constraints:
            self.var_constraints[variable] = []
        exists = False
        for _, related_vars in self.var_constraints[variable]:
            if variables[1] == related_vars[1]:
                exists = True
        if not exists:
            self.var_constraints[variable].append((constraint_func, variables))
            self.constraints.append((constraint_func, variables))

    def add_variable(self, variable: str, domain: List) -> None:
        self.variables[variable] = domain
        self.unassigned_var.append(variable)

    def assign(self, variable: str, value) -> bool:
        self.assignments[variable] = value
        self.unassigned_var.remove(variable)
        self.assignments_number += 1
        return self.is_consistent(variable, value)

    def is_consistent(self, variable: str, value) -> bool:
        if variable not in self.var_constraints:
            return True  # No constraints on this variable

        for constraint_func, related_vars in self.var_constraints[variable]:
            related_value = self.assignments[related_vars[1]] if related_vars[1] in self.assignments else None

            if not constraint_func(value, related_value):
                # self.variables[variable].remove(value)
                return False  # Constraint violated

        return True  # All constraints satisfied

    def is_complete(self) -> bool:
        return len(self.unassigned_var) == 0

    def is_assigned(self, variable: str) -> bool:
        return variable not in self.unassigned_var

    def unassign(self, removed_values_from_domain: List[Tuple[str, any]], variable: str) -> None:
        if variable in self.assignments:
            self.restore_domains(removed_values_from_domain)
            del self.assignments[variable]
            self.unassigned_var.append(variable)

    def changing_domains(self, variable):
        removed_values = []
        value = self.assignments.get(variable)
        for val in self.variables[variable]:
            if val != value:
                removed_values.append((variable, val))
        self.variables[variable] = [value]
        for _, related_vars in self.var_constraints[variable]:
            neighbor = related_vars[1]
            if neighbor and neighbor not in self.assignments and value in self.variables[neighbor]:
                self.variables[neighbor].remove(value)
                removed_values.append((neighbor, value))

        return removed_values

    def restore_domains(self, removed_values):
        for variable, value in removed_values:
            self.variables[variable].append(value)
