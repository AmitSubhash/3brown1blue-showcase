"""Scenes 4-6 for FORCE paper explainer video.

Scene 4: BuildingTheSignalModel -- multi-compartment signal model
Scene 5: BuildingTheDictionary  -- simulation dictionary construction
Scene 6: CosineSimilarity       -- why cosine similarity beats L2
"""
from manim import *
from style import *
import numpy as np


# ---------------------------------------------------------------------------
# Scene 4: BuildingTheSignalModel (2.5 min)
# ---------------------------------------------------------------------------
class BuildingTheSignalModel(Scene):
    """Build the multi-compartment signal model piece by piece.

    Geometry before algebra: show each compartment visually, then its equation,
    then assemble the full signal model.
    """

    def construct(self) -> None:
        # ---- Title --------------------------------------------------------
        title = section_title("The Biophysical Signal Model")
        self.play(Write(title))
        self.wait(0.8)

        # ---- Single axon fiber (horizontal cylinder as a line) ------------
        fiber = Line(LEFT * 4, RIGHT * 4, color=WHITE, stroke_width=4)
        fiber.shift(UP * 0.5)
        fiber_label = label_text("Single axon fiber").next_to(fiber, UP, buff=0.3)
        self.play(Create(fiber), Write(fiber_label))
        self.wait(0.8)
        self.play(FadeOut(fiber_label))

        # ==================================================================
        # INTRA-AXONAL (Stick)
        # ==================================================================
        self._build_intra_axonal(fiber, title)

        # ==================================================================
        # EXTRA-AXONAL (Zeppelin)
        # ==================================================================
        self._build_extra_axonal(fiber, title)

        # ==================================================================
        # BINGHAM DISTRIBUTION (Dispersion)
        # ==================================================================
        self._build_dispersion(title)

        # ==================================================================
        # FREE WATER (CSF)
        # ==================================================================
        self._build_free_water(title)

        # ==================================================================
        # GRAY MATTER
        # ==================================================================
        self._build_gray_matter(title)

        # ==================================================================
        # FULL SIGNAL EQUATION
        # ==================================================================
        self._build_full_equation(title)

    # -- Intra-axonal compartment ------------------------------------------
    def _build_intra_axonal(self, fiber: Line, title: Mobject) -> None:
        """Show stick model: 1D restricted diffusion along fiber."""
        # Section label
        comp_label = body_text("Intra-axonal Compartment", color=INTRA_COLOR)
        comp_label.next_to(title, DOWN, buff=0.5)
        self.play(Write(comp_label))

        # Color the fiber
        fiber_colored = fiber.copy().set_color(INTRA_COLOR)
        self.play(Transform(fiber, fiber_colored))

        # Dots moving ALONG the fiber only
        dots = VGroup()
        for x_pos in np.linspace(-3.5, 3.5, 8):
            dot = Dot(
                point=fiber.get_start() + RIGHT * (x_pos + 4),
                radius=0.06,
                color=INTRA_COLOR,
            )
            dots.add(dot)

        self.play(FadeIn(dots, lag_ratio=0.1))

        # Animate dots sliding along the fiber
        dot_shifts = [0.4, -0.3, 0.5, -0.2, 0.3, -0.4, 0.2, -0.5]
        anims = []
        for i, dot in enumerate(dots):
            anims.append(dot.animate.shift(RIGHT * dot_shifts[i]))
        self.play(*anims, run_time=1.5)

        desc = body_text(
            "Water inside axons: restricted to 1D", color=INTRA_COLOR
        ).scale(0.8)
        desc.next_to(fiber, DOWN, buff=0.6)
        self.play(Write(desc))
        self.wait(0.5)

        # Signal equation
        eq_intra = MathTex(
            r"S_{\text{in}} = \exp\!\bigl(-b\, D_{\parallel}\,"
            r"(\mathbf{g} \cdot \mathbf{n})^2\bigr)",
            font_size=EQ_SIZE,
            color=INTRA_COLOR,
        )
        eq_intra.next_to(desc, DOWN, buff=0.5)
        self.play(Write(eq_intra))
        self.wait(0.8)

        # Gradient parallel to fiber: strong attenuation
        g_arrow_par = Arrow(
            fiber.get_start() + DOWN * 1.8 + LEFT * 0.5,
            fiber.get_start() + DOWN * 1.8 + RIGHT * 1.5,
            color=YELLOW,
            buff=0,
            stroke_width=3,
        )
        g_par_label = MathTex(
            r"\mathbf{g} \parallel \mathbf{n} \Rightarrow"
            r" \mathbf{g}\!\cdot\!\mathbf{n}=1 \text{, strong decay}",
            font_size=LABEL_SIZE,
            color=YELLOW,
        ).next_to(g_arrow_par, DOWN, buff=0.2)

        self.play(FadeOut(eq_intra))
        eq_intra.next_to(comp_label, DOWN, buff=0.4)
        self.play(Write(eq_intra))

        self.play(GrowArrow(g_arrow_par), Write(g_par_label))
        self.wait(1.0)
        self.play(FadeOut(g_arrow_par), FadeOut(g_par_label))

        # Gradient perpendicular: no attenuation
        g_arrow_perp = Arrow(
            fiber.get_center() + DOWN * 0.5,
            fiber.get_center() + DOWN * 2.0,
            color=YELLOW,
            buff=0,
            stroke_width=3,
        )
        g_perp_label = MathTex(
            r"\mathbf{g} \perp \mathbf{n} \Rightarrow"
            r" \mathbf{g}\!\cdot\!\mathbf{n}=0 \text{, no decay}",
            font_size=LABEL_SIZE,
            color=YELLOW,
        ).next_to(g_arrow_perp, RIGHT, buff=0.3)

        self.play(GrowArrow(g_arrow_perp), Write(g_perp_label))
        self.wait(1.0)

        # Clean up
        self.play(
            FadeOut(dots),
            FadeOut(desc),
            FadeOut(eq_intra),
            FadeOut(comp_label),
            FadeOut(g_arrow_perp),
            FadeOut(g_perp_label),
        )

    # -- Extra-axonal compartment ------------------------------------------
    def _build_extra_axonal(self, fiber: Line, title: Mobject) -> None:
        """Show zeppelin model: hindered anisotropic diffusion outside fibers."""
        comp_label = body_text("Extra-axonal Compartment", color=EXTRA_COLOR)
        comp_label.next_to(title, DOWN, buff=0.5)
        self.play(Write(comp_label))

        # Ellipse surrounding the fiber (zeppelin cross-section)
        zeppelin = Ellipse(
            width=5.0, height=1.8, color=EXTRA_COLOR, stroke_width=3
        )
        zeppelin.move_to(fiber.get_center())
        self.play(Create(zeppelin))

        # Dots moving around the fiber with more freedom
        extra_dots = VGroup()
        rng = np.random.default_rng(42)
        for _ in range(14):
            x = rng.uniform(-2.0, 2.0)
            y = rng.uniform(-0.6, 0.6)
            dot = Dot(
                point=fiber.get_center() + RIGHT * x + UP * y,
                radius=0.05,
                color=EXTRA_COLOR,
            )
            extra_dots.add(dot)
        self.play(FadeIn(extra_dots, lag_ratio=0.05))

        # Animate dots anisotropically (more along x, less along y)
        anims = []
        for dot in extra_dots:
            dx = rng.uniform(-0.5, 0.5)
            dy = rng.uniform(-0.15, 0.15)
            anims.append(dot.animate.shift(RIGHT * dx + UP * dy))
        self.play(*anims, run_time=1.5)

        desc = body_text(
            "Water outside axons: hindered, anisotropic",
            color=EXTRA_COLOR,
        ).scale(0.8)
        desc.next_to(zeppelin, DOWN, buff=0.5)
        self.play(Write(desc))
        self.wait(0.5)

        # Signal equation
        eq_extra = MathTex(
            r"S_{\text{ex}} = \exp\!\bigl(-b\,"
            r"\bigl[D_{\perp} + (D_{\parallel} - D_{\perp})"
            r"(\mathbf{g}\!\cdot\!\mathbf{n})^2\bigr]\bigr)",
            font_size=SMALL_EQ,
            color=EXTRA_COLOR,
        )
        eq_extra.next_to(desc, DOWN, buff=0.4)
        self.play(Write(eq_extra))
        self.wait(0.8)

        note_extra = label_text(
            "Has both parallel AND perpendicular diffusivity",
            color=EXTRA_COLOR,
        )
        note_extra.next_to(eq_extra, DOWN, buff=0.3)
        self.play(Write(note_extra))
        self.wait(1.0)

        # Clean up
        self.play(
            FadeOut(extra_dots),
            FadeOut(zeppelin),
            FadeOut(desc),
            FadeOut(eq_extra),
            FadeOut(note_extra),
            FadeOut(comp_label),
        )

    # -- Bingham dispersion ------------------------------------------------
    def _build_dispersion(self, title: Mobject) -> None:
        """Show fiber orientation dispersion via Bingham distribution."""
        comp_label = body_text("Fiber Dispersion", color=ODI_COLOR)
        comp_label.next_to(title, DOWN, buff=0.5)
        self.play(Write(comp_label))

        # Many fibers fanning out from a central direction
        center = ORIGIN + UP * 0.2
        fibers = VGroup()
        rng = np.random.default_rng(7)
        n_fibers = 18
        base_angle = 0  # horizontal
        for i in range(n_fibers):
            angle = base_angle + rng.normal(0, 15)  # degrees
            rad = np.radians(angle)
            length = rng.uniform(2.5, 3.5)
            direction = RIGHT * np.cos(rad) + UP * np.sin(rad)
            line = Line(
                center - direction * length * 0.5,
                center + direction * length * 0.5,
                color=ManimColor.from_hex(INTRA_COLOR).interpolate(
                    ManimColor.from_hex(ODI_COLOR), i / n_fibers
                ),
                stroke_width=2,
                stroke_opacity=0.7,
            )
            fibers.add(line)

        self.play(
            LaggedStart(*[Create(f) for f in fibers], lag_ratio=0.08),
            run_time=2.0,
        )

        desc = body_text(
            "Fiber dispersion: orientation spread within a voxel",
            color=ODI_COLOR,
        ).scale(0.75)
        desc.next_to(fibers, DOWN, buff=0.5)
        self.play(Write(desc))
        self.wait(0.5)

        # Bingham equation
        eq_bingham = MathTex(
            r"p_i(\mathbf{n}) = \frac{1}{c(\mathbf{Z})}"
            r"\exp\!\bigl(\mathbf{n}^T \mathbf{Z}\, \mathbf{n}\bigr)",
            font_size=EQ_SIZE,
            color=ODI_COLOR,
        )
        eq_bingham.next_to(desc, DOWN, buff=0.4)
        self.play(Write(eq_bingham))
        self.wait(0.5)

        odi_note = label_text(
            "ODI parameter controls the orientation spread",
            color=ODI_COLOR,
        )
        odi_note.next_to(eq_bingham, DOWN, buff=0.3)
        self.play(Write(odi_note))
        self.wait(1.0)

        # Clean up
        self.play(
            FadeOut(fibers),
            FadeOut(desc),
            FadeOut(eq_bingham),
            FadeOut(odi_note),
            FadeOut(comp_label),
        )

    # -- Free water (CSF) --------------------------------------------------
    def _build_free_water(self, title: Mobject) -> None:
        """Show isotropic fast diffusion for CSF."""
        comp_label = body_text("Free Water (CSF)", color=CSF_COLOR)
        comp_label.next_to(title, DOWN, buff=0.5)
        self.play(Write(comp_label))

        # Circle (isotropic, no preferred direction)
        iso_circle = Circle(radius=1.2, color=CSF_COLOR, stroke_width=3)
        iso_circle.move_to(ORIGIN + UP * 0.3)
        self.play(Create(iso_circle))

        # Dots moving in ALL directions equally
        csf_dots = VGroup()
        rng = np.random.default_rng(99)
        for _ in range(16):
            angle = rng.uniform(0, TAU)
            r = rng.uniform(0, 0.9)
            pos = iso_circle.get_center() + RIGHT * r * np.cos(angle) + UP * r * np.sin(angle)
            dot = Dot(pos, radius=0.05, color=CSF_COLOR)
            csf_dots.add(dot)
        self.play(FadeIn(csf_dots, lag_ratio=0.05))

        # Animate dots moving radially outward in all directions
        anims = []
        for dot in csf_dots:
            angle = rng.uniform(0, TAU)
            dist = rng.uniform(0.3, 0.6)
            anims.append(
                dot.animate.shift(RIGHT * dist * np.cos(angle) + UP * dist * np.sin(angle))
            )
        self.play(*anims, run_time=1.5)

        desc = body_text(
            "Isotropic, fast diffusion (no barriers)",
            color=CSF_COLOR,
        ).scale(0.8)
        desc.next_to(iso_circle, DOWN, buff=0.6)
        self.play(Write(desc))
        self.wait(0.5)

        eq_csf = MathTex(
            r"S_{\text{FW}} = \exp(-b\, D_{\text{FW}})",
            font_size=SMALL_EQ,
            color=CSF_COLOR,
        )
        eq_csf.next_to(desc, DOWN, buff=0.4)
        self.play(Write(eq_csf))
        self.wait(1.0)

        # Clean up
        self.play(
            FadeOut(csf_dots),
            FadeOut(iso_circle),
            FadeOut(desc),
            FadeOut(eq_csf),
            FadeOut(comp_label),
        )

    # -- Gray matter -------------------------------------------------------
    def _build_gray_matter(self, title: Mobject) -> None:
        """Show gray matter: isotropic but slower than CSF."""
        comp_label = body_text("Gray Matter", color=GM_COLOR)
        comp_label.next_to(title, DOWN, buff=0.5)
        self.play(Write(comp_label))

        # Circle (isotropic) but with small organelle-like blobs inside
        gm_circle = Circle(radius=1.2, color=GM_COLOR, stroke_width=3)
        gm_circle.move_to(ORIGIN + UP * 0.3)
        self.play(Create(gm_circle))

        # Small obstacles inside to suggest organelles hindering movement
        obstacles = VGroup()
        rng = np.random.default_rng(55)
        for _ in range(6):
            angle = rng.uniform(0, TAU)
            r = rng.uniform(0.3, 0.8)
            blob = Circle(
                radius=0.12,
                color=GM_COLOR,
                fill_color=GM_COLOR,
                fill_opacity=0.3,
                stroke_width=1,
            )
            blob.move_to(
                gm_circle.get_center()
                + RIGHT * r * np.cos(angle)
                + UP * r * np.sin(angle)
            )
            obstacles.add(blob)
        self.play(FadeIn(obstacles, lag_ratio=0.1))

        # Slower dots
        gm_dots = VGroup()
        for _ in range(10):
            angle = rng.uniform(0, TAU)
            r = rng.uniform(0, 0.7)
            pos = (
                gm_circle.get_center()
                + RIGHT * r * np.cos(angle)
                + UP * r * np.sin(angle)
            )
            dot = Dot(pos, radius=0.05, color=WHITE)
            gm_dots.add(dot)
        self.play(FadeIn(gm_dots, lag_ratio=0.05))

        # Small movements (slower)
        anims = []
        for dot in gm_dots:
            angle = rng.uniform(0, TAU)
            dist = rng.uniform(0.1, 0.25)
            anims.append(
                dot.animate.shift(RIGHT * dist * np.cos(angle) + UP * dist * np.sin(angle))
            )
        self.play(*anims, run_time=1.5)

        desc = body_text(
            "Isotropic but slower (organelles hinder movement)",
            color=GM_COLOR,
        ).scale(0.8)
        desc.next_to(gm_circle, DOWN, buff=0.6)
        self.play(Write(desc))
        self.wait(0.5)

        eq_gm = MathTex(
            r"S_{\text{GM}} = \exp(-b\, D_{\text{GM}})",
            font_size=SMALL_EQ,
            color=GM_COLOR,
        )
        eq_gm.next_to(desc, DOWN, buff=0.4)
        self.play(Write(eq_gm))
        self.wait(1.0)

        # Clean up
        self.play(
            FadeOut(gm_dots),
            FadeOut(obstacles),
            FadeOut(gm_circle),
            FadeOut(desc),
            FadeOut(eq_gm),
            FadeOut(comp_label),
        )

    # -- Full signal equation (assembly) -----------------------------------
    def _build_full_equation(self, title: Mobject) -> None:
        """Assemble the complete multi-compartment signal equation."""
        # Clear the fiber
        self.play(*[FadeOut(m) for m in self.mobjects if m is not title])
        self.wait(0.3)

        heading = body_text("Assembling the Full Model", color=HIGHLIGHT)
        heading.next_to(title, DOWN, buff=0.5)
        self.play(Write(heading))

        # Build equation term by term
        # Start with S = S0 [ ... ]
        eq_base = MathTex(
            r"S = S_0 \Big[", r"\cdots", r"\Big]",
            font_size=EQ_SIZE,
        )
        eq_base.move_to(ORIGIN + UP * 0.5)
        self.play(Write(eq_base))
        self.wait(0.5)

        # Full equation with colored terms
        # We use substrings for coloring
        eq_full = MathTex(
            r"S = S_0 \Big[",                        # 0
            r"f_{\text{in}}",                         # 1
            r"\, S_{\text{in}}",                      # 2
            r"+",                                     # 3
            r"f_{\text{ex}}",                         # 4
            r"\, S_{\text{ex}}",                      # 5
            r"+",                                     # 6
            r"f_{\text{FW}}",                         # 7
            r"\, S_{\text{FW}}",                      # 8
            r"+",                                     # 9
            r"f_{\text{GM}}",                         # 10
            r"\, S_{\text{GM}}",                      # 11
            r"\Big]",                                 # 12
            font_size=EQ_SIZE,
        )
        eq_full.move_to(ORIGIN + UP * 0.5)

        # Color each compartment term
        eq_full[1].set_color(INTRA_COLOR)
        eq_full[2].set_color(INTRA_COLOR)
        eq_full[4].set_color(EXTRA_COLOR)
        eq_full[5].set_color(EXTRA_COLOR)
        eq_full[7].set_color(CSF_COLOR)
        eq_full[8].set_color(CSF_COLOR)
        eq_full[10].set_color(GM_COLOR)
        eq_full[11].set_color(GM_COLOR)

        # Staged build: transform base into full
        self.play(ReplacementTransform(eq_base, eq_full), run_time=2.0)
        self.wait(0.5)

        # Highlight each term with a surrounding box, one at a time
        # Intra
        intra_box = SurroundingRectangle(
            VGroup(eq_full[1], eq_full[2]),
            color=INTRA_COLOR,
            buff=0.08,
        )
        intra_label = label_text("Intra-axonal (stick)", color=INTRA_COLOR)
        intra_label.next_to(intra_box, DOWN, buff=0.3)
        self.play(Create(intra_box), Write(intra_label))
        self.wait(0.6)
        self.play(FadeOut(intra_box), FadeOut(intra_label))

        # Extra
        extra_box = SurroundingRectangle(
            VGroup(eq_full[4], eq_full[5]),
            color=EXTRA_COLOR,
            buff=0.08,
        )
        extra_label = label_text("Extra-axonal (zeppelin)", color=EXTRA_COLOR)
        extra_label.next_to(extra_box, DOWN, buff=0.3)
        self.play(Create(extra_box), Write(extra_label))
        self.wait(0.6)
        self.play(FadeOut(extra_box), FadeOut(extra_label))

        # CSF
        csf_box = SurroundingRectangle(
            VGroup(eq_full[7], eq_full[8]),
            color=CSF_COLOR,
            buff=0.08,
        )
        csf_label = label_text("Free water (CSF)", color=CSF_COLOR)
        csf_label.next_to(csf_box, DOWN, buff=0.3)
        self.play(Create(csf_box), Write(csf_label))
        self.wait(0.6)
        self.play(FadeOut(csf_box), FadeOut(csf_label))

        # GM
        gm_box = SurroundingRectangle(
            VGroup(eq_full[10], eq_full[11]),
            color=GM_COLOR,
            buff=0.08,
        )
        gm_label = label_text("Gray matter", color=GM_COLOR)
        gm_label.next_to(gm_box, DOWN, buff=0.3)
        self.play(Create(gm_box), Write(gm_label))
        self.wait(0.6)
        self.play(FadeOut(gm_box), FadeOut(gm_label))

        # Constraint: fractions sum to 1
        constraint = MathTex(
            r"f_{\text{in}} + f_{\text{ex}} + f_{\text{FW}}"
            r"+ f_{\text{GM}} = 1",
            font_size=EQ_SIZE,
        )
        constraint.next_to(eq_full, DOWN, buff=0.8)
        constraint_box = SurroundingRectangle(
            constraint, color=HIGHLIGHT, buff=0.15
        )
        self.play(Write(constraint), Create(constraint_box))
        self.wait(1.0)

        # Bottom note
        note = bottom_note(
            "Each compartment captures a distinct physical behavior"
        )
        self.play(Write(note))
        self.wait(2.0)

        # Clean up everything
        self.play(
            *[FadeOut(m) for m in self.mobjects],
        )


# ---------------------------------------------------------------------------
# Scene 5: BuildingTheDictionary (1.5 min)
# ---------------------------------------------------------------------------
class BuildingTheDictionary(Scene):
    """Show how the simulation dictionary is constructed.

    Random tissue configurations are fed through the signal model to produce
    signal fingerprints, which are assembled into a large dictionary matrix.
    """

    def construct(self) -> None:
        # ---- Title --------------------------------------------------------
        title = section_title("Building the Dictionary")
        self.play(Write(title))
        self.wait(0.8)

        # ==================================================================
        # Step 1: Single configuration -> signal model -> signal profile
        # ==================================================================
        self._show_single_config(title)

        # ==================================================================
        # Step 2: Many configurations -> dictionary matrix
        # ==================================================================
        self._show_dictionary_matrix(title)

        # ==================================================================
        # Step 3: Parameter ranges table
        # ==================================================================
        self._show_parameter_ranges(title)

        # ==================================================================
        # Step 4: Fingerprint visualization
        # ==================================================================
        self._show_fingerprints(title)

    def _show_single_config(self, title: Mobject) -> None:
        """Show one configuration card -> signal model -> bar chart."""
        # Configuration card
        card_rect = RoundedRectangle(
            corner_radius=0.15,
            width=3.2,
            height=2.0,
            color=SIGNAL_BLUE,
            stroke_width=2,
        )
        card_rect.shift(LEFT * 4.5 + DOWN * 0.3)

        card_lines = VGroup(
            Text("N = 2 fibers", font_size=16, color=WHITE),
            Text("angles = [45, 120]", font_size=16, color=WHITE),
            Text("ODI = 0.1", font_size=16, color=WHITE),
            Text("f_in = 0.7, f_ex = 0.2", font_size=16, color=WHITE),
            Text("f_FW = 0.1", font_size=16, color=WHITE),
        )
        card_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        card_lines.move_to(card_rect.get_center())

        card_title_text = label_text("Configuration", color=SIGNAL_BLUE)
        card_title_text.next_to(card_rect, UP, buff=0.15)

        card_group = VGroup(card_rect, card_lines, card_title_text)

        self.play(FadeIn(card_group))
        self.wait(0.5)

        # Arrow to signal model
        arrow1 = Arrow(
            card_rect.get_right(),
            card_rect.get_right() + RIGHT * 1.5,
            color=WHITE,
            buff=0.1,
            stroke_width=3,
        )
        model_box = RoundedRectangle(
            corner_radius=0.15,
            width=2.5,
            height=1.2,
            color=FORWARD_GREEN,
            stroke_width=2,
            fill_color=FORWARD_GREEN,
            fill_opacity=0.15,
        )
        model_box.next_to(arrow1, RIGHT, buff=0.1)
        model_label = Text(
            "Signal Model", font_size=LABEL_SIZE, color=FORWARD_GREEN
        ).move_to(model_box)

        self.play(GrowArrow(arrow1), FadeIn(model_box), Write(model_label))
        self.wait(0.3)

        # Arrow to signal profile
        arrow2 = Arrow(
            model_box.get_right(),
            model_box.get_right() + RIGHT * 1.5,
            color=WHITE,
            buff=0.1,
            stroke_width=3,
        )
        self.play(GrowArrow(arrow2))

        # Bar chart of signal intensities
        rng = np.random.default_rng(12)
        bar_heights = rng.uniform(0.2, 1.0, 10)
        bars = VGroup()
        bar_start = model_box.get_right() + RIGHT * 2.0 + DOWN * 0.6
        for i, h in enumerate(bar_heights):
            bar = Rectangle(
                width=0.18,
                height=h * 1.2,
                color=MATCH_GOLD,
                fill_color=MATCH_GOLD,
                fill_opacity=0.8,
                stroke_width=1,
            )
            bar.move_to(bar_start + RIGHT * i * 0.22)
            bar.align_to(bar_start, DOWN)
            bars.add(bar)

        bar_label = label_text("Signal profile", color=MATCH_GOLD)
        bar_label.next_to(bars, UP, buff=0.25)

        self.play(
            LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.05),
            Write(bar_label),
            run_time=1.5,
        )
        self.wait(1.0)

        # Clean up
        self.play(
            FadeOut(card_group),
            FadeOut(arrow1),
            FadeOut(model_box),
            FadeOut(model_label),
            FadeOut(arrow2),
            FadeOut(bars),
            FadeOut(bar_label),
        )

    def _show_dictionary_matrix(self, title: Mobject) -> None:
        """Multiply: show multiple configs producing a matrix."""
        # Show 5 config cards appearing
        cards = VGroup()
        for i in range(5):
            card = RoundedRectangle(
                corner_radius=0.1,
                width=1.8,
                height=0.5,
                color=SIGNAL_BLUE,
                stroke_width=1.5,
                fill_color=SIGNAL_BLUE,
                fill_opacity=0.1 + 0.1 * i,
            )
            card_text = Text(
                f"Config {i + 1}", font_size=14, color=SIGNAL_BLUE
            ).move_to(card)
            cards.add(VGroup(card, card_text))

        cards.arrange(DOWN, buff=0.15)
        cards.shift(LEFT * 4.5)

        self.play(
            LaggedStart(*[FadeIn(c, shift=RIGHT * 0.3) for c in cards], lag_ratio=0.15),
            run_time=1.5,
        )
        self.wait(0.5)

        # Arrows
        arrow_group = VGroup()
        for card in cards:
            arr = Arrow(
                card.get_right(),
                card.get_right() + RIGHT * 1.2,
                color=WHITE,
                buff=0.05,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.15,
            )
            arrow_group.add(arr)
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrow_group], lag_ratio=0.1),
            run_time=1.0,
        )

        # Dictionary matrix grid
        n_rows, n_cols = 8, 14
        cell_w, cell_h = 0.35, 0.25
        grid = VGroup()
        rng = np.random.default_rng(42)

        for r in range(n_rows):
            for c in range(n_cols):
                intensity = rng.uniform(0.1, 1.0)
                cell = Rectangle(
                    width=cell_w,
                    height=cell_h,
                    stroke_width=0.5,
                    stroke_color=WHITE,
                    fill_color=ManimColor(BLACK).interpolate(
                        ManimColor.from_hex(MATCH_GOLD), intensity
                    ),
                    fill_opacity=0.9,
                )
                cell.move_to(
                    RIGHT * (c * cell_w - n_cols * cell_w / 2)
                    + DOWN * (r * cell_h - n_rows * cell_h / 2)
                    + RIGHT * 1.8
                )
                grid.add(cell)

        self.play(
            FadeOut(cards),
            FadeOut(arrow_group),
            FadeIn(grid, lag_ratio=0.003),
            run_time=2.0,
        )

        # Labels
        row_label = Text(
            "500,000 configurations",
            font_size=LABEL_SIZE,
            color=WHITE,
        )
        row_label.rotate(PI / 2)
        row_label.next_to(grid, LEFT, buff=0.4)

        col_label = Text(
            "N gradient directions",
            font_size=LABEL_SIZE,
            color=WHITE,
        )
        col_label.next_to(grid, DOWN, buff=0.3)

        matrix_label = body_text("Dictionary Matrix", color=MATCH_GOLD)
        matrix_label.next_to(grid, UP, buff=0.4)

        self.play(Write(row_label), Write(col_label), Write(matrix_label))
        self.wait(1.5)

        self.play(
            FadeOut(grid),
            FadeOut(row_label),
            FadeOut(col_label),
            FadeOut(matrix_label),
        )

    def _show_parameter_ranges(self, title: Mobject) -> None:
        """Show a table of parameter ranges from Table 1 of the paper."""
        heading = body_text("Parameter Ranges", color=HIGHLIGHT)
        heading.next_to(title, DOWN, buff=0.5)
        self.play(Write(heading))

        # Build a simple table
        table_data = [
            [r"D_{\parallel}", r"[0.5,\; 2.5] \times 10^{-3}"],
            [r"D_{\perp}", r"[0.1,\; 1.5] \times 10^{-3}"],
            [r"\text{ODI}", r"[0.01,\; 0.99]"],
            [r"\text{Fiber fractions}", r"[0,\; 1] \;\text{(sum to 1)}"],
            [r"N_{\text{fibers}}", r"\{1,\; 2,\; 3\}"],
        ]

        rows = VGroup()
        for param, range_str in table_data:
            param_tex = MathTex(param, font_size=LABEL_SIZE, color=SIGNAL_BLUE)
            range_tex = MathTex(range_str, font_size=LABEL_SIZE, color=WHITE)
            if param_tex.width > 2.0:
                param_tex.scale_to_fit_width(2.0)
            if range_tex.width > 3.5:
                range_tex.scale_to_fit_width(3.5)
            param_tex.align_to(LEFT * 2, RIGHT)
            range_tex.next_to(param_tex, RIGHT, buff=0.8)
            row = VGroup(param_tex, range_tex)
            rows.add(row)

        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows.move_to(ORIGIN + DOWN * 0.2)

        self.play(
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.15),
            run_time=2.0,
        )
        self.wait(1.5)

        bio_label = body_text(
            '"Biologically plausible" parameter space',
            color=FORWARD_GREEN,
        ).scale(0.8)
        bio_label.next_to(rows, DOWN, buff=0.6)
        self.play(Write(bio_label))
        self.wait(1.0)

        self.play(FadeOut(rows), FadeOut(bio_label), FadeOut(heading))

    def _show_fingerprints(self, title: Mobject) -> None:
        """Show overlaid signal profiles as unique fingerprints."""
        heading = body_text(
            "A Library of Signal Fingerprints", color=MATCH_GOLD
        )
        heading.next_to(title, DOWN, buff=0.5)
        self.play(Write(heading))

        # Several signal profiles overlaid
        rng = np.random.default_rng(7)
        colors = [INTRA_COLOR, EXTRA_COLOR, CSF_COLOR, MATCH_GOLD, INVERSE_RED]
        profiles = VGroup()

        n_points = 20
        x_range = np.linspace(-3.5, 3.5, n_points)

        for idx, color in enumerate(colors):
            # Generate a unique signal shape
            base = rng.uniform(0.3, 0.8)
            freqs = rng.uniform(0.5, 2.0, 3)
            amps = rng.uniform(0.1, 0.3, 3)
            y_vals = base + sum(
                a * np.sin(f * x_range + rng.uniform(0, TAU))
                for a, f in zip(amps, freqs)
            )
            y_vals = np.clip(y_vals, 0.1, 1.2)

            points = [
                np.array([x, y - 1.5, 0])
                for x, y in zip(x_range, y_vals)
            ]

            profile = VMobject(color=color, stroke_width=2.5, stroke_opacity=0.8)
            profile.set_points_smoothly(points)
            profiles.add(profile)

        self.play(
            LaggedStart(
                *[Create(p) for p in profiles],
                lag_ratio=0.3,
            ),
            run_time=3.0,
        )
        self.wait(0.5)

        fingerprint_label = label_text(
            "Each tissue configuration produces a unique signal shape",
            color=WHITE,
        )
        fingerprint_label.next_to(profiles, DOWN, buff=0.6)
        self.play(Write(fingerprint_label))
        self.wait(1.0)

        # Bottom note
        note = bottom_note(
            "Every possible tissue arrangement has a unique signal fingerprint"
        )
        self.play(Write(note))
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects])


# ---------------------------------------------------------------------------
# Scene 6: CosineSimilarity (2 min)
# ---------------------------------------------------------------------------
class CosineSimilarity(Scene):
    """Explain why cosine similarity is preferred over L2 distance.

    Shows scale invariance of cosine, the matching pipeline,
    and a visual proof comparing the two metrics.
    """

    def construct(self) -> None:
        # ---- Title --------------------------------------------------------
        title = section_title("Finding the Best Match")
        self.play(Write(title))
        self.wait(0.8)

        # ==================================================================
        # Step 1: Measured vs simulated bar charts + question
        # ==================================================================
        self._show_comparison_setup(title)

        # ==================================================================
        # Step 2: L2 distance -- the wrong way
        # ==================================================================
        self._show_l2_problem(title)

        # ==================================================================
        # Step 3: Cosine similarity -- the right way
        # ==================================================================
        self._show_cosine_advantage(title)

        # ==================================================================
        # Step 4: The matching pipeline
        # ==================================================================
        self._show_matching_pipeline(title)

        # ==================================================================
        # Step 5: Visual proof -- same shape, different magnitude
        # ==================================================================
        self._show_visual_proof(title)

    def _show_comparison_setup(self, title: Mobject) -> None:
        """Show measured and simulated signal bar charts side by side."""
        rng = np.random.default_rng(42)
        base_signal = rng.uniform(0.3, 1.0, 8)

        # Measured signal (left)
        meas_bars = self._make_bar_chart(
            base_signal, LEFT * 3.5 + DOWN * 0.5, SIGNAL_BLUE, "Measured voxel"
        )
        # Simulated signal (right)
        sim_bars = self._make_bar_chart(
            base_signal * 0.8 + rng.normal(0, 0.03, 8),
            RIGHT * 3.5 + DOWN * 0.5,
            MATCH_GOLD,
            "Simulated",
        )

        self.play(FadeIn(meas_bars), FadeIn(sim_bars))
        self.wait(0.5)

        question = body_text("How do we measure similarity?", color=HIGHLIGHT)
        question.move_to(ORIGIN + DOWN * 2.8)
        self.play(Write(question))
        self.wait(1.5)

        self.play(FadeOut(meas_bars), FadeOut(sim_bars), FadeOut(question))

    def _show_l2_problem(self, title: Mobject) -> None:
        """Demonstrate how L2 distance is fooled by scale."""
        subtitle = body_text("L2 Distance (the wrong way)", color=INVERSE_RED)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(subtitle))

        # Two vectors in 2D
        origin_pt = LEFT * 3 + DOWN * 1
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 3, 1],
            x_length=4,
            y_length=3,
            axis_config={"include_tip": False, "stroke_width": 2},
        )
        axes.move_to(LEFT * 2 + DOWN * 0.5)

        vec_y = Arrow(
            axes.c2p(0, 0),
            axes.c2p(2, 2.5),
            color=SIGNAL_BLUE,
            buff=0,
            stroke_width=3,
        )
        vec_d = Arrow(
            axes.c2p(0, 0),
            axes.c2p(3, 1.5),
            color=MATCH_GOLD,
            buff=0,
            stroke_width=3,
        )
        y_label = MathTex(r"\mathbf{y}", font_size=BODY_SIZE, color=SIGNAL_BLUE)
        y_label.next_to(vec_y.get_end(), UP + LEFT, buff=0.1)
        d_label = MathTex(r"\mathbf{d}", font_size=BODY_SIZE, color=MATCH_GOLD)
        d_label.next_to(vec_d.get_end(), RIGHT, buff=0.1)

        self.play(Create(axes), GrowArrow(vec_y), GrowArrow(vec_d))
        self.play(Write(y_label), Write(d_label))
        self.wait(0.5)

        # L2 formula
        l2_eq = MathTex(
            r"\|\mathbf{y} - \mathbf{d}\|^2",
            font_size=EQ_SIZE,
            color=INVERSE_RED,
        )
        l2_eq.move_to(RIGHT * 3.5 + UP * 1)
        self.play(Write(l2_eq))
        self.wait(0.5)

        # Now scale y by gamma
        gamma_label = MathTex(
            r"\gamma \mathbf{y}",
            font_size=BODY_SIZE,
            color=COSINE_ORANGE,
        )
        vec_gy = Arrow(
            axes.c2p(0, 0),
            axes.c2p(1, 1.25),
            color=COSINE_ORANGE,
            buff=0,
            stroke_width=3,
        )
        gamma_label.next_to(vec_gy.get_end(), LEFT, buff=0.15)

        self.play(GrowArrow(vec_gy), Write(gamma_label))
        self.wait(0.3)

        # Explanation
        l2_problem = MathTex(
            r"\|\gamma\mathbf{y} - \mathbf{d}\|^2 \neq \|\mathbf{y} - \mathbf{d}\|^2",
            font_size=EQ_SIZE,
            color=INVERSE_RED,
        )
        l2_problem.move_to(RIGHT * 3.5 + DOWN * 0.3)
        self.play(Write(l2_problem))
        self.wait(0.5)

        explain_l2 = label_text(
            "Same shape, different magnitude",
            color=COSINE_ORANGE,
        )
        explain_l2.next_to(l2_problem, DOWN, buff=0.3)
        self.play(Write(explain_l2))
        self.wait(0.3)

        explain_l2b = label_text(
            "but L2 says they are different!",
            color=INVERSE_RED,
        )
        explain_l2b.next_to(explain_l2, DOWN, buff=0.2)
        self.play(Write(explain_l2b))
        self.wait(0.5)

        # Red X
        red_x = Text("X", font_size=60, color=INVERSE_RED, weight=BOLD)
        red_x.move_to(RIGHT * 3.5 + DOWN * 2.2)
        x_label = label_text("L2 is fooled by scale", color=INVERSE_RED)
        x_label.next_to(red_x, RIGHT, buff=0.3)
        self.play(Write(red_x), Write(x_label))
        self.wait(1.0)

        self.play(
            FadeOut(axes),
            FadeOut(vec_y),
            FadeOut(vec_d),
            FadeOut(vec_gy),
            FadeOut(y_label),
            FadeOut(d_label),
            FadeOut(gamma_label),
            FadeOut(l2_eq),
            FadeOut(l2_problem),
            FadeOut(explain_l2),
            FadeOut(explain_l2b),
            FadeOut(red_x),
            FadeOut(x_label),
            FadeOut(subtitle),
        )

    def _show_cosine_advantage(self, title: Mobject) -> None:
        """Show cosine similarity is scale-invariant."""
        subtitle = body_text(
            "Cosine Similarity (the right way)", color=FORWARD_GREEN
        )
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(subtitle))

        # Cosine formula
        cos_eq = MathTex(
            r"\cos(\mathbf{y}, \mathbf{d}) = "
            r"\frac{\mathbf{y}^T \mathbf{d}}"
            r"{\|\mathbf{y}\|\;\|\mathbf{d}\|}",
            font_size=EQ_SIZE,
            color=FORWARD_GREEN,
        )
        cos_eq.move_to(ORIGIN + UP * 1.0)
        self.play(Write(cos_eq))
        self.wait(0.8)

        # Scale invariance
        scale_eq = MathTex(
            r"\cos(\gamma\mathbf{y}, \mathbf{d})"
            r" = \cos(\mathbf{y}, \mathbf{d})",
            font_size=EQ_SIZE,
            color=FORWARD_GREEN,
        )
        scale_eq.next_to(cos_eq, DOWN, buff=0.6)

        because = label_text(
            "gamma cancels in numerator and denominator!",
            color=COSINE_ORANGE,
        )
        because.next_to(scale_eq, DOWN, buff=0.3)

        self.play(Write(scale_eq))
        self.play(Write(because))
        self.wait(1.0)

        # Vectors showing angle
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 3, 1],
            x_length=3.5,
            y_length=2.5,
            axis_config={"include_tip": False, "stroke_width": 2},
        )
        axes.move_to(LEFT * 3.5 + DOWN * 1.5)

        vec_y = Arrow(
            axes.c2p(0, 0),
            axes.c2p(2, 2.5),
            color=SIGNAL_BLUE,
            buff=0,
            stroke_width=3,
        )
        vec_d = Arrow(
            axes.c2p(0, 0),
            axes.c2p(3, 1.5),
            color=MATCH_GOLD,
            buff=0,
            stroke_width=3,
        )

        # Angle arc between them
        angle_arc = Angle(
            vec_d, vec_y, radius=0.8, color=FORWARD_GREEN, stroke_width=3
        )
        theta_label = MathTex(
            r"\theta", font_size=BODY_SIZE, color=FORWARD_GREEN
        )
        theta_label.move_to(
            axes.c2p(0, 0) + RIGHT * 1.1 + UP * 0.6
        )

        self.play(Create(axes), GrowArrow(vec_y), GrowArrow(vec_d))
        self.play(Create(angle_arc), Write(theta_label))
        self.wait(0.5)

        angle_note = label_text(
            "Only the angle matters, not the length",
            color=FORWARD_GREEN,
        )
        angle_note.move_to(RIGHT * 2.5 + DOWN * 1.5)
        self.play(Write(angle_note))
        self.wait(0.5)

        # Green check
        green_check = Text(
            "Cosine compares SHAPE, not magnitude",
            font_size=LABEL_SIZE,
            color=FORWARD_GREEN,
            weight=BOLD,
        )
        green_check.move_to(RIGHT * 2.5 + DOWN * 2.3)
        self.play(Write(green_check))
        self.wait(0.5)

        practical = label_text(
            "S0 normalization is noisy -- cosine doesn't care",
            color=WHITE,
        )
        practical.to_edge(DOWN, buff=0.5)
        self.play(Write(practical))
        self.wait(1.5)

        self.play(
            FadeOut(subtitle),
            FadeOut(cos_eq),
            FadeOut(scale_eq),
            FadeOut(because),
            FadeOut(axes),
            FadeOut(vec_y),
            FadeOut(vec_d),
            FadeOut(angle_arc),
            FadeOut(theta_label),
            FadeOut(angle_note),
            FadeOut(green_check),
            FadeOut(practical),
        )

    def _show_matching_pipeline(self, title: Mobject) -> None:
        """Show the full matching pipeline from voxel to winner."""
        subtitle = body_text("The Matching Pipeline", color=MATCH_GOLD)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(subtitle))

        # Step 1: Measured signal
        voxel_rect = RoundedRectangle(
            corner_radius=0.12,
            width=2.0,
            height=1.0,
            color=SIGNAL_BLUE,
            stroke_width=2,
            fill_color=SIGNAL_BLUE,
            fill_opacity=0.15,
        )
        voxel_rect.move_to(LEFT * 5.0 + DOWN * 0.5)
        voxel_label = Text(
            "Measured\nsignal", font_size=16, color=SIGNAL_BLUE
        ).move_to(voxel_rect)
        self.play(FadeIn(voxel_rect), Write(voxel_label))

        # Step 2: Compute cosine similarity to all 500K
        arrow1 = Arrow(
            voxel_rect.get_right(),
            voxel_rect.get_right() + RIGHT * 1.3,
            color=WHITE,
            buff=0.1,
            stroke_width=2,
        )
        cos_box = RoundedRectangle(
            corner_radius=0.12,
            width=2.8,
            height=1.0,
            color=COSINE_ORANGE,
            stroke_width=2,
            fill_color=COSINE_ORANGE,
            fill_opacity=0.15,
        )
        cos_box.next_to(arrow1, RIGHT, buff=0.1)
        cos_label = Text(
            "Cosine similarity\nvs 500K entries",
            font_size=14,
            color=COSINE_ORANGE,
        ).move_to(cos_box)

        self.play(GrowArrow(arrow1), FadeIn(cos_box), Write(cos_label))

        # Step 3: Similarity scores
        arrow2 = Arrow(
            cos_box.get_right(),
            cos_box.get_right() + RIGHT * 1.0,
            color=WHITE,
            buff=0.1,
            stroke_width=2,
        )
        scores = VGroup()
        score_vals = [0.98, 0.95, 0.92, 0.87, 0.43, 0.21]
        for i, val in enumerate(score_vals):
            color = ManimColor.from_hex(DIMMED).interpolate(
                ManimColor.from_hex(FORWARD_GREEN), val
            )
            score_text = Text(
                f"{val:.2f}", font_size=14, color=color
            )
            scores.add(score_text)
        scores.arrange(DOWN, buff=0.08)
        scores.next_to(arrow2, RIGHT, buff=0.15)

        self.play(GrowArrow(arrow2))
        self.play(
            LaggedStart(*[Write(s) for s in scores], lag_ratio=0.1),
            run_time=1.0,
        )
        self.wait(0.5)

        # Step 4: Top K=50 + complexity penalty
        rank_label = label_text("Top K=50", color=FORWARD_GREEN)
        rank_label.next_to(scores, DOWN, buff=0.3)
        self.play(Write(rank_label))

        # Complexity penalty equation
        penalty_eq = MathTex(
            r"\hat{i} = \arg\max_i \Big["
            r"\cos(\mathbf{y}, \mathbf{d}_i)"
            r"- \alpha \cdot n_{\text{fibers}}\Big]",
            font_size=SMALL_EQ,
            color=MATCH_GOLD,
        )
        penalty_eq.move_to(ORIGIN + DOWN * 2.3)
        self.play(Write(penalty_eq))
        self.wait(0.5)

        alpha_note = label_text(
            "alpha discourages overly complex (3-fiber) solutions",
            color=COSINE_ORANGE,
        )
        alpha_note.next_to(penalty_eq, DOWN, buff=0.25)
        self.play(Write(alpha_note))
        self.wait(0.8)

        # Winner highlight
        winner_box = SurroundingRectangle(
            scores[0], color=MATCH_GOLD, buff=0.08, stroke_width=3
        )
        winner_label = label_text("WINNER", color=MATCH_GOLD)
        winner_label.next_to(winner_box, RIGHT, buff=0.2)
        self.play(Create(winner_box), Write(winner_label))
        self.wait(1.5)

        self.play(
            FadeOut(subtitle),
            FadeOut(voxel_rect),
            FadeOut(voxel_label),
            FadeOut(arrow1),
            FadeOut(cos_box),
            FadeOut(cos_label),
            FadeOut(arrow2),
            FadeOut(scores),
            FadeOut(rank_label),
            FadeOut(penalty_eq),
            FadeOut(alpha_note),
            FadeOut(winner_box),
            FadeOut(winner_label),
        )

    def _show_visual_proof(self, title: Mobject) -> None:
        """Visual proof: same shape, different magnitudes."""
        subtitle = body_text("Visual Proof", color=HIGHLIGHT)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(subtitle))

        # Two signal profiles: same shape, different magnitudes
        rng = np.random.default_rng(42)
        n_pts = 16
        x_vals = np.linspace(-3, 3, n_pts)
        base_y = 0.5 + 0.3 * np.sin(x_vals * 1.2) + 0.2 * np.cos(x_vals * 0.8)

        # Profile 1: original magnitude
        profile1_pts = [
            np.array([x, y, 0]) for x, y in zip(x_vals, base_y)
        ]
        profile1 = VMobject(color=SIGNAL_BLUE, stroke_width=3)
        profile1.set_points_smoothly(profile1_pts)
        profile1.shift(UP * 0.5)

        # Profile 2: scaled down (same shape)
        scaled_y = base_y * 0.4
        profile2_pts = [
            np.array([x, y, 0]) for x, y in zip(x_vals, scaled_y)
        ]
        profile2 = VMobject(color=COSINE_ORANGE, stroke_width=3)
        profile2.set_points_smoothly(profile2_pts)
        profile2.shift(UP * 0.5)

        label1 = label_text("Signal A (strong)", color=SIGNAL_BLUE)
        label1.next_to(profile1, UP, buff=0.3).align_to(profile1, LEFT)
        label2 = label_text("Signal B (weak, same shape)", color=COSINE_ORANGE)
        label2.next_to(profile2, DOWN, buff=0.3).align_to(profile2, LEFT)

        self.play(Create(profile1), Write(label1))
        self.play(Create(profile2), Write(label2))
        self.wait(0.8)

        # L2 verdict
        l2_verdict = VGroup(
            Text("L2 says:", font_size=LABEL_SIZE, color=INVERSE_RED),
            Text('"Very different"', font_size=LABEL_SIZE, color=INVERSE_RED, slant=ITALIC),
        )
        l2_verdict.arrange(RIGHT, buff=0.2)
        l2_verdict.move_to(RIGHT * 3 + DOWN * 1.5)
        l2_icon = Text("X", font_size=36, color=INVERSE_RED, weight=BOLD)
        l2_icon.next_to(l2_verdict, LEFT, buff=0.3)

        self.play(Write(l2_verdict), Write(l2_icon))
        self.wait(0.5)

        # Cosine verdict
        cos_verdict = VGroup(
            Text("Cosine says:", font_size=LABEL_SIZE, color=FORWARD_GREEN),
            Text('"Identical"', font_size=LABEL_SIZE, color=FORWARD_GREEN, slant=ITALIC),
        )
        cos_verdict.arrange(RIGHT, buff=0.2)
        cos_verdict.next_to(l2_verdict, DOWN, buff=0.4)
        cos_icon = MathTex(r"\checkmark", font_size=36, color=FORWARD_GREEN)
        cos_icon.next_to(cos_verdict, LEFT, buff=0.3)

        self.play(Write(cos_verdict), Write(cos_icon))
        self.wait(0.5)

        # Right answer
        right_answer = body_text(
            "The right answer: same microstructure",
            color=FORWARD_GREEN,
        ).scale(0.8)
        right_answer.move_to(ORIGIN + DOWN * 2.8)
        right_answer_box = SurroundingRectangle(
            right_answer, color=FORWARD_GREEN, buff=0.15
        )
        self.play(Write(right_answer), Create(right_answer_box))
        self.wait(1.0)

        # Fade verdict, show bottom note
        self.play(
            FadeOut(l2_verdict),
            FadeOut(cos_verdict),
            FadeOut(l2_icon),
            FadeOut(cos_icon),
            FadeOut(right_answer),
            FadeOut(right_answer_box),
            FadeOut(profile1),
            FadeOut(profile2),
            FadeOut(label1),
            FadeOut(label2),
            FadeOut(subtitle),
        )

        note = bottom_note("Shape matters, not scale")
        self.play(Write(note))
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # -- Utility: bar chart builder ----------------------------------------
    def _make_bar_chart(
        self,
        heights: np.ndarray,
        center: np.ndarray,
        color: str,
        label_str: str,
    ) -> VGroup:
        """Create a simple bar chart with a label.

        Parameters
        ----------
        heights : np.ndarray
            Bar heights (0-1 range).
        center : np.ndarray
            Center position for the chart.
        color : str
            Bar color.
        label_str : str
            Label text below the chart.

        Returns
        -------
        VGroup
            The bar chart group.
        """
        bars = VGroup()
        bar_w = 0.2
        total_w = len(heights) * (bar_w + 0.05)
        start_x = center[0] - total_w / 2

        for i, h in enumerate(heights):
            bar = Rectangle(
                width=bar_w,
                height=max(h * 1.5, 0.05),
                color=color,
                fill_color=color,
                fill_opacity=0.7,
                stroke_width=1,
            )
            bar.move_to(
                np.array([start_x + i * (bar_w + 0.05), center[1], 0])
            )
            bar.align_to(np.array([0, center[1] - 0.8, 0]), DOWN)
            bars.add(bar)

        label = Text(label_str, font_size=LABEL_SIZE, color=color)
        label.next_to(bars, UP, buff=0.25)

        return VGroup(bars, label)
