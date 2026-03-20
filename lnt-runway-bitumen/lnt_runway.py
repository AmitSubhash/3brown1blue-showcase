"""
Performance Grade Bitumen for Airport Runways
Complete Manim animation - 9 scenes
Render: manim -pql bitumen_video.py SceneName  (dev)
        manim -qh bitumen_video.py SceneName   (final)
        manim -qh bitumen_video.py -a           (all scenes)
"""

from manim import *
import numpy as np

# ============================================================
# STYLE SECTION: Colors, sizes, helpers
# ============================================================

# -- Semantic Colors --
ASPHALT_BLACK = "#2C2C2C"
POLYMER_BLUE = "#4A90D9"
HEAT_RED = "#E74C3C"
COLD_CYAN = "#00BCD4"
STRESS_YELLOW = "#F1C40F"
SUCCESS_GREEN = "#2ECC71"
FUEL_ORANGE = "#E67E22"
CONTEXT_GRAY = "#7F8C8D"

# -- Font Sizes --
TITLE_SIZE = 40
HEADING_SIZE = 32
BODY_SIZE = 26
LABEL_SIZE = 20
EQ_SIZE = 32
SMALL_EQ = 24

# -- Layout Constants --
TITLE_Y = 3.0
BOTTOM_Y = -3.2
SAFE_WIDTH = 12.0


def section_title(text: str, color=WHITE) -> Text:
    """Create a section title positioned at the top of the frame."""
    return Text(text, font_size=TITLE_SIZE, color=color, weight=BOLD).to_edge(UP, buff=0.5)


def safe_text(text: str, font_size: int = BODY_SIZE, color=WHITE, max_width: float = 12.0) -> Text:
    """Create text that auto-scales to fit within max_width."""
    t = Text(text, font_size=font_size, color=color)
    if t.width > max_width:
        t.scale_to_fit_width(max_width)
    return t


def bottom_note(text: str, color=YELLOW) -> Text:
    """Create a bottom caption in the reserved caption zone."""
    t = Text(text, font_size=LABEL_SIZE, color=color)
    if t.width > SAFE_WIDTH:
        t.scale_to_fit_width(SAFE_WIDTH)
    return t.to_edge(DOWN, buff=0.5)


def fade_all(scene: Scene, *mobjects: Mobject) -> None:
    """Fade out all given mobjects in parallel."""
    valid = [m for m in mobjects if m is not None]
    if valid:
        scene.play(*[FadeOut(m) for m in valid])


def temperature_number_line(
    x_range: tuple = (-30, 80, 10),
    length: float = 10.0,
    position=UP * 2.5,
) -> tuple:
    """
    Create the persistent temperature number line used across scenes.

    Returns
    -------
    tuple
        (NumberLine, label_group) where label_group includes the axis labels.
    """
    nline = NumberLine(
        x_range=list(x_range),
        length=length,
        include_numbers=True,
        numbers_to_include=list(range(x_range[0], x_range[1] + 1, 20)),
        font_size=18,
        color=WHITE,
        decimal_number_config={"num_decimal_places": 0},
    ).move_to(position)
    unit_label = Text("°C", font_size=16, color=WHITE).next_to(nline, RIGHT, buff=0.2)
    return nline, unit_label


def runway_cross_section(
    layer_data: list | None = None,
    total_width: float = 3.0,
    position=ORIGIN,
) -> VGroup:
    """
    Build a stacked pavement cross-section diagram.

    Parameters
    ----------
    layer_data : list of (name, thickness_mm, color)
    """
    if layer_data is None:
        layer_data = [
            ("GSB", 230, GRAY),
            ("WMM", 250, "#8B7355"),
            ("DBM", 150, ASPHALT_BLACK),
            ("BC", 40, "#1a1a1a"),
        ]
    # Normalize heights so total is ~4 Manim units
    total_mm = sum(t for _, t, _ in layer_data)
    scale_factor = 4.0 / total_mm

    layers = VGroup()
    labels = VGroup()
    current_y = 0.0
    for name, thickness_mm, color in layer_data:
        h = thickness_mm * scale_factor
        rect = Rectangle(
            width=total_width,
            height=h,
            fill_color=color,
            fill_opacity=0.85,
            stroke_color=WHITE,
            stroke_width=1.5,
        )
        rect.move_to(UP * (current_y + h / 2))
        lbl = Text(f"{name} {thickness_mm}mm", font_size=14, color=WHITE)
        lbl.move_to(rect.get_center())
        layers.add(rect)
        labels.add(lbl)
        current_y += h

    group = VGroup(layers, labels).move_to(position)
    return group


def polymer_chain(
    n_points: int = 8,
    amplitude: float = 0.3,
    length: float = 2.5,
    color=ASPHALT_BLACK,
    stroke_width: float = 3,
) -> VMobject:
    """Create a wiggly polymer/bitumen chain as a smooth curve."""
    points = []
    for i in range(n_points):
        x = (i / (n_points - 1)) * length - length / 2
        y = amplitude * np.sin(i * 1.8) * ((-1) ** i)
        points.append([x, y, 0])
    chain = VMobject(color=color, stroke_width=stroke_width)
    chain.set_points_smoothly([np.array(p) for p in points])
    return chain


# ============================================================
# SCENE 1: RunwayForces (~45s)
# ============================================================
class RunwayForces(Scene):
    """Aircraft landing forces and contact pressure comparison."""

    def construct(self) -> None:
        # -- Title --
        title = section_title("Why Runway Asphalt is Different")
        self.play(Write(title))
        self.wait(0.5)

        # -- Runway (top-down view) --
        runway = Rectangle(
            width=10, height=2.5,
            fill_color=ASPHALT_BLACK, fill_opacity=0.9,
            stroke_color=WHITE, stroke_width=1,
        ).shift(DOWN * 0.3)
        # Dashed center line
        dashes = VGroup(*[
            Line(LEFT * (4.5 - i * 1.2), LEFT * (4.5 - i * 1.2) + RIGHT * 0.6,
                 color=STRESS_YELLOW, stroke_width=2)
            for i in range(8)
        ]).move_to(runway.get_center())
        runway_group = VGroup(runway, dashes)
        self.play(FadeIn(runway_group))
        self.wait(0.3)

        # -- Aircraft silhouette (simplified triangle + wings) --
        fuselage = Polygon(
            [-0.8, 0.6, 0], [0.8, 0.6, 0], [0, -0.8, 0],
            fill_color=GRAY, fill_opacity=0.7, stroke_color=WHITE, stroke_width=1,
        )
        left_wing = Line([-0.4, 0.2, 0], [-1.5, 0.5, 0], color=GRAY, stroke_width=3)
        right_wing = Line([0.4, 0.2, 0], [1.5, 0.5, 0], color=GRAY, stroke_width=3)
        aircraft = VGroup(fuselage, left_wing, right_wing)
        aircraft.scale(0.8).move_to(UP * 3)

        # Animate landing
        self.play(aircraft.animate.move_to(runway.get_center() + UP * 0.3), run_time=1.5)

        # -- Stress rings on touchdown --
        rings = VGroup(*[
            Circle(radius=r, color=STRESS_YELLOW, stroke_width=2, stroke_opacity=1 - r / 3)
            for r in [0.4, 0.8, 1.3, 1.8]
        ]).move_to(runway.get_center())
        self.play(
            LaggedStart(*[Create(r) for r in rings], lag_ratio=0.3),
            run_time=1.5,
        )
        self.wait(0.3)

        # -- Fade title and aircraft for pressure comparison --
        self.play(FadeOut(title), FadeOut(aircraft), FadeOut(rings))

        # -- Pressure comparison --
        pressure_title = safe_text("Contact Pressure Comparison", font_size=HEADING_SIZE)
        pressure_title.to_edge(UP, buff=0.5)
        self.play(Write(pressure_title))

        # Pressure equation
        eq = MathTex(
            r"P = \frac{F}{A}",
            font_size=EQ_SIZE, color=WHITE,
        ).shift(UP * 1.5)
        self.play(Write(eq))
        self.wait(0.5)

        # Car pressure bar
        car_label = safe_text("Car", font_size=LABEL_SIZE, color=CONTEXT_GRAY)
        car_bar = Rectangle(
            width=0.8, height=0.5,
            fill_color=CONTEXT_GRAY, fill_opacity=0.6,
            stroke_width=0,
        )
        car_value = safe_text("~0.2 MPa", font_size=LABEL_SIZE, color=CONTEXT_GRAY)
        car_group = VGroup(car_label, car_bar, car_value).arrange(DOWN, buff=0.15)
        car_group.shift(LEFT * 2.5 + DOWN * 1.2)

        # Aircraft pressure bar
        plane_label = safe_text("Boeing 777", font_size=LABEL_SIZE, color=STRESS_YELLOW)
        plane_bar = Rectangle(
            width=0.8, height=3.0,
            fill_color=STRESS_YELLOW, fill_opacity=0.8,
            stroke_width=0,
        )
        plane_value = safe_text("~1.5 MPa", font_size=LABEL_SIZE, color=STRESS_YELLOW)
        plane_group = VGroup(plane_label, plane_bar, plane_value).arrange(DOWN, buff=0.15)
        plane_group.shift(RIGHT * 2.5 + DOWN * 0.5)

        self.play(
            FadeIn(car_label), GrowFromEdge(car_bar, DOWN), FadeIn(car_value),
        )
        self.play(
            FadeIn(plane_label), GrowFromEdge(plane_bar, DOWN), FadeIn(plane_value),
        )

        # Ratio indicator
        ratio = safe_text("7.5×", font_size=42, color=STRESS_YELLOW)
        ratio.next_to(plane_bar, RIGHT, buff=0.5)
        self.play(Write(ratio))
        self.play(
            ratio.animate.scale(1.3),
            rate_func=there_and_back,
            run_time=0.8,
        )

        note = bottom_note(
            "Pressure is only half the problem -- temperature is the other half."
        )
        self.play(Write(note))
        self.wait(2)

        # Cleanup: keep runway for conceptual continuity, fade the rest
        fade_all(
            self, pressure_title, eq,
            car_label, car_bar, car_value,
            plane_label, plane_bar, plane_value,
            ratio, note, runway_group,
        )


# ============================================================
# SCENE 2: TemperatureProblem (~50s)
# ============================================================
class TemperatureProblem(Scene):
    """Temperature extremes: cracking vs rutting, and PG naming."""

    def construct(self) -> None:
        title = section_title("The Temperature Problem")
        self.play(Write(title))
        self.wait(0.3)

        # -- Temperature number line --
        nline, unit_lbl = temperature_number_line(
            x_range=(-30, 80, 10), length=11, position=UP * 1.8
        )
        self.play(Create(nline), FadeIn(unit_lbl))
        self.wait(0.3)

        # -- Cold end: cracking demo --
        cold_pos = nline.n2p(-22)
        cold_dot = Dot(cold_pos, color=COLD_CYAN, radius=0.12)
        cold_label = safe_text("-22°C", font_size=LABEL_SIZE, color=COLD_CYAN)
        cold_label.next_to(cold_dot, DOWN, buff=0.2)

        # Pavement block that cracks
        pave_cold = Rectangle(
            width=2, height=0.8,
            fill_color=ASPHALT_BLACK, fill_opacity=0.9,
            stroke_color=WHITE, stroke_width=1,
        ).shift(DOWN * 1.0 + LEFT * 3.5)
        cold_heading = safe_text("Cold Failure", font_size=LABEL_SIZE, color=COLD_CYAN)
        cold_heading.next_to(pave_cold, UP, buff=0.2)

        self.play(FadeIn(cold_dot), Write(cold_label))
        self.play(FadeIn(pave_cold), Write(cold_heading))

        # Crack animation: jagged line splits the block
        crack_points = [
            pave_cold.get_top() + DOWN * 0.05,
            pave_cold.get_center() + LEFT * 0.15 + UP * 0.1,
            pave_cold.get_center() + RIGHT * 0.1 + DOWN * 0.05,
            pave_cold.get_bottom() + UP * 0.05,
        ]
        crack = VMobject(color=COLD_CYAN, stroke_width=3)
        crack.set_points_as_corners(crack_points)
        self.play(Create(crack), run_time=0.8)
        crack_label = safe_text("Thermal Cracking", font_size=16, color=COLD_CYAN)
        crack_label.next_to(pave_cold, DOWN, buff=0.2)
        self.play(FadeIn(crack_label))

        # -- Hot end: rutting demo --
        hot_pos = nline.n2p(76)
        hot_dot = Dot(hot_pos, color=HEAT_RED, radius=0.12)
        hot_label = safe_text("+76°C", font_size=LABEL_SIZE, color=HEAT_RED)
        hot_label.next_to(hot_dot, DOWN, buff=0.2)

        pave_hot = Rectangle(
            width=2, height=0.8,
            fill_color=ASPHALT_BLACK, fill_opacity=0.9,
            stroke_color=WHITE, stroke_width=1,
        ).shift(DOWN * 1.0 + RIGHT * 3.5)
        hot_heading = safe_text("Hot Failure", font_size=LABEL_SIZE, color=HEAT_RED)
        hot_heading.next_to(pave_hot, UP, buff=0.2)

        self.play(FadeIn(hot_dot), Write(hot_label))
        self.play(FadeIn(pave_hot), Write(hot_heading))

        # Rut animation: top edge deforms into concave curve
        rut_curve = VMobject(color=HEAT_RED, stroke_width=3, fill_opacity=0)
        left_pt = pave_hot.get_corner(UL)
        right_pt = pave_hot.get_corner(UR)
        mid_pt = (left_pt + right_pt) / 2 + DOWN * 0.3
        rut_curve.set_points_smoothly([left_pt, mid_pt, right_pt])
        self.play(Create(rut_curve), run_time=0.8)
        rut_label = safe_text("Rutting", font_size=16, color=HEAT_RED)
        rut_label.next_to(pave_hot, DOWN, buff=0.2)
        self.play(FadeIn(rut_label))
        self.wait(0.5)

        # -- Usable range brackets --
        # Conventional: narrow range
        conv_left = nline.n2p(0)
        conv_right = nline.n2p(40)
        conv_bracket = Line(conv_left + DOWN * 0.4, conv_right + DOWN * 0.4,
                            color=CONTEXT_GRAY, stroke_width=4, stroke_opacity=0.6)
        conv_text = safe_text("Conventional Range", font_size=14, color=CONTEXT_GRAY)
        conv_text.next_to(conv_bracket, DOWN, buff=0.1)

        # PG: wide range
        pg_left = nline.n2p(-22)
        pg_right = nline.n2p(76)
        pg_bracket = Line(pg_left + DOWN * 0.8, pg_right + DOWN * 0.8,
                          color=SUCCESS_GREEN, stroke_width=5)
        pg_text = safe_text("PG 76-22 Range", font_size=16, color=SUCCESS_GREEN)
        pg_text.next_to(pg_bracket, DOWN, buff=0.1)

        self.play(FadeOut(title))
        self.play(Create(conv_bracket), Write(conv_text))
        self.wait(0.5)
        self.play(Create(pg_bracket), Write(pg_text))
        self.wait(0.5)

        # -- PG Grade label with color-coded numbers --
        pg_eq = MathTex(
            r"\text{PG }", r"76", r"\text{-}", r"22",
            font_size=48,
        )
        pg_eq[1].set_color(HEAT_RED)
        pg_eq[3].set_color(COLD_CYAN)
        pg_eq.shift(DOWN * 2.8)

        self.play(Write(pg_eq))

        # Arrows from numbers to positions on the line
        arrow_hot = Arrow(
            pg_eq[1].get_top(), hot_pos + DOWN * 1.0,
            color=HEAT_RED, stroke_width=2, max_tip_length_to_length_ratio=0.15,
        )
        arrow_cold = Arrow(
            pg_eq[3].get_top(), cold_pos + DOWN * 1.0,
            color=COLD_CYAN, stroke_width=2, max_tip_length_to_length_ratio=0.15,
        )
        self.play(GrowArrow(arrow_hot), GrowArrow(arrow_cold))
        self.wait(1)

        note = bottom_note(
            "PG 76-22: won't rut above 76°C, won't crack below -22°C"
        )
        # Move note to avoid overlap with pg_eq
        note.shift(DOWN * 0.2)
        self.play(FadeOut(pg_eq), FadeOut(arrow_hot), FadeOut(arrow_cold))
        note.to_edge(DOWN, buff=0.3)
        self.play(Write(note))
        self.wait(2)

        # Cleanup
        all_mobs = [
            nline, unit_lbl, cold_dot, cold_label,
            pave_cold, cold_heading, crack, crack_label,
            hot_dot, hot_label, pave_hot, hot_heading,
            rut_curve, rut_label,
            conv_bracket, conv_text, pg_bracket, pg_text, note,
        ]
        fade_all(self, *all_mobs)


# ============================================================
# SCENE 3: WhatIsBitumen (~40s)
# ============================================================
class WhatIsBitumen(Scene):
    """Dual panel: aggregate view and molecular view of bitumen."""

    def construct(self) -> None:
        title = section_title("What is Bitumen?")
        self.play(Write(title))
        self.wait(0.3)

        divider = Line(UP * 2.2, DOWN * 2.5, color=WHITE, stroke_width=1, stroke_opacity=0.3)
        self.play(Create(divider))

        # ============ LEFT PANEL: Aggregate view ============
        left_title = safe_text("Pavement Structure", font_size=LABEL_SIZE, color=POLYMER_BLUE)
        left_title.move_to(LEFT * 3.5 + UP * 2.0)
        self.play(Write(left_title))

        # Aggregate particles (irregular polygons)
        np.random.seed(42)
        aggregates = VGroup()
        for _ in range(12):
            n_sides = np.random.randint(5, 8)
            poly = RegularPolygon(
                n=n_sides,
                fill_color=GRAY,
                fill_opacity=0.7,
                stroke_color=WHITE,
                stroke_width=1,
            )
            s = np.random.uniform(0.25, 0.5)
            poly.scale(s)
            poly.rotate(np.random.uniform(0, TAU))
            poly.move_to([
                np.random.uniform(-5.0, -2.0),
                np.random.uniform(-1.8, 1.0),
                0,
            ])
            aggregates.add(poly)

        # Dark fill between aggregates (bitumen)
        bitumen_bg = Rectangle(
            width=3.5, height=3.0,
            fill_color=ASPHALT_BLACK, fill_opacity=0.8,
            stroke_width=0,
        ).move_to(LEFT * 3.5 + DOWN * 0.3)

        self.play(FadeIn(bitumen_bg))
        self.play(LaggedStart(*[FadeIn(a) for a in aggregates], lag_ratio=0.08))

        binder_label = safe_text("Bitumen = the glue", font_size=18, color=STRESS_YELLOW)
        binder_label.next_to(bitumen_bg, DOWN, buff=0.3)
        arrow_to_gap = Arrow(
            binder_label.get_top(),
            LEFT * 3.5 + DOWN * 0.3,
            color=STRESS_YELLOW, stroke_width=2,
            max_tip_length_to_length_ratio=0.2,
        )
        self.play(Write(binder_label), GrowArrow(arrow_to_gap))

        # ============ RIGHT PANEL: Molecular view ============
        right_title = safe_text("Molecular View", font_size=LABEL_SIZE, color=POLYMER_BLUE)
        right_title.move_to(RIGHT * 3.5 + UP * 2.0)
        self.play(Write(right_title))

        # Create bitumen chains (short, wiggly)
        chains = VGroup()
        for i in range(6):
            c = polymer_chain(
                n_points=6,
                amplitude=0.2,
                length=1.8,
                color=ASPHALT_BLACK if i % 2 == 0 else "#4a4a4a",
                stroke_width=3,
            )
            c.move_to([
                np.random.uniform(2.0, 5.0),
                np.random.uniform(-1.5, 1.0),
                0,
            ])
            c.rotate(np.random.uniform(-0.5, 0.5))
            chains.add(c)

        self.play(LaggedStart(*[Create(c) for c in chains], lag_ratio=0.15))
        self.wait(0.5)

        # -- Heat test: chains slide apart --
        heat_wash = Rectangle(
            width=4.0, height=3.5,
            fill_color=HEAT_RED, fill_opacity=0.15,
            stroke_width=0,
        ).move_to(RIGHT * 3.5 + DOWN * 0.2)
        heat_label = safe_text("HEAT", font_size=20, color=HEAT_RED)
        heat_label.move_to(RIGHT * 3.5 + UP * 1.5)

        self.play(FadeOut(title))
        self.play(FadeIn(heat_wash), Write(heat_label))
        self.play(
            *[c.animate.shift(
                RIGHT * np.random.uniform(0.1, 0.3) + UP * np.random.uniform(-0.2, 0.2)
            ) for c in chains],
            run_time=1.5,
        )
        rut_note = safe_text("Chains slide → RUTTING", font_size=16, color=HEAT_RED)
        rut_note.next_to(heat_wash, DOWN, buff=0.2)
        self.play(Write(rut_note))
        self.wait(0.8)

        # -- Cold test: chains lock, crack --
        self.play(FadeOut(heat_wash), FadeOut(heat_label), FadeOut(rut_note))

        cold_wash = Rectangle(
            width=4.0, height=3.5,
            fill_color=COLD_CYAN, fill_opacity=0.15,
            stroke_width=0,
        ).move_to(RIGHT * 3.5 + DOWN * 0.2)
        cold_label = safe_text("COLD", font_size=20, color=COLD_CYAN)
        cold_label.move_to(RIGHT * 3.5 + UP * 1.5)

        self.play(FadeIn(cold_wash), Write(cold_label))
        # Chains become rigid (straighten slightly)
        self.play(
            *[c.animate.stretch(1.1, 0) for c in chains],
            run_time=1.0,
        )
        # Crack through the chains
        crack = Line(
            RIGHT * 2 + UP * 1.0, RIGHT * 5 + DOWN * 1.5,
            color=COLD_CYAN, stroke_width=4,
        )
        self.play(Create(crack), run_time=0.6)
        crack_note = safe_text("Chains lock → CRACKING", font_size=16, color=COLD_CYAN)
        crack_note.next_to(cold_wash, DOWN, buff=0.2)
        self.play(Write(crack_note))
        self.wait(0.8)

        note = bottom_note("The molecule itself is the problem. We need to change it.")
        self.play(FadeOut(crack_note))
        self.play(Write(note))
        self.wait(2)

        # Cleanup
        fade_all(
            self, divider, left_title, bitumen_bg, aggregates,
            binder_label, arrow_to_gap, right_title, chains,
            cold_wash, cold_label, crack, note,
        )


# ============================================================
# SCENE 4: PolymerModification (~60s)
# ============================================================
class PolymerModification(Scene):
    """How SBS polymers create an elastic network in bitumen."""

    def construct(self) -> None:
        title = section_title("Polymer Modification: Engineering the Network")
        self.play(Write(title))
        self.wait(0.3)

        # -- Bitumen chains (reused motif, now centered) --
        np.random.seed(7)
        bitumen_chains = VGroup()
        for i in range(8):
            c = polymer_chain(
                n_points=6, amplitude=0.2, length=1.5,
                color="#4a4a4a", stroke_width=2.5,
            )
            c.move_to([
                np.random.uniform(-2.5, 2.5),
                np.random.uniform(-1.5, 1.0),
                0,
            ])
            c.rotate(np.random.uniform(-0.6, 0.6))
            bitumen_chains.add(c)

        bitumen_label = safe_text("Bitumen molecules", font_size=LABEL_SIZE, color=CONTEXT_GRAY)
        bitumen_label.next_to(bitumen_chains, UP, buff=0.3)

        self.play(FadeOut(title))
        title2 = section_title("Polymer Modification")
        self.play(Write(title2))
        self.play(
            LaggedStart(*[Create(c) for c in bitumen_chains], lag_ratio=0.1),
            Write(bitumen_label),
        )
        self.wait(0.5)

        # -- Introduce SBS polymer chains --
        sbs_chains = VGroup()
        for i in range(4):
            c = polymer_chain(
                n_points=10, amplitude=0.35, length=3.5,
                color=POLYMER_BLUE, stroke_width=4,
            )
            c.move_to([
                np.random.uniform(-2.0, 2.0),
                np.random.uniform(-1.2, 0.8),
                0,
            ])
            c.rotate(np.random.uniform(-0.4, 0.4))
            sbs_chains.add(c)

        sbs_label = safe_text("SBS Polymer Network", font_size=LABEL_SIZE, color=POLYMER_BLUE)
        sbs_label.next_to(bitumen_chains, DOWN, buff=1.5)

        self.play(FadeOut(bitumen_label))
        self.play(
            LaggedStart(*[Create(c) for c in sbs_chains], lag_ratio=0.2),
            run_time=2,
        )
        self.play(Write(sbs_label))
        self.wait(0.5)

        # -- Heat test with polymer: chains stretch but hold --
        heat_box = Rectangle(
            width=8, height=4, fill_color=HEAT_RED, fill_opacity=0.08, stroke_width=0,
        ).shift(DOWN * 0.3)
        heat_text = safe_text("Applying Heat...", font_size=20, color=HEAT_RED)
        heat_text.to_edge(UP, buff=0.5)

        self.play(FadeOut(title2))
        self.play(FadeIn(heat_box), Write(heat_text))

        # Bitumen tries to slide but polymer holds
        self.play(
            *[c.animate.shift(RIGHT * np.random.uniform(0.05, 0.15))
              for c in bitumen_chains],
            *[c.animate.stretch(1.15, 0) for c in sbs_chains],  # elastic stretch
            run_time=1.5,
        )
        hold_text = safe_text("Polymer chains stretch but hold!", font_size=18, color=SUCCESS_GREEN)
        hold_text.next_to(sbs_label, DOWN, buff=0.3)
        self.play(Write(hold_text))
        self.wait(0.8)

        self.play(FadeOut(heat_box), FadeOut(heat_text), FadeOut(hold_text))

        # -- Cold test with polymer: chains stay flexible --
        cold_box = Rectangle(
            width=8, height=4, fill_color=COLD_CYAN, fill_opacity=0.08, stroke_width=0,
        ).shift(DOWN * 0.3)
        cold_text = safe_text("Applying Cold...", font_size=20, color=COLD_CYAN)
        cold_text.to_edge(UP, buff=0.5)

        self.play(FadeIn(cold_box), Write(cold_text))
        # Polymer chains remain flexible (gentle wave)
        self.play(
            *[c.animate.stretch(0.92, 0) for c in sbs_chains],
            run_time=1.0,
        )
        flex_text = safe_text(
            "Polymer stays flexible -- no cracking!", font_size=18, color=SUCCESS_GREEN
        )
        flex_text.next_to(sbs_label, DOWN, buff=0.3)
        self.play(Write(flex_text))
        self.wait(0.8)

        self.play(FadeOut(cold_box), FadeOut(cold_text), FadeOut(flex_text))

        # -- Performance bars --
        bars_title = section_title("Performance Improvement")
        self.play(
            FadeOut(bitumen_chains), FadeOut(sbs_chains), FadeOut(sbs_label),
        )
        self.play(Write(bars_title))

        rut_bar = Rectangle(
            width=1.2, height=3.0,
            fill_color=SUCCESS_GREEN, fill_opacity=0.8,
            stroke_width=0,
        )
        rut_label = safe_text("Rutting\nResistance", font_size=16, color=WHITE)
        rut_group = VGroup(rut_label, rut_bar).arrange(DOWN, buff=0.2)
        rut_group.shift(LEFT * 2.5 + DOWN * 0.3)

        crack_bar = Rectangle(
            width=1.2, height=3.0,
            fill_color=SUCCESS_GREEN, fill_opacity=0.8,
            stroke_width=0,
        )
        crack_label = safe_text("Crack\nResistance", font_size=16, color=WHITE)
        crack_group = VGroup(crack_label, crack_bar).arrange(DOWN, buff=0.2)
        crack_group.shift(RIGHT * 2.5 + DOWN * 0.3)

        self.play(
            FadeIn(rut_label), GrowFromEdge(rut_bar, DOWN),
            FadeIn(crack_label), GrowFromEdge(crack_bar, DOWN),
            run_time=1.5,
        )

        # -- Spec equations --
        rut_eq = MathTex(
            r"G^* / \sin\delta \geq 1.0 \text{ kPa}",
            font_size=SMALL_EQ, color=STRESS_YELLOW,
        ).next_to(rut_bar, RIGHT, buff=0.3)

        crack_eq = MathTex(
            r"S \leq 300 \text{ MPa}, \; m \geq 0.300",
            font_size=SMALL_EQ, color=COLD_CYAN,
        ).next_to(crack_bar, LEFT, buff=0.3)

        self.play(Write(rut_eq), Write(crack_eq))
        self.wait(1)

        note = bottom_note(
            "PMB creates elastic bridges that resist both flow and fracture."
        )
        self.play(Write(note))
        self.wait(2)

        fade_all(
            self, bars_title, rut_bar, rut_label, crack_bar, crack_label,
            rut_eq, crack_eq, note,
        )


# ============================================================
# SCENE 5: PGGradingSystem (~55s)
# ============================================================
class PGGradingSystem(Scene):
    """PG grades, temperature ranges, and global deployment."""

    def construct(self) -> None:
        # -- Temperature line at top (persistent) --
        nline, unit_lbl = temperature_number_line(
            x_range=(-30, 80, 10), length=11, position=UP * 2.8
        )
        self.play(Create(nline), FadeIn(unit_lbl))

        subtitle = safe_text("Performance Grade Specifications", font_size=HEADING_SIZE)
        subtitle.move_to(UP * 1.8)
        self.play(Write(subtitle))
        self.wait(0.3)

        # -- Grade table (simplified as rows of text) --
        grades_data = [
            ("PG 76-22", 76, -22, "Airport Runway"),
            ("PG 76E-10", 76, -10, "Expressway"),
            ("PG 64-22", 64, -22, "Highway"),
        ]

        rows = VGroup()
        range_highlights = VGroup()

        colors_for_use = [STRESS_YELLOW, POLYMER_BLUE, CONTEXT_GRAY]

        for i, (grade, hi, lo, use) in enumerate(grades_data):
            grade_text = safe_text(grade, font_size=20, color=colors_for_use[i])
            grade_text.move_to(LEFT * 4.5 + DOWN * (0.0 + i * 0.7))

            use_text = safe_text(use, font_size=18, color=WHITE)
            use_text.move_to(LEFT * 1.0 + DOWN * (0.0 + i * 0.7))

            range_text = safe_text(
                f"{lo}°C to {hi}°C", font_size=18, color=colors_for_use[i]
            )
            range_text.move_to(RIGHT * 2.5 + DOWN * (0.0 + i * 0.7))

            row = VGroup(grade_text, use_text, range_text)
            rows.add(row)

            # Highlight span on temperature line
            left_pt = nline.n2p(lo)
            right_pt = nline.n2p(hi)
            span = Line(
                left_pt + DOWN * (0.3 + i * 0.15),
                right_pt + DOWN * (0.3 + i * 0.15),
                color=colors_for_use[i],
                stroke_width=5,
                stroke_opacity=0.8,
            )
            range_highlights.add(span)

        # Animate rows appearing with stagger
        for i, (row, span) in enumerate(zip(rows, range_highlights)):
            self.play(
                LaggedStart(*[FadeIn(m, shift=RIGHT * 0.3) for m in row], lag_ratio=0.15),
                Create(span),
                run_time=0.8,
            )

        # Highlight PG 76-22 as the airport standard
        airport_rect = SurroundingRectangle(
            rows[0], color=STRESS_YELLOW, buff=0.1, stroke_width=2,
        )
        self.play(Create(airport_rect))
        self.wait(0.5)

        # -- Deployment map (simplified: dots with labels) --
        self.play(
            FadeOut(subtitle), FadeOut(rows), FadeOut(airport_rect),
            FadeOut(range_highlights),
        )

        map_title = safe_text("Global Airport Deployment", font_size=HEADING_SIZE)
        map_title.move_to(UP * 1.8)
        self.play(Write(map_title))

        # Airport locations as labeled dots (approximate relative positions)
        airports = [
            ("Hanoi", LEFT * 2 + DOWN * 0.2),
            ("Ho Chi Minh", LEFT * 1.5 + DOWN * 1.0),
            ("Kuala Lumpur", LEFT * 0.5 + DOWN * 1.5),
            ("Jakarta", RIGHT * 0.5 + DOWN * 2.0),
            ("Phnom Penh", LEFT * 0.8 + DOWN * 0.5),
            ("Hyderabad", LEFT * 3.5 + DOWN * 0.3),
            ("Bangalore", LEFT * 3.2 + DOWN * 1.2),
        ]

        dots = VGroup()
        labels = VGroup()
        for name, pos in airports:
            dot = Dot(pos, color=STRESS_YELLOW, radius=0.1)
            lbl = safe_text(name, font_size=14, color=WHITE)
            lbl.next_to(dot, UR, buff=0.08)
            dots.add(dot)
            labels.add(lbl)

        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.15))
        self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.1))

        # Counter
        counter_text = safe_text(
            "23 airports  |  6 countries  |  45,000 tonnes PMB",
            font_size=20, color=SUCCESS_GREEN,
        )
        counter_text.shift(DOWN * 2.8)
        self.play(Write(counter_text))
        self.wait(1)

        note = bottom_note("But the grade alone doesn't tell you if the mix survives jet fuel.")
        self.play(FadeOut(counter_text))
        self.play(Write(note))
        self.wait(2)

        fade_all(self, nline, unit_lbl, map_title, dots, labels, note)


# ============================================================
# SCENE 6: FuelResistance (~40s)
# ============================================================
class FuelResistance(Scene):
    """Jet fuel dissolves standard bitumen; fuel-resistant PMB survives."""

    def construct(self) -> None:
        title = section_title("Jet Fuel Resistance")
        self.play(Write(title))
        self.wait(0.3)

        divider = Line(UP * 2.2, DOWN * 2.5, color=WHITE, stroke_width=1, stroke_opacity=0.3)

        # ============ LEFT: Standard bitumen ============
        left_label = safe_text("Standard Bitumen", font_size=20, color=HEAT_RED)
        left_label.move_to(LEFT * 3.5 + UP * 2.0)

        left_pave = Rectangle(
            width=3, height=0.8,
            fill_color=ASPHALT_BLACK, fill_opacity=0.9,
            stroke_color=WHITE, stroke_width=1.5,
        ).move_to(LEFT * 3.5 + DOWN * 0.5)

        # ============ RIGHT: Fuel-resistant PMB ============
        right_label = safe_text("Fuel-Resistant PMB", font_size=20, color=SUCCESS_GREEN)
        right_label.move_to(RIGHT * 3.5 + UP * 2.0)

        right_pave = Rectangle(
            width=3, height=0.8,
            fill_color=ASPHALT_BLACK, fill_opacity=0.9,
            stroke_color=WHITE, stroke_width=1.5,
        ).move_to(RIGHT * 3.5 + DOWN * 0.5)

        self.play(
            Create(divider),
            Write(left_label), FadeIn(left_pave),
            Write(right_label), FadeIn(right_pave),
        )
        self.wait(0.3)

        # -- Fuel droplets --
        def make_droplet(position):
            """Create a teardrop shape at position."""
            drop = Circle(radius=0.2, fill_color=FUEL_ORANGE, fill_opacity=0.9, stroke_width=0)
            tip = Triangle(fill_color=FUEL_ORANGE, fill_opacity=0.9, stroke_width=0)
            tip.scale(0.15).rotate(PI).next_to(drop, UP, buff=-0.07)
            return VGroup(drop, tip).move_to(position)

        left_drop = make_droplet(LEFT * 3.5 + UP * 1.0)
        right_drop = make_droplet(RIGHT * 3.5 + UP * 1.0)

        self.play(FadeOut(title))
        fuel_text = safe_text("Jet Fuel Contact", font_size=HEADING_SIZE)
        fuel_text.to_edge(UP, buff=0.5)
        self.play(Write(fuel_text))

        # Drops fall
        self.play(
            left_drop.animate.move_to(left_pave.get_top() + UP * 0.15),
            right_drop.animate.move_to(right_pave.get_top() + UP * 0.15),
            run_time=1.0,
        )
        self.wait(0.3)

        # LEFT: surface dissolves
        dissolve_anims = [
            left_pave.animate.set_fill(opacity=0.2).set_stroke(opacity=0.3),
            left_drop.animate.scale(1.8).set_opacity(0.3),
        ]
        damage_label = safe_text("DISSOLVED", font_size=22, color=HEAT_RED)
        damage_label.move_to(left_pave.get_center())

        # RIGHT: droplet beads up, surface intact
        bead_anims = [
            right_drop.animate.scale(0.6).shift(UP * 0.15),
        ]
        intact_label = safe_text("INTACT", font_size=22, color=SUCCESS_GREEN)
        intact_label.next_to(right_pave, DOWN, buff=0.3)

        self.play(*dissolve_anims, *bead_anims, run_time=1.5)
        self.play(Write(damage_label), Write(intact_label))
        self.wait(0.5)

        # Grade label
        grade_label = safe_text("PG 76 Fuel Resistant", font_size=24, color=FUEL_ORANGE)
        grade_label.next_to(right_pave, UP, buff=0.8)
        self.play(Write(grade_label))

        note = bottom_note(
            "Cross-linked polymers create a barrier jet fuel cannot penetrate."
        )
        self.play(Write(note))
        self.wait(2)

        fade_all(
            self, divider, left_label, left_pave, left_drop,
            right_label, right_pave, right_drop,
            fuel_text, damage_label, intact_label, grade_label, note,
        )


# ============================================================
# SCENE 7: ThicknessReduction (~50s)
# ============================================================
class ThicknessReduction(Scene):
    """HIPB allows thinner pavement layers due to higher stiffness modulus."""

    def construct(self) -> None:
        title = section_title("Thickness Reduction with HIPB")
        self.play(Write(title))
        self.wait(0.3)

        divider = Line(UP * 2.2, DOWN * 3.0, color=WHITE, stroke_width=1, stroke_opacity=0.3)

        # ============ LEFT: VG40 cross-section ============
        left_heading = safe_text("VG40 (Conventional)", font_size=18, color=CONTEXT_GRAY)
        left_heading.move_to(LEFT * 3.2 + UP * 1.8)

        vg40_data = [
            ("BC", 40, "#1a1a1a"),
            ("DBM", 150, ASPHALT_BLACK),
            ("WMM", 250, "#8B7355"),
            ("GSB", 230, GRAY),
        ]
        # Build cross-section manually for precise control
        vg40_layers = VGroup()
        vg40_labels = VGroup()
        total_mm = sum(t for _, t, _ in vg40_data)
        scale = 3.5 / total_mm
        y_cursor = -2.5

        for name, thick, color in reversed(vg40_data):  # bottom to top
            h = thick * scale
            rect = Rectangle(
                width=2.5, height=h,
                fill_color=color, fill_opacity=0.85,
                stroke_color=WHITE, stroke_width=1,
            ).move_to(LEFT * 3.2 + UP * (y_cursor + h / 2))
            lbl = safe_text(f"{name} {thick}mm", font_size=12, color=WHITE)
            lbl.move_to(rect.get_center())
            vg40_layers.add(rect)
            vg40_labels.add(lbl)
            y_cursor += h

        vg40_total = safe_text(
            f"Total: {total_mm}mm", font_size=16, color=WHITE
        )
        vg40_total.next_to(VGroup(vg40_layers), RIGHT, buff=0.3)

        # ============ RIGHT: HIPB cross-section ============
        right_heading = safe_text("HIPB (High Performance)", font_size=18, color=POLYMER_BLUE)
        right_heading.move_to(RIGHT * 3.2 + UP * 1.8)

        hipb_data = [
            ("BC", 40, "#1a1a1a"),
            ("DBM", 120, POLYMER_BLUE),  # reduced!
            ("WMM", 250, "#8B7355"),
            ("GSB", 230, GRAY),
        ]
        hipb_layers = VGroup()
        hipb_labels = VGroup()
        hipb_total_mm = sum(t for _, t, _ in hipb_data)
        y_cursor = -2.5

        for name, thick, color in reversed(hipb_data):
            h = thick * scale  # same scale as VG40 for visual comparison
            rect = Rectangle(
                width=2.5, height=h,
                fill_color=color, fill_opacity=0.85,
                stroke_color=WHITE, stroke_width=1,
            ).move_to(RIGHT * 3.2 + UP * (y_cursor + h / 2))
            lbl = safe_text(f"{name} {thick}mm", font_size=12, color=WHITE)
            lbl.move_to(rect.get_center())
            hipb_layers.add(rect)
            hipb_labels.add(lbl)
            y_cursor += h

        hipb_total = safe_text(
            f"Total: {hipb_total_mm}mm", font_size=16, color=SUCCESS_GREEN
        )
        hipb_total.next_to(VGroup(hipb_layers), RIGHT, buff=0.3)

        # Animate
        self.play(FadeOut(title))
        self.play(Create(divider), Write(left_heading), Write(right_heading))
        self.play(
            LaggedStart(*[FadeIn(r) for r in vg40_layers], lag_ratio=0.15),
            LaggedStart(*[FadeIn(l) for l in vg40_labels], lag_ratio=0.15),
            LaggedStart(*[FadeIn(r) for r in hipb_layers], lag_ratio=0.15),
            LaggedStart(*[FadeIn(l) for l in hipb_labels], lag_ratio=0.15),
            run_time=2,
        )
        self.play(Write(vg40_total), Write(hipb_total))
        self.wait(0.5)

        # Highlight the DBM difference
        # DBM is index 1 in both (second from bottom in the reversed build)
        vg40_dbm = vg40_layers[1]  # DBM in VG40
        hipb_dbm = hipb_layers[1]  # DBM in HIPB

        dbm_highlight_l = SurroundingRectangle(vg40_dbm, color=HEAT_RED, buff=0.05)
        dbm_highlight_r = SurroundingRectangle(hipb_dbm, color=SUCCESS_GREEN, buff=0.05)
        self.play(Create(dbm_highlight_l), Create(dbm_highlight_r))

        savings_text = safe_text("30mm saved!", font_size=22, color=SUCCESS_GREEN)
        savings_text.next_to(hipb_dbm, LEFT, buff=0.5)
        savings_arrow = Arrow(
            savings_text.get_right(), hipb_dbm.get_left(),
            color=SUCCESS_GREEN, stroke_width=2,
            max_tip_length_to_length_ratio=0.2,
        )
        self.play(Write(savings_text), GrowArrow(savings_arrow))
        self.wait(0.5)

        # Stiffness modulus equation
        stiff_eq = MathTex(
            r"E_{\text{HIPB}} = 4000 \text{ MPa}",
            r" > ",
            r"E_{\text{VG40}} = 3000 \text{ MPa}",
            font_size=SMALL_EQ,
        )
        stiff_eq[0].set_color(POLYMER_BLUE)
        stiff_eq[2].set_color(CONTEXT_GRAY)
        stiff_eq.to_edge(DOWN, buff=1.2)
        self.play(Write(stiff_eq))
        self.wait(1)

        note = bottom_note(
            "Higher stiffness = thinner layers = thousands of tonnes of material saved."
        )
        self.play(Write(note))
        self.wait(2)

        fade_all(
            self, divider, left_heading, right_heading,
            vg40_layers, vg40_labels, vg40_total,
            hipb_layers, hipb_labels, hipb_total,
            dbm_highlight_l, dbm_highlight_r,
            savings_text, savings_arrow, stiff_eq, note,
        )


# ============================================================
# SCENE 8: TestingPipeline (~45s)
# ============================================================
class TestingPipeline(Scene):
    """Quality assurance pipeline from binder selection to full construction."""

    def construct(self) -> None:
        title = section_title("Quality Assurance Pipeline")
        self.play(Write(title))
        self.wait(0.3)
        self.play(FadeOut(title))

        # -- Pipeline nodes --
        node_data = [
            ("Binder\nSelection", POLYMER_BLUE),
            ("Lab\nTesting", STRESS_YELLOW),
            ("Mix\nDesign", FUEL_ORANGE),
            ("Field\nTrials", SUCCESS_GREEN),
            ("Full\nConstruction", WHITE),
        ]

        nodes = VGroup()
        node_labels = VGroup()

        for i, (label_text, color) in enumerate(node_data):
            # Node circle
            circle = Circle(
                radius=0.55, fill_color=color, fill_opacity=0.2,
                stroke_color=color, stroke_width=2,
            )
            label = safe_text(label_text, font_size=14, color=color)
            label.move_to(circle.get_center())
            node_group = VGroup(circle, label)
            nodes.add(circle)
            node_labels.add(label)

        all_nodes = VGroup(*[VGroup(n, l) for n, l in zip(nodes, node_labels)])
        all_nodes.arrange(RIGHT, buff=0.8).shift(UP * 1.2)

        # Arrows between nodes
        arrows = VGroup()
        for i in range(len(nodes) - 1):
            arrow = Arrow(
                nodes[i].get_right(), nodes[i + 1].get_left(),
                color=WHITE, stroke_width=2, buff=0.1,
                max_tip_length_to_length_ratio=0.2,
            )
            arrows.add(arrow)

        # Animate build-up: nodes grow one by one, arrows connect
        for i in range(len(nodes)):
            anims = [GrowFromCenter(nodes[i]), FadeIn(node_labels[i])]
            if i > 0:
                anims.append(GrowArrow(arrows[i - 1]))
            self.play(*anims, run_time=0.6)

        self.wait(0.5)

        # -- Highlight Lab Testing: DSR rheology --
        highlight = SurroundingRectangle(
            VGroup(nodes[1], node_labels[1]),
            color=STRESS_YELLOW, buff=0.15,
        )
        self.play(Create(highlight))

        # DSR visualization: oscillating parallel plates
        dsr_title = safe_text("Dynamic Shear Rheometer (DSR)", font_size=18, color=STRESS_YELLOW)
        dsr_title.shift(DOWN * 0.5)
        self.play(Write(dsr_title))

        # Two parallel plates
        top_plate = Rectangle(width=2, height=0.15, fill_color=GRAY, fill_opacity=0.8,
                              stroke_width=1).shift(DOWN * 1.2)
        bot_plate = Rectangle(width=2, height=0.15, fill_color=GRAY, fill_opacity=0.8,
                              stroke_width=1).shift(DOWN * 2.0)
        sample = Rectangle(width=1.8, height=0.55, fill_color=ASPHALT_BLACK, fill_opacity=0.7,
                           stroke_width=0).move_to((top_plate.get_center() + bot_plate.get_center()) / 2)

        self.play(FadeIn(top_plate), FadeIn(bot_plate), FadeIn(sample))

        # Oscillation animation using ValueTracker
        phase = ValueTracker(0)
        top_plate.add_updater(
            lambda m, dt: m.move_to(
                DOWN * 1.2 + RIGHT * 0.3 * np.sin(phase.get_value())
            )
        )

        # G*/sin(delta) readout
        readout = MathTex(
            r"G^*/\sin\delta = 1.24 \text{ kPa}",
            font_size=SMALL_EQ, color=SUCCESS_GREEN,
        ).shift(DOWN * 2.8)
        self.play(Write(readout))

        self.play(phase.animate.set_value(4 * PI), run_time=3, rate_func=linear)
        top_plate.clear_updaters()
        self.wait(0.3)

        # Case study reference
        case_text = safe_text(
            "First customized PMB on Indian airport runways: Hyderabad & Bangalore (2006-07)",
            font_size=16, color=POLYMER_BLUE,
        )
        case_text.to_edge(DOWN, buff=0.4)
        self.play(FadeOut(readout))
        self.play(Write(case_text))
        self.wait(2)

        fade_all(
            self, nodes, node_labels, arrows, highlight,
            dsr_title, top_plate, bot_plate, sample, case_text,
        )


# ============================================================
# SCENE 9: Synthesis (~35s)
# ============================================================
class Synthesis(Scene):
    """Final synthesis: all key visuals converge, density ramp climax."""

    def construct(self) -> None:
        # -- Temperature number line (top) --
        nline, unit_lbl = temperature_number_line(
            x_range=(-30, 80, 10), length=11, position=UP * 3.0
        )
        self.play(Create(nline), FadeIn(unit_lbl), run_time=1)

        # -- PG 76-22 label (center-left) --
        pg_label = MathTex(
            r"\text{PG }", r"76", r"\text{-}", r"22",
            font_size=40,
        )
        pg_label[1].set_color(HEAT_RED)
        pg_label[3].set_color(COLD_CYAN)
        pg_label.move_to(LEFT * 3.5 + UP * 1.2)
        self.play(Write(pg_label))

        # -- Polymer network mini-diagram (center-right) --
        mini_chains = VGroup()
        np.random.seed(99)
        for _ in range(4):
            c = polymer_chain(
                n_points=6, amplitude=0.15, length=1.2,
                color=POLYMER_BLUE, stroke_width=2,
            )
            c.move_to([
                np.random.uniform(2.5, 4.5),
                np.random.uniform(0.5, 1.8),
                0,
            ])
            c.rotate(np.random.uniform(-0.3, 0.3))
            mini_chains.add(c)
        chain_label = safe_text("SBS Network", font_size=14, color=POLYMER_BLUE)
        chain_label.next_to(mini_chains, DOWN, buff=0.15)
        self.play(
            LaggedStart(*[Create(c) for c in mini_chains], lag_ratio=0.1),
            Write(chain_label),
            run_time=1,
        )

        # -- Runway cross-section (bottom-left) --
        cross = runway_cross_section(
            total_width=1.8,
            position=LEFT * 3.5 + DOWN * 1.5,
        )
        cross.scale(0.6)
        cross_label = safe_text("Pavement Design", font_size=14, color=WHITE)
        cross_label.next_to(cross, DOWN, buff=0.15)
        self.play(FadeIn(cross), Write(cross_label), run_time=0.8)

        # -- Airport dots (bottom-right) --
        airport_names = ["HAN", "SGN", "KUL", "CGK", "HYD", "BLR", "PNH"]
        dots = VGroup()
        for i, name in enumerate(airport_names):
            dot = Dot(
                RIGHT * (1.5 + (i % 4) * 0.8) + DOWN * (1.0 + (i // 4) * 0.6),
                color=STRESS_YELLOW, radius=0.08,
            )
            lbl = safe_text(name, font_size=10, color=WHITE)
            lbl.next_to(dot, DOWN, buff=0.05)
            dots.add(VGroup(dot, lbl))

        self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.08))

        # -- Dashed connectors showing logical flow --
        connector_1 = DashedLine(
            nline.n2p(76) + DOWN * 0.3, pg_label.get_top() + UP * 0.1,
            color=WHITE, stroke_opacity=0.3, stroke_width=1,
        )
        connector_2 = DashedLine(
            pg_label.get_right(), mini_chains.get_left() + LEFT * 0.1,
            color=WHITE, stroke_opacity=0.3, stroke_width=1,
        )
        connector_3 = DashedLine(
            mini_chains.get_bottom() + DOWN * 0.3, dots[0].get_left() + LEFT * 0.2,
            color=WHITE, stroke_opacity=0.3, stroke_width=1,
        )
        self.play(
            Create(connector_1), Create(connector_2), Create(connector_3),
            run_time=1,
        )
        self.wait(0.5)

        # -- Final equation: conceptual throughline --
        final_eq = MathTex(
            r"\text{PG } T_{\max}\text{-}|T_{\min}|",
            r"\implies",
            r"\text{Safe Runway}",
            font_size=36,
        )
        final_eq[0].set_color(STRESS_YELLOW)
        final_eq[2].set_color(SUCCESS_GREEN)
        final_eq.move_to(DOWN * 3.0)
        self.play(Write(final_eq))
        self.wait(1)

        # -- Fade everything except final equation --
        all_context = [
            nline, unit_lbl, pg_label, mini_chains, chain_label,
            cross, cross_label, dots,
            connector_1, connector_2, connector_3,
        ]
        self.play(*[FadeOut(m) for m in all_context], run_time=1.5)

        # Pulse the final equation in SUCCESS_GREEN
        self.play(
            final_eq.animate.set_color(SUCCESS_GREEN).scale(1.15),
            rate_func=there_and_back,
            run_time=1.2,
        )
        self.wait(1)

        # Closing text
        closing = safe_text(
            "Two numbers. Thirty years of engineering.",
            font_size=HEADING_SIZE, color=WHITE,
        )
        closing.shift(UP * 1.0)
        self.play(Write(closing))
        self.wait(3)

        fade_all(self, final_eq, closing)