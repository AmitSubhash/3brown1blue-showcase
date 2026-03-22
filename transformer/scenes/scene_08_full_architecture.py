"""Scene 08: The Full Transformer Architecture.

Builds the iconic encoder-decoder diagram piece by piece,
then traces a translation example through the forward pass.
Duration target: ~120 seconds.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from utils.style import (
    BG_COLOR, C, TITLE_SIZE, BODY_SIZE, LABEL_SIZE, TINY_SIZE,
    TITLE_Y, BOTTOM_Y, SAFE_WIDTH, SAFE_Y,
    HOLD_SHORT, HOLD_MEDIUM, HOLD_LONG,
    section_title, safe_text, labeled_box, bottom_note,
)


# ── Local constants ──────────────────────────────────────────────────
ENC_X = -2.8          # encoder column center
DEC_X = 2.8           # decoder column center
BOX_W = 2.3           # component box width
BOX_H = 0.5           # component box height
STACK_GAP = 0.12      # vertical gap between stacked boxes
ARROW_STROKE = 2


def _vflow_arrow(start_mob, end_mob, color=WHITE) -> Arrow:
    """Vertical upward arrow between two boxes."""
    return Arrow(
        start_mob.get_top(), end_mob.get_bottom(),
        color=color, buff=0.06, stroke_width=ARROW_STROKE,
        max_tip_length_to_length_ratio=0.2,
    )


def _make_block_stack(labels, base_y, x_center, color, tag=""):
    """Build a vertical stack of labeled_box components.

    Returns (VGroup of all boxes, list of individual boxes).
    """
    boxes = []
    y = base_y
    for lbl in labels:
        b = labeled_box(lbl, width=BOX_W, height=BOX_H,
                        color=color, font_size=TINY_SIZE)
        b.move_to([x_center, y, 0])
        boxes.append(b)
        y += BOX_H + STACK_GAP
    return VGroup(*boxes), boxes


class FullArchitecture(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self) -> None:
        # ── Phase 1: Build the architecture diagram ──────────────
        self.next_section("Architecture Diagram")

        title = section_title("The Full Transformer", color=C["highlight"])
        self.play(Write(title), run_time=1.0)
        self.wait(HOLD_SHORT)

        # ── Encoder column ───────────────────────────────────────
        enc_base_y = -2.6

        # Input embedding
        enc_embed = labeled_box("Input\nEmbedding", width=BOX_W, height=0.6,
                                color=C["encoder"], font_size=TINY_SIZE)
        enc_embed.move_to([ENC_X, enc_base_y, 0])

        # Positional encoding circle
        enc_pos = self._pos_enc_symbol(ENC_X, enc_base_y + 0.55)

        # Encoder sub-layers
        enc_labels = [
            "Multi-Head\nAttention",
            "Add & Norm",
            "Feed Forward",
            "Add & Norm",
        ]
        enc_block_y = enc_base_y + 1.05
        enc_stack, enc_boxes = _make_block_stack(
            enc_labels, enc_block_y, ENC_X, C["encoder"])

        # Nx bracket
        enc_bracket_group = self._nx_bracket(
            enc_stack, side="left", color=C["encoder"])

        # Encoder label
        enc_label = safe_text("Encoder", font_size=LABEL_SIZE,
                              color=C["encoder"])
        enc_label.next_to(enc_stack, UP, buff=0.3)

        # Assemble encoder
        encoder_all = VGroup(
            enc_embed, enc_pos, enc_stack, enc_bracket_group, enc_label)

        # ── Decoder column ───────────────────────────────────────
        dec_base_y = -2.6

        # Output embedding
        dec_embed = labeled_box("Output\nEmbedding", width=BOX_W, height=0.6,
                                color=C["decoder"], font_size=TINY_SIZE)
        dec_embed.move_to([DEC_X, dec_base_y, 0])

        # Positional encoding circle
        dec_pos = self._pos_enc_symbol(DEC_X, dec_base_y + 0.55)

        # Decoder sub-layers
        dec_labels = [
            "Masked\nAttention",
            "Add & Norm",
            "Cross\nAttention",
            "Add & Norm",
            "Feed Forward",
            "Add & Norm",
        ]
        dec_block_y = dec_base_y + 1.05
        dec_stack, dec_boxes = _make_block_stack(
            dec_labels, dec_block_y, DEC_X, C["decoder"])

        # Nx bracket
        dec_bracket_group = self._nx_bracket(
            dec_stack, side="right", color=C["decoder"])

        # Linear + Softmax on top of decoder
        linear_box = labeled_box("Linear", width=BOX_W, height=BOX_H,
                                 color=GRAY_B, font_size=TINY_SIZE)
        linear_box.next_to(dec_stack, UP, buff=STACK_GAP + 0.05)

        softmax_box = labeled_box("Softmax", width=BOX_W, height=BOX_H,
                                  color=GRAY_B, font_size=TINY_SIZE)
        softmax_box.next_to(linear_box, UP, buff=STACK_GAP)

        output_label = safe_text("Output\nProbabilities", font_size=TINY_SIZE,
                                 color=GRAY_B)
        output_label.next_to(softmax_box, UP, buff=0.15)

        dec_label = safe_text("Decoder", font_size=LABEL_SIZE,
                              color=C["decoder"])
        dec_label.move_to([DEC_X, enc_label.get_y(), 0])

        decoder_all = VGroup(
            dec_embed, dec_pos, dec_stack, dec_bracket_group,
            linear_box, softmax_box, output_label, dec_label)

        # ── Animate build-up ─────────────────────────────────────
        # Encoder side
        self.play(FadeIn(enc_embed, shift=UP * 0.3), run_time=0.6)
        self.play(FadeIn(enc_pos, scale=0.5), run_time=0.4)

        # Stack encoder boxes one by one
        for box in enc_boxes:
            self.play(FadeIn(box, shift=UP * 0.15), run_time=0.3)
        self.play(
            FadeIn(enc_bracket_group),
            Write(enc_label),
            run_time=0.6,
        )
        self.wait(0.5)

        # Decoder side
        self.play(FadeIn(dec_embed, shift=UP * 0.3), run_time=0.6)
        self.play(FadeIn(dec_pos, scale=0.5), run_time=0.4)

        for box in dec_boxes:
            self.play(FadeIn(box, shift=UP * 0.15), run_time=0.25)

        self.play(
            FadeIn(dec_bracket_group),
            Write(dec_label),
            run_time=0.6,
        )
        self.play(
            FadeIn(linear_box, shift=UP * 0.15),
            FadeIn(softmax_box, shift=UP * 0.15),
            FadeIn(output_label, shift=UP * 0.1),
            run_time=0.6,
        )
        self.wait(HOLD_SHORT)

        # ── Encoder arrows (internal flow) ───────────────────────
        enc_arrows = VGroup(
            _vflow_arrow(enc_embed, enc_pos, C["encoder"]),
            _vflow_arrow(enc_pos, enc_boxes[0], C["encoder"]),
        )
        for i in range(len(enc_boxes) - 1):
            enc_arrows.add(_vflow_arrow(enc_boxes[i], enc_boxes[i + 1],
                                        C["encoder"]))

        dec_arrows = VGroup(
            _vflow_arrow(dec_embed, dec_pos, C["decoder"]),
            _vflow_arrow(dec_pos, dec_boxes[0], C["decoder"]),
        )
        for i in range(len(dec_boxes) - 1):
            dec_arrows.add(_vflow_arrow(dec_boxes[i], dec_boxes[i + 1],
                                        C["decoder"]))
        dec_arrows.add(_vflow_arrow(dec_boxes[-1], linear_box, GRAY_B))
        dec_arrows.add(_vflow_arrow(linear_box, softmax_box, GRAY_B))

        self.play(
            Create(enc_arrows),
            Create(dec_arrows),
            run_time=0.8,
        )

        # ── Cross-attention arrow (encoder -> decoder) ───────────
        # Arrow from top of encoder stack to cross-attention box (dec_boxes[2])
        cross_attn_box = dec_boxes[2]  # "Cross Attention"
        cross_arrow = Arrow(
            enc_boxes[-1].get_right() + RIGHT * 0.05,
            cross_attn_box.get_left() + LEFT * 0.05,
            color=C["attention"], stroke_width=3,
            buff=0.08,
            max_tip_length_to_length_ratio=0.15,
        )
        kv_label = safe_text("K, V", font_size=TINY_SIZE,
                             color=C["attention"])
        kv_label.next_to(cross_arrow, UP, buff=0.08)

        self.play(
            GrowArrow(cross_arrow),
            FadeIn(kv_label),
            run_time=0.8,
        )
        self.wait(HOLD_MEDIUM)

        # FadeOut title to free top region
        self.play(FadeOut(title), run_time=0.5)

        # ── Phase 2: Trace a translation example ─────────────────
        self.next_section("Translation Trace")

        # Collect all architecture elements for dimming
        arch_group = VGroup(
            encoder_all, decoder_all, enc_arrows, dec_arrows,
            cross_arrow, kv_label)

        # Input tokens below encoder
        input_tokens = safe_text('"I love learning"', font_size=LABEL_SIZE,
                                 color=C["encoder"])
        input_tokens.next_to(enc_embed, DOWN, buff=0.25)

        self.play(Write(input_tokens), run_time=0.7)
        self.wait(0.5)

        # Highlight encoder forward pass (pulse upward through encoder)
        self.play(
            enc_embed[0].animate.set_fill(C["encoder"], opacity=0.6),
            run_time=0.3,
        )
        for box in enc_boxes:
            self.play(
                box[0].animate.set_fill(C["encoder"], opacity=0.5),
                run_time=0.2,
            )
        # Flash "parallel" note
        parallel_note = safe_text("All 3 tokens processed in parallel",
                                  font_size=TINY_SIZE, color=C["highlight"])
        parallel_note.move_to([ENC_X, SAFE_Y[1] - 0.3, 0])
        self.play(FadeIn(parallel_note), run_time=0.4)
        self.wait(HOLD_SHORT)

        # Reset encoder highlight
        self.play(
            enc_embed[0].animate.set_fill(C["encoder"], opacity=0.2),
            *[box[0].animate.set_fill(C["encoder"], opacity=0.2)
              for box in enc_boxes],
            FadeOut(parallel_note),
            run_time=0.4,
        )

        # ── Autoregressive decoder trace ─────────────────────────
        self.next_section("Autoregressive Decoding")

        # Output token area below decoder
        output_area_y = dec_embed.get_bottom()[1] - 0.35

        # Step 1: <start> -> J'
        step_tokens = [
            ("<start>", "J'"),
            ("<start> J'", "aime"),
            ("<start> J' aime", "apprendre"),
        ]

        prev_dec_input = None
        prev_dec_output = None

        for i, (inp, out) in enumerate(step_tokens):
            # Show decoder input
            dec_input = safe_text(f'"{inp}"', font_size=TINY_SIZE,
                                  color=C["decoder"])
            dec_input.move_to([DEC_X, output_area_y, 0])

            anims = [FadeIn(dec_input, shift=UP * 0.15)]
            if prev_dec_input is not None:
                anims.append(FadeOut(prev_dec_input))
            if prev_dec_output is not None:
                anims.append(FadeOut(prev_dec_output))
            self.play(*anims, run_time=0.5)

            # Pulse through decoder boxes
            for box in dec_boxes:
                self.play(
                    box[0].animate.set_fill(C["decoder"], opacity=0.5),
                    run_time=0.12,
                )
            # Flash cross-attention arrow
            self.play(
                cross_arrow.animate.set_color(WHITE),
                run_time=0.15,
            )
            self.play(
                cross_arrow.animate.set_color(C["attention"]),
                run_time=0.15,
            )

            # Reset decoder boxes
            self.play(
                *[box[0].animate.set_fill(C["decoder"], opacity=0.2)
                  for box in dec_boxes],
                run_time=0.2,
            )

            # Show predicted output
            dec_output = safe_text(f'-> "{out}"', font_size=TINY_SIZE,
                                   color=C["highlight"])
            dec_output.next_to(output_label, RIGHT, buff=0.3)
            # Keep within bounds
            if dec_output.get_right()[0] > 6.3:
                dec_output.shift(LEFT * (dec_output.get_right()[0] - 6.3))

            self.play(FadeIn(dec_output, shift=UP * 0.1), run_time=0.4)
            self.wait(0.6)

            prev_dec_input = dec_input
            prev_dec_output = dec_output

        # Clean up last step
        self.play(
            FadeOut(prev_dec_input),
            FadeOut(prev_dec_output),
            FadeOut(input_tokens),
            run_time=0.5,
        )

        # ── Phase 3: Model stats ─────────────────────────────────
        self.next_section("Model Stats")

        stats = safe_text(
            "Base model: 65M parameters, trained in 12 hours on 8 GPUs",
            font_size=LABEL_SIZE, color=C["highlight"],
        )
        stats.move_to([0, BOTTOM_Y + 0.3, 0])

        self.play(Write(stats), run_time=1.2)
        self.wait(HOLD_LONG)

        # Final fade
        self.play(
            FadeOut(arch_group),
            FadeOut(stats),
            run_time=1.5,
        )
        self.wait(0.5)

    # ── Helper methods ───────────────────────────────────────────

    def _pos_enc_symbol(self, x: float, y: float) -> VGroup:
        """Create a small circled '+' for positional encoding."""
        circle = Circle(radius=0.18, color=WHITE, stroke_width=1.5)
        circle.set_fill(BG_COLOR, opacity=1)
        plus = Text("+", font_size=20, color=WHITE)
        plus.move_to(circle)
        group = VGroup(circle, plus)
        group.move_to([x, y, 0])
        return group

    def _nx_bracket(self, stack: VGroup, side="left",
                    color=WHITE) -> VGroup:
        """Add an 'Nx' bracket beside a stack of boxes."""
        if side == "left":
            brace = Brace(stack, LEFT, color=color, buff=0.12)
        else:
            brace = Brace(stack, RIGHT, color=color, buff=0.12)

        nx_text = safe_text("N\u00d7", font_size=TINY_SIZE, color=color)
        if side == "left":
            nx_text.next_to(brace, LEFT, buff=0.08)
        else:
            nx_text.next_to(brace, RIGHT, buff=0.08)

        return VGroup(brace, nx_text)
