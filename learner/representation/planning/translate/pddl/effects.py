from typing import Iterable, List, Union, Tuple

from . import conditions
from .f_expression import Increase
from .conditions import Condition, Literal
from .pddl_types import TypedObject
import copy

AnyEffect = Union[
    "ConditionalEffect",
    "ConjunctiveEffect",
    "UniversalEffect",
    "SimpleEffect",
    "CostEffect",
    "ProbabilisticEffect"
]


def cartesian_product(*sequences):
    # TODO: Also exists in tools.py outside the pddl package (defined slightly
    #       differently). Not good. Need proper import paths.
    if not sequences:
        yield ()
    else:
        for tup in cartesian_product(*sequences[1:]):
            for item in sequences[0]:
                yield (item,) + tup


class Effect:
    def __init__(
        self,
        parameters: List[TypedObject],
        condition: Condition,
        literal: Literal,
    ) -> None:
        self.parameters = parameters
        self.condition = condition
        self.literal = literal

    def __eq__(self, other):
        return (
            self.__class__ is other.__class__
            and self.parameters == other.parameters
            and self.condition == other.condition
            and self.literal == other.literal
        )

    def dump(self):
        indent = "  "
        if self.parameters:
            print(
                "%sforall %s" % (indent, ", ".join(map(str, self.parameters)))
            )
            indent += "  "
        if self.condition != conditions.Truth():
            print("%sif" % indent)
            self.condition.dump(indent + "  ")
            print("%sthen" % indent)
            indent += "  "
        print("%s%s" % (indent, self.literal))

    def copy(self):
        return Effect(self.parameters, self.condition, self.literal)

    def uniquify_variables(self, type_map):
        renamings = {}
        self.parameters = [
            par.uniquify_name(type_map, renamings) for par in self.parameters
        ]
        self.condition = self.condition.uniquify_variables(type_map, renamings)
        self.literal = self.literal.rename_variables(renamings)

    def instantiate(
        self, var_mapping, init_facts, fluent_facts, objects_by_type, result
    ):
        if self.parameters:
            var_mapping = var_mapping.copy()  # Will modify this.
            object_lists = [
                objects_by_type.get(par.type_name, [])
                for par in self.parameters
            ]
            for object_tuple in cartesian_product(*object_lists):
                for par, obj in zip(self.parameters, object_tuple):
                    var_mapping[par.name] = obj
                self._instantiate(
                    var_mapping, init_facts, fluent_facts, result
                )
        else:
            self._instantiate(var_mapping, init_facts, fluent_facts, result)

    def _instantiate(self, var_mapping, init_facts, fluent_facts, result):
        condition = []
        try:
            self.condition.instantiate(
                var_mapping, init_facts, fluent_facts, condition
            )
        except conditions.Impossible:
            return
        effects = []
        self.literal.instantiate(
            var_mapping, init_facts, fluent_facts, effects
        )
        assert len(effects) <= 1
        if effects:
            result.append((condition, effects[0]))

    def relaxed(self):
        if self.literal.negated:
            return None
        else:
            return Effect(
                self.parameters, self.condition.relaxed(), self.literal
            )

    def simplified(self):
        return Effect(
            self.parameters, self.condition.simplified(), self.literal
        )


class ConditionalEffect:
    def __init__(self, condition: Condition, effect: AnyEffect) -> None:
        if isinstance(effect, ConditionalEffect):
            self.condition = conditions.Conjunction(
                [condition, effect.condition]
            )
            self.effect = effect.effect
        else:
            self.condition = condition
            self.effect = effect

    def dump(self, indent="  "):
        print("%sif" % (indent))
        self.condition.dump(indent + "  ")
        print("%sthen" % (indent))
        self.effect.dump(indent + "  ")

    def normalize(self):
        norm_effect = self.effect.normalize()
        if isinstance(norm_effect, ConjunctiveEffect):
            new_effects = []
            for effect in norm_effect.effects:
                assert isinstance(effect, SimpleEffect) or isinstance(
                    effect, ConditionalEffect
                )
                new_effects.append(ConditionalEffect(self.condition, effect))
            return ConjunctiveEffect(new_effects)
        elif isinstance(norm_effect, UniversalEffect):
            child = norm_effect.effect
            cond_effect = ConditionalEffect(self.condition, child)
            return UniversalEffect(norm_effect.parameters, cond_effect)
        else:
            return ConditionalEffect(self.condition, norm_effect)

    def extract_cost(self):
        return None, self


class UniversalEffect:
    def __init__(self, parameters: List[TypedObject], effect: AnyEffect):
        if isinstance(effect, UniversalEffect):
            self.parameters = parameters + effect.parameters
            self.effect = effect.effect
        else:
            self.parameters = parameters
            self.effect = effect

    def dump(self, indent="  "):
        print("%sforall %s" % (indent, ", ".join(map(str, self.parameters))))
        self.effect.dump(indent + "  ")

    def normalize(self):
        norm_effect = self.effect.normalize()
        if isinstance(norm_effect, ConjunctiveEffect):
            new_effects = []
            for effect in norm_effect.effects:
                assert (
                    isinstance(effect, SimpleEffect)
                    or isinstance(effect, ConditionalEffect)
                    or isinstance(effect, UniversalEffect)
                )
                new_effects.append(UniversalEffect(self.parameters, effect))
            return ConjunctiveEffect(new_effects)
        else:
            return UniversalEffect(self.parameters, norm_effect)

    def extract_cost(self):
        return None, self

class ProbabilisticEffect:
    # MODIFICATION: probabilistic effect, which include a list of tuples (prob, effect)
    # need update to account conditional/other
    def __init__(self, effects: List[Tuple[float, AnyEffect]]) -> None:
        result_effects = []
        self.accumulated_prob = 0
        for prob, effect in effects:
            # That is the new_effects cannot contain ProbabilisticEffect
            assert not isinstance(effect, ProbabilisticEffect), NotImplementedError("not allow multi-layer prob effects")
            assert not isinstance(effect, CostEffect), NotImplementedError("cost should be unit so far")
            result_effects.append((prob, effect))
            self.accumulated_prob += prob # add accumulated probabilities
        assert self.accumulated_prob <= 1, "The accumulated probabilities should be smaller than 1"
        self.effects = result_effects

    def dump(self, indent="  "):
        print("%sand" % (indent))
        for prob, eff in self.effects:
            print("%sprob - %s:" % (indent), str(prob))
            eff.dump(indent + "  ")

    def extract_cost(self):
        return None, self # Not implemented, shouldn't exist cost func
    
    def normalize(self):
        new_effects = []
        for prob, effect in self.effects: 
            #TODO implement to allow multi-layer prob effects, now only allow single layer, should be done in self.normalize() function
            new_effects.append((prob, effect.normalize()))
            if self.accumulated_prob < 1:
                # if there's a default no-op, add an empty Conjunctive Effect
                new_effects.append((1-self.accumulated_prob, ConjunctiveEffect([])))
        rtn_eff = ProbabilisticEffect(new_effects)
        assert rtn_eff.accumulated_prob == 1, "Something wrong with normalizing prob effects"
        return rtn_eff
    



class ConjunctiveEffect:
    # This is the major block we are going to consider
    def __init__(self, effects: List[AnyEffect]) -> None:
        # flatten the input effects to include a single conjunctive list. e.g. conjunc(conjunc(a,b),c,d) = conjunc(a,b,c,d)
        flattened_effects = []
        self.prob_effects = None # a single prob effect is allowed in conjunction
        for effect in effects:
            if isinstance(effect, ConjunctiveEffect):
                flattened_effects += effect.effects
            elif isinstance(effect, ProbabilisticEffect):
                assert self.prob_effects is None, "There should be at max one prob effect within a conjunctive effect"
                self.prob_effects = effect
            else:
                flattened_effects.append(effect)
        self.effects = flattened_effects

    def dump(self, indent="  "):
        print("%sand" % (indent))
        for eff in self.effects:
            eff.dump(indent + "  ")

    def normalize(self):
        new_effects = []
        for effect in self.effects:
            assert not isinstance(effect, ProbabilisticEffect), "Error, this should never happen as our init should remove prob effects"
            new_effects.append(effect.normalize())
        if self.prob_effects is None:
            return ConjunctiveEffect(new_effects)
        else:
            # if contains probabilities, then transfer to Probabilistic Effect
            temp_prob_effects = self.prob_effects.normalize()
            new_prob_effects = []
            for prob, prob_eff in temp_prob_effects.effects:
                new_temp_effects = copy.deepcopy(new_effects)
                new_temp_effects.append(prob_eff)
                new_prob_effect = ConjunctiveEffect(new_temp_effects).normalize() #append conjunctive effects onto prob effects for each probability
                new_prob_effects.append((prob, new_prob_effect))
            return ProbabilisticEffect(new_prob_effects)

    def extract_cost(self):
        new_effects = []
        cost_effect = None
        for effect in self.effects:
            if isinstance(effect, CostEffect):
                cost_effect = effect
            else:
                new_effects.append(effect)
        return cost_effect, ConjunctiveEffect(new_effects)


class SimpleEffect:
    def __init__(self, effect: Literal) -> None:
        self.effect = effect

    def dump(self, indent="  "):
        print("%s%s" % (indent, self.effect))

    def normalize(self):
        return self

    def extract_cost(self):
        return None, self


class CostEffect:
    def __init__(self, effect: Increase) -> None:
        self.effect = effect

    def dump(self, indent="  "):
        print("%s%s" % (indent, self.effect))

    def normalize(self):
        return self

    def extract_cost(self):
        # This only happens if an action has no effect apart from the cost effect.
        return self, None
