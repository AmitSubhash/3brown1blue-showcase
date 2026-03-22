"""Scene 07 -- The Decoder and Causal Masking (~90 seconds).

Covers:
  1. Encoder self-attention recap (bidirectional)
  2. Decoder autoregressive constraint
  3. Causal mask on 6x6 attention grid
  4. Growing mask during generation
  5. Cross-attention (decoder queries -> encoder keys/values)
  6. Three attention types summary
"""

from manim import *
import numpy as np
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.style import (
    BG_COLOR, C, TITLE_Y, SUBTITLE_Y, BOTTOM_Y,
    TITLE_SIZE, SUBTITLE_SIZE, BODY_SIZE, LABEL_SIZE, TINY_SIZE,
    EQ_SIZE, EQ_SMALL,
    SAFE_WIDTH, SAFE_X, SAFE_Y,
    LEFT_CENTER, RIGHT_CENTER, PANEL_WIDTH,
    HOLD_SHORT, HOLD_MEDIUM, HOLD_LONG, DIM_OPACITY,
    section_title, subtitle, body_text, safe_text, bottom_note,
    labeled_box, story_bridge, arrow_between,
)


# ---------------------------------------------------------------------------
# Helper: build an NxN attention grid
# ---------------------------------------------------------------------------

def build_attention_grid(
    n: int,
    cell_size: float = 0.55,
    row_labels: list[str] | None = None,
    col_labels: list[str] | None = None,
) -> tuple[VGroup, list[list[Square]], VGroup, VGroup]:
    """Return (grid_group, cells[][], row_label_mobjects, col_label_mobjects).

    cells[row][col] is the Square at that position.
    """
    cells: list[list[Square]] = []
    all_squares = VGroup()
    for r in range(n):
        row = []
        for c in range(n):
            sq = Square(side_length=cell_size, stroke_width=1.5, stroke_color=GRAY)
            sq.move_to(np.array([c * cell_size, -r * cell_size, 0]))
            row.append(sq)
            all_squares.add(sq)
        cells.append(row)
    # center the grid
    all_squares.move_to(ORIGIN)

    rl_group = VGroup()
    cl_group = VGroup()
    if row_labels:
        for r, lbl in enumerate(row_labels):
            t = safe_text(lbl, max_width=cell_size * 1.8,
                          font_size=TINY_SIZE, color=C["label"])
            t.next_to(cells[r][0], LEFT, buff=0.15)
            rl_group.add(t)
    if col_labels:
        for c_idx, lbl in enumerate(col_labels):
            t = safe_text(lbl, max_width=cell_size * 1.8,
                          font_size=TINY_SIZE, color=C["label"])
            t.next_to(cells[0][c_idx], UP, buff=0.15)
            cl_group.add(t)

    grid_group = VGroup(all_squares, rl_group, cl_group)
    return grid_group, cells, rl_group, cl_group


# ---------------------------------------------------------------------------
# Main Scene
# ---------------------------------------------------------------------------

class DecoderCausalMasking(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        self.part1_encoder_recap()
        self.part2_causal_mask()
        self.part3_growing_mask()
        self.part4_cross_attention()
        self.part5_summary()

    # -----------------------------------------------------------------------
    # Part 1 -- Encoder recap (bidirectional self-attention)  ~12s
    # -----------------------------------------------------------------------
    def part1_encoder_recap(self):
        title = section_title("Encoder Self-Attention", color=C["encoder"])
        self.play(Write(title))
        self.wait(0.5)

        # Show a row of words with bidirectional arrows
        words = ["The", "cat", "sat", "on", "the", "mat"]
        word_mobs = VGroup()
        for w in words:
            t = safe_text(w, font_size=BODY_SIZE, color=WHITE, max_width=1.5)
            word_mobs.add(t)
        word_mobs.arrange(RIGHT, buff=0.5)
        word_mobs.move_to(ORIGIN)

        self.play(FadeIn(word_mobs, shift=UP * 0.2))
        self.wait(0.5)

        # Bidirectional arrows: show a few curved arrows between non-adjacent words
        bi_arrows = VGroup()
        pairs = [(0, 5), (1, 3), (2, 4), (0, 2)]
        for i, j in pairs:
            arr = CurvedArrow(
                word_mobs[i].get_top() + UP * 0.1,
                word_mobs[j].get_top() + UP * 0.1,
                angle=-0.4,
                color=C["encoder"],
                stroke_width=2,
            )
            bi_arrows.add(arr)

        note = safe_text(
            "Every word attends to every other word",
            font_size=LABEL_SIZE, color=C["encoder"], max_width=SAFE_WIDTH,
        )
        note.next_to(word_mobs, DOWN, buff=0.8)

        self.play(
            *[Create(a) for a in bi_arrows],
            Write(note),
            run_time=1.5,
        )
        self.wait(HOLD_MEDIUM)

        # Clear
        self.play(
            FadeOut(title), FadeOut(word_mobs),
            FadeOut(bi_arrows), FadeOut(note),
        )

    # -----------------------------------------------------------------------
    # Part 2 -- Causal mask on 6x6 grid  ~25s
    # -----------------------------------------------------------------------
    def part2_causal_mask(self):
        title = section_title("Causal Masking in the Decoder", color=C["decoder"])
        self.play(Write(title))
        self.wait(0.5)

        problem = safe_text(
            "The decoder generates tokens left to right.",
            font_size=LABEL_SIZE, color=C["attention"], max_width=SAFE_WIDTH,
        )
        problem.move_to(UP * SUBTITLE_Y)
        self.play(Write(problem))
        self.wait(HOLD_SHORT)

        problem2 = safe_text(
            "Token at position 5 must NOT peek at positions 6, 7, 8 ...",
            font_size=LABEL_SIZE, color=C["negative"], max_width=SAFE_WIDTH,
        )
        problem2.next_to(problem, DOWN, buff=0.3)
        self.play(Write(problem2))
        self.wait(HOLD_MEDIUM)

        self.play(FadeOut(problem), FadeOut(problem2))

        # Build 6x6 grid
        tokens = ["<s>", "J'", "aime", "le", "petit", "chat"]
        grid_group, cells, rl, cl = build_attention_grid(
            6, cell_size=0.6, row_labels=tokens, col_labels=tokens,
        )
        grid_group.move_to(DOWN * 0.3)
        self.play(FadeIn(grid_group), run_time=1.0)
        self.wait(0.5)

        # Label axes
        q_label = safe_text("Query (output pos)", font_size=TINY_SIZE,
                            color=C["query"], max_width=4.0)
        q_label.next_to(grid_group, LEFT, buff=0.6).shift(DOWN * 0.3)
        q_label.rotate(PI / 2)
        k_label = safe_text("Key (input pos)", font_size=TINY_SIZE,
                            color=C["key"], max_width=4.0)
        k_label.next_to(grid_group, UP, buff=0.5)
        self.play(Write(q_label), Write(k_label))
        self.wait(0.5)

        # Fill lower triangle (valid) with green gradient
        np.random.seed(42)  # reproducible
        lower_anims = []
        for r in range(6):
            for c in range(r + 1):
                opacity = 0.3 + 0.4 * np.random.random()
                lower_anims.append(
                    cells[r][c].animate.set_fill(C["positive"], opacity=opacity)
                )
        self.play(*lower_anims, run_time=1.0)
        self.wait(0.5)

        # Animate upper triangle: fill red + label "-inf"
        upper_anims = []
        inf_labels = VGroup()
        for r in range(6):
            for c in range(r + 1, 6):
                upper_anims.append(
                    cells[r][c].animate.set_fill(C["mask"], opacity=0.7)
                )
                inf_t = safe_text("-inf", font_size=10, color=WHITE, max_width=0.5)
                inf_t.move_to(cells[r][c])
                inf_labels.add(inf_t)

        mask_note = safe_text(
            "Upper triangle masked with -inf",
            font_size=LABEL_SIZE, color=C["mask"], max_width=SAFE_WIDTH,
        )
        mask_note.move_to(DOWN * abs(BOTTOM_Y) + UP * 0.3)

        self.play(*upper_anims, FadeIn(inf_labels), Write(mask_note), run_time=1.5)
        self.wait(HOLD_MEDIUM)

        # After softmax: red cells become black (zero probability)
        softmax_note = safe_text(
            "After softmax: masked positions become 0",
            font_size=LABEL_SIZE, color=C["attention"], max_width=SAFE_WIDTH,
        )
        softmax_note.move_to(mask_note.get_center())

        zero_anims = []
        zero_labels = VGroup()
        for r in range(6):
            for c in range(r + 1, 6):
                zero_anims.append(
                    cells[r][c].animate.set_fill(BLACK, opacity=0.8)
                )
                z_t = safe_text("0", font_size=10, color=GRAY, max_width=0.4)
                z_t.move_to(cells[r][c])
                zero_labels.add(z_t)

        self.play(
            *zero_anims,
            ReplacementTransform(inf_labels, zero_labels),
            ReplacementTransform(mask_note, softmax_note),
            run_time=1.5,
        )
        self.wait(HOLD_MEDIUM)

        # Store references for next part
        self.grid_group = grid_group
        self.cells = cells
        self.rl = rl
        self.cl = cl
        self.q_label = q_label
        self.k_label = k_label
        self.zero_labels = zero_labels
        self.softmax_note = softmax_note
        self.title_p2 = title

    # -----------------------------------------------------------------------
    # Part 3 -- Growing mask during autoregressive generation  ~20s
    # -----------------------------------------------------------------------
    def part3_growing_mask(self):
        # Clear previous grid
        self.play(
            FadeOut(self.grid_group), FadeOut(self.q_label),
            FadeOut(self.k_label), FadeOut(self.zero_labels),
            FadeOut(self.softmax_note), FadeOut(self.title_p2),
        )

        title = section_title("Autoregressive Generation", color=C["decoder"])
        self.play(Write(title))
        self.wait(0.5)

        tokens = ["<s>", "J'", "aime", "le", "petit", "chat"]
        cell_size = 0.65
        n = 6

        grid_group, cells, rl, cl = build_attention_grid(
            n, cell_size=cell_size, row_labels=tokens, col_labels=tokens,
        )
        grid_group.move_to(DOWN * 0.2)
        # Start with all cells dark
        for r in range(n):
            for c in range(n):
                cells[r][c].set_fill(BLACK, opacity=0.6)

        self.play(FadeIn(grid_group), run_time=0.8)

        step_label = safe_text("Step 1: only '<s>' visible",
                               font_size=LABEL_SIZE, color=C["attention"],
                               max_width=SAFE_WIDTH)
        step_label.move_to(DOWN * abs(BOTTOM_Y) + UP * 0.3)
        self.play(Write(step_label))

        # Animate steps: reveal one more row at a time
        step_descriptions = [
            "Step 1: '<s>' attends to itself",
            "Step 2: 'J'' attends to '<s>', 'J''",
            "Step 3: 'aime' attends to '<s>', 'J'', 'aime'",
            "Step 4: 'le' sees previous 4 tokens",
            "Step 5: 'petit' sees previous 5 tokens",
            "Step 6: 'chat' sees all 6 tokens",
        ]

        for step in range(n):
            # Reveal cells[step][0..step]
            reveal_anims = []
            for c in range(step + 1):
                opacity = 0.4 + 0.35 * (c / max(step, 1))
                reveal_anims.append(
                    cells[step][c].animate.set_fill(C["positive"], opacity=opacity)
                )
            # Highlight current row label
            if step < len(rl):
                reveal_anims.append(
                    rl[step].animate.set_color(C["highlight"])
                )

            new_label = safe_text(
                step_descriptions[step],
                font_size=LABEL_SIZE, color=C["attention"],
                max_width=SAFE_WIDTH,
            )
            new_label.move_to(step_label.get_center())

            self.play(
                *reveal_anims,
                ReplacementTransform(step_label, new_label),
                run_time=0.7,
            )
            step_label = new_label
            self.wait(0.4)

        self.wait(HOLD_SHORT)

        # Cleanup
        self.play(FadeOut(grid_group), FadeOut(step_label), FadeOut(title))

    # -----------------------------------------------------------------------
    # Part 4 -- Cross-attention (encoder-decoder attention)  ~20s
    # -----------------------------------------------------------------------
    def part4_cross_attention(self):
        title = section_title("Cross-Attention", color=C["attention"])
        self.play(Write(title))
        self.wait(0.5)

        # Encoder words (English) on the left
        enc_words = ["The", "cat", "is", "small"]
        enc_mobs = VGroup()
        for w in enc_words:
            box = labeled_box(w, width=1.4, height=0.6,
                              color=C["encoder"], font_size=LABEL_SIZE,
                              fill_opacity=0.3)
            enc_mobs.add(box)
        enc_mobs.arrange(DOWN, buff=0.3)
        enc_mobs.move_to(LEFT * 3.5 + DOWN * 0.3)

        enc_title = safe_text("Encoder Output", font_size=LABEL_SIZE,
                              color=C["encoder"], max_width=3.0)
        enc_title.next_to(enc_mobs, UP, buff=0.4)

        # Decoder words (French) on the right
        dec_words = ["Le", "chat", "est", "petit"]
        dec_mobs = VGroup()
        for w in dec_words:
            box = labeled_box(w, width=1.4, height=0.6,
                              color=C["decoder"], font_size=LABEL_SIZE,
                              fill_opacity=0.3)
            dec_mobs.add(box)
        dec_mobs.arrange(DOWN, buff=0.3)
        dec_mobs.move_to(RIGHT * 3.5 + DOWN * 0.3)

        dec_title = safe_text("Decoder Queries", font_size=LABEL_SIZE,
                              color=C["decoder"], max_width=3.0)
        dec_title.next_to(dec_mobs, UP, buff=0.4)

        self.play(
            FadeIn(enc_mobs, shift=RIGHT * 0.3),
            FadeIn(dec_mobs, shift=LEFT * 0.3),
            Write(enc_title), Write(dec_title),
            run_time=1.2,
        )
        self.wait(0.5)

        # QKV label
        qkv_note = safe_text(
            "Q from decoder,  K and V from encoder",
            font_size=LABEL_SIZE, color=C["attention"], max_width=SAFE_WIDTH,
        )
        qkv_note.move_to(DOWN * abs(BOTTOM_Y) + UP * 0.3)
        self.play(Write(qkv_note))
        self.wait(HOLD_SHORT)

        # Show cross-attention: "chat" (decoder) -> "cat" (encoder) strong
        # Also dimmer arrows to other encoder words
        arrows = VGroup()
        # dec_mobs[1] = "chat", enc_mobs[1] = "cat"
        strong_arrow = Arrow(
            dec_mobs[1].get_left(), enc_mobs[1].get_right(),
            color=C["attention"], stroke_width=4, buff=0.1,
            max_tip_length_to_length_ratio=0.15,
        )
        arrows.add(strong_arrow)

        # Dim arrows from "chat" to other encoder words
        for i in range(len(enc_words)):
            if i == 1:
                continue
            dim_arrow = Arrow(
                dec_mobs[1].get_left(), enc_mobs[i].get_right(),
                color=C["dim"], stroke_width=1.5, buff=0.1,
                max_tip_length_to_length_ratio=0.12,
            )
            dim_arrow.set_opacity(0.35)
            arrows.add(dim_arrow)

        attn_label = safe_text(
            "'chat' attends strongly to 'cat'",
            font_size=LABEL_SIZE, color=C["highlight"], max_width=SAFE_WIDTH,
        )
        attn_label.move_to(UP * SUBTITLE_Y)

        # Highlight the "chat" and "cat" boxes
        self.play(
            *[Create(a) for a in arrows],
            Write(attn_label),
            enc_mobs[1][0].animate.set_fill(C["encoder"], opacity=0.6),
            dec_mobs[1][0].animate.set_fill(C["decoder"], opacity=0.6),
            run_time=1.5,
        )
        self.wait(HOLD_MEDIUM)

        # Cleanup
        self.play(
            FadeOut(title), FadeOut(enc_mobs), FadeOut(dec_mobs),
            FadeOut(enc_title), FadeOut(dec_title),
            FadeOut(arrows), FadeOut(attn_label), FadeOut(qkv_note),
        )

    # -----------------------------------------------------------------------
    # Part 5 -- Three attention types summary  ~13s
    # -----------------------------------------------------------------------
    def part5_summary(self):
        title = section_title("Three Types of Attention", color=WHITE)
        self.play(Write(title))
        self.wait(0.5)

        types_data = [
            ("Self-Attention", "Encoder", C["encoder"],
             "Bidirectional: every token sees all tokens"),
            ("Masked Self-Attention", "Decoder", C["decoder"],
             "Causal: each token sees only past tokens"),
            ("Cross-Attention", "Decoder -> Encoder", C["attention"],
             "Decoder queries attend to encoder keys/values"),
        ]

        cards = VGroup()
        for name, location, color, description in types_data:
            # Card background
            card_rect = RoundedRectangle(
                width=4.0, height=1.6, corner_radius=0.15,
                color=color, fill_opacity=0.15, stroke_width=2,
            )
            name_t = safe_text(name, font_size=LABEL_SIZE, color=color,
                               max_width=3.5)
            loc_t = safe_text(location, font_size=TINY_SIZE, color=C["label"],
                              max_width=3.5)
            desc_t = safe_text(description, font_size=TINY_SIZE - 2,
                               color=WHITE, max_width=3.5)

            name_t.move_to(card_rect.get_top() + DOWN * 0.35)
            loc_t.next_to(name_t, DOWN, buff=0.15)
            desc_t.next_to(loc_t, DOWN, buff=0.15)

            card = VGroup(card_rect, name_t, loc_t, desc_t)
            cards.add(card)

        cards.arrange(RIGHT, buff=0.4)
        cards.move_to(DOWN * 0.2)

        # Scale down if too wide
        if cards.width > SAFE_WIDTH:
            cards.scale_to_fit_width(SAFE_WIDTH)

        self.play(
            LaggedStart(
                *[FadeIn(c, shift=UP * 0.3) for c in cards],
                lag_ratio=0.3,
            ),
            run_time=2.0,
        )
        self.wait(HOLD_LONG)

        # Final fade
        self.play(FadeOut(title), FadeOut(cards))
        self.wait(0.5)
