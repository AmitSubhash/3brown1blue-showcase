"""Scene 03: Scaled Dot-Product Attention.

Builds the attention formula step by step, then shows *why*
we divide by sqrt(d_k) using a side-by-side softmax comparison.
Duration target: ~90 seconds.
"""

from manim import *
import numpy as np
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.style import (
    BG_COLOR, C, TITLE_Y, SUBTITLE_Y, BOTTOM_Y,
    TITLE_SIZE, SUBTITLE_SIZE, BODY_SIZE, LABEL_SIZE, EQ_SIZE, EQ_SMALL,
    TINY_SIZE, SAFE_WIDTH, SAFE_X, SAFE_Y,
    LEFT_CENTER, RIGHT_CENTER, PANEL_WIDTH,
    HOLD_SHORT, HOLD_MEDIUM, HOLD_LONG, DIM_OPACITY,
    section_title, subtitle, body_text, safe_text, bottom_note,
    labeled_box, story_bridge,
)


# ------------------------------------------------------------------ helpers
def softmax(x: np.ndarray) -> np.ndarray:
    """Numerically stable softmax."""
    e = np.exp(x - x.max())
    return e / e.sum()


def _make_attention_grid(
    n: int, values: np.ndarray, cell_size: float = 0.55
) -> VGroup:
    """Create an n x n grid of cells colored by value magnitude."""
    grid = VGroup()
    for i in range(n):
        for j in range(n):
            v = values[i, j]
            intensity = float(np.clip(abs(v) / 3.0, 0, 1))
            fill_c = interpolate_color(
                ManimColor(BG_COLOR), ManimColor(C["attention"]), intensity
            )
            sq = Square(side_length=cell_size)
            sq.set_fill(fill_c, opacity=0.85)
            sq.set_stroke(WHITE, width=0.5)
            sq.move_to(
                RIGHT * (j - n / 2 + 0.5) * cell_size
                + DOWN * (i - n / 2 + 0.5) * cell_size,
            )
            num_label = Text(
                f"{v:.1f}", font_size=14, color=WHITE
            ).move_to(sq)
            cell = VGroup(sq, num_label)
            grid.add(cell)
    return grid


# ================================================================== Scene
class ScaledDotProductAttention(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        self._phase1_formula()
        self._phase2_step_through()
        self._phase3_why_scale()
        self._phase4_temperature()

    # ---------------------------------------------------------------- P1
    def _phase1_formula(self):
        """Show the full attention formula front and center."""
        title = section_title("Scaled Dot-Product Attention")
        self.play(Write(title), run_time=1.0)
        self.wait(HOLD_SHORT)

        formula = MathTex(
            r"\text{Attention}(Q, K, V)",
            r"=",
            r"\text{softmax}\!\left(",
            r"\frac{Q K^\top}{\sqrt{d_k}}",
            r"\right)",
            r"\cdot V",
            font_size=EQ_SIZE,
        )
        formula[0][10:11].set_color(C["query"])   # Q
        formula[0][12:13].set_color(C["key"])      # K
        formula[0][14:15].set_color(C["value"])    # V
        formula[3][0:1].set_color(C["query"])      # Q in fraction
        formula[3][1:3].set_color(C["key"])        # K^T
        formula[5][1:2].set_color(C["value"])      # V
        formula.move_to(ORIGIN)
        if formula.width > SAFE_WIDTH:
            formula.scale_to_fit_width(SAFE_WIDTH)

        self.play(Write(formula), run_time=2.5)
        self.wait(HOLD_MEDIUM)

        # Store refs for next phase
        self.title_mob = title
        self.formula_mob = formula

    # ---------------------------------------------------------------- P2
    def _phase2_step_through(self):
        """Highlight each component of the formula and show visuals."""
        formula = self.formula_mob

        # Shrink formula to top region
        formula_target = formula.copy().scale(0.75).move_to(UP * 2.2)
        self.play(
            FadeOut(self.title_mob, shift=UP * 0.5),
            ReplacementTransform(formula, formula_target),
            run_time=1.0,
        )
        formula = formula_target

        # --- Step A: QK^T dot product grid ---
        step_label = safe_text(
            "Step 1: Compute QK^T (dot products)",
            font_size=LABEL_SIZE, color=C["attention"],
        ).move_to(UP * 1.2)
        self.play(Write(step_label), run_time=0.8)

        np.random.seed(42)
        n = 5
        raw_dots = np.random.randn(n, n) * 2.5
        grid = _make_attention_grid(n, raw_dots, cell_size=0.6)
        grid.move_to(DOWN * 0.8)

        # Row / col labels
        q_labels = VGroup()
        k_labels = VGroup()
        for i in range(n):
            ql = Text(f"q{i+1}", font_size=14, color=C["query"])
            ql.next_to(grid[i * n], LEFT, buff=0.2)
            q_labels.add(ql)
        for j in range(n):
            kl = Text(f"k{j+1}", font_size=14, color=C["key"])
            kl.next_to(grid[j], UP, buff=0.2)
            k_labels.add(kl)

        # Animate cells appearing row by row
        for row in range(n):
            row_cells = VGroup(*[grid[row * n + c] for c in range(n)])
            self.play(
                FadeIn(row_cells, shift=DOWN * 0.15),
                run_time=0.3,
            )
        self.play(FadeIn(q_labels), FadeIn(k_labels), run_time=0.5)
        self.wait(HOLD_SHORT)

        # --- Step B: divide by sqrt(d_k) ---
        step_b_label = safe_text(
            "Step 2: Scale by 1/sqrt(d_k)",
            font_size=LABEL_SIZE, color=C["highlight"],
        ).move_to(UP * 1.2)
        scaled_dots = raw_dots / 8.0  # sqrt(64) = 8
        scaled_grid = _make_attention_grid(n, scaled_dots, cell_size=0.6)
        scaled_grid.move_to(DOWN * 0.8)

        self.play(
            ReplacementTransform(step_label, step_b_label),
            ReplacementTransform(grid, scaled_grid),
            run_time=1.2,
        )
        self.wait(HOLD_SHORT)

        # --- Step C: softmax row normalization ---
        step_c_label = safe_text(
            "Step 3: Softmax (rows sum to 1)",
            font_size=LABEL_SIZE, color=C["positive"],
        ).move_to(UP * 1.2)

        sm_vals = np.zeros_like(scaled_dots)
        for i in range(n):
            sm_vals[i] = softmax(scaled_dots[i])
        sm_grid = _make_attention_grid(n, sm_vals * 3, cell_size=0.6)
        sm_grid.move_to(DOWN * 0.8)

        # Add row sum annotations
        sum_labels = VGroup()
        for i in range(n):
            s = Text("= 1.0", font_size=12, color=C["positive"])
            s.next_to(sm_grid[i * n + (n - 1)], RIGHT, buff=0.2)
            sum_labels.add(s)

        self.play(
            ReplacementTransform(step_b_label, step_c_label),
            ReplacementTransform(scaled_grid, sm_grid),
            run_time=1.2,
        )
        self.play(FadeIn(sum_labels, shift=RIGHT * 0.1), run_time=0.5)
        self.wait(HOLD_SHORT)

        # --- Step D: multiply by V ---
        step_d_label = safe_text(
            "Step 4: Weighted sum of Value vectors",
            font_size=LABEL_SIZE, color=C["value"],
        ).move_to(UP * 1.2)

        v_vecs = VGroup()
        for j in range(n):
            rect = Rectangle(
                width=0.45, height=2.0,
                fill_color=C["value"], fill_opacity=0.3,
                stroke_color=C["value"], stroke_width=1.5,
            )
            lbl = Text(f"v{j+1}", font_size=14, color=C["value"])
            lbl.move_to(rect)
            col = VGroup(rect, lbl)
            col.next_to(sm_grid[j], DOWN, buff=0.45)
            v_vecs.add(col)
        v_vecs.move_to(DOWN * 2.8)

        times_sign = MathTex(r"\times", font_size=28, color=WHITE)
        times_sign.move_to(DOWN * 1.9)

        self.play(
            ReplacementTransform(step_c_label, step_d_label),
            FadeIn(times_sign),
            FadeIn(v_vecs, shift=DOWN * 0.2),
            run_time=1.0,
        )
        self.wait(HOLD_MEDIUM)

        # Clear phase 2
        self.play(
            *[FadeOut(m) for m in [
                formula, step_d_label, sm_grid, q_labels,
                k_labels, sum_labels, v_vecs, times_sign,
            ]],
            run_time=0.8,
        )

    # ---------------------------------------------------------------- P3
    def _phase3_why_scale(self):
        """Dual-panel: unscaled vs. scaled dot products through softmax."""
        title = section_title("Why Scale by sqrt(d_k)?")
        self.play(Write(title), run_time=1.0)
        self.wait(0.5)

        # Divider line
        divider = DashedLine(
            UP * 2.2, DOWN * 3.0, color=GRAY, stroke_width=1
        )
        self.play(Create(divider), run_time=0.4)

        # Panel headers
        left_hdr = safe_text(
            "Unscaled", font_size=SUBTITLE_SIZE, color=C["negative"],
        ).move_to(LEFT * abs(LEFT_CENTER) + UP * 2.2)
        right_hdr = safe_text(
            "Scaled (/ sqrt(d_k))", font_size=SUBTITLE_SIZE,
            color=C["positive"],
        ).move_to(RIGHT * abs(RIGHT_CENTER) + UP * 2.2)
        self.play(Write(left_hdr), Write(right_hdr), run_time=0.8)

        # Build softmax curves
        x_range_vals = np.linspace(-5, 5, 200)
        sm_curve = 1 / (1 + np.exp(-x_range_vals))  # sigmoid as proxy

        # Left axes (unscaled)
        left_ax = Axes(
            x_range=[-5, 5, 2.5], y_range=[0, 1, 0.5],
            x_length=4.2, y_length=2.2,
            axis_config={"color": GRAY_B, "stroke_width": 1.5},
            tips=False,
        ).move_to(LEFT * abs(LEFT_CENTER) + DOWN * 0.2)

        left_curve = left_ax.plot(
            lambda x: 1 / (1 + np.exp(-x)), color=C["attention"],
        )
        left_ax_label = safe_text(
            "softmax input", font_size=TINY_SIZE, color=GRAY_B,
        ).next_to(left_ax, DOWN, buff=0.15)

        # Right axes (scaled)
        right_ax = Axes(
            x_range=[-5, 5, 2.5], y_range=[0, 1, 0.5],
            x_length=4.2, y_length=2.2,
            axis_config={"color": GRAY_B, "stroke_width": 1.5},
            tips=False,
        ).move_to(RIGHT * abs(RIGHT_CENTER) + DOWN * 0.2)

        right_curve = right_ax.plot(
            lambda x: 1 / (1 + np.exp(-x)), color=C["attention"],
        )
        right_ax_label = safe_text(
            "softmax input", font_size=TINY_SIZE, color=GRAY_B,
        ).next_to(right_ax, DOWN, buff=0.15)

        self.play(
            Create(left_ax), Create(right_ax),
            Create(left_curve), Create(right_curve),
            Write(left_ax_label), Write(right_ax_label),
            run_time=1.5,
        )

        # Unscaled dots: land in the saturated tails
        unscaled_points = [-4.2, -3.5, 3.8, 4.5, -4.0]
        left_dots = VGroup()
        for val in unscaled_points:
            clamped = np.clip(val, -5, 5)
            y = 1 / (1 + np.exp(-clamped))
            dot = Dot(
                left_ax.c2p(clamped, y),
                radius=0.07, color=C["negative"],
            )
            left_dots.add(dot)

        # Scaled dots: land in the informative middle
        scaled_points = [-1.2, -0.5, 0.8, 1.5, -0.3]
        right_dots = VGroup()
        for val in scaled_points:
            y = 1 / (1 + np.exp(-val))
            dot = Dot(
                right_ax.c2p(val, y),
                radius=0.07, color=C["positive"],
            )
            right_dots.add(dot)

        self.play(
            FadeIn(left_dots, scale=0.5),
            FadeIn(right_dots, scale=0.5),
            run_time=1.0,
        )
        self.wait(HOLD_SHORT)

        # Result distributions
        left_dist_label = safe_text(
            "Near one-hot", font_size=LABEL_SIZE, color=C["negative"],
        ).move_to(LEFT * abs(LEFT_CENTER) + DOWN * 2.0)
        left_bar_vals = softmax(np.array(unscaled_points))
        left_bars = self._mini_bar_chart(
            left_bar_vals, C["negative"],
        ).move_to(LEFT * abs(LEFT_CENTER) + DOWN * 2.7)

        right_dist_label = safe_text(
            "Smooth distribution", font_size=LABEL_SIZE, color=C["positive"],
        ).move_to(RIGHT * abs(RIGHT_CENTER) + DOWN * 2.0)
        right_bar_vals = softmax(np.array(scaled_points))
        right_bars = self._mini_bar_chart(
            right_bar_vals, C["positive"],
        ).move_to(RIGHT * abs(RIGHT_CENTER) + DOWN * 2.7)

        self.play(
            Write(left_dist_label), Write(right_dist_label),
            FadeIn(left_bars, shift=UP * 0.15),
            FadeIn(right_bars, shift=UP * 0.15),
            run_time=1.2,
        )
        self.wait(HOLD_SHORT)

        # Gradient labels
        left_grad = safe_text(
            "Vanishing gradients", font_size=TINY_SIZE, color=C["negative"],
        ).next_to(left_bars, DOWN, buff=0.2)
        right_grad = safe_text(
            "Healthy gradients", font_size=TINY_SIZE, color=C["positive"],
        ).next_to(right_bars, DOWN, buff=0.2)
        self.play(Write(left_grad), Write(right_grad), run_time=0.7)
        self.wait(HOLD_MEDIUM)

        # Math note at bottom
        math_note = MathTex(
            r"\text{If } q_i, k_i \sim \mathcal{N}(0,1) \implies"
            r"\text{Var}(q \cdot k) = d_k",
            font_size=EQ_SMALL - 4,
            color=GRAY_B,
        )
        math_note.move_to(DOWN * abs(BOTTOM_Y) + UP * 0.15)
        if math_note.width > SAFE_WIDTH:
            math_note.scale_to_fit_width(SAFE_WIDTH)
        self.play(Write(math_note), run_time=1.0)
        self.wait(HOLD_MEDIUM)

        # Collect everything on screen for cleanup
        self.phase3_mobs = VGroup(
            title, divider, left_hdr, right_hdr,
            left_ax, left_curve, left_ax_label,
            right_ax, right_curve, right_ax_label,
            left_dots, right_dots,
            left_dist_label, left_bars,
            right_dist_label, right_bars,
            left_grad, right_grad, math_note,
        )

    # ---------------------------------------------------------------- P4
    def _phase4_temperature(self):
        """Temperature analogy: thermometer from 'too hot' to 'just right'."""
        self.play(FadeOut(self.phase3_mobs), run_time=0.8)

        title = section_title("The Temperature Analogy")
        self.play(Write(title), run_time=0.8)

        # Thermometer: a vertical rounded rect with fill
        therm_outline = RoundedRectangle(
            width=0.7, height=3.5, corner_radius=0.35,
            stroke_color=WHITE, stroke_width=2,
            fill_opacity=0,
        ).move_to(ORIGIN)

        # Mercury fill (animated)
        mercury_hot = RoundedRectangle(
            width=0.5, height=3.1, corner_radius=0.25,
            fill_color=RED, fill_opacity=0.9, stroke_width=0,
        ).move_to(therm_outline)

        mercury_right = RoundedRectangle(
            width=0.5, height=1.5, corner_radius=0.25,
            fill_color=C["positive"], fill_opacity=0.9, stroke_width=0,
        ).align_to(therm_outline, DOWN).shift(UP * 0.2)

        # Labels
        hot_label = safe_text(
            '"Too hot" (one-hot)', font_size=LABEL_SIZE, color=RED,
        ).next_to(therm_outline, RIGHT, buff=0.8).shift(UP * 0.8)

        right_label = safe_text(
            '"Just right" (soft)', font_size=LABEL_SIZE, color=C["positive"],
        ).next_to(therm_outline, RIGHT, buff=0.8).shift(DOWN * 0.3)

        # Temperature scale marks
        ticks = VGroup()
        for frac, label_text in [(0.85, "High T"), (0.35, "Low T")]:
            y_pos = therm_outline.get_bottom()[1] + frac * 3.5
            tick = Line(
                therm_outline.get_left() + LEFT * 0.15 + UP * (y_pos - therm_outline.get_center()[1]),
                therm_outline.get_left() + UP * (y_pos - therm_outline.get_center()[1]),
                color=GRAY_B, stroke_width=1.5,
            )
            tick_lbl = safe_text(
                label_text, font_size=14, color=GRAY_B,
            ).next_to(tick, LEFT, buff=0.1)
            ticks.add(VGroup(tick, tick_lbl))

        # Show hot state
        self.play(
            FadeIn(therm_outline),
            FadeIn(mercury_hot),
            Write(hot_label),
            FadeIn(ticks),
            run_time=1.2,
        )
        self.wait(HOLD_SHORT)

        # Mini one-hot bar chart next to hot label
        one_hot_vals = np.array([0.98, 0.005, 0.005, 0.005, 0.005])
        one_hot_bars = self._mini_bar_chart(
            one_hot_vals, RED, bar_width=0.2, max_height=1.0,
        ).next_to(hot_label, DOWN, buff=0.3)
        self.play(FadeIn(one_hot_bars, shift=UP * 0.1), run_time=0.6)
        self.wait(HOLD_SHORT)

        # Animate mercury going down
        self.play(
            ReplacementTransform(mercury_hot, mercury_right),
            Write(right_label),
            run_time=1.5,
        )

        # Mini smooth bar chart
        smooth_vals = softmax(np.array([1.2, 0.8, -0.3, 0.5, -0.5]))
        smooth_bars = self._mini_bar_chart(
            smooth_vals, C["positive"], bar_width=0.2, max_height=1.0,
        ).next_to(right_label, DOWN, buff=0.3)
        self.play(FadeIn(smooth_bars, shift=UP * 0.1), run_time=0.6)
        self.wait(HOLD_SHORT)

        # Bottom note
        note = bottom_note(
            "Scaling = controlling the 'temperature' of attention"
        )
        self.play(Write(note), run_time=0.8)
        self.wait(HOLD_LONG)

        # Final fade
        self.play(
            *[FadeOut(m) for m in self.mobjects],
            run_time=1.0,
        )

    # ----------------------------------------------------------- utilities
    def _mini_bar_chart(
        self,
        values: np.ndarray,
        color,
        bar_width: float = 0.3,
        max_height: float = 0.8,
    ) -> VGroup:
        """Simple bar chart from an array of probabilities."""
        bars = VGroup()
        n = len(values)
        for i, v in enumerate(values):
            h = max(float(v) * max_height / max(values), 0.04)
            bar = Rectangle(
                width=bar_width, height=h,
                fill_color=color, fill_opacity=0.8,
                stroke_color=color, stroke_width=1,
            )
            bar.move_to(
                RIGHT * (i - n / 2 + 0.5) * (bar_width + 0.08)
            )
            bar.align_to(ORIGIN, DOWN)
            bars.add(bar)
        return bars
