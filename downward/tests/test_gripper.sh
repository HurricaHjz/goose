DOMAIN="../../benchmarks/goose/gripper/domain.pddl"
INSTANCE="../../benchmarks/goose/gripper/val/gripper-n11.pddl"
CONFIG="1"

# 0: slg, 1: flg, 2: llg, 3: glg

export GOOSE="$HOME/code/goose/learner"

cd tests

# by default, reopen_closed=false
./../fast-downward.py $DOMAIN $INSTANCE --search "eager_greedy([goose(graph=$CONFIG)])"
