import unittest
from experiments.causal_role_preservation import (
    ActiveSystem, HollowedSystem, TranslatedSystem, expected,
    ExecutionHistorian, ArtifactArchivist,
)


class TestCausalRole(unittest.TestCase):
    def test_baseline_agreement(self):
        for Sys in (ActiveSystem, HollowedSystem, TranslatedSystem):
            s = Sys()
            for x in [0, 3, 4, 5, 7, 9]:
                self.assertEqual(s.evaluate(x), expected(x))

    def test_active_intervention_changes_output(self):
        s = ActiveSystem()
        self.assertEqual(s.evaluate(3), 6)
        s.intervene_rule("low_mult", 99)
        self.assertEqual(s.evaluate(3), 297)

    def test_hollowed_intervention_does_nothing(self):
        s = HollowedSystem()
        self.assertEqual(s.evaluate(3), 6)
        s.intervene_rule("low_mult", 99)
        self.assertEqual(s.evaluate(3), 6)

    def test_translated_intervention_works(self):
        s = TranslatedSystem()
        self.assertEqual(s.evaluate(3), 6)
        s.intervene_translated("low_mult", 99)
        self.assertEqual(s.evaluate(3), 297)

    def test_historian_distinguishes(self):
        h = ExecutionHistorian()
        self.assertEqual(h.classify(ActiveSystem()), "active")
        self.assertEqual(h.classify(HollowedSystem()), "hollowed")

    def test_archivist_sees_inert(self):
        a = ArtifactArchivist()
        self.assertEqual(a.classify(ActiveSystem()), "active_or_translated")
        self.assertEqual(a.classify(HollowedSystem()), "inert_or_unrelated")

    def test_out_of_domain(self):
        h = HollowedSystem()
        self.assertEqual(h.evaluate(100), -999)
        a = ActiveSystem()
        self.assertEqual(a.evaluate(100), 110)


if __name__ == "__main__":
    unittest.main()
