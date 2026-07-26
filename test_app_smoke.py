import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


APP_PATH = Path(__file__).with_name("app_rg.py")


class AppSmokeTests(unittest.TestCase):
    def test_demo_profile_renders_polished_dashboard(self):
        app = AppTest.from_file(str(APP_PATH)).run(timeout=30)
        demo_button = next(button for button in app.button if "Geovany" in button.label)
        demo_button.click().run(timeout=30)

        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any("Live cohort analysis" in (item.value or "") for item in app.markdown))
        self.assertTrue(any("Human-in-loop" in (item.value or "") for item in app.markdown))
        self.assertTrue(any("TOPSIS C =" in (item.value or "") for item in app.markdown))
        self.assertTrue(any("identity-card" in (item.value or "") for item in app.markdown))
        self.assertTrue(any("Avatar sintetis" in (item.value or "") for item in app.markdown))
        self.assertTrue(any("Semarang, Jawa Tengah" in (item.value or "") for item in app.markdown))

    def test_math_view_renders_bwm_and_topsis_steps(self):
        app = AppTest.from_file(str(APP_PATH)).run(timeout=30)
        demo_button = next(button for button in app.button if "Geovany" in button.label)
        demo_button.click().run(timeout=30)
        math_button = next(button for button in app.button if button.label == "Math")
        math_button.click().run(timeout=30)

        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any("CONTEXTUAL BWM" in (item.value or "") for item in app.markdown))
        self.assertTrue(any("TOPSIS CLOSENESS" in (item.value or "") for item in app.markdown))


if __name__ == "__main__":
    unittest.main()
