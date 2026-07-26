import copy
import unittest

import numpy as np

from score_engine import (
    calculate_environmental_score,
    classify_pathway,
    derive_contextual_weights,
    reference_anchored_topsis,
    review_status,
    score_debtor_cohort,
    sensitivity_grid,
    solve_bwm,
)


def make_debtor(scores, esg, available, activity="agri", claim_match=True):
    keys = ("transaction_history", "digital_payments", "financial_statements", "credit_bureau")
    return {
        "activity_type": activity,
        "data_availability": {key: i < available for i, key in enumerate(keys)},
        "5C": scores,
        "ESG": esg,
        "geo": {
            "ndvi": 0.70 if claim_match else 0.10,
            "claim_match": claim_match,
            "flood_score": 80,
            "land_class": "agri" if claim_match else "empty",
            "protected_zone_ok": claim_match,
            "proximity_m": 100,
        },
    }


class BWMTests(unittest.TestCase):
    def test_bwm_solves_a_consistent_two_criterion_case(self):
        result = solve_bwm(
            ["Credit", "ESG"], "Credit", "ESG", [1, 2], [2, 1]
        )
        np.testing.assert_allclose(result["weights"], [2 / 3, 1 / 3], atol=1e-7)
        self.assertAlmostEqual(result["xi"], 0.0)

    def test_context_changes_bwm_weights_without_applicant_specific_tuning(self):
        thin = derive_contextual_weights(True)
        rich = derive_contextual_weights(False)
        self.assertGreater(thin["top_weights"][0], thin["top_weights"][1])
        self.assertLess(rich["top_weights"][0], rich["top_weights"][1])
        self.assertEqual(int(np.argmax(thin["credit_weights"])), 0)
        self.assertEqual(int(np.argmax(rich["credit_weights"])), 1)
        self.assertAlmostEqual(float(thin["global_weights"].sum()), 1.0)
        self.assertAlmostEqual(float(rich["global_weights"].sum()), 1.0)


class TOPSISTests(unittest.TestCase):
    def test_reference_anchors_are_zero_and_one(self):
        result = reference_anchored_topsis([[20, 20], [80, 80]], [0.5, 0.5])
        self.assertEqual(result["anchor_scores"], (0.0, 1.0))
        np.testing.assert_allclose(result["scores"], [0.2, 0.8], atol=1e-4)

    def test_dominant_profile_ranks_higher(self):
        result = reference_anchored_topsis(
            [[40, 50, 60], [70, 80, 90]], [0.3, 0.4, 0.3]
        )
        self.assertGreater(result["scores"][1], result["scores"][0])

    def test_invalid_values_outside_policy_anchors_are_rejected(self):
        with self.assertRaises(ValueError):
            reference_anchored_topsis([[101, 50]], [0.5, 0.5])


class CohortEngineTests(unittest.TestCase):
    def setUp(self):
        self.debtors = {
            "thin_high": make_debtor([90, 80, 70, 75, 50], [70, 85, 55], 1),
            "thin_low": make_debtor([20, 30, 25, 35, 10], [20, 30, 15], 0, claim_match=False),
            "rich": make_debtor([65, 90, 80, 75, 85], [65, 75, 80], 4, activity="urban"),
        }

    def test_pathway_is_derived_from_available_data(self):
        self.assertEqual(classify_pathway(self.debtors["rich"]), (False, 4))

    def test_cohort_scores_are_bounded_and_ranked_within_pathway(self):
        scores = score_debtor_cohort(self.debtors)
        self.assertEqual(scores["thin_high"]["cohort_size"], 2)
        self.assertEqual(scores["rich"]["cohort_size"], 1)
        self.assertEqual(scores["thin_high"]["rank"], 1)
        self.assertEqual(scores["thin_low"]["rank"], 2)
        for result in scores.values():
            self.assertTrue(0 <= result["vi"] <= 1)
            self.assertTrue(0 <= result["esg"] <= 1)
            self.assertTrue(0 <= result["fcs"] <= 1)

    def test_rural_proximity_is_context_not_score(self):
        near = copy.deepcopy(self.debtors["thin_high"])
        far = copy.deepcopy(near)
        far["geo"]["proximity_m"] = 10000
        self.assertEqual(calculate_environmental_score(near), calculate_environmental_score(far))

    def test_contradictory_geospatial_claim_lowers_environmental_score(self):
        consistent = self.debtors["thin_high"]
        contradictory = self.debtors["thin_low"]
        self.assertGreater(
            calculate_environmental_score(consistent)[0],
            calculate_environmental_score(contradictory)[0],
        )

    def test_sensitivity_grid_recalculates_topsis(self):
        scores = score_debtor_cohort(self.debtors)
        ids = ["thin_high", "thin_low"]
        matrix = np.vstack([scores[item]["criteria"] for item in ids])
        rows = sensitivity_grid(matrix, scores["thin_high"]["global_weights"], 0)
        self.assertEqual(len(rows), matrix.shape[1] * 2)
        self.assertTrue(all(0 <= row["score"] <= 1 for row in rows))

    def test_status_is_human_review_language(self):
        self.assertIn("TINJAUAN MANUAL", review_status(0.2)[1])


if __name__ == "__main__":
    unittest.main()
