"""DOT explainer scenes 4-6: wavelengths, banana shape, sensitivity matrix."""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from style import *


# ---------------------------------------------------------------------------
# Absorption spectrum helpers (simplified but physically motivated)
# ---------------------------------------------------------------------------

def _hbr_absorption(wavelength: float) -> float:
    """Approximate HbR molar extinction (arbitrary units for animation).

    Peaks near 760 nm with higher absorption at 690 nm than 830 nm.
    """
    return 0.8 * np.exp(-((wavelength - 760) ** 2) / (2 * 50**2)) + 0.15


def _hbo2_absorption(wavelength: float) -> float:
    """Approximate HbO2 molar extinction (arbitrary units for animation).

    Peaks near 900 nm with higher absorption at 830 nm than 690 nm.
    """
    return 0.7 * np.exp(-((wavelength - 900) ** 2) / (2 * 70**2)) + 0.12


# Isosbestic crossing calibrated to ~805 nm
_ISO_WL = 805.0


def _greens(r: float, mu_eff: float = 0.3, D: float = 0.05) -> float:
    """Simplified Green's function for semi-infinite diffusion model.

    G(r) = exp(-mu_eff * r) / (4 pi D r)
    Clamped to avoid singularity at r=0.
    """
    r_safe = max(r, 0.05)
    return np.exp(-mu_eff * r_safe) / (4 * np.pi * D * r_safe)


# ===================================================================
# Scene 4: TwoWavelengths
# ===================================================================

class TwoWavelengths(Scene):
    """Two Wavelengths, Two Chromophores -- ~1.5 min."""

    def construct(self) -> None:
        # Title
        title = Text("Two Wavelengths, Two Chromophores",
                      font_size=TITLE_SIZE, color=C["highlight"])
        self.play(Write(title), run_time=1.5)
        self.wait(HOLD)
        self.play(title.animate.scale(0.5).to_edge(UP), run_time=0.8)

        # ---------------------------------------------------------------
        # Phase 1: Absorption spectra
        # ---------------------------------------------------------------
        axes = Axes(
            x_range=[650, 900, 50],
            y_range=[0, 1.0, 0.2],
            x_length=10,
            y_length=5,
            axis_config={
                "include_numbers": True,
                "font_size": 20,
                "include_tip": True,
            },
        ).shift(DOWN * 0.3)

        x_label = axes.get_x_axis_label(
            Tex(r"Wavelength (nm)", font_size=LABEL_SIZE), direction=DOWN,
        )
        y_label = axes.get_y_axis_label(
            Tex(r"Absorption", font_size=LABEL_SIZE), direction=LEFT,
        )

        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.5)
        self.wait(0.5)

        # HbR curve (deoxy) -- blue-purple
        hbr_graph = axes.plot(
            _hbr_absorption, x_range=[650, 900], color=BLUE_D,
            use_smoothing=True,
        )
        hbr_label = Text("HbR", font_size=LABEL_SIZE, color=BLUE_D)
        hbr_label.move_to(axes.c2p(720, _hbr_absorption(720)) + UP * 0.35)

        self.play(Create(hbr_graph), run_time=2)
        self.play(Write(hbr_label), run_time=0.8)

        # HbO2 curve (oxy) -- red-orange
        hbo2_graph = axes.plot(
            _hbo2_absorption, x_range=[650, 900], color=RED_C,
            use_smoothing=True,
        )
        hbo2_label = Text("HbO2", font_size=LABEL_SIZE, color=RED_C)
        hbo2_label.move_to(axes.c2p(870, _hbo2_absorption(870)) + UP * 0.35)

        self.play(Create(hbo2_graph), run_time=2)
        self.play(Write(hbo2_label), run_time=0.8)
        self.wait(HOLD)

        # ---------------------------------------------------------------
        # Phase 2: Mark 690 nm and 830 nm
        # ---------------------------------------------------------------
        wl_690 = 690.0
        wl_830 = 830.0

        line_690 = DashedLine(
            axes.c2p(wl_690, 0), axes.c2p(wl_690, 0.95),
            color=YELLOW, dash_length=0.1,
        )
        line_830 = DashedLine(
            axes.c2p(wl_830, 0), axes.c2p(wl_830, 0.95),
            color=YELLOW, dash_length=0.1,
        )
        label_690 = Text("690 nm", font_size=LABEL_SIZE, color=YELLOW)
        label_690.next_to(line_690, DOWN, buff=0.15)
        label_830 = Text("830 nm", font_size=LABEL_SIZE, color=YELLOW)
        label_830.next_to(line_830, DOWN, buff=0.15)

        self.play(Create(line_690), Write(label_690), run_time=1)
        self.play(Create(line_830), Write(label_830), run_time=1)
        self.wait(1)

        # Highlight HbR dominance at 690 nm
        dot_hbr_690 = Dot(axes.c2p(wl_690, _hbr_absorption(wl_690)),
                          color=BLUE_D, radius=0.1)
        dot_hbo2_690 = Dot(axes.c2p(wl_690, _hbo2_absorption(wl_690)),
                           color=RED_C, radius=0.1)
        brace_690 = BraceBetweenPoints(
            axes.c2p(wl_690, _hbo2_absorption(wl_690)),
            axes.c2p(wl_690, _hbr_absorption(wl_690)),
            direction=LEFT,
        )
        brace_690_label = Tex(r"HbR dominates", font_size=LABEL_SIZE,
                              color=BLUE_D)
        brace_690.put_at_tip(brace_690_label)

        self.play(FadeIn(dot_hbr_690), FadeIn(dot_hbo2_690), run_time=0.6)
        self.play(Create(brace_690), Write(brace_690_label), run_time=1.2)
        self.wait(1)

        # Highlight HbO2 dominance at 830 nm
        dot_hbr_830 = Dot(axes.c2p(wl_830, _hbr_absorption(wl_830)),
                          color=BLUE_D, radius=0.1)
        dot_hbo2_830 = Dot(axes.c2p(wl_830, _hbo2_absorption(wl_830)),
                           color=RED_C, radius=0.1)
        brace_830 = BraceBetweenPoints(
            axes.c2p(wl_830, _hbr_absorption(wl_830)),
            axes.c2p(wl_830, _hbo2_absorption(wl_830)),
            direction=RIGHT,
        )
        brace_830_label = Tex(r"HbO2 dominates", font_size=LABEL_SIZE,
                              color=RED_C)
        brace_830.put_at_tip(brace_830_label)

        self.play(FadeIn(dot_hbr_830), FadeIn(dot_hbo2_830), run_time=0.6)
        self.play(Create(brace_830), Write(brace_830_label), run_time=1.2)
        self.wait(HOLD)

        # ---------------------------------------------------------------
        # Phase 3: Isosbestic point
        # ---------------------------------------------------------------
        iso_y = _hbr_absorption(_ISO_WL)
        iso_dot = Dot(axes.c2p(_ISO_WL, iso_y), color=WHITE, radius=0.12)
        iso_label = Text("Isosbestic point\n~805 nm",
                         font_size=LABEL_SIZE, color=WHITE)
        iso_label.next_to(iso_dot, UR, buff=0.2)

        self.play(FadeIn(iso_dot, scale=1.5), run_time=0.8)
        self.play(Write(iso_label), run_time=1)
        self.wait(1)

        iso_note = Text(
            "At this wavelength, both absorb equally\n"
            "-- useless for distinguishing them.",
            font_size=LABEL_SIZE - 2, color=C["dim"],
        ).next_to(axes, DOWN, buff=0.5)
        self.play(Write(iso_note), run_time=1.5)
        self.wait(HOLD)

        # ---------------------------------------------------------------
        # Phase 4: System of equations
        # ---------------------------------------------------------------
        # Clear annotations
        annotations = VGroup(
            brace_690, brace_690_label, brace_830, brace_830_label,
            dot_hbr_690, dot_hbo2_690, dot_hbr_830, dot_hbo2_830,
            iso_dot, iso_label, iso_note,
        )
        self.play(FadeOut(annotations), run_time=0.8)

        # Shrink the plot to the left
        plot_group = VGroup(axes, x_label, y_label,
                            hbr_graph, hbr_label, hbo2_graph, hbo2_label,
                            line_690, label_690, line_830, label_830)
        self.play(plot_group.animate.scale(0.5).to_edge(LEFT, buff=0.3),
                  run_time=1.2)

        # Equation system on the right
        eq1 = MathTex(
            r"\Delta\mu_a^{690}",
            r"=",
            r"\varepsilon_{\text{HbO}_2}^{690}",
            r"\cdot \Delta[\text{HbO}_2]",
            r"+",
            r"\varepsilon_{\text{HbR}}^{690}",
            r"\cdot \Delta[\text{HbR}]",
            font_size=BODY_SIZE - 4,
        )
        eq2 = MathTex(
            r"\Delta\mu_a^{830}",
            r"=",
            r"\varepsilon_{\text{HbO}_2}^{830}",
            r"\cdot \Delta[\text{HbO}_2]",
            r"+",
            r"\varepsilon_{\text{HbR}}^{830}",
            r"\cdot \Delta[\text{HbR}]",
            font_size=BODY_SIZE - 4,
        )
        eq_group = VGroup(eq1, eq2).arrange(DOWN, buff=0.4)
        eq_group.to_edge(RIGHT, buff=0.5)

        # Color-code
        for eq in (eq1, eq2):
            eq[0].set_color(YELLOW)       # delta mu_a
            eq[2].set_color(RED_C)        # eps HbO2
            eq[3].set_color(RED_C)        # delta [HbO2]
            eq[5].set_color(BLUE_D)       # eps HbR
            eq[6].set_color(BLUE_D)       # delta [HbR]

        self.play(Write(eq1), run_time=2)
        self.wait(0.5)
        self.play(Write(eq2), run_time=2)
        self.wait(1)

        # Brace around both equations
        eq_brace = Brace(eq_group, LEFT, color=C["highlight"])
        solvable = Text("2 wavelengths,\n2 unknowns:\nsolvable!",
                        font_size=LABEL_SIZE, color=C["highlight"])
        eq_brace.put_at_tip(solvable)

        self.play(Create(eq_brace), Write(solvable), run_time=1.5)
        self.wait(HOLD)

        # Final hold
        self.wait(1)


# ===================================================================
# Scene 5: BananaShape
# ===================================================================

class BananaShape(Scene):
    """The Banana Shape: A Visual Proof -- ~2 min.

    The 'aha' moment: sensitivity = G_source x G_detector.
    """

    def construct(self) -> None:
        # Title
        title = Text("The Banana Shape: A Visual Proof",
                      font_size=TITLE_SIZE, color=C["highlight"])
        self.play(Write(title), run_time=1.5)
        self.wait(HOLD)
        self.play(FadeOut(title), run_time=0.5)

        # ---------------------------------------------------------------
        # Phase 1: Tissue surface with source and detector
        # ---------------------------------------------------------------
        surface_y = 2.5
        surface = Line(LEFT * 6, RIGHT * 6, color=C["tissue"], stroke_width=3)
        surface.move_to(UP * surface_y)
        surface_label = Text("tissue surface", font_size=LABEL_SIZE,
                             color=C["tissue"])
        surface_label.next_to(surface, UP, buff=0.1)

        src_x = -2.0
        det_x = 2.0
        source_dot = Dot(point=[src_x, surface_y, 0], color=C["source"],
                         radius=0.15)
        detector_dot = Dot(point=[det_x, surface_y, 0], color=C["detector"],
                           radius=0.15)
        src_label = Text("S", font_size=LABEL_SIZE, color=C["source"])
        src_label.next_to(source_dot, UP, buff=0.15)
        det_label = Text("D", font_size=LABEL_SIZE, color=C["detector"])
        det_label.next_to(detector_dot, UP, buff=0.15)

        self.play(Create(surface), Write(surface_label), run_time=1)
        self.play(FadeIn(source_dot), Write(src_label), run_time=0.8)
        self.play(FadeIn(detector_dot), Write(det_label), run_time=0.8)
        self.wait(1)

        sep_brace = BraceBetweenPoints(
            [src_x, surface_y - 0.1, 0],
            [det_x, surface_y - 0.1, 0],
            direction=DOWN,
            color=C["dim"],
        )
        sep_text = Tex(r"$d = 4$ cm", font_size=LABEL_SIZE, color=C["dim"])
        sep_brace.put_at_tip(sep_text)
        self.play(Create(sep_brace), Write(sep_text), run_time=0.8)
        self.wait(0.5)
        self.play(FadeOut(sep_brace), FadeOut(sep_text), run_time=0.5)

        # ---------------------------------------------------------------
        # Phase 2: Green's function from source
        # ---------------------------------------------------------------
        g_src_label = Text(
            "G_source: light reaching each point from S",
            font_size=LABEL_SIZE - 2, color=C["source"],
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(g_src_label), run_time=1)

        # Concentric semicircles from source
        src_arcs = VGroup()
        for radius in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]:
            opacity = max(0.1, 1.0 - radius / 4.0)
            arc = Arc(
                radius=radius,
                start_angle=-PI, angle=PI,
                color=C["source"],
                stroke_width=2,
                stroke_opacity=opacity,
            )
            arc.move_to([src_x, surface_y, 0])
            src_arcs.add(arc)

        self.play(
            LaggedStart(*[Create(a) for a in src_arcs], lag_ratio=0.15),
            run_time=2.5,
        )
        self.wait(HOLD)

        # ---------------------------------------------------------------
        # Phase 3: Green's function from detector (by reciprocity)
        # ---------------------------------------------------------------
        g_det_label = Text(
            "G_detector: light from each point reaching D",
            font_size=LABEL_SIZE - 2, color=C["detector"],
        ).to_edge(DOWN, buff=0.5)
        self.play(ReplacementTransform(g_src_label, g_det_label), run_time=0.8)

        det_arcs = VGroup()
        for radius in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]:
            opacity = max(0.1, 1.0 - radius / 4.0)
            arc = Arc(
                radius=radius,
                start_angle=-PI, angle=PI,
                color=C["detector"],
                stroke_width=2,
                stroke_opacity=opacity,
            )
            arc.move_to([det_x, surface_y, 0])
            det_arcs.add(arc)

        self.play(
            LaggedStart(*[Create(a) for a in det_arcs], lag_ratio=0.15),
            run_time=2.5,
        )
        self.wait(HOLD)

        # ---------------------------------------------------------------
        # Phase 4: THE VISUAL PROOF -- product of two Green's functions
        # ---------------------------------------------------------------
        multiply_label = Text(
            "Sensitivity = G_source  x  G_detector",
            font_size=BODY_SIZE, color=C["sensitivity"],
        ).to_edge(DOWN, buff=0.5)
        self.play(
            ReplacementTransform(g_det_label, multiply_label),
            run_time=1,
        )

        # Fade out the individual arcs to make room for the product
        self.play(
            src_arcs.animate.set_opacity(0.15),
            det_arcs.animate.set_opacity(0.15),
            run_time=1,
        )

        # Build banana from small squares whose opacity = G_s * G_d
        # Grid below the surface
        nx, ny = 40, 25
        x_min, x_max = -5.5, 5.5
        y_min = surface_y - 5.0
        y_max = surface_y
        dx = (x_max - x_min) / nx
        dy = (y_max - y_min) / ny

        # Pre-compute sensitivity values for normalization
        sensitivity_vals = []
        grid_positions = []
        for ix in range(nx):
            for iy in range(ny):
                cx = x_min + (ix + 0.5) * dx
                cy = y_min + (iy + 0.5) * dy
                # Only below surface
                if cy >= surface_y:
                    continue
                r_src = np.sqrt((cx - src_x)**2 + (cy - surface_y)**2)
                r_det = np.sqrt((cx - det_x)**2 + (cy - surface_y)**2)
                gs = _greens(r_src)
                gd = _greens(r_det)
                sens = gs * gd
                sensitivity_vals.append(sens)
                grid_positions.append((cx, cy, ix, iy))

        max_sens = max(sensitivity_vals) if sensitivity_vals else 1.0

        # Create squares
        banana_squares = VGroup()
        for (cx, cy, ix, iy), sens in zip(grid_positions, sensitivity_vals):
            norm_sens = sens / max_sens
            if norm_sens < 0.02:
                continue
            sq = Square(
                side_length=min(dx, dy) * 0.95,
                fill_color=interpolate_color(BLACK, C["sensitivity"], norm_sens),
                fill_opacity=norm_sens ** 0.6,
                stroke_width=0,
            )
            sq.move_to([cx, cy, 0])
            banana_squares.add(sq)

        self.play(
            FadeIn(banana_squares, lag_ratio=0.005),
            run_time=3,
        )
        self.wait(1)

        # Annotation: "The banana emerges from pure math!"
        emerge_text = Text(
            "The banana emerges from pure math!",
            font_size=BODY_SIZE, color=WHITE,
        ).next_to(multiply_label, UP, buff=0.3)
        self.play(Write(emerge_text), run_time=1.5)
        self.wait(HOLD)

        # ---------------------------------------------------------------
        # Phase 5: PARAMETER SWEEP -- source-detector separation
        # ---------------------------------------------------------------
        # Clear static elements
        self.play(
            FadeOut(emerge_text),
            FadeOut(banana_squares),
            FadeOut(src_arcs), FadeOut(det_arcs),
            FadeOut(multiply_label),
            FadeOut(surface_label),
            run_time=0.8,
        )

        # ValueTracker for separation (half-separation from center)
        sep_tracker = ValueTracker(2.0)  # half-separation

        # Redrawable source and detector
        src_dyn = always_redraw(
            lambda: Dot(
                point=[-sep_tracker.get_value(), surface_y, 0],
                color=C["source"], radius=0.15,
            )
        )
        det_dyn = always_redraw(
            lambda: Dot(
                point=[sep_tracker.get_value(), surface_y, 0],
                color=C["detector"], radius=0.15,
            )
        )
        src_lbl_dyn = always_redraw(
            lambda: Text("S", font_size=LABEL_SIZE, color=C["source"]).next_to(
                [-sep_tracker.get_value(), surface_y, 0], UP, buff=0.15,
            )
        )
        det_lbl_dyn = always_redraw(
            lambda: Text("D", font_size=LABEL_SIZE, color=C["detector"]).next_to(
                [sep_tracker.get_value(), surface_y, 0], UP, buff=0.15,
            )
        )

        # Dynamic separation label
        sep_label_dyn = always_redraw(
            lambda: Text(
                f"Separation: {2 * sep_tracker.get_value():.1f} cm",
                font_size=LABEL_SIZE, color=WHITE,
            ).to_corner(UR, buff=0.3)
        )

        # Dynamic depth label (depth ~ 0.2 * separation)
        depth_label_dyn = always_redraw(
            lambda: Text(
                f"Depth: ~{0.2 * 2 * sep_tracker.get_value():.1f} cm",
                font_size=LABEL_SIZE, color=C["sensitivity"],
            ).to_corner(UR, buff=0.3).shift(DOWN * 0.5)
        )

        # Dynamic banana heatmap
        def _build_banana() -> VGroup:
            half_sep = sep_tracker.get_value()
            sx = -half_sep
            dx_pos = half_sep
            local_nx, local_ny = 35, 20
            lx_min, lx_max = -5.5, 5.5
            ly_min = surface_y - 5.0
            ly_max = surface_y
            cell_dx = (lx_max - lx_min) / local_nx
            cell_dy = (ly_max - ly_min) / local_ny

            vals = []
            positions = []
            for iix in range(local_nx):
                for iiy in range(local_ny):
                    ccx = lx_min + (iix + 0.5) * cell_dx
                    ccy = ly_min + (iiy + 0.5) * cell_dy
                    if ccy >= surface_y:
                        continue
                    rs = np.sqrt((ccx - sx)**2 + (ccy - surface_y)**2)
                    rd = np.sqrt((ccx - dx_pos)**2 + (ccy - surface_y)**2)
                    gs_val = _greens(rs)
                    gd_val = _greens(rd)
                    s_val = gs_val * gd_val
                    vals.append(s_val)
                    positions.append((ccx, ccy))

            local_max = max(vals) if vals else 1.0
            group = VGroup()
            for (ccx, ccy), s_val in zip(positions, vals):
                ns = s_val / local_max
                if ns < 0.03:
                    continue
                cell = Square(
                    side_length=min(cell_dx, cell_dy) * 0.9,
                    fill_color=interpolate_color(BLACK, C["sensitivity"],
                                                 ns),
                    fill_opacity=ns ** 0.6,
                    stroke_width=0,
                )
                cell.move_to([ccx, ccy, 0])
                group.add(cell)
            return group

        banana_dyn = always_redraw(_build_banana)

        # Depth indicator line
        depth_line_dyn = always_redraw(
            lambda: DashedLine(
                [0, surface_y, 0],
                [0, surface_y - 0.2 * 2 * sep_tracker.get_value(), 0],
                color=C["sensitivity"], dash_length=0.08,
            )
        )

        # Remove static source/detector, add dynamic
        self.play(
            FadeOut(source_dot), FadeOut(detector_dot),
            FadeOut(src_label), FadeOut(det_label),
            run_time=0.3,
        )
        self.add(
            banana_dyn, src_dyn, det_dyn, src_lbl_dyn, det_lbl_dyn,
            sep_label_dyn, depth_label_dyn, depth_line_dyn,
        )
        self.wait(1, frozen_frame=False)

        # Sweep: close separation -> wide separation
        self.play(
            sep_tracker.animate.set_value(0.8),
            run_time=3, rate_func=smooth,
        )
        self.wait(1, frozen_frame=False)

        self.play(
            sep_tracker.animate.set_value(3.0),
            run_time=4, rate_func=smooth,
        )
        self.wait(1, frozen_frame=False)

        self.play(
            sep_tracker.animate.set_value(2.0),
            run_time=2, rate_func=smooth,
        )
        self.wait(1, frozen_frame=False)

        # Annotation: depth rule
        rule_text = Text(
            "Depth ~ 0.2 x separation",
            font_size=BODY_SIZE, color=C["sensitivity"],
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(rule_text), run_time=1.2)
        self.wait(HOLD, frozen_frame=False)

        # ---------------------------------------------------------------
        # Phase 6: Jacobian equation
        # ---------------------------------------------------------------
        self.play(FadeOut(rule_text), run_time=0.5)

        jacobian_eq = MathTex(
            r"J(\mathbf{r})",
            r"=",
            r"G(\mathbf{r}_s, \mathbf{r})",
            r"\cdot",
            r"G(\mathbf{r}, \mathbf{r}_d)",
            font_size=EQ_SIZE,
        ).to_edge(DOWN, buff=0.5)
        jacobian_eq[0].set_color(C["sensitivity"])
        jacobian_eq[2].set_color(C["source"])
        jacobian_eq[4].set_color(C["detector"])

        bg_rect = BackgroundRectangle(jacobian_eq, fill_opacity=0.85,
                                      buff=0.2)
        self.play(FadeIn(bg_rect), Write(jacobian_eq), run_time=2)
        self.wait(1, frozen_frame=False)

        # Caption
        feels_text = Text(
            "After the visual proof, this equation feels inevitable.",
            font_size=LABEL_SIZE, color=C["dim"],
        ).next_to(jacobian_eq, UP, buff=0.2)
        feels_bg = BackgroundRectangle(feels_text, fill_opacity=0.85,
                                       buff=0.1)
        self.play(FadeIn(feels_bg), Write(feels_text), run_time=1.5)
        self.wait(HOLD, frozen_frame=False)

        # Final hold
        self.wait(1, frozen_frame=False)


# ===================================================================
# Scene 6: BuildingA
# ===================================================================

class BuildingA(Scene):
    """Building the Sensitivity Matrix -- ~2 min."""

    def construct(self) -> None:
        # Title
        title = Text("Building the Sensitivity Matrix",
                      font_size=TITLE_SIZE, color=C["matrix"])
        self.play(Write(title), run_time=1.5)
        self.wait(HOLD)
        self.play(FadeOut(title), run_time=0.5)

        # ---------------------------------------------------------------
        # Phase 1: Head outline with sources and detectors
        # ---------------------------------------------------------------
        # Semi-circular head
        head = Arc(
            radius=3.0, start_angle=PI, angle=-PI,
            color=C["tissue"], stroke_width=3,
        ).shift(DOWN * 0.5)
        head_top = Line(
            head.get_start(), head.get_end(),
            color=C["tissue"], stroke_width=3,
        )
        head_group = VGroup(head, head_top)

        self.play(Create(head_group), run_time=1.5)

        # Place 4 sources and 4 detectors on the curved surface
        # Sources on left half, detectors on right half
        source_angles = [PI * 0.85, PI * 0.7, PI * 0.55, PI * 0.4]
        detector_angles = [PI * 0.15, PI * 0.3, PI * 0.45, PI * 0.6]

        head_center = DOWN * 0.5
        head_radius = 3.0

        sources = VGroup()
        source_labels = VGroup()
        for i, angle in enumerate(source_angles):
            pos = head_center + head_radius * np.array(
                [np.cos(angle), np.sin(angle), 0]
            )
            dot = Dot(pos, color=C["source"], radius=0.12)
            label = Text(f"S{i+1}", font_size=LABEL_SIZE - 4,
                         color=C["source"])
            label.next_to(dot, normalize(pos - head_center) * 0.5,
                          buff=0.1)
            sources.add(dot)
            source_labels.add(label)

        detectors = VGroup()
        detector_labels = VGroup()
        for i, angle in enumerate(detector_angles):
            pos = head_center + head_radius * np.array(
                [np.cos(angle), np.sin(angle), 0]
            )
            dot = Dot(pos, color=C["detector"], radius=0.12)
            label = Text(f"D{i+1}", font_size=LABEL_SIZE - 4,
                         color=C["detector"])
            label.next_to(dot, normalize(pos - head_center) * 0.5,
                          buff=0.1)
            detectors.add(dot)
            detector_labels.add(label)

        # Animate appearing one by one
        self.play(
            LaggedStart(
                *[FadeIn(s, scale=1.5) for s in sources],
                lag_ratio=0.2,
            ),
            LaggedStart(
                *[Write(l) for l in source_labels],
                lag_ratio=0.2,
            ),
            run_time=2,
        )
        self.play(
            LaggedStart(
                *[FadeIn(d, scale=1.5) for d in detectors],
                lag_ratio=0.2,
            ),
            LaggedStart(
                *[Write(l) for l in detector_labels],
                lag_ratio=0.2,
            ),
            run_time=2,
        )
        self.wait(1)

        # ---------------------------------------------------------------
        # Helper: build a banana between two optode positions
        # ---------------------------------------------------------------
        def _make_banana(
            src_pos: np.ndarray,
            det_pos: np.ndarray,
            color: ManimColor,
            n_cells: int = 20,
            opacity_scale: float = 0.5,
        ) -> VGroup:
            """Build a banana-shaped sensitivity region inside the head."""
            group = VGroup()
            # Sample grid inside the head semicircle
            for ix in range(n_cells):
                for iy in range(n_cells):
                    cx = -2.8 + ix * (5.6 / n_cells)
                    cy = -3.3 + iy * (2.8 / n_cells)
                    pos = np.array([cx, cy, 0])
                    # Must be inside head
                    dist_from_center = np.linalg.norm(pos - head_center)
                    if dist_from_center > head_radius * 0.92:
                        continue
                    if cy > head_center[1] + head_radius * 0.05:
                        continue
                    r_s = np.linalg.norm(pos - src_pos)
                    r_d = np.linalg.norm(pos - det_pos)
                    gs_val = _greens(r_s, mu_eff=0.8)
                    gd_val = _greens(r_d, mu_eff=0.8)
                    sens = gs_val * gd_val
                    # Normalize roughly
                    ns = min(1.0, sens * 50)
                    if ns < 0.05:
                        continue
                    cell_size = 5.6 / n_cells * 0.85
                    cell = Square(
                        side_length=cell_size,
                        fill_color=color,
                        fill_opacity=ns * opacity_scale,
                        stroke_width=0,
                    )
                    cell.move_to(pos)
                    group.add(cell)
            return group

        # ---------------------------------------------------------------
        # Phase 2: First source-detector pair banana
        # ---------------------------------------------------------------
        pair1_src = sources[1].get_center()
        pair1_det = detectors[1].get_center()

        # Highlight the pair
        highlight1 = VGroup(
            SurroundingRectangle(sources[1], color=YELLOW, buff=0.08),
            SurroundingRectangle(detectors[1], color=YELLOW, buff=0.08),
        )
        conn1 = Line(pair1_src, pair1_det, color=YELLOW,
                      stroke_width=1, stroke_opacity=0.4)
        self.play(Create(highlight1), Create(conn1), run_time=0.8)

        banana1 = _make_banana(pair1_src, pair1_det, C["sensitivity"])
        meas1_label = Text("Measurement 1", font_size=LABEL_SIZE,
                           color=C["sensitivity"])
        meas1_label.to_edge(DOWN, buff=0.5)

        self.play(FadeIn(banana1, lag_ratio=0.01), Write(meas1_label),
                  run_time=2)
        self.wait(1)
        self.play(FadeOut(highlight1), FadeOut(conn1), run_time=0.5)

        # ---------------------------------------------------------------
        # Phase 3: Second pair with different separation
        # ---------------------------------------------------------------
        pair2_src = sources[0].get_center()
        pair2_det = detectors[2].get_center()

        highlight2 = VGroup(
            SurroundingRectangle(sources[0], color=YELLOW, buff=0.08),
            SurroundingRectangle(detectors[2], color=YELLOW, buff=0.08),
        )
        conn2 = Line(pair2_src, pair2_det, color=YELLOW,
                      stroke_width=1, stroke_opacity=0.4)
        self.play(Create(highlight2), Create(conn2), run_time=0.8)

        banana2 = _make_banana(pair2_src, pair2_det, TEAL_C)
        meas2_label = Text("Measurement 2", font_size=LABEL_SIZE,
                           color=TEAL_C)
        meas2_label.to_edge(DOWN, buff=0.5)

        self.play(
            FadeIn(banana2, lag_ratio=0.01),
            ReplacementTransform(meas1_label, meas2_label),
            run_time=2,
        )
        self.wait(1)
        self.play(FadeOut(highlight2), FadeOut(conn2), run_time=0.5)

        overlap_note = Text("Both bananas visible, overlapping",
                            font_size=LABEL_SIZE, color=C["dim"])
        overlap_note.to_edge(DOWN, buff=0.5)
        self.play(ReplacementTransform(meas2_label, overlap_note),
                  run_time=0.8)
        self.wait(1)

        # ---------------------------------------------------------------
        # Phase 4: All pairs with overlapping bananas
        # ---------------------------------------------------------------
        # Define 6 more source-detector pairs
        more_pairs = [
            (0, 0), (1, 0), (2, 3), (3, 3), (0, 3), (2, 1),
        ]
        banana_colors = [
            GREEN_C, ORANGE, MAROON_C, LIGHT_PINK, GOLD_C, BLUE_C,
        ]

        all_bananas = VGroup(banana1, banana2)
        for (si, di), bcolor in zip(more_pairs, banana_colors):
            sp = sources[si].get_center()
            dp = detectors[di].get_center()
            b = _make_banana(sp, dp, bcolor, n_cells=18, opacity_scale=0.35)
            all_bananas.add(b)

        # Animate new bananas appearing in a staggered fashion
        new_bananas = all_bananas[2:]
        self.play(
            LaggedStart(
                *[FadeIn(b, lag_ratio=0.005) for b in new_bananas],
                lag_ratio=0.15,
            ),
            run_time=3,
        )

        dense_note = Text("Dense, overlapping sensitivity patterns",
                          font_size=LABEL_SIZE, color=C["dim"])
        dense_note.to_edge(DOWN, buff=0.5)
        self.play(ReplacementTransform(overlap_note, dense_note),
                  run_time=0.8)
        self.wait(HOLD)

        # ---------------------------------------------------------------
        # Phase 5: DUAL VIEW transition
        # ---------------------------------------------------------------
        self.play(FadeOut(dense_note), run_time=0.4)

        # Shrink head + bananas to the left
        head_side = VGroup(head_group, sources, source_labels,
                           detectors, detector_labels, all_bananas)
        self.play(
            head_side.animate.scale(0.55).to_edge(LEFT, buff=0.3),
            run_time=1.5,
        )

        left_title = Text("Physical Space", font_size=LABEL_SIZE,
                          color=C["tissue"])
        left_title.next_to(head_side, UP, buff=0.15)
        self.play(Write(left_title), run_time=0.6)

        # Build matrix heatmap on the right
        n_measurements = 8
        n_voxels = 12
        right_title = Text("Sensitivity Matrix", font_size=LABEL_SIZE,
                           color=C["matrix"])

        # Create a grid of colored rectangles as a heatmap
        matrix_group = VGroup()
        row_colors = [
            C["sensitivity"], TEAL_C, GREEN_C, ORANGE,
            MAROON_C, LIGHT_PINK, GOLD_C, BLUE_C,
        ]
        np.random.seed(42)
        cell_w = 0.3
        cell_h = 0.35
        heatmap_data = []  # store for later highlight
        for row in range(n_measurements):
            row_data = []
            for col in range(n_voxels):
                # Simulate banana-like pattern: peak in middle, tapering
                peak = 2 + row * 1.1
                val = np.exp(-((col - peak) ** 2) / (2 * 2.0**2))
                val *= (0.5 + 0.5 * np.random.random())
                val = min(1.0, max(0.0, val))
                row_data.append(val)
                rect = Rectangle(
                    width=cell_w, height=cell_h,
                    fill_color=interpolate_color(BLACK, row_colors[row], val),
                    fill_opacity=0.8,
                    stroke_color=C["dim"], stroke_width=0.5,
                )
                rect.move_to([
                    col * cell_w,
                    -row * cell_h,
                    0,
                ])
                matrix_group.add(rect)
            heatmap_data.append(row_data)

        matrix_group.move_to(RIGHT * 2.5)
        right_title.next_to(matrix_group, UP, buff=0.2)

        # Row / column labels
        row_labels = VGroup()
        for i in range(n_measurements):
            rl = Text(f"m{i+1}", font_size=14, color=C["dim"])
            rl.next_to(matrix_group[i * n_voxels], LEFT, buff=0.1)
            row_labels.add(rl)

        col_labels = VGroup()
        for j in range(n_voxels):
            cl = Text(f"v{j+1}", font_size=12, color=C["dim"])
            cl.next_to(matrix_group[j], UP, buff=0.05)
            col_labels.add(cl)

        self.play(
            Write(right_title),
            FadeIn(matrix_group, lag_ratio=0.01),
            run_time=2.5,
        )
        self.play(
            LaggedStart(*[Write(l) for l in row_labels], lag_ratio=0.05),
            LaggedStart(*[Write(l) for l in col_labels], lag_ratio=0.05),
            run_time=1.5,
        )
        self.wait(1)

        # Highlight row 0 in matrix -> highlight banana 0 in head
        row0_rect = SurroundingRectangle(
            VGroup(*matrix_group[:n_voxels]),
            color=YELLOW, buff=0.04, stroke_width=2,
        )
        self.play(Create(row0_rect), run_time=0.8)
        self.play(
            all_bananas[0].animate.set_opacity(0.9),
            run_time=0.8,
        )
        self.wait(1)

        # Highlight row 2 instead
        row2_rect = SurroundingRectangle(
            VGroup(*matrix_group[2 * n_voxels:3 * n_voxels]),
            color=YELLOW, buff=0.04, stroke_width=2,
        )
        self.play(
            ReplacementTransform(row0_rect, row2_rect),
            all_bananas[0].animate.set_opacity(0.35),
            all_bananas[2].animate.set_opacity(0.9),
            run_time=1,
        )
        self.wait(1)
        self.play(
            FadeOut(row2_rect),
            all_bananas[2].animate.set_opacity(0.35),
            run_time=0.6,
        )

        # ---------------------------------------------------------------
        # Phase 6: Label the matrix
        # ---------------------------------------------------------------
        big_a = MathTex(r"\mathbf{A}", font_size=72, color=C["matrix"])
        big_a.next_to(matrix_group, LEFT, buff=0.8)

        self.play(Write(big_a), run_time=1.2)
        self.wait(1)

        row_explain = Text(
            "Each row = one banana",
            font_size=LABEL_SIZE, color=C["sensitivity"],
        )
        col_explain = Text(
            "Each column = one voxel's influence on ALL measurements",
            font_size=LABEL_SIZE - 2, color=C["matrix"],
        )
        explains = VGroup(row_explain, col_explain).arrange(DOWN, buff=0.2)
        explains.to_edge(DOWN, buff=0.5)

        self.play(Write(row_explain), run_time=1.2)
        self.wait(0.5)
        self.play(Write(col_explain), run_time=1.5)
        self.wait(HOLD)

        # Final equation
        final_eq = MathTex(
            r"\Delta \mathbf{y}",
            r"=",
            r"\mathbf{A}",
            r"\cdot",
            r"\Delta \mathbf{x}",
            font_size=EQ_SIZE,
        )
        final_eq[0].set_color(C["detector"])
        final_eq[2].set_color(C["matrix"])
        final_eq[4].set_color(C["recon"])
        final_eq.next_to(explains, UP, buff=0.3)

        bg = BackgroundRectangle(final_eq, fill_opacity=0.85, buff=0.15)
        self.play(FadeIn(bg), Write(final_eq), run_time=2)
        self.wait(1)

        # Closing remark
        closing = Text(
            "We SAW what A contains.",
            font_size=BODY_SIZE, color=C["highlight"],
        )
        closing.next_to(final_eq, UP, buff=0.25)
        closing_bg = BackgroundRectangle(closing, fill_opacity=0.85, buff=0.1)
        self.play(FadeIn(closing_bg), Write(closing), run_time=1.5)
        self.wait(HOLD)

        # Final hold
        self.wait(1)
