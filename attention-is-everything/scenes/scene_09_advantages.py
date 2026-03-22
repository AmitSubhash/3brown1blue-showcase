"""Scene 09: Why It Works -- Computational Advantages (~60 seconds).

Compares Transformer computational complexity against RNNs and CNNs,
visualizes sequential vs parallel processing, shows BLEU score results,
and highlights training cost savings.
"""

from manim import *
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.style import (
    BG_COLOR, C, TITLE_Y, SUBTITLE_Y, BOTTOM_Y,
    SAFE_WIDTH, SAFE_X, SAFE_Y,
    TITLE_SIZE, SUBTITLE_SIZE, BODY_SIZE, LABEL_SIZE, EQ_SIZE,
    EQ_SMALL, TINY_SIZE,
    HOLD_SHORT, HOLD_MEDIUM, HOLD_LONG, DIM_OPACITY,
    LEFT_CENTER, RIGHT_CENTER, PANEL_WIDTH,
    section_title, subtitle, body_text, safe_text, bottom_note,
    labeled_box, story_bridge, arrow_between,
)


# ── Helpers ──────────────────────────────────────────────────────────

def table_cell(text: str, width: float = 2.5, height: float = 0.55,
               color=WHITE, font_size: int = TINY_SIZE,
               fill_opacity: float = 0.0, fill_color=WHITE) -> VGroup:
    """A single cell for the comparison table."""
    rect = Rectangle(
        width=width, height=height,
        stroke_color=GRAY, stroke_width=1,
        fill_opacity=fill_opacity, fill_color=fill_color,
    )
    txt = safe_text(text, font_size=font_size, color=color, max_width=width - 0.2)
    txt.move_to(rect)
    return VGroup(rect, txt)


def token_dot(color=WHITE, radius: float = 0.12) -> Dot:
    """A small dot representing a token."""
    return Dot(radius=radius, color=color, fill_opacity=0.85)


# ── Scene ────────────────────────────────────────────────────────────

class ComputationalAdvantages(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        self.complexity_table()
        self.parallelization_visual()
        self.bleu_scores()
        self.training_cost()

    # ── Phase 1: Complexity Comparison Table ──────────────────────────

    def complexity_table(self):
        title = section_title("Computational Complexity")
        self.play(Write(title), run_time=0.7)

        # Table dimensions
        col_widths = [2.6, 2.8, 2.0, 2.0]
        row_height = 0.55

        # Header row
        headers = ["Layer Type", "Complexity", "Sequential", "Max Path"]
        header_cells = VGroup()
        for i, h in enumerate(headers):
            cell = table_cell(
                h, width=col_widths[i], height=row_height,
                color=C["highlight"], font_size=TINY_SIZE,
                fill_opacity=0.15, fill_color=C["highlight"],
            )
            header_cells.add(cell)
        header_cells.arrange(RIGHT, buff=0)

        # Data rows
        rows_data = [
            ("Self-Attention", "O(n^2 d)", "O(1)", "O(1)"),
            ("Recurrent", "O(n d^2)", "O(n)", "O(n)"),
            ("Convolutional", "O(k n d^2)", "O(1)", "O(log n)"),
        ]
        row_colors = [C["transformer"], C["rnn"], GRAY_B]

        data_rows = VGroup()
        for r_idx, (layer, comp, seq, path) in enumerate(rows_data):
            cells = VGroup()
            row_vals = [layer, comp, seq, path]
            for c_idx, val in enumerate(row_vals):
                cell = table_cell(
                    val, width=col_widths[c_idx], height=row_height,
                    color=row_colors[r_idx], font_size=TINY_SIZE,
                )
                cells.add(cell)
            cells.arrange(RIGHT, buff=0)
            data_rows.add(cells)

        # Assemble table
        full_table = VGroup(header_cells, *data_rows)
        full_table.arrange(DOWN, buff=0)
        full_table.move_to(DOWN * 0.3)

        # Animate: header first, then rows one by one
        self.play(FadeIn(header_cells, shift=DOWN * 0.15), run_time=0.5)
        for row in data_rows:
            self.play(FadeIn(row, shift=DOWN * 0.1), run_time=0.4)

        # Highlight self-attention row advantages
        highlight_rect = SurroundingRectangle(
            data_rows[0], color=C["transformer"], buff=0.06, stroke_width=2.5,
        )
        advantage_note = safe_text(
            "Constant sequential ops + constant path length",
            font_size=TINY_SIZE, color=C["transformer"],
        )
        advantage_note.next_to(full_table, DOWN, buff=0.4)

        self.play(Create(highlight_rect), run_time=0.5)
        self.play(Write(advantage_note), run_time=0.6)
        self.wait(HOLD_MEDIUM)

        self.table_group = VGroup(
            title, full_table, highlight_rect, advantage_note,
        )
        self.play(FadeOut(self.table_group), run_time=0.6)

    # ── Phase 2: Sequential vs Parallel Processing ───────────────────

    def parallelization_visual(self):
        title = section_title("Parallelization")
        self.play(Write(title), run_time=0.6)

        # Panel labels
        rnn_label = safe_text("RNN (Sequential)", font_size=LABEL_SIZE,
                              color=C["rnn"])
        rnn_label.move_to(LEFT_CENTER * RIGHT + UP * 2.2)

        tf_label = safe_text("Transformer (Parallel)", font_size=LABEL_SIZE,
                             color=C["transformer"])
        tf_label.move_to(RIGHT_CENTER * RIGHT + UP * 2.2)

        # Divider
        divider = DashedLine(
            UP * 2.0, DOWN * 2.8,
            color=GRAY, stroke_width=1, dash_length=0.15,
        )

        self.play(
            Write(rnn_label), Write(tf_label),
            Create(divider),
            run_time=0.6,
        )

        # -- LEFT PANEL: RNN sequential processing --
        n_tokens = 6
        rnn_dots = VGroup()
        rnn_pipe_x_start = LEFT_CENTER - 2.0
        rnn_pipe_x_end = LEFT_CENTER + 2.0
        rnn_y = 0.0

        # Processing pipe
        pipe = RoundedRectangle(
            width=4.2, height=0.7, corner_radius=0.15,
            color=C["rnn"], fill_opacity=0.1, stroke_width=1.5,
        )
        pipe.move_to(LEFT_CENTER * RIGHT + rnn_y * UP)
        pipe_label = safe_text("RNN Cell", font_size=TINY_SIZE, color=C["rnn"])
        pipe_label.move_to(pipe.get_center() + DOWN * 0.55)

        # Queue of dots waiting
        for i in range(n_tokens):
            d = token_dot(color=C["rnn"], radius=0.14)
            d.move_to(LEFT_CENTER * RIGHT + LEFT * (1.8 - i * 0.55) + UP * 1.2)
            d.set_opacity(0.4)
            rnn_dots.add(d)

        self.play(
            Create(pipe), Write(pipe_label),
            *[FadeIn(d, scale=0.5) for d in rnn_dots],
            run_time=0.6,
        )

        # Animate sequential processing: each dot moves through pipe one at a time
        processed_rnn = VGroup()
        for i in range(n_tokens):
            dot = rnn_dots[i]
            target_in = pipe.get_left() + RIGHT * 0.4
            target_out = LEFT_CENTER * RIGHT + RIGHT * (i * 0.55 - 1.3) + DOWN * 1.5
            self.play(
                dot.animate.move_to(target_in).set_opacity(1.0),
                run_time=0.15,
            )
            self.play(
                dot.animate.move_to(target_out).set_color(C["positive"]),
                run_time=0.15,
            )
            processed_rnn.add(dot)

        slow_label = safe_text("Slow", font_size=BODY_SIZE, color=C["negative"])
        slow_label.move_to(LEFT_CENTER * RIGHT + DOWN * 2.5)

        # -- RIGHT PANEL: Transformer parallel processing --
        tf_dots = VGroup()
        for i in range(n_tokens):
            d = token_dot(color=C["transformer"], radius=0.14)
            d.move_to(RIGHT_CENTER * RIGHT + LEFT * (1.3 - i * 0.55) + UP * 1.2)
            d.set_opacity(0.4)
            tf_dots.add(d)

        # Attention block
        attn_block = RoundedRectangle(
            width=4.2, height=0.7, corner_radius=0.15,
            color=C["transformer"], fill_opacity=0.1, stroke_width=1.5,
        )
        attn_block.move_to(RIGHT_CENTER * RIGHT + rnn_y * UP)
        attn_label = safe_text("Self-Attention", font_size=TINY_SIZE,
                               color=C["transformer"])
        attn_label.move_to(attn_block.get_center() + DOWN * 0.55)

        self.play(
            Create(attn_block), Write(attn_label),
            *[FadeIn(d, scale=0.5) for d in tf_dots],
            run_time=0.5,
        )

        # ALL dots process simultaneously
        tf_targets = VGroup()
        anims = []
        for i, dot in enumerate(tf_dots):
            target = RIGHT_CENTER * RIGHT + LEFT * (1.3 - i * 0.55) + DOWN * 1.5
            anims.append(dot.animate.move_to(target).set_color(C["positive"]).set_opacity(1.0))

        # Flash the attention block
        flash = attn_block.copy()
        flash.set_fill(C["transformer"], opacity=0.4)
        self.play(
            FadeIn(flash, run_time=0.15),
            FadeOut(flash, run_time=0.25),
            *anims,
            run_time=0.4,
        )

        fast_label = safe_text("Fast!", font_size=BODY_SIZE, color=C["positive"])
        fast_label.move_to(RIGHT_CENTER * RIGHT + DOWN * 2.5)

        self.play(Write(slow_label), Write(fast_label), run_time=0.5)
        self.wait(HOLD_MEDIUM)

        # Cleanup
        parallel_group = VGroup(
            title, rnn_label, tf_label, divider,
            pipe, pipe_label, rnn_dots, slow_label,
            attn_block, attn_label, tf_dots, fast_label,
        )
        self.play(FadeOut(parallel_group), run_time=0.6)

    # ── Phase 3: BLEU Score Bar Chart ────────────────────────────────

    def bleu_scores(self):
        title = section_title("Translation Quality (BLEU)")
        self.play(Write(title), run_time=0.6)

        # Data
        models = ["GNMT+RL", "ConvS2S", "Transformer\n(base)", "Transformer\n(big)"]
        scores = [24.6, 25.16, 27.3, 28.4]
        bar_colors = [GRAY_B, GRAY_B, BLUE_C, BLUE_B]
        fill_opacities = [0.6, 0.6, 0.75, 0.85]

        # Chart dimensions
        chart_bottom = -2.2
        chart_top = 2.0
        chart_left = -4.5
        bar_width = 1.6
        bar_gap = 0.5
        max_score = 30.0
        bar_height_range = chart_top - chart_bottom

        # Y axis
        y_axis = Line(
            chart_left * RIGHT + chart_bottom * UP,
            chart_left * RIGHT + chart_top * UP,
            color=GRAY, stroke_width=1.5,
        )
        # Y axis ticks
        y_ticks = VGroup()
        for val in [20, 22, 24, 26, 28, 30]:
            y_pos = chart_bottom + (val / max_score) * bar_height_range
            tick_line = Line(
                (chart_left - 0.1) * RIGHT + y_pos * UP,
                (chart_left + 0.1) * RIGHT + y_pos * UP,
                color=GRAY, stroke_width=1,
            )
            tick_label = Text(str(val), font_size=14, color=GRAY)
            tick_label.next_to(tick_line, LEFT, buff=0.1)
            y_ticks.add(VGroup(tick_line, tick_label))

        self.play(Create(y_axis), FadeIn(y_ticks), run_time=0.5)

        # Bars
        bars = VGroup()
        bar_labels = VGroup()
        score_labels = VGroup()

        for i, (model, score, color, opacity) in enumerate(
            zip(models, scores, bar_colors, fill_opacities)
        ):
            x = chart_left + 1.2 + i * (bar_width + bar_gap)
            h = (score / max_score) * bar_height_range
            bar = Rectangle(
                width=bar_width, height=h,
                fill_color=color, fill_opacity=opacity,
                stroke_color=color, stroke_width=1.5,
            )
            bar.move_to(x * RIGHT + (chart_bottom + h / 2) * UP)
            bars.add(bar)

            # Model name below
            m_label = safe_text(model, font_size=14, color=WHITE, max_width=bar_width)
            m_label.next_to(bar, DOWN, buff=0.12)
            bar_labels.add(m_label)

            # Score on top
            s_label = Text(str(score), font_size=TINY_SIZE, color=color)
            s_label.next_to(bar, UP, buff=0.08)
            score_labels.add(s_label)

        # Animate bars growing from bottom
        for bar in bars:
            bar.save_state()
            bar.stretch(0, 1, about_edge=DOWN)

        self.play(
            *[bar.animate.restore() for bar in bars],
            *[Write(bl) for bl in bar_labels],
            run_time=1.0,
        )
        self.play(
            *[FadeIn(sl, shift=UP * 0.1) for sl in score_labels],
            run_time=0.5,
        )

        # Highlight transformer (big) bar
        winner_rect = SurroundingRectangle(
            VGroup(bars[3], score_labels[3]),
            color=C["highlight"], buff=0.08, stroke_width=2,
        )
        self.play(Create(winner_rect), run_time=0.4)
        self.wait(HOLD_SHORT)

        # Cleanup
        self.bleu_group = VGroup(
            title, y_axis, y_ticks, bars, bar_labels, score_labels, winner_rect,
        )
        self.play(FadeOut(self.bleu_group), run_time=0.6)

    # ── Phase 4: Training Cost Comparison ────────────────────────────

    def training_cost(self):
        title = section_title("Training Cost")
        self.play(Write(title), run_time=0.6)

        # Scale / balance visual using two bars
        # Previous SOTA: large cost bar
        prev_label = safe_text("Previous SOTA", font_size=LABEL_SIZE, color=C["rnn"])
        prev_label.move_to(LEFT * 3.0 + UP * 1.5)

        prev_bar_bg = RoundedRectangle(
            width=5.0, height=0.7, corner_radius=0.1,
            color=C["rnn"], fill_opacity=0.0, stroke_width=1.5,
        )
        prev_bar_fill = RoundedRectangle(
            width=5.0, height=0.7, corner_radius=0.1,
            color=C["rnn"], fill_opacity=0.6, stroke_width=0,
        )
        prev_bar_bg.move_to(LEFT * 1.0 + UP * 0.7)
        prev_bar_fill.move_to(prev_bar_bg)
        prev_cost = safe_text("10^20 FLOPs", font_size=LABEL_SIZE, color=WHITE)
        prev_cost.move_to(prev_bar_bg)
        prev_group = VGroup(prev_bar_bg, prev_bar_fill, prev_cost)

        # Transformer (big): smaller cost bar
        tf_label = safe_text("Transformer (big)", font_size=LABEL_SIZE,
                             color=C["transformer"])
        tf_label.move_to(LEFT * 3.0 + DOWN * 0.5)

        tf_bar_bg = RoundedRectangle(
            width=5.0, height=0.7, corner_radius=0.1,
            color=C["transformer"], fill_opacity=0.0, stroke_width=1.5,
        )
        tf_bar_fill = RoundedRectangle(
            width=0.5, height=0.7, corner_radius=0.1,
            color=C["transformer"], fill_opacity=0.7, stroke_width=0,
        )
        tf_bar_bg.move_to(LEFT * 1.0 + DOWN * 1.1)
        tf_bar_fill.align_to(tf_bar_bg, LEFT)
        tf_cost = safe_text("10^19 FLOPs", font_size=LABEL_SIZE,
                            color=C["transformer"])
        tf_cost.move_to(tf_bar_bg)
        tf_group = VGroup(tf_bar_bg, tf_bar_fill, tf_cost)

        self.play(
            Write(prev_label), FadeIn(prev_group, shift=RIGHT * 0.3),
            run_time=0.6,
        )
        self.play(
            Write(tf_label), FadeIn(tf_group, shift=RIGHT * 0.3),
            run_time=0.6,
        )

        # "10x less!" annotation
        savings_arrow = Arrow(
            prev_bar_bg.get_right() + RIGHT * 0.3,
            tf_bar_bg.get_right() + RIGHT * 0.3,
            color=C["positive"], buff=0.1, stroke_width=3,
            max_tip_length_to_length_ratio=0.15,
        )
        savings_text = safe_text("10x less!", font_size=BODY_SIZE,
                                 color=C["positive"])
        savings_text.next_to(savings_arrow, RIGHT, buff=0.25)

        self.play(GrowArrow(savings_arrow), run_time=0.5)
        self.play(Write(savings_text), run_time=0.4)
        self.wait(HOLD_SHORT)

        # Conclusion text
        conclusion = safe_text("Faster AND Better", font_size=TITLE_SIZE,
                               color=C["highlight"])
        conclusion.move_to(DOWN * 2.6)

        self.play(Write(conclusion), run_time=0.8)
        self.wait(HOLD_LONG)

        # Final cleanup
        all_objs = VGroup(
            title, prev_label, prev_group, tf_label, tf_group,
            savings_arrow, savings_text, conclusion,
        )
        self.play(FadeOut(all_objs), run_time=0.8)
