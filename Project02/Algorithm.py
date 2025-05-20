from _helpers import Node, Stack, Queue, PriorityQueue
from  math import sqrt


class DFS_Algorithm:


    def __init__(self, start_pos, goal_pos, grid_dim):
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.grid_dim = grid_dim
        self.stack = Stack()
        self.stack.push(Node(pos=start_pos, parent=None))
        self.visited = []

    def get_successors(self, x, y):
        return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    def is_valid_cell(self, pos):
        return 0 <= pos[0] <= self.grid_dim[0] and 0 <= pos[1] <= self.grid_dim[1]

    def backtrack_solution(self, curr_node):
        return self._backtrack(curr_node)

    def _backtrack(self, curr_node):
        return [] if curr_node.parent is None else self._backtrack(curr_node.parent) + [curr_node.position()]

    def update(self, grid):
        curr_state = self.stack.pop()
        x, y = curr_state.position()
        done = False
        solution_path = []

        for step in self.get_successors(x, y):
            if self.is_valid_cell(step) and grid[step[0], step[1]] in [1, 3] and step not in self.visited:  # 1: empty cell has not explored yet, 3: goal cell

                self.visited.append(step)
                self.stack.push(Node(pos=step, parent=curr_state))

                if step == self.goal_pos:
                    done = True
                    solution_path = self.backtrack_solution(curr_state)
                    break

            grid[x, y] = 4  # visited

        return solution_path, done, grid

class BFS_Algorithm:
    def __init__(self, start_pos, goal_pos, grid_dim):
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.grid_dim = grid_dim
        self.queue = Queue()
        self.queue.push(Node(pos=start_pos, parent=None))
        self.visited = []

    def get_successors(self, x, y):
        return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    def is_valid_cell(self, pos):
        return 0 <= pos[0] <= self.grid_dim[0] and 0 <= pos[1] <= self.grid_dim[1]

    def backtrack_solution(self, curr_node):
        return self._backtrack(curr_node)

    def _backtrack(self, curr_node):
        return [] if curr_node.parent is None else self._backtrack(curr_node.parent) + [curr_node.position()]

    def update(self, grid):
        curr_state = self.queue.pop()
        x, y = curr_state.position()
        done = False
        solution_path = []

        for step in self.get_successors(x, y):
            if self.is_valid_cell(step) and grid[step[0], step[1]] in [1,3] and step not in self.visited:  # 1: empty cell has not explored yet, 3: goal cell

                self.visited.append(step)
                self.queue.push(Node(pos=step, parent=curr_state))

                if step == self.goal_pos:
                    done = True
                    solution_path = self.backtrack_solution(curr_state)
                    break

            grid[x, y] = 4  # visited

        return solution_path, done, grid


class IDS_Algorithm:

    def __init__(self, start_pos, goal_pos, grid_dim):
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.grid_dim = grid_dim
        self.stack = Stack()
        self.stack.push(Node(pos=start_pos, parent=None))
        self.depth = 1
        self.visited = []

    def get_successors(self, x, y):
        return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    def is_valid_cell(self, pos):
        return 0 <= pos[0] <= self.grid_dim[0] and 0 <= pos[1] <= self.grid_dim[1]

    def backtrack_solution(self, curr_node):
        return self._backtrack(curr_node)

    def _backtrack(self, curr_node):
        return [] if curr_node.parent is None else self._backtrack(curr_node.parent) + [curr_node.position()]

    def clearGrid(self, grid):
        for i in range(self.grid_dim[0]+1):
            for j in range(self.grid_dim[1]+1):
                if grid[i][j] == 4 :
                    grid[i][j] = 1
    def update(self, grid):
        curr_state = self.stack.pop()
        x, y = curr_state.position()
        done = False
        solution_path = []
        level = len(self.backtrack_solution(curr_state))
        for step in self.get_successors(x, y):
            if self.is_valid_cell(step) and grid[step[0], step[1]] in [1,3] and step not in self.visited :  # 1: empty cell has not explored yet, 3: goal cell
                if level<= self.depth :
                    self.visited.append(step)
                    self.stack.push(Node(pos=step, parent=curr_state))

                    if step == self.goal_pos:
                        done = True
                        solution_path = self.backtrack_solution(curr_state)
                        break

            grid[x, y] = 4  # visited

            if not done and self.stack.isEmpty():
                self.visited.clear()  #ids 27.307   #BFS 3.143   #a* 1.126
                self.clearGrid(grid)
                self.stack.push(Node(pos=self.start_pos, parent=None))
                self.depth += 1

        return solution_path, done, grid


class A_Star_Algorithm:
    def __init__(self, start_pos, goal_pos, grid_dim):
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.grid_dim = grid_dim
        self.open_set = PriorityQueue()
        self.open_set.push(Node(pos=start_pos, parent=None),priority=0)
        self.visited = []

    def get_successors(self, x, y):
        return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    def is_valid_cell(self, pos):
        return 0 <= pos[0] < self.grid_dim[0] and 0 <= pos[1] < self.grid_dim[1]

    def heuristic(self, pos):
        return abs(pos[0] - self.goal_pos[0]) + abs(pos[1] - self.goal_pos[1])

    def backtrack_solution(self, curr_node):
        return self._backtrack(curr_node)

    def _backtrack(self, curr_node):
        return [] if curr_node.parent is None else self._backtrack(curr_node.parent) + [curr_node.position()]

    def update(self, grid):
        curr_state = self.open_set.pop()
        x, y = curr_state.position()
        done = False
        solution_path = []

        for step in self.get_successors(x, y):
            if self.is_valid_cell(step) and grid[step[0], step[1]] in [1,3] and step not  in self.visited:  # 1: empty cell has not been explored yet, 3: goal cell
                self.visited.append(step)
                new_g = len(self.backtrack_solution(curr_state)) + 1
                new_h = self.heuristic(step)
                cost = new_h + new_g
                new_node = Node(pos=step, parent=curr_state)
                self.open_set.push(new_node, priority=cost)

                if step == self.goal_pos:
                    done = True
                    solution_path = self.backtrack_solution(curr_state)
                    break

            grid[x, y] = 4  # visited
        return solution_path, done, grid

class A_Star_Geometric_Algorithm:
    pass