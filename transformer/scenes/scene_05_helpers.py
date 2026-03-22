"""Helper builders for Scene 05 -- Positional Encoding.

Extracted to keep the main scene file under 300 lines.
"""

from manim import *
import numpy as np

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.style import (
    C, SAFE_X, BODY_SIZE, LABEL_SIZE, TINY_SIZE, safe_text,
)


def word_row(words, colors, y_pos, box_w=1.8, box_h=0.7):
    """Build a row of colored word boxes."""
    boxes = VGroup()
    for i, w in enumerate(words):
        rect = RoundedRectangle(
            width=box_w, height=box_h, corner_radius=0.1,
            color=colors[i], fill_opacity=0.15, stroke_width=2,
        )
        txt = safe_text(w, max_width=box_w - 0.3,
                        font_size=BODY_SIZE, color=colors[i])
        txt.move_to(rect)
        boxes.add(VGroup(rect, txt))
    boxes.arrange(RIGHT, buff=0.4).move_to(UP * y_pos)
    return boxes


def bar_vector(values, color, label_str, x_pos, bar_w=0.4, bar_h=2.5):
    """Vertical bar chart representing a vector."""
    bars = VGroup()
    for i, v in enumerate(values):
        rect = Rectangle(width=bar_w, height=bar_h * abs(v),
                         color=color, fill_opacity=0.5, stroke_width=1.5)
        rect.move_to([x_pos + i * (bar_w + 0.08), 0, 0])
        rect.shift((UP if v >= 0 else DOWN) * bar_h * abs(v) / 2)
        bars.add(rect)
    bars.move_to([x_pos, 0, 0])
    label = safe_text(label_str, font_size=LABEL_SIZE, color=color)
    label.next_to(bars, DOWN, buff=0.3)
    return VGroup(bars, label)


def build_sinusoid_elements(dims, d_model=512):
    """Build stacked sine waves, sample dots, dim labels, and position markers.

    Returns
    -------
    axes_grp, dots, labels, markers : VGroup
    """
    n_waves = len(dims)
    h, spacing, top_y = 0.35, 0.85, 2.0
    x_half, n_pos = 3.0, 20
    colors = [interpolate_color(BLUE_C, RED_C, k / (n_waves - 1))
              for k in range(n_waves)]
    axes_grp, dots, labels = VGroup(), VGroup(), VGroup()

    for idx, dim_i in enumerate(dims):
        yc = top_y - idx * spacing
        freq = 1.0 / (10000 ** (dim_i / d_model))
        col = colors[idx]
        axis = Line(LEFT * x_half + UP * yc, RIGHT * x_half + UP * yc,
                    color=GRAY, stroke_width=0.5, stroke_opacity=0.4)
        wave = FunctionGraph(
            lambda x, f=freq, yc=yc:
                h * np.sin((x + x_half) / (x_half * 2 / n_pos) * f) + yc,
            x_range=[-x_half, x_half, 0.05], color=col, stroke_width=2)
        axes_grp.add(axis, wave)
        for p in range(6):
            xp = -x_half + p * (2 * x_half / n_pos)
            yv = h * np.sin(p * freq) + yc
            dots.add(Dot([xp, yv, 0], radius=0.06, color=col))
        dl = safe_text(f"dim {dim_i}", font_size=TINY_SIZE, color=col)
        dl.next_to(axis, LEFT, buff=0.25)
        if dl.get_left()[0] < SAFE_X[0]:
            dl.move_to([SAFE_X[0] + dl.width / 2 + 0.1, yc, 0])
        labels.add(dl)

    total_h = (n_waves - 1) * spacing
    markers = VGroup()
    for p in range(6):
        xp = -x_half + p * (2 * x_half / n_pos)
        m = safe_text(f"pos {p}", font_size=TINY_SIZE, color=WHITE)
        m.move_to([xp, top_y - total_h - 0.6, 0])
        guide = DashedLine(
            [xp, top_y + h + 0.1, 0],
            [xp, top_y - total_h - 0.35, 0],
            color=WHITE, stroke_width=0.5, stroke_opacity=0.25,
            dash_length=0.08)
        markers.add(guide, m)

    return axes_grp, dots, labels, markers


def build_binary_grid():
    """Build 8-row x 4-bit binary counter grid with rate labels."""
    bit_cols = [RED_C, ORANGE, GREEN_C, BLUE_C]
    grp = VGroup()
    for i in range(8):
        bs = f"{i:04b}"
        row = VGroup(*[
            VGroup(
                Square(0.5, color=bit_cols[j],
                       fill_opacity=0.6 if ch == "1" else 0.1,
                       stroke_width=1.5),
                safe_text(ch, font_size=LABEL_SIZE,
                          color=WHITE if ch == "1" else GRAY)
            ).arrange(ORIGIN)
            for j, ch in enumerate(bs)
        ]).arrange(RIGHT, buff=0.08)
        grp.add(row)
    grp.arrange(DOWN, buff=0.08).move_to(LEFT * 3.0)

    lbls = VGroup()
    for j, s in [(0, "Slow"), (3, "Fast")]:
        bl = safe_text(s, font_size=TINY_SIZE, color=bit_cols[j])
        bl.next_to(grp[0][j], UP, buff=0.25)
        lbls.add(bl)
    title = safe_text("Binary (discrete)", font_size=LABEL_SIZE, color=GRAY_B)
    title.next_to(grp, UP, buff=0.7)
    return grp, lbls, title


def build_pe_heatmap():
    """Build 8-row x 4-dim PE heatmap grid."""
    grp = VGroup()
    for pos in range(8):
        row = VGroup()
        for d in range(4):
            freq = 1.0 / (10000 ** (2 * d / 8))
            val = np.sin(pos * freq) if d % 2 == 0 else np.cos(pos * freq)
            col = interpolate_color(BLUE_C, RED_C, d / 3)
            cell = Square(0.5, color=col,
                          fill_opacity=0.1 + 0.4 * (val + 1),
                          stroke_width=1.5)
            row.add(cell)
        row.arrange(RIGHT, buff=0.08)
        grp.add(row)
    grp.arrange(DOWN, buff=0.08).move_to(RIGHT * 3.0)
    title = safe_text("PE (continuous)", font_size=LABEL_SIZE, color=GRAY_B)
    title.next_to(grp, UP, buff=0.7)
    return grp, title
