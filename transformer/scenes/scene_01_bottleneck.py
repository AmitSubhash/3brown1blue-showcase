"""Scene 01: The Sequential Bottleneck (~90 seconds).

Why RNNs fail at long sequences. The information bottleneck.
Motivate WHY we need Transformers.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from manim import *
from utils.style import (
    BG_COLOR,
    C,
    TITLE_SIZE,
    SUBTITLE_SIZE,
    BODY_SIZE,
    LABEL_SIZE,
    TINY_SIZE,
    TITLE_Y,
    SUBTITLE_Y,
    BOTTOM_Y,
    SAFE_WIDTH,
    SAFE_X,
    SAFE_Y,
    LEFT_CENTER,
    RIGHT_CENTER,
    PANEL_WIDTH,
    HOLD_SHORT,
    HOLD_MEDIUM,
    HOLD_LONG,
    DIM_OPACITY,
    section_title,
    subtitle,
    body_text,
    safe_text,
    bottom_note,
    labeled_box,
    story_bridge,
    arrow_between,
)


# ── Scene-local constants ───────────────────────────────────────────
SENTENCE_TOKENS = [
    "The", "cat", "sat", "on", "the", "mat",
    "because", "it", "was", "tired",
]
RNN_BOX_SIZE = 0.55
RNN_ARROW_LEN = 0.35
INFO_BLUE = BLUE_C
INFO_FADED = GRAY_E


class SequentialBottleneck(Scene):
    """Scene 01: The Sequential Bottleneck."""

    def setup(self) -> None:
        self.camera.background_color = BG_COLOR

    def construct(self) -> None:
        self.next_section("Hook_Sentence")
        self._phase_sentence()

        self.next_section("RNN_Chain")
        self._phase_rnn_chain()

        self.next_section("Bottleneck")
        self._phase_bottleneck()

        self.next_section("DualPanel")
        self._phase_dual_panel()

        self.next_section("ClosingQuestion")
        self._phase_closing()

    # ── Phase 1: Show the sentence ──────────────────────────────────

    def _phase_sentence(self) -> None:
        """Display the example sentence with each word as a token."""
        title = section_title("The Sequential Bottleneck", color=C["rnn"])
        self.play(Write(title), run_time=1.0)
        self.wait(HOLD_SHORT)

        # Build token cards
        token_group = self._build_token_cards()
        token_group.move_to(ORIGIN)

        self.play(
            LaggedStart(
                *[FadeIn(t, shift=DOWN * 0.3) for t in token_group],
                lag_ratio=0.08,
            ),
            run_time=1.5,
        )
        self.wait(HOLD_MEDIUM)

        # Highlight "cat" and "tired" with labels
        cat_card = token_group[1]
        tired_card = token_group[9]

        cat_highlight = SurroundingRectangle(
            cat_card, color=INFO_BLUE, buff=0.08, stroke_width=2.5,
        )
        tired_highlight = SurroundingRectangle(
            tired_card, color=C["attention"], buff=0.08, stroke_width=2.5,
        )
        cat_label = safe_text(
            "subject", font_size=TINY_SIZE, color=INFO_BLUE,
        )
        cat_label.next_to(cat_highlight, UP, buff=0.15)
        tired_label = safe_text(
            "refers to cat?", font_size=TINY_SIZE, color=C["attention"],
        )
        tired_label.next_to(tired_highlight, DOWN, buff=0.15)

        self.play(
            Create(cat_highlight), Write(cat_label),
            Create(tired_highlight), Write(tired_label),
            run_time=1.0,
        )
        self.wait(HOLD_MEDIUM)

        # Store references then clean up
        self.play(
            FadeOut(title), FadeOut(token_group),
            FadeOut(cat_highlight), FadeOut(cat_label),
            FadeOut(tired_highlight), FadeOut(tired_label),
            run_time=0.8,
        )

    # ── Phase 2: RNN chain animation ────────────────────────────────

    def _phase_rnn_chain(self) -> None:
        """Animate tokens flowing through an RNN chain with fading info."""
        rnn_title = safe_text(
            "Recurrent Neural Network", font_size=SUBTITLE_SIZE,
            color=C["rnn"],
        )
        rnn_title.move_to(UP * TITLE_Y)
        self.play(Write(rnn_title), run_time=0.8)

        # Build the RNN chain: boxes + arrows, centered on screen
        n = len(SENTENCE_TOKENS)
        spacing = RNN_BOX_SIZE + RNN_ARROW_LEN + 0.1
        total_width = (n - 1) * spacing
        # Ensure it fits in safe area
        if total_width > SAFE_WIDTH - 1.0:
            spacing = (SAFE_WIDTH - 1.0) / (n - 1)
            total_width = (n - 1) * spacing

        start_x = -total_width / 2

        boxes = VGroup()
        arrows = VGroup()
        token_labels = VGroup()

        for i in range(n):
            x = start_x + i * spacing
            # Hidden state box -- starts with full blue fill for first box
            info_ratio = max(0.0, 1.0 - i * 0.12)
            box_color = interpolate_color(INFO_FADED, INFO_BLUE, info_ratio)

            box = RoundedRectangle(
                width=RNN_BOX_SIZE,
                height=RNN_BOX_SIZE,
                corner_radius=0.08,
                color=box_color,
                fill_opacity=0.7,
                stroke_width=1.5,
                stroke_color=WHITE,
            )
            box.move_to([x, 0, 0])
            boxes.add(box)

            # Hidden state label
            h_label = safe_text(
                f"h{i}", font_size=14, color=WHITE,
            )
            h_label.move_to(box)
            token_labels.add(h_label)

            # Arrow from previous box
            if i > 0:
                arr = Arrow(
                    boxes[i - 1].get_right(),
                    box.get_left(),
                    color=WHITE,
                    buff=0.05,
                    stroke_width=2,
                    max_tip_length_to_length_ratio=0.3,
                )
                arrows.add(arr)

        # Token input labels below boxes
        input_labels = VGroup()
        for i, token in enumerate(SENTENCE_TOKENS):
            lbl = safe_text(
                token, font_size=TINY_SIZE, color=C["label"],
            )
            lbl.next_to(boxes[i], DOWN, buff=0.35)
            input_labels.add(lbl)

        # Input arrows from token labels to boxes
        input_arrows = VGroup()
        for i in range(n):
            arr = Arrow(
                input_labels[i].get_top(),
                boxes[i].get_bottom(),
                color=GRAY,
                buff=0.05,
                stroke_width=1.5,
                max_tip_length_to_length_ratio=0.3,
            )
            input_arrows.add(arr)

        # Animate: tokens flow through one by one
        # First box appears
        self.play(
            FadeIn(boxes[0], scale=0.8),
            Write(token_labels[0]),
            FadeIn(input_labels[0], shift=DOWN * 0.2),
            GrowArrow(input_arrows[0]),
            run_time=0.5,
        )

        # Remaining boxes appear sequentially with arrows
        for i in range(1, n):
            self.play(
                GrowArrow(arrows[i - 1]),
                FadeIn(boxes[i], scale=0.8),
                Write(token_labels[i]),
                FadeIn(input_labels[i], shift=DOWN * 0.2),
                GrowArrow(input_arrows[i]),
                run_time=0.3,
            )

        self.wait(HOLD_SHORT)

        # Now animate the information fading: pulse color changes
        # to show early info diluting
        info_note = safe_text(
            "Information about early tokens fades...",
            font_size=LABEL_SIZE, color=C["attention"],
        )
        info_note.move_to(UP * (TITLE_Y - 0.8))
        self.play(Write(info_note), run_time=0.6)

        # Animate boxes changing color to show fading
        color_anims = []
        for i in range(n):
            info_ratio = max(0.0, 1.0 - i * 0.12)
            target_color = interpolate_color(INFO_FADED, INFO_BLUE, info_ratio)
            target_opacity = 0.3 + 0.5 * info_ratio
            new_box = boxes[i].copy()
            new_box.set_fill(target_color, opacity=target_opacity)
            new_box.set_stroke(
                interpolate_color(GRAY, WHITE, info_ratio), width=1.5,
            )
            color_anims.append(
                boxes[i].animate.set_fill(target_color, opacity=target_opacity)
            )

        self.play(*color_anims, run_time=1.5)
        self.wait(HOLD_SHORT)

        # Highlight: by the time we reach "tired", "cat" info is nearly gone
        cat_ghost = safe_text(
            '"cat" info', font_size=TINY_SIZE, color=INFO_BLUE,
        )
        cat_ghost.next_to(boxes[1], UP, buff=0.3)
        # Dashed path
        dashed_line = DashedLine(
            boxes[1].get_top() + UP * 0.5,
            boxes[9].get_top() + UP * 0.5,
            color=INFO_BLUE,
            dash_length=0.1,
            stroke_opacity=0.4,
        )
        fade_label = safe_text(
            "nearly gone!", font_size=TINY_SIZE, color=C["negative"],
        )
        fade_label.next_to(boxes[9], UP, buff=0.3)

        self.play(
            Write(cat_ghost),
            Create(dashed_line),
            Write(fade_label),
            run_time=1.0,
        )
        self.wait(HOLD_MEDIUM)

        # Store the chain for transition and clean up
        self.rnn_chain = VGroup(
            boxes, arrows, token_labels, input_labels, input_arrows,
        )
        self.play(
            FadeOut(info_note), FadeOut(cat_ghost),
            FadeOut(dashed_line), FadeOut(fade_label),
            FadeOut(rnn_title),
            run_time=0.6,
        )

    # ── Phase 3: Bottleneck funnel ──────────────────────────────────

    def _phase_bottleneck(self) -> None:
        """Show the fixed-length context vector as a bottleneck funnel."""
        # Fade out the chain
        self.play(FadeOut(self.rnn_chain), run_time=0.5)

        # Funnel visualization
        funnel_top = Polygon(
            [-3.0, 1.5, 0], [3.0, 1.5, 0],
            [0.5, -0.5, 0], [-0.5, -0.5, 0],
            color=C["rnn"],
            fill_opacity=0.3,
            stroke_width=2,
        )

        # Tiny context vector box at bottom
        ctx_box = RoundedRectangle(
            width=1.0, height=0.6,
            corner_radius=0.1,
            color=C["negative"],
            fill_opacity=0.6,
            stroke_width=2,
        )
        ctx_box.move_to([0, -1.5, 0])
        ctx_label = safe_text(
            "context\nvector", font_size=TINY_SIZE, color=WHITE,
        )
        ctx_label.move_to(ctx_box)

        # Token dots flowing into funnel
        token_dots = VGroup()
        colors = [
            INFO_BLUE, BLUE_D, TEAL_C, GREEN_C, BLUE_C,
            TEAL_C, PURPLE_C, BLUE_C, GREEN_C, YELLOW_C,
        ]
        for i, token in enumerate(SENTENCE_TOKENS):
            dot = Dot(
                point=[-3.5 + i * 0.78, 2.5, 0],
                radius=0.12,
                color=colors[i % len(colors)],
            )
            lbl = safe_text(token, font_size=12, color=WHITE)
            lbl.next_to(dot, UP, buff=0.08)
            token_dots.add(VGroup(dot, lbl))

        funnel_title = safe_text(
            "Everything must fit through a tiny bottleneck",
            font_size=BODY_SIZE, color=C["attention"],
        )
        funnel_title.move_to(UP * TITLE_Y)

        self.play(Write(funnel_title), run_time=0.8)
        self.play(
            FadeIn(funnel_top, shift=DOWN * 0.3),
            FadeIn(ctx_box, scale=0.8),
            Write(ctx_label),
            run_time=0.8,
        )

        # Animate tokens falling into funnel
        self.play(
            LaggedStart(
                *[FadeIn(td, shift=DOWN * 0.5) for td in token_dots],
                lag_ratio=0.06,
            ),
            run_time=1.2,
        )
        self.wait(0.5)

        # Tokens shrink and flow into the context box
        shrink_anims = []
        for td in token_dots:
            shrink_anims.append(
                td.animate.move_to(ctx_box.get_center()).scale(0.1).set_opacity(0.2)
            )
        self.play(
            LaggedStart(*shrink_anims, lag_ratio=0.05),
            run_time=2.0,
        )

        # Pulse the context box red to emphasize constraint
        self.play(
            ctx_box.animate.set_fill(C["negative"], opacity=0.9),
            rate_func=there_and_back,
            run_time=0.8,
        )
        self.play(
            ctx_box.animate.set_fill(C["negative"], opacity=0.9),
            rate_func=there_and_back,
            run_time=0.8,
        )

        self.wait(HOLD_SHORT)

        # Clean up
        self.play(
            FadeOut(funnel_title), FadeOut(funnel_top),
            FadeOut(ctx_box), FadeOut(ctx_label),
            FadeOut(token_dots),
            run_time=0.6,
        )

    # ── Phase 4: Dual panel comparison ──────────────────────────────

    def _phase_dual_panel(self) -> None:
        """Side-by-side: RNN sequential chain vs Transformer all-to-all."""
        # Panel divider
        divider = DashedLine(
            UP * (SAFE_Y[1] - 0.3), DOWN * (abs(SAFE_Y[0]) - 0.3),
            color=GRAY, dash_length=0.15, stroke_opacity=0.3,
        )

        # Left panel title: RNN
        left_title = safe_text(
            "RNN", font_size=SUBTITLE_SIZE, color=C["rnn"],
        )
        left_title.move_to([LEFT_CENTER, TITLE_Y - 0.3, 0])

        # Right panel title: Transformer
        right_title = safe_text(
            "Transformer", font_size=SUBTITLE_SIZE, color=C["transformer"],
        )
        right_title.move_to([RIGHT_CENTER, TITLE_Y - 0.3, 0])

        self.play(
            Create(divider),
            Write(left_title), Write(right_title),
            run_time=0.8,
        )

        # ── Left panel: sequential chain ────────────────────────────
        left_nodes = VGroup()
        n_nodes = 6
        chain_spacing = 0.7
        chain_start_y = 1.2
        for i in range(n_nodes):
            y = chain_start_y - i * chain_spacing
            info_ratio = max(0.0, 1.0 - i * 0.2)
            node_color = interpolate_color(INFO_FADED, INFO_BLUE, info_ratio)
            node = Dot(
                point=[LEFT_CENTER, y, 0],
                radius=0.18,
                color=node_color,
            )
            left_nodes.add(node)

        left_arrows = VGroup()
        for i in range(n_nodes - 1):
            arr = Arrow(
                left_nodes[i].get_bottom(),
                left_nodes[i + 1].get_top(),
                color=GRAY_B,
                buff=0.05,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.25,
            )
            left_arrows.add(arr)

        # O(n) label
        left_complexity = safe_text(
            "O(n) path length", font_size=LABEL_SIZE, color=C["negative"],
        )
        left_complexity.move_to([LEFT_CENTER, BOTTOM_Y + 0.5, 0])

        self.play(
            LaggedStart(
                *[FadeIn(n, scale=0.5) for n in left_nodes],
                lag_ratio=0.1,
            ),
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                *[GrowArrow(a) for a in left_arrows],
                lag_ratio=0.1,
            ),
            run_time=0.6,
        )
        self.play(Write(left_complexity), run_time=0.5)

        # ── Right panel: fully connected graph ──────────────────────
        right_nodes = VGroup()
        radius = 1.3
        for i in range(n_nodes):
            angle = PI / 2 + i * TAU / n_nodes
            x = RIGHT_CENTER + radius * np.cos(angle)
            y = 0.3 + radius * np.sin(angle)
            node = Dot(
                point=[x, y, 0],
                radius=0.18,
                color=C["transformer"],
            )
            right_nodes.add(node)

        # Edges: every node connected to every other
        right_edges = VGroup()
        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                edge = Line(
                    right_nodes[i].get_center(),
                    right_nodes[j].get_center(),
                    color=C["transformer"],
                    stroke_width=1.2,
                    stroke_opacity=0.35,
                )
                right_edges.add(edge)

        # O(1) label
        right_complexity = safe_text(
            "O(1) path length", font_size=LABEL_SIZE, color=C["positive"],
        )
        right_complexity.move_to([RIGHT_CENTER, BOTTOM_Y + 0.5, 0])

        self.play(
            LaggedStart(
                *[FadeIn(n, scale=0.5) for n in right_nodes],
                lag_ratio=0.08,
            ),
            run_time=0.6,
        )
        self.play(
            LaggedStart(
                *[Create(e) for e in right_edges],
                lag_ratio=0.02,
            ),
            run_time=1.5,
        )
        self.play(Write(right_complexity), run_time=0.5)

        self.wait(HOLD_MEDIUM)

        # Highlight: pulse a pair in the transformer graph
        # to show direct connection
        highlight_edge = Line(
            right_nodes[0].get_center(),
            right_nodes[3].get_center(),
            color=C["attention"],
            stroke_width=4,
            stroke_opacity=1.0,
        )
        self.play(Create(highlight_edge), run_time=0.5)
        self.play(
            highlight_edge.animate.set_stroke(opacity=0.3),
            rate_func=there_and_back,
            run_time=0.8,
        )

        self.wait(HOLD_SHORT)

        # Store for cleanup
        self.dual_panel = VGroup(
            divider, left_title, right_title,
            left_nodes, left_arrows, left_complexity,
            right_nodes, right_edges, right_complexity,
            highlight_edge,
        )

    # ── Phase 5: Closing question ───────────────────────────────────

    def _phase_closing(self) -> None:
        """End with the motivating question."""
        self.play(FadeOut(self.dual_panel), run_time=0.8)

        question = safe_text(
            "What if every word could talk to\nevery other word directly?",
            font_size=TITLE_SIZE,
            color=C["attention"],
        )
        question.move_to(ORIGIN)

        self.play(Write(question), run_time=2.0)
        self.wait(HOLD_LONG)
        self.play(FadeOut(question, shift=UP * 0.5), run_time=1.0)

    # ── Helpers ─────────────────────────────────────────────────────

    def _build_token_cards(self) -> VGroup:
        """Build styled token cards for the sentence."""
        cards = VGroup()
        for token in SENTENCE_TOKENS:
            rect = RoundedRectangle(
                width=1.0,
                height=0.55,
                corner_radius=0.1,
                color=WHITE,
                fill_opacity=0.08,
                stroke_width=1.5,
                stroke_color=GRAY_B,
            )
            label = safe_text(
                token, font_size=LABEL_SIZE, color=WHITE,
            )
            label.move_to(rect)
            if label.width > rect.width - 0.15:
                label.scale_to_fit_width(rect.width - 0.15)
            cards.add(VGroup(rect, label))

        cards.arrange(RIGHT, buff=0.15)
        # Scale down if too wide
        if cards.width > SAFE_WIDTH - 0.5:
            cards.scale_to_fit_width(SAFE_WIDTH - 0.5)
        return cards
