import os
import random
from tqdm import tqdm
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
from sklearn.model_selection import train_test_split
from util.stats import get_stats
from representation import REPRESENTATIONS

_DOWNWARD = "./../planners/downward_cpu/fast-downward.py"
_POWERLIFTED = "./../planners/powerlifted/powerlifted.py"


def get_plan_info(domain_pddl, problem_pddl, plan_file, args):
    planner = args.planner

    states = []
    actions = []

    with open(plan_file, "r") as f:
        for line in f.readlines():
            if ";" in line:
                continue
            actions.append(line.replace("\n", ""))

    aux_garbage = repr(
        hash((domain_pddl, problem_pddl, plan_file, repr(args)))
    )
    aux_garbage = aux_garbage.replace("-", "n")
    state_output_file = aux_garbage + ".states"
    sas_file = aux_garbage + ".sas"

    cmd = {
        "pwl": f"export PLAN_PATH={plan_file} "
        + f"&& {_POWERLIFTED} -d {domain_pddl} -i {problem_pddl} -s perfect "
        + f"--plan-file {state_output_file}",
        "fd": f"export PLAN_INPUT_PATH={plan_file} "
        + f"&& export STATES_OUTPUT_PATH={state_output_file} "
        + f"&& {_DOWNWARD} --sas-file {sas_file} {domain_pddl} {problem_pddl} "
        + f"--search 'perfect([blind()])'",  # need filler h
    }[planner]
    output = os.popen(cmd).readlines()
    if output:
        pass  # this is so syntax highlighting sees `output`
    # os.system(cmd)

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
            states.append(s)
    if os.path.exists(sas_file):
        os.remove(sas_file)
    if os.path.exists(state_output_file):
        os.remove(state_output_file)

    schema_cnt = {}
    for action in actions:
        schema = action.replace("(", "").split()[0]
        if schema not in schema_cnt:
            schema_cnt[schema] = 0
        schema_cnt[schema] += 1

    ret = []
    for i, state in enumerate(states):
        if i == len(actions):
            ret.append((state, {0: 0}))
        else:
            action = actions[i]
            schema = action.replace("(", "").split()[0]
            ret.append((state, schema_cnt.copy()))
            schema_cnt[schema] -= 1
    return ret


# def get_tensor_graphs_from_plans(args):
#     print("Generating graphs from plans...")
#     graphs = []

#     representation = args.rep
#     domain_pddl = args.domain_pddl
#     tasks_dir = args.tasks_dir
#     plans_dir = args.plans_dir

#     for plan_file in tqdm(sorted(list(os.listdir(plans_dir)))):
#         problem_pddl = f"{tasks_dir}/{plan_file.replace('.plan', '.pddl')}"
#         assert os.path.exists(problem_pddl), problem_pddl
#         plan_file = f"{plans_dir}/{plan_file}"
#         rep = REPRESENTATIONS[representation](
#             domain_pddl=domain_pddl, problem_pddl=problem_pddl
#         )
#         rep.convert_to_pyg()
#         plan = get_plan_info(domain_pddl, problem_pddl, plan_file, args)

#         for state, schema_cnt in plan:
#             state = rep.str_to_state(state)
#             x, edge_index = rep.state_to_tgraph(state)
#             y = sum(schema_cnt.values())
#             graph = Data(x=x, edge_index=edge_index, y=y)
#             graphs.append(graph)

#     print("Graphs generated!")
#     return graphs


# def get_loaders_from_args_gnn(args):
#     batch_size = args.batch_size
#     small_train = args.small_train

#     dataset = get_tensor_graphs_from_plans(args)
#     if small_train:
#         random.seed(123)
#         dataset = random.sample(dataset, k=1000)

#     trainset, valset = train_test_split(
#         dataset, test_size=0.15, random_state=4550
#     )

#     get_stats(dataset=dataset, desc="Whole dataset")
#     get_stats(dataset=trainset, desc="Train set")
#     get_stats(dataset=valset, desc="Val set")
#     print("train size:", len(trainset))
#     print("validation size:", len(valset))

#     train_loader = DataLoader(
#         trainset,
#         batch_size=batch_size,
#         shuffle=True,
#     )
#     val_loader = DataLoader(
#         valset,
#         batch_size=batch_size,
#         shuffle=False,
#     )

#     return train_loader, val_loader


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
                            # print("split in another form")
                            fact_lists = fact_lists[0].split(')(')
                        for fact in fact_lists:
                            all_init.add('(' + fact + ')')

    except FileNotFoundError:
        print("The specified file was not found.")

    return all_init

# Modified version that use txt for generate dataset, y_keys pairs
def get_tensor_graph(tasks_dir, plans_dir, representation, domain_pddl):
    graphs = []
    for plan_file in tqdm(sorted(list(os.listdir(plans_dir)))):
        print(f'plan file name: {plan_file}')
        problem_pddl = f"{tasks_dir}/{plan_file.replace('.txt', '.pddl')}"
        assert os.path.exists(problem_pddl), problem_pddl
        plan_file = f"{plans_dir}/{plan_file}"
        rep = REPRESENTATIONS[representation](domain_pddl, problem_pddl) # get rep and plan_file name
        rep.convert_to_pyg()

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
                s = rep.str_to_state(s)
                x, edge_index = rep.state_to_tgraph(s)
                y = float(parts[1].strip())

                graph = Data(x=x, edge_index=edge_index, y=y)
                graphs.append(graph)
    return graphs 
        
# Modified version that generate both train and test data
def get_tensor_graphs_from_plans(args, test:bool = True):
    print("Generating graphs from plans...")
    representation = args.rep
    domain_pddl = args.domain_pddl
    tasks_dir = args.tasks_dir
    plans_dir = args.plans_dir
    plans_tests_dir = args.plans_tests_dir

    train_graphs = get_tensor_graph(tasks_dir, plans_dir, representation, domain_pddl)
    test_graphs = []
    if test:
        test_graphs = get_tensor_graph(tasks_dir, plans_tests_dir, representation, domain_pddl)
    print("My Graphs generated!")
    return train_graphs, test_graphs


# Modified version that collect final graph, y pairs
def get_loaders_from_args_gnn(args, test:bool = True):
    batch_size = args.batch_size
    small_train = args.small_train

    trainset, testset = get_tensor_graphs_from_plans(args, test)
    if small_train:
        random.seed(123)
        dataset = random.sample(dataset, k=1000)

    get_stats(dataset=trainset, desc="Train set")
    get_stats(dataset=testset, desc="Test set")
    print("train size:", len(trainset))
    print("test size:", len(testset))

    train_loader = DataLoader(
        trainset,
        batch_size=batch_size,
        shuffle=True,
    )
    test_loader = DataLoader(
        testset,
        batch_size=batch_size,
        shuffle=False,
    )

    return train_loader, test_loader