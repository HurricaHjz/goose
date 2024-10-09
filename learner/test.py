import networkx as nx
from representation import plg_s, llg

# domain_filename= "/home/moss/COMP4550/goose/benchmarks/mcmp/test/test_domain.pddl"
# task_filename="/home/moss/COMP4550/goose/benchmarks/mcmp/test/test_task.pddl"
# prob = plg_s.ProbabilisitcLiftedLearningGraphSimple(domain_filename, task_filename)
# print(plg_s.prob_to_colour(0))

# domain_filename= "/home/moss/COMP4550/goose/benchmarks/mcmp/exbw.domain_det.NO-COND.pddl"
# task_filename="/home/moss/COMP4550/goose/benchmarks/mcmp/tasks_exbw/exbw_p01-n2-N5-s1.pddl"
# prob = llg.LiftedLearningGraph(domain_filename, task_filename)

from collections import defaultdict

# Create a defaultdict with list as the default factory
my_dict = defaultdict(list)

# Access a key that does not exist
# print(my_dict['a'])  # Output: []

# Add elements to a non-existing key
my_dict['b'].append(1)

# Print the dictionary after modification
# print(my_dict)  # Output: defaultdict(<class 'list'>, {'a': [1]})

for a,b in []:
    print(a)
    print(b)

