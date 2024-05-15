def parse_pddl_init_section(pddl_file_path):
    # This function reads a PDDL file and extracts the initial state predicates.
    all_init = set()
    in_init_section = False

    try:
        with open(pddl_file_path, 'r') as file:
            for line in file:
                stripped_line = line.strip()
                
                # Check if the init section begins
                if stripped_line.startswith('(:init'):
                    in_init_section = True
                    stripped_line = stripped_line.replace("(:init", "").strip()
                
                # If in the init section, add predicates to the set
                if in_init_section:
                    # Check if the init section ends
                    if stripped_line.endswith('))'):
                        in_init_section = False
                        stripped_line = stripped_line[:-1]
                    # Remove comments if any
                    cleaned_line = stripped_line.split(';')[0].strip()
                    if cleaned_line:  # Ensure it's not an empty line
                        fact_lists = stripped_line.strip()[1:-1].split(') (')
                        for fact in fact_lists:
                            all_init.add('(' + fact + ')')

    except FileNotFoundError:
        print("The specified file was not found.")

    return all_init

# Example usage
if __name__ == "__main__":
    pddl_file_path = 'benchmarks/mcmp/tasks_exbw/exbw_p01-n2-N5-s1.pddl'  # Replace this with the actual file path
    initial_state_predicates = parse_pddl_init_section(pddl_file_path)
    print(initial_state_predicates)
    print(len(initial_state_predicates))