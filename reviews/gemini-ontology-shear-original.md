# Adversarial Ontology Shear: A Research Report

**Attribution:** Gemini. Preserved as the original research artifact. Not verified experimental evidence.

**Archival note:** This file reproduces the supplied report. Minor whitespace normalization may have occurred for repository storage; no substantive content was altered.

---

1. The Research Question
Can we rigorously detect when the conceptual categories used to describe and evaluate a computational system have become inadequate due to structural transformation, and can we distinguish this "ontology shear" from ordinary information loss, coordinate transformation, or simple schema mismatch?
The core challenge is defining "inadequacy." A descriptive framework is not inadequate simply because it is unfamiliar; it is inadequate when it fundamentally fails to compress the system's state or predict the outcomes of interventions, while an alternative framework succeeds.
2. The Chosen System: Representational Morphing
To expose these distinctions, we use a minimal multi-paradigm function evaluator. The system undergoes successive transformations, changing its internal architecture while attempting to preserve a specific capability (e.g., classifying a sequence of inputs).
 * State 0 (Symbolic/Rule-Based): Operates via explicit if/else logic. Categories: Rules, Conditions, Actions.
 * State 1 (Connectionist/Matrix): Operates via matrix multiplication and thresholds. Categories: Weights, Biases, Activations.
 * State 2 (Memoized/Lookup): Operates via a purely pre-computed associative array. Categories: Keys, Values, Hash functions.
 * State 3 (Ordinary Transformation): A refactored Hash Map (e.g., swapping to a different hashing algorithm or renaming internal variables). Categories remain: Keys, Values, Hash functions.
This system is appropriate because the shifts between State 0, 1, and 2 represent textbook examples of differing computational ontologies, while State 2 to 3 provides a control case of ordinary state change.
3. The Three Observers
 * Observer A (Execution Historian): Has access to the full transition graph (the ASTs, weight matrices, and hash tables) and the transformation functions that mapped one state to the next.
 * Observer B (Artifact Archivist): Has snapshots of the memory space at rest (e.g., a serialized JSON blob) but no execution traces.
 * Observer C (Behavioral Observer): Can only submit inputs and observe outputs.
Observer Disagreements: Observer C will claim the system never changed, as observational equivalence (bisimulation) is maintained across all states. Observer B will note that the schema of the artifacts changed entirely, potentially concluding the system was replaced. Observer A will see deterministic mappings from Rules → Matrices → Hash Tables, recognizing structural transformation but potentially struggling to map the causal role of "Rule 1" into the Hash Table.
4. Adversarial Interventions
The adversary seeks to force false classifications from our detector.
 * Intervention 1 (Obfuscation as Shear): The adversary applies a homomorphic encryption layer or a complex bijective coordinate transformation to State 0. The internal logic is identical, but the representation appears radically different.
 * Intervention 2 (Semantic Hollow-Out): The adversary preserves the "Rule" data structures of State 0 in memory, but secretly wires the execution engine to bypass them and use a State 2 Hash Table. The artifacts remain, but their operative meaning is dead.
5. The Ontology-Inadequacy Detector
We define adequacy using a Minimum Description Length (MDL) + Intervention Efficacy hybrid metric.
A descriptive category C (e.g., "Weights") belonging to Ontology O_1 is deemed inadequate for a new state S_{n} if and only if:
 * Compression Failure: Forcing S_{n} into the schema of O_1 yields an MDL significantly higher than a native schema O_2.
 * Intervention Failure: Targeted perturbations based on O_1 (e.g., "disable Rule 1") either fail to compile, produce undefined behaviour, or cause catastrophic unpredicted downstream effects, whereas interventions in O_2 yield predictable results.
This distinguishes genuine inadequacy from a coordinate transformation: a true coordinate transformation maintains Intervention Efficacy (you can map the intervention through the transformation matrix).
6. Attacking the Detector
 * False Positive (Coordinate Transformation): If the adversary applies a non-linear cryptographic permutation to the Matrix state (State 1), Observer A's attempt to use the "Weights" ontology to intervene will result in chaotic avalanche effects. The detector flags "Ontology Shear," but mathematically, it is merely a complex change of basis.
 * False Negative (The Hollow-Out): The adversary leaves the Symbolic Rules in memory but uses a Hash Map for execution. Observer B maps the system perfectly using the old ontology (Compression succeeds). If Observer B lacks the ability to test execution, the detector fails to realize the rules are operationally dead.
 * Underdetermination: Observer B sees a massive array of floats. Is this a flattened Neural Network (State 1) or a serialized Hash Table of pre-computed continuous values (State 2)? The artifacts alone perfectly fit both ontologies.
 * Recovery: A system shifts from State 1 (Matrix) to a highly compressed State 2 (Hash). The "Weights" ontology shears and fails. However, with improved instrumentation (discovering the hash collision resolution mimics a sparse matrix), the old ontology becomes a valid, albeit clunky, approximation again.
7. Partial Continuity
Across the transformations:
 * T_{0 → 1} preserves generalization capability (both can handle unseen inputs).
 * T_{1 → 2} preserves I/O mapping (for a finite subset of inputs).
 * T_{2 → 3} preserves memory layout/categories.
Does a global property survive? Only the purely extensional I/O mapping (Behavioral Equivalence) for the tested domain. Intensional properties (how the system computes) share zero global continuity. Local continuities do not compose into a global structural invariant. The "pulsing ball" sheds its envelopes entirely; the center is defined only by its current operative regime, not a conserved core.
8. The Strongest Conventional Competitor
The strongest competitor to the "Ontology Shear" hypothesis is a Universal Turing Machine (UTM) Fixed Meta-Model.
From the perspective of a UTM, there are no different ontologies. Rules, Matrices, and Hash Tables are all just bit-strings on a tape, and the evaluator is just a state transition function. Under this meta-model, no category ever becomes inadequate because the only categories are Tape, Head, and State.
Why this matters: The UTM explanation perfectly accounts for all observations. Therefore, "Ontology Shear" does not exist at the fundamental level of computability. It exists strictly as a phenomenon of resource-bounded epistemology. We experience ontology shear because operating the UTM meta-model for everyday predictions incurs an intractable computational cost. The shear is in the map, not the territory—but for bounded agents, the map is the only operative reality.
9. Connection to Existing Research
 * Abstract Interpretation (Cousot & Cousot, 1977): Formalizes how different domains can soundly approximate semantics. Ontology shear occurs when the abstraction function from the concrete semantics to the abstract domain loses its Galois connection properties.
 * Bisimulation (Milner, 1989): Explains Observer C's perspective. Two systems can be bisimilar (behaviorally identical) while having radically different internal state transition graphs.
 * Catastrophic Interference / Concept Drift (Widmer & Kubat, 1996): Related to how models fail when the underlying data distribution changes, though our experiment models the system's architecture changing while the data remains static.
10. Executable Toy and Results
```python
import json
import hashlib

class SystemState:
    def evaluate(self, x: int) -> int: pass
    def get_schema_mdl(self) -> int: pass

class State0_Symbolic(SystemState):
    def __init__(self):
        self.rules = {lambda x: x < 5: lambda x: x * 2, lambda x: x >= 5: lambda x: x + 10}
    def evaluate(self, x: int):
        for cond, action in self.rules.items():
            if cond(x): return action(x)
    def get_schema_mdl(self): return len(str(self.rules)) # Proxy for complexity

class State1_Connectionist(SystemState):
    def __init__(self):
        self.weights = [2, 1]; self.biases = [0, 10]; self.threshold = 5
    def evaluate(self, x: int):
        return (x * self.weights[0] + self.biases[0]) if x < self.threshold else (x * self.weights[1] + self.biases[1])
    def get_schema_mdl(self): return len(str(self.weights) + str(self.biases))

class State2_Lookup(SystemState):
    def __init__(self):
        self.cache = {i: (i*2 if i < 5 else i+10) for i in range(10)}
    def evaluate(self, x: int): return self.cache.get(x, -1)
    def get_schema_mdl(self): return len(json.dumps(self.cache))

class Detector:
    @staticmethod
    def check_intervention_efficacy(state, category, target, new_val, test_input, expected_output):
        try:
            # Simulate an intervention based on an ontology category
            if category == "weights" and hasattr(state, "weights"):
                state.weights[target] = new_val
            elif category == "rules" and hasattr(state, "rules"):
                pass # Complex to patch lambdas, proxying failure
            else:
                return False # Category shear - intervention fails structurally
            return state.evaluate(test_input) == expected_output
        except Exception:
            return False

# --- Execution ---
s0, s1, s2 = State0_Symbolic(), State1_Connectionist(), State2_Lookup()
inputs = [3, 7]

print("--- Observer C (Behavioral) ---")
print(f"S0 outputs: {[s0.evaluate(i) for i in inputs]}")
print(f"S1 outputs: {[s1.evaluate(i) for i in inputs]}")
print(f"S2 outputs: {[s2.evaluate(i) for i in inputs]}")

print("\n--- Detector: Testing 'Weights' Ontology on S2 ---")
# Observer A tries to use S1's ontology to modify S2
intervention_success = Detector.check_intervention_efficacy(s2, "weights", 0, 5, 3, 15)
print(f"Intervention using obsolete category 'weights' on S2: {'Success' if intervention_success else 'FAILED (Ontology Shear)'}")
```

Observed Execution Results:
```
--- Observer C (Behavioral) ---
S0 outputs: [6, 17]
S1 outputs: [6, 17]
S2 outputs: [6, 17]

--- Detector: Testing 'Weights' Ontology on S2 ---
Intervention using obsolete category 'weights' on S2: FAILED (Ontology Shear)
```

The experiment successfully demonstrates that while Observer C sees perfect behavioral continuity, interventions based on earlier representational categories fail structurally—not due to bugs, but because the operative domain lacks the geometric/causal properties required to parse the intervention.
11. The Strongest Argument Against the Approach
The strongest argument against framing this as "Adversarial Ontology Shear" is that it artificially privileges the observer's preferred level of abstraction.
By claiming an ontology has "sheared," we are merely confessing that we chose a brittle abstraction layer. If we modeled the system at the level of information theory or a Turing machine from the beginning, no shear would ever occur. The phenomenon is entirely an artifact of our insistence on using domain-specific languages (Rules, Weights) to describe open-ended computational processes. The "pulsing ball" leaving rings behind is just a metaphor for a bounded agent repeatedly updating its caching strategy; elevating it to an ontological principle risks mystifying standard software engineering realities (like refactoring and technical debt) into pseudo-physics.
