"""Scene 4: Results, insights, and takeaway -- one continuous scene
flowing from evidence through explanation to legacy."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.style import *


class ResultsAndTakeaway(Scene):
    """Bar charts -> training cost -> three insights -> timeline -> final equation."""

    def construct(self) -> None:
        story_bridge(self, "Does it actually work?")

        # ── PHASE 1: BLEU Scores ────────────────────────────────────
        self.next_section("BLEU")

        title = Text("Results: State of the Art", font_size=TITLE_SIZE, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(HOLD_SHORT)

        chart = BarChart(
            values=[0, 0, 0],
            bar_names=["GNMT\n(prev. best)", "Transformer\n(base)", "Transformer\n(big)"],
            y_range=[0, 30, 5], y_length=3.5, x_length=8,
            bar_colors=[C["dim"], C["attention"], C["attention"]],
            bar_width=0.8,
        )
        chart.next_to(title, DOWN, buff=0.6)
        self.play(FadeIn(chart))
        self.play(chart.animate.change_bar_values([26.03, 27.3, 28.4]),
                  rate_func=linear, run_time=2)

        bleu_values = [26.03, 27.3, 28.4]
        vlabels = VGroup()
        for i, val in enumerate(bleu_values):
            lbl = Text(str(val), font_size=LABEL_SIZE, color=WHITE)
            lbl.next_to(chart.bars[i], UP, buff=0.1)
            vlabels.add(lbl)
        self.play(LaggedStartMap(FadeIn, vlabels, lag_ratio=0.2))
        self.wait(HOLD_MEDIUM)

        # Shrink chart left, add training cost right
        bleu_group = VGroup(chart, vlabels)
        self.play(bleu_group.animate.scale(0.55).to_edge(LEFT, buff=0.4))

        cost_title = Text("Training Cost", font_size=SUBTITLE_SIZE, color=WHITE)
        cost_title.move_to(RIGHT * 2.5 + UP * 0.8)
        self.play(Write(cost_title))

        rnn_box = labeled_box("RNN: 3 weeks", width=4.0, height=0.9, color=C["negative"])
        tf_box = labeled_box("Transformer: 3.5 days", width=2.0, height=0.9, color=C["positive"])
        rnn_box.next_to(cost_title, DOWN, buff=0.5)
        tf_box.next_to(rnn_box, DOWN, buff=0.4).align_to(rnn_box, LEFT)

        self.play(FadeIn(rnn_box, shift=LEFT * 0.5))
        self.play(FadeIn(tf_box, shift=LEFT * 0.5))
        speedup = Text("~6x faster", font_size=LABEL_SIZE, color=C["positive"])
        speedup.next_to(tf_box, RIGHT, buff=0.3)
        self.play(Write(speedup))
        self.wait(HOLD_MEDIUM)

        # TRANSITION: clear results, carry the question forward
        results_all = VGroup(title, bleu_group, cost_title, rnn_box, tf_box, speedup)
        self.play(FadeOut(results_all))

        # ── PHASE 2: Why It Works ───────────────────────────────────
        self.next_section("WhyItWorks")

        title2 = Text("Why Does This Work?", font_size=TITLE_SIZE, color=WHITE)
        title2.to_edge(UP, buff=0.5)
        self.play(Write(title2))
        self.wait(HOLD_SHORT)

        insights = VGroup()

        # Insight 1: Parallelism
        p_label = Text("1. Parallelism", font_size=SUBTITLE_SIZE, color=C["positive"])
        dots = VGroup(*[Dot(radius=0.12, color=C["dim"]) for _ in range(20)])
        dots.arrange_in_grid(4, 5, buff=0.3)
        p_group = VGroup(p_label, dots).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        self.play(FadeIn(p_label), FadeIn(dots))
        self.play(*[d.animate.set_color(C["attention"]) for d in dots], run_time=0.6)
        self.wait(HOLD_SHORT)
        self.play(p_group.animate.scale(0.45).to_edge(LEFT, buff=0.8).shift(UP * 0.5))
        insights.add(p_group)

        # Insight 2: Long-range
        lr_label = Text("2. Long-Range", font_size=SUBTITLE_SIZE, color=C["query"])
        w1 = labeled_box("word 1", width=1.2, height=0.6, color=C["input"])
        ell = Text("...", font_size=BODY_SIZE, color=C["dim"])
        w100 = labeled_box("word 100", width=1.4, height=0.6, color=C["input"])
        row = VGroup(w1, ell, w100).arrange(RIGHT, buff=0.6)
        lr_group = VGroup(lr_label, row).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        self.play(FadeIn(lr_label), FadeIn(row))
        direct = CurvedArrow(w1[0].get_top() + UP*0.1, w100[0].get_top() + UP*0.1,
                             color=C["attention"], angle=-0.5)
        dlbl = Text("Direct!", font_size=LABEL_SIZE, color=C["attention"])
        dlbl.next_to(direct, UP, buff=0.1)
        self.play(Create(direct), Write(dlbl))
        self.wait(HOLD_SHORT)
        lr_all = VGroup(lr_label, row, direct, dlbl)
        self.play(lr_all.animate.scale(0.45).move_to(ORIGIN).shift(UP * 0.5))
        insights.add(lr_all)

        # Insight 3: Learned
        at_label = Text("3. Learned", font_size=SUBTITLE_SIZE, color=C["value"])
        grid = VGroup()
        for r in [[0.8,0.1,0.05,0.05],[0.1,0.6,0.2,0.1],[0.05,0.2,0.7,0.05],[0.1,0.1,0.1,0.7]]:
            for w in r:
                sq = Square(side_length=0.45, stroke_width=1, stroke_color=WHITE)
                sq.set_fill(C["attention"], opacity=w)
                grid.add(sq)
        grid.arrange_in_grid(4, 4, buff=0.05)
        at_group = VGroup(at_label, grid).arrange(DOWN, buff=0.3).move_to(ORIGIN)
        self.play(FadeIn(at_label), LaggedStartMap(FadeIn, grid, lag_ratio=0.03, run_time=0.8))
        self.wait(HOLD_SHORT)
        self.play(at_group.animate.scale(0.45).to_edge(RIGHT, buff=0.8).shift(UP * 0.5))
        insights.add(at_group)

        self.wait(HOLD_MEDIUM)

        # TRANSITION: carry insights to takeaway
        self.play(FadeOut(title2), FadeOut(insights))

        # ── PHASE 3: Takeaway ───────────────────────────────────────
        self.next_section("Takeaway")

        title3 = Text("The Legacy", font_size=TITLE_SIZE, color=WHITE)
        title3.to_edge(UP, buff=0.5)
        self.play(Write(title3))
        self.wait(HOLD_SHORT)

        timeline = [
            "2017: Transformer introduced",
            "2018: BERT (encoder for understanding)",
            "2019: GPT-2 (decoder for generation)",
            "2020-2025: GPT-4, Claude, Gemini... all Transformers",
        ]
        current = Text(timeline[0], font_size=BODY_SIZE, color=C["label"])
        current.next_to(title3, DOWN, buff=1.5)
        self.play(Write(current))
        self.wait(HOLD_SHORT)
        for line in timeline[1:]:
            nxt = Text(line, font_size=BODY_SIZE, color=C["label"]).move_to(current)
            self.play(ReplacementTransform(current, nxt))
            self.wait(HOLD_SHORT)
            current = nxt
        self.play(FadeOut(current))

        # Final equation
        eq = MathTex(
            r"\text{Attention}(", r"Q", r",", r"K", r",", r"V",
            r") = \text{softmax}\!\left(\frac{",
            r"Q", r"K", r"^T}{\sqrt{d_k}}\right)", r"V",
            font_size=EQ_SIZE,
        )
        eq.set_color_by_tex("Q", C["query"])
        eq.set_color_by_tex("K", C["key"])
        eq.set_color_by_tex("V", C["value"])
        eq.next_to(title3, DOWN, buff=1.2)
        self.play(Write(eq, run_time=2))

        rect = SurroundingRectangle(eq, color=C["attention"], buff=0.2,
                                    corner_radius=0.1, stroke_width=3)
        self.play(Create(rect))

        closing = Text("One equation. An entire field transformed.",
                       font_size=SUBTITLE_SIZE, color=C["attention"])
        closing.next_to(rect, DOWN, buff=0.8)
        self.play(Write(closing))
        self.wait(HOLD_LONG)

        self.play(*[FadeOut(m) for m in self.mobjects])
