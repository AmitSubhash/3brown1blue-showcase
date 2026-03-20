"""Scene 3: Transformer Architecture -- one continuous scene building
from multi-head attention through a single encoder layer to the full
encoder-decoder architecture. Each phase visually carries into the next."""

from pathlib import Path
from manim import *

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils.style import *


class Architecture(Scene):
    """Build the Transformer architecture piece by piece in one flow."""

    def construct(self) -> None:
        story_bridge(self, "Now let's build the architecture")

        # ── PHASE 1: Multi-Head Attention ───────────────────────────
        self.next_section("MultiHead")

        title = Text(
            "Multi-Head Attention",
            font_size=TITLE_SIZE, color=WHITE,
        ).to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(HOLD_SHORT)

        # Single head
        single = labeled_box("Attention\nHead", width=1.6, height=1.0, color=C["query"])
        single.shift(DOWN * 0.3)
        explain = Text(
            "One head = one type of relationship",
            font_size=LABEL_SIZE, color=C["label"],
        ).next_to(single, DOWN, buff=0.5)
        self.play(FadeIn(single, shift=UP * 0.3), Write(explain))
        self.wait(HOLD_MEDIUM)
        self.play(FadeOut(explain))

        # Expand to 8 heads
        head_labels = ["Syntax", "Semantics", "Position", "Coref",
                       "Tense", "Negation", "Entity", "Style"]
        heads = VGroup(*[
            labeled_box(l, width=1.2, height=0.9, color=C["query"], font_size=18)
            for l in head_labels
        ]).arrange(RIGHT, buff=0.15).next_to(title, DOWN, buff=0.7)

        self.play(ReplacementTransform(single, heads[0]))
        self.play(LaggedStart(
            *[FadeIn(h, shift=UP * 0.3) for h in heads[1:]],
            lag_ratio=0.12, run_time=1.5,
        ))
        self.wait(HOLD_SHORT)

        # Concat + Linear
        concat = labeled_box("Concat", width=heads.width, height=0.7, color=C["value"])
        concat.next_to(heads, DOWN, buff=0.5)
        c_arrows = VGroup(*[
            Arrow(h[0].get_bottom(), concat[0].get_top(),
                  buff=0.08, stroke_width=1.5, color=C["dim"])
            for h in heads
        ])
        self.play(
            LaggedStart(*[GrowArrow(a) for a in c_arrows], lag_ratio=0.05),
            FadeIn(concat, shift=UP * 0.3), run_time=1.0,
        )

        proj = labeled_box("Linear W^O", width=2.5, height=0.7, color=C["output"])
        proj.next_to(concat, DOWN, buff=0.5)
        p_arrow = Arrow(concat[0].get_bottom(), proj[0].get_top(), buff=0.08, color=WHITE)
        self.play(GrowArrow(p_arrow), FadeIn(proj, shift=UP * 0.3))
        self.wait(HOLD_SHORT)

        mh_eq = MathTex(
            r"\text{MultiHead} = \text{Concat}(\text{head}_1 \dots \text{head}_h)\, W^O",
            font_size=EQ_SMALL, color=C["attention"],
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(mh_eq))
        self.wait(HOLD_MEDIUM)

        # TRANSITION: shrink multi-head to a single box representing it
        mh_all = VGroup(title, heads, c_arrows, concat, p_arrow, proj, mh_eq)
        mh_box = labeled_box("Multi-Head\nAttention", width=3.5, height=0.7, color=C["query"])
        self.play(FadeOut(mh_all))

        # ── PHASE 2: Encoder Layer ──────────────────────────────────
        self.next_section("EncoderLayer")

        title2 = Text("One Encoder Layer", font_size=TITLE_SIZE, color=WHITE)
        title2.to_edge(UP, buff=0.4)
        self.play(Write(title2))
        self.wait(HOLD_SHORT)

        specs = [
            ("Input Embeddings", C["input"]),
            ("Multi-Head Attention", C["query"]),
            ("Add & Norm", C["dim"]),
            ("Feed Forward", C["value"]),
            ("Add & Norm", C["dim"]),
        ]
        boxes = VGroup(*[
            labeled_box(n, width=3.5, height=0.7, color=c) for n, c in specs
        ]).arrange(UP, buff=0.35).next_to(title2, DOWN, buff=0.6)

        layer_arrows = VGroup()
        for i, box in enumerate(boxes):
            self.play(FadeIn(box, shift=UP * 0.3), run_time=0.6)
            if i > 0:
                arr = Arrow(boxes[i-1][0].get_top(), box[0].get_bottom(),
                            buff=0.06, color=WHITE, stroke_width=2)
                layer_arrows.add(arr)
                self.play(GrowArrow(arr), run_time=0.3)
            if i == 2:
                res = Text("residual shortcut", font_size=18, color=C["label"])
                res.next_to(box, RIGHT, buff=0.4)
                self.play(Write(res))
                self.wait(HOLD_SHORT)
                self.play(FadeOut(res))
            self.wait(0.2)

        brace = Brace(boxes, RIGHT, color=C["encoder"])
        bl = Tex(r"1 Encoder\\Layer", font_size=LABEL_SIZE).set_color(C["encoder"])
        brace.put_at_tip(bl)
        self.play(Create(brace), Write(bl))
        self.wait(HOLD_MEDIUM)

        # TRANSITION: shrink encoder layer into a single tall box
        layer_group = VGroup(title2, boxes, layer_arrows, brace, bl)
        self.play(FadeOut(layer_group))

        # ── PHASE 3: Full Architecture ──────────────────────────────
        self.next_section("FullArchitecture")

        title3 = Text("The Full Transformer", font_size=TITLE_SIZE, color=WHITE)
        title3.to_edge(UP, buff=0.4)
        self.play(Write(title3))
        self.wait(HOLD_SHORT)

        # Encoder
        enc = labeled_box("Encoder\nx6", width=2.8, height=3.0,
                          color=C["encoder"], font_size=BODY_SIZE)
        enc.shift(LEFT * 2.5 + DOWN * 0.3)
        enc_in = Text("Source sentence", font_size=LABEL_SIZE, color=C["input"])
        enc_in.next_to(enc, DOWN, buff=0.5)
        enc_arr = Arrow(enc_in.get_top(), enc[0].get_bottom(), buff=0.1, color=C["input"])
        self.play(FadeIn(enc_in), GrowArrow(enc_arr), FadeIn(enc, shift=UP * 0.3))
        self.wait(HOLD_SHORT)

        # Decoder
        dec = labeled_box("Decoder\nx6", width=2.8, height=3.0,
                          color=C["decoder"], font_size=BODY_SIZE)
        dec.shift(RIGHT * 2.5 + DOWN * 0.3)
        dec_in = Text("Target sentence\n(shifted right)",
                      font_size=LABEL_SIZE, color=C["input"], line_spacing=1.2)
        dec_in.next_to(dec, DOWN, buff=0.5)
        dec_arr = Arrow(dec_in.get_top(), dec[0].get_bottom(), buff=0.1, color=C["input"])
        self.play(FadeIn(dec_in), GrowArrow(dec_arr), FadeIn(dec, shift=UP * 0.3))
        self.wait(HOLD_SHORT)

        # Cross-attention
        cross = Arrow(enc[0].get_right(), dec[0].get_left(),
                      buff=0.1, color=C["attention"], stroke_width=3)
        cross_lbl = Text("Cross-Attention", font_size=18, color=C["attention"])
        cross_lbl.next_to(cross, UP, buff=0.1)
        self.play(GrowArrow(cross), Write(cross_lbl))
        self.wait(HOLD_SHORT)

        # Output
        out_txt = Text("Predicted next word", font_size=LABEL_SIZE, color=C["output"])
        out_txt.next_to(dec, UP, buff=0.5)
        out_arr = Arrow(dec[0].get_top(), out_txt.get_bottom(), buff=0.1, color=C["output"])
        self.play(GrowArrow(out_arr), FadeIn(out_txt, shift=UP * 0.3))
        self.wait(HOLD_SHORT)

        tagline = Text("No recurrence. No convolution. Just attention.",
                       font_size=BODY_SIZE, color=C["attention"])
        tagline.to_edge(DOWN, buff=0.4)
        self.play(Write(tagline, run_time=1.5))
        self.wait(HOLD_LONG)

        self.play(*[FadeOut(m) for m in self.mobjects])
