import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "flet_circular_slider" / "src"))

from flet_circular_slider import FletCircularSlider
from flet_circular_slider.flet_circular_slider import _canonical_key


def build(**kwargs):
    slider = FletCircularSlider(**kwargs)
    slider.before_update()
    return slider


class CanonicalKeyTests(unittest.TestCase):
    def test_integer_values_drop_decimal(self):
        self.assertEqual(_canonical_key(50.0), "50")
        self.assertEqual(_canonical_key(0.0), "0")

    def test_fractional_values_trim_trailing_zeros(self):
        self.assertEqual(_canonical_key(2.5), "2.5")
        self.assertEqual(_canonical_key(0.30000000000), "0.3")


class ValidationTests(unittest.TestCase):
    def test_defaults_pass_validation(self):
        build()

    def test_min_must_be_less_than_max(self):
        with self.assertRaisesRegex(ValueError, "min"):
            build(min=10, max=10)

    def test_value_clamped_to_range(self):
        self.assertEqual(build(min=0, max=100, value=250).value, 100)
        self.assertEqual(build(min=0, max=100, value=-5).value, 0)

    def test_rejects_out_of_range_properties(self):
        bad = [
            {"divisions": 0},
            {"size": 0},
            {"start_angle": 360},
            {"angle_range": 0},
            {"angle_range": 361},
            {"anim_duration_multiplier": 0},
            {"change_throttle_ms": 0},
            {"progress_bar_width": -1},
            {"track_width": 0},
            {"handler_size": 0},
            {"shadow_width": 0},
            {"inner_text_size": 0},
        ]
        for kwargs in bad:
            with self.assertRaises(ValueError, msg=str(kwargs)):
                build(**kwargs)

    def test_font_weight_validation(self):
        build(inner_text_font_weight="w300", top_label_font_weight="bold")
        with self.assertRaisesRegex(ValueError, "inner_text_font_weight"):
            build(inner_text_font_weight="heavy")

    def test_progress_bar_colors_needs_at_least_two(self):
        build(progress_bar_colors=["red", "blue"])
        with self.assertRaisesRegex(ValueError, "at least 2"):
            build(progress_bar_colors=["red"])


class LabelFormatterTests(unittest.TestCase):
    def test_requires_divisions(self):
        with self.assertRaisesRegex(ValueError, "divisions"):
            build(label_formatter=str)

    def test_mutually_exclusive_with_label_map(self):
        with self.assertRaisesRegex(ValueError, "mutually exclusive"):
            build(divisions=2, label_formatter=str, label_map={"0": "zero"})

    def test_builds_label_map_with_canonical_keys(self):
        slider = build(min=0, max=10, divisions=2, label_formatter=lambda v: f"{v:g}u")
        self.assertEqual(slider.label_map, {"0": "0u", "5": "5u", "10": "10u"})

    def test_formatter_errors_are_wrapped(self):
        def boom(_v):
            raise KeyError("missing")

        with self.assertRaisesRegex(ValueError, "label_formatter raised KeyError"):
            build(min=0, max=10, divisions=2, label_formatter=boom)


if __name__ == "__main__":
    unittest.main()
