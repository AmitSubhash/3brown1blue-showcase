"""Scene 05 -- Positional Encoding

Covers: permutation-invariance problem, sinusoidal PE formula,
stacked sine-wave visualization, binary counting analogy,
embedding + PE addition, rotation/linear-transform property.
Duration target: ~90 seconds.
"""

from manim import *
import numpy as np
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.style import (
    BG_COLOR, C, SAFE_WIDTH,
    BODY_SIZE, LABEL_SIZE, EQ_SIZE, EQ_SMALL, TINY_SIZE,
    HOLD_SHORT, HOLD_MEDIUM, HOLD_LONG,
    section_title, safe_text,
)

sys.path.insert(0, os.path.dirname(__file__))
from scene_05_helpers import (
    word_row, bar_vector, build_sinusoid_elements,
    build_binary_grid, build_pe_heatmap,
)


class PositionalEncoding(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        self._part1_permutation_problem()
        self._part2_pe_formula()
        self._part3_sinusoid_viz()
        self._part4_binary_analogy()
        self._part5_addition()
        self._part6_rotation()

    def _fadeout_all(self, *mobs):
        self.play(*[FadeOut(m) for m in mobs])

    # -- Part 1: Permutation-invariance problem ----------------------------
    def _part1_permutation_problem(self):
        title = section_title("The Position Problem")
        self.play(Write(title))
        self.wait(HOLD_SHORT)

        colors = [C["query"], C["attention"], C["value"]]
        row_a = word_row(["dog", "bites", "man"], colors, 1.2)
        row_b = word_row(["man", "bites", "dog"], colors, -0.6)
        lbl_a = safe_text("Sentence A:", font_size=LABEL_SIZE, color=GRAY_B)
        lbl_a.next_to(row_a, LEFT, buff=0.4)
        lbl_b = safe_text("Sentence B:", font_size=LABEL_SIZE, color=GRAY_B)
        lbl_b.next_to(row_b, LEFT, buff=0.4)

        self.play(FadeIn(row_a, shift=RIGHT * 0.3), Write(lbl_a))
        self.play(FadeIn(row_b, shift=RIGHT * 0.3), Write(lbl_b))
        self.wait(HOLD_SHORT)

        problem = safe_text("Self-attention is permutation-invariant!",
                            font_size=BODY_SIZE, color=C["negative"])
        problem.move_to(DOWN * 2.2)
        self.play(Write(problem))
        self.wait(HOLD_MEDIUM)

        hint = safe_text("Same words -> same attention scores -> same output",
                         font_size=LABEL_SIZE, color=C["dim"])
        hint.move_to(DOWN * 2.9)
        self.play(FadeIn(hint))
        self.wait(HOLD_MEDIUM)
        self._fadeout_all(title, row_a, row_b, lbl_a, lbl_b, problem, hint)

    # -- Part 2: PE formula ------------------------------------------------
    def _part2_pe_formula(self):
        title = section_title("Positional Encoding")
        self.play(Write(title))
        self.wait(HOLD_SHORT)

        sol = safe_text(
            "Solution: inject position information into each embedding",
            font_size=BODY_SIZE, color=C["positive"])
        sol.move_to(UP * 2.0)
        self.play(Write(sol))
        self.wait(HOLD_SHORT)

        f_sin = MathTex(
            r"PE(\text{pos}, 2i) = \sin\!\left(\frac{\text{pos}}"
            r"{10000^{2i/d_{\text{model}}}}\right)",
            font_size=EQ_SMALL, color=WHITE)
        f_cos = MathTex(
            r"PE(\text{pos}, 2i{+}1) = \cos\!\left(\frac{\text{pos}}"
            r"{10000^{2i/d_{\text{model}}}}\right)",
            font_size=EQ_SMALL, color=WHITE)
        formulas = VGroup(f_sin, f_cos).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        if formulas.width > SAFE_WIDTH - 1:
            formulas.scale_to_fit_width(SAFE_WIDTH - 1)

        self.play(Write(f_sin))
        self.wait(HOLD_SHORT)
        self.play(Write(f_cos))
        self.wait(HOLD_MEDIUM)

        note = safe_text("Each dimension oscillates at a different frequency",
                         font_size=LABEL_SIZE, color=C["attention"])
        note.move_to(DOWN * 2.2)
        self.play(FadeIn(note))
        self.wait(HOLD_MEDIUM)
        self._fadeout_all(title, sol, formulas, note)

    # -- Part 3: Stacked sinusoid visualization ----------------------------
    def _part3_sinusoid_viz(self):
        title = section_title("Sinusoids at Different Frequencies")
        self.play(Write(title))
        self.wait(HOLD_SHORT)

        axes_grp, dots, labels, markers = build_sinusoid_elements(
            [0, 2, 8, 32, 128, 510])

        self.play(
            LaggedStart(*[FadeIn(m) for m in axes_grp], lag_ratio=0.05),
            LaggedStart(*[Write(l) for l in labels], lag_ratio=0.1),
            run_time=2)
        self.play(
            LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.03),
            FadeIn(markers), run_time=1.5)

        note = safe_text(
            "Each position samples a unique pattern across dimensions",
            font_size=LABEL_SIZE, color=C["highlight"])
        note.move_to(DOWN * 3.1)
        self.play(Write(note))
        self.wait(HOLD_LONG)
        self._fadeout_all(title, axes_grp, dots, labels, markers, note)

    # -- Part 4: Binary counting analogy -----------------------------------
    def _part4_binary_analogy(self):
        title = section_title("Binary Counting Analogy")
        self.play(Write(title))
        self.wait(HOLD_SHORT)

        bin_grp, bit_lbls, bt = build_binary_grid()
        pe_grp, pt = build_pe_heatmap()

        arrow = Arrow(bin_grp.get_right() + RIGHT * 0.3,
                      pe_grp.get_left() + LEFT * 0.3,
                      color=C["highlight"], buff=0.1, stroke_width=3)
        al = safe_text("continuous\nversion", font_size=TINY_SIZE,
                       color=C["highlight"])
        al.next_to(arrow, UP, buff=0.15)

        self.play(FadeIn(bin_grp, shift=UP * 0.3), Write(bt), FadeIn(bit_lbls))
        self.wait(HOLD_SHORT)
        self.play(GrowArrow(arrow), FadeIn(al),
                  FadeIn(pe_grp, shift=UP * 0.3), Write(pt), run_time=1.5)
        self.wait(HOLD_SHORT)

        an = safe_text(
            "Each bit flips at a different rate -- PE is the smooth analog",
            font_size=LABEL_SIZE, color=C["dim"])
        an.move_to(DOWN * 3.1)
        self.play(FadeIn(an))
        self.wait(HOLD_MEDIUM)
        self._fadeout_all(title, bin_grp, bt, bit_lbls, pe_grp, pt,
                          arrow, al, an)

    # -- Part 5: Embedding + PE addition -----------------------------------
    def _part5_addition(self):
        title = section_title("Adding Position to Meaning")
        self.play(Write(title))
        self.wait(HOLD_SHORT)

        np.random.seed(42)
        n = 8
        emb = np.random.uniform(0.2, 0.8, n) * \
            np.array([1, -1, 1, 1, -1, 1, -1, 1])
        pe = np.array([
            np.sin(3 * k / (10000 ** (2 * k / n))) for k in range(n)
        ]) * 0.4

        ev = bar_vector(emb, C["query"], "Embedding", -4.5)
        plus = safe_text("+", font_size=EQ_SIZE, color=WHITE)
        plus.move_to([-1.5, 0, 0])
        pv = bar_vector(pe, C["positive"], "Pos. Encoding", 0.5)
        eq = safe_text("=", font_size=EQ_SIZE, color=WHITE)
        eq.move_to([3.0, 0, 0])
        sv = bar_vector(emb + pe, C["attention"], "Position-Aware", 5.0)

        self.play(FadeIn(ev, shift=UP * 0.3))
        self.play(Write(plus))
        self.play(FadeIn(pv, shift=UP * 0.3))
        self.wait(HOLD_SHORT)
        self.play(Write(eq))
        self.play(FadeIn(sv, shift=UP * 0.3))
        self.wait(HOLD_SHORT)

        note = safe_text("Element-wise addition preserves embedding dimension",
                         font_size=LABEL_SIZE, color=C["dim"])
        note.move_to(DOWN * 3.0)
        self.play(FadeIn(note))
        self.wait(HOLD_MEDIUM)
        self._fadeout_all(title, ev, plus, pv, eq, sv, note)

    # -- Part 6: Rotation / linear transformation property -----------------
    def _part6_rotation(self):
        title = section_title("Why Sinusoids?")
        self.play(Write(title))
        self.wait(HOLD_SHORT)

        prop = MathTex(
            r"PE(\text{pos}+k) = M_k \cdot PE(\text{pos})",
            font_size=EQ_SIZE, color=C["highlight"])
        prop.move_to(UP * 1.5)
        if prop.width > SAFE_WIDTH - 1:
            prop.scale_to_fit_width(SAFE_WIDTH - 1)
        self.play(Write(prop))
        self.wait(HOLD_SHORT)

        expl = safe_text("Relative positions are a linear transformation!",
                         font_size=BODY_SIZE, color=WHITE)
        expl.move_to(UP * 0.3)
        self.play(Write(expl))
        self.wait(HOLD_SHORT)

        rot = MathTex(
            r"M_k = \begin{bmatrix}\cos(k\omega) & \sin(k\omega) \\"
            r"-\sin(k\omega) & \cos(k\omega)\end{bmatrix}",
            font_size=EQ_SMALL, color=C["encoder"])
        rot.move_to(DOWN * 1.0)
        if rot.width > SAFE_WIDTH - 2:
            rot.scale_to_fit_width(SAFE_WIDTH - 2)
        self.play(Write(rot))
        self.wait(HOLD_SHORT)

        # 2D rotation visual
        circ = Circle(radius=1.0, color=GRAY, stroke_width=1,
                      stroke_opacity=0.4)
        d1 = Dot(circ.get_center() + RIGHT, color=C["attention"], radius=0.08)
        d2 = Dot(circ.get_center() + np.array([np.cos(0.8), np.sin(0.8), 0]),
                 color=C["positive"], radius=0.08)
        arc = Arc(start_angle=0, angle=0.8, radius=1.0,
                  color=C["highlight"], stroke_width=2)
        arc.move_arc_center_to(circ.get_center())
        l1 = safe_text("PE(pos)", font_size=TINY_SIZE, color=C["attention"])
        l1.next_to(d1, RIGHT, buff=0.15)
        l2 = safe_text("PE(pos+k)", font_size=TINY_SIZE, color=C["positive"])
        l2.next_to(d2, UP + RIGHT, buff=0.1)
        rv = VGroup(circ, d1, d2, arc, l1, l2)
        rv.move_to(RIGHT * 3.5 + DOWN * 1.0)

        self.play(rot.animate.move_to(LEFT * 2.5 + DOWN * 1.0),
                  FadeIn(rv), run_time=1.5)
        self.wait(HOLD_SHORT)

        fn = safe_text("The model can learn to attend to relative positions",
                       font_size=LABEL_SIZE, color=C["dim"])
        fn.move_to(DOWN * 3.1)
        self.play(FadeIn(fn))
        self.wait(HOLD_LONG)
        self._fadeout_all(title, prop, expl, rot, rv, fn)
