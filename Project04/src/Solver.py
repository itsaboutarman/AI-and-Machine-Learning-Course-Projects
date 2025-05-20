from collections import deque
from typing import Callable, List, Tuple
from CSP import CSP


class Solver(object):

    def __init__(self, csp: CSP, domain_heuristics: bool = False, variable_heuristics: bool = False,
                 AC_3: bool = False) -> None:
        self.domain_heuristic = domain_heuristics
        self.variable_heuristic = variable_heuristics
        self.AC_3 = AC_3
        self.csp = csp

    def backtrack_solver(self) -> List[Tuple[str, str]]:
        removed = self.apply_AC3() if self.AC_3 else []

        if self.csp.is_complete():
            return list(self.csp.assignments.items())

        variable = self.select_unassigned_variable()
        # print(variable, len(self.csp.var_constraints[variable]))
        for value in self.ordered_domain_value(variable):
            if self.csp.is_consistent(variable, value):

                self.csp.assign(variable, value)

                removed.extend(self.csp.changing_domains(variable))

                result = self.backtrack_solver()
                if result is not None:
                    return result
                self.csp.unassign(removed, variable)
                removed = []

        return None

    def select_unassigned_variable(self) -> str:
        if self.variable_heuristic:
            return self.MRV()
        return self.csp.unassigned_var[0]

    def ordered_domain_value(self, variable: str) -> List[str]:
        # Function implementation goes here
        if self.domain_heuristic:
            return self.LCV(variable)
        return self.csp.variables[variable]

    def arc_reduce(self, x, y, consistent) -> List[str]:
        removed_values = []

        for x_value in self.csp.variables[x]:
            if all(not consistent(x_value, y_value) for y_value in self.csp.variables[y]):
                self.csp.variables[x].remove(x_value)
                removed_values.append(x_value)
                if len(self.csp.variables[x]) == 0:
                    return removed_values
        return removed_values

    def apply_AC3(self) -> List[Tuple[str, str]]:
        removed_values = []
        queue = deque(self.csp.constraints)

        while queue:
            constraint, variables = queue.popleft()
            x, y = variables[0], variables[1]

            # Ensure x and y are valid variables (not lists or tuples)
            if not isinstance(x, str) or not isinstance(y, str):
                continue

            removed = self.arc_reduce(x, y, constraint)
            for removed_value in removed:
                removed_values.append((x, removed_value))
            if len(self.csp.variables[x]) == 0:
                return removed_values  # Domain wiped out for x, no solution possible

        return removed_values

    def MRV(self) -> str:
        min_var = None
        min_domain_size = float('inf')
        for var in self.csp.unassigned_var:
            if len(self.csp.variables[var]) < min_domain_size:
                min_domain_size = len(self.csp.variables[var])
                min_var = var
        return min_var

    def LCV(self, variable: str) -> List[str]:

        def count_constraints(value):
            count = 0
            if variable in self.csp.var_constraints:
                for _, related_vars in self.csp.var_constraints[variable]:
                    neighbor = related_vars[1]
                    if neighbor and not self.csp.is_assigned(neighbor) and value in self.csp.variables[neighbor]:
                        count += 1
            return count

        return sorted(self.csp.variables[variable], key=count_constraints)
