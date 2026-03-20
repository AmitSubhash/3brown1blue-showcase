"""Scenes 7-10 for FORCE paper explainer video.

Scene 7: OneMatchAllMaps - One match yields all microstructure maps
Scene 8: ResolvingShallowCrossings - Fiber crossing resolution at shallow angles
Scene 9: UncertaintyAndAmbiguity - Built-in quality metrics (IQR, FWHM)
Scene 10: FullPipelineAndImpact - Complete pipeline wrap-up and results
"""

from manim import *
from style import *

import numpy as np


# ---------------------------------------------------------------------------
# Scene 7: OneMatchAllMaps
# ---------------------------------------------------------------------------
class OneMatchAllMaps(Scene):
    """From a single dictionary match, extract every microstructure metric."""

    def construct(self) -> None:
        # -- Title --
        title = section_title("One Match, All Maps", color=MATCH_GOLD)
        self.play(Write(title))
        self.wait(0.5)

        # -- Winning match signal bar --
        signal_bar = Rectangle(
            width=4, height=0.6,
            fill_color=MATCH_GOLD, fill_opacity=0.85,
            stroke_color=WHITE, stroke_width=2,
        ).shift(UP * 1.8)
        signal_label = label_text("Best-match dictionary entry").next_to(
            signal_bar, UP, buff=0.2
        )
        glow = SurroundingRectangle(
            signal_bar, color=MATCH_GOLD, buff=0.12, stroke_width=3
        )
        self.play(FadeIn(signal_bar), Write(signal_label), Create(glow))
        self.wait(0.5)

        # -- Build metric cards --
        def _make_card(
            name: str, color: str, width: float = 1.1, height: float = 0.55
        ) -> VGroup:
            rect = RoundedRectangle(
                width=width, height=height, corner_radius=0.08,
                fill_color=color, fill_opacity=0.25,
                stroke_color=color, stroke_width=2,
            )
            txt = Text(name, font_size=LABEL_SIZE, color=color)
            txt.move_to(rect.get_center())
            return VGroup(rect, txt)

        # Group 1: DTI
        dti_cards = VGroup(
            _make_card("FA", FA_COLOR),
            _make_card("MD", MD_COLOR),
            _make_card("AD", "#8E44AD"),
            _make_card("RD", "#16A085"),
        ).arrange(RIGHT, buff=0.15)
        dti_label = Text(
            "DTI", font_size=LABEL_SIZE, color=GRAY_B, weight=BOLD
        ).next_to(dti_cards, LEFT, buff=0.3)
        dti_group = VGroup(dti_label, dti_cards)

        # Group 2: DKI
        dki_cards = VGroup(
            _make_card("MK", "#E67E22"),
            _make_card("AK", "#D35400"),
            _make_card("RK", "#C0392B"),
            _make_card("KFA", "#E74C3C"),
        ).arrange(RIGHT, buff=0.15)
        dki_label = Text(
            "DKI", font_size=LABEL_SIZE, color=GRAY_B, weight=BOLD
        ).next_to(dki_cards, LEFT, buff=0.3)
        dki_group = VGroup(dki_label, dki_cards)

        # Group 3: NODDI
        noddi_cards = VGroup(
            _make_card("NDI", NDI_COLOR),
            _make_card("ODI", ODI_COLOR),
            _make_card("FW", FW_MAP_COLOR),
        ).arrange(RIGHT, buff=0.15)
        noddi_label = Text(
            "NODDI", font_size=LABEL_SIZE, color=GRAY_B, weight=BOLD
        ).next_to(noddi_cards, LEFT, buff=0.3)
        noddi_group = VGroup(noddi_label, noddi_cards)

        # Group 4: Bonus (orientations + tissue fractions)
        orient_arrow_group = VGroup(
            Arrow(ORIGIN, RIGHT * 0.6, color=YELLOW, stroke_width=3),
            Arrow(ORIGIN, UP * 0.5 + RIGHT * 0.3, color=YELLOW, stroke_width=3),
        ).arrange(RIGHT, buff=0.1)
        orient_card_rect = RoundedRectangle(
            width=1.1, height=0.55, corner_radius=0.08,
            fill_color=YELLOW, fill_opacity=0.15,
            stroke_color=YELLOW, stroke_width=2,
        )
        orient_arrow_group.move_to(orient_card_rect.get_center()).scale(0.7)
        orient_card = VGroup(orient_card_rect, orient_arrow_group)
        orient_lbl = Text(
            "Orientations", font_size=18, color=YELLOW
        ).next_to(orient_card, DOWN, buff=0.08)

        # Pie chart for tissue segmentation
        pie_colors = [WM_COLOR, GM_COLOR, CSF_COLOR]
        pie_angles = [0.5 * TAU, 0.35 * TAU, 0.15 * TAU]
        pie_sectors = VGroup()
        cumulative = 0.0
        for angle, color in zip(pie_angles, pie_colors):
            sector = AnnularSector(
                inner_radius=0, outer_radius=0.25,
                angle=angle, start_angle=cumulative,
                fill_color=color, fill_opacity=0.7,
                stroke_color=WHITE, stroke_width=1,
            )
            pie_sectors.add(sector)
            cumulative += angle
        pie_card_rect = RoundedRectangle(
            width=1.1, height=0.55, corner_radius=0.08,
            fill_color=GRAY, fill_opacity=0.1,
            stroke_color=GRAY_B, stroke_width=2,
        )
        pie_sectors.move_to(pie_card_rect.get_center())
        pie_card = VGroup(pie_card_rect, pie_sectors)
        pie_lbl = Text(
            "WM/GM/CSF", font_size=18, color=GRAY_B
        ).next_to(pie_card, DOWN, buff=0.08)

        bonus_cards = VGroup(
            VGroup(orient_card, orient_lbl),
            VGroup(pie_card, pie_lbl),
        ).arrange(RIGHT, buff=0.25)
        bonus_label = Text(
            "Bonus", font_size=LABEL_SIZE, color=GRAY_B, weight=BOLD
        ).next_to(bonus_cards, LEFT, buff=0.3)
        bonus_group = VGroup(bonus_label, bonus_cards)

        # Arrange all groups vertically
        all_groups = VGroup(
            dti_group, dki_group, noddi_group, bonus_group
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        all_groups.next_to(signal_bar, DOWN, buff=0.5)

        # Align left edges of labels
        for grp in [dti_group, dki_group, noddi_group, bonus_group]:
            grp[0].align_to(dti_group[0], LEFT)

        # -- Cascade reveal with connecting arrows --
        for i, grp in enumerate([dti_group, dki_group, noddi_group, bonus_group]):
            grp_label = grp[0]
            grp_cards = grp[1:]
            connector = Arrow(
                signal_bar.get_bottom(),
                grp_label.get_top() + UP * 0.1,
                color=MATCH_GOLD, stroke_width=2,
                buff=0.05, max_tip_length_to_length_ratio=0.15,
            )
            if i == 0:
                self.play(
                    GrowArrow(connector),
                    LaggedStart(
                        *[FadeIn(c, shift=UP * 0.2) for c in grp],
                        lag_ratio=0.15,
                    ),
                    run_time=1.2,
                )
            else:
                self.play(
                    GrowArrow(connector),
                    LaggedStart(
                        *[FadeIn(c, shift=UP * 0.2) for c in grp],
                        lag_ratio=0.15,
                    ),
                    run_time=0.9,
                )
            self.wait(0.3)

        self.wait(0.5)

        # -- Contrast: Traditional vs FORCE --
        # Fade out the extraction view
        self.play(
            FadeOut(title), FadeOut(signal_bar), FadeOut(signal_label),
            FadeOut(glow), FadeOut(all_groups),
            *[FadeOut(m) for m in self.mobjects if m not in [title]],
            run_time=0.8,
        )

        compare_title = section_title("Traditional vs FORCE", color=WHITE)
        self.play(Write(compare_title))

        # Left side: Traditional - 4 separate pipelines
        trad_label = Text(
            "Traditional", font_size=BODY_SIZE, color=INVERSE_RED
        ).shift(LEFT * 3.5 + UP * 1.8)

        pipeline_names = ["DTI\nPipeline", "CSD\nPipeline", "NODDI\nPipeline", "DKI\nPipeline"]
        pipeline_colors = [FA_COLOR, FIBER_GREEN, NDI_COLOR, COSINE_ORANGE]
        trad_boxes = VGroup()
        for name, color in zip(pipeline_names, pipeline_colors):
            box = VGroup(
                RoundedRectangle(
                    width=1.5, height=0.9, corner_radius=0.1,
                    fill_color=color, fill_opacity=0.2,
                    stroke_color=color, stroke_width=2,
                ),
                Text(name, font_size=18, color=color),
            )
            box[1].move_to(box[0].get_center())
            trad_boxes.add(box)
        trad_boxes.arrange_in_grid(2, 2, buff=0.2)
        trad_boxes.next_to(trad_label, DOWN, buff=0.4)

        # Right side: FORCE - ONE box
        force_label = Text(
            "FORCE", font_size=BODY_SIZE, color=MATCH_GOLD
        ).shift(RIGHT * 3.5 + UP * 1.8)

        force_box = VGroup(
            RoundedRectangle(
                width=2.5, height=1.8, corner_radius=0.15,
                fill_color=MATCH_GOLD, fill_opacity=0.15,
                stroke_color=MATCH_GOLD, stroke_width=3,
            ),
            Text("FORCE", font_size=HEADING_SIZE, color=MATCH_GOLD, weight=BOLD),
        )
        force_box[1].move_to(force_box[0].get_center())
        force_box.next_to(force_label, DOWN, buff=0.4)

        # Outputs from FORCE
        output_names = ["DTI", "DKI", "NODDI", "Orientations"]
        force_outputs = VGroup()
        for name in output_names:
            out = Text(name, font_size=18, color=WHITE)
            force_outputs.add(out)
        force_outputs.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        force_outputs.next_to(force_box, RIGHT, buff=0.3)

        # Divider
        divider = DashedLine(
            UP * 2.2, DOWN * 2.2, color=GRAY, dash_length=0.15
        ).move_to(ORIGIN)

        self.play(
            Write(trad_label),
            LaggedStart(
                *[FadeIn(b, shift=DOWN * 0.2) for b in trad_boxes],
                lag_ratio=0.15,
            ),
            Create(divider),
            run_time=1.2,
        )
        self.play(
            Write(force_label),
            FadeIn(force_box, shift=DOWN * 0.2),
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                *[FadeIn(o, shift=LEFT * 0.3) for o in force_outputs],
                lag_ratio=0.12,
            ),
            run_time=0.8,
        )
        self.wait(0.5)

        # Bottom note
        note = bottom_note("One forward fit replaces four separate pipelines")
        self.play(Write(note))
        self.wait(2)


# ---------------------------------------------------------------------------
# Scene 8: ResolvingShallowCrossings
# ---------------------------------------------------------------------------
class ResolvingShallowCrossings(Scene):
    """Show FORCE resolving fiber crossings at very shallow angles."""

    def construct(self) -> None:
        # -- Title --
        title = section_title("Resolving Fiber Crossings", color=SIGNAL_BLUE)
        self.play(Write(title))
        self.wait(0.5)

        # -- Voxel with crossing fibers --
        angle_tracker = ValueTracker(90)

        voxel_rect = Square(
            side_length=2.8, color=GRAY_B, stroke_width=1.5
        ).shift(LEFT * 3.5 + DOWN * 0.3)
        voxel_label = label_text("Voxel").next_to(voxel_rect, UP, buff=0.15)

        # Fiber bundles as lines crossing at a tracked angle
        fiber_length = 1.2
        voxel_center = voxel_rect.get_center()

        def make_fiber_pair() -> VGroup:
            angle_deg = angle_tracker.get_value()
            half_angle = angle_deg / 2
            rad1 = np.radians(half_angle)
            rad2 = np.radians(-half_angle)
            fiber1 = Line(
                voxel_center + LEFT * fiber_length * np.cos(rad1)
                + DOWN * fiber_length * np.sin(rad1),
                voxel_center + RIGHT * fiber_length * np.cos(rad1)
                + UP * fiber_length * np.sin(rad1),
                color=FIBER_GREEN, stroke_width=5,
            )
            fiber2 = Line(
                voxel_center + LEFT * fiber_length * np.cos(rad2)
                + DOWN * fiber_length * np.sin(rad2),
                voxel_center + RIGHT * fiber_length * np.cos(rad2)
                + UP * fiber_length * np.sin(rad2),
                color=SIGNAL_BLUE, stroke_width=5,
            )
            return VGroup(fiber1, fiber2)

        fibers = always_redraw(make_fiber_pair)

        # Angle label
        angle_display = always_redraw(
            lambda: Text(
                f"{angle_tracker.get_value():.0f}\u00b0",
                font_size=BODY_SIZE, color=MATCH_GOLD,
            ).next_to(voxel_rect, DOWN, buff=0.25)
        )

        self.play(
            Create(voxel_rect), Write(voxel_label),
            run_time=0.6,
        )
        self.add(fibers, angle_display)
        self.play(FadeIn(fibers), FadeIn(angle_display))
        self.wait(0.5)

        # -- ODF and FORCE side-by-side indicators --
        odf_title = Text(
            "ODF Methods", font_size=LABEL_SIZE, color=COSINE_ORANGE
        ).move_to(RIGHT * 1.5 + UP * 1.8)
        force_ind_title = Text(
            "FORCE", font_size=LABEL_SIZE, color=MATCH_GOLD
        ).move_to(RIGHT * 4.5 + UP * 1.8)

        # Status indicators (always_redraw based on angle)
        def odf_status() -> VGroup:
            angle = angle_tracker.get_value()
            if angle >= 50:
                icon = Text(
                    "\u2713 2 peaks", font_size=LABEL_SIZE, color=GREEN
                )
            elif angle >= 30:
                icon = Text(
                    "\u2248 merging", font_size=LABEL_SIZE, color=YELLOW
                )
            else:
                icon = Text(
                    "\u2717 1 peak", font_size=LABEL_SIZE, color=RED
                )
            icon.move_to(RIGHT * 1.5 + UP * 1.0)
            return icon

        def force_status() -> VGroup:
            angle = angle_tracker.get_value()
            if angle >= 10:
                icon = Text(
                    "\u2713 2 fibers", font_size=LABEL_SIZE, color=GREEN
                )
            else:
                icon = Text(
                    "\u2713 2 fibers", font_size=LABEL_SIZE, color=GREEN
                )
            icon.move_to(RIGHT * 4.5 + UP * 1.0)
            return icon

        odf_indicator = always_redraw(odf_status)
        force_indicator = always_redraw(force_status)

        # Stylized ODF lobes (two overlapping ellipses)
        def make_odf_visual() -> VGroup:
            angle_deg = angle_tracker.get_value()
            half = angle_deg / 2
            center = RIGHT * 1.5 + DOWN * 0.3

            lobe_scale = 0.7
            lobe1 = Ellipse(
                width=1.2 * lobe_scale, height=0.3 * lobe_scale,
                fill_color=COSINE_ORANGE, fill_opacity=0.3,
                stroke_color=COSINE_ORANGE, stroke_width=2,
            ).rotate(np.radians(half)).move_to(center)
            lobe2 = Ellipse(
                width=1.2 * lobe_scale, height=0.3 * lobe_scale,
                fill_color=COSINE_ORANGE, fill_opacity=0.3,
                stroke_color=COSINE_ORANGE, stroke_width=2,
            ).rotate(np.radians(-half)).move_to(center)

            # Merge visualization: if angle < 30, show merged ellipse
            if angle_deg < 30:
                merged = Ellipse(
                    width=1.3 * lobe_scale, height=0.5 * lobe_scale,
                    fill_color=RED, fill_opacity=0.35,
                    stroke_color=RED, stroke_width=2,
                ).move_to(center)
                return VGroup(merged)
            return VGroup(lobe1, lobe2)

        odf_visual = always_redraw(make_odf_visual)

        # FORCE match indicator (two distinct arrows)
        def make_force_visual() -> VGroup:
            angle_deg = angle_tracker.get_value()
            half = angle_deg / 2
            center = RIGHT * 4.5 + DOWN * 0.3
            rad1 = np.radians(half)
            rad2 = np.radians(-half)
            arr_len = 0.6
            arrow1 = Arrow(
                center, center + RIGHT * arr_len * np.cos(rad1)
                + UP * arr_len * np.sin(rad1),
                color=FIBER_GREEN, stroke_width=4, buff=0,
                max_tip_length_to_length_ratio=0.3,
            )
            arrow2 = Arrow(
                center, center + RIGHT * arr_len * np.cos(rad2)
                + UP * arr_len * np.sin(rad2),
                color=SIGNAL_BLUE, stroke_width=4, buff=0,
                max_tip_length_to_length_ratio=0.3,
            )
            return VGroup(arrow1, arrow2)

        force_visual = always_redraw(make_force_visual)

        self.play(
            Write(odf_title), Write(force_ind_title),
            run_time=0.6,
        )
        self.add(odf_indicator, force_indicator, odf_visual, force_visual)
        self.play(
            FadeIn(odf_indicator), FadeIn(force_indicator),
            FadeIn(odf_visual), FadeIn(force_visual),
        )
        self.wait(0.5)

        # -- Angle sweep: 90 -> 60 -> 40 -> 20 -> 10 --
        note1 = bottom_note("90\u00b0: Both methods find two fibers")
        self.play(Write(note1))
        self.wait(1)

        self.play(FadeOut(note1))
        note2 = bottom_note("Reducing crossing angle...")
        self.play(Write(note2))
        self.play(
            angle_tracker.animate.set_value(60), run_time=1.5, rate_func=smooth
        )
        self.wait(0.5, frozen_frame=False)

        self.play(
            angle_tracker.animate.set_value(40), run_time=1.2, rate_func=smooth
        )
        self.wait(0.5, frozen_frame=False)

        self.play(FadeOut(note2))
        note3 = bottom_note("Below 30\u00b0: ODF peaks merge into one!")
        self.play(Write(note3))
        self.play(
            angle_tracker.animate.set_value(20), run_time=1.5, rate_func=smooth
        )
        self.wait(1, frozen_frame=False)

        self.play(
            angle_tracker.animate.set_value(10), run_time=1.2, rate_func=smooth
        )
        self.wait(1, frozen_frame=False)
        self.play(FadeOut(note3))

        # -- Performance comparison bar chart --
        # Clear previous
        self.play(
            FadeOut(voxel_rect), FadeOut(voxel_label), FadeOut(angle_display),
            FadeOut(odf_title), FadeOut(force_ind_title),
            FadeOut(odf_indicator), FadeOut(force_indicator),
            FadeOut(odf_visual), FadeOut(force_visual),
            FadeOut(title),
            run_time=0.6,
        )
        self.remove(fibers, angle_display, odf_indicator, force_indicator,
                     odf_visual, force_visual)

        chart_title = section_title("Peak Detection Rate", color=WHITE)
        self.play(Write(chart_title))

        # Axes for the comparison
        axes = Axes(
            x_range=[0, 90, 10],
            y_range=[0, 100, 20],
            x_length=8,
            y_length=4,
            axis_config={"include_numbers": True, "font_size": 18},
            tips=False,
        ).shift(DOWN * 0.3)

        x_label = Text(
            "Crossing Angle (\u00b0)", font_size=LABEL_SIZE
        ).next_to(axes, DOWN, buff=0.35)
        y_label = Text(
            "Detection (%)", font_size=LABEL_SIZE
        ).rotate(PI / 2).next_to(axes, LEFT, buff=0.35)

        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1)

        # Data points (stylized from Fig. 3)
        # angle_centers: midpoints of buckets
        angle_centers = [15, 25, 35, 45, 55, 65, 75, 85]

        # Detection rates (approximate)
        force_rates = [80, 88, 92, 95, 97, 98, 99, 99]
        csd_rates = [25, 45, 65, 78, 88, 93, 95, 97]
        csa_rates = [20, 35, 55, 70, 82, 90, 94, 96]
        gqi_rates = [15, 30, 50, 65, 78, 87, 92, 95]

        def plot_line(rates, color, label_str):
            points = [axes.c2p(a, r) for a, r in zip(angle_centers, rates)]
            line = VMobject(color=color, stroke_width=3)
            line.set_points_smoothly(points)

            dots = VGroup(*[
                Dot(p, color=color, radius=0.05) for p in points
            ])
            lbl = Text(
                label_str, font_size=18, color=color
            ).next_to(points[-1], RIGHT, buff=0.15)
            return line, dots, lbl

        force_line, force_dots, force_lbl = plot_line(
            force_rates, MATCH_GOLD, "FORCE"
        )
        csd_line, csd_dots, csd_lbl = plot_line(csd_rates, "#E67E22", "CSD")
        csa_line, csa_dots, csa_lbl = plot_line(csa_rates, "#3498DB", "CSA")
        gqi_line, gqi_dots, gqi_lbl = plot_line(gqi_rates, "#95A5A6", "GQI")

        # Animate lines
        for line, dots, lbl in [
            (csa_line, csa_dots, csa_lbl),
            (gqi_line, gqi_dots, gqi_lbl),
            (csd_line, csd_dots, csd_lbl),
        ]:
            self.play(Create(line), FadeIn(dots), Write(lbl), run_time=0.7)

        # FORCE line last with emphasis
        self.play(
            Create(force_line), FadeIn(force_dots), Write(force_lbl),
            run_time=1,
        )
        self.play(Indicate(force_lbl, color=MATCH_GOLD))
        self.wait(0.5)

        # Highlight the low-angle region
        low_angle_rect = Rectangle(
            width=axes.c2p(20, 0)[0] - axes.c2p(0, 0)[0],
            height=axes.c2p(0, 100)[1] - axes.c2p(0, 0)[1],
            fill_color=RED, fill_opacity=0.1,
            stroke_color=RED, stroke_width=1.5,
        ).move_to(
            axes.c2p(10, 50)
        )
        low_label = Text(
            "Shallow crossings", font_size=18, color=RED
        ).next_to(low_angle_rect, UP, buff=0.1)

        self.play(FadeIn(low_angle_rect), Write(low_label), run_time=0.8)
        self.wait(0.5)

        # Why explanation
        note_why = bottom_note(
            "FORCE matches pre-simulated two-fiber configs directly"
        )
        self.play(Write(note_why))
        self.wait(1.5)

        self.play(FadeOut(note_why))
        note_final = bottom_note(
            "FORCE resolves crossings where ODF methods fail"
        )
        self.play(Write(note_final))
        self.wait(2)


# ---------------------------------------------------------------------------
# Scene 9: UncertaintyAndAmbiguity
# ---------------------------------------------------------------------------
class UncertaintyAndAmbiguity(Scene):
    """Built-in quality metrics: uncertainty (IQR) and ambiguity (FWHM)."""

    def construct(self) -> None:
        # -- Title --
        title = section_title("Built-in Confidence", color=FORWARD_GREEN)
        self.play(Write(title))
        self.wait(0.3)

        concept = body_text(
            "FORCE tells you HOW CONFIDENT it is"
        ).next_to(title, DOWN, buff=0.4)
        self.play(Write(concept))
        self.wait(0.8)
        self.play(FadeOut(concept))

        # ===================== UNCERTAINTY (IQR) =====================
        unc_title = Text(
            "Uncertainty (IQR)", font_size=BODY_SIZE, color=SIGNAL_BLUE
        ).move_to(UP * 2.3 + LEFT * 3)

        # Histogram: top-50 scores for a GOOD voxel - tightly clustered
        np.random.seed(42)
        good_scores = np.clip(
            np.random.normal(loc=0.92, scale=0.02, size=50), 0.8, 1.0
        )
        good_scores.sort()

        hist_axes = Axes(
            x_range=[0.75, 1.0, 0.05],
            y_range=[0, 20, 5],
            x_length=4.5,
            y_length=2.5,
            axis_config={"include_numbers": True, "font_size": 16},
            tips=False,
        ).move_to(LEFT * 3 + DOWN * 0.3)

        hist_x_label = Text(
            "Similarity Score", font_size=18
        ).next_to(hist_axes, DOWN, buff=0.25)

        # Build histogram bars
        bins = np.linspace(0.75, 1.0, 11)
        counts, _ = np.histogram(good_scores, bins=bins)
        bar_width_scene = (
            hist_axes.c2p(bins[1], 0)[0] - hist_axes.c2p(bins[0], 0)[0]
        )

        hist_bars = VGroup()
        for i, count in enumerate(counts):
            if count == 0:
                continue
            bar = Rectangle(
                width=bar_width_scene * 0.85,
                height=(
                    hist_axes.c2p(0, count)[1] - hist_axes.c2p(0, 0)[1]
                ),
                fill_color=SIGNAL_BLUE, fill_opacity=0.6,
                stroke_color=SIGNAL_BLUE, stroke_width=1,
            )
            bar_center_x = (bins[i] + bins[i + 1]) / 2
            bar.move_to(
                hist_axes.c2p(bar_center_x, count / 2)
            )
            hist_bars.add(bar)

        self.play(Write(unc_title), run_time=0.5)
        self.play(Create(hist_axes), Write(hist_x_label), run_time=0.7)
        self.play(
            LaggedStart(
                *[FadeIn(b, shift=UP * 0.1) for b in hist_bars],
                lag_ratio=0.08,
            ),
            run_time=1,
        )

        # IQR annotation
        p25 = np.percentile(good_scores, 25)
        p75 = np.percentile(good_scores, 75)
        iqr_brace = BraceBetweenPoints(
            hist_axes.c2p(p25, -1),
            hist_axes.c2p(p75, -1),
            direction=DOWN,
            color=MATCH_GOLD,
        )
        iqr_label = Text(
            f"IQR = {p75 - p25:.3f}", font_size=18, color=MATCH_GOLD
        )
        iqr_label.next_to(iqr_brace, DOWN, buff=0.1)
        tight_label = Text(
            "Tight = HIGH confidence", font_size=18, color=GREEN
        ).next_to(iqr_label, DOWN, buff=0.15)

        self.play(Create(iqr_brace), Write(iqr_label), run_time=0.7)
        self.play(Write(tight_label), run_time=0.5)
        self.wait(0.5)

        # Formula
        unc_formula = MathTex(
            r"U(v) = P_{75} - P_{25}",
            font_size=EQ_SIZE, color=SIGNAL_BLUE,
        ).move_to(RIGHT * 3 + UP * 0.5)
        small_iqr_note = Text(
            "Small IQR = high confidence", font_size=18, color=GREEN
        ).next_to(unc_formula, DOWN, buff=0.3)

        self.play(Write(unc_formula), run_time=0.8)
        self.play(Write(small_iqr_note), run_time=0.5)
        self.wait(1)

        # ===================== AMBIGUITY (FWHM) =====================
        # Fade uncertainty visuals
        unc_objects = VGroup(
            unc_title, hist_axes, hist_x_label, hist_bars,
            iqr_brace, iqr_label, tight_label,
            unc_formula, small_iqr_note,
        )
        self.play(FadeOut(unc_objects), run_time=0.6)

        amb_title = Text(
            "Ambiguity (FWHM)", font_size=BODY_SIZE, color=COSINE_ORANGE
        ).move_to(UP * 2.3 + LEFT * 3)

        # Histogram: scores for a PROBLEMATIC voxel - many near max
        np.random.seed(7)
        bad_scores = np.clip(
            np.concatenate([
                np.random.normal(loc=0.88, scale=0.04, size=30),
                np.random.normal(loc=0.82, scale=0.03, size=20),
            ]),
            0.7, 1.0,
        )
        bad_scores.sort()

        hist_axes2 = Axes(
            x_range=[0.7, 1.0, 0.05],
            y_range=[0, 15, 5],
            x_length=4.5,
            y_length=2.5,
            axis_config={"include_numbers": True, "font_size": 16},
            tips=False,
        ).move_to(LEFT * 3 + DOWN * 0.3)

        hist_x_label2 = Text(
            "Similarity Score", font_size=18
        ).next_to(hist_axes2, DOWN, buff=0.25)

        bins2 = np.linspace(0.7, 1.0, 13)
        counts2, _ = np.histogram(bad_scores, bins=bins2)
        bar_width2 = (
            hist_axes2.c2p(bins2[1], 0)[0] - hist_axes2.c2p(bins2[0], 0)[0]
        )

        hist_bars2 = VGroup()
        max_score = bad_scores.max()
        half_max = 0.5 * max_score
        for i, count in enumerate(counts2):
            if count == 0:
                continue
            bin_mid = (bins2[i] + bins2[i + 1]) / 2
            above_half = bin_mid > half_max
            bar_color = COSINE_ORANGE if above_half else GRAY_B
            bar = Rectangle(
                width=bar_width2 * 0.85,
                height=(
                    hist_axes2.c2p(0, count)[1] - hist_axes2.c2p(0, 0)[1]
                ),
                fill_color=bar_color, fill_opacity=0.6,
                stroke_color=bar_color, stroke_width=1,
            )
            bar.move_to(hist_axes2.c2p(bin_mid, count / 2))
            hist_bars2.add(bar)

        self.play(Write(amb_title), run_time=0.5)
        self.play(Create(hist_axes2), Write(hist_x_label2), run_time=0.7)
        self.play(
            LaggedStart(
                *[FadeIn(b, shift=UP * 0.1) for b in hist_bars2],
                lag_ratio=0.08,
            ),
            run_time=1,
        )

        # FWHM line
        fwhm_line = DashedLine(
            hist_axes2.c2p(half_max, 0),
            hist_axes2.c2p(half_max, 15),
            color=YELLOW, dash_length=0.1,
        )
        fwhm_label = Text(
            f"0.5 \u00d7 max = {half_max:.2f}", font_size=16, color=YELLOW
        ).next_to(fwhm_line, RIGHT, buff=0.15)

        spread_label = Text(
            "Many near-matches = HIGH ambiguity",
            font_size=18, color=COSINE_ORANGE,
        ).next_to(hist_bars2, DOWN, buff=0.8)

        self.play(Create(fwhm_line), Write(fwhm_label), run_time=0.6)
        self.play(Write(spread_label), run_time=0.5)

        # Formula
        amb_formula = MathTex(
            r"A(v) = \frac{|\{s > 0.5 \cdot s_{\max}\}|}{N}",
            font_size=EQ_SIZE, color=COSINE_ORANGE,
        ).move_to(RIGHT * 3 + UP * 0.5)
        amb_note = Text(
            "Multiple configs could produce this signal",
            font_size=18, color=COSINE_ORANGE,
        ).next_to(amb_formula, DOWN, buff=0.3)

        self.play(Write(amb_formula), run_time=0.8)
        self.play(Write(amb_note), run_time=0.5)
        self.wait(1)

        # ===================== Brain map examples =====================
        amb_objects = VGroup(
            amb_title, hist_axes2, hist_x_label2, hist_bars2,
            fwhm_line, fwhm_label, spread_label,
            amb_formula, amb_note,
        )
        self.play(FadeOut(amb_objects), run_time=0.6)

        brain_title = Text(
            "Where do we see each?", font_size=BODY_SIZE, color=WHITE
        ).move_to(UP * 2.3)
        self.play(Write(brain_title))

        # Simple brain outline (ellipse)
        brain_outline = Ellipse(
            width=4, height=3,
            stroke_color=WHITE, stroke_width=2,
            fill_opacity=0,
        ).shift(DOWN * 0.5)

        # Corpus callosum (inner ellipse, coherent WM)
        cc_region = Ellipse(
            width=2.2, height=0.5,
            fill_color=GREEN, fill_opacity=0.35,
            stroke_color=GREEN, stroke_width=1.5,
        ).move_to(brain_outline.get_center() + UP * 0.2)
        cc_label = Text(
            "Corpus Callosum", font_size=16, color=GREEN
        ).next_to(cc_region, UP, buff=0.1)
        cc_note = Text(
            "LOW ambiguity\n(unique answer)", font_size=16, color=GREEN
        ).next_to(cc_label, RIGHT, buff=0.4)

        # GM/WM boundary
        boundary = Arc(
            radius=1.4, start_angle=PI * 0.3, angle=PI * 0.4,
            stroke_color=COSINE_ORANGE, stroke_width=4,
        ).move_to(brain_outline.get_center() + DOWN * 0.3 + LEFT * 0.3)
        boundary_label = Text(
            "GM/WM Boundary", font_size=16, color=COSINE_ORANGE
        ).next_to(boundary, DOWN, buff=0.15)
        boundary_note = Text(
            "HIGH uncertainty\n(partial volume)", font_size=16, color=COSINE_ORANGE
        ).next_to(boundary_label, RIGHT, buff=0.3)

        self.play(Create(brain_outline), run_time=0.6)
        self.play(
            FadeIn(cc_region), Write(cc_label), Write(cc_note),
            run_time=0.8,
        )
        self.play(
            Create(boundary), Write(boundary_label), Write(boundary_note),
            run_time=0.8,
        )
        self.wait(1)

        # Bottom note
        note = bottom_note(
            "Quality control is free -- no extra computation needed"
        )
        self.play(Write(note))
        self.wait(2)


# ---------------------------------------------------------------------------
# Scene 10: FullPipelineAndImpact
# ---------------------------------------------------------------------------
class FullPipelineAndImpact(Scene):
    """Complete pipeline, results summary, and conclusion."""

    def construct(self) -> None:
        # -- Title --
        title = section_title("The FORCE Framework", color=MATCH_GOLD)
        self.play(Write(title))
        self.wait(0.5)

        # ===================== Full Pipeline Flowchart =====================
        # Steps: Brain Scan -> Diffusion Signal -> Dictionary Matching -> Maps
        step_data = [
            ("Brain\nScan", SIGNAL_BLUE),
            ("Diffusion\nSignal", INTRA_COLOR),
            ("Dictionary\nMatching", MATCH_GOLD),
            ("Microstructure\nMaps", FORWARD_GREEN),
        ]
        step_boxes = VGroup()
        for label_str, color in step_data:
            box_rect = RoundedRectangle(
                width=2.0, height=1.0, corner_radius=0.1,
                fill_color=color, fill_opacity=0.2,
                stroke_color=color, stroke_width=2,
            )
            box_txt = Text(
                label_str, font_size=18, color=color
            ).move_to(box_rect.get_center())
            step_boxes.add(VGroup(box_rect, box_txt))
        step_boxes.arrange(RIGHT, buff=0.8)
        step_boxes.shift(UP * 1.2)

        # Arrows between steps
        step_arrows = VGroup()
        for i in range(len(step_boxes) - 1):
            arr = Arrow(
                step_boxes[i].get_right(),
                step_boxes[i + 1].get_left(),
                color=WHITE, buff=0.1, stroke_width=2,
                max_tip_length_to_length_ratio=0.2,
            )
            step_arrows.add(arr)

        # Animate left to right
        for i, box in enumerate(step_boxes):
            anims = [FadeIn(box, shift=RIGHT * 0.3)]
            if i > 0:
                anims.append(GrowArrow(step_arrows[i - 1]))
            self.play(*anims, run_time=0.6)
        self.wait(0.5)

        # ===================== Results Summary =====================
        self.play(FadeOut(title))
        results_title = section_title("Key Results", color=WHITE)
        self.play(
            step_boxes.animate.scale(0.65).move_to(UP * 3),
            step_arrows.animate.scale(0.65).move_to(UP * 3),
            Write(results_title),
            run_time=0.8,
        )

        checkmark = "\u2713"
        result_items = [
            f"{checkmark}  Resolves crossings at 10-20\u00b0",
            f"{checkmark}  Single-shell AND multi-shell",
            f"{checkmark}  Human AND mouse brain",
            f"{checkmark}  In vivo AND ex vivo",
            f"{checkmark}  Clinical: glioma, Parkinson's",
            f"{checkmark}  Parallelizable across voxels",
        ]
        result_texts = VGroup()
        for item in result_items:
            t = Text(item, font_size=LABEL_SIZE, color=WHITE)
            result_texts.add(t)
        result_texts.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        result_texts.move_to(DOWN * 0.5 + LEFT * 0.5)

        # Color the checkmarks green
        for t in result_texts:
            t[0].set_color(FORWARD_GREEN)

        self.play(
            LaggedStart(
                *[FadeIn(r, shift=LEFT * 0.3) for r in result_texts],
                lag_ratio=0.12,
            ),
            run_time=1.5,
        )
        self.wait(1)

        # ===================== Unification Animation =====================
        # Clear results
        self.play(
            FadeOut(result_texts), FadeOut(results_title),
            FadeOut(step_boxes), FadeOut(step_arrows),
            run_time=0.6,
        )

        unify_title = section_title("Unification", color=MATCH_GOLD)
        self.play(Write(unify_title))

        # Before: 4 separate boxes
        before_label = Text(
            "Before", font_size=BODY_SIZE, color=GRAY_B
        ).move_to(UP * 1.8)
        self.play(Write(before_label))

        pipeline_names = ["DTI", "CSD", "NODDI", "DKI"]
        pipeline_colors = [FA_COLOR, FIBER_GREEN, NDI_COLOR, COSINE_ORANGE]
        before_boxes = VGroup()
        for name, color in zip(pipeline_names, pipeline_colors):
            box = VGroup(
                RoundedRectangle(
                    width=1.6, height=0.9, corner_radius=0.1,
                    fill_color=color, fill_opacity=0.25,
                    stroke_color=color, stroke_width=2,
                ),
                Text(name, font_size=BODY_SIZE, color=color),
            )
            box[1].move_to(box[0].get_center())
            before_boxes.add(box)
        before_boxes.arrange(RIGHT, buff=0.3)
        before_boxes.next_to(before_label, DOWN, buff=0.4)

        self.play(
            LaggedStart(
                *[FadeIn(b, shift=DOWN * 0.2) for b in before_boxes],
                lag_ratio=0.1,
            ),
            run_time=0.8,
        )
        self.wait(0.5)

        # After: FORCE (1 box) - merge animation
        after_box = VGroup(
            RoundedRectangle(
                width=3.0, height=1.2, corner_radius=0.15,
                fill_color=MATCH_GOLD, fill_opacity=0.2,
                stroke_color=MATCH_GOLD, stroke_width=3,
            ),
            Text("FORCE", font_size=HEADING_SIZE, color=MATCH_GOLD, weight=BOLD),
        )
        after_box[1].move_to(after_box[0].get_center())
        after_box.move_to(before_boxes.get_center())

        self.play(FadeOut(before_label))
        after_label = Text(
            "After", font_size=BODY_SIZE, color=MATCH_GOLD
        ).move_to(UP * 1.8)
        self.play(
            Write(after_label),
            *[
                b.animate.move_to(after_box.get_center()).set_opacity(0)
                for b in before_boxes
            ],
            FadeIn(after_box, scale=0.5),
            run_time=1.5,
        )
        self.play(Indicate(after_box, color=MATCH_GOLD))
        self.wait(0.5)

        # ===================== Future =====================
        self.play(FadeOut(after_label), FadeOut(after_box), FadeOut(unify_title))

        future_title = section_title("Open Source and Beyond", color=FORWARD_GREEN)
        self.play(Write(future_title))

        dipy_text = Text(
            "Available in DIPY (dipy.org)", font_size=BODY_SIZE, color=WHITE
        ).move_to(UP * 0.5)
        beyond_text = Text(
            "Beyond the brain: any diffusion process",
            font_size=BODY_SIZE, color=GRAY_B,
        ).next_to(dipy_text, DOWN, buff=0.4)

        self.play(Write(dipy_text), run_time=0.8)
        self.play(Write(beyond_text), run_time=0.8)
        self.wait(1)

        # ===================== Final Frame =====================
        self.play(
            FadeOut(future_title), FadeOut(dipy_text), FadeOut(beyond_text),
            run_time=0.6,
        )

        # Paper title
        paper_title = Text(
            "FORCE: FORward modeling for\nComplex microstructure Estimation",
            font_size=HEADING_SIZE, color=MATCH_GOLD, weight=BOLD,
        ).move_to(UP * 1.0)

        authors = Text(
            "Shah, Henriques, Ramirez-Manzanares et al.",
            font_size=LABEL_SIZE, color=GRAY_B,
        ).next_to(paper_title, DOWN, buff=0.4)

        tagline = Text(
            "One forward fit to rule them all",
            font_size=BODY_SIZE, color=WHITE,
        ).next_to(authors, DOWN, buff=0.5)

        # Underline the tagline for emphasis
        tagline_underline = Underline(tagline, color=MATCH_GOLD, buff=0.1)

        self.play(Write(paper_title), run_time=1.2)
        self.play(Write(authors), run_time=0.6)
        self.play(Write(tagline), Create(tagline_underline), run_time=1)
        self.wait(3)
