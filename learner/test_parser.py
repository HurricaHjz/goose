from representation.planning.translate.pddl import Task
from representation.planning.translate.pddl_parser import open

problem: Task = open(
            domain_filename= "/home/moss/COMP4550/goose/benchmarks/mcmp/exbw.domain_det.NO-COND.pddl", 
            task_filename="/home/moss/COMP4550/goose/benchmarks/mcmp/tasks_exbw/exbw_p01-n2-N5-s1.pddl"
        )
# problem: Task = open(
#             domain_filename= "/home/moss/COMP4550/goose/benchmarks/mcmp/tire.domain.pddl", 
#             task_filename="/home/moss/COMP4550/goose/benchmarks/mcmp/tasks_tire/tire03.pddl"
#         )
# problem: Task = open(
#             domain_filename= "/home/moss/COMP4550/goose/benchmarks/mcmp/test/test_domain.pddl", 
#             task_filename="/home/moss/COMP4550/goose/benchmarks/mcmp/test/test_task.pddl"
#         )
problem.dump()

# Problem exploding-blocksworld: ex_bw_5_p01 [:conditional-effects, :equality, :negative-preconditions, :probabilistic-effects, :rewards, :typing]
# Types:
#   object
#   block
# Objects:
#   b1: block
#   b2: block
#   b3: block
#   b4: block
#   b5: block
# Predicates:
#   on(?b1: block, ?b2: block)
#   on-table(?b: block)
#   clear(?b: block)
#   holding(?b: block)
#   emptyhand()
#   no-detonated(?b: block)
#   no-destroyed(?b: block)
#   no-destroyed-table()
#   =(?x: object, ?y: object)
# Functions:
# Init:
#   Atom no-detonated(b4)
#   Atom no-detonated(b5)
#   Atom no-destroyed(b2)
#   Atom on-table(b2)
#   Atom no-detonated(b1)
#   Atom no-detonated(b3)
#   Atom no-destroyed(b4)
#   Atom no-destroyed-table()
#   Atom on(b1, b4)
#   Atom no-destroyed(b5)
#   Atom on-table(b5)
#   Atom on(b4, b5)
#   Atom no-detonated(b2)
#   Atom no-destroyed(b1)
#   Atom clear(b1)
#   Atom no-destroyed(b3)
#   Atom on(b3, b2)
#   Atom clear(b3)
#   Atom emptyhand()
#   Atom =(b1, b1)
#   Atom =(b2, b2)
#   Atom =(b3, b3)
#   Atom =(b4, b4)
#   Atom =(b5, b5)
# Goal:
#   Conjunction
#     Atom on(b2, b4)
#     Atom on-table(b4)
# Actions:
# pick-up(?b1: block, ?b2: block)
# Precondition:
#   Conjunction
#     Atom emptyhand()
#     Atom clear(?b1)
#     Atom on(?b1, ?b2)
#     Atom no-destroyed(?b1)
# Effects:
#   Atom holding(?b1)
#   Atom clear(?b2)
#   NegatedAtom emptyhand()
#   NegatedAtom on(?b1, ?b2)
# Probabilities effects:
# Cost:
#   None
# pick-up-from-table(?b: block)
# Precondition:
#   Conjunction
#     Atom emptyhand()
#     Atom clear(?b)
#     Atom on-table(?b)
#     Atom no-destroyed(?b)
# Effects:
#   Atom holding(?b)
#   NegatedAtom emptyhand()
#   NegatedAtom on-table(?b)
# Probabilities effects:
# Cost:
#   None
# put-down-condtrue(?b: block)
# Precondition:
#   Conjunction
#     Atom holding(?b)
#     Atom no-destroyed-table()
#     Atom no-detonated(?b)
# Effects:
# Probabilities effects:
# prob - 0.4: 
#   Atom emptyhand()
#   Atom on-table(?b)
#   NegatedAtom holding(?b)
#   NegatedAtom no-destroyed-table()
#   NegatedAtom no-detonated(?b)
# prob - 0.6: 
#   Atom emptyhand()
#   Atom on-table(?b)
#   NegatedAtom holding(?b)
# Cost:
#   None
# put-down-condfalse(?b: block)
# Precondition:
#   Conjunction
#     Atom holding(?b)
#     Atom no-destroyed-table()
#     NegatedAtom no-detonated(?b)
# Effects:
#   Atom emptyhand()
#   Atom on-table(?b)
#   NegatedAtom holding(?b)
# Probabilities effects:
# Cost:
#   None
# put-on-block-condtrue(?b1: block, ?b2: block)
# Precondition:
#   Conjunction
#     Atom holding(?b1)
#     Atom no-detonated(?b1)
#     Atom clear(?b2)
#     Atom no-destroyed(?b2)
#     NegatedAtom =(?b1, ?b2)
# Effects:
# Probabilities effects:
# prob - 0.1: 
#   Atom emptyhand()
#   Atom on(?b1, ?b2)
#   NegatedAtom holding(?b1)
#   NegatedAtom clear(?b2)
#   NegatedAtom no-destroyed(?b2)
#   NegatedAtom no-detonated(?b1)
# prob - 0.9: 
#   Atom emptyhand()
#   Atom on(?b1, ?b2)
#   NegatedAtom holding(?b1)
#   NegatedAtom clear(?b2)
# Cost:
#   None
# put-on-block-condfalse(?b1: block, ?b2: block)
# Precondition:
#   Conjunction
#     Atom holding(?b1)
#     NegatedAtom no-detonated(?b1)
#     Atom clear(?b2)
#     Atom no-destroyed(?b2)
#     NegatedAtom =(?b1, ?b2)
# Effects:
#   Atom emptyhand()
#   Atom on(?b1, ?b2)
#   NegatedAtom holding(?b1)
#   NegatedAtom clear(?b2)
# Probabilities effects:
# Cost:
#   None

# Problem triangle-tire: triangle-tire-3 [:equality, :probabilistic-effects, :strips, :typing]
# Types:
#   object
#   location
# Objects:
#   l-1-1: location
#   l-1-2: location
#   l-1-3: location
#   l-1-4: location
#   l-1-5: location
#   l-1-6: location
#   l-1-7: location
#   l-2-1: location
#   l-2-2: location
#   l-2-3: location
#   l-2-4: location
#   l-2-5: location
#   l-2-6: location
#   l-2-7: location
#   l-3-1: location
#   l-3-2: location
#   l-3-3: location
#   l-3-4: location
#   l-3-5: location
#   l-3-6: location
#   l-3-7: location
#   l-4-1: location
#   l-4-2: location
#   l-4-3: location
#   l-4-4: location
#   l-4-5: location
#   l-4-6: location
#   l-4-7: location
#   l-5-1: location
#   l-5-2: location
#   l-5-3: location
#   l-5-4: location
#   l-5-5: location
#   l-5-6: location
#   l-5-7: location
#   l-6-1: location
#   l-6-2: location
#   l-6-3: location
#   l-6-4: location
#   l-6-5: location
#   l-6-6: location
#   l-6-7: location
#   l-7-1: location
#   l-7-2: location
#   l-7-3: location
#   l-7-4: location
#   l-7-5: location
#   l-7-6: location
#   l-7-7: location
# Predicates:
#   vehicle-at(?loc: location)
#   spare-in(?loc: location)
#   road(?from: location, ?to: location)
#   not-flattire()
#   hasspare()
#   =(?x: object, ?y: object)
# Functions:
# Init:
#   Atom road(l-4-4, l-3-5)
#   Atom road(l-5-2, l-6-2)
#   Atom road(l-3-2, l-4-2)
#   Atom road(l-4-3, l-3-4)
#   Atom spare-in(l-2-2)
#   Atom road(l-3-1, l-2-2)
#   Atom spare-in(l-3-5)
#   Atom spare-in(l-2-6)
#   Atom vehicle-at(l-1-1)
#   Atom spare-in(l-5-1)
#   Atom spare-in(l-2-1)
#   Atom road(l-1-6, l-1-7)
#   Atom road(l-1-2, l-2-2)
#   Atom spare-in(l-6-1)
#   Atom road(l-2-3, l-1-4)
#   Atom road(l-1-3, l-2-3)
#   Atom road(l-3-4, l-3-5)
#   Atom road(l-1-1, l-1-2)
#   Atom spare-in(l-7-1)
#   Atom not-flattire()
#   Atom road(l-7-1, l-6-2)
#   Atom road(l-2-5, l-1-6)
#   Atom road(l-2-1, l-3-1)
#   Atom road(l-3-3, l-4-3)
#   Atom road(l-4-1, l-3-2)
#   Atom road(l-4-1, l-5-1)
#   Atom spare-in(l-3-1)
#   Atom road(l-5-1, l-6-1)
#   Atom road(l-1-4, l-1-5)
#   Atom road(l-2-2, l-1-3)
#   Atom road(l-2-5, l-3-5)
#   Atom road(l-6-1, l-7-1)
#   Atom spare-in(l-5-3)
#   Atom road(l-1-4, l-2-4)
#   Atom road(l-3-5, l-2-6)
#   Atom spare-in(l-4-2)
#   Atom road(l-2-1, l-1-2)
#   Atom road(l-3-2, l-3-3)
#   Atom road(l-4-2, l-3-3)
#   Atom road(l-1-6, l-2-6)
#   Atom road(l-2-3, l-3-3)
#   Atom spare-in(l-4-3)
#   Atom road(l-6-2, l-5-3)
#   Atom spare-in(l-6-2)
#   Atom road(l-1-2, l-1-3)
#   Atom road(l-2-6, l-1-7)
#   Atom road(l-1-3, l-1-4)
#   Atom road(l-5-2, l-5-3)
#   Atom road(l-1-5, l-2-5)
#   Atom road(l-1-1, l-2-1)
#   Atom road(l-4-3, l-5-3)
#   Atom road(l-5-1, l-5-2)
#   Atom road(l-1-5, l-1-6)
#   Atom road(l-3-1, l-4-1)
#   Atom spare-in(l-4-4)
#   Atom road(l-3-1, l-3-2)
#   Atom spare-in(l-2-4)
#   Atom road(l-6-1, l-5-2)
#   Atom spare-in(l-4-1)
#   Atom road(l-2-4, l-1-5)
#   Atom spare-in(l-2-5)
#   Atom road(l-5-3, l-4-4)
#   Atom road(l-5-1, l-4-2)
#   Atom spare-in(l-2-3)
#   Atom road(l-3-3, l-2-4)
#   Atom road(l-3-4, l-4-4)
#   Atom road(l-3-3, l-3-4)
#   Atom =(l-1-1, l-1-1)
#   Atom =(l-1-2, l-1-2)
#   Atom =(l-1-3, l-1-3)
#   Atom =(l-1-4, l-1-4)
#   Atom =(l-1-5, l-1-5)
#   Atom =(l-1-6, l-1-6)
#   Atom =(l-1-7, l-1-7)
#   Atom =(l-2-1, l-2-1)
#   Atom =(l-2-2, l-2-2)
#   Atom =(l-2-3, l-2-3)
#   Atom =(l-2-4, l-2-4)
#   Atom =(l-2-5, l-2-5)
#   Atom =(l-2-6, l-2-6)
#   Atom =(l-2-7, l-2-7)
#   Atom =(l-3-1, l-3-1)
#   Atom =(l-3-2, l-3-2)
#   Atom =(l-3-3, l-3-3)
#   Atom =(l-3-4, l-3-4)
#   Atom =(l-3-5, l-3-5)
#   Atom =(l-3-6, l-3-6)
#   Atom =(l-3-7, l-3-7)
#   Atom =(l-4-1, l-4-1)
#   Atom =(l-4-2, l-4-2)
#   Atom =(l-4-3, l-4-3)
#   Atom =(l-4-4, l-4-4)
#   Atom =(l-4-5, l-4-5)
#   Atom =(l-4-6, l-4-6)
#   Atom =(l-4-7, l-4-7)
#   Atom =(l-5-1, l-5-1)
#   Atom =(l-5-2, l-5-2)
#   Atom =(l-5-3, l-5-3)
#   Atom =(l-5-4, l-5-4)
#   Atom =(l-5-5, l-5-5)
#   Atom =(l-5-6, l-5-6)
#   Atom =(l-5-7, l-5-7)
#   Atom =(l-6-1, l-6-1)
#   Atom =(l-6-2, l-6-2)
#   Atom =(l-6-3, l-6-3)
#   Atom =(l-6-4, l-6-4)
#   Atom =(l-6-5, l-6-5)
#   Atom =(l-6-6, l-6-6)
#   Atom =(l-6-7, l-6-7)
#   Atom =(l-7-1, l-7-1)
#   Atom =(l-7-2, l-7-2)
#   Atom =(l-7-3, l-7-3)
#   Atom =(l-7-4, l-7-4)
#   Atom =(l-7-5, l-7-5)
#   Atom =(l-7-6, l-7-6)
#   Atom =(l-7-7, l-7-7)
# Goal:
#   Atom vehicle-at(l-1-7)
# Actions:
# move-car(?from: location, ?to: location)
# Precondition:
#   Conjunction
#     Atom vehicle-at(?from)
#     Atom road(?from, ?to)
#     Atom not-flattire()
# Effects:
# Probabilities effects:
# prob - 0.5: 
#   Atom vehicle-at(?to)
#   NegatedAtom vehicle-at(?from)
#   NegatedAtom not-flattire()
# prob - 0.5: 
#   Atom vehicle-at(?to)
#   NegatedAtom vehicle-at(?from)
# Cost:
#   None
# loadtire(?loc: location)
# Precondition:
#   Conjunction
#     Atom vehicle-at(?loc)
#     Atom spare-in(?loc)
# Effects:
#   Atom hasspare()
#   NegatedAtom spare-in(?loc)
# Probabilities effects:
# Cost:
#   None
# changetire()
# Precondition:
#   Atom hasspare()
# Effects:
#   NegatedAtom hasspare()
#   Atom not-flattire()
# Probabilities effects:
# Cost:
# None