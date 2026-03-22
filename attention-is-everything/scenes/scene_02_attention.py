"""Scene 02: Attention as Soft Dictionary Lookup (~90 seconds).

Builds intuition for attention by comparing hard vs soft dictionary
lookup, then introduces Q/K/V projections and the dot-product + softmax
mechanism.
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

def kv_pair_box(key_text: str, value_text: str,
                key_color=C["key"], value_color=C["value"],
                width: float = 2.4, height: float = 0.65) -> VGroup:
    """A small key-value pair with a dividing line."""
    rect = RoundedRectangle(
        width=width, height=height, corner_radius=0.1,
        stroke_color=WHITE, stroke_width=1.5, fill_opacity=0.08,
        fill_color=WHITE,
    )
    k = Text(key_text, font_size=LABEL_SIZE, color=key_color)
    v = Text(value_text, font_size=LABEL_SIZE, color=value_color)
    k.move_to(rect.get_left() + RIGHT * width * 0.25)
    v.move_to(rect.get_right() + LEFT * width * 0.25)
    divider = Line(
        rect.get_top() + DOWN * 0.08,
        rect.get_bottom() + UP * 0.08,
        stroke_width=1, color=GRAY,
    ).move_to(rect)
    return VGroup(rect, k, divider, v)


def sim_bar(score: float, max_width: float = 1.8,
            height: float = 0.25, color=C["attention"]) -> VGroup:
    """Horizontal bar whose fill represents a similarity score 0-1."""
    bg = Rectangle(
        width=max_width, height=height,
        stroke_color=GRAY, stroke_width=1,
        fill_opacity=0.1, fill_color=GRAY,
    )
    fill = Rectangle(
        width=max(max_width * score, 0.05), height=height,
        stroke_width=0, fill_opacity=0.75, fill_color=color,
    )
    fill.align_to(bg, LEFT)
    label = Text(f"{score:.2f}", font_size=TINY_SIZE, color=WHITE)
    label.next_to(bg, RIGHT, buff=0.15)
    return VGroup(bg, fill, label)


def projection_lens(label: str, color, width=1.6, height=0.9) -> VGroup:
    """A 'lens' representing a linear projection matrix."""
    ellipse = Ellipse(width=width, height=height,
                      color=color, fill_opacity=0.25, stroke_width=2.5)
    txt = Text(label, font_size=LABEL_SIZE, color=color)
    txt.move_to(ellipse)
    if txt.width > width - 0.2:
        txt.scale_to_fit_width(width - 0.2)
    return VGroup(ellipse, txt)


# ── Scene ────────────────────────────────────────────────────────────

class AttentionSoftDictionary(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        self.hard_lookup()
        self.transition_question()
        self.soft_lookup()
        self.qkv_projections()
        self.dot_product_softmax()

    # ── Phase 1: Hard Dictionary Lookup ──────────────────────────────

    def hard_lookup(self):
        title = section_title("Hard Dictionary Lookup")
        self.play(Write(title), run_time=0.8)

        # Build dictionary entries
        entries_data = [
            ("cat", "furry pet"),
            ("dog", "loyal friend"),
            ("car", "vehicle"),
            ("sun", "bright star"),
        ]
        entries = VGroup(*[kv_pair_box(k, v) for k, v in entries_data])
        entries.arrange(DOWN, buff=0.2)
        entries.move_to(RIGHT * 1.5)

        dict_label = safe_text("Dictionary", font_size=LABEL_SIZE, color=C["dim"])
        dict_label.next_to(entries, UP, buff=0.25)

        # Query box
        query_box = RoundedRectangle(
            width=2.0, height=0.65, corner_radius=0.1,
            color=C["query"], fill_opacity=0.2, stroke_width=2,
        )
        query_txt = Text("cat", font_size=BODY_SIZE, color=C["query"])
        query_txt.move_to(query_box)
        query_group = VGroup(query_box, query_txt)
        query_group.move_to(LEFT * 3.5 + UP * 0.3)

        q_label = safe_text("Query", font_size=LABEL_SIZE, color=C["query"])
        q_label.next_to(query_group, UP, buff=0.2)

        self.play(
            FadeIn(entries, shift=RIGHT * 0.3),
            Write(dict_label),
            FadeIn(query_group, shift=LEFT * 0.3),
            Write(q_label),
            run_time=1.0,
        )
        self.wait(HOLD_SHORT)

        # Arrow from query to matching entry
        match_arrow = Arrow(
            query_group.get_right(), entries[0].get_left(),
            color=C["attention"], buff=0.15, stroke_width=3,
            max_tip_length_to_length_ratio=0.12,
        )
        # Highlight matching entry
        highlight = SurroundingRectangle(
            entries[0], color=C["attention"], buff=0.06, stroke_width=2.5,
        )

        result_box = RoundedRectangle(
            width=2.2, height=0.65, corner_radius=0.1,
            color=C["value"], fill_opacity=0.2, stroke_width=2,
        )
        result_txt = Text("furry pet", font_size=LABEL_SIZE, color=C["value"])
        result_txt.move_to(result_box)
        result_group = VGroup(result_box, result_txt)
        result_group.next_to(query_group, DOWN, buff=0.9)

        result_label = safe_text("Result", font_size=LABEL_SIZE, color=C["value"])
        result_label.next_to(result_group, DOWN, buff=0.15)

        self.play(
            GrowArrow(match_arrow),
            Create(highlight),
            run_time=0.7,
        )
        self.play(FadeIn(result_group, shift=DOWN * 0.2), Write(result_label), run_time=0.6)
        self.wait(HOLD_MEDIUM)

        # Store for cleanup
        self.hard_lookup_group = VGroup(
            title, entries, dict_label, query_group, q_label,
            match_arrow, highlight, result_group, result_label,
        )

    # ── Phase 2: Transition Question ─────────────────────────────────

    def transition_question(self):
        self.play(FadeOut(self.hard_lookup_group), run_time=0.6)
        story_bridge(self, "But what if no key matches exactly?")

    # ── Phase 3: Soft Lookup ─────────────────────────────────────────

    def soft_lookup(self):
        title = section_title("Soft Dictionary Lookup")
        self.play(Write(title), run_time=0.7)

        # Dictionary entries (right side)
        entries_data = [
            ("kitten", "playful"),
            ("puppy", "energetic"),
            ("tiger", "fierce"),
            ("rock", "solid"),
        ]
        scores = [0.70, 0.15, 0.10, 0.05]
        colors_for_bars = [YELLOW_C, YELLOW_D, GOLD_E, GRAY]

        entries = VGroup(*[kv_pair_box(k, v) for k, v in entries_data])
        entries.arrange(DOWN, buff=0.25)
        entries.move_to(ORIGIN + RIGHT * 0.3 + DOWN * 0.15)

        # Query
        query_box = RoundedRectangle(
            width=2.0, height=0.65, corner_radius=0.1,
            color=C["query"], fill_opacity=0.2, stroke_width=2,
        )
        query_txt = Text("cat", font_size=BODY_SIZE, color=C["query"])
        query_txt.move_to(query_box)
        query_group = VGroup(query_box, query_txt)
        query_group.move_to(LEFT * 4.5 + UP * 0.3)

        q_label = safe_text("Query", font_size=LABEL_SIZE, color=C["query"])
        q_label.next_to(query_group, UP, buff=0.2)

        self.play(
            FadeIn(entries, shift=RIGHT * 0.3),
            FadeIn(query_group, shift=LEFT * 0.3),
            Write(q_label),
            run_time=0.8,
        )

        # Similarity bars next to each entry
        bars = VGroup()
        arrows = VGroup()
        for i, (entry, score) in enumerate(zip(entries, scores)):
            bar = sim_bar(score, max_width=1.6, height=0.22,
                          color=colors_for_bars[i])
            bar.next_to(entry, RIGHT, buff=0.25)
            bars.add(bar)

            arr = Arrow(
                query_group.get_right(), entry.get_left(),
                color=interpolate_color(C["attention"], C["dim"], 1.0 - score),
                buff=0.1, stroke_width=max(1.0, 3.0 * score),
                max_tip_length_to_length_ratio=0.1,
            )
            arrows.add(arr)

        sim_label = safe_text("Similarity", font_size=TINY_SIZE, color=C["dim"])
        sim_label.next_to(bars, UP, buff=0.15)

        self.play(
            *[GrowArrow(a) for a in arrows],
            run_time=0.8,
        )
        self.play(
            *[FadeIn(b, shift=RIGHT * 0.2) for b in bars],
            Write(sim_label),
            run_time=0.7,
        )
        self.wait(HOLD_SHORT)

        # Weighted result -- blended box
        note = safe_text(
            "Result = weighted sum of all values",
            font_size=LABEL_SIZE, color=C["highlight"],
        )
        note.move_to(DOWN * 2.8)

        # Value labels with opacity matching weight
        value_words = ["playful", "energetic", "fierce", "solid"]
        blend_parts = VGroup()
        for i, (word, score) in enumerate(zip(value_words, scores)):
            t = Text(word, font_size=LABEL_SIZE, color=C["value"])
            t.set_opacity(max(0.2, score))
            blend_parts.add(t)
        blend_parts.arrange(RIGHT, buff=0.3)
        blend_parts.move_to(DOWN * 2.1)
        if blend_parts.width > SAFE_WIDTH:
            blend_parts.scale_to_fit_width(SAFE_WIDTH)

        self.play(Write(note), run_time=0.5)
        self.play(
            *[FadeIn(bp, shift=DOWN * 0.15) for bp in blend_parts],
            run_time=0.8,
        )
        self.wait(HOLD_MEDIUM)

        # Cleanup
        self.soft_lookup_group = VGroup(
            title, entries, query_group, q_label,
            bars, arrows, sim_label, note, blend_parts,
        )
        self.play(FadeOut(self.soft_lookup_group), run_time=0.6)

    # ── Phase 4: Q, K, V Projections ────────────────────────────────

    def qkv_projections(self):
        title = section_title("Creating Q, K, V")
        self.play(Write(title), run_time=0.7)

        # Word embedding vector
        emb_rect = RoundedRectangle(
            width=2.2, height=0.7, corner_radius=0.1,
            color=WHITE, fill_opacity=0.12, stroke_width=2,
        )
        emb_txt = Text("word embedding", font_size=LABEL_SIZE, color=WHITE)
        emb_txt.move_to(emb_rect)
        if emb_txt.width > emb_rect.width - 0.2:
            emb_txt.scale_to_fit_width(emb_rect.width - 0.2)
        emb = VGroup(emb_rect, emb_txt)
        emb.move_to(LEFT * 4.5)

        self.play(FadeIn(emb, shift=LEFT * 0.3), run_time=0.6)

        # Three projection lenses
        lens_data = [
            ("W^Q", C["query"], "Query", '"What am I\nlooking for?"'),
            ("W^K", C["key"], "Key", '"What do I\ncontain?"'),
            ("W^V", C["value"], "Value", '"What info do\nI provide?"'),
        ]

        lenses = VGroup()
        output_boxes = VGroup()
        role_labels = VGroup()
        lens_arrows_in = VGroup()
        lens_arrows_out = VGroup()

        y_positions = [1.2, 0.0, -1.2]

        for i, (matrix_label, color, out_label, role_text) in enumerate(lens_data):
            # Lens at center
            lens = projection_lens(matrix_label, color, width=1.5, height=0.8)
            lens.move_to(LEFT * 1.0 + UP * y_positions[i])
            lenses.add(lens)

            # Output box
            out_box = RoundedRectangle(
                width=1.8, height=0.6, corner_radius=0.1,
                color=color, fill_opacity=0.2, stroke_width=2,
            )
            out_txt = Text(out_label, font_size=LABEL_SIZE, color=color)
            out_txt.move_to(out_box)
            out = VGroup(out_box, out_txt)
            out.move_to(RIGHT * 2.0 + UP * y_positions[i])
            output_boxes.add(out)

            # Role description
            role = safe_text(role_text, font_size=TINY_SIZE, color=color,
                             max_width=3.5)
            role.next_to(out, RIGHT, buff=0.3)
            role_labels.add(role)

            # Arrows
            arr_in = Arrow(
                emb.get_right(), lens.get_left(),
                color=color, buff=0.1, stroke_width=2,
                max_tip_length_to_length_ratio=0.12,
            )
            arr_out = Arrow(
                lens.get_right(), out.get_left(),
                color=color, buff=0.1, stroke_width=2,
                max_tip_length_to_length_ratio=0.12,
            )
            lens_arrows_in.add(arr_in)
            lens_arrows_out.add(arr_out)

        # Animate: lenses appear, then arrows, then outputs
        self.play(
            *[FadeIn(l, scale=0.8) for l in lenses],
            run_time=0.7,
        )
        self.play(
            *[GrowArrow(a) for a in lens_arrows_in],
            run_time=0.5,
        )
        self.play(
            *[GrowArrow(a) for a in lens_arrows_out],
            *[FadeIn(ob, shift=RIGHT * 0.2) for ob in output_boxes],
            run_time=0.6,
        )
        self.play(
            *[Write(rl) for rl in role_labels],
            run_time=0.8,
        )
        self.wait(HOLD_MEDIUM)

        # Cleanup
        self.qkv_group = VGroup(
            title, emb, lenses, output_boxes, role_labels,
            lens_arrows_in, lens_arrows_out,
        )
        self.play(FadeOut(self.qkv_group), run_time=0.6)

    # ── Phase 5: Dot Product + Softmax ───────────────────────────────

    def dot_product_softmax(self):
        title = section_title("Computing Attention Weights")
        self.play(Write(title), run_time=0.7)

        # One query vector vs multiple key vectors
        q_vec = RoundedRectangle(
            width=1.6, height=0.55, corner_radius=0.08,
            color=C["query"], fill_opacity=0.25, stroke_width=2,
        )
        q_label = Text("q", font_size=BODY_SIZE, color=C["query"])
        q_label.move_to(q_vec)
        q_group = VGroup(q_vec, q_label)
        q_group.move_to(LEFT * 5.0 + UP * 1.0)

        q_heading = safe_text("Query", font_size=TINY_SIZE, color=C["query"])
        q_heading.next_to(q_group, UP, buff=0.15)

        # Key vectors
        key_labels_text = ["k1", "k2", "k3", "k4"]
        key_groups = VGroup()
        for kl in key_labels_text:
            k_rect = RoundedRectangle(
                width=1.2, height=0.5, corner_radius=0.08,
                color=C["key"], fill_opacity=0.2, stroke_width=1.5,
            )
            k_txt = Text(kl, font_size=LABEL_SIZE, color=C["key"])
            k_txt.move_to(k_rect)
            key_groups.add(VGroup(k_rect, k_txt))
        key_groups.arrange(DOWN, buff=0.2)
        key_groups.move_to(LEFT * 2.0 + UP * 0.2)

        k_heading = safe_text("Keys", font_size=TINY_SIZE, color=C["key"])
        k_heading.next_to(key_groups, UP, buff=0.15)

        self.play(
            FadeIn(q_group, shift=LEFT * 0.2),
            Write(q_heading),
            FadeIn(key_groups, shift=RIGHT * 0.2),
            Write(k_heading),
            run_time=0.7,
        )

        # Dot products: arrows from q to each k, producing raw scores
        raw_scores = [3.2, 1.1, 0.4, 0.1]
        dot_arrows = VGroup()
        score_texts = VGroup()

        for i, (kg, score) in enumerate(zip(key_groups, raw_scores)):
            arr = Arrow(
                q_group.get_right(), kg.get_left(),
                color=C["query"], buff=0.08, stroke_width=1.5,
                max_tip_length_to_length_ratio=0.1,
            )
            dot_arrows.add(arr)

            s_txt = Text(f"{score:.1f}", font_size=LABEL_SIZE, color=C["attention"])
            s_txt.next_to(kg, RIGHT, buff=0.3)
            score_texts.add(s_txt)

        dot_label = safe_text("q . k", font_size=LABEL_SIZE, color=C["dim"])
        dot_label.next_to(score_texts, UP, buff=0.3)

        self.play(
            *[GrowArrow(a) for a in dot_arrows],
            run_time=0.6,
        )
        self.play(
            *[FadeIn(st, shift=RIGHT * 0.15) for st in score_texts],
            Write(dot_label),
            run_time=0.6,
        )
        self.wait(HOLD_SHORT)

        # Softmax step: raw scores -> weights
        softmax_label = safe_text("softmax", font_size=BODY_SIZE,
                                  color=C["highlight"])
        softmax_label.move_to(RIGHT * 1.8 + UP * 2.0)

        soft_arrow = Arrow(
            score_texts.get_right() + UP * 0.3,
            RIGHT * 3.0 + UP * 1.5,
            color=C["highlight"], buff=0.15, stroke_width=2,
            max_tip_length_to_length_ratio=0.1,
        )

        weights = [0.72, 0.18, 0.07, 0.03]
        weight_bars = VGroup()
        for i, w in enumerate(weights):
            bar_group = VGroup()
            # Bar
            bg = Rectangle(width=2.2, height=0.3, stroke_color=GRAY,
                            stroke_width=1, fill_opacity=0.08, fill_color=GRAY)
            fill = Rectangle(
                width=max(2.2 * w, 0.04), height=0.3,
                stroke_width=0, fill_opacity=0.7,
                fill_color=interpolate_color(C["attention"], WHITE, 0.15),
            )
            fill.align_to(bg, LEFT)
            w_label = Text(f"{w:.2f}", font_size=TINY_SIZE, color=WHITE)
            w_label.next_to(bg, RIGHT, buff=0.12)
            bar_group.add(bg, fill, w_label)
            weight_bars.add(bar_group)

        weight_bars.arrange(DOWN, buff=0.2)
        weight_bars.move_to(RIGHT * 3.8 + DOWN * 0.2)

        w_heading = safe_text("Weights (sum = 1)", font_size=TINY_SIZE,
                              color=C["attention"])
        w_heading.next_to(weight_bars, UP, buff=0.2)

        self.play(
            Write(softmax_label),
            GrowArrow(soft_arrow),
            run_time=0.6,
        )
        self.play(
            *[FadeIn(wb, shift=RIGHT * 0.2) for wb in weight_bars],
            Write(w_heading),
            run_time=0.8,
        )

        # Bottom note
        eq_note = safe_text(
            "Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V",
            font_size=TINY_SIZE, color=C["dim"], max_width=12.0,
        )
        eq_note.move_to(DOWN * 3.1)
        self.play(Write(eq_note), run_time=0.7)
        self.wait(HOLD_LONG)

        # Final cleanup
        all_objs = VGroup(
            title, q_group, q_heading, key_groups, k_heading,
            dot_arrows, score_texts, dot_label,
            softmax_label, soft_arrow, weight_bars, w_heading, eq_note,
        )
        self.play(FadeOut(all_objs), run_time=0.8)
