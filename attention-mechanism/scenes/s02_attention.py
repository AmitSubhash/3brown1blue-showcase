"""Scene 2: Scaled Dot-Product Attention -- unified flow from intuition
through formalization to visualization. One continuous scene so elements
carry visually between sections."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.style import *


def _build_weight_grid(
    words: list[str],
    weights: list[list[float]],
    cell_size: float = 0.9,
) -> tuple[VGroup, dict[tuple[int, int], VGroup]]:
    """Build a colored grid of attention weights."""
    n = len(words)
    grid = VGroup()
    cells: dict[tuple[int, int], VGroup] = {}
    for row in range(n):
        for col in range(n):
            w = weights[row][col]
            sq = Square(side_length=cell_size)
            sq.set_fill(interpolate_color(BLACK, C["attention"], w), opacity=1)
            sq.set_stroke(WHITE, width=1)
            sq.move_to(RIGHT * col * cell_size + DOWN * row * cell_size)
            lbl = Text(f"{w:.2f}", font_size=18, color=WHITE).move_to(sq)
            cell_group = VGroup(sq, lbl)
            grid.add(cell_group)
            cells[(row, col)] = cell_group
    grid.center()
    return grid, cells


class Attention(Scene):
    """Unified attention scene: intuition -> equation -> matrix.

    Uses self.next_section() for logical breaks but keeps visual
    continuity -- elements from one phase carry into the next.
    """

    def construct(self) -> None:
        story_bridge(self, "The answer is a mechanism called Attention")

        # ── PHASE 1: Intuition ──────────────────────────────────────
        self.next_section("Intuition")

        title = Text("What is Attention?", font_size=TITLE_SIZE)
        self.play(Write(title))
        self.wait(HOLD_MEDIUM)
        self.play(title.animate.scale(0.6).to_corner(UL))

        analogy = Text(
            "When you read, you don't give equal\nweight to every word.",
            font_size=BODY_SIZE, color=C["label"],
        )
        self.play(FadeIn(analogy, shift=UP * 0.3))
        self.wait(HOLD_MEDIUM)
        self.play(FadeOut(analogy))

        # Sentence with attention lines
        words = ["The", "animal", "didn't", "cross", "the",
                 "street", "because", "it", "was", "too", "tired"]
        word_mobs = VGroup(
            *[Text(w, font_size=BODY_SIZE) for w in words]
        ).arrange(RIGHT, buff=0.25).move_to(UP * 0.5)
        self.play(Write(word_mobs))
        self.wait(HOLD_SHORT)

        it_mob = word_mobs[7]
        self.play(it_mob.animate.set_color(C["attention"]))
        self.wait(0.5)

        attn = {0: 0.15, 1: 0.95, 2: 0.20, 3: 0.25, 4: 0.10,
                5: 0.20, 6: 0.15, 8: 0.30, 9: 0.15, 10: 0.55}
        lines = VGroup()
        for idx, w in attn.items():
            lines.add(Line(
                it_mob.get_top() + UP * 0.15, word_mobs[idx].get_top() + UP * 0.15,
                stroke_width=max(1, w * 8), stroke_opacity=max(0.2, w),
                color=YELLOW if w > 0.5 else GRAY_B,
            ))
        self.play(LaggedStartMap(Create, lines, lag_ratio=0.08))
        self.wait(HOLD_SHORT)

        takeaway = Text(
            "Attention = how relevant each word is",
            font_size=BODY_SIZE, color=WHITE,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(takeaway, shift=UP * 0.3))
        self.wait(HOLD_MEDIUM)

        # TRANSITION: shrink the intuition to corner, carry the takeaway idea forward
        intuition_group = VGroup(word_mobs, lines, takeaway)
        self.play(
            FadeOut(intuition_group),
            title.animate.set_opacity(0.3),
        )

        # ── PHASE 2: Equation (dim-and-reveal) ─────────────────────
        self.next_section("Equation")

        subtitle = Text(
            "Scaled Dot-Product Attention", font_size=SUBTITLE_SIZE
        ).to_edge(UP)
        self.play(ReplacementTransform(title, subtitle))
        self.wait(0.5)

        eq = MathTex(
            r"\text{Attention}(",
            r"Q", r",", r"K", r",", r"V",
            r") = \text{softmax}\!\left(",
            r"\frac{", r"Q", r"K", r"^T",
            r"}{", r"\sqrt{d_k}", r"}", r"\right)",
            r"V",
            font_size=EQ_SIZE,
        )
        self.play(Write(eq))
        self.wait(HOLD_MEDIUM)
        self.play(eq.animate.set_opacity(0.3))
        self.wait(0.5)

        reveals = [
            ([1], C["query"], "Query: what am I looking for?"),
            ([3], C["key"], "Key: what do I contain?"),
            ([8, 9, 10], C["key"], "Dot product: how well\ndoes each key match?"),
            ([12], C["dim"], "Scale: prevent large values"),
            ([6, 14], WHITE, "Softmax: scores to probabilities"),
            ([5, 15], C["value"], "Value: content to retrieve"),
        ]
        for indices, color, label_text in reveals:
            parts = VGroup(*[eq[i] for i in indices])
            for p in parts:
                p.set_opacity(1.0)
            box = SurroundingRectangle(parts, color=color, buff=0.1)
            label = Text(label_text, font_size=LABEL_SIZE, color=color)
            label.next_to(box, DOWN, buff=0.3)
            self.play(Create(box), Write(label))
            self.wait(HOLD_SHORT)
            self.play(FadeOut(box), FadeOut(label))
            for p in parts:
                p.set_color(color)

        eq[8].set_color(C["query"])
        self.play(eq.animate.set_opacity(1.0))
        self.wait(HOLD_MEDIUM)

        # TRANSITION: shrink equation to top, carry it visually into matrix phase
        self.play(
            eq.animate.scale(0.5).to_edge(UP, buff=0.3),
            FadeOut(subtitle),
        )

        # ── PHASE 3: Attention matrix ──────────────────────────────
        self.next_section("Matrix")

        matrix_title = Text(
            "What does this look like?", font_size=SUBTITLE_SIZE, color=C["label"]
        ).next_to(eq, DOWN, buff=0.3)
        self.play(Write(matrix_title))
        self.wait(0.5)

        mat_words = ["The", "cat", "sat", "on"]
        n = len(mat_words)
        weights = [
            [0.70, 0.10, 0.10, 0.10],
            [0.05, 0.30, 0.55, 0.10],
            [0.05, 0.50, 0.30, 0.15],
            [0.10, 0.10, 0.15, 0.65],
        ]
        grid, cells = _build_weight_grid(mat_words, weights, cell_size=0.85)
        grid.shift(DOWN * 0.5)

        row_labels = VGroup(*[
            Text(mat_words[r], font_size=LABEL_SIZE, color=C["query"])
            .next_to(cells[(r, 0)], LEFT, buff=0.3) for r in range(n)
        ])
        col_labels = VGroup(*[
            Text(mat_words[c], font_size=LABEL_SIZE, color=C["key"])
            .next_to(cells[(0, c)], UP, buff=0.3) for c in range(n)
        ])

        self.play(
            LaggedStartMap(FadeIn, grid, lag_ratio=0.03),
            run_time=1.2,
        )
        self.play(Write(row_labels), Write(col_labels))
        self.wait(HOLD_SHORT)

        # Highlight cat->sat
        cat_sat = SurroundingRectangle(
            cells[(1, 2)], color=C["positive"], buff=0.02, stroke_width=4
        )
        note = Text(
            '"cat" attends to "sat" (subject-verb)',
            font_size=LABEL_SIZE, color=C["positive"],
        ).to_edge(DOWN, buff=0.4)
        self.play(Create(cat_sat), Write(note))
        self.wait(HOLD_MEDIUM)

        summary = Text(
            "Each row = one word's attention over all words",
            font_size=BODY_SIZE, color=WHITE,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeOut(cat_sat), ReplacementTransform(note, summary))
        self.wait(HOLD_LONG)

        # Clean exit
        self.play(*[FadeOut(m) for m in self.mobjects])
