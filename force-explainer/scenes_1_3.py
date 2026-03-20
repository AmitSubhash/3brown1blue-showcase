"""Scenes 1-3 for FORCE paper explainer video.

Scene 1: WhatIsDiffusionMRI - what diffusion MRI measures from first principles
Scene 2: TheInverseProblemTrap - traditional approaches and their limitations
Scene 3: TheKeyInsight - the forward modeling paradigm shift
"""

from manim import *
from style import *

import numpy as np


# ---------------------------------------------------------------------------
# Scene 1: What is Diffusion MRI?
# ---------------------------------------------------------------------------
class WhatIsDiffusionMRI(Scene):
    """Build intuition for diffusion MRI from first principles (~1.5 min)."""

    def construct(self) -> None:
        # ---- 1. Title ----
        title = section_title("What is Diffusion MRI?", color=SIGNAL_BLUE)
        self.play(Write(title))
        self.wait(0.5)

        # ---- 2. Brain with zoomed-in voxel containing axon bundles ----
        brain_outline = Ellipse(
            width=3.0, height=3.5, color=GM_COLOR, stroke_width=3
        ).shift(LEFT * 3.5 + DOWN * 0.3)
        brain_label = label_text("Brain").next_to(brain_outline, DOWN, buff=0.3)

        # A small square representing one voxel
        voxel_rect = Square(
            side_length=0.5, color=YELLOW, stroke_width=2
        ).move_to(brain_outline.get_center() + RIGHT * 0.3 + UP * 0.3)

        self.play(
            Create(brain_outline),
            Write(brain_label),
            run_time=1.5,
        )
        self.play(Create(voxel_rect))
        self.wait(0.3)

        # Zoom arrow from voxel to a larger view on the right
        zoomed_box = Rectangle(
            width=4.0, height=3.5, color=WHITE, stroke_width=2
        ).shift(RIGHT * 2.5 + DOWN * 0.3)
        zoom_arrow = Arrow(
            voxel_rect.get_right(),
            zoomed_box.get_left(),
            buff=0.15,
            color=YELLOW,
            stroke_width=3,
        )
        zoom_label = label_text("1 voxel (~2mm)", color=YELLOW).next_to(
            zoom_arrow, UP, buff=0.15
        )

        self.play(
            GrowArrow(zoom_arrow),
            Write(zoom_label),
            Create(zoomed_box),
            run_time=1.2,
        )

        # Axon bundles inside the zoomed view (parallel lines = fibers)
        axon_group = VGroup()
        fiber_start_x = zoomed_box.get_left()[0] + 0.3
        fiber_end_x = zoomed_box.get_right()[0] - 0.3
        fiber_center_y = zoomed_box.get_center()[1]
        for i in range(7):
            y_offset = (i - 3) * 0.35 + fiber_center_y
            fiber = Line(
                start=np.array([fiber_start_x, y_offset, 0]),
                end=np.array([fiber_end_x, y_offset, 0]),
                color=FIBER_GREEN,
                stroke_width=3,
                stroke_opacity=0.8,
            )
            axon_group.add(fiber)

        axon_label = label_text("Axon bundles", color=FIBER_GREEN).next_to(
            zoomed_box, UP, buff=0.2
        )
        self.play(
            LaggedStart(
                *[Create(f) for f in axon_group],
                lag_ratio=0.1,
            ),
            Write(axon_label),
            run_time=1.5,
        )
        self.wait(0.5)

        # ---- 3. Water molecules doing random walks ----
        np.random.seed(42)
        water_dots = VGroup()
        for _ in range(15):
            cx = zoomed_box.get_center()[0] + np.random.uniform(-1.5, 1.5)
            cy = zoomed_box.get_center()[1] + np.random.uniform(-1.2, 1.2)
            dot = Dot(
                point=np.array([cx, cy, 0]),
                radius=0.06,
                color=SIGNAL_BLUE,
            )
            water_dots.add(dot)

        water_label = label_text("Water molecules", color=SIGNAL_BLUE).next_to(
            zoomed_box, DOWN, buff=0.3
        )
        self.play(
            LaggedStart(
                *[FadeIn(d, scale=0.5) for d in water_dots],
                lag_ratio=0.05,
            ),
            Write(water_label),
            run_time=1.0,
        )

        # Animate jiggling for a moment (random walk)
        for d in water_dots:
            d.add_updater(
                lambda m, dt: m.shift(
                    np.array([
                        np.random.normal(0, 0.3) * dt,
                        np.random.normal(0, 0.3) * dt,
                        0,
                    ])
                )
            )
        self.wait(2, frozen_frame=False)

        # Stop jiggling
        for d in water_dots:
            d.clear_updaters()

        # ---- 4. Key insight: free along, restricted perpendicular ----
        note1 = bottom_note("Water diffuses FREELY along axons...")
        self.play(Write(note1))
        self.wait(1.0)

        # Show a horizontal double arrow (along fiber) = free
        along_arrow = DoubleArrow(
            start=zoomed_box.get_center() + LEFT * 1.2,
            end=zoomed_box.get_center() + RIGHT * 1.2,
            color=FIBER_GREEN,
            buff=0,
            stroke_width=5,
        )
        along_label = label_text("FREE", color=FIBER_GREEN).next_to(
            along_arrow, UP, buff=0.15
        )
        self.play(GrowArrow(along_arrow), Write(along_label), run_time=0.8)
        self.wait(0.5)

        # Replace bottom note
        note2 = bottom_note("...but is RESTRICTED perpendicular to them")
        self.play(FadeOut(note1))
        self.play(Write(note2))

        # Show a short vertical double arrow (perpendicular) = restricted
        perp_arrow = DoubleArrow(
            start=zoomed_box.get_center() + DOWN * 0.4,
            end=zoomed_box.get_center() + UP * 0.4,
            color=INVERSE_RED,
            buff=0,
            stroke_width=5,
        )
        perp_label = label_text("RESTRICTED", color=INVERSE_RED).next_to(
            perp_arrow, RIGHT, buff=0.15
        )
        self.play(GrowArrow(perp_arrow), Write(perp_label), run_time=0.8)
        self.wait(1.0)

        # ---- 5. Clear and show MRI gradient ----
        self.play(
            FadeOut(note2),
            FadeOut(along_arrow), FadeOut(along_label),
            FadeOut(perp_arrow), FadeOut(perp_label),
            FadeOut(water_dots), FadeOut(water_label),
            FadeOut(brain_outline), FadeOut(brain_label),
            FadeOut(voxel_rect), FadeOut(zoom_arrow), FadeOut(zoom_label),
            FadeOut(axon_label),
        )

        # Keep zoomed box and fibers, shift to left
        content_group = VGroup(zoomed_box, axon_group)
        self.play(content_group.animate.shift(LEFT * 1.5), run_time=0.8)

        # MRI scanner applies a gradient g
        gradient_tracker = ValueTracker(0)  # angle of gradient direction
        gradient_origin = zoomed_box.get_center()

        gradient_arrow = always_redraw(
            lambda: Arrow(
                start=gradient_origin,
                end=gradient_origin
                + 1.5
                * np.array([
                    np.cos(gradient_tracker.get_value()),
                    np.sin(gradient_tracker.get_value()),
                    0,
                ]),
                color=MATCH_GOLD,
                stroke_width=5,
                buff=0,
            )
        )
        g_label = always_redraw(
            lambda: MathTex(
                r"\vec{g}", font_size=EQ_SIZE, color=MATCH_GOLD
            ).next_to(
                gradient_origin
                + 1.7
                * np.array([
                    np.cos(gradient_tracker.get_value()),
                    np.sin(gradient_tracker.get_value()),
                    0,
                ]),
                direction=np.array([
                    np.cos(gradient_tracker.get_value()),
                    np.sin(gradient_tracker.get_value()),
                    0,
                ]),
                buff=0.1,
            )
        )

        scanner_note = label_text(
            "MRI gradient direction", color=MATCH_GOLD
        ).next_to(zoomed_box, DOWN, buff=0.4)

        self.play(
            Create(gradient_arrow),
            Write(g_label),
            Write(scanner_note),
            run_time=1.0,
        )
        self.wait(0.5, frozen_frame=False)

        # ---- 6. Show signal equation ----
        signal_eq = MathTex(
            r"S", r"=", r"S_0", r"\cdot",
            r"e^{", r"-b", r"\,\vec{g}^T", r"\mathbf{D}", r"\vec{g}", r"}",
            font_size=SMALL_EQ,
        ).shift(RIGHT * 2.5 + UP * 2.5)
        signal_eq[0].set_color(SIGNAL_BLUE)
        signal_eq[2].set_color(WHITE)
        signal_eq[5].set_color(COSINE_ORANGE)
        signal_eq[6].set_color(MATCH_GOLD)
        signal_eq[7].set_color(FIBER_GREEN)
        signal_eq[8].set_color(MATCH_GOLD)

        eq_box = SurroundingRectangle(
            signal_eq, color=WHITE, buff=0.2, corner_radius=0.1, stroke_width=1
        )

        self.play(Write(signal_eq), Create(eq_box), run_time=1.5)
        self.wait(0.5)

        # ---- 7. Rotate gradient to show signal change ----
        # Signal bar on the right that reacts to gradient angle
        signal_bar_bg = Rectangle(
            width=0.6, height=2.5, color=DIMMED, fill_opacity=0.3, stroke_width=1
        ).shift(RIGHT * 5.5 + DOWN * 0.5)
        signal_label_top = label_text("Signal", color=SIGNAL_BLUE).next_to(
            signal_bar_bg, UP, buff=0.2
        )

        signal_bar = always_redraw(
            lambda: Rectangle(
                width=0.5,
                height=max(
                    0.05,
                    2.4
                    * np.exp(
                        -2.0 * np.cos(gradient_tracker.get_value()) ** 2
                    ),
                ),
                color=SIGNAL_BLUE,
                fill_opacity=0.8,
                stroke_width=0,
            ).align_to(signal_bar_bg, DOWN).shift(UP * 0.05)
        )

        self.play(
            Create(signal_bar_bg),
            Write(signal_label_top),
            FadeIn(signal_bar),
            run_time=0.8,
        )
        self.wait(0.3, frozen_frame=False)

        # Gradient along fiber (angle=0) -> strong attenuation (low signal)
        note3 = bottom_note(
            "Gradient along fiber: free diffusion, strong signal loss"
        )
        self.play(Write(note3))
        self.play(
            gradient_tracker.animate.set_value(0),
            run_time=1.5,
            rate_func=smooth,
        )
        self.wait(1.0, frozen_frame=False)

        # Gradient perpendicular (angle=PI/2) -> weak attenuation (high signal)
        note4 = bottom_note(
            "Gradient perpendicular: restricted diffusion, weak signal loss"
        )
        self.play(FadeOut(note3))
        self.play(Write(note4))
        self.play(
            gradient_tracker.animate.set_value(PI / 2),
            run_time=1.5,
            rate_func=smooth,
        )
        self.wait(1.0, frozen_frame=False)

        # Continue rotating to show continuous relationship
        self.play(
            gradient_tracker.animate.set_value(2 * PI),
            run_time=4,
            rate_func=linear,
        )
        self.wait(0.5, frozen_frame=False)

        # ---- 8. Isotropic vs anisotropic signal profiles ----
        self.play(
            FadeOut(note4),
            FadeOut(gradient_arrow), FadeOut(g_label),
            FadeOut(scanner_note),
            FadeOut(signal_bar), FadeOut(signal_bar_bg), FadeOut(signal_label_top),
            FadeOut(signal_eq), FadeOut(eq_box),
            FadeOut(content_group),
        )

        # Isotropic profile (sphere-like)
        iso_profile = Circle(
            radius=1.0, color=CSF_COLOR, fill_opacity=0.3, stroke_width=3
        ).shift(LEFT * 3 + DOWN * 0.3)
        iso_label = body_text("Isotropic", color=CSF_COLOR).next_to(
            iso_profile, UP, buff=0.3
        )
        iso_sub = label_text("(e.g. CSF, gray matter)", color=CSF_COLOR).next_to(
            iso_label, DOWN, buff=0.15
        )

        # Anisotropic profile (elongated ellipse)
        aniso_profile = Ellipse(
            width=3.0, height=0.8, color=FIBER_GREEN,
            fill_opacity=0.3, stroke_width=3,
        ).shift(RIGHT * 3 + DOWN * 0.3)
        aniso_label = body_text("Anisotropic", color=FIBER_GREEN).next_to(
            aniso_profile, UP, buff=0.3
        )
        aniso_sub = label_text(
            "(e.g. white matter tracts)", color=FIBER_GREEN
        ).next_to(aniso_label, DOWN, buff=0.15)

        # Directional arrows on each
        iso_arrows = VGroup()
        for angle in np.linspace(0, 2 * PI, 8, endpoint=False):
            arr = Arrow(
                start=iso_profile.get_center(),
                end=iso_profile.get_center()
                + 0.9 * np.array([np.cos(angle), np.sin(angle), 0]),
                buff=0,
                color=CSF_COLOR,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.2,
            )
            iso_arrows.add(arr)

        aniso_arrows = VGroup()
        for angle in np.linspace(0, 2 * PI, 8, endpoint=False):
            length = 0.3 + 1.2 * abs(np.cos(angle))
            arr = Arrow(
                start=aniso_profile.get_center(),
                end=aniso_profile.get_center()
                + length * np.array([np.cos(angle), np.sin(angle), 0]),
                buff=0,
                color=FIBER_GREEN,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.2,
            )
            aniso_arrows.add(arr)

        self.play(
            Create(iso_profile), Write(iso_label), Write(iso_sub),
            Create(aniso_profile), Write(aniso_label), Write(aniso_sub),
            run_time=1.5,
        )
        self.play(
            LaggedStart(
                *[GrowArrow(a) for a in iso_arrows],
                lag_ratio=0.1,
            ),
            LaggedStart(
                *[GrowArrow(a) for a in aniso_arrows],
                lag_ratio=0.1,
            ),
            run_time=1.5,
        )
        self.wait(1.0)

        # Equal arrows vs unequal arrows explanation
        eq_note = label_text(
            "Equal in all directions", color=CSF_COLOR
        ).next_to(iso_profile, DOWN, buff=0.4)
        neq_note = label_text(
            "Longest along fiber axis", color=FIBER_GREEN
        ).next_to(aniso_profile, DOWN, buff=0.4)
        self.play(Write(eq_note), Write(neq_note))
        self.wait(1.0)

        # ---- 9. Final bottom note ----
        note_final = bottom_note(
            "The diffusion signal ENCODES tissue microstructure"
        )
        self.play(FadeOut(eq_note), FadeOut(neq_note))
        self.play(Write(note_final))
        self.wait(2.0)

        # Fade everything
        self.play(*[FadeOut(m) for m in self.mobjects])
        self.wait(0.5)


# ---------------------------------------------------------------------------
# Scene 2: The Inverse Problem Trap
# ---------------------------------------------------------------------------
class TheInverseProblemTrap(Scene):
    """Traditional approaches and their limitations (~2 min)."""

    def construct(self) -> None:
        # ---- 1. Title ----
        title = section_title("The Inverse Problem", color=INVERSE_RED)
        self.play(Write(title))
        self.wait(0.5)

        # ---- 2. Pipeline: Signal -> [??] -> Tissue Properties ----
        signal_box = Rectangle(
            width=2.2, height=1.0, color=SIGNAL_BLUE,
            fill_opacity=0.2, stroke_width=2,
        ).shift(LEFT * 4.5 + UP * 1.5)
        signal_text = body_text("Brain\nSignal", color=SIGNAL_BLUE).scale(0.7)
        signal_text.move_to(signal_box)

        black_box = Rectangle(
            width=2.5, height=1.0, color=DIMMED,
            fill_opacity=0.6, stroke_width=2,
        ).shift(UP * 1.5)
        bb_text = body_text("?? Black Box ??", color=INVERSE_RED).scale(0.65)
        bb_text.move_to(black_box)

        tissue_box = Rectangle(
            width=2.5, height=1.0, color=FIBER_GREEN,
            fill_opacity=0.2, stroke_width=2,
        ).shift(RIGHT * 4.5 + UP * 1.5)
        tissue_text = body_text("Tissue\nProperties", color=FIBER_GREEN).scale(0.7)
        tissue_text.move_to(tissue_box)

        arrow1 = Arrow(
            signal_box.get_right(), black_box.get_left(),
            buff=0.1, color=WHITE, stroke_width=3,
        )
        arrow2 = Arrow(
            black_box.get_right(), tissue_box.get_left(),
            buff=0.1, color=WHITE, stroke_width=3,
        )

        pipeline = VGroup(
            signal_box, signal_text, arrow1,
            black_box, bb_text, arrow2,
            tissue_box, tissue_text,
        )

        self.play(
            FadeIn(signal_box), Write(signal_text),
            GrowArrow(arrow1),
            FadeIn(black_box), Write(bb_text),
            GrowArrow(arrow2),
            FadeIn(tissue_box), Write(tissue_text),
            run_time=2.0,
        )
        self.wait(1.0)

        # Fade title, shrink pipeline to top
        self.play(FadeOut(title), run_time=0.3)
        self.play(pipeline.animate.scale(0.6).to_edge(UP, buff=0.3), run_time=0.8)

        # ---- 3. DTI: fit an ellipsoid ----
        dti_title = body_text("DTI: Diffusion Tensor Imaging", color=SIGNAL_BLUE)
        dti_title.next_to(pipeline, DOWN, buff=0.5)
        self.play(Write(dti_title))

        # Single fiber: elongated ellipsoid
        single_ellipse = Ellipse(
            width=2.5, height=0.7, color=SIGNAL_BLUE,
            fill_opacity=0.3, stroke_width=3,
        ).shift(LEFT * 3 + DOWN * 1.0)
        single_label = label_text(
            "Single fiber: FA is high", color=SIGNAL_BLUE
        ).next_to(single_ellipse, DOWN, buff=0.25)

        # Fiber lines through the ellipse
        single_fibers = VGroup(
            Line(
                single_ellipse.get_left() + RIGHT * 0.1,
                single_ellipse.get_right() + LEFT * 0.1,
                color=FIBER_GREEN, stroke_width=2,
            )
        )

        self.play(
            Create(single_ellipse),
            Create(single_fibers),
            Write(single_label),
            run_time=1.2,
        )
        self.wait(0.5)

        # Two crossing fibers: ellipsoid becomes spherical
        crossing_ellipse = Ellipse(
            width=1.5, height=1.4, color=INVERSE_RED,
            fill_opacity=0.3, stroke_width=3,
        ).shift(RIGHT * 3 + DOWN * 1.0)

        crossing_fibers = VGroup(
            Line(
                crossing_ellipse.get_center() + LEFT * 0.8 + DOWN * 0.5,
                crossing_ellipse.get_center() + RIGHT * 0.8 + UP * 0.5,
                color=FIBER_GREEN, stroke_width=2,
            ),
            Line(
                crossing_ellipse.get_center() + LEFT * 0.8 + UP * 0.5,
                crossing_ellipse.get_center() + RIGHT * 0.8 + DOWN * 0.5,
                color=FIBER_GREEN, stroke_width=2,
            ),
        )
        crossing_label = label_text(
            "Crossing fibers: FA drops!", color=INVERSE_RED
        ).next_to(crossing_ellipse, DOWN, buff=0.25)

        # X mark on the crossing case
        cross_mark = Cross(
            crossing_ellipse, stroke_color=INVERSE_RED, stroke_width=4
        ).scale(0.6)

        self.play(
            Create(crossing_ellipse),
            Create(crossing_fibers),
            Write(crossing_label),
            run_time=1.2,
        )
        self.play(Create(cross_mark), run_time=0.5)

        note_dti = bottom_note("DTI cannot resolve crossing fibers (60-90% of WM voxels)")
        self.play(Write(note_dti))
        self.wait(1.5)

        # Clear DTI section
        self.play(
            FadeOut(dti_title),
            FadeOut(single_ellipse), FadeOut(single_fibers), FadeOut(single_label),
            FadeOut(crossing_ellipse), FadeOut(crossing_fibers),
            FadeOut(crossing_label), FadeOut(cross_mark),
            FadeOut(note_dti),
        )

        # ---- 4. CSD: deconvolve to get ODF ----
        csd_title = body_text(
            "CSD: Constrained Spherical Deconvolution", color=COSINE_ORANGE
        )
        csd_title.next_to(pipeline, DOWN, buff=0.5)
        self.play(Write(csd_title))

        # ODF with two peaks (peanut shape from parametric curve)
        odf_center = DOWN * 1.0
        odf_good = always_redraw(
            lambda: ParametricFunction(
                lambda t: odf_center + np.array([
                    (0.5 + 0.8 * np.abs(np.cos(t))) * np.cos(t),
                    (0.5 + 0.8 * np.abs(np.cos(t))) * np.sin(t),
                    0,
                ]),
                t_range=[0, TAU],
                color=COSINE_ORANGE,
                fill_opacity=0.2,
                stroke_width=3,
            )
        )
        odf_label_good = label_text(
            "ODF: two clear peaks", color=COSINE_ORANGE
        ).next_to(odf_good, DOWN, buff=0.3)

        # Peak arrows
        peak1_arrow = Arrow(
            odf_center, odf_center + RIGHT * 1.3,
            buff=0, color=FIBER_GREEN, stroke_width=3,
        )
        peak2_arrow = Arrow(
            odf_center, odf_center + LEFT * 1.3,
            buff=0, color=FIBER_GREEN, stroke_width=3,
        )

        self.play(Create(odf_good), Write(odf_label_good), run_time=1.0)
        self.play(GrowArrow(peak1_arrow), GrowArrow(peak2_arrow), run_time=0.8)
        self.wait(0.5)

        # Problem: crossing angle < 40 degrees
        note_csd = bottom_note("But fails when crossing angle < 40 degrees: peaks merge!")
        self.play(Write(note_csd))
        self.wait(1.0)

        # Show merged peaks (close angles - looks like single lobe)
        merged_center = odf_center
        odf_merged = ParametricFunction(
            lambda t: merged_center + np.array([
                (0.6 + 0.5 * np.abs(np.cos(t - 0.3))) * np.cos(t),
                (0.6 + 0.5 * np.abs(np.cos(t - 0.3))) * np.sin(t),
                0,
            ]),
            t_range=[0, TAU],
            color=INVERSE_RED,
            fill_opacity=0.2,
            stroke_width=3,
        )
        merged_label = label_text(
            "Peaks merged: information lost", color=INVERSE_RED
        ).next_to(odf_merged, DOWN, buff=0.3)
        cross_csd = Cross(odf_merged, stroke_color=INVERSE_RED, stroke_width=4).scale(0.5)

        self.play(
            FadeOut(odf_good), FadeOut(odf_label_good),
            FadeOut(peak1_arrow), FadeOut(peak2_arrow),
            Create(odf_merged), Write(merged_label),
            run_time=1.0,
        )
        self.play(Create(cross_csd), run_time=0.5)
        self.wait(1.0)

        # Clear CSD
        self.play(
            FadeOut(csd_title), FadeOut(odf_merged), FadeOut(merged_label),
            FadeOut(cross_csd), FadeOut(note_csd),
        )

        # ---- 5. NODDI: multi-compartment ----
        noddi_title = body_text(
            "NODDI: Multi-Compartment Model", color=EXTRA_COLOR
        )
        noddi_title.next_to(pipeline, DOWN, buff=0.5)
        self.play(Write(noddi_title))

        # Compartment shapes
        compartment_y = DOWN * 1.0
        stick = Line(
            LEFT * 0.8 + compartment_y + LEFT * 3.5,
            RIGHT * 0.8 + compartment_y + LEFT * 3.5,
            color=INTRA_COLOR, stroke_width=6,
        )
        stick_label = label_text("Stick\n(intra-axonal)", color=INTRA_COLOR).scale(
            0.85
        ).next_to(stick, DOWN, buff=0.25)

        zeppelin = Ellipse(
            width=1.8, height=0.6, color=EXTRA_COLOR,
            fill_opacity=0.3, stroke_width=3,
        ).move_to(compartment_y)
        zeppelin_label = label_text(
            "Zeppelin\n(extra-axonal)", color=EXTRA_COLOR
        ).scale(0.85).next_to(zeppelin, DOWN, buff=0.25)

        ball = Circle(
            radius=0.5, color=CSF_COLOR,
            fill_opacity=0.3, stroke_width=3,
        ).move_to(compartment_y + RIGHT * 3.5)
        ball_label = label_text(
            "Ball\n(free water)", color=CSF_COLOR
        ).scale(0.85).next_to(ball, DOWN, buff=0.25)

        plus1 = MathTex("+", font_size=BODY_SIZE).move_to(
            (stick.get_center() + zeppelin.get_center()) / 2
        )
        plus2 = MathTex("+", font_size=BODY_SIZE).move_to(
            (zeppelin.get_center() + ball.get_center()) / 2
        )

        self.play(
            Create(stick), Write(stick_label),
            Write(plus1),
            Create(zeppelin), Write(zeppelin_label),
            Write(plus2),
            Create(ball), Write(ball_label),
            run_time=1.5,
        )
        self.wait(0.5)

        # NODDI problems
        note_noddi = bottom_note(
            "Assumes single fiber, requires multi-shell, slow nonlinear fitting"
        )
        self.play(Write(note_noddi))

        noddi_problems = VGroup()
        problem_texts = [
            "Single fiber only",
            "Multi-shell required",
            "Nonlinear fitting",
        ]
        for i, txt in enumerate(problem_texts):
            prob = label_text(txt, color=INVERSE_RED).shift(
                RIGHT * 3.5 + DOWN * (0.3 + i * 0.4)
            )
            noddi_problems.add(prob)

        cross_noddi = Cross(
            VGroup(stick, zeppelin, ball),
            stroke_color=INVERSE_RED,
            stroke_width=3,
        ).scale(0.7)

        self.play(
            LaggedStart(
                *[Write(p) for p in noddi_problems],
                lag_ratio=0.3,
            ),
            Create(cross_noddi),
            run_time=1.5,
        )
        self.wait(1.0)

        # Clear NODDI
        self.play(
            FadeOut(noddi_title),
            FadeOut(stick), FadeOut(stick_label),
            FadeOut(zeppelin), FadeOut(zeppelin_label),
            FadeOut(ball), FadeOut(ball_label),
            FadeOut(plus1), FadeOut(plus2),
            FadeOut(noddi_problems), FadeOut(cross_noddi),
            FadeOut(note_noddi),
        )

        # ---- 6. The fragmented landscape ----
        frag_title = body_text(
            "The Fragmented Landscape", color=INVERSE_RED
        ).next_to(pipeline, DOWN, buff=0.4)
        self.play(Write(frag_title))

        # Signal box on the left
        sig_box = Rectangle(
            width=1.8, height=1.0, color=SIGNAL_BLUE,
            fill_opacity=0.2, stroke_width=2,
        ).shift(LEFT * 5 + DOWN * 1.2)
        sig_text = label_text("Signal", color=SIGNAL_BLUE).move_to(sig_box)

        # Method boxes on the right
        method_names = ["DTI", "CSD", "NODDI", "DKI"]
        method_colors = [SIGNAL_BLUE, COSINE_ORANGE, EXTRA_COLOR, MATCH_GOLD]
        method_boxes = VGroup()
        method_texts = VGroup()
        method_arrows = VGroup()

        for i, (name, col) in enumerate(zip(method_names, method_colors)):
            box = Rectangle(
                width=1.6, height=0.7, color=col,
                fill_opacity=0.2, stroke_width=2,
            ).shift(RIGHT * (i * 2.0 - 1.5) + DOWN * 1.2)
            txt = label_text(name, color=col).move_to(box)
            arrow = Arrow(
                sig_box.get_right(), box.get_left(),
                buff=0.1, color=col, stroke_width=2,
            )
            method_boxes.add(box)
            method_texts.add(txt)
            method_arrows.add(arrow)

        self.play(FadeIn(sig_box), Write(sig_text), run_time=0.5)
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        FadeIn(method_boxes[i]),
                        Write(method_texts[i]),
                        GrowArrow(method_arrows[i]),
                    )
                    for i in range(4)
                ],
                lag_ratio=0.2,
            ),
            run_time=2.0,
        )
        self.wait(0.5)

        # Damning text
        frag_note = Text(
            "4 separate pipelines, 4 different assumptions,\n"
            "4 potentially inconsistent results",
            font_size=LABEL_SIZE,
            color=INVERSE_RED,
        ).next_to(method_boxes, DOWN, buff=0.5)
        self.play(Write(frag_note), run_time=1.5)
        self.wait(1.5)

        # ---- 7. Bridge ----
        self.play(*[FadeOut(m) for m in self.mobjects])
        story_bridge(self, "What if there's a better way?", color=MATCH_GOLD)
        self.wait(0.5)


# ---------------------------------------------------------------------------
# Scene 3: The Key Insight -- flip the problem
# ---------------------------------------------------------------------------
class TheKeyInsight(Scene):
    """The paradigm shift: forward modeling (~1.5 min)."""

    def construct(self) -> None:
        # ---- 1. Title ----
        title = section_title("Flip the Problem", color=FORWARD_GREEN)
        self.play(Write(title))
        self.wait(0.5)

        # ---- 2. Inverse direction ----
        inv_signal = Rectangle(
            width=2.2, height=0.9, color=SIGNAL_BLUE,
            fill_opacity=0.2, stroke_width=2,
        ).shift(LEFT * 4 + UP * 1.5)
        inv_signal_txt = label_text("Signal", color=SIGNAL_BLUE).move_to(inv_signal)

        inv_box = Rectangle(
            width=2.0, height=0.9, color=INVERSE_RED,
            fill_opacity=0.3, stroke_width=2,
        ).shift(UP * 1.5)
        inv_box_txt = label_text("Invert", color=INVERSE_RED).move_to(inv_box)

        inv_micro = Rectangle(
            width=2.5, height=0.9, color=FIBER_GREEN,
            fill_opacity=0.2, stroke_width=2,
        ).shift(RIGHT * 4 + UP * 1.5)
        inv_micro_txt = label_text(
            "Microstructure", color=FIBER_GREEN
        ).move_to(inv_micro)

        inv_arrow1 = Arrow(
            inv_signal.get_right(), inv_box.get_left(),
            buff=0.1, color=INVERSE_RED, stroke_width=3,
        )
        inv_arrow2 = Arrow(
            inv_box.get_right(), inv_micro.get_left(),
            buff=0.1, color=INVERSE_RED, stroke_width=3,
        )

        inv_group = VGroup(
            inv_signal, inv_signal_txt, inv_arrow1,
            inv_box, inv_box_txt, inv_arrow2,
            inv_micro, inv_micro_txt,
        )

        inv_heading = body_text(
            "Traditional: Inverse", color=INVERSE_RED
        ).next_to(inv_group, LEFT, buff=0.1).scale(0.65).shift(LEFT * 0.2)

        self.play(
            FadeIn(inv_signal), Write(inv_signal_txt),
            GrowArrow(inv_arrow1),
            FadeIn(inv_box), Write(inv_box_txt),
            GrowArrow(inv_arrow2),
            FadeIn(inv_micro), Write(inv_micro_txt),
            run_time=1.5,
        )

        # X marks for problems
        x_marks = VGroup()
        problem_labels = ["Ill-posed", "Noise-sensitive", "Local minima"]
        for i, prob in enumerate(problem_labels):
            x_mark = Text(
                "X", font_size=BODY_SIZE, color=INVERSE_RED, weight=BOLD
            ).next_to(inv_box, DOWN, buff=0.2 + i * 0.35)
            x_label = label_text(prob, color=INVERSE_RED).next_to(
                x_mark, RIGHT, buff=0.15
            )
            x_marks.add(VGroup(x_mark, x_label))

        self.play(
            LaggedStart(
                *[FadeIn(xm, shift=LEFT * 0.2) for xm in x_marks],
                lag_ratio=0.2,
            ),
            run_time=1.2,
        )
        self.wait(1.0)

        # ---- 3. Key question ----
        question = body_text(
            "What if we go FORWARD instead?", color=MATCH_GOLD
        ).shift(DOWN * 2.5)
        self.play(Write(question))
        self.wait(1.0)
        self.play(FadeOut(question))

        # ---- 4. Forward direction ----
        # Clear inverse problems
        self.play(FadeOut(x_marks))

        # Dim inverse row
        self.play(inv_group.animate.set_opacity(0.3), run_time=0.5)

        # Forward row below
        fwd_micro = Rectangle(
            width=2.5, height=0.9, color=FIBER_GREEN,
            fill_opacity=0.2, stroke_width=2,
        ).shift(LEFT * 4 + DOWN * 0.8)
        fwd_micro_txt = label_text(
            "Microstructure", color=FIBER_GREEN
        ).move_to(fwd_micro)

        fwd_box = Rectangle(
            width=2.0, height=0.9, color=FORWARD_GREEN,
            fill_opacity=0.3, stroke_width=2,
        ).shift(DOWN * 0.8)
        fwd_box_txt = label_text("Physics", color=FORWARD_GREEN).move_to(fwd_box)

        fwd_signal = Rectangle(
            width=2.2, height=0.9, color=SIGNAL_BLUE,
            fill_opacity=0.2, stroke_width=2,
        ).shift(RIGHT * 4 + DOWN * 0.8)
        fwd_signal_txt = label_text(
            "Signal", color=SIGNAL_BLUE
        ).move_to(fwd_signal)

        fwd_arrow1 = Arrow(
            fwd_micro.get_right(), fwd_box.get_left(),
            buff=0.1, color=FORWARD_GREEN, stroke_width=3,
        )
        fwd_arrow2 = Arrow(
            fwd_box.get_right(), fwd_signal.get_left(),
            buff=0.1, color=FORWARD_GREEN, stroke_width=3,
        )

        fwd_group = VGroup(
            fwd_micro, fwd_micro_txt, fwd_arrow1,
            fwd_box, fwd_box_txt, fwd_arrow2,
            fwd_signal, fwd_signal_txt,
        )

        check_labels = ["Deterministic", "No fitting", "Robust"]
        check_marks = VGroup()
        for i, chk in enumerate(check_labels):
            check_sym = MathTex(
                r"\checkmark", font_size=BODY_SIZE, color=FORWARD_GREEN
            ).next_to(fwd_box, DOWN, buff=0.2 + i * 0.35)
            check_txt = label_text(chk, color=FORWARD_GREEN).next_to(
                check_sym, RIGHT, buff=0.15
            )
            check_marks.add(VGroup(check_sym, check_txt))

        self.play(
            FadeIn(fwd_micro), Write(fwd_micro_txt),
            GrowArrow(fwd_arrow1),
            FadeIn(fwd_box), Write(fwd_box_txt),
            GrowArrow(fwd_arrow2),
            FadeIn(fwd_signal), Write(fwd_signal_txt),
            run_time=1.5,
        )
        self.play(
            LaggedStart(
                *[FadeIn(cm, shift=LEFT * 0.2) for cm in check_marks],
                lag_ratio=0.2,
            ),
            run_time=1.0,
        )
        self.wait(1.5)

        # ---- 5. Shoe-fitting analogy ----
        self.play(*[FadeOut(m) for m in self.mobjects])

        title_analogy = section_title("The Shoe-Fitting Analogy", color=MATCH_GOLD)
        self.play(Write(title_analogy))

        # Inverse side: measure foot precisely, compute shoe
        inv_side_label = body_text("Inverse", color=INVERSE_RED).shift(
            LEFT * 3.5 + UP * 1.5
        )

        # Simplified foot shape (rounded polygon)
        foot_shape = Ellipse(
            width=1.0, height=2.0, color=COSINE_ORANGE,
            fill_opacity=0.3, stroke_width=2,
        ).shift(LEFT * 3.5 + DOWN * 0.2)
        foot_label = label_text("Foot", color=COSINE_ORANGE).next_to(
            foot_shape, DOWN, buff=0.2
        )

        # Measuring lines
        measure_h = DoubleArrow(
            foot_shape.get_left() + LEFT * 0.2,
            foot_shape.get_right() + RIGHT * 0.2,
            buff=0, color=INVERSE_RED, stroke_width=2,
        ).next_to(foot_shape, UP, buff=0.15)
        measure_v = DoubleArrow(
            foot_shape.get_top() + UP * 0.1,
            foot_shape.get_bottom() + DOWN * 0.1,
            buff=0, color=INVERSE_RED, stroke_width=2,
        ).next_to(foot_shape, RIGHT, buff=0.2)

        inv_desc = label_text(
            "Measure precisely,\ncompute exact shoe\n(hard, error-prone)",
            color=INVERSE_RED,
        ).next_to(foot_shape, DOWN, buff=0.8)

        self.play(
            Write(inv_side_label),
            Create(foot_shape), Write(foot_label),
            run_time=1.0,
        )
        self.play(GrowArrow(measure_h), GrowArrow(measure_v), run_time=0.8)
        self.play(Write(inv_desc), run_time=0.8)
        self.wait(0.5)

        # Forward side: try many shoes, pick best
        fwd_side_label = body_text("Forward", color=FORWARD_GREEN).shift(
            RIGHT * 3.5 + UP * 1.5
        )

        # Many shoe boxes
        shoe_boxes = VGroup()
        shoe_colors = [SIGNAL_BLUE, EXTRA_COLOR, MATCH_GOLD, FORWARD_GREEN, CSF_COLOR, COSINE_ORANGE]
        for i in range(6):
            shoe = RoundedRectangle(
                width=0.6, height=0.9, corner_radius=0.1,
                color=shoe_colors[i], fill_opacity=0.3, stroke_width=2,
            )
            shoe_boxes.add(shoe)
        shoe_boxes.arrange_in_grid(rows=2, cols=3, buff=0.15)
        shoe_boxes.move_to(RIGHT * 3.5 + DOWN * 0.2)

        shoe_label = label_text("500K shoes", color=MATCH_GOLD).next_to(
            shoe_boxes, DOWN, buff=0.2
        )

        fwd_desc = label_text(
            "Try many shoes,\npick best fit\n(simple, robust)",
            color=FORWARD_GREEN,
        ).next_to(shoe_boxes, DOWN, buff=0.8)

        self.play(
            Write(fwd_side_label),
            LaggedStart(
                *[FadeIn(s, scale=0.5) for s in shoe_boxes],
                lag_ratio=0.1,
            ),
            Write(shoe_label),
            run_time=1.2,
        )
        self.play(Write(fwd_desc), run_time=0.8)

        # Highlight best match
        best_highlight = SurroundingRectangle(
            shoe_boxes[3], color=MATCH_GOLD, buff=0.08, stroke_width=3
        )
        best_text = label_text("Best match!", color=MATCH_GOLD).next_to(
            best_highlight, UP, buff=0.15
        )
        self.play(Create(best_highlight), Write(best_text), run_time=0.8)
        self.wait(1.5)

        # ---- 6. FORCE pipeline ----
        self.play(*[FadeOut(m) for m in self.mobjects])

        title_force = section_title("The FORCE Pipeline", color=FORWARD_GREEN)
        self.play(Write(title_force))

        # Pipeline steps
        step_texts = [
            "Sample 500K tissue\nconfigurations",
            "Simulate signal\nusing biophysics",
            "Compare to\nmeasured signal",
            "Pick best\nmatch",
            "Read off ALL\nproperties",
        ]
        step_colors = [FIBER_GREEN, FORWARD_GREEN, SIGNAL_BLUE, MATCH_GOLD, COSINE_ORANGE]

        step_boxes = VGroup()
        step_labels = VGroup()
        step_nums = VGroup()

        for i, (txt, col) in enumerate(zip(step_texts, step_colors)):
            box = RoundedRectangle(
                width=2.2, height=1.1, corner_radius=0.15,
                color=col, fill_opacity=0.15, stroke_width=2,
            )
            label = label_text(txt, color=col).scale(0.85).move_to(box)
            num = Text(
                str(i + 1), font_size=LABEL_SIZE, color=col, weight=BOLD
            ).next_to(box, UP, buff=0.1)
            step_boxes.add(box)
            step_labels.add(label)
            step_nums.add(num)

        all_steps = VGroup(*[
            VGroup(step_boxes[i], step_labels[i], step_nums[i])
            for i in range(5)
        ])
        # Arrange in two rows: 3 on top, 2 on bottom
        top_row = VGroup(all_steps[0], all_steps[1], all_steps[2])
        bottom_row = VGroup(all_steps[3], all_steps[4])
        top_row.arrange(RIGHT, buff=0.5).shift(UP * 0.5)
        bottom_row.arrange(RIGHT, buff=1.0).shift(DOWN * 1.5)

        # Arrows between steps
        step_arrows = VGroup()
        # top row arrows
        for i in range(2):
            arr = Arrow(
                step_boxes[i].get_right(),
                step_boxes[i + 1].get_left(),
                buff=0.1, color=WHITE, stroke_width=2,
            )
            step_arrows.add(arr)
        # top to bottom
        arr_down = Arrow(
            step_boxes[2].get_bottom(),
            step_boxes[3].get_top(),
            buff=0.1, color=WHITE, stroke_width=2,
        )
        step_arrows.add(arr_down)
        # bottom row arrow
        arr_last = Arrow(
            step_boxes[3].get_right(),
            step_boxes[4].get_left(),
            buff=0.1, color=WHITE, stroke_width=2,
        )
        step_arrows.add(arr_last)

        # Animate step by step
        for i in range(5):
            anims = [FadeIn(step_boxes[i]), Write(step_labels[i]), Write(step_nums[i])]
            if i > 0:
                anims.append(GrowArrow(step_arrows[i - 1]))
            self.play(*anims, run_time=0.8)
            self.wait(0.3)

        # Highlight final step
        final_highlight = SurroundingRectangle(
            all_steps[4], color=MATCH_GOLD, buff=0.15, stroke_width=3,
        )
        note_one_fit = bottom_note("One forward fit yields EVERYTHING")
        self.play(Create(final_highlight), Write(note_one_fit), run_time=1.0)
        self.wait(1.5)

        # ---- 8. Arc diagram: FORCE at center, metrics radiating out ----
        self.play(*[FadeOut(m) for m in self.mobjects])

        force_title = section_title("FORCE: All Metrics at Once", color=FORWARD_GREEN)
        self.play(Write(force_title))

        # Central FORCE circle
        force_circle = Circle(
            radius=0.8, color=FORWARD_GREEN,
            fill_opacity=0.3, stroke_width=3,
        ).shift(DOWN * 0.3)
        force_label = body_text("FORCE", color=FORWARD_GREEN).move_to(force_circle)

        self.play(Create(force_circle), Write(force_label), run_time=1.0)

        # Metric groups radiating outward
        metric_groups = {
            "DTI": ["FA", "MD", "AD", "RD"],
            "DKI": ["MK", "AK", "RK", "KFA"],
            "NODDI": ["NDI", "ODI", "FW"],
            "Fibers": ["Orientations", "Segmentation"],
        }
        group_colors = {
            "DTI": FA_COLOR,
            "DKI": MATCH_GOLD,
            "NODDI": NDI_COLOR,
            "Fibers": EXTRA_COLOR,
        }
        group_angles = {
            "DTI": PI / 2 + PI / 6,
            "DKI": PI / 6,
            "NODDI": -PI / 6 - PI / 6,
            "Fibers": PI + PI / 6,
        }

        all_metric_mobjects = VGroup()
        all_metric_arrows = VGroup()

        for group_name, metrics in metric_groups.items():
            col = group_colors[group_name]
            base_angle = group_angles[group_name]
            n_metrics = len(metrics)
            angle_spread = 0.25  # radians between metrics

            # Group label (farther out)
            group_dist = 3.2
            group_pos = force_circle.get_center() + group_dist * np.array([
                np.cos(base_angle), np.sin(base_angle), 0
            ])
            group_label = body_text(group_name, color=col).scale(0.8).move_to(group_pos)

            # Arrow from FORCE to group label
            arrow_start = force_circle.get_center() + 0.85 * np.array([
                np.cos(base_angle), np.sin(base_angle), 0
            ])
            arrow_end = group_pos - 0.6 * np.array([
                np.cos(base_angle), np.sin(base_angle), 0
            ])
            group_arrow = Arrow(
                arrow_start, arrow_end,
                buff=0, color=col, stroke_width=2,
            )

            # Individual metrics around the group label
            metric_labels = VGroup()
            for j, metric in enumerate(metrics):
                offset_angle = base_angle + (j - (n_metrics - 1) / 2) * angle_spread
                metric_pos = force_circle.get_center() + (group_dist + 0.8) * np.array([
                    np.cos(offset_angle), np.sin(offset_angle), 0
                ])
                m_label = label_text(metric, color=col).move_to(metric_pos)
                metric_labels.add(m_label)

            all_metric_mobjects.add(group_label, metric_labels)
            all_metric_arrows.add(group_arrow)

        # Animate all groups appearing
        self.play(
            LaggedStart(
                *[GrowArrow(a) for a in all_metric_arrows],
                lag_ratio=0.15,
            ),
            run_time=1.5,
        )
        self.play(
            LaggedStart(
                *[Write(m) for m in all_metric_mobjects],
                lag_ratio=0.1,
            ),
            run_time=2.0,
        )
        self.wait(1.5)

        # ---- 9. Bridge to next scene ----
        self.play(*[FadeOut(m) for m in self.mobjects])
        story_bridge(
            self,
            "But how do we build the signal model?",
            color=MATCH_GOLD,
        )
        self.wait(0.5)
