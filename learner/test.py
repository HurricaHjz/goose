from models.save_load import load_gnn_model_and_setup, load_kernel_model_and_setup
from typing import FrozenSet, TypeVar

state_string = ["(no-destroyed b1)", "(clear b1)","(holding b1)", "(clear b3)", "(clear b4)", "(no-destroyed b2)", "(no-destroyed b3)", "(on b3 b2)", "(no-destroyed b4)", "(on b4 b5)", "(no-destroyed b5)", "(on-table b2)", "(on-table b5)", "(no-destroyed-table)", "(no-detonated b1)", "(no-detonated b2)", "(no-detonated b3)", "(no-detonated b4)", "(no-detonated b5)"]
wl_MODEL_PATH = "/home/moss/COMP4550/goose/mcmp_exbw_wl_plgl_small.model"
gnn_MODEL_PATH = "/home/moss/COMP4550/mcmp-planner/mcmp_exbw_gnn_plgs_small.model"
DOMAIN_FILE = "/home/moss/COMP4550/mcmp-planner/benchmarks/mcmp/exbw.domain.NO-COND.pddl"
TASK_FILE = "/home/moss/COMP4550/mcmp-planner/benchmarks/mcmp/tasks_exbw/exbw_p01-n2-N5-s1.pddl"

# model = load_gnn_model_and_setup(gnn_MODEL_PATH, DOMAIN_FILE, TASK_FILE)
# lifted_state = model.rep.str_to_state(state_string)

model = load_kernel_model_and_setup(wl_MODEL_PATH, DOMAIN_FILE, TASK_FILE)
lifted_state = model._representation.str_to_state(state_string)


print(model.__class__)
print(lifted_state)
print(model.h_help(state_string))