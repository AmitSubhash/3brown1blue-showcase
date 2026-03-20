"""DOT Explainer Scenes 7-10.

Scene 7: FlatField - Why we measure changes, not absolutes
Scene 8: InverseProblem - Solving the inverse problem with regularization
Scene 9: HDDOT - High-density DOT and multi-distance sensing
Scene 10: Pipeline - The complete DOT pipeline overview
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from style import *


# ---------------------------------------------------------------------------
# Helper: labeled box used across scenes
# ---------------------------------------------------------------------------

def labeled_box(
    label: str,
    color: ManimColor,
    width: float = 2.0,
    height: float = 1.0,
    font_size: int = LABEL_SIZE,
) -> VGroup:
    """Return a rounded rectangle with centered text."""
    rect = RoundedRectangle(
        corner_radius=0.12,
        width=width,
        height=height,
        stroke_color=color,
        fill_color=color,
        fill_opacity=0.15,
        stroke_width=2,
    )
    txt = Text(label, font_size=font_size, color=color)
    txt.move_to(rect.get_center())
    return VGroup(rect, txt)


def annotation_arrow(
    target_pos: np.ndarray,
    label_text: str,
    direction: np.ndarray,
    color: ManimColor = C["label"],
    font_size: int = LABEL_SIZE,
) -> VGroup:
    """Arrow + label pointing toward *target_pos* from *direction* away."""
    label = Text(label_text, font_size=font_size, color=color)
    label.move_to(target_pos + direction * 1.4)
    arrow = Arrow(
        start=label.get_edge_center(-direction),
        end=target_pos,
        buff=0.08,
        color=color,
        stroke_width=2,
        tip_length=0.15,
    )
    return VGroup(arrow, label)


# ===================================================================
# Scene 7 -- FlatField
# "Why We Measure Changes, Not Absolutes" (~1.5 min)
# ===================================================================


class FlatField(Scene):
    """Show why DOT uses baseline-normalized measurements."""

    def construct(self) -> None:
        # ---- Phase 1: The raw measurement is useless ----
        title = Text(
            "Why We Measure Changes, Not Absolutes",
            font_size=TITLE_SIZE,
            color=C["highlight"],
        )
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(1)

        # Source-detector pair
        source_dot = Dot(LEFT * 3 + DOWN * 0.5, radius=0.18, color=C["source"])
        source_lbl = Text("S", font_size=LABEL_SIZE, color=C["source"])
        source_lbl.next_to(source_dot, DOWN, buff=0.15)

        det_dot = Dot(RIGHT * 3 + DOWN * 0.5, radius=0.18, color=C["detector"])
        det_lbl = Text("D", font_size=LABEL_SIZE, color=C["detector"])
        det_lbl.next_to(det_dot, DOWN, buff=0.15)

        connect_line = Line(
            source_dot.get_center(), det_dot.get_center(),
            color=C["photon"], stroke_width=2, stroke_opacity=0.5,
        )

        self.play(
            FadeIn(source_dot), Write(source_lbl),
            FadeIn(det_dot), Write(det_lbl),
            Create(connect_line),
        )
        self.wait(0.5)

        # Raw signal bar
        bar_bg = Rectangle(
            width=1.8, height=0.5, stroke_color=WHITE,
            fill_color=DARK_GRAY, fill_opacity=0.6,
        ).move_to(RIGHT * 0.0 + DOWN * 2.2)
        bar_fill = Rectangle(
            width=1.35, height=0.44,
            stroke_width=0, fill_color=C["photon"], fill_opacity=0.7,
        ).align_to(bar_bg, LEFT).shift(RIGHT * 0.04).move_to(
            bar_bg.get_center()
        ).align_to(bar_bg, LEFT).shift(RIGHT * 0.04)
        bar_label = MathTex(r"I = 3.7\;\text{mW}", font_size=BODY_SIZE)
        bar_label.next_to(bar_bg, RIGHT, buff=0.3)

        self.play(FadeIn(bar_bg), GrowFromEdge(bar_fill, LEFT), Write(bar_label))
        self.wait(1)

        # Confound annotations
        ann_source = annotation_arrow(
            source_dot.get_center(),
            "Power: 2.1 mW\n(varies day to day)",
            direction=UP + LEFT * 0.5,
            color=C["absorb"],
        )

        skin_pos = (source_dot.get_center() + det_dot.get_center()) / 2 + UP * 0.2
        ann_coupling = annotation_arrow(
            skin_pos,
            "Coupling: poor\n(hair in the way)",
            direction=UP,
            color=C["absorb"],
        )

        ann_detector = annotation_arrow(
            det_dot.get_center(),
            "Gain: 1.2x\n(calibration drift)",
            direction=UP + RIGHT * 0.5,
            color=C["absorb"],
        )

        self.play(GrowArrow(ann_source[0]), Write(ann_source[1]), run_time=1)
        self.wait(0.8)
        self.play(GrowArrow(ann_coupling[0]), Write(ann_coupling[1]), run_time=1)
        self.wait(0.8)
        self.play(GrowArrow(ann_detector[0]), Write(ann_detector[1]), run_time=1)
        self.wait(1)

        useless = Text(
            "The raw number is USELESS!",
            font_size=BODY_SIZE, color=C["absorb"],
        ).next_to(bar_bg, DOWN, buff=0.4)
        self.play(Write(useless))
        self.wait(HOLD)

        # Clear phase 1
        phase1_mobs = VGroup(
            source_dot, source_lbl, det_dot, det_lbl, connect_line,
            bar_bg, bar_fill, bar_label,
            ann_source, ann_coupling, ann_detector, useless,
        )
        self.play(FadeOut(phase1_mobs), run_time=0.8)

        # ---- Phase 2: Measure TWICE ----
        solution = Text(
            "Solution: Measure TWICE", font_size=BODY_SIZE, color=C["scatter"],
        ).next_to(title, DOWN, buff=0.5)
        self.play(Write(solution))
        self.wait(1)

        # Frame 1: baseline
        frame1_box = RoundedRectangle(
            corner_radius=0.12, width=4.5, height=2.0,
            stroke_color=C["dim"], fill_color=BLACK, fill_opacity=0.3,
        ).shift(LEFT * 3 + DOWN * 1.0)
        f1_title = Text(
            "Baseline (resting)", font_size=LABEL_SIZE, color=C["label"],
        ).next_to(frame1_box, UP, buff=0.15)
        f1_val = MathTex(
            r"I_0 = 3.7\;\text{mW}", font_size=BODY_SIZE, color=C["photon"],
        ).move_to(frame1_box.get_center())

        # Frame 2: task
        frame2_box = RoundedRectangle(
            corner_radius=0.12, width=4.5, height=2.0,
            stroke_color=C["dim"], fill_color=BLACK, fill_opacity=0.3,
        ).shift(RIGHT * 3 + DOWN * 1.0)
        f2_title = Text(
            "Task (brain active)", font_size=LABEL_SIZE, color=C["label"],
        ).next_to(frame2_box, UP, buff=0.15)
        f2_val = MathTex(
            r"I_{\text{task}} = 3.5\;\text{mW}",
            font_size=BODY_SIZE, color=C["photon"],
        ).move_to(frame2_box.get_center())

        self.play(
            Create(frame1_box), Write(f1_title), Write(f1_val), run_time=1,
        )
        self.wait(0.8)
        self.play(
            Create(frame2_box), Write(f2_title), Write(f2_val), run_time=1,
        )
        self.wait(1)

        # Compute delta_OD
        delta_eq = MathTex(
            r"\Delta OD",
            r"= -\ln\!\left(\frac{I_{\text{task}}}{I_0}\right)",
            r"= -\ln\!\left(\frac{3.5}{3.7}\right)",
            r"= 0.056",
            font_size=BODY_SIZE,
        ).next_to(VGroup(frame1_box, frame2_box), DOWN, buff=0.5)
        delta_eq[0].set_color(C["recon"])
        delta_eq[3].set_color(C["highlight"])

        for part in delta_eq:
            self.play(Write(part), run_time=0.8)
            self.wait(0.5)
        self.wait(HOLD)

        # Clear phase 2
        phase2_mobs = VGroup(
            solution, frame1_box, f1_title, f1_val,
            frame2_box, f2_title, f2_val, delta_eq,
        )
        self.play(FadeOut(phase2_mobs), run_time=0.8)

        # ---- Phase 3: WHY the ratio cancels confounds ----
        why_title = Text(
            "Why does the ratio work?", font_size=BODY_SIZE, color=C["scatter"],
        ).next_to(title, DOWN, buff=0.5)
        self.play(Write(why_title))
        self.wait(1)

        # Write I_0 equation
        eq_i0 = MathTex(
            r"I_0",
            r"=",
            r"\underbrace{P}",
            r"\cdot",
            r"\underbrace{\eta}",
            r"\cdot",
            r"\underbrace{G}",
            r"\cdot",
            r"e^{-\mu_{a,0} \, L}",
            font_size=BODY_SIZE,
        ).shift(UP * 0.4)

        # Color the confound factors
        eq_i0[2].set_color(C["absorb"])   # P
        eq_i0[4].set_color(C["absorb"])   # eta
        eq_i0[6].set_color(C["absorb"])   # G
        eq_i0[8].set_color(C["scatter"])  # exp term

        i0_label = Text("Baseline:", font_size=LABEL_SIZE, color=C["label"])
        i0_label.next_to(eq_i0, LEFT, buff=0.3)

        self.play(Write(i0_label), Write(eq_i0), run_time=1.5)
        self.wait(1)

        # Annotations on confound factors
        p_ann = Text("Power", font_size=18, color=C["absorb"])
        p_ann.next_to(eq_i0[2], DOWN, buff=0.5)
        eta_ann = Text("Coupling", font_size=18, color=C["absorb"])
        eta_ann.next_to(eq_i0[4], DOWN, buff=0.5)
        g_ann = Text("Gain", font_size=18, color=C["absorb"])
        g_ann.next_to(eq_i0[6], DOWN, buff=0.5)
        self.play(Write(p_ann), Write(eta_ann), Write(g_ann), run_time=0.8)
        self.wait(1)

        # Write I_task equation
        eq_itask = MathTex(
            r"I_{\text{task}}",
            r"=",
            r"\underbrace{P}",
            r"\cdot",
            r"\underbrace{\eta}",
            r"\cdot",
            r"\underbrace{G}",
            r"\cdot",
            r"e^{-\mu_{a,1} \, L}",
            font_size=BODY_SIZE,
        ).shift(DOWN * 1.2)

        eq_itask[2].set_color(C["absorb"])
        eq_itask[4].set_color(C["absorb"])
        eq_itask[6].set_color(C["absorb"])
        eq_itask[8].set_color(C["scatter"])

        itask_label = Text("Task:", font_size=LABEL_SIZE, color=C["label"])
        itask_label.next_to(eq_itask, LEFT, buff=0.3)

        self.play(Write(itask_label), Write(eq_itask), run_time=1.5)
        self.wait(1.5)

        # Show ratio
        ratio_eq = MathTex(
            r"\frac{I_{\text{task}}}{I_0}",
            r"=",
            r"\frac{"
            r"e^{-\mu_{a,1} L}"
            r"}{"
            r"e^{-\mu_{a,0} L}"
            r"}",
            font_size=BODY_SIZE,
        ).shift(DOWN * 3.0)

        self.play(
            FadeOut(p_ann, eta_ann, g_ann),
            Write(ratio_eq),
            run_time=1.5,
        )
        self.wait(1.5)

        # Animate confounds disappearing: fade the red parts
        cancel_text = Text(
            "Calibration factors CANCEL in the ratio!",
            font_size=BODY_SIZE, color=C["highlight"],
        ).to_edge(DOWN, buff=0.5)
        self.play(
            eq_i0[2].animate.set_opacity(0.2),
            eq_i0[4].animate.set_opacity(0.2),
            eq_i0[6].animate.set_opacity(0.2),
            eq_itask[2].animate.set_opacity(0.2),
            eq_itask[4].animate.set_opacity(0.2),
            eq_itask[6].animate.set_opacity(0.2),
            Write(cancel_text),
            run_time=1.5,
        )
        self.wait(HOLD)

        # Simplified result
        result_eq = MathTex(
            r"\frac{I_{\text{task}}}{I_0}",
            r"= e^{-(\mu_{a,1} - \mu_{a,0})\,L}",
            r"= e^{-\Delta\mu_a \, L}",
            font_size=EQ_SIZE,
            color=C["recon"],
        )
        result_eq.move_to(ORIGIN)

        phase3_keep = VGroup(title, why_title)
        phase3_clear = VGroup(
            i0_label, eq_i0, itask_label, eq_itask,
            ratio_eq, cancel_text,
        )
        self.play(
            FadeOut(phase3_clear),
            Write(result_eq),
            run_time=1.5,
        )
        self.wait(HOLD)

        # ---- Phase 4: Takeaway ----
        takeaway = Text(
            "DOT measures CHANGES in absorption, not absolute values.",
            font_size=BODY_SIZE, color=C["highlight"],
        ).next_to(result_eq, DOWN, buff=0.8)

        self.play(Write(takeaway))
        self.wait(HOLD + 1)

        self.play(FadeOut(VGroup(title, why_title, result_eq, takeaway)))
        self.wait(0.5)


# ===================================================================
# Scene 8 -- InverseProblem
# "Solving the Inverse Problem" (~2 min)
# ===================================================================


class InverseProblem(Scene):
    """Underdetermined system, multiple solutions, regularization sweep."""

    def construct(self) -> None:
        # ---- Phase 1: The equation ----
        title = Text(
            "Solving the Inverse Problem",
            font_size=TITLE_SIZE, color=C["highlight"],
        )
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(1)

        main_eq = MathTex(
            r"\Delta \mathbf{y}",
            r"=",
            r"\mathbf{A}",
            r"\,\Delta \mathbf{x}",
            font_size=60,
        )
        main_eq[0].set_color(C["detector"])
        main_eq[2].set_color(C["matrix"])
        main_eq[3].set_color(C["recon"])
        main_eq.next_to(title, DOWN, buff=0.6)

        self.play(Write(main_eq), run_time=1.5)
        self.wait(1)

        # Annotations on the equation
        y_ann = Text("measured", font_size=18, color=C["detector"])
        y_ann.next_to(main_eq[0], DOWN, buff=0.3)
        a_ann = Text("sensitivity\nmatrix", font_size=18, color=C["matrix"])
        a_ann.next_to(main_eq[2], DOWN, buff=0.3)
        x_ann = Text("image\n(want this!)", font_size=18, color=C["recon"])
        x_ann.next_to(main_eq[3], DOWN, buff=0.3)

        self.play(Write(y_ann), Write(a_ann), Write(x_ann), run_time=1)
        self.wait(HOLD)

        self.play(FadeOut(y_ann, a_ann, x_ann))

        # ---- Phase 2: Underdetermined visual ----
        phase2_title = Text(
            "More unknowns than equations",
            font_size=BODY_SIZE, color=C["absorb"],
        ).shift(DOWN * 0.2)
        self.play(Write(phase2_title))
        self.wait(0.5)

        # 4x4 grid of voxels
        grid_size = 4
        cell_size = 0.45
        grid_group = VGroup()
        grid_origin = LEFT * 4.0 + DOWN * 2.2

        for row in range(grid_size):
            for col in range(grid_size):
                cell = Square(
                    side_length=cell_size,
                    stroke_color=C["dim"],
                    stroke_width=1,
                    fill_color=BLACK,
                    fill_opacity=0.3,
                )
                cell.move_to(
                    grid_origin
                    + RIGHT * col * cell_size
                    + DOWN * row * cell_size
                )
                grid_group.add(cell)

        grid_label = Text(
            "16 voxels (unknowns)", font_size=LABEL_SIZE, color=C["recon"],
        ).next_to(grid_group, DOWN, buff=0.25)

        self.play(
            LaggedStart(*[FadeIn(c) for c in grid_group], lag_ratio=0.03),
            run_time=1,
        )
        self.play(Write(grid_label))
        self.wait(0.5)

        meas_label = Text(
            "6 measurements", font_size=LABEL_SIZE, color=C["detector"],
        ).shift(RIGHT * 3 + DOWN * 2.2)
        meas_bars = VGroup()
        for i in range(6):
            bar = Rectangle(
                width=1.2, height=0.28,
                stroke_color=C["detector"],
                fill_color=C["detector"],
                fill_opacity=0.3,
                stroke_width=1,
            )
            bar.next_to(meas_label, UP, buff=0.15 + i * 0.35)
            meas_bars.add(bar)

        self.play(
            LaggedStart(*[FadeIn(b) for b in meas_bars], lag_ratio=0.08),
            Write(meas_label),
            run_time=1,
        )
        self.wait(0.5)

        problem_txt = Text(
            "16 unknowns, 6 equations.\nInfinitely many solutions!",
            font_size=LABEL_SIZE, color=C["absorb"],
        ).next_to(phase2_title, DOWN, buff=0.3)
        self.play(Write(problem_txt))
        self.wait(1.5)

        # Show 3 different solutions on grids
        sol_grids = VGroup()
        sol_labels = ["Solution A", "Solution B", "Solution C"]
        # Different random-looking activation patterns
        patterns = [
            [0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
        ]
        for sol_idx in range(3):
            sg = VGroup()
            for idx in range(16):
                row, col = divmod(idx, 4)
                cell = Square(
                    side_length=cell_size * 0.8,
                    stroke_color=C["dim"],
                    stroke_width=1,
                    fill_color=C["recon"] if patterns[sol_idx][idx] else BLACK,
                    fill_opacity=0.7 if patterns[sol_idx][idx] else 0.15,
                )
                cell.move_to(
                    RIGHT * (sol_idx - 1) * 2.8
                    + DOWN * 2.2
                    + RIGHT * col * cell_size * 0.8
                    + DOWN * row * cell_size * 0.8
                )
                sg.add(cell)
            lbl = Text(
                sol_labels[sol_idx],
                font_size=18, color=C["label"],
            ).next_to(sg, DOWN, buff=0.15)
            sol_grids.add(VGroup(sg, lbl))

        # Clear previous grid display and show solutions
        self.play(
            FadeOut(grid_group, grid_label, meas_bars, meas_label),
            run_time=0.6,
        )
        self.play(
            LaggedStart(*[FadeIn(g) for g in sol_grids], lag_ratio=0.15),
            run_time=1.2,
        )
        which_txt = Text(
            "Which one is right?", font_size=BODY_SIZE, color=C["highlight"],
        ).next_to(sol_grids, DOWN, buff=0.4)
        self.play(Write(which_txt))
        self.wait(HOLD)

        self.play(FadeOut(sol_grids, which_txt, phase2_title, problem_txt))
        self.wait(0.3)

        # ---- Phase 3: Regularization ----
        reg_title = Text(
            "Add prior knowledge: activations are SMOOTH",
            font_size=BODY_SIZE, color=C["scatter"],
        ).next_to(main_eq, DOWN, buff=0.5)
        self.play(Write(reg_title))
        self.wait(1)

        tik_eq = MathTex(
            r"\Delta\mathbf{x}",
            r"= \left(",
            r"\mathbf{A}^T\!\mathbf{A}",
            r"+ \lambda\,\mathbf{I}",
            r"\right)^{\!-1}",
            r"\mathbf{A}^T",
            r"\,\Delta\mathbf{y}",
            font_size=EQ_SIZE,
        ).next_to(reg_title, DOWN, buff=0.5)
        tik_eq[0].set_color(C["recon"])
        tik_eq[2].set_color(C["matrix"])
        tik_eq[3].set_color(C["highlight"])
        tik_eq[5].set_color(C["matrix"])
        tik_eq[6].set_color(C["detector"])

        self.play(Write(tik_eq), run_time=2)
        self.wait(1)

        lam_ann = Text(
            "regularization\nparameter",
            font_size=18, color=C["highlight"],
        ).next_to(tik_eq[3], DOWN, buff=0.3)
        self.play(Write(lam_ann))
        self.wait(HOLD)

        self.play(FadeOut(reg_title, lam_ann))

        # ---- Phase 4: Parameter sweep with ValueTracker ----
        sweep_title = Text(
            "Effect of regularization strength",
            font_size=BODY_SIZE, color=C["scatter"],
        ).next_to(tik_eq, DOWN, buff=0.3)
        self.play(Write(sweep_title))
        self.wait(0.5)

        lam_tracker = ValueTracker(0.0)  # 0 = small, 1 = right, 2 = large

        # Build the reconstruction grid (6x6) driven by tracker
        recon_grid_size = 6
        rc_cell = 0.42
        recon_origin = LEFT * 1.5 + DOWN * 2.8

        def _build_recon_grid() -> VGroup:
            """Construct the 6x6 grid colored by lambda value."""
            lam_val = lam_tracker.get_value()
            grp = VGroup()
            for row in range(recon_grid_size):
                for col in range(recon_grid_size):
                    # Ideal: gaussian blob in center
                    cx, cy = 2.5, 2.5
                    dist = np.sqrt((row - cy) ** 2 + (col - cx) ** 2)
                    ideal = np.exp(-dist ** 2 / 2.5)

                    # Noise added at low lambda
                    np.random.seed(row * recon_grid_size + col + 42)
                    noise = np.random.randn() * 0.4

                    # Blend: small lambda => noisy, large lambda => blurred
                    if lam_val < 1.0:
                        # Interpolate from noisy to just right
                        t = lam_val
                        value = ideal + noise * (1.0 - t)
                    else:
                        # Interpolate from just right to over-smoothed
                        t = lam_val - 1.0
                        smoothed = 0.3  # uniform low value
                        value = ideal * (1.0 - t) + smoothed * t

                    value = float(np.clip(value, 0, 1))
                    cell_color = interpolate_color(BLACK, C["recon"], value)

                    cell = Square(
                        side_length=rc_cell,
                        stroke_color=C["dim"],
                        stroke_width=0.5,
                        fill_color=cell_color,
                        fill_opacity=0.9,
                    )
                    cell.move_to(
                        recon_origin
                        + RIGHT * col * rc_cell
                        + DOWN * row * rc_cell
                    )
                    grp.add(cell)
            return grp

        recon_grid = always_redraw(_build_recon_grid)
        self.add(recon_grid)

        # Lambda display
        lam_display = always_redraw(
            lambda: MathTex(
                r"\lambda = "
                + f"{10 ** (lam_tracker.get_value() * 3 - 3):.3f}",
                font_size=BODY_SIZE,
                color=C["highlight"],
            ).move_to(RIGHT * 4 + DOWN * 1.8)
        )
        self.add(lam_display)

        # Noise bar
        noise_bar_bg = Rectangle(
            width=0.4, height=2.0,
            stroke_color=C["absorb"], stroke_width=1,
            fill_color=BLACK, fill_opacity=0.3,
        ).move_to(RIGHT * 4 + DOWN * 3.2)
        noise_label = Text(
            "Noise", font_size=18, color=C["absorb"],
        ).next_to(noise_bar_bg, DOWN, buff=0.15)

        noise_fill = always_redraw(
            lambda: Rectangle(
                width=0.34,
                height=max(0.01, 1.8 * (1.0 - lam_tracker.get_value() / 2.0)),
                stroke_width=0, fill_color=C["absorb"], fill_opacity=0.7,
            ).align_to(noise_bar_bg, DOWN).shift(UP * 0.03)
        )

        # Blur bar
        blur_bar_bg = Rectangle(
            width=0.4, height=2.0,
            stroke_color=C["scatter"], stroke_width=1,
            fill_color=BLACK, fill_opacity=0.3,
        ).move_to(RIGHT * 5.2 + DOWN * 3.2)
        blur_label = Text(
            "Blur", font_size=18, color=C["scatter"],
        ).next_to(blur_bar_bg, DOWN, buff=0.15)

        blur_fill = always_redraw(
            lambda: Rectangle(
                width=0.34,
                height=max(0.01, 1.8 * lam_tracker.get_value() / 2.0),
                stroke_width=0, fill_color=C["scatter"], fill_opacity=0.7,
            ).align_to(blur_bar_bg, DOWN).shift(UP * 0.03)
        )

        self.play(
            FadeIn(noise_bar_bg), Write(noise_label),
            FadeIn(blur_bar_bg), Write(blur_label),
        )
        self.add(noise_fill, blur_fill)

        # Quality label driven by tracker
        quality_label = always_redraw(
            lambda: Text(
                (
                    "Too noisy"
                    if lam_tracker.get_value() < 0.4
                    else (
                        "Just right"
                        if lam_tracker.get_value() < 1.3
                        else "Too smooth"
                    )
                ),
                font_size=LABEL_SIZE,
                color=(
                    C["absorb"]
                    if lam_tracker.get_value() < 0.4
                    else (
                        C["highlight"]
                        if lam_tracker.get_value() < 1.3
                        else C["scatter"]
                    )
                ),
            ).next_to(recon_grid, DOWN, buff=0.3)
        )
        self.add(quality_label)
        self.wait(0.5, frozen_frame=False)

        # Sweep: small lambda (noisy)
        self.play(lam_tracker.animate.set_value(0.0), run_time=0.5)
        self.wait(1.5, frozen_frame=False)

        # Sweep to just right
        self.play(
            lam_tracker.animate.set_value(1.0),
            run_time=3,
            rate_func=smooth,
        )
        self.wait(HOLD, frozen_frame=False)

        # Sweep to too smooth
        self.play(
            lam_tracker.animate.set_value(2.0),
            run_time=3,
            rate_func=smooth,
        )
        self.wait(1.5, frozen_frame=False)

        # Sweep back to optimal
        self.play(
            lam_tracker.animate.set_value(1.0),
            run_time=2,
            rate_func=smooth,
        )
        self.wait(HOLD, frozen_frame=False)

        # ---- Phase 5: Final result ----
        final_txt = Text(
            "Clean reconstructed activation map",
            font_size=BODY_SIZE, color=C["recon"],
        )
        final_rect = SurroundingRectangle(
            recon_grid, color=C["recon"], buff=0.15, corner_radius=0.1,
        )
        final_txt.next_to(final_rect, RIGHT, buff=0.4).shift(UP * 0.5)
        self.play(Create(final_rect), Write(final_txt), run_time=1)
        self.wait(HOLD)

        # Cleanup
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
        self.wait(0.5)


# ===================================================================
# Scene 9 -- HDDOT
# "High-Density DOT: Seeing Deeper" (~1 min)
# ===================================================================


class HDDOT(Scene):
    """Sparse vs HD-DOT, multi-distance sensing, short-channel regression."""

    def construct(self) -> None:
        title = Text(
            "High-Density DOT: Seeing Deeper",
            font_size=TITLE_SIZE, color=C["highlight"],
        )
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(1)

        # ---- Phase 1: Sparse layout ----
        head_arc = Arc(
            radius=2.5, angle=PI, start_angle=0,
            color=C["tissue"], stroke_width=3,
        ).shift(DOWN * 0.8)
        head_line = Line(
            head_arc.get_start(), head_arc.get_end(),
            color=C["tissue"], stroke_width=3,
        )
        head = VGroup(head_arc, head_line)

        self.play(Create(head))
        self.wait(0.5)

        # Sparse: 4 sources, 4 detectors
        sparse_sources = VGroup()
        sparse_detectors = VGroup()
        src_positions = [LEFT * 2 + UP * 0.5, LEFT * 0.7 + UP * 1.5,
                         RIGHT * 0.7 + UP * 1.5, RIGHT * 2 + UP * 0.5]
        det_positions = [LEFT * 1.4 + UP * 0.2, LEFT * 0.0 + UP * 1.8,
                         RIGHT * 1.4 + UP * 0.2, RIGHT * 0.0 + UP * 0.8]

        for pos in src_positions:
            d = Dot(pos + DOWN * 0.8, radius=0.1, color=C["source"])
            sparse_sources.add(d)
        for pos in det_positions:
            d = Dot(pos + DOWN * 0.8, radius=0.1, color=C["detector"])
            sparse_detectors.add(d)

        sparse_label = Text(
            "Standard fNIRS: ~20 channels",
            font_size=BODY_SIZE, color=C["label"],
        ).to_edge(DOWN, buff=0.6)

        self.play(
            LaggedStart(*[FadeIn(d) for d in sparse_sources], lag_ratio=0.1),
            LaggedStart(*[FadeIn(d) for d in sparse_detectors], lag_ratio=0.1),
            Write(sparse_label),
            run_time=1,
        )
        self.wait(HOLD)

        # ---- Phase 2: HD-DOT layout ----
        hd_sources = VGroup()
        hd_detectors = VGroup()

        # Dense grid on the head arc
        for i in range(12):
            angle = PI * (0.1 + 0.8 * i / 11)
            r = 2.5
            pos = np.array([
                r * np.cos(angle),
                r * np.sin(angle) - 0.8,
                0,
            ])
            color = C["source"] if i % 2 == 0 else C["detector"]
            dot = Dot(pos, radius=0.07, color=color)
            if i % 2 == 0:
                hd_sources.add(dot)
            else:
                hd_detectors.add(dot)

        # Additional inner ring
        for i in range(8):
            angle = PI * (0.15 + 0.7 * i / 7)
            r = 2.0
            pos = np.array([
                r * np.cos(angle),
                r * np.sin(angle) - 0.8,
                0,
            ])
            color = C["detector"] if i % 2 == 0 else C["source"]
            dot = Dot(pos, radius=0.07, color=color)
            if color == C["source"]:
                hd_sources.add(dot)
            else:
                hd_detectors.add(dot)

        hd_label = Text(
            "HD-DOT: 1000+ channels",
            font_size=BODY_SIZE, color=C["highlight"],
        ).to_edge(DOWN, buff=0.6)

        self.play(
            FadeOut(sparse_sources, sparse_detectors, sparse_label),
            LaggedStart(*[FadeIn(d) for d in hd_sources], lag_ratio=0.04),
            LaggedStart(*[FadeIn(d) for d in hd_detectors], lag_ratio=0.04),
            ReplacementTransform(sparse_label.copy(), hd_label),
            run_time=1.5,
        )
        self.wait(HOLD)

        # ---- Phase 3: Multiple source-detector distances ----
        self.play(
            FadeOut(head, hd_sources, hd_detectors, hd_label),
            run_time=0.6,
        )

        dist_title = Text(
            "Multiple distances from the SAME region",
            font_size=BODY_SIZE, color=C["scatter"],
        ).next_to(title, DOWN, buff=0.5)
        self.play(Write(dist_title))
        self.wait(0.5)

        # Draw a tissue cross-section
        tissue_rect = Rectangle(
            width=10, height=3.5,
            fill_color=C["tissue"], fill_opacity=0.1,
            stroke_color=C["tissue"], stroke_width=1,
        ).shift(DOWN * 1.5)
        scalp_line = Line(
            LEFT * 5 + DOWN * 0.0, RIGHT * 5 + DOWN * 0.0,
            color=C["tissue"], stroke_width=2,
        )
        scalp_lbl = Text(
            "scalp surface", font_size=18, color=C["tissue"],
        ).next_to(scalp_line, RIGHT, buff=0.2).shift(UP * 0.15)

        self.play(Create(tissue_rect), Create(scalp_line), Write(scalp_lbl))

        # Source on surface
        src = Dot(LEFT * 2 + DOWN * 0.0, radius=0.15, color=C["source"])
        src_label = Text("S", font_size=LABEL_SIZE, color=C["source"])
        src_label.next_to(src, UP, buff=0.15)
        self.play(FadeIn(src), Write(src_label))

        # Short separation banana (8mm ~ 0.8 units)
        det_short = Dot(LEFT * 1.2 + DOWN * 0.0, radius=0.12, color=C["detector"])
        banana_short = Arc(
            radius=0.4, angle=PI, start_angle=0, color=C["sensitivity"],
            stroke_width=3, stroke_opacity=0.8,
        )
        banana_short.move_to((src.get_center() + det_short.get_center()) / 2)
        banana_short.shift(DOWN * 0.15)
        short_lbl = Text(
            "8mm: Sees scalp\nblood flow",
            font_size=18, color=C["sensitivity"],
        ).next_to(banana_short, DOWN, buff=0.15).shift(LEFT * 0.3)

        self.play(FadeIn(det_short), Create(banana_short), Write(short_lbl))
        self.wait(1)

        # Medium separation banana (25mm ~ 2.5 units)
        det_med = Dot(RIGHT * 0.5 + DOWN * 0.0, radius=0.12, color=C["detector"])
        banana_med = Arc(
            radius=1.25, angle=PI, start_angle=0, color=C["scatter"],
            stroke_width=3, stroke_opacity=0.8,
        )
        banana_med.move_to((src.get_center() + det_med.get_center()) / 2)
        banana_med.shift(DOWN * 0.3)
        med_lbl = Text(
            "25mm: Sees cortex",
            font_size=18, color=C["scatter"],
        ).next_to(banana_med, DOWN, buff=0.15)

        self.play(FadeIn(det_med), Create(banana_med), Write(med_lbl))
        self.wait(1)

        # Long separation banana (40mm ~ 4.0 units)
        det_long = Dot(RIGHT * 2.0 + DOWN * 0.0, radius=0.12, color=C["detector"])
        banana_long = Arc(
            radius=2.0, angle=PI, start_angle=0, color=C["recon"],
            stroke_width=3, stroke_opacity=0.8,
        )
        banana_long.move_to((src.get_center() + det_long.get_center()) / 2)
        banana_long.shift(DOWN * 0.5)
        long_lbl = Text(
            "40mm: Sees deep brain",
            font_size=18, color=C["recon"],
        ).next_to(banana_long, DOWN, buff=0.15)

        self.play(FadeIn(det_long), Create(banana_long), Write(long_lbl))
        self.wait(HOLD)

        # ---- Phase 4: Short-channel regression ----
        phase3_clear = VGroup(
            dist_title, tissue_rect, scalp_line, scalp_lbl,
            src, src_label,
            det_short, banana_short, short_lbl,
            det_med, banana_med, med_lbl,
            det_long, banana_long, long_lbl,
        )
        self.play(FadeOut(phase3_clear), run_time=0.6)

        reg_title = Text(
            "Short-Channel Regression",
            font_size=BODY_SIZE, color=C["scatter"],
        ).next_to(title, DOWN, buff=0.5)
        self.play(Write(reg_title))
        self.wait(0.5)

        # Signal bars
        bar_width = 3.5
        bar_height = 0.6
        bar_y_start = DOWN * 0.3

        # Raw signal
        raw_bar = Rectangle(
            width=bar_width, height=bar_height,
            fill_color=C["detector"], fill_opacity=0.5,
            stroke_color=C["detector"], stroke_width=2,
        ).move_to(LEFT * 1.5 + bar_y_start)
        raw_lbl = Text(
            "Raw signal", font_size=LABEL_SIZE, color=C["detector"],
        ).next_to(raw_bar, LEFT, buff=0.3)
        raw_eq = MathTex(
            r"= \text{scalp} + \text{brain}",
            font_size=LABEL_SIZE,
        ).next_to(raw_bar, RIGHT, buff=0.3)

        self.play(FadeIn(raw_bar), Write(raw_lbl), Write(raw_eq))
        self.wait(1)

        # Scalp estimate from short channel
        scalp_bar = Rectangle(
            width=bar_width * 0.4, height=bar_height,
            fill_color=C["absorb"], fill_opacity=0.5,
            stroke_color=C["absorb"], stroke_width=2,
        ).move_to(LEFT * 2.6 + bar_y_start + DOWN * 1.2)
        scalp_lbl = Text(
            "Short channel", font_size=LABEL_SIZE, color=C["absorb"],
        ).next_to(scalp_bar, LEFT, buff=0.3)
        scalp_eq = MathTex(
            r"\approx \text{scalp signal}",
            font_size=LABEL_SIZE,
        ).next_to(scalp_bar, RIGHT, buff=0.3)

        self.play(FadeIn(scalp_bar), Write(scalp_lbl), Write(scalp_eq))
        self.wait(1)

        # Subtraction
        minus_sign = MathTex(r"-", font_size=48, color=C["highlight"])
        minus_sign.move_to(LEFT * 4.5 + bar_y_start + DOWN * 2.4)

        brain_bar = Rectangle(
            width=bar_width * 0.6, height=bar_height,
            fill_color=C["recon"], fill_opacity=0.6,
            stroke_color=C["recon"], stroke_width=2,
        ).move_to(LEFT * 1.5 + bar_y_start + DOWN * 2.4)
        brain_lbl = Text(
            "Brain signal", font_size=LABEL_SIZE, color=C["recon"],
        ).next_to(brain_bar, LEFT, buff=0.3)
        brain_eq = MathTex(
            r"= \text{raw} - \text{scalp}",
            font_size=LABEL_SIZE,
        ).next_to(brain_bar, RIGHT, buff=0.3)

        # Animate the subtraction
        arrow_down = Arrow(
            raw_bar.get_bottom(), brain_bar.get_top(),
            buff=0.15, color=C["highlight"], stroke_width=2, tip_length=0.15,
        )
        self.play(GrowArrow(arrow_down), Write(minus_sign))
        self.play(FadeIn(brain_bar), Write(brain_lbl), Write(brain_eq))
        self.wait(HOLD)

        # ---- Phase 5: Takeaway ----
        takeaway = Text(
            "HD-DOT approaches fMRI resolution.\n"
            "Portable. Silent. Safe for babies.",
            font_size=BODY_SIZE, color=C["highlight"],
            line_spacing=1.3,
        ).to_edge(DOWN, buff=0.5)

        self.play(Write(takeaway), run_time=1.5)
        self.wait(HOLD + 1)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
        self.wait(0.5)


# ===================================================================
# Scene 10 -- Pipeline
# "The Complete DOT Pipeline" (~0.5 min)
# ===================================================================


class Pipeline(Scene):
    """Horizontal flow of the full DOT pipeline."""

    def construct(self) -> None:
        title = Text(
            "The Complete DOT Pipeline",
            font_size=TITLE_SIZE, color=C["highlight"],
        )
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(1)

        # Pipeline stages: label, color
        stages = [
            ("Light\nSource", C["source"]),
            ("Tissue\n(scatter/absorb)", C["tissue"]),
            ("Detectors", C["detector"]),
            ("Baseline\nSubtraction", C["sensitivity"]),
            ("A" + "\u2020", C["matrix"]),         # A-dagger
            ("Reconstructed\nImage", C["recon"]),
        ]

        boxes = VGroup()
        arrows = VGroup()

        for idx, (label, color) in enumerate(stages):
            box = labeled_box(
                label, color,
                width=1.8, height=1.1,
                font_size=18,
            )
            boxes.add(box)

        boxes.arrange(RIGHT, buff=0.45)
        boxes.move_to(ORIGIN + DOWN * 0.3)

        # If too wide, scale down
        if boxes.get_width() > 13:
            boxes.scale_to_fit_width(13)

        # Create arrows between boxes
        for i in range(len(stages) - 1):
            arr = Arrow(
                boxes[i].get_right(),
                boxes[i + 1].get_left(),
                buff=0.08,
                color=WHITE,
                stroke_width=2,
                tip_length=0.15,
            )
            arrows.add(arr)

        # Animate boxes and arrows one at a time
        for idx in range(len(stages)):
            self.play(FadeIn(boxes[idx], shift=UP * 0.3), run_time=0.5)
            if idx < len(stages) - 1:
                self.play(GrowArrow(arrows[idx]), run_time=0.3)
            self.wait(0.3)

        self.wait(1)

        # Final text
        final = Text(
            "Non-invasive. Portable. Safe for babies.\n"
            "That's Diffuse Optical Tomography.",
            font_size=BODY_SIZE,
            color=C["highlight"],
            line_spacing=1.3,
        ).next_to(boxes, DOWN, buff=0.8)

        self.play(Write(final), run_time=2)
        self.wait(3)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
        self.wait(0.5)
