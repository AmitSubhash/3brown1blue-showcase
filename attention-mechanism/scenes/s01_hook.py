"""Scene 1: Hook and Problem -- Attention Is All You Need explainer."""

from pathlib import Path

from manim import *

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.style import *


class Hook(Scene):
    """Punchline first: sequential vs parallel processing."""

    def construct(self) -> None:
        # -- Punchline question --
        question = Text(
            "What if we could translate languages...\n"
            "without reading words one at a time?",
            font_size=BODY_SIZE, color=C["label"], line_spacing=1.4,
        )
        self.play(Write(question, run_time=2))
        self.wait(HOLD_MEDIUM)
        self.play(FadeOut(question))
        self.wait(HOLD_SHORT)

        # -- Sequential processing (RNN): boxes revealed one at a time --
        seq_label = Text("RNN: Sequential", font_size=SUBTITLE_SIZE, color=C["dim"])
        seq_label.to_edge(UP, buff=0.6)
        self.play(Write(seq_label))

        rnn_boxes = VGroup(*[
            labeled_box(f"w{i+1}", width=1.0, height=0.8, color=C["encoder"])
            for i in range(5)
        ]).arrange(RIGHT, buff=0.8).next_to(seq_label, DOWN, buff=1.0)

        self.play(FadeIn(rnn_boxes[0], shift=UP * 0.3))
        rnn_arrows = VGroup()
        for i in range(1, len(rnn_boxes)):
            arrow = Arrow(
                rnn_boxes[i - 1][0].get_right(), rnn_boxes[i][0].get_left(),
                buff=0.08, color=WHITE, stroke_width=2,
            )
            rnn_arrows.add(arrow)
            self.play(GrowArrow(arrow), FadeIn(rnn_boxes[i], shift=UP * 0.3), run_time=0.6)

        # Cursor sweep: emphasize one-at-a-time bottleneck
        cursor = Triangle(color=C["attention"], fill_opacity=1).scale(0.15)
        cursor.rotate(PI).next_to(rnn_boxes[0], DOWN, buff=0.3)
        self.play(FadeIn(cursor, scale=0.5))
        for i in range(1, len(rnn_boxes)):
            self.play(
                cursor.animate.next_to(rnn_boxes[i], DOWN, buff=0.3),
                rnn_boxes[i][0].animate.set_fill(C["attention"], opacity=0.35),
                run_time=0.5,
            )
        slow_text = Text("Slow...", font_size=LABEL_SIZE, color=C["negative"])
        slow_text.next_to(rnn_boxes, DOWN, buff=0.8)
        self.play(Write(slow_text))
        self.wait(HOLD_SHORT)

        # -- Transition to parallel processing --
        self.play(FadeOut(VGroup(seq_label, rnn_boxes, rnn_arrows, cursor, slow_text)))

        par_label = Text("Transformer: Parallel", font_size=SUBTITLE_SIZE, color=C["attention"])
        par_label.to_edge(UP, buff=0.6)
        self.play(Write(par_label))

        par_boxes = VGroup(*[
            labeled_box(f"w{i+1}", width=1.0, height=0.8, color=C["input"])
            for i in range(5)
        ]).arrange(RIGHT, buff=0.8).next_to(par_label, DOWN, buff=1.0)

        # All boxes appear near-simultaneously, then light up together
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.3) for b in par_boxes], lag_ratio=0.08))
        self.wait(FADE_FAST)
        self.play(*[b[0].animate.set_fill(C["attention"], opacity=0.5) for b in par_boxes], run_time=0.4)
        fast_text = Text("All at once!", font_size=LABEL_SIZE, color=C["positive"])
        fast_text.next_to(par_boxes, DOWN, buff=0.8)
        self.play(Write(fast_text))
        self.wait(HOLD_MEDIUM)

        # -- Closing statement --
        self.play(FadeOut(VGroup(par_label, par_boxes, fast_text)))
        closing = Text(
            "This is the Transformer.\nIt changed everything.",
            font_size=SUBTITLE_SIZE, color=WHITE, line_spacing=1.4,
        )
        self.play(Write(closing, run_time=1.5))
        self.wait(HOLD_LONG)
        self.play(FadeOut(closing))


class Problem(Scene):
    """Why sequential models are a bottleneck."""

    def construct(self) -> None:
        story_bridge(self, "But first... why do we need a new architecture?")

        title = Text("The Problem with Sequential Models", font_size=TITLE_SIZE, color=WHITE)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(HOLD_SHORT)

        # -- Sentence as individual word boxes --
        words = ["The", "cat", "sat", "on", "the", "mat"]
        word_boxes = VGroup(*[
            labeled_box(w, width=1.2, height=0.7, color=C["input"]) for w in words
        ]).arrange(RIGHT, buff=0.35).next_to(title, DOWN, buff=1.0)

        self.play(LaggedStart(
            *[FadeIn(b, shift=UP * 0.3) for b in word_boxes],
            lag_ratio=0.1, run_time=1.2,
        ))
        self.wait(HOLD_SHORT)

        # -- RNN cursor sweep with step counter --
        step_counter = VGroup(
            Text("Step: ", font_size=LABEL_SIZE, color=C["label"]),
            Integer(0, font_size=LABEL_SIZE, color=C["attention"]),
        ).arrange(RIGHT, buff=0.15).next_to(word_boxes, DOWN, buff=0.7)
        self.play(FadeIn(step_counter))

        highlight = SurroundingRectangle(word_boxes[0], color=C["attention"], buff=0.08)
        self.play(Create(highlight))
        for i in range(len(words)):
            target = SurroundingRectangle(word_boxes[i], color=C["attention"], buff=0.08)
            self.play(
                Transform(highlight, target),
                step_counter[1].animate.set_value(i + 1),
                word_boxes[i][0].animate.set_fill(C["attention"], opacity=0.3),
                run_time=0.45,
            )
        self.wait(HOLD_SHORT)

        # -- Bottleneck callout --
        bottleneck = Text("Word 6 must wait for words 1-5", font_size=BODY_SIZE, color=C["negative"])
        bottleneck.next_to(step_counter, DOWN, buff=0.6)
        self.play(Write(bottleneck))
        self.wait(HOLD_MEDIUM)

        # -- Scale-up --
        scale_text = Text(
            "1,000-word document = 1,000 sequential steps",
            font_size=BODY_SIZE, color=C["negative"],
        )
        scale_text.next_to(bottleneck, DOWN, buff=0.5)
        self.play(Write(scale_text))
        self.wait(HOLD_MEDIUM)

        # -- Key insight --
        self.play(FadeOut(VGroup(title, word_boxes, highlight, step_counter, bottleneck, scale_text)))
        self.wait(FADE_FAST)

        insight = Text(
            "What if every word could look at\n"
            "every other word... simultaneously?",
            font_size=SUBTITLE_SIZE, color=C["attention"], line_spacing=1.4,
        )
        self.play(Write(insight, run_time=2))
        self.wait(HOLD_LONG)
        self.play(FadeOut(insight))
