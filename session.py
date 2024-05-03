from queue import PriorityQueue, Queue

# Define the goal state
GOAL_STATE = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 0]]


class PuzzleState:
    def __init__(self, board, parent=None, move=""):
        self.board = board
        self.parent = parent
        self.move = move

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))

    def __lt__(self, other):
        return True

    def __gt__(self, other):
        return True

    def __le__(self, other):
        return True

    def __ge__(self, other):
        return True

    def __str__(self):
        return '\n'.join([' '.join([str(cell) for cell in row]) for row in self.board])

    def get_blank_position(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    return i, j

    def is_goal(self):
        return self.board == GOAL_STATE

    def get_children(self):
        children = []
        x, y = self.get_blank_position()
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in moves:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < 3 and 0 <= new_y < 3:
                new_board = [row[:] for row in self.board]
                new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]
                children.append(PuzzleState(new_board, parent=self, move=new_board[new_x][new_y]))
        return children


def depth_first_search(initial_state):
    visited = set()
    stack = [initial_state]
    enqueued_states = 0
    while stack:
        state = stack.pop()
        visited.add(state)
        enqueued_states += 1
        if state.is_goal():
            return state, enqueued_states
        children = state.get_children()
        for child in children:
            if child not in visited:
                stack.append(child)


def breadth_first_search(initial_state):
    visited = set()
    queue = Queue()
    queue.put(initial_state)
    enqueued_states = 0
    while not queue.empty():
        state = queue.get()
        visited.add(state)
        enqueued_states += 1
        if state.is_goal():
            return state, enqueued_states
        children = state.get_children()
        for child in children:
            if child not in visited:
                queue.put(child)


def best_first_search(initial_state, priority_function):
    visited = set()
    priority_queue = PriorityQueue()
    priority_queue.put((priority_function(initial_state), initial_state))
    enqueued_states = 0
    while not priority_queue.empty():
        state = priority_queue.get()[1]
        visited.add(state)
        enqueued_states += 1
        if state.is_goal():
            return state, enqueued_states
        children = state.get_children()
        for child in children:
            if child not in visited:
                priority_queue.put((priority_function(child), child))


def hamming_priority(state):
    # Number of tiles in the wrong position
    count = 0
    for i in range(3):
        for j in range(3):
            if state.board[i][j] != GOAL_STATE[i][j]:
                count += 1
    return count


def manhattan_priority(state):
    # Sum of the distances from the blocks to their goal positions
    distance = 0
    for i in range(3):
        for j in range(3):
            if state.board[i][j] != 0:
                x, y = divmod(state.board[i][j] - 1, 3)
                distance += abs(x - i) + abs(y - j)
    return distance


def get_solution_path(state):
    path = []
    while state:
        path.insert(0, state.move)
        state = state.parent
    return path


def print_solution(state, enqueued_states, algorithm_name):
    solution_path = get_solution_path(state)
    print(f"Algorithm: {algorithm_name}")
   # print("Solution:")
   # for i, move in enumerate(solution_path):
   #     print(f"Move {i + 1}: {move}")
    print(f"Number of states enqueued: {enqueued_states}")
    print(f"Number of moves: {len(solution_path) - 1}")


def main():
    initial_state = PuzzleState([[1, 8, 2],
                                 [0, 4, 3],
                                 [7, 6, 5]])
    algorithms = {
        "Depth-First Search": depth_first_search,
        "Breadth-First Search": breadth_first_search
    }
    for algorithm_name, algorithm in algorithms.items():
        solution_state, enqueued_states = algorithm(initial_state)
        print_solution(solution_state, enqueued_states, algorithm_name)
        print()

    # Best-first search with Hamming priority
    solution_state, enqueued_states = best_first_search(initial_state, hamming_priority)
    print_solution(solution_state, enqueued_states, "Best-First Search (Hamming Priority)")
    print()

    # Best-first search with Manhattan priority
    solution_state, enqueued_states = best_first_search(initial_state, manhattan_priority)
    print_solution(solution_state, enqueued_states, "Best-First Search (Manhattan Priority)")
    print()


if __name__ == "__main__":
    main()
