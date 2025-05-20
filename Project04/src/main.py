import argparse
from enum import Enum
from CSP import CSP
from Solver import Solver
from map_generator import generate_borders_by_continent
from graphics import draw
import random


class Continent(Enum):
    asia = "Asia"
    africa = "Africa"
    america = "America"
    europe = "Europe"

    def __str__(self):
        return self.value


def main():
    parser = argparse.ArgumentParser(
        prog="Map Coloring",
        description="Utilizing CSP to solve map coloring problem",
    )

    parser.add_argument(
        "-m",
        "--map",
        type=Continent,
        choices=list(Continent),
        help="Map must be: [Asia, Africa, America, Europe]",
    )
    parser.add_argument(
        "-lcv",
        "--lcv",
        action="store_true",
        help="Enable least constraint value (LCV) as a order-type optimizer"
    )
    parser.add_argument(
        "-mrv",
        "--mrv",
        action="store_true",
        help="Enable minimum remaining values (MRV) as a order-type optimizer"
    )
    parser.add_argument(
        "-ac3",
        "--arc-consistency",
        action="store_true",
        help="Enable arc consistency as a mechanism to eliminate the domain of variables achieving an optimized solution"
    )
    parser.add_argument(
        "-ND",
        "--Neighborhood-distance",
        type=int,
        default=1,
        help="The value determines the threshold for neighboring regions' similarity in color, with a default of 1 ensuring adjacent regions have distinct colors; increasing it, for instance to 2, extends this dissimilarity to the neighbors of neighbors."
    )

    args = parser.parse_args()
    continent_str = str(args.map)

    # Generate borders for the specified continent
    borders = generate_borders_by_continent(continent=continent_str)

    # Create a CSP instance
    csp = CSP()

    # Add variables (regions) and their domains
    for region in borders:
        if args.Neighborhood_distance == 1:
            csp.add_variable(region, ["Red", "Green", "Blue", "Yellow"])
        else:
            csp.add_variable(region,
                             ["Red", "Green", "Blue", "Yellow", "Pink", "Purple", "Brown", "Orange", "Violet",
                              "Olive", "Lightblue", "Teal", "Lime", "Maroon", "#AE1461", "#954334", "#1F2945"])

    for region, neighbors in borders.items():

        if not len(neighbors):
            csp.add_constraint(lambda x, y: x != y, [region, None])
            continue
        ND_neighbors = []
        for i in range(args.Neighborhood_distance):
            for neighbor in neighbors:
                if neighbor in csp.variables and neighbor != region:
                    csp.add_constraint(lambda x, y: x != y, [region, neighbor])
                if neighbor in borders:
                    for n in borders[neighbor]:
                        if n not in ND_neighbors:
                            ND_neighbors.append(n)
            neighbors = ND_neighbors.copy()

    # Initialize the Solver
    solver = Solver(csp, domain_heuristics=args.lcv, variable_heuristics=args.mrv, AC_3=args.arc_consistency)

    solver.backtrack_solver()

    result = csp.assignments  # your solution
    colors = []
    for region, val in result.items():
        if val not in colors:
            colors.append(val)
    print(f"{len(colors)} colors found")
    assignments_number = csp.assignments_number  # number of assignments that you can get it from
    # solver.csp.assignments_number

    draw(solution=result, continent=str(args.map), assignments_number=assignments_number)


if __name__ == '__main__':
    main()
