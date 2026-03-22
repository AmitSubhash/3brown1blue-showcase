"""Scene 06: The Encoder Block (~90 seconds)

Builds up one encoder block, shows residual connections,
the residual stream metaphor, then stacks 6 blocks with
a token traveling upward through all layers.
"""

import sys
sys.path.insert(0, "/Users/amit/Projects/3brown1blue-showcase")

from manim import *
from transformer.utils.style import (
    BG_COLOR, C, TITLE_Y, SUBTITLE_Y, BOTTOM_Y,
    SAFE_WIDTH, SAFE_X, SAFE_Y,
    TITLE_SIZE, SUBTITLE_SIZE, BODY_SIZE, LABEL_SIZE, TINY_SIZE,
    HOLD_SHORT, HOLD_MEDIUM, HOLD_LONG, DIM_OPACITY,
    section_title, subtitle, body_text, safe_text, bottom_note,
    labeled_box, story_bridge, arrow_between,
)

# ---- Layout constants for this scene ----
# Persistent title at top, content in lower region
CONTENT_CENTER_Y = -0.2
CONTENT_TOP = 2.2
CONTENT_BOTTOM = -3.2


def _thin_bar(label: str, width: float = 3.0, color=C["residual"]) -> VGroup:
    """A thin 'Add & Norm' bar for the encoder diagram."""
    rect = RoundedRectangle(
        width=width, height=0.35, corner_radius=0.08,
        color=color, fill_opacity=0.25, stroke_width=1.5,
    )
    text = safe_text(label, max_width=width - 0.2,
                     font_size=TINY_SIZE, color=color)
    text.move_to(rect)
    return VGroup(rect, text)


def _residual_arrow(start_mob, end_mob, direction=LEFT, color=C["residual"]):
    """Curved bypass arrow for residual connection."""
    start_pt = start_mob.get_edge_center(direction)
    end_pt = end_mob.get_edge_center(direction)

    offset = 0.6 * direction
    mid_y = (start_pt[1] + end_pt[1]) / 2

    path = CubicBezier(
        start_pt,
        start_pt + offset + UP * 0.3,
        end_pt + offset + DOWN * 0.3,
        end_pt,
    )
    path.set_color(color)
    path.set_stroke(width=2, opacity=0.7)

    tip = ArrowTriangleFilledTip(
        color=color, fill_opacity=0.7,
    ).scale(0.5)
    tip.move_to(end_pt)
    tip.rotate(path.get_angle() + PI / 2)

    return VGroup(path, tip)


def _build_encoder_block(
    width: float = 3.0,
    spacing: float = 0.15,
    show_labels: bool = True,
) -> VGroup:
    """Build a single encoder block as a vertical stack."""
    # Components bottom to top
    mha_box = labeled_box(
        "Multi-Head\nSelf-Attention",
        width=width, height=0.8,
        color=C["encoder"], font_size=TINY_SIZE,
        fill_opacity=0.25,
    )
    add_norm_1 = _thin_bar("Add & Norm", width=width)
    ffn_box = labeled_box(
        "Feed-Forward\n512 > 2048 > 512, ReLU",
        width=width, height=0.8,
        color=C["ffn"], font_size=TINY_SIZE,
        fill_opacity=0.25,
    )
    add_norm_2 = _thin_bar("Add & Norm", width=width)

    # Stack them vertically (bottom to top)
    stack = VGroup(mha_box, add_norm_1, ffn_box, add_norm_2)
    stack.arrange(UP, buff=spacing)

    return stack


class EncoderBlock(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        self._part1_build_block()
        self._part2_residual_connections()
        self._part3_residual_stream()
        self._part4_stack_six()
        self._part5_token_travel()
        self._part6_layer_norm_note()

    # ------------------------------------------------------------------
    # Part 1: Build up one encoder block (~20s)
    # ------------------------------------------------------------------
    def _part1_build_block(self):
        title = section_title("The Encoder Block", color=C["encoder"])
        self.play(Write(title), run_time=0.8)
        self.wait(HOLD_SHORT)

        # Store title for persistent display
        self.title_mob = title

        # Build block components one at a time
        block_width = 3.2
        sp = 0.18

        mha = labeled_box(
            "Multi-Head Self-Attention",
            width=block_width, height=0.75,
            color=C["encoder"], font_size=TINY_SIZE,
            fill_opacity=0.25,
        )
        an1 = _thin_bar("Add & Norm", width=block_width)
        ffn = labeled_box(
            "Feed-Forward Network",
            width=block_width, height=0.75,
            color=C["ffn"], font_size=TINY_SIZE,
            fill_opacity=0.25,
        )
        ffn_detail = safe_text(
            "512 -> 2048 -> 512, ReLU",
            max_width=block_width - 0.4,
            font_size=14, color=C["ffn"],
        )
        an2 = _thin_bar("Add & Norm", width=block_width)

        # Arrange bottom to top
        stack = VGroup(mha, an1, ffn, an2)
        stack.arrange(UP, buff=sp)
        stack.move_to(ORIGIN + DOWN * 0.3)

        ffn_detail.next_to(ffn, DOWN, buff=0.04)
        ffn_detail.shift(UP * 0.02)
        # Place detail inside ffn box
        ffn_detail.move_to(ffn[0].get_center() + DOWN * 0.18)

        # Input arrow at bottom
        input_arrow = Arrow(
            stack.get_bottom() + DOWN * 0.7,
            stack.get_bottom() + DOWN * 0.05,
            color=WHITE, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.2,
        )
        input_label = safe_text(
            "Input Embeddings", max_width=3.0,
            font_size=TINY_SIZE, color=C["dim"],
        )
        input_label.next_to(input_arrow, DOWN, buff=0.1)

        # Output arrow at top
        output_arrow = Arrow(
            stack.get_top() + UP * 0.05,
            stack.get_top() + UP * 0.7,
            color=WHITE, stroke_width=2.5,
            max_tip_length_to_length_ratio=0.2,
        )
        output_label = safe_text(
            "To Next Layer", max_width=3.0,
            font_size=TINY_SIZE, color=C["dim"],
        )
        output_label.next_to(output_arrow, UP, buff=0.1)

        # Animate building up from bottom
        self.play(
            GrowArrow(input_arrow),
            Write(input_label),
            run_time=0.6,
        )
        self.play(FadeIn(mha, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(an1, shift=UP * 0.1), run_time=0.3)
        self.play(
            FadeIn(ffn, shift=UP * 0.2),
            Write(ffn_detail),
            run_time=0.5,
        )
        self.play(FadeIn(an2, shift=UP * 0.1), run_time=0.3)
        self.play(
            GrowArrow(output_arrow),
            Write(output_label),
            run_time=0.6,
        )
        self.wait(HOLD_MEDIUM)

        # Store references
        self.block_group = VGroup(
            input_arrow, input_label,
            stack, ffn_detail,
            output_arrow, output_label,
        )
        self.mha = mha
        self.an1 = an1
        self.ffn = ffn
        self.an2 = an2
        self.stack = stack
        self.input_arrow = input_arrow
        self.output_arrow = output_arrow

    # ------------------------------------------------------------------
    # Part 2: Show residual connections (~15s)
    # ------------------------------------------------------------------
    def _part2_residual_connections(self):
        sub = subtitle("Residual Connections", color=C["residual"])
        self.play(Write(sub), run_time=0.6)

        # Residual bypass around MHA -> Add&Norm1
        # Curved arrow on the left side
        res1_start = self.mha[0].get_bottom() + DOWN * 0.02
        res1_end = self.an1[0].get_top() + UP * 0.02

        res1_path = ArcBetweenPoints(
            self.mha[0].get_left() + LEFT * 0.05 + DOWN * 0.1,
            self.an1[0].get_left() + LEFT * 0.05 + UP * 0.05,
            angle=-PI / 2,
            color=C["residual"],
        )
        res1_path.set_stroke(width=2.5, opacity=0.8)

        # Residual bypass around FFN -> Add&Norm2
        res2_path = ArcBetweenPoints(
            self.ffn[0].get_left() + LEFT * 0.05 + DOWN * 0.1,
            self.an2[0].get_left() + LEFT * 0.05 + UP * 0.05,
            angle=-PI / 2,
            color=C["residual"],
        )
        res2_path.set_stroke(width=2.5, opacity=0.8)

        # Dashed styling
        res1_dashed = DashedVMobject(res1_path, num_dashes=8)
        res2_dashed = DashedVMobject(res2_path, num_dashes=8)

        res_label1 = safe_text(
            "skip", max_width=1.0,
            font_size=14, color=C["residual"],
        )
        res_label1.next_to(res1_dashed, LEFT, buff=0.08)

        res_label2 = safe_text(
            "skip", max_width=1.0,
            font_size=14, color=C["residual"],
        )
        res_label2.next_to(res2_dashed, LEFT, buff=0.08)

        self.play(
            Create(res1_dashed),
            Write(res_label1),
            run_time=0.8,
        )
        self.play(
            Create(res2_dashed),
            Write(res_label2),
            run_time=0.8,
        )
        self.wait(HOLD_MEDIUM)

        self.residual_group = VGroup(
            res1_dashed, res2_dashed, res_label1, res_label2,
        )

        # Fade out subtitle
        self.play(FadeOut(sub), run_time=0.4)

    # ------------------------------------------------------------------
    # Part 3: Residual stream metaphor (~20s)
    # ------------------------------------------------------------------
    def _part3_residual_stream(self):
        # Fade out the block diagram
        self.play(
            FadeOut(self.block_group),
            FadeOut(self.residual_group),
            run_time=0.6,
        )

        stream_title = subtitle("The Residual Stream", color=C["attention"])
        self.play(Write(stream_title), run_time=0.6)

        # Draw a thick horizontal "river" representing the residual stream
        river_y = -0.3
        river = Arrow(
            LEFT * 5.5 + UP * river_y,
            RIGHT * 5.5 + UP * river_y,
            color=BLUE_B,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.04,
        )
        river_label = safe_text(
            "Residual Stream",
            max_width=4.0,
            font_size=LABEL_SIZE, color=BLUE_B,
        )
        river_label.next_to(river, DOWN, buff=0.3)

        self.play(GrowArrow(river), Write(river_label), run_time=1.0)
        self.wait(HOLD_SHORT)

        # Tributaries: Self-Attention reads and writes
        sa_x = -2.5
        sa_box = labeled_box(
            "Self-Attention",
            width=2.2, height=0.6,
            color=C["encoder"], font_size=TINY_SIZE,
            fill_opacity=0.2,
        )
        sa_box.move_to(UP * 1.5 + RIGHT * sa_x)

        # Read arrow (from stream up to SA)
        sa_read = Arrow(
            RIGHT * sa_x + UP * river_y,
            sa_box.get_bottom(),
            color=C["encoder"],
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )
        # Write arrow (from SA back to stream, slightly to the right)
        sa_write = Arrow(
            sa_box.get_bottom() + RIGHT * 0.5,
            RIGHT * (sa_x + 0.8) + UP * river_y,
            color=C["encoder"],
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )

        sa_read_label = safe_text(
            "read", max_width=1.0,
            font_size=14, color=C["encoder"],
        )
        sa_read_label.next_to(sa_read, LEFT, buff=0.05)

        sa_write_label = safe_text(
            "write", max_width=1.0,
            font_size=14, color=C["encoder"],
        )
        sa_write_label.next_to(sa_write, RIGHT, buff=0.05)

        # FFN tributary
        ffn_x = 2.5
        ffn_box = labeled_box(
            "FFN",
            width=1.8, height=0.6,
            color=C["ffn"], font_size=TINY_SIZE,
            fill_opacity=0.2,
        )
        ffn_box.move_to(UP * 1.5 + RIGHT * ffn_x)

        ffn_read = Arrow(
            RIGHT * ffn_x + UP * river_y,
            ffn_box.get_bottom(),
            color=C["ffn"],
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )
        ffn_write = Arrow(
            ffn_box.get_bottom() + RIGHT * 0.5,
            RIGHT * (ffn_x + 0.8) + UP * river_y,
            color=C["ffn"],
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )

        ffn_read_label = safe_text(
            "read", max_width=1.0,
            font_size=14, color=C["ffn"],
        )
        ffn_read_label.next_to(ffn_read, LEFT, buff=0.05)

        ffn_write_label = safe_text(
            "write", max_width=1.0,
            font_size=14, color=C["ffn"],
        )
        ffn_write_label.next_to(ffn_write, RIGHT, buff=0.05)

        self.play(
            FadeIn(sa_box, shift=UP * 0.2),
            GrowArrow(sa_read),
            Write(sa_read_label),
            run_time=0.7,
        )
        self.play(
            GrowArrow(sa_write),
            Write(sa_write_label),
            run_time=0.5,
        )
        self.play(
            FadeIn(ffn_box, shift=UP * 0.2),
            GrowArrow(ffn_read),
            Write(ffn_read_label),
            run_time=0.7,
        )
        self.play(
            GrowArrow(ffn_write),
            Write(ffn_write_label),
            run_time=0.5,
        )

        # "Information accumulates" note
        accum_note = safe_text(
            "Information accumulates -- the stream gets richer",
            max_width=10.0,
            font_size=BODY_SIZE, color=C["highlight"],
        )
        accum_note.move_to(DOWN * 2.0)
        self.play(Write(accum_note), run_time=0.8)
        self.wait(HOLD_MEDIUM)

        # Animate the stream getting thicker (richer)
        thicker_river = Arrow(
            LEFT * 5.5 + UP * river_y,
            RIGHT * 5.5 + UP * river_y,
            color=BLUE_B,
            stroke_width=12,
            max_tip_length_to_length_ratio=0.04,
        )
        self.play(
            ReplacementTransform(river, thicker_river),
            run_time=0.8,
        )
        self.wait(HOLD_SHORT)

        # Clean up
        stream_group = VGroup(
            thicker_river, river_label,
            sa_box, sa_read, sa_write,
            sa_read_label, sa_write_label,
            ffn_box, ffn_read, ffn_write,
            ffn_read_label, ffn_write_label,
            accum_note, stream_title,
        )
        self.play(FadeOut(stream_group), run_time=0.6)

    # ------------------------------------------------------------------
    # Part 4: Scale to 6 stacked blocks (~15s)
    # ------------------------------------------------------------------
    def _part4_stack_six(self):
        stack_title = subtitle("Stacking N = 6 Layers", color=C["encoder"])
        self.play(Write(stack_title), run_time=0.6)

        # Build a single small encoder block
        def mini_block(label_num):
            box = RoundedRectangle(
                width=2.2, height=0.55, corner_radius=0.1,
                color=C["encoder"], fill_opacity=0.2, stroke_width=1.5,
            )
            # Two thin colored strips inside to suggest MHA + FFN
            mha_strip = Rectangle(
                width=1.8, height=0.12, color=C["encoder"],
                fill_opacity=0.4, stroke_width=0,
            )
            ffn_strip = Rectangle(
                width=1.8, height=0.12, color=C["ffn"],
                fill_opacity=0.4, stroke_width=0,
            )
            mha_strip.move_to(box.get_center() + UP * 0.12)
            ffn_strip.move_to(box.get_center() + DOWN * 0.12)
            num_label = safe_text(
                str(label_num), max_width=0.3,
                font_size=14, color=WHITE,
            )
            num_label.move_to(box.get_right() + LEFT * 0.25)
            return VGroup(box, mha_strip, ffn_strip, num_label)

        # Create 6 blocks
        blocks = VGroup(*[mini_block(i + 1) for i in range(6)])
        blocks.arrange(UP, buff=0.12)
        blocks.move_to(DOWN * 0.2)

        # Ensure within bounds
        if blocks.get_top()[1] > SAFE_Y[1] - 0.5:
            blocks.scale_to_fit_height(SAFE_Y[1] - SAFE_Y[0] - 2.5)
            blocks.move_to(DOWN * 0.2)

        # Input arrow
        inp_arr = Arrow(
            blocks.get_bottom() + DOWN * 0.6,
            blocks.get_bottom() + DOWN * 0.05,
            color=WHITE, stroke_width=2,
            max_tip_length_to_length_ratio=0.2,
        )
        inp_lbl = safe_text(
            "Input", max_width=1.5,
            font_size=TINY_SIZE, color=C["dim"],
        )
        inp_lbl.next_to(inp_arr, DOWN, buff=0.08)

        # Output arrow
        out_arr = Arrow(
            blocks.get_top() + UP * 0.05,
            blocks.get_top() + UP * 0.6,
            color=WHITE, stroke_width=2,
            max_tip_length_to_length_ratio=0.2,
        )
        out_lbl = safe_text(
            "Output", max_width=1.5,
            font_size=TINY_SIZE, color=C["dim"],
        )
        out_lbl.next_to(out_arr, UP, buff=0.08)

        # x6 label
        x6_label = safe_text(
            "x6", max_width=1.5,
            font_size=TITLE_SIZE, color=C["encoder"],
        )
        x6_label.next_to(blocks, RIGHT, buff=0.5)

        # Animate: first block appears, then the rest
        self.play(
            FadeIn(blocks[0], shift=UP * 0.2),
            GrowArrow(inp_arr),
            Write(inp_lbl),
            run_time=0.6,
        )
        self.play(
            LaggedStart(
                *[FadeIn(b, shift=UP * 0.15) for b in blocks[1:]],
                lag_ratio=0.12,
            ),
            run_time=1.2,
        )
        self.play(
            GrowArrow(out_arr),
            Write(out_lbl),
            Write(x6_label),
            run_time=0.6,
        )
        self.wait(HOLD_MEDIUM)

        # Store for next part
        self.six_blocks = blocks
        self.six_group = VGroup(
            blocks, inp_arr, inp_lbl, out_arr, out_lbl, x6_label,
        )
        self.stack_title = stack_title

    # ------------------------------------------------------------------
    # Part 5: Token traveling upward (~15s)
    # ------------------------------------------------------------------
    def _part5_token_travel(self):
        self.play(FadeOut(self.stack_title), run_time=0.3)

        travel_sub = subtitle(
            "A Token's Journey Through 6 Layers",
            color=C["attention"],
        )
        self.play(Write(travel_sub), run_time=0.6)

        # Create a glowing dot
        token_dot = Dot(
            radius=0.12,
            color=C["attention"],
            fill_opacity=1.0,
        )
        glow = Dot(
            radius=0.25,
            color=C["attention"],
            fill_opacity=0.3,
        )
        token = VGroup(glow, token_dot)
        token.move_to(self.six_blocks[0].get_bottom() + DOWN * 0.3)

        self.play(FadeIn(token, scale=0.5), run_time=0.4)

        # Travel through each block with a color shift
        color_progression = [
            interpolate_color(C["attention"], C["encoder"], alpha)
            for alpha in [0.0, 0.15, 0.3, 0.45, 0.6, 0.75]
        ]

        for i, block in enumerate(self.six_blocks):
            target_pos = block.get_center()
            new_color = color_progression[i]

            # Flash the block as token passes through
            self.play(
                token.animate.move_to(target_pos),
                block[0].animate.set_fill(
                    color=new_color, opacity=0.4,
                ),
                run_time=0.4,
            )
            # Brief hold at each layer
            self.wait(0.15)

        # Token exits at the top
        self.play(
            token.animate.move_to(
                self.six_blocks[-1].get_top() + UP * 0.5
            ),
            run_time=0.3,
        )

        refined_label = safe_text(
            "Refined representation",
            max_width=4.0,
            font_size=LABEL_SIZE, color=C["encoder"],
        )
        refined_label.next_to(token, RIGHT, buff=0.3)
        self.play(Write(refined_label), run_time=0.5)
        self.wait(HOLD_MEDIUM)

        # Clean up
        self.play(
            FadeOut(VGroup(
                self.six_group, token, refined_label, travel_sub,
            )),
            run_time=0.6,
        )

    # ------------------------------------------------------------------
    # Part 6: Layer Norm note (~10s)
    # ------------------------------------------------------------------
    def _part6_layer_norm_note(self):
        ln_title = subtitle("Layer Normalization", color=WHITE)
        self.play(Write(ln_title), run_time=0.5)

        # Visual: feature dimension normalization
        # Show a vector of values, then normalized
        raw_vals = [0.2, 3.1, -1.5, 0.8, 2.4]
        norm_vals = []
        mean_v = sum(raw_vals) / len(raw_vals)
        var_v = sum((v - mean_v) ** 2 for v in raw_vals) / len(raw_vals)
        std_v = var_v ** 0.5
        for v in raw_vals:
            norm_vals.append((v - mean_v) / (std_v + 1e-5))

        # Raw vector bars
        raw_bars = VGroup()
        for i, v in enumerate(raw_vals):
            bar = Rectangle(
                width=0.4,
                height=abs(v) * 0.4,
                color=C["attention"],
                fill_opacity=0.5,
                stroke_width=1,
            )
            if v >= 0:
                bar.next_to(ORIGIN, UP, buff=0)
            else:
                bar.next_to(ORIGIN, DOWN, buff=0)
            bar.shift(RIGHT * (i - 2) * 0.6)
            raw_bars.add(bar)

        raw_group = VGroup(raw_bars)
        raw_group.move_to(LEFT * 3 + DOWN * 0.5)

        raw_label = safe_text(
            "Before LayerNorm",
            max_width=3.0,
            font_size=TINY_SIZE, color=C["dim"],
        )
        raw_label.next_to(raw_group, DOWN, buff=0.3)

        # Normalized vector bars
        norm_bars = VGroup()
        for i, v in enumerate(norm_vals):
            bar = Rectangle(
                width=0.4,
                height=abs(v) * 0.4,
                color=C["positive"],
                fill_opacity=0.5,
                stroke_width=1,
            )
            if v >= 0:
                bar.next_to(ORIGIN, UP, buff=0)
            else:
                bar.next_to(ORIGIN, DOWN, buff=0)
            bar.shift(RIGHT * (i - 2) * 0.6)
            norm_bars.add(bar)

        norm_group = VGroup(norm_bars)
        norm_group.move_to(RIGHT * 3 + DOWN * 0.5)

        norm_label = safe_text(
            "After LayerNorm",
            max_width=3.0,
            font_size=TINY_SIZE, color=C["dim"],
        )
        norm_label.next_to(norm_group, DOWN, buff=0.3)

        # Arrow between
        transform_arrow = Arrow(
            raw_group.get_right() + RIGHT * 0.2,
            norm_group.get_left() + LEFT * 0.2,
            color=WHITE,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )

        formula = safe_text(
            "Normalize across features: stabilizes training",
            max_width=10.0,
            font_size=LABEL_SIZE, color=WHITE,
        )
        formula.move_to(DOWN * 2.5)

        self.play(
            FadeIn(raw_bars, shift=UP * 0.2),
            Write(raw_label),
            run_time=0.6,
        )
        self.play(
            GrowArrow(transform_arrow),
            run_time=0.4,
        )
        self.play(
            FadeIn(norm_bars, shift=UP * 0.2),
            Write(norm_label),
            run_time=0.6,
        )
        self.play(Write(formula), run_time=0.6)
        self.wait(HOLD_MEDIUM)

        # Final cleanup
        all_remaining = VGroup(
            self.title_mob, ln_title,
            raw_bars, raw_label,
            norm_bars, norm_label,
            transform_arrow, formula,
        )
        self.play(FadeOut(all_remaining), run_time=0.8)
        self.wait(0.5)
