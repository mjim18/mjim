import csv

class NTM:
    def __init__(self, tm_file):
        self.transitions = {}
        self.start_state = None
        self.accept_state = None
        self.reject_state = None
        self.name = None
        self.parse_tm_file(tm_file)

    def parse_tm_file(self, file_path):
        """Parse the file describing the Turing Machine."""
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            self.name = next(reader)[0].strip()
            _ = next(reader)  # States 
            _ = next(reader)  # Input alphabet 
            _ = next(reader)  # Tape alphabet 
            self.start_state = next(reader)[0].strip()
            self.accept_state = next(reader)[0].strip()
            self.reject_state = next(reader)[0].strip()

            for row in reader:
                current_state, symbol, next_state, write_symbol, move = [item.strip() for item in row]
                key = (current_state, symbol)
                if key not in self.transitions:
                    self.transitions[key] = []
                self.transitions[key].append((next_state, write_symbol, move))

    def simulate(self, input_string, max_steps=None):
        """Simulate the Non-Deterministic Turing Machine on the input string."""
        initial_config = ["", self.start_state, input_string, None]
        tree = [[initial_config]]  # List representing the configuration levels (each level is a list of configurations)
        step_count = 0
        total_transitions = 0
        total_non_leaves = 0

        print(f"Machine Name: {self.name}")
        print(f"Initial String: {input_string}")

        while tree:
            current_level = tree.pop(0)  # Get the first level of the tree
            next_level = []

            for config in current_level:
                left, state, right, parent = config

                # Check if the current state is an accept state
                if state == self.accept_state:
                    print(f"String accepted in {step_count} steps")
                    self.print_accept_path(config)
                    avg_nondeterminism = total_transitions / total_non_leaves if total_non_leaves > 0 else 0
                    print(f"Average nondeterminism: {avg_nondeterminism:.2f}")
                    return

                # Check if the current state is a reject state
                if state == self.reject_state:
                    continue

                # Process transitions for the current configuration
                current_symbol = right[0] if right else "_"
                key = (state, current_symbol)

                if key in self.transitions:
                    for next_state, write_symbol, move in self.transitions[key]:
                        total_transitions += 1
                        new_left = left
                        new_right = right[1:] if len(right) > 1 else ""

                        if move == "L":
                            new_left = left[:-1] if left else ""
                            new_right = (left[-1] if left else "") + write_symbol + new_right
                        elif move == "R":
                            new_left += write_symbol

                        next_level.append([new_left, next_state, new_right, config])

            if next_level:
                total_non_leaves += len(current_level)
                tree.append(next_level)  # Add the next level to the tree for further processing

            # If no more transitions are possible, reject the string
            if not next_level:
                print(f"String rejected in {step_count} steps")
                avg_nondeterminism = total_transitions / total_non_leaves if total_non_leaves > 0 else 0
                print(f"Average nondeterminism: {avg_nondeterminism:.2f}")
                return

            step_count += 1

            # Check if we have reached the step limit
            if max_steps and step_count >= max_steps:
                print(f"Execution stopped after {max_steps} steps")
                avg_nondeterminism = total_transitions / total_non_leaves if total_non_leaves > 0 else 0
                print(f"Average nondeterminism: {avg_nondeterminism:.2f}")
                return

    def print_accept_path(self, config):
        """Trace and print the accepting path."""
        path = []
        while config:
            path.append(config)
            config = config[3]  # Parent configuration
        path.reverse()
        depth = len(path) - 1
        for step in path:
            left, state, right, _ = step
            head_char = right[0] if right else "_"
            print(f"{left} {state} {head_char}{right[1:]}")

        print(f"Depth of tree: {depth}")

# Example usage
tm = NTM("equal_01s.csv")
tm.simulate("10101", max_steps=1000)
