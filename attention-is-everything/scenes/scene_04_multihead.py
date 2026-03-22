"""Scene 04: Multi-Head Attention

Shows how a single embedding is split into multiple heads,
each learning different attention patterns (local, coreference,
syntax, global), then concatenated and projected through W^O.

Duration target: ~90 seconds.
"""

import sys
sys.path.insert(0, "/Users/amit/Projects/3brown1blue-showcase/transformer")

from manim import *
from utils.style import (
    BG_COLOR, C, TITLE_Y, SUBTITLE_Y, BOTTOM_Y,
    SAFE_WIDTH, SAFE_X, SAFE_Y,
    TITLE_SIZE, SUBTITLE_SIZE, BODY_SIZE, LABEL_SIZE, EQ_SIZE,
    EQ_SMALL, TINY_SIZE,
    HOLD_SHORT, HOLD_MEDIUM, HOLD_LONG, DIM_OPACITY,
    section_title, subtitle, body_text, safe_text, bottom_note,
    labeled_box, story_bridge, arrow_between,
)

# Head colors -- 8 distinct hues
HEAD_COLORS = [
    BLUE_C, GREEN_C, RED_C, YELLOW_C,
    PURPLE_C, ORANGE, TEAL_C, PINK,
]

# Tokens for the example sentence
TOKENS = ["The", "animal", "didn't", "cross",
           "the", "street", "because", "it",
           "was", "too", "tired"]

# Short tokens for 4x4 heatmaps
HEATMAP_TOKENS = ["animal", "street", "it", "tired"]


class Scene04MultiHead(Scene):
    """Multi-Head Attention visualization."""

    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        self._phase_embedding_split()
        self._phase_parallel_heads()
        self._phase_attention_patterns()
        self._phase_concat_project()
        self._phase_formula()

    # ------------------------------------------------------------------
    # Phase 1: Show 512-dim vector, split into 8 heads of 64 dims
    # ------------------------------------------------------------------
    def _phase_embedding_split(self):
        title = section_title("Multi-Head Attention")
        self.play(Write(title))
        self.wait(HOLD_SHORT)

        # Single tall embedding vector (512-dim)
        embed_rect = Rectangle(
            width=0.8, height=4.5,
            color=WHITE, fill_opacity=0.15,
            stroke_width=2,
        ).move_to(ORIGIN)

        embed_label = safe_text(
            "512-dim\nembedding",
            font_size=LABEL_SIZE, color=C["text"],
        ).next_to(embed_rect, DOWN, buff=0.3)

        dim_ticks = VGroup()
        for i in range(8):
            y = embed_rect.get_top()[1] - (i + 0.5) * (4.5 / 8)
            tick = Line(
                embed_rect.get_left() + LEFT * 0.1 + UP * 0 ,
                embed_rect.get_left() + RIGHT * 0.0,
                stroke_width=1, color=GRAY,
            ).move_to([embed_rect.get_left()[0] - 0.05, y, 0])
            dim_ticks.add(tick)

        self.play(
            FadeIn(embed_rect, shift=UP * 0.3),
            Write(embed_label),
            run_time=1.0,
        )
        self.wait(HOLD_SHORT)

        # Split into 8 colored segments
        segment_height = 4.5 / 8
        segments = VGroup()
        seg_labels = VGroup()

        for i in range(8):
            seg = Rectangle(
                width=0.8, height=segment_height,
                color=HEAD_COLORS[i],
                fill_color=HEAD_COLORS[i],
                fill_opacity=0.4,
                stroke_width=2,
            )
            segments.add(seg)

        # Stack them vertically to match original rect
        segments.arrange(DOWN, buff=0)
        segments.move_to(embed_rect)

        # Labels "64" for each
        for i, seg in enumerate(segments):
            lbl = safe_text(
                "64", font_size=TINY_SIZE, color=HEAD_COLORS[i],
            ).move_to(seg)
            seg_labels.add(lbl)

        self.play(
            FadeOut(embed_rect),
            *[FadeIn(s, shift=RIGHT * 0.1 * (i % 2 * 2 - 1))
              for i, s in enumerate(segments)],
            run_time=1.2,
        )
        self.play(
            *[Write(lbl) for lbl in seg_labels],
            run_time=0.6,
        )
        self.wait(HOLD_SHORT)

        # Spread segments out horizontally
        start_x = -5.0
        spacing = 10.0 / 7

        head_numbers = VGroup()
        for i in range(8):
            target_x = start_x + i * spacing
            hn = safe_text(
                f"H{i+1}", font_size=TINY_SIZE,
                color=HEAD_COLORS[i],
            ).move_to([target_x, -0.3, 0])
            head_numbers.add(hn)

        self.play(
            FadeOut(embed_label),
            FadeOut(seg_labels),
            *[seg.animate.move_to(
                [start_x + i * spacing, 0.5, 0]
            ).set_height(1.2).set_width(0.7)
              for i, seg in enumerate(segments)],
            run_time=1.2,
        )
        self.play(
            *[Write(hn) for hn in head_numbers],
            run_time=0.5,
        )

        sub = subtitle("Each head learns a different aspect of attention")
        self.play(Write(sub))
        self.wait(HOLD_MEDIUM)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(sub),
            FadeOut(segments), FadeOut(head_numbers),
            run_time=0.8,
        )

    # ------------------------------------------------------------------
    # Phase 2: Show Q, K, V projections per head (parallel)
    # ------------------------------------------------------------------
    def _phase_parallel_heads(self):
        title = section_title("Parallel Attention Heads")
        self.play(Write(title))
        self.wait(0.5)

        # Show 4 heads (representative) with Q/K/V mini-blocks
        head_groups = VGroup()
        positions_x = [-4.5, -1.5, 1.5, 4.5]

        for idx, hx in enumerate(positions_x):
            head_color = HEAD_COLORS[idx]

            # Input segment
            inp = Rectangle(
                width=0.5, height=0.8,
                color=head_color, fill_opacity=0.4,
                stroke_width=2,
            ).move_to([hx, 1.5, 0])

            # Q, K, V boxes
            q_box = Rectangle(
                width=0.4, height=0.5,
                color=C["query"], fill_opacity=0.4,
                stroke_width=1.5,
            ).move_to([hx - 0.5, 0.3, 0])
            q_lbl = safe_text("Q", font_size=TINY_SIZE, color=C["query"]
                              ).move_to(q_box)

            k_box = Rectangle(
                width=0.4, height=0.5,
                color=C["key"], fill_opacity=0.4,
                stroke_width=1.5,
            ).move_to([hx, 0.3, 0])
            k_lbl = safe_text("K", font_size=TINY_SIZE, color=C["key"]
                              ).move_to(k_box)

            v_box = Rectangle(
                width=0.4, height=0.5,
                color=C["value"], fill_opacity=0.4,
                stroke_width=1.5,
            ).move_to([hx + 0.5, 0.3, 0])
            v_lbl = safe_text("V", font_size=TINY_SIZE, color=C["value"]
                              ).move_to(v_box)

            # Attention block
            attn_box = RoundedRectangle(
                width=1.4, height=0.6, corner_radius=0.1,
                color=C["attention"], fill_opacity=0.3,
                stroke_width=1.5,
            ).move_to([hx, -0.7, 0])
            attn_lbl = safe_text(
                "Attention", font_size=TINY_SIZE - 2,
                color=C["attention"],
            ).move_to(attn_box)

            # Output
            out = Rectangle(
                width=0.5, height=0.8,
                color=head_color, fill_opacity=0.4,
                stroke_width=2,
            ).move_to([hx, -1.8, 0])

            # Arrows
            a1 = Arrow(inp.get_bottom(), q_box.get_top(),
                        buff=0.05, stroke_width=1.5, color=GRAY_B,
                        max_tip_length_to_length_ratio=0.2)
            a2 = Arrow(inp.get_bottom(), k_box.get_top(),
                        buff=0.05, stroke_width=1.5, color=GRAY_B,
                        max_tip_length_to_length_ratio=0.2)
            a3 = Arrow(inp.get_bottom(), v_box.get_top(),
                        buff=0.05, stroke_width=1.5, color=GRAY_B,
                        max_tip_length_to_length_ratio=0.2)
            a4 = Arrow(
                [hx - 0.5, q_box.get_bottom()[1], 0],
                attn_box.get_top() + LEFT * 0.3,
                buff=0.05, stroke_width=1.5, color=GRAY_B,
                max_tip_length_to_length_ratio=0.2,
            )
            a5 = Arrow(
                [hx, k_box.get_bottom()[1], 0],
                attn_box.get_top(),
                buff=0.05, stroke_width=1.5, color=GRAY_B,
                max_tip_length_to_length_ratio=0.2,
            )
            a6 = Arrow(
                [hx + 0.5, v_box.get_bottom()[1], 0],
                attn_box.get_top() + RIGHT * 0.3,
                buff=0.05, stroke_width=1.5, color=GRAY_B,
                max_tip_length_to_length_ratio=0.2,
            )
            a7 = Arrow(attn_box.get_bottom(), out.get_top(),
                        buff=0.05, stroke_width=1.5, color=GRAY_B,
                        max_tip_length_to_length_ratio=0.2)

            head_lbl = safe_text(
                f"Head {idx + 1}", font_size=TINY_SIZE,
                color=head_color,
            ).next_to(inp, UP, buff=0.15)

            grp = VGroup(
                inp, q_box, q_lbl, k_box, k_lbl, v_box, v_lbl,
                attn_box, attn_lbl, out,
                a1, a2, a3, a4, a5, a6, a7,
                head_lbl,
            )
            head_groups.add(grp)

        # Animate heads appearing one by one quickly
        for i, grp in enumerate(head_groups):
            self.play(FadeIn(grp, shift=UP * 0.2), run_time=0.4)

        dots_label = safe_text(
            "... (8 heads total, d_k = 64 each)",
            font_size=TINY_SIZE, color=C["dim"],
        ).move_to([0, BOTTOM_Y + 0.4, 0])
        self.play(Write(dots_label))
        self.wait(HOLD_MEDIUM)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(head_groups), FadeOut(dots_label),
            run_time=0.8,
        )

    # ------------------------------------------------------------------
    # Phase 3: Attention pattern heatmaps for different heads
    # ------------------------------------------------------------------
    def _phase_attention_patterns(self):
        title = section_title("What Different Heads Learn")
        self.play(Write(title))
        self.wait(0.5)

        # Show the sentence
        sentence = safe_text(
            '"The animal didn\'t cross the street because it was too tired"',
            font_size=LABEL_SIZE, color=C["text"],
        ).move_to([0, SUBTITLE_Y - 0.2, 0])
        self.play(Write(sentence))
        self.wait(HOLD_SHORT)

        # 4 heatmap patterns: Local, Coreference, Syntax, Global
        # Using HEATMAP_TOKENS = ["animal", "street", "it", "tired"]
        #
        # Attention weights (row = query, col = key)
        patterns = {
            "Local Context": [
                [0.7, 0.2, 0.05, 0.05],
                [0.15, 0.6, 0.15, 0.1],
                [0.05, 0.2, 0.6, 0.15],
                [0.05, 0.05, 0.2, 0.7],
            ],
            "Coreference": [
                [0.3, 0.1, 0.1, 0.5],
                [0.1, 0.3, 0.2, 0.4],
                [0.7, 0.05, 0.1, 0.15],   # "it" attends to "animal"
                [0.5, 0.1, 0.2, 0.2],
            ],
            "Syntax": [
                [0.15, 0.15, 0.15, 0.55],  # animal -> tired (subj-pred)
                [0.1, 0.2, 0.1, 0.6],
                [0.5, 0.1, 0.2, 0.2],
                [0.6, 0.1, 0.1, 0.2],      # tired -> animal
            ],
            "Global": [
                [0.25, 0.25, 0.25, 0.25],
                [0.2, 0.3, 0.25, 0.25],
                [0.25, 0.25, 0.25, 0.25],
                [0.3, 0.2, 0.25, 0.25],
            ],
        }

        head_colors_map = {
            "Local Context": HEAD_COLORS[0],
            "Coreference": HEAD_COLORS[1],
            "Syntax": HEAD_COLORS[2],
            "Global": HEAD_COLORS[3],
        }

        heatmaps = VGroup()
        positions_x = [-4.5, -1.5, 1.5, 4.5]

        for idx, (name, weights) in enumerate(patterns.items()):
            hm = self._build_heatmap(
                weights, HEATMAP_TOKENS, name,
                head_colors_map[name],
            )
            hm.move_to([positions_x[idx], -0.5, 0])
            heatmaps.add(hm)

        self.play(
            *[FadeIn(hm, shift=UP * 0.2) for hm in heatmaps],
            run_time=1.5,
        )
        self.wait(HOLD_LONG)

        # Highlight coreference head specifically
        highlight_box = SurroundingRectangle(
            heatmaps[1], color=C["highlight"],
            buff=0.15, stroke_width=2,
        )
        note = safe_text(
            '"it" strongly attends to "animal"',
            font_size=TINY_SIZE, color=C["highlight"],
        ).move_to([0, BOTTOM_Y + 0.5, 0])

        self.play(Create(highlight_box), Write(note))
        self.wait(HOLD_MEDIUM)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(sentence),
            FadeOut(heatmaps), FadeOut(highlight_box),
            FadeOut(note),
            run_time=0.8,
        )

    def _build_heatmap(
        self,
        weights: list[list[float]],
        tokens: list[str],
        label: str,
        color,
    ) -> VGroup:
        """Build a 4x4 heatmap grid with row/column labels."""
        cell_size = 0.45
        n = len(tokens)
        grid = VGroup()

        # Cells
        for row in range(n):
            for col in range(n):
                w = weights[row][col]
                cell = Square(
                    side_length=cell_size,
                    color=color,
                    fill_color=color,
                    fill_opacity=max(0.3, w),  # min 0.3 per rules
                    stroke_width=0.5,
                    stroke_color=GRAY,
                )
                cell.move_to([col * cell_size, -row * cell_size, 0])
                grid.add(cell)

        grid.move_to(ORIGIN)

        # Row labels (left side -- queries)
        row_labels = VGroup()
        for i, tok in enumerate(tokens):
            lbl = safe_text(
                tok, font_size=TINY_SIZE - 4, color=WHITE,
            )
            target_y = grid[i * n].get_center()[1]
            lbl.move_to([
                grid[0].get_left()[0] - 0.4,
                target_y, 0,
            ])
            if lbl.width > 0.7:
                lbl.scale_to_fit_width(0.7)
            row_labels.add(lbl)

        # Column labels (top -- keys)
        col_labels = VGroup()
        for j, tok in enumerate(tokens):
            lbl = safe_text(
                tok, font_size=TINY_SIZE - 4, color=WHITE,
            )
            target_x = grid[j].get_center()[0]
            lbl.move_to([
                target_x,
                grid[0].get_top()[1] + 0.3,
                0,
            ])
            lbl.rotate(PI / 4)
            if lbl.width > 0.7:
                lbl.scale_to_fit_width(0.7)
            col_labels.add(lbl)

        # Title label
        title_lbl = safe_text(
            label, font_size=TINY_SIZE - 2, color=color,
        )
        title_lbl.next_to(
            VGroup(grid, col_labels), UP, buff=0.25,
        )

        return VGroup(grid, row_labels, col_labels, title_lbl)

    # ------------------------------------------------------------------
    # Phase 4: Concatenation and W^O projection
    # ------------------------------------------------------------------
    def _phase_concat_project(self):
        title = section_title("Concat & Project")
        self.play(Write(title))
        self.wait(0.5)

        # 8 colored output segments on the left
        seg_height = 0.5
        seg_width = 0.8
        output_segs = VGroup()
        for i in range(8):
            seg = Rectangle(
                width=seg_width, height=seg_height,
                color=HEAD_COLORS[i],
                fill_color=HEAD_COLORS[i],
                fill_opacity=0.4,
                stroke_width=2,
            )
            output_segs.add(seg)

        output_segs.arrange(DOWN, buff=0.05)
        output_segs.move_to([-4.0, 0, 0])

        head_labels = VGroup()
        for i, seg in enumerate(output_segs):
            lbl = safe_text(
                f"H{i+1}", font_size=TINY_SIZE - 2,
                color=HEAD_COLORS[i],
            ).next_to(seg, LEFT, buff=0.2)
            head_labels.add(lbl)

        self.play(
            *[FadeIn(s, shift=RIGHT * 0.1) for s in output_segs],
            *[Write(l) for l in head_labels],
            run_time=1.0,
        )
        self.wait(0.5)

        # Concat arrow
        concat_arrow = Arrow(
            output_segs.get_right() + RIGHT * 0.2,
            [-1.0, 0, 0],
            color=WHITE, stroke_width=2,
            max_tip_length_to_length_ratio=0.1,
        )
        concat_label = safe_text(
            "Concat", font_size=LABEL_SIZE, color=C["label"],
        ).next_to(concat_arrow, UP, buff=0.15)

        # Concatenated vector
        concat_rect = Rectangle(
            width=0.8, height=4.2,
            color=WHITE, fill_opacity=0.15,
            stroke_width=2,
        ).move_to([0, 0, 0])

        # Color stripes inside concat rect
        stripe_height = 4.2 / 8
        stripes = VGroup()
        for i in range(8):
            stripe = Rectangle(
                width=0.75, height=stripe_height - 0.02,
                color=HEAD_COLORS[i],
                fill_color=HEAD_COLORS[i],
                fill_opacity=0.3,
                stroke_width=0,
            )
            y_pos = concat_rect.get_top()[1] - (i + 0.5) * stripe_height
            stripe.move_to([0, y_pos, 0])
            stripes.add(stripe)

        concat_dim_label = safe_text(
            "512", font_size=TINY_SIZE, color=WHITE,
        ).next_to(concat_rect, DOWN, buff=0.2)

        self.play(
            GrowArrow(concat_arrow),
            Write(concat_label),
            run_time=0.8,
        )
        self.play(
            FadeIn(concat_rect),
            *[FadeIn(s) for s in stripes],
            Write(concat_dim_label),
            run_time=0.8,
        )
        self.wait(0.5)

        # W^O projection
        proj_arrow = Arrow(
            concat_rect.get_right() + RIGHT * 0.2,
            [3.0, 0, 0],
            color=C["attention"], stroke_width=2,
            max_tip_length_to_length_ratio=0.1,
        )
        wo_label = MathTex(r"W^O", font_size=EQ_SMALL, color=C["attention"])
        wo_label.next_to(proj_arrow, UP, buff=0.15)

        # Final output vector
        final_rect = Rectangle(
            width=0.8, height=4.2,
            color=C["attention"],
            fill_color=C["attention"],
            fill_opacity=0.15,
            stroke_width=2,
        ).move_to([4.5, 0, 0])
        final_label = safe_text(
            "Output\n512-dim", font_size=TINY_SIZE,
            color=C["attention"],
        ).next_to(final_rect, DOWN, buff=0.2)

        self.play(
            GrowArrow(proj_arrow),
            Write(wo_label),
            run_time=0.8,
        )
        self.play(
            FadeIn(final_rect, shift=RIGHT * 0.2),
            Write(final_label),
            run_time=0.8,
        )
        self.wait(HOLD_MEDIUM)

        # Cleanup
        self.play(
            FadeOut(title),
            FadeOut(output_segs), FadeOut(head_labels),
            FadeOut(concat_arrow), FadeOut(concat_label),
            FadeOut(concat_rect), FadeOut(stripes),
            FadeOut(concat_dim_label),
            FadeOut(proj_arrow), FadeOut(wo_label),
            FadeOut(final_rect), FadeOut(final_label),
            run_time=0.8,
        )

    # ------------------------------------------------------------------
    # Phase 5: Formula
    # ------------------------------------------------------------------
    def _phase_formula(self):
        title = section_title("Multi-Head Attention Formula")
        self.play(Write(title))
        self.wait(0.5)

        # Main formula
        formula = MathTex(
            r"\text{MultiHead}(Q, K, V)",
            r"=",
            r"\text{Concat}(\text{head}_1, \dots, \text{head}_h)",
            r"\cdot",
            r"W^O",
            font_size=EQ_SIZE,
        )
        formula[0].set_color(C["attention"])
        formula[2].set_color(WHITE)
        formula[4].set_color(C["attention"])

        if formula.width > SAFE_WIDTH - 1:
            formula.scale_to_fit_width(SAFE_WIDTH - 1)
        formula.move_to([0, 0.5, 0])

        # Sub-formula for each head
        head_formula = MathTex(
            r"\text{head}_i",
            r"=",
            r"\text{Attention}(",
            r"Q W_i^Q",
            r",\;",
            r"K W_i^K",
            r",\;",
            r"V W_i^V",
            r")",
            font_size=EQ_SMALL,
        )
        head_formula[0].set_color(C["attention"])
        head_formula[3].set_color(C["query"])
        head_formula[5].set_color(C["key"])
        head_formula[7].set_color(C["value"])

        if head_formula.width > SAFE_WIDTH - 1:
            head_formula.scale_to_fit_width(SAFE_WIDTH - 1)
        head_formula.move_to([0, -0.7, 0])

        # Dimension note
        dim_note = safe_text(
            "h = 8,  d_k = d_v = d_model / h = 64",
            font_size=TINY_SIZE, color=C["dim"],
        ).move_to([0, -1.8, 0])

        self.play(Write(formula), run_time=1.5)
        self.wait(HOLD_SHORT)
        self.play(Write(head_formula), run_time=1.5)
        self.wait(HOLD_SHORT)
        self.play(Write(dim_note), run_time=0.6)
        self.wait(HOLD_SHORT)

        # Bottom note about computational cost
        cost_note = bottom_note(
            "Same total computation as single-head with d_model dimensions"
        )
        self.play(Write(cost_note))
        self.wait(HOLD_LONG)

        # Final fadeout
        self.play(
            FadeOut(title), FadeOut(formula),
            FadeOut(head_formula), FadeOut(dim_note),
            FadeOut(cost_note),
            run_time=1.0,
        )
