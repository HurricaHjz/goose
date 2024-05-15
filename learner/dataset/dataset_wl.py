import sys

sys.path.append("..")
import os
import random
import numpy as np
from tqdm import tqdm
from util.stats import get_stats
from representation import REPRESENTATIONS

# from deadend.deadend import deadend_states

_DOWNWARD = "./../planners/downward_cpu/fast-downward.py"
_POWERLIFTED = "./../planners/powerlifted/powerlifted.py"

ALL_KEY = "_all_"


def sample_from_dict(d, sample, seed):
    random.seed(seed)
    keys = random.sample(list(d), sample)
    values = [d[k] for k in keys]
    return dict(zip(keys, values))


def get_plan_info(domain_pddl, problem_pddl, plan_file, args):
    states = []
    actions = []

    planner = args.planner

    with open(plan_file, "r") as f:
        for line in f.readlines():
            if ";" in line:
                continue
            actions.append(line.replace("\n", ""))

    state_output_file = repr(hash(repr(args))).replace("-", "n")
    state_output_file += (
        repr(hash(domain_pddl))
        + repr(hash(problem_pddl))
        + repr(hash(plan_file))
    )
    aux_file = state_output_file + ".sas"
    state_output_file = state_output_file + ".states"

    cmd = {
        "pwl": f"export PLAN_PATH={plan_file} "
        + f"&& {_POWERLIFTED} -d {domain_pddl} -i {problem_pddl} -s perfect "
        + f"--plan-file {state_output_file}",
        "fd": f"export PLAN_INPUT_PATH={plan_file} "
        + f"&& export STATES_OUTPUT_PATH={state_output_file} "
        + f"&& {_DOWNWARD} --sas-file {aux_file} {domain_pddl} {problem_pddl} "
        + f"--search 'perfect([blind()])'",  # need filler h
    }[planner]

    # print("generating plan states with:") print(cmd)

    # disgusting method which hopefully makes running in parallel work fine
    assert not os.path.exists(aux_file), aux_file
    assert not os.path.exists(state_output_file), state_output_file
    output = os.popen(cmd).readlines()
    if output == None:
        print("make this variable seen")
    if os.path.exists(aux_file):
        os.remove(aux_file)

    if not os.path.exists(state_output_file):
        err_msg = f"Failed to generate states from training data plans. This may be because you did not build the planners yet. This can be done with\n\n\tsh build_components.sh\n"
        raise RuntimeError(err_msg)
    
    with open(state_output_file, "r") as f:
        for line in f.readlines():
            if ";" in line:
                continue
            line = line.replace("\n", "")
            s = set()
            for fact in line.split():
                if "(" not in fact:
                    lime = f"({fact})"
                else:
                    pred = fact[: fact.index("(")]
                    fact = fact.replace(pred + "(", "").replace(")", "")
                    args = fact.split(",")[:-1]
                    lime = "(" + " ".join([pred] + args) + ")"
                s.add(lime)
            states.append(sorted(list(s)))
    os.remove(state_output_file)

    schema_cnt = {ALL_KEY: len(actions)}
    for action in actions:
        schema = action.replace("(", "").split()[0]
        if schema not in schema_cnt:
            schema_cnt[schema] = 0
        schema_cnt[schema] += 1

    ret = []
    for i, state in enumerate(states):
        if i == len(actions):
            continue  # ignore the goal state, annoying for learning useful schema
        action = actions[i]
        schema = action.replace("(", "").split()[0]
        ret.append((state, schema_cnt.copy()))
        # print(state)
        # for s, v in schema_cnt.items():
        #     print(f"{s:>15} {v:>4}")
        # print()
        schema_cnt[schema] -= 1
        schema_cnt[ALL_KEY] -= 1
    # breakpoint()
    return ret


# def get_graphs_from_plans(args):
#     print("Generating graphs from plans...")
#     dataset = []  # can probably make a class for this

#     schema_keys = set()

#     representation = args.rep
#     domain_pddl = args.domain_pddl
#     tasks_dir = args.tasks_dir
#     plans_dir = args.plans_dir

#     for plan_file in tqdm(sorted(list(os.listdir(plans_dir)))):
#         problem_pddl = f"{tasks_dir}/{plan_file.replace('.plan', '.pddl')}"
#         assert os.path.exists(problem_pddl), problem_pddl
#         plan_file = f"{plans_dir}/{plan_file}"
#         rep = REPRESENTATIONS[representation](domain_pddl, problem_pddl)

#         plan = get_plan_info(domain_pddl, problem_pddl, plan_file, args)

#         for s, schema_cnt in plan:
#             s = rep.str_to_state(s)
#             graph = rep.state_to_cgraph(s)
#             dataset.append((graph, schema_cnt))
#             schema_keys = schema_keys.union(set(schema_cnt.keys()))

#     print("Graphs generated!")
#     return dataset, schema_keys

# def get_dataset_from_args(args):
#     """Returns list of graphs, and dictionaries where keys are given by h* and schema counts"""
#     dataset, schema_keys = get_graphs_from_plans(args)

#     graphs = []
#     ys = []

#     y_true = [] ## MODIFICATION: The randomly generated data for ALL train

#     for graph, schema_cnt in dataset:
#         graphs.append(graph)
#         test = 0 #NOTE: just to test whether schema_cnt with ALL_KEY stores the sum of all other vars
#         for k in schema_keys:
#             if k not in schema_cnt:
#                 schema_cnt[k] = 0  # probably should never happen?
#             test += schema_cnt[k] if k != ALL_KEY else 0
#         assert test == schema_cnt[ALL_KEY]

#         ## MODIFICATION: The randomly generated data for ALL train
#         random_p = np.random.rand()
#         y_true.append(random_p)
#         schema_cnt[ALL_KEY] = random_p
#         ys.append(schema_cnt)
#     print(f"saved test random probability y with length {len(y_true)} \n =true_y: {y_true[:7]}")
#     np.savez("test_prob_y.npz", array = np.array(y_true))
#     return graphs, ys


# MODIFICATION:
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
                        if len(fact_lists) == 1:
                            print("split in another form")
                            fact_lists = fact_lists[0].split(')(')
                        for fact in fact_lists:
                            all_init.add('(' + fact + ')')

    except FileNotFoundError:
        print("The specified file was not found.")

    return all_init

# Modified version that use txt for generate dataset, y_keys pairs
def get_graph_y(tasks_dir, plans_dir, representation, domain_pddl):
    dataset = [] 
    y_keys = set()
    for plan_file in tqdm(sorted(list(os.listdir(plans_dir)))):
        print(f'plan file name: {plan_file}')
        problem_pddl = f"{tasks_dir}/{plan_file.replace('.txt', '.pddl')}"
        assert os.path.exists(problem_pddl), problem_pddl
        plan_file = f"{plans_dir}/{plan_file}"
        rep = REPRESENTATIONS[representation](domain_pddl, problem_pddl) # get rep and plan_file name

        # get all init propositions
        all_init = parse_pddl_init_section(problem_pddl)
        static_facts = set()
        
        # out own policy (plan file) that has the format of [state] = x*
        with open(plan_file, 'r') as file:
            is_init = True # if needed to determine static facts
            for line in file:
                # Split the line at ']' to separate facts from the float value
                parts = line.split(') ] = ')
                if len(parts) < 2:
                    continue  # Skip lines that do not conform to the expected format
                
                # Clean and split the facts part to extract individual facts
                facts = parts[0][3:].strip().split(') (')  # Removes the leading '[' and splits the facts
                facts = ['(' + f + ')' for f in facts]  # Add back the closing parenthesis removed by split
                
                # Convert the list of facts to a set and back to a list to ensure uniqueness and ready for graph
                s = set(facts)

                # if is the first line (init), then compare to get the static predicates
                if is_init:
                    is_init = False
                    static_facts.update(all_init - s)
                    # print("update num, should only once")
                    # print(f's before: {s} with length {len(s)}')
                    # print(f'all init : {all_init} with length {len(all_init)}')
                    # print(f'static facts : {static_facts} with length {len(static_facts)}')

                s = s | static_facts
                s = sorted(list(s))
                # print(f's after: {s} with length {len(s)}')
                # return

                
                
                # Parse the float value to the y_dict
                value = float(parts[1].strip())
                y_dict = {ALL_KEY : value} # just to align with output format

                s = rep.str_to_state(s)
                graph = rep.state_to_cgraph(s)

                dataset.append((graph, y_dict))
                y_keys = y_keys.union(set(y_dict.keys()))
    return dataset, y_keys 
        
# Modified version that generate both train and test data
def get_graphs_from_plans(args, test:bool = False):
    print("Generating graphs from plans...")
    representation = args.rep
    domain_pddl = args.domain_pddl
    tasks_dir = args.tasks_dir
    plans_dir = args.plans_dir
    plans_tests_dir = args.plans_tests_dir

    dataset, y_keys = get_graph_y(tasks_dir, plans_dir, representation, domain_pddl)
    test_dataset, test_y_keys = get_graph_y(tasks_dir, plans_tests_dir, representation, domain_pddl)
    print("My Graphs generated!")
    return dataset, test_dataset,  y_keys, test_y_keys

# Modified version that collect final graph, y pairs
def get_dataset_from_args(args, test:bool = False):
    """Returns list of graphs, and dictionaries where keys are given by h* and schema counts"""
    dataset, test_dataset, _, _ = get_graphs_from_plans(args, test)

    graphs = []
    test_graphs = []
    ys = []
    test_ys = []

    y_true = [] ## MODIFICATION: The randomly generated data for ALL train

    for graph, y_dict in dataset:
        graphs.append(graph)
        ys.append(y_dict)
        y_true.append(y_dict[ALL_KEY])
    for graph, y_dict in test_dataset:
        test_graphs.append(graph)
        test_ys.append(y_dict)
    # print(f"saved test X* in y with length {len(y_true)} \ntrue_y: {y_true[:7]}")
    # np.savez("test_y.npz", array = np.array(y_true))
    return graphs, test_graphs, ys, test_ys

