# singularity exec --nv ../gpu.sif python3 run.py ../benchmarks/goose/gripper/domain.pddl ../benchmarks/goose/gripper/test/gripper-n20.pddl gnn -m saved_models/dd_llg_gripper.dt
singularity exec --nv ../gpu.sif python3 run.py ../benchmarks/goose/gripper/domain.pddl ../benchmarks/goose/gripper/test/gripper-n20.pddl gnn -m saved_models/dd_slg_gripper.dt