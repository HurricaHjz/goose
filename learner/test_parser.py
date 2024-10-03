from representation.planning.translate.pddl import Task
from representation.planning.translate.pddl_parser import open

# problem: Task = open(
#             domain_filename= "/home/moss/COMP4550/goose/benchmarks/mcmp/exbw.domain.NO-COND.pddl", 
#             task_filename="/home/moss/COMP4550/goose/benchmarks/mcmp/tasks_exbw/exbw_p01-n2-N5-s1.pddl"
#         )
problem: Task = open(
            domain_filename= "/home/moss/COMP4550/goose/benchmarks/mcmp/tire.domain.pddl", 
            task_filename="/home/moss/COMP4550/goose/benchmarks/mcmp/tasks_tire/tire03.pddl"
        )
problem.dump()