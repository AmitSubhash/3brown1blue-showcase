"""Solar Panel Mechanical Delamination -- 8-Scene Manim Explainer Video.

Render individual scenes:
    manim -pql solar_delamination.py S01_Hook
    manim -pqh solar_delamination.py S05_HotKnife

Render all scenes:
    manim -pql -a solar_delamination.py
"""

from manim import *
import numpy as np

# ============================================================
# STYLE CONTRACT -- shared constants, colors, helpers
# ============================================================

# -- Semantic Color Palette --
GLASS_COLOR = "#7EC8E3"
EVA_COLOR = "#FF8C42"
CELL_COLOR = "#2E5090"
SILVER_COLOR = "#C0C0C0"
COPPER_COLOR = "#B87333"
BACKSHEET_COLOR = "#888888"
FRAME_COLOR = "#A8A8A8"

HEAT_LOW = "#3B82F6"
HEAT_MID = "#F59E0B"
HEAT_HIGH = "#EF4444"

HOTKNIFE_COLOR = "#EF4444"
ROLLER_COLOR = "#6B7280"
CHEMICAL_COLOR = "#10B981"

HIGHLIGHT = "#FACC15"
DIMMED = "#4B5563"
POSITIVE = "#22C55E"
DANGER = "#EF4444"

BG_COLOR = "#0F172A"

# -- Font Sizes --
TITLE_SIZE = 42
SUBTITLE_SIZE = 34
BODY_SIZE = 28
LABEL_SIZE = 22
EQ_SIZE = 36
EQ_SMALL = 28
VALUE_SIZE = 20

# -- Layout Constants --
TITLE_Y = 3.0
SUBTITLE_Y = 1.6
BOTTOM_Y = -3.2
LEFT_X = -3.5
RIGHT_X = 3.5
SAFE_WIDTH = 12.0
MINI_SCALE = 0.4

# -- Timing --
HOLD_SHORT = 1.0
HOLD_MEDIUM = 2.0
HOLD_LONG = 3.0

# -- Layer data: (name, color, thickness_mm, visual_height) bottom-to-top --
LAYER_SCALE = 0.8
LAYERS = [
    ("Backsheet (TPT)", BACKSHEET_COLOR, 0.30, 0.4),
    ("EVA", EVA_COLOR, 0.45, 0.5),
    ("Si Cells + Ag", CELL_COLOR, 0.18, 0.6),
    ("EVA", EVA_COLOR, 0.45, 0.5),
    ("Tempered Glass", GLASS_COLOR, 3.20, 1.5),
]


# -- Helper Functions --

def section_title(text: str, color=WHITE) -> Text:
    """Styled section title at top of frame."""
    return Text(text, font_size=TITLE_SIZE, color=color).move_to(UP * TITLE_Y)


def safe_text(
    text: str,
    font_size: int = BODY_SIZE,
    color=WHITE,
    max_width: float = SAFE_WIDTH,
    **kwargs,
) -> Text:
    """Text that auto-scales to fit within max_width."""
    t = Text(text, font_size=font_size, color=color, **kwargs)
    if t.width > max_width:
        t.scale_to_fit_width(max_width)
    return t


def bottom_note(text: str, color=HIGHLIGHT) -> Text:
    """Width-capped bottom note."""
    t = Text(text, font_size=LABEL_SIZE, color=color)
    if t.width > SAFE_WIDTH:
        t.scale_to_fit_width(SAFE_WIDTH)
    return t.to_edge(DOWN, buff=0.5)


def fade_all(scene: Scene, run_time: float = 0.8) -> None:
    """Fade out every mobject in the scene."""
    if scene.mobjects:
        scene.play(*[FadeOut(m) for m in scene.mobjects], run_time=run_time)


def build_cross_section(width: float = 5.0) -> VGroup:
    """Panel cross-section as VGroup of (Rectangle, label) layers, bottom-to-top."""
    layers = VGroup()
    for name, color, _mm, visual_h in LAYERS:
        rect = Rectangle(
            width=width,
            height=visual_h * LAYER_SCALE,
            color=color,
            fill_color=color,
            fill_opacity=0.7,
            stroke_width=1.5,
        )
        label = Text(name, font_size=VALUE_SIZE, color=WHITE)
        label.move_to(rect)
        if label.width > rect.width - 0.3:
            label.scale_to_fit_width(rect.width - 0.3)
        layer = VGroup(rect, label)
        layers.add(layer)
    layers.arrange(UP, buff=0.02)
    return layers


def mini_cross_section() -> VGroup:
    """Small persistent cross-section for TOP_PERSISTENT scenes."""
    cs = build_cross_section(width=3.0)
    cs.scale(MINI_SCALE)
    cs.to_corner(UL, buff=0.4)
    cs.set_opacity(0.7)
    return cs


def safe_brace_label(
    brace: Brace, text: str, font_size: int = 24, color=WHITE
) -> Tex:
    """Brace label that avoids the font_size kwarg crash."""
    label = Tex(text, font_size=font_size, color=color)
    brace.put_at_tip(label)
    return label


# ============================================================
# SCENE 1: HOOK -- waste crisis and hidden treasure
# ============================================================

class S01_Hook(Scene):
    """Show the waste crisis counter, then explode the panel to reveal value."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        # -- Stylized solar panel --
        panel_body = Rectangle(
            width=4, height=2.5, color=CELL_COLOR,
            fill_color=CELL_COLOR, fill_opacity=0.6, stroke_width=2,
        )
        # Grid lines to suggest cells
        grid_lines = VGroup()
        for x_off in np.linspace(-1.5, 1.5, 4):
            grid_lines.add(
                Line(
                    panel_body.get_top() + RIGHT * x_off,
                    panel_body.get_bottom() + RIGHT * x_off,
                    stroke_width=1, color=SILVER_COLOR, stroke_opacity=0.5,
                )
            )
        for y_off in np.linspace(-0.8, 0.8, 3):
            grid_lines.add(
                Line(
                    panel_body.get_left() + UP * y_off,
                    panel_body.get_right() + UP * y_off,
                    stroke_width=1, color=SILVER_COLOR, stroke_opacity=0.5,
                )
            )
        panel = VGroup(panel_body, grid_lines).move_to(ORIGIN)

        self.play(FadeIn(panel, scale=0.9), run_time=0.8)

        # -- Waste counter --
        counter_text = Text(
            "78 MILLION TONNES BY 2050",
            font_size=SUBTITLE_SIZE, color=DANGER, weight=BOLD,
        )
        counter_text.next_to(panel, UP, buff=0.6)
        self.play(Write(counter_text), run_time=1.2)
        self.wait(HOLD_MEDIUM)

        # -- Explode into layers --
        self.play(FadeOut(counter_text), run_time=0.4)

        # Build cross-section layers at panel position
        cs = build_cross_section(width=4.0)
        cs.move_to(panel.get_center())

        # Animate panel fading to exploded cross-section
        # Spread layers apart vertically
        target_positions = [
            DOWN * 2.0, DOWN * 1.0, ORIGIN, UP * 1.0, UP * 2.2,
        ]
        for layer, target_pos in zip(cs, target_positions):
            layer.move_to(panel.get_center())

        self.play(FadeOut(panel), run_time=0.3)
        self.play(
            LaggedStart(
                *[
                    layer.animate.move_to(target_pos)
                    for layer, target_pos in zip(cs, target_positions)
                ],
                lag_ratio=0.15,
            ),
            run_time=1.5,
        )

        # -- Value labels on right side --
        value_labels = VGroup()
        # Glass (top layer, index 4)
        glass_val = Text("70% mass, $0.50/kg", font_size=VALUE_SIZE, color=GLASS_COLOR)
        glass_val.next_to(cs[4], RIGHT, buff=0.3)
        value_labels.add(glass_val)

        # Cell layer (index 2)
        cell_val = Text("~$15 Ag per panel", font_size=VALUE_SIZE, color=HIGHLIGHT)
        cell_val.next_to(cs[2], RIGHT, buff=0.3)
        value_labels.add(cell_val)

        self.play(
            LaggedStart(*[FadeIn(v, shift=LEFT * 0.3) for v in value_labels], lag_ratio=0.3),
            run_time=1.0,
        )
        self.wait(HOLD_SHORT)

        # -- Bottom question --
        note = bottom_note("What if we could recover what's inside?")
        self.play(FadeIn(note, shift=UP * 0.3))
        self.wait(HOLD_MEDIUM)

        fade_all(self)


# ============================================================
# SCENE 2: PROBLEM -- EVA adhesion resists separation
# ============================================================

class S02_Problem(Scene):
    """EVA makes panels permanent. Show bonding, failed separation, question frame."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = section_title("The Problem")
        self.play(Write(title))
        self.wait(0.5)

        # -- LEFT PANEL: cross-section with EVA glowing --
        left_group = VGroup()

        # Simplified cross-section (3 layers: glass, EVA, cells)
        glass_rect = Rectangle(
            width=3.5, height=1.0, color=GLASS_COLOR,
            fill_color=GLASS_COLOR, fill_opacity=0.6,
        )
        glass_label = Text("Glass", font_size=VALUE_SIZE, color=WHITE).move_to(glass_rect)

        eva_rect = Rectangle(
            width=3.5, height=0.4, color=EVA_COLOR,
            fill_color=EVA_COLOR, fill_opacity=0.9,
        )
        eva_label = Text("EVA", font_size=VALUE_SIZE, color=WHITE).move_to(eva_rect)

        cell_rect = Rectangle(
            width=3.5, height=0.5, color=CELL_COLOR,
            fill_color=CELL_COLOR, fill_opacity=0.7,
        )
        cell_label = Text("Si Cells", font_size=VALUE_SIZE, color=WHITE).move_to(cell_rect)

        stack = VGroup(
            VGroup(cell_rect, cell_label),
            VGroup(eva_rect, eva_label),
            VGroup(glass_rect, glass_label),
        ).arrange(UP, buff=0.02)
        stack.move_to(LEFT_X * UP * 0 + LEFT * 3.2 + DOWN * 0.3)

        # Adhesion force arrows (small, pointing inward toward EVA)
        arrows_left = VGroup()
        for y_off in [-0.15, 0.15]:
            for x_off in np.linspace(-1.2, 1.2, 4):
                arr = Arrow(
                    eva_rect.get_center() + RIGHT * x_off + UP * (y_off + np.sign(y_off) * 0.35),
                    eva_rect.get_center() + RIGHT * x_off + UP * y_off,
                    buff=0, stroke_width=2, color=EVA_COLOR,
                    max_tip_length_to_length_ratio=0.4,
                )
                arrows_left.add(arr)

        cure_label = Text(
            "Cured at 150\u00b0C", font_size=VALUE_SIZE, color=EVA_COLOR
        )
        cure_label.next_to(stack, DOWN, buff=0.3)

        left_group.add(stack, arrows_left, cure_label)

        # -- RIGHT PANEL: attempted peel fails --
        right_group = VGroup()

        # Panel rectangle (simplified)
        panel_r = Rectangle(
            width=3.0, height=0.8, color=GLASS_COLOR,
            fill_color=GLASS_COLOR, fill_opacity=0.5,
        )
        backsheet_r = Rectangle(
            width=3.0, height=0.3, color=BACKSHEET_COLOR,
            fill_color=BACKSHEET_COLOR, fill_opacity=0.6,
        )
        eva_thin = Rectangle(
            width=3.0, height=0.15, color=EVA_COLOR,
            fill_color=EVA_COLOR, fill_opacity=0.8,
        )
        right_stack = VGroup(backsheet_r, eva_thin, panel_r).arrange(UP, buff=0.01)
        right_stack.move_to(RIGHT * 3.2 + DOWN * 0.3)

        # Force arrow pulling backsheet down-right
        pull_arrow = Arrow(
            backsheet_r.get_right(),
            backsheet_r.get_right() + DOWN * 0.8 + RIGHT * 0.6,
            color=DANGER, stroke_width=4, buff=0,
        )
        pull_label = Text("F", font_size=BODY_SIZE, color=DANGER)
        pull_label.next_to(pull_arrow.get_end(), RIGHT, buff=0.1)

        force_text = Text(
            "Peel force: 8 N/mm\nat room temp",
            font_size=VALUE_SIZE, color=DANGER,
        )
        force_text.next_to(right_stack, DOWN, buff=0.5)

        right_group.add(right_stack, pull_arrow, pull_label, force_text)

        # -- Animate both panels --
        self.play(FadeIn(stack, shift=UP * 0.3), run_time=0.8)
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows_left], lag_ratio=0.05),
            Write(cure_label),
            run_time=1.2,
        )
        self.wait(HOLD_SHORT)

        self.play(FadeIn(right_stack, shift=UP * 0.3), run_time=0.8)
        self.play(GrowArrow(pull_arrow), Write(pull_label), run_time=0.6)

        # Backsheet resists: wobble slightly and snap back
        self.play(
            backsheet_r.animate.shift(DOWN * 0.15 + RIGHT * 0.1),
            run_time=0.3, rate_func=there_and_back,
        )
        self.play(Write(force_text), run_time=0.6)
        self.wait(HOLD_SHORT)

        # -- Question frame --
        question = Text(
            "How do you undo a bond\ndesigned to last 25 years?",
            font_size=BODY_SIZE, color=HIGHLIGHT,
        )
        question.move_to(ORIGIN + DOWN * 0.2)
        # Dim existing content
        self.play(
            left_group.animate.set_opacity(0.2),
            right_group.animate.set_opacity(0.2),
            FadeOut(title),
            run_time=0.5,
        )
        self.play(Write(question))
        self.wait(2.5)

        # -- Bottom note --
        note = bottom_note(
            'Ethylene-Vinyl Acetate (EVA) -- the adhesive that won\'t let go'
        )
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(HOLD_MEDIUM)

        fade_all(self)


# ============================================================
# SCENE 3: ANATOMY -- build cross-section layer by layer
# ============================================================

class S03_Anatomy(Scene):
    """Build the panel cross-section bottom-to-top with thicknesses and values."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = section_title("Panel Anatomy")
        self.play(Write(title))
        self.wait(0.5)

        # Build layers one at a time
        layer_data = [
            ("Backsheet (TPT)", BACKSHEET_COLOR, "0.30 mm", 0.45),
            ("Rear EVA", EVA_COLOR, "0.45 mm", 0.55),
            ("Si Cells + Ag Busbars", CELL_COLOR, "0.18 mm", 0.65),
            ("Front EVA", EVA_COLOR, "0.45 mm", 0.55),
            ("Tempered Glass", GLASS_COLOR, "3.2 mm", 1.4),
        ]

        built_layers = VGroup()
        braces = VGroup()
        thickness_labels = VGroup()

        # Pre-compute final positions so we can animate to correct spots
        all_rects = VGroup()
        for name, color, thickness_str, visual_h in layer_data:
            rect = Rectangle(
                width=5.5, height=visual_h,
                color=color, fill_color=color, fill_opacity=0.7,
                stroke_width=1.5,
            )
            lbl = Text(name, font_size=VALUE_SIZE, color=WHITE)
            lbl.move_to(rect)
            if lbl.width > rect.width - 0.4:
                lbl.scale_to_fit_width(rect.width - 0.4)
            layer_grp = VGroup(rect, lbl)
            all_rects.add(layer_grp)

        all_rects.arrange(UP, buff=0.03)
        all_rects.move_to(LEFT * 0.8 + DOWN * 0.3)

        # Animate each layer appearing
        for i, (layer_grp, (name, color, thickness_str, _vh)) in enumerate(
            zip(all_rects, layer_data)
        ):
            self.play(FadeIn(layer_grp, shift=UP * 0.3), run_time=0.6)

            # Add thickness brace on the right
            brace = Brace(layer_grp[0], RIGHT, buff=0.1, color=color)
            t_label = Text(thickness_str, font_size=18, color=color)
            t_label.next_to(brace, RIGHT, buff=0.1)
            braces.add(brace)
            thickness_labels.add(t_label)
            self.play(Create(brace), FadeIn(t_label), run_time=0.4)

        self.wait(HOLD_SHORT)

        # -- Value annotations on left side --
        self.play(FadeOut(title), run_time=0.3)

        value_data = [
            (4, "70% mass, $0.50/kg", GLASS_COLOR),       # glass
            (2, "4% mass, ~$15 Ag/panel", HIGHLIGHT),      # cells
            (0, "4% mass", BACKSHEET_COLOR),                # backsheet
        ]
        val_labels = VGroup()
        for idx, val_text, color in value_data:
            vl = Text(val_text, font_size=VALUE_SIZE, color=color)
            vl.next_to(all_rects[idx][0], LEFT, buff=0.3)
            if vl.get_left()[0] < -6.5:
                vl.scale_to_fit_width(2.5)
                vl.next_to(all_rects[idx][0], LEFT, buff=0.3)
            val_labels.add(vl)

        self.play(
            LaggedStart(*[FadeIn(v, shift=RIGHT * 0.2) for v in val_labels], lag_ratio=0.2),
            run_time=1.0,
        )
        self.wait(HOLD_SHORT)

        # -- Frame annotation (at edge) --
        frame_rect = Rectangle(
            width=0.3, height=all_rects.height + 0.2,
            color=FRAME_COLOR, fill_color=FRAME_COLOR, fill_opacity=0.5,
        )
        frame_rect.next_to(all_rects, RIGHT, buff=1.8)
        frame_label = Text("Al Frame\n8% mass\n$1.80/kg", font_size=16, color=FRAME_COLOR)
        frame_label.next_to(frame_rect, RIGHT, buff=0.15)

        self.play(FadeIn(frame_rect), Write(frame_label), run_time=0.6)

        # -- Bottom note --
        note = bottom_note("Total: 18.5 kg per standard 60-cell panel")
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(HOLD_LONG)

        fade_all(self)


# ============================================================
# SCENE 4: ADHESION -- peel test physics and temperature sweep
# ============================================================

class S04_Adhesion(Scene):
    """Peel test diagram, dim-and-reveal equation, temperature-dependent peel force."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        # -- Persistent mini cross-section --
        mini_cs = mini_cross_section()
        self.add(mini_cs)

        subtitle = Text(
            "Peel Test: Measuring Adhesion",
            font_size=SUBTITLE_SIZE, color=WHITE,
        ).move_to(UP * TITLE_Y)
        self.play(Write(subtitle))
        self.wait(0.5)

        # -- Peel test diagram --
        # Substrate (horizontal bar)
        substrate = Rectangle(
            width=5, height=0.3, color=GLASS_COLOR,
            fill_color=GLASS_COLOR, fill_opacity=0.5,
        ).move_to(DOWN * 0.8)
        sub_label = Text("Substrate", font_size=16, color=GLASS_COLOR)
        sub_label.next_to(substrate, DOWN, buff=0.1)

        # Specimen bonded on top
        specimen = Rectangle(
            width=3.5, height=0.15, color=EVA_COLOR,
            fill_color=EVA_COLOR, fill_opacity=0.8,
        )
        specimen.move_to(substrate.get_top() + UP * 0.1 + LEFT * 0.5)

        # Peeled-up portion (angled line from specimen end)
        peel_start = specimen.get_right()
        peel_angle = 70 * DEGREES
        peel_length = 1.8
        peel_end = peel_start + peel_length * np.array(
            [np.cos(peel_angle), np.sin(peel_angle), 0]
        )
        peel_line = Line(peel_start, peel_end, color=EVA_COLOR, stroke_width=3)

        # Force arrow at tip
        force_dir = np.array([np.cos(peel_angle), np.sin(peel_angle), 0])
        force_arrow = Arrow(
            peel_end, peel_end + force_dir * 1.0,
            color=DANGER, stroke_width=4, buff=0,
        )
        f_label = MathTex("F", font_size=BODY_SIZE, color=DANGER)
        f_label.next_to(force_arrow.get_end(), UR, buff=0.1)

        # Angle arc
        angle_arc = Arc(
            radius=0.6, start_angle=0, angle=peel_angle,
            arc_center=peel_start, color=HIGHLIGHT,
        )
        theta_label = MathTex(r"\theta", font_size=LABEL_SIZE, color=HIGHLIGHT)
        theta_label.next_to(angle_arc, RIGHT, buff=0.15).shift(UP * 0.15)

        # Width brace
        w_brace = Brace(specimen, DOWN, buff=0.05, color=WHITE)
        w_label = Text("w", font_size=18, color=WHITE)
        w_label.next_to(w_brace, DOWN, buff=0.05)

        peel_diagram = VGroup(
            substrate, sub_label, specimen, peel_line,
            force_arrow, f_label, angle_arc, theta_label, w_brace, w_label,
        )
        peel_diagram.move_to(LEFT * 0.5 + UP * 0.3)

        self.play(
            FadeIn(substrate, sub_label),
            FadeIn(specimen),
            run_time=0.6,
        )
        self.play(Create(peel_line), GrowArrow(force_arrow), Write(f_label), run_time=0.8)
        self.play(Create(angle_arc), Write(theta_label), run_time=0.5)
        self.play(Create(w_brace), Write(w_label), run_time=0.4)
        self.wait(HOLD_SHORT)

        # -- Equation: dim-and-reveal --
        self.play(FadeOut(subtitle), run_time=0.3)

        eq = MathTex(
            r"G", r"=", r"\frac{F}{w}", r"\left(1 - \cos\theta\right)",
            font_size=EQ_SIZE,
        )
        eq.move_to(DOWN * 2.2)
        self.play(Write(eq))
        self.wait(HOLD_SHORT)

        # Dim equation
        self.play(eq.animate.set_opacity(0.3), run_time=0.4)

        # Reveal G
        eq[0].set_opacity(1.0)
        g_rect = SurroundingRectangle(eq[0], color=POSITIVE, buff=0.08)
        g_desc = Text("Adhesion energy (J/m\u00b2)", font_size=18, color=POSITIVE)
        g_desc.next_to(g_rect, DOWN, buff=0.15)
        self.play(Create(g_rect), Write(g_desc), run_time=0.6)
        self.wait(HOLD_SHORT)
        self.play(FadeOut(g_rect), FadeOut(g_desc), run_time=0.3)
        eq[0].set_color(POSITIVE)

        # Reveal F/w
        eq[2].set_opacity(1.0)
        fw_rect = SurroundingRectangle(eq[2], color=DANGER, buff=0.08)
        fw_desc = Text("Peel force per unit width", font_size=18, color=DANGER)
        fw_desc.next_to(fw_rect, DOWN, buff=0.15)
        self.play(Create(fw_rect), Write(fw_desc), run_time=0.6)
        self.wait(HOLD_SHORT)
        self.play(FadeOut(fw_rect), FadeOut(fw_desc), run_time=0.3)
        eq[2].set_color(DANGER)

        # Reveal (1 - cos theta)
        eq[3].set_opacity(1.0)
        ct_rect = SurroundingRectangle(eq[3], color=HIGHLIGHT, buff=0.08)
        ct_desc = Text("Geometric factor", font_size=18, color=HIGHLIGHT)
        ct_desc.next_to(ct_rect, DOWN, buff=0.15)
        self.play(Create(ct_rect), Write(ct_desc), run_time=0.6)
        self.wait(HOLD_SHORT)
        self.play(FadeOut(ct_rect), FadeOut(ct_desc), run_time=0.3)
        eq[3].set_color(HIGHLIGHT)

        # Un-dim the "="
        eq[1].set_opacity(1.0)
        self.wait(HOLD_SHORT)

        # -- Temperature sweep: peel force vs temperature --
        self.play(
            FadeOut(peel_diagram),
            eq.animate.scale(0.7).to_edge(UP, buff=0.4).shift(RIGHT * 3),
            run_time=0.8,
        )

        # Axes for temperature sweep
        temp_axes = Axes(
            x_range=[0, 350, 50],
            y_range=[0, 10, 2],
            x_length=7,
            y_length=3.5,
            axis_config={"include_numbers": True, "font_size": 16},
            tips=False,
        ).move_to(DOWN * 0.3 + LEFT * 0.3)

        x_label = Text("Temperature (\u00b0C)", font_size=18)
        x_label.next_to(temp_axes.x_axis, DOWN, buff=0.3)
        y_label = Text("Peel Force (N/mm)", font_size=18)
        y_label.next_to(temp_axes.y_axis, LEFT, buff=0.3).rotate(90 * DEGREES)

        # Peel force curve: 8 N/mm at 25C, drops to ~0.5 at 300C
        # Sigmoid-like drop centered around 120C
        def peel_force(T: float) -> float:
            return 0.5 + 7.5 / (1 + np.exp(0.03 * (T - 120)))

        curve = temp_axes.plot(peel_force, x_range=[20, 340], color=EVA_COLOR)

        # Tg marker
        tg_line = DashedLine(
            temp_axes.c2p(65, 0), temp_axes.c2p(65, peel_force(65)),
            color=HIGHLIGHT, stroke_width=2,
        )
        tg_label = Text("T\u2097 ~ 65\u00b0C", font_size=16, color=HIGHLIGHT)
        tg_label.next_to(tg_line, UP, buff=0.1)

        self.play(Create(temp_axes), Write(x_label), Write(y_label), run_time=1.0)
        self.play(Create(curve), run_time=1.5)
        self.play(Create(tg_line), Write(tg_label), run_time=0.6)
        self.wait(HOLD_SHORT)

        # -- Bottom note --
        note = bottom_note("EVA softens above T\u2097 ~ 65\u00b0C -- peel force drops 10x")
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(HOLD_LONG)

        fade_all(self)


# ============================================================
# SCENE 5: HOT KNIFE -- the dominant mechanical method
# ============================================================

class S05_HotKnife(Scene):
    """Animated hot-knife sliding through EVA, separating glass from cells."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        # -- Persistent mini cross-section --
        mini_cs = mini_cross_section()
        # Highlight EVA layers in the mini
        for i in [1, 3]:  # EVA layer indices
            mini_cs[i][0].set_fill(EVA_COLOR, opacity=0.9)
            mini_cs[i][0].set_stroke(HIGHLIGHT, width=1.5)
        self.add(mini_cs)

        subtitle = Text(
            "Method 1: Hot-Knife Delamination",
            font_size=SUBTITLE_SIZE, color=HOTKNIFE_COLOR,
        ).move_to(UP * TITLE_Y)
        self.play(Write(subtitle))
        self.wait(0.5)

        # -- Panel cross-section (side view, larger) --
        panel_width = 8.0
        panel_x_start = -4.0

        glass = Rectangle(
            width=panel_width, height=0.8, color=GLASS_COLOR,
            fill_color=GLASS_COLOR, fill_opacity=0.5,
        )
        eva_layer = Rectangle(
            width=panel_width, height=0.25, color=EVA_COLOR,
            fill_color=EVA_COLOR, fill_opacity=0.8,
        )
        cell_layer = Rectangle(
            width=panel_width, height=0.35, color=CELL_COLOR,
            fill_color=CELL_COLOR, fill_opacity=0.7,
        )

        panel_stack = VGroup(cell_layer, eva_layer, glass).arrange(UP, buff=0.01)
        panel_stack.move_to(DOWN * 0.5)

        # Labels
        g_lbl = Text("Glass", font_size=16, color=WHITE).move_to(glass)
        e_lbl = Text("EVA", font_size=14, color=WHITE).move_to(eva_layer)
        c_lbl = Text("Si Cells", font_size=16, color=WHITE).move_to(cell_layer)

        self.play(
            FadeIn(panel_stack), Write(g_lbl), Write(e_lbl), Write(c_lbl),
            run_time=0.8,
        )
        self.wait(0.5)

        # -- Hot knife blade --
        blade_height = 0.5
        blade = Polygon(
            LEFT * 0.05 + UP * blade_height / 2,
            LEFT * 0.05 + DOWN * blade_height / 2,
            RIGHT * 0.4,
            color=HOTKNIFE_COLOR,
            fill_color=HOTKNIFE_COLOR,
            fill_opacity=0.9,
            stroke_width=2,
        )
        blade.move_to(eva_layer.get_left() + LEFT * 0.5)

        blade_label = Text(
            "300-350\u00b0C", font_size=16, color=HOTKNIFE_COLOR,
        )
        blade_label.next_to(blade, DOWN, buff=0.15)

        self.play(FadeIn(blade), Write(blade_label), run_time=0.5)

        # Speed label
        speed_label = Text(
            "5-15 mm/s", font_size=VALUE_SIZE, color=WHITE,
        ).next_to(panel_stack, UP, buff=0.8).shift(RIGHT * 2)
        speed_arrow = Arrow(
            speed_label.get_left() + LEFT * 0.3,
            speed_label.get_right() + RIGHT * 0.3,
            color=WHITE, stroke_width=2, buff=0,
        )
        speed_arrow.next_to(speed_label, DOWN, buff=0.1)
        self.play(Write(speed_label), GrowArrow(speed_arrow), run_time=0.5)

        self.play(FadeOut(subtitle), run_time=0.3)

        # -- Animate blade sliding through --
        # As blade passes, EVA darkens behind it and glass separates upward
        # We simulate this with a ValueTracker controlling blade x-position

        blade_tracker = ValueTracker(eva_layer.get_left()[0] - 0.3)
        target_x = eva_layer.get_right()[0] + 0.5

        # Decomposed EVA region (dark) that grows as blade advances
        decomposed = always_redraw(
            lambda: Rectangle(
                width=max(
                    0.01,
                    blade_tracker.get_value() - eva_layer.get_left()[0],
                ),
                height=0.25,
                color=DIMMED,
                fill_color=DIMMED,
                fill_opacity=0.9,
                stroke_width=0,
            ).align_to(eva_layer, LEFT).align_to(eva_layer, DOWN)
        )

        # Glass separation: glass shifts up proportional to blade progress
        def glass_offset() -> float:
            progress = (blade_tracker.get_value() - eva_layer.get_left()[0]) / panel_width
            return max(0, min(progress, 1.0)) * 0.4

        glass.add_updater(
            lambda m: m.shift(
                UP * (glass_offset() - getattr(m, "_prev_offset", 0))
            ) or setattr(m, "_prev_offset", glass_offset())
        )
        glass._prev_offset = 0.0

        blade.add_updater(
            lambda m: m.move_to(
                [blade_tracker.get_value(), eva_layer.get_center()[1], 0]
            )
        )
        blade_label.add_updater(lambda m: m.next_to(blade, DOWN, buff=0.15))

        self.add(decomposed)
        self.play(
            blade_tracker.animate.set_value(target_x),
            run_time=4.0,
            rate_func=linear,
        )
        self.wait(frozen_frame=False)

        # Clear updaters
        glass.clear_updaters()
        blade.clear_updaters()
        blade_label.clear_updaters()

        self.wait(HOLD_SHORT)

        # -- Result labels --
        glass_result = Text("Glass (intact)", font_size=VALUE_SIZE, color=GLASS_COLOR)
        glass_result.next_to(glass, UP, buff=0.15)
        cell_result = Text("Cell layer (recoverable)", font_size=VALUE_SIZE, color=CELL_COLOR)
        cell_result.next_to(cell_layer, DOWN, buff=0.15)

        self.play(Write(glass_result), Write(cell_result), run_time=0.6)
        self.wait(HOLD_SHORT)

        # -- Bottom note --
        note = bottom_note(
            "Hot knife exploits EVA's thermal weakness: 300\u00b0C decomposes the adhesive"
        )
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(HOLD_LONG)

        fade_all(self)


# ============================================================
# SCENE 6: ROLLER CRUSH -- crushing + electrostatic separation
# ============================================================

class S06_RollerCrush(Scene):
    """Two-stage process: roller crushing, then electrostatic material separation."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        mini_cs = mini_cross_section()
        self.add(mini_cs)

        subtitle = Text(
            "Method 2: Roller Crushing + Separation",
            font_size=SUBTITLE_SIZE, color=ROLLER_COLOR,
        ).move_to(UP * TITLE_Y)
        self.play(Write(subtitle))
        self.wait(0.5)
        self.play(FadeOut(subtitle), run_time=0.3)

        # ---- STAGE A: Roller Crushing (left half) ----
        stage_a_label = Text(
            "Stage A: Controlled Crushing",
            font_size=LABEL_SIZE, color=WHITE,
        ).move_to(UP * 2.6 + LEFT * 3.2)

        # Two counter-rotating rollers
        roller_radius = 0.6
        roller_top = Circle(
            radius=roller_radius, color=FRAME_COLOR,
            fill_color=FRAME_COLOR, fill_opacity=0.4,
        ).move_to(LEFT * 3.5 + UP * 0.7)
        roller_bot = Circle(
            radius=roller_radius, color=FRAME_COLOR,
            fill_color=FRAME_COLOR, fill_opacity=0.4,
        ).move_to(LEFT * 3.5 + DOWN * 0.7)

        # Rotation arrows
        rot_top = Arc(
            radius=0.35, start_angle=30 * DEGREES, angle=240 * DEGREES,
            color=WHITE, stroke_width=2,
        ).move_to(roller_top).add_tip(tip_length=0.12)
        rot_bot = Arc(
            radius=0.35, start_angle=210 * DEGREES, angle=240 * DEGREES,
            color=WHITE, stroke_width=2,
        ).move_to(roller_bot).add_tip(tip_length=0.12)

        # Panel going in from left
        panel_in = Rectangle(
            width=1.8, height=0.3, color=GLASS_COLOR,
            fill_color=GLASS_COLOR, fill_opacity=0.6,
        ).move_to(LEFT * 5.5)

        # Fragments coming out right
        fragment_colors = [GLASS_COLOR, GLASS_COLOR, CELL_COLOR, BACKSHEET_COLOR, GLASS_COLOR]
        fragments = VGroup()
        for i, fc in enumerate(fragment_colors):
            frag = Rectangle(
                width=np.random.uniform(0.15, 0.35),
                height=np.random.uniform(0.08, 0.15),
                color=fc, fill_color=fc, fill_opacity=0.7,
            ).move_to(LEFT * 1.8 + RIGHT * i * 0.35 + UP * np.random.uniform(-0.4, 0.4))
            frag.rotate(np.random.uniform(-30, 30) * DEGREES)
            fragments.add(frag)

        rollers = VGroup(roller_top, roller_bot, rot_top, rot_bot)

        self.play(Write(stage_a_label), run_time=0.4)
        self.play(FadeIn(rollers), run_time=0.5)

        # Animate panel feeding through
        self.play(FadeIn(panel_in, shift=RIGHT * 0.3), run_time=0.3)
        self.play(
            panel_in.animate.move_to(LEFT * 3.5),
            run_time=0.8,
        )
        # Panel "shatters" into fragments
        self.play(
            FadeOut(panel_in),
            LaggedStart(*[FadeIn(f, shift=RIGHT * 0.3) for f in fragments], lag_ratio=0.1),
            run_time=0.8,
        )
        self.wait(HOLD_SHORT)

        # ---- Arrow connecting stages ----
        connecting_arrow = Arrow(
            LEFT * 1.0, RIGHT * 0.2,
            color=WHITE, stroke_width=3, buff=0,
        ).move_to(RIGHT * -0.4)
        self.play(GrowArrow(connecting_arrow), run_time=0.4)

        # ---- STAGE B: Electrostatic Separation (right half) ----
        stage_b_label = Text(
            "Stage B: Electrostatic Separation",
            font_size=LABEL_SIZE, color=WHITE,
        ).move_to(UP * 2.6 + RIGHT * 3.2)

        # Two parallel plates (capacitor)
        plate_top = Rectangle(
            width=3.0, height=0.1, color=DANGER,
            fill_color=DANGER, fill_opacity=0.6,
        ).move_to(RIGHT * 3.0 + UP * 1.2)
        plus_label = Text("+", font_size=BODY_SIZE, color=DANGER)
        plus_label.next_to(plate_top, LEFT, buff=0.15)

        plate_bot = Rectangle(
            width=3.0, height=0.1, color=HEAT_LOW,
            fill_color=HEAT_LOW, fill_opacity=0.6,
        ).move_to(RIGHT * 3.0 + DOWN * 1.2)
        minus_label = Text("-", font_size=BODY_SIZE, color=HEAT_LOW)
        minus_label.next_to(plate_bot, LEFT, buff=0.15)

        # Conveyor belt line
        conveyor = Line(
            RIGHT * 1.5, RIGHT * 4.8,
            color=FRAME_COLOR, stroke_width=3,
        ).move_to(RIGHT * 3.0 + DOWN * 0.0)

        # Bins at bottom
        bin_width = 0.9
        glass_bin = Rectangle(
            width=bin_width, height=0.6, color=GLASS_COLOR,
            fill_color=GLASS_COLOR, fill_opacity=0.3,
        ).move_to(RIGHT * 2.0 + DOWN * 2.2)
        glass_bin_label = Text("Glass\n95%", font_size=14, color=GLASS_COLOR)
        glass_bin_label.next_to(glass_bin, DOWN, buff=0.08)

        si_bin = Rectangle(
            width=bin_width, height=0.6, color=CELL_COLOR,
            fill_color=CELL_COLOR, fill_opacity=0.3,
        ).move_to(RIGHT * 3.2 + DOWN * 2.2)
        si_bin_label = Text("Si\n85%", font_size=14, color=CELL_COLOR)
        si_bin_label.next_to(si_bin, DOWN, buff=0.08)

        cu_bin = Rectangle(
            width=bin_width, height=0.6, color=COPPER_COLOR,
            fill_color=COPPER_COLOR, fill_opacity=0.3,
        ).move_to(RIGHT * 4.4 + DOWN * 2.2)
        cu_bin_label = Text("Cu\n90%", font_size=14, color=COPPER_COLOR)
        cu_bin_label.next_to(cu_bin, DOWN, buff=0.08)

        separator = VGroup(
            plate_top, plus_label, plate_bot, minus_label,
            conveyor,
            glass_bin, glass_bin_label,
            si_bin, si_bin_label,
            cu_bin, cu_bin_label,
        )

        self.play(Write(stage_b_label), run_time=0.4)
        self.play(FadeIn(separator), run_time=0.8)

        # Animate fragments falling into bins
        # Glass fragment falls straight
        glass_dot = Dot(color=GLASS_COLOR, radius=0.1).move_to(RIGHT * 2.0 + UP * 0.0)
        self.play(FadeIn(glass_dot), run_time=0.2)
        self.play(glass_dot.animate.move_to(glass_bin.get_top()), run_time=0.5)
        self.play(FadeOut(glass_dot), run_time=0.1)

        # Si fragment deflects toward + plate then falls
        si_dot = Dot(color=CELL_COLOR, radius=0.1).move_to(RIGHT * 3.0 + UP * 0.0)
        self.play(FadeIn(si_dot), run_time=0.2)
        self.play(
            si_dot.animate.move_to(RIGHT * 3.2 + UP * 0.4),
            run_time=0.3,
        )
        self.play(si_dot.animate.move_to(si_bin.get_top()), run_time=0.4)
        self.play(FadeOut(si_dot), run_time=0.1)

        # Cu fragment deflects more
        cu_dot = Dot(color=COPPER_COLOR, radius=0.1).move_to(RIGHT * 4.0 + UP * 0.0)
        self.play(FadeIn(cu_dot), run_time=0.2)
        self.play(
            cu_dot.animate.move_to(RIGHT * 4.4 + UP * 0.5),
            run_time=0.3,
        )
        self.play(cu_dot.animate.move_to(cu_bin.get_top()), run_time=0.4)
        self.play(FadeOut(cu_dot), run_time=0.1)

        self.wait(HOLD_SHORT)

        # -- Bottom note --
        note = bottom_note("Throughput: ~20 panels/hour -- faster but lower cell integrity")
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(HOLD_LONG)

        fade_all(self)


# ============================================================
# SCENE 7: RECOVERY -- grouped bar chart of recovery rates
# ============================================================

class S07_Recovery(Scene):
    """Grouped bar chart comparing recovery rates across methods."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        title = section_title("Material Recovery Rates by Method")
        self.play(Write(title))
        self.wait(0.5)

        # -- Data --
        materials = ["Glass", "Silicon", "Silver", "Copper"]
        hot_knife_vals = [95, 85, 80, 88]
        roller_vals = [98, 70, 60, 90]
        chemical_vals = [90, 95, 92, 85]

        # -- Manual grouped bar chart --
        # Axes
        axes = Axes(
            x_range=[0, 4.5, 1],
            y_range=[0, 105, 20],
            x_length=10,
            y_length=4.5,
            axis_config={"include_numbers": False, "font_size": 16},
            y_axis_config={"include_numbers": True},
            tips=False,
        ).move_to(DOWN * 0.2)

        y_label = Text("Recovery (%)", font_size=18)
        y_label.next_to(axes.y_axis, LEFT, buff=0.3).rotate(90 * DEGREES)

        self.play(FadeOut(title), run_time=0.3)

        chart_title = Text(
            "Material Recovery Rates by Method",
            font_size=SUBTITLE_SIZE, color=WHITE,
        ).to_edge(UP, buff=0.35)
        self.play(Write(chart_title), run_time=0.5)
        self.play(Create(axes), Write(y_label), run_time=0.8)

        # Bar parameters
        bar_width = 0.28
        group_spacing = 2.2
        intra_spacing = 0.33

        all_bars = VGroup()
        all_labels = VGroup()
        value_texts = VGroup()

        method_colors = [HOTKNIFE_COLOR, ROLLER_COLOR, CHEMICAL_COLOR]
        method_names = ["Hot Knife", "Roller Crush", "Chemical"]
        all_vals = [hot_knife_vals, roller_vals, chemical_vals]

        for mat_idx, mat_name in enumerate(materials):
            x_center = 0.6 + mat_idx * 1.05
            # Material label on x-axis
            mat_label = Text(mat_name, font_size=16)
            mat_label.move_to(axes.c2p(x_center, 0) + DOWN * 0.35)
            all_labels.add(mat_label)

            for method_idx in range(3):
                val = all_vals[method_idx][mat_idx]
                x_pos = x_center + (method_idx - 1) * intra_spacing

                bar = Rectangle(
                    width=bar_width,
                    height=max(0.05, val / 105 * 4.5),
                    color=method_colors[method_idx],
                    fill_color=method_colors[method_idx],
                    fill_opacity=0.75,
                    stroke_width=1,
                )
                bar.move_to(axes.c2p(x_pos, val / 2))

                val_text = Text(f"{val}%", font_size=12, color=WHITE)
                val_text.next_to(bar, UP, buff=0.05)

                all_bars.add(bar)
                value_texts.add(val_text)

        # Animate bars in groups
        self.play(
            LaggedStart(*[FadeIn(l) for l in all_labels], lag_ratio=0.1),
            run_time=0.5,
        )
        self.play(
            LaggedStart(
                *[GrowFromEdge(b, DOWN) for b in all_bars],
                lag_ratio=0.04,
            ),
            run_time=2.0,
        )
        self.play(
            LaggedStart(*[FadeIn(v) for v in value_texts], lag_ratio=0.03),
            run_time=1.0,
        )
        self.wait(HOLD_SHORT)

        # -- Legend --
        legend = VGroup()
        for i, (name, color) in enumerate(zip(method_names, method_colors)):
            dot = Square(side_length=0.2, color=color, fill_color=color, fill_opacity=0.75)
            lbl = Text(name, font_size=16, color=color)
            entry = VGroup(dot, lbl).arrange(RIGHT, buff=0.15)
            legend.add(entry)
        legend.arrange(RIGHT, buff=0.6)
        legend.next_to(axes, DOWN, buff=0.7)
        self.play(FadeIn(legend), run_time=0.5)
        self.wait(HOLD_SHORT)

        # -- Highlight trade-offs --
        # Hot knife Si (85%) vs Roller Si (70%) -- index: Si is mat_idx=1
        # Hot knife Si bar: all_bars[1*3 + 0] = all_bars[3]
        # Roller Si bar: all_bars[1*3 + 1] = all_bars[4]
        hk_si_bar = all_bars[3]
        ro_si_bar = all_bars[4]
        si_highlight = SurroundingRectangle(
            VGroup(hk_si_bar, ro_si_bar), color=HIGHLIGHT, buff=0.08
        )
        si_note = Text(
            "Hot knife preserves\nwafer integrity",
            font_size=16, color=HIGHLIGHT,
        )
        si_note.next_to(si_highlight, RIGHT, buff=0.2)
        if si_note.get_right()[0] > 5.5:
            si_note.next_to(si_highlight, UP, buff=0.15)

        self.play(Create(si_highlight), Write(si_note), run_time=0.8)
        self.wait(HOLD_MEDIUM)
        self.play(FadeOut(si_highlight), FadeOut(si_note), run_time=0.4)

        # Roller glass (98%) vs Hot knife glass (95%)
        hk_gl_bar = all_bars[0]
        ro_gl_bar = all_bars[1]
        gl_highlight = SurroundingRectangle(
            VGroup(hk_gl_bar, ro_gl_bar), color=GLASS_COLOR, buff=0.08
        )
        gl_note = Text(
            "Roller maximizes\nglass yield",
            font_size=16, color=GLASS_COLOR,
        )
        gl_note.next_to(gl_highlight, LEFT, buff=0.2)

        self.play(Create(gl_highlight), Write(gl_note), run_time=0.8)
        self.wait(HOLD_MEDIUM)
        self.play(FadeOut(gl_highlight), FadeOut(gl_note), run_time=0.4)

        # -- Bottom note --
        note = bottom_note("No single method wins everywhere -- hybrid approaches emerging")
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(HOLD_LONG)

        fade_all(self)


# ============================================================
# SCENE 8: CIRCULAR -- closing with design for deconstruction
# ============================================================

class S08_Circular(Scene):
    """Panel reassembles, text morphs, circular economy message."""

    def construct(self) -> None:
        self.camera.background_color = BG_COLOR

        # -- Exploded layers reassemble --
        layer_data = [
            ("Backsheet", BACKSHEET_COLOR, 0.35),
            ("EVA", EVA_COLOR, 0.4),
            ("Si Cells", CELL_COLOR, 0.5),
            ("EVA", EVA_COLOR, 0.4),
            ("Glass", GLASS_COLOR, 1.0),
        ]

        exploded = VGroup()
        spread_positions = [
            DOWN * 2.0, DOWN * 1.0, ORIGIN, UP * 1.0, UP * 2.2,
        ]
        for (name, color, h), pos in zip(layer_data, spread_positions):
            rect = Rectangle(
                width=4.0, height=h, color=color,
                fill_color=color, fill_opacity=0.7, stroke_width=1.5,
            )
            lbl = Text(name, font_size=16, color=WHITE).move_to(rect)
            layer = VGroup(rect, lbl)
            layer.move_to(pos)
            exploded.add(layer)

        self.play(
            LaggedStart(*[FadeIn(l) for l in exploded], lag_ratio=0.1),
            run_time=1.0,
        )
        self.wait(HOLD_SHORT)

        # Reassemble: all layers converge to center
        assembled = VGroup()
        for name, color, h in layer_data:
            rect = Rectangle(
                width=4.0, height=h * 0.5, color=color,
                fill_color=color, fill_opacity=0.7, stroke_width=1,
            )
            assembled.add(rect)
        assembled.arrange(UP, buff=0.01)
        assembled.move_to(ORIGIN)

        self.play(
            *[
                layer.animate.move_to(target.get_center()).set(
                    height=target.height, width=target.width
                )
                for layer, target in zip(exploded, assembled)
            ],
            run_time=1.5,
        )
        self.wait(HOLD_SHORT)

        # -- Text morph --
        text_service = Text(
            "25 years of service",
            font_size=BODY_SIZE, color=WHITE,
        ).next_to(assembled, UP, buff=0.5)
        self.play(Write(text_service), run_time=0.8)
        self.wait(HOLD_SHORT)

        text_second = Text(
            "Then a second life for every layer",
            font_size=BODY_SIZE, color=POSITIVE,
        ).next_to(assembled, UP, buff=0.5)
        self.play(ReplacementTransform(text_service, text_second), run_time=1.0)
        self.wait(HOLD_MEDIUM)

        # -- Circular arrow around the panel --
        self.play(FadeOut(text_second), run_time=0.3)

        # Shrink panel to make room for circular arrow
        panel_icon = VGroup(*[l[0] if isinstance(l, VGroup) else l for l in exploded])
        self.play(panel_icon.animate.scale(0.6).move_to(ORIGIN), run_time=0.5)

        circle_arrow = Arc(
            radius=1.8, start_angle=60 * DEGREES, angle=300 * DEGREES,
            color=POSITIVE, stroke_width=4,
        ).add_tip(tip_length=0.2)
        circle_arrow.move_to(ORIGIN)

        final_text = Text(
            "Design for Deconstruction",
            font_size=TITLE_SIZE, color=POSITIVE, weight=BOLD,
        ).next_to(circle_arrow, DOWN, buff=0.6)

        self.play(Create(circle_arrow), run_time=1.2)
        self.play(Write(final_text), run_time=1.0)
        self.wait(HOLD_LONG)