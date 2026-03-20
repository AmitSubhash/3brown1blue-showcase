"""Scene 03: Little's Law -- Dim-and-reveal equation, interactive ValueTracker demo,
and rearrangement transformations."""
from manim import *

from style import *


class LittlesLaw(Scene):
    def construct(self) -> None:
        self.phase_equation_reveal()
        self.phase_interactive_demo()
        self.phase_rearrangements()

    # ------------------------------------------------------------------ #
    #  Phase 1: Dim-and-reveal equation decomposition
    # ------------------------------------------------------------------ #
    def phase_equation_reveal(self) -> None:
        title = section_title("Little's Law")
        self.play(Write(title))
        self.wait(0.5)

        # Full equation centered at y=1.0
        eq = MathTex(
            "{{I}}", "=", "{{R}}", r"\times", "{{T}}",
            font_size=EQ_SIZE,
        ).move_to(UP * 1.0)
        self.play(Write(eq), run_time=1.0)
        self.wait(0.5)

        # Dim entire equation to 30%
        self.play(eq.animate.set_opacity(0.3), run_time=0.5)

        # -- Highlight I --
        i_part = eq.get_part_by_tex("I")
        brace_i = Brace(i_part, DOWN, color=FLOW_BLUE)
        label_i = safe_text("Inventory (units in system)", font_size=LABEL_SIZE, color=FLOW_BLUE)
        label_i.next_to(brace_i, DOWN, buff=0.3)

        self.play(
            i_part.animate.set_opacity(1.0).set_color(FLOW_BLUE),
            GrowFromCenter(brace_i),
            FadeIn(label_i, shift=UP * 0.15),
            run_time=0.8,
        )
        self.wait(0.8)
        self.play(FadeOut(brace_i), FadeOut(label_i), run_time=0.4)

        # -- Highlight R --
        r_part = eq.get_part_by_tex("R")
        brace_r = Brace(r_part, DOWN, color=RATE_GREEN)
        label_r = safe_text("Flow Rate (units/time)", font_size=LABEL_SIZE, color=RATE_GREEN)
        label_r.next_to(brace_r, DOWN, buff=0.3)

        self.play(
            r_part.animate.set_opacity(1.0).set_color(RATE_GREEN),
            GrowFromCenter(brace_r),
            FadeIn(label_r, shift=UP * 0.15),
            run_time=0.8,
        )
        self.wait(0.8)
        self.play(FadeOut(brace_r), FadeOut(label_r), run_time=0.4)

        # -- Highlight T --
        t_part = eq.get_part_by_tex("T")
        brace_t = Brace(t_part, DOWN, color=TIME_ORANGE)
        label_t = safe_text("Flow Time (time in system)", font_size=LABEL_SIZE, color=TIME_ORANGE)
        label_t.next_to(brace_t, DOWN, buff=0.3)

        self.play(
            t_part.animate.set_opacity(1.0).set_color(TIME_ORANGE),
            GrowFromCenter(brace_t),
            FadeIn(label_t, shift=UP * 0.15),
            run_time=0.8,
        )
        self.wait(0.8)
        self.play(FadeOut(brace_t), FadeOut(label_t), run_time=0.4)

        # Un-dim remaining parts (= and \times) to full opacity
        equals_sign = eq.get_part_by_tex("=")
        times_sign = eq.get_part_by_tex(r"\times")
        self.play(
            equals_sign.animate.set_opacity(1.0),
            times_sign.animate.set_opacity(1.0),
            run_time=0.4,
        )
        self.wait(0.8)

        # Cleanup phase 1
        fade_all(self, title)
        self.wait(0.3)

        # Store equation for next phase
        self._eq = eq

    # ------------------------------------------------------------------ #
    #  Phase 2: Interactive parameter demo with ValueTrackers
    # ------------------------------------------------------------------ #
    def phase_interactive_demo(self) -> None:
        eq = self._eq

        # Move equation to top
        self.play(eq.animate.move_to(UP * 2.5).scale(0.85), run_time=0.6)
        self.wait(0.3)

        # ValueTrackers
        r_tracker = ValueTracker(5.0)
        t_tracker = ValueTracker(0.5)

        # -- Slider dimensions --
        slider_width = 3.0
        slider_height = 0.15

        # -- R slider (left side) --
        r_bar_bg = RoundedRectangle(
            width=slider_width, height=slider_height, corner_radius=0.05,
            color=DIMMED, fill_color=DIMMED, fill_opacity=0.4, stroke_width=1,
        ).move_to(LEFT * 3.2 + DOWN * 0.0)

        r_label = safe_text("R  (Flow Rate)", font_size=LABEL_SIZE, color=RATE_GREEN)
        r_label.next_to(r_bar_bg, UP, buff=0.4)

        r_range_lo = safe_text("2", font_size=18, color=GREY_B)
        r_range_hi = safe_text("20", font_size=18, color=GREY_B)
        r_range_lo.next_to(r_bar_bg, LEFT, buff=0.2)
        r_range_hi.next_to(r_bar_bg, RIGHT, buff=0.2)

        # R fill bar and knob (always_redraw)
        def make_r_fill() -> VGroup:
            frac = (r_tracker.get_value() - 2.0) / (20.0 - 2.0)
            fill_w = max(slider_width * frac, 0.05)
            fill = RoundedRectangle(
                width=fill_w, height=slider_height, corner_radius=0.05,
                color=RATE_GREEN, fill_color=RATE_GREEN, fill_opacity=0.7,
                stroke_width=0,
            )
            fill.align_to(r_bar_bg, LEFT)
            fill.align_to(r_bar_bg, UP)
            knob = Dot(
                fill.get_right(), radius=0.1,
                color=RATE_GREEN, fill_opacity=1.0,
            )
            val = DecimalNumber(
                r_tracker.get_value(), num_decimal_places=1,
                font_size=20, color=RATE_GREEN,
            )
            val.next_to(knob, DOWN, buff=0.25)
            return VGroup(fill, knob, val)

        r_fill = always_redraw(make_r_fill)

        # -- T slider (right side) --
        t_bar_bg = RoundedRectangle(
            width=slider_width, height=slider_height, corner_radius=0.05,
            color=DIMMED, fill_color=DIMMED, fill_opacity=0.4, stroke_width=1,
        ).move_to(RIGHT * 3.2 + DOWN * 0.0)

        t_label = safe_text("T  (Flow Time)", font_size=LABEL_SIZE, color=TIME_ORANGE)
        t_label.next_to(t_bar_bg, UP, buff=0.4)

        t_range_lo = safe_text("0.1", font_size=18, color=GREY_B)
        t_range_hi = safe_text("1.0", font_size=18, color=GREY_B)
        t_range_lo.next_to(t_bar_bg, LEFT, buff=0.2)
        t_range_hi.next_to(t_bar_bg, RIGHT, buff=0.2)

        def make_t_fill() -> VGroup:
            frac = (t_tracker.get_value() - 0.1) / (1.0 - 0.1)
            fill_w = max(slider_width * frac, 0.05)
            fill = RoundedRectangle(
                width=fill_w, height=slider_height, corner_radius=0.05,
                color=TIME_ORANGE, fill_color=TIME_ORANGE, fill_opacity=0.7,
                stroke_width=0,
            )
            fill.align_to(t_bar_bg, LEFT)
            fill.align_to(t_bar_bg, UP)
            knob = Dot(
                fill.get_right(), radius=0.1,
                color=TIME_ORANGE, fill_opacity=1.0,
            )
            val = DecimalNumber(
                t_tracker.get_value(), num_decimal_places=2,
                font_size=20, color=TIME_ORANGE,
            )
            val.next_to(knob, DOWN, buff=0.25)
            return VGroup(fill, knob, val)

        t_fill = always_redraw(make_t_fill)

        # -- I display (center, large) --
        def make_i_display() -> VGroup:
            i_val = r_tracker.get_value() * t_tracker.get_value()
            num = DecimalNumber(
                i_val, num_decimal_places=1, font_size=60, color=FLOW_BLUE,
            )
            num.move_to(DOWN * 1.6)
            i_label_inner = safe_text("I  =", font_size=HEADING_SIZE, color=FLOW_BLUE)
            i_label_inner.next_to(num, LEFT, buff=0.3)
            units = safe_text("units", font_size=LABEL_SIZE, color=GREY_B)
            units.next_to(num, RIGHT, buff=0.3)
            return VGroup(i_label_inner, num, units)

        i_display = always_redraw(make_i_display)

        # Fade in all slider elements
        self.play(
            FadeIn(r_bar_bg), FadeIn(r_label), FadeIn(r_range_lo), FadeIn(r_range_hi),
            FadeIn(t_bar_bg), FadeIn(t_label), FadeIn(t_range_lo), FadeIn(t_range_hi),
            FadeIn(r_fill), FadeIn(t_fill), FadeIn(i_display),
            run_time=0.8,
        )
        self.wait(0.5, frozen_frame=False)

        # -- Sweep R from 5 to 15, T fixed at 0.5 --
        note1 = bottom_note("Sweeping R with T fixed at 0.5")
        self.play(FadeIn(note1, shift=UP * 0.15), run_time=0.4)
        self.play(r_tracker.animate.set_value(15.0), run_time=3.0, rate_func=smooth)
        self.wait(0.8, frozen_frame=False)
        self.play(FadeOut(note1), run_time=0.3)

        # -- Sweep T from 0.2 to 1.0, R fixed at 10 --
        # First set R to 10
        self.play(r_tracker.animate.set_value(10.0), run_time=1.0, rate_func=smooth)
        self.wait(0.3, frozen_frame=False)

        # Set T to 0.2 start
        self.play(t_tracker.animate.set_value(0.2), run_time=0.6, rate_func=smooth)
        self.wait(0.3, frozen_frame=False)

        note2 = bottom_note("Sweeping T with R fixed at 10")
        self.play(FadeIn(note2, shift=UP * 0.15), run_time=0.4)
        self.play(t_tracker.animate.set_value(1.0), run_time=3.0, rate_func=smooth)
        self.wait(0.8, frozen_frame=False)
        self.play(FadeOut(note2), run_time=0.3)

        # Cleanup phase 2
        slider_group = VGroup(
            r_bar_bg, r_label, r_range_lo, r_range_hi,
            t_bar_bg, t_label, t_range_lo, t_range_hi,
        )
        fade_all(self, eq, slider_group, r_fill, t_fill, i_display)
        self.wait(0.3)

    # ------------------------------------------------------------------ #
    #  Phase 3: Rearrangements with TransformMatchingTex
    # ------------------------------------------------------------------ #
    def phase_rearrangements(self) -> None:
        title = section_title("Three Forms of Little's Law")
        self.play(Write(title))
        self.wait(0.5)

        # Form 1: I = R x T
        eq1 = MathTex(
            "{{I}}", "=", "{{R}}", r"\times", "{{T}}",
            font_size=EQ_SIZE,
        ).move_to(ORIGIN)
        eq1.get_part_by_tex("I").set_color(FLOW_BLUE)
        eq1.get_part_by_tex("R").set_color(RATE_GREEN)
        eq1.get_part_by_tex("T").set_color(TIME_ORANGE)

        self.play(Write(eq1), run_time=0.8)
        self.wait(1.0)

        # Form 2: T = I / R
        eq2 = MathTex(
            "{{T}}", "=", r"\frac{", "{{I}}", "}{", "{{R}}", "}",
            font_size=EQ_SIZE,
        ).move_to(ORIGIN)
        eq2.get_part_by_tex("T").set_color(TIME_ORANGE)
        eq2.get_part_by_tex("I").set_color(FLOW_BLUE)
        eq2.get_part_by_tex("R").set_color(RATE_GREEN)

        self.play(TransformMatchingTex(eq1, eq2), run_time=1.2)
        self.wait(1.0)

        # Form 3: R = I / T
        eq3 = MathTex(
            "{{R}}", "=", r"\frac{", "{{I}}", "}{", "{{T}}", "}",
            font_size=EQ_SIZE,
        ).move_to(ORIGIN)
        eq3.get_part_by_tex("R").set_color(RATE_GREEN)
        eq3.get_part_by_tex("I").set_color(FLOW_BLUE)
        eq3.get_part_by_tex("T").set_color(TIME_ORANGE)

        self.play(TransformMatchingTex(eq2, eq3), run_time=1.2)
        self.wait(1.0)

        # Show all three side by side
        eq_final_1 = MathTex(
            "{{I}}", "=", "{{R}}", r"\times", "{{T}}",
            font_size=SMALL_EQ,
        ).move_to(LEFT * 4.0 + DOWN * 0.5)
        eq_final_1.get_part_by_tex("I").set_color(FLOW_BLUE)
        eq_final_1.get_part_by_tex("R").set_color(RATE_GREEN)
        eq_final_1.get_part_by_tex("T").set_color(TIME_ORANGE)

        eq_final_2 = MathTex(
            "{{T}}", "=", r"\frac{", "{{I}}", "}{", "{{R}}", "}",
            font_size=SMALL_EQ,
        ).move_to(ORIGIN + DOWN * 0.5)
        eq_final_2.get_part_by_tex("T").set_color(TIME_ORANGE)
        eq_final_2.get_part_by_tex("I").set_color(FLOW_BLUE)
        eq_final_2.get_part_by_tex("R").set_color(RATE_GREEN)

        eq_final_3 = MathTex(
            "{{R}}", "=", r"\frac{", "{{I}}", "}{", "{{T}}", "}",
            font_size=SMALL_EQ,
        ).move_to(RIGHT * 4.0 + DOWN * 0.5)
        eq_final_3.get_part_by_tex("R").set_color(RATE_GREEN)
        eq_final_3.get_part_by_tex("I").set_color(FLOW_BLUE)
        eq_final_3.get_part_by_tex("T").set_color(TIME_ORANGE)

        self.play(
            ReplacementTransform(eq3, eq_final_1),
            FadeIn(eq_final_2, shift=DOWN * 0.2),
            FadeIn(eq_final_3, shift=DOWN * 0.2),
            run_time=1.0,
        )
        self.wait(0.5)

        # Bottom note
        note = bottom_note("Measure any two, get the third for free")
        self.play(FadeIn(note, shift=UP * 0.15), run_time=0.5)
        self.wait(2.0)

        # Final cleanup
        fade_all(self, title, eq_final_1, eq_final_2, eq_final_3, note)
        self.wait(0.3)
