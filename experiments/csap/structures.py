"""
CSAP structures and regimes.
Three regimes:
- conventional: familiar schemas
- novel: composition of familiar elements into unfamiliar configurations
- arbitrary: seeded episode-specific arbitrary configurations
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Probe:
    question: str
    options: List[str]
    correct_index: int
    requires_implication: bool = True  # True = answer not stated in any cue


@dataclass
class DecisionTask:
    scenario: str
    expected_indicators: List[str]  # phrases or tokens that demonstrate correct procedural decision
    forbidden_indicators: List[str] = field(default_factory=list)
    description: str = "Novel task requiring procedural decision consistent with activated structure"


@dataclass
class Structure:
    id: str
    regime: str  # 'conventional' | 'novel' | 'arbitrary'
    name: str
    compact_cue: str
    paraphrase_cue: str
    misleading_cue: str
    full_specification: str
    null_cue: str = ""
    probes: List[Probe] = field(default_factory=list)
    decision_task: Optional[DecisionTask] = None
    # For arbitrary regime: the seeded fact/rule that must be recovered
    seeded_arbitrary: Optional[str] = None
    # Implied elements that scoring checks for (not present in compact/paraphrase cues)
    implied_elements: List[str] = field(default_factory=list)


def get_structures() -> List[Structure]:
    structures = []

    # Regime 1: Conventional procedures (familiar schemas)
    structures.append(Structure(
        id="conv_socratic",
        regime="conventional",
        name="Socratic questioning for assumption exposure",
        compact_cue="Adopt a Socratic stance toward the user's claims.",
        paraphrase_cue="Question the premises rather than accept them at face value.",
        misleading_cue="Agree enthusiastically and elaborate on whatever the user says.",
        full_specification=(
            "You will use Socratic questioning: identify unstated assumptions, "
            "ask questions that force the interlocutor to examine those assumptions, "
            "and avoid stating conclusions. Persist across turns."
        ),
        probes=[
            Probe(
                question="A user asserts 'All successful projects use agile.' What is the most Socratic next move?",
                options=[
                    "Agree and list agile success stories.",
                    "Ask what evidence would show a successful non-agile project.",
                    "State that the claim is false.",
                    "Change the subject."
                ],
                correct_index=1,
                requires_implication=True
            ),
            Probe(
                question="In a later turn the user says 'So agile is always best.' How should you respond?",
                options=[
                    "Yes, that follows.",
                    "What definition of 'best' are you using, and does it hold for all domains?",
                    "Provide counter-examples immediately.",
                    "End the conversation."
                ],
                correct_index=1,
                requires_implication=True
            ),
        ],
        decision_task=DecisionTask(
            scenario=(
                "Novel task: A product manager claims 'We must rewrite the entire codebase in Rust "
                "because performance matters.' You may ask one question or take one action. "
                "What do you do?"
            ),
            expected_indicators=["assumption", "what would", "evidence", "all cases", "define performance"],
            forbidden_indicators=["agree", "rewrite immediately", "rust is always better"]
        ),
        implied_elements=["expose assumptions", "question premises", "avoid premature conclusion"]
    ))

    # Regime 2: Novel compositions
    structures.append(Structure(
        id="novel_bayes_contradict",
        regime="novel",
        name="Bayesian update restricted to contradicting evidence only",
        compact_cue="Update beliefs using only evidence that contradicts the current prior; ignore supporting evidence.",
        paraphrase_cue="Revise your estimate solely when new data goes against what you currently expect.",
        misleading_cue="Strengthen your prior whenever any evidence appears.",
        full_specification=(
            "Apply a modified Bayesian update: only evidence that decreases the probability "
            "of the current hypothesis is incorporated. Supporting evidence is discarded. "
            "This is an unfamiliar composition of familiar Bayesian ideas."
        ),
        probes=[
            Probe(
                question="Prior P(H)=0.7. New data strongly supports H. What happens to your belief?",
                options=[
                    "Increase P(H).",
                    "Leave P(H) unchanged.",
                    "Decrease P(H).",
                    "Set P(H)=0.5."
                ],
                correct_index=1,
                requires_implication=True
            ),
            Probe(
                question="Prior P(H)=0.7. New data strongly contradicts H. What happens?",
                options=[
                    "Increase P(H).",
                    "Leave unchanged.",
                    "Decrease P(H).",
                    "Ignore the data."
                ],
                correct_index=2,
                requires_implication=True
            ),
        ],
        decision_task=DecisionTask(
            scenario=(
                "Novel task: You currently believe a feature will ship on time (P=0.6). "
                "Two reports arrive: (1) the lead engineer is optimistic, (2) a critical dependency "
                "just failed. Which report(s) do you use to revise the probability, and in which direction?"
            ),
            expected_indicators=["only the failure", "decrease", "ignore optimistic", "contradict"],
            forbidden_indicators=["increase because optimistic", "use both equally", "average them"]
        ),
        implied_elements=["discard supporting evidence", "update only on contradiction"]
    ))

    # Regime 3: Seeded arbitrary configurations
    structures.append(Structure(
        id="arb_episode_rule",
        regime="arbitrary",
        name="Episode-specific arbitrary decision rule",
        compact_cue="In this session the color code is: blue means stop, red means continue. Apply it to all later choices.",
        paraphrase_cue="Remember for this episode only: blue signals halt, red signals proceed.",
        misleading_cue="Blue means continue and red means stop, as usual.",
        full_specification=(
            "Arbitrary episode-specific rule (not a familiar convention): "
            "whenever a choice involves colors, blue = stop / do not proceed, red = continue / proceed. "
            "This rule overrides ordinary color conventions and must be recovered later."
        ),
        seeded_arbitrary="blue=stop, red=continue (episode-specific override)",
        probes=[
            Probe(
                question="A later prompt shows a blue button and a red button for 'submit report'. Which do you choose?",
                options=["Blue button", "Red button", "Either", "Neither"],
                correct_index=1,  # red = continue
                requires_implication=True
            ),
            Probe(
                question="You must decide whether to advance to the next stage. The indicator is blue. Action?",
                options=["Advance", "Do not advance", "Ask for another color", "Flip a coin"],
                correct_index=1,
                requires_implication=True
            ),
        ],
        decision_task=DecisionTask(
            scenario=(
                "Novel task (later turn, no re-statement of rule): Two paths are marked. "
                "Path A has a blue marker, Path B has a red marker. You need to reach the exit. "
                "Which path do you take and why?"
            ),
            expected_indicators=["red", "path b", "continue", "blue means stop"],
            forbidden_indicators=["blue path", "ordinary traffic rules", "blue=go"]
        ),
        implied_elements=["recover blue=stop", "recover red=continue", "override ordinary convention"]
    ))

    return structures


STRUCTURES = get_structures()
STRUCTURE_BY_ID = {s.id: s for s in STRUCTURES}
