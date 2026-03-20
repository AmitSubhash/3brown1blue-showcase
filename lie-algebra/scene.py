"""Lie Groups & Lie Algebras - From First Principles.

One continuous scene: rotations on a circle -> tangent space ->
generators -> the bracket -> why physicists care.
"""

from manim import *
import numpy as np
from style import *


class LieAlgebra(Scene):
    """The full explainer: what are Lie groups/algebras, visually."""

    def construct(self) -> None:

        # ════════════════════════════════════════════════════════
        # HOOK
        # ════════════════════════════════════════════════════════
        self.next_section("Hook")

        hook = Text(
            "Every symmetry in physics\ncomes from a Lie group.",
            font_size=BODY_SIZE, color=C["highlight"], line_spacing=1.4,
        )
        self.play(FadeIn(hook, shift=UP * 0.3))
        self.wait(HOLD)

        hook2 = Text(
            "Rotations. Gauge fields. Spacetime.\nAll the same math.",
            font_size=BODY_SIZE, color=C["label"], line_spacing=1.4,
        )
        self.play(ReplacementTransform(hook, hook2))
        self.wait(HOLD)
        self.play(FadeOut(hook2))

        # ════════════════════════════════════════════════════════
        # PART 1: The Circle Group SO(2)
        # ════════════════════════════════════════════════════════
        self.next_section("CircleGroup")

        title = Text("Start Simple: Rotations in 2D", font_size=TITLE_SIZE)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.scale(0.5).to_corner(UL))

        # Draw unit circle
        circle = Circle(radius=2, color=C["group"], stroke_width=3)
        dot = Dot(circle.point_at_angle(0), color=C["highlight"], radius=0.12)
        angle_label = always_redraw(
            lambda: Text(
                f"{np.degrees(np.arctan2(dot.get_center()[1], dot.get_center()[0])):.0f}°",
                font_size=LABEL_SIZE, color=C["highlight"],
            ).next_to(dot, UR, buff=0.15)
        )

        self.play(Create(circle))
        self.play(FadeIn(dot), Write(angle_label))
        self.wait(1)

        # Rotate the dot around the circle
        tracker = ValueTracker(0)
        dot.add_updater(
            lambda d: d.move_to(circle.point_at_angle(tracker.get_value()))
        )

        self.play(tracker.animate.set_value(PI / 3), run_time=2, rate_func=smooth)
        self.wait(0.5)
        self.play(tracker.animate.set_value(PI), run_time=2, rate_func=smooth)
        self.wait(0.5)
        self.play(tracker.animate.set_value(2 * PI), run_time=2, rate_func=smooth)
        self.wait(1)

        # Explain: this is a GROUP
        group_text = Text(
            "All rotations form a group: SO(2)\n"
            "Compose two rotations = another rotation\n"
            "Every rotation has an inverse",
            font_size=LABEL_SIZE, color=C["label"], line_spacing=1.3,
        ).to_edge(RIGHT, buff=0.5).shift(UP * 0.5)
        self.play(Write(group_text))
        self.wait(HOLD)

        so2_label = MathTex(r"SO(2)", font_size=48, color=C["group"])
        so2_label.next_to(circle, DOWN, buff=0.5)
        self.play(Write(so2_label))
        self.wait(1)

        # Clean for next section
        dot.clear_updaters()
        self.play(FadeOut(group_text), FadeOut(angle_label))

        # ════════════════════════════════════════════════════════
        # PART 2: The Tangent Space (Lie Algebra)
        # ════════════════════════════════════════════════════════
        self.next_section("TangentSpace")

        # Move circle left
        circle_group = VGroup(circle, dot, so2_label)
        self.play(circle_group.animate.shift(LEFT * 2.5).scale(0.8))

        # Draw tangent line at identity (angle=0)
        identity_pt = circle.point_at_angle(0)
        tangent = Line(
            identity_pt + DOWN * 1.5, identity_pt + UP * 1.5,
            color=C["tangent"], stroke_width=4,
        )
        tangent_label = Text(
            "Tangent space\nat identity",
            font_size=LABEL_SIZE, color=C["tangent"], line_spacing=1.2,
        ).next_to(tangent, RIGHT, buff=0.3)

        self.play(Create(tangent))
        self.play(Write(tangent_label))
        self.wait(1)

        # Key insight
        insight = Text(
            "The tangent space at the identity\n"
            "IS the Lie algebra.",
            font_size=BODY_SIZE, color=C["highlight"],
        ).to_edge(RIGHT, buff=0.5)
        self.play(FadeIn(insight, shift=UP * 0.3))
        self.wait(HOLD)

        algebra_label = MathTex(r"\mathfrak{so}(2)", font_size=48, color=C["algebra"])
        algebra_label.next_to(tangent, DOWN, buff=0.5)
        self.play(Write(algebra_label))
        self.wait(1)

        # Arrow connecting them
        connection = CurvedArrow(
            algebra_label.get_left() + LEFT * 0.2,
            so2_label.get_right() + RIGHT * 0.2,
            color=C["highlight"], angle=-0.3,
        )
        exp_label = MathTex(r"e^{X}", font_size=LABEL_SIZE, color=C["highlight"])
        exp_label.next_to(connection, DOWN, buff=0.1)
        self.play(Create(connection), Write(exp_label))
        self.wait(1)

        exp_text = Text(
            "The exponential map\ntakes you from algebra to group",
            font_size=LABEL_SIZE, color=C["label"], line_spacing=1.2,
        ).to_edge(DOWN, buff=0.3)
        self.play(Write(exp_text))
        self.wait(HOLD)

        # Clear
        self.play(*[FadeOut(m) for m in self.mobjects if m != title])

        # ════════════════════════════════════════════════════════
        # PART 3: Generators - The DNA of Symmetry
        # ════════════════════════════════════════════════════════
        self.next_section("Generators")

        sub = Text("Generators: The DNA of Symmetry", font_size=BODY_SIZE)
        self.play(ReplacementTransform(title, sub))
        self.play(sub.animate.scale(0.7).to_corner(UL))
        self.wait(0.5)

        # SO(2) has ONE generator
        gen_eq = MathTex(
            r"R(\theta) = e^{i\theta}",
            font_size=EQ_SIZE,
        )
        self.play(Write(gen_eq))
        self.wait(1)

        gen_explain = Text(
            "SO(2) has 1 generator.\n"
            "One knob to turn = one dimension.",
            font_size=BODY_SIZE, color=C["label"],
        ).next_to(gen_eq, DOWN, buff=0.8)
        self.play(Write(gen_explain))
        self.wait(HOLD)

        self.play(FadeOut(gen_eq, gen_explain))

        # SO(3) has THREE generators
        so3_title = Text("3D rotations: SO(3)", font_size=BODY_SIZE, color=C["group"])
        self.play(Write(so3_title))
        self.play(so3_title.animate.next_to(sub, DOWN, buff=0.5).to_edge(LEFT, buff=0.5))

        generators = VGroup()
        gen_names = [
            (r"J_x", "Roll", RED),
            (r"J_y", "Pitch", GREEN),
            (r"J_z", "Yaw", BLUE),
        ]
        for i, (sym, name, color) in enumerate(gen_names):
            eq = MathTex(sym, font_size=44, color=color)
            label = Text(name, font_size=LABEL_SIZE, color=color)
            grp = VGroup(eq, label).arrange(DOWN, buff=0.2)
            generators.add(grp)
        generators.arrange(RIGHT, buff=1.5).move_to(ORIGIN)

        self.play(LaggedStart(
            *[FadeIn(g, shift=UP * 0.3) for g in generators],
            lag_ratio=0.3,
        ))
        self.wait(1)

        dim_text = Text(
            "3 generators = 3 dimensions\n"
            "dim(Lie algebra) = dim(Lie group)",
            font_size=BODY_SIZE, color=C["highlight"],
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(dim_text))
        self.wait(HOLD)

        self.play(FadeOut(generators, so3_title, dim_text))

        # ════════════════════════════════════════════════════════
        # PART 4: The Lie Bracket [X, Y]
        # ════════════════════════════════════════════════════════
        self.next_section("Bracket")

        bracket_title = Text("The Lie Bracket: [X, Y]", font_size=BODY_SIZE, color=C["algebra"])
        self.play(ReplacementTransform(sub, bracket_title))
        self.play(bracket_title.animate.scale(0.7).to_corner(UL))

        # Show the bracket equation
        bracket_eq = MathTex(
            r"[", r"X", r",", r"Y", r"]",
            r"=", r"X", r"Y", r"-", r"Y", r"X",
            font_size=EQ_SIZE,
        )
        self.play(Write(bracket_eq))
        self.wait(HOLD)

        # Dim and reveal
        self.play(bracket_eq.animate.set_opacity(0.3))

        # XY - YX
        for indices, color, text in [
            ([6, 7], BLUE, "Do Y first, then X"),
            ([9, 10], RED, "Do X first, then Y"),
            ([8], WHITE, "The DIFFERENCE tells you\nhow much order matters"),
        ]:
            parts = VGroup(*[bracket_eq[i] for i in indices])
            for p in parts:
                p.set_opacity(1.0)
            box = SurroundingRectangle(parts, color=color, buff=0.1)
            lbl = Text(text, font_size=LABEL_SIZE, color=color)
            lbl.next_to(box, DOWN, buff=0.3)
            self.play(Create(box), Write(lbl))
            self.wait(1.5)
            self.play(FadeOut(box), FadeOut(lbl))
            for p in parts:
                p.set_color(color)

        self.play(bracket_eq.animate.set_opacity(1.0))
        self.wait(1)

        # Physical meaning
        phys = Text(
            "For rotations:\n"
            "[Jx, Jy] = Jz\n\n"
            "Rotating around X then Y\n"
            "differs from Y then X\n"
            "by a rotation around Z!",
            font_size=LABEL_SIZE, color=C["label"], line_spacing=1.3,
        ).to_edge(RIGHT, buff=0.5)
        self.play(Write(phys))
        self.wait(HOLD + 1)

        self.play(FadeOut(bracket_eq, phys))

        # ════════════════════════════════════════════════════════
        # PART 5: Why Physicists Care
        # ════════════════════════════════════════════════════════
        self.next_section("WhyCare")

        why = Text("Why This Matters", font_size=TITLE_SIZE, color=WHITE)
        self.play(ReplacementTransform(bracket_title, why))
        self.play(why.animate.to_edge(UP, buff=0.5))

        applications = [
            ("U(1)", "Electromagnetism", "1 generator = photon"),
            ("SU(2)", "Weak nuclear force", "3 generators = W+, W-, Z bosons"),
            ("SU(3)", "Strong nuclear force", "8 generators = 8 gluons"),
        ]

        app_groups = VGroup()
        for sym, force, detail in applications:
            sym_tex = MathTex(sym, font_size=36, color=C["group"])
            force_text = Text(force, font_size=BODY_SIZE, color=WHITE)
            detail_text = Text(detail, font_size=LABEL_SIZE, color=C["label"])
            grp = VGroup(sym_tex, force_text, detail_text).arrange(DOWN, buff=0.15)
            app_groups.add(grp)
        app_groups.arrange(RIGHT, buff=1.0).move_to(ORIGIN)

        self.play(LaggedStart(
            *[FadeIn(g, shift=UP * 0.3) for g in app_groups],
            lag_ratio=0.4, run_time=3,
        ))
        self.wait(HOLD)

        punchline = Text(
            "The generators of the symmetry group\n"
            "ARE the force-carrying particles.",
            font_size=BODY_SIZE, color=C["highlight"],
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(punchline))
        self.wait(HOLD + 1)

        # ════════════════════════════════════════════════════════
        # FINALE
        # ════════════════════════════════════════════════════════
        self.next_section("Finale")

        self.play(FadeOut(app_groups, punchline, why))

        summary_eq = MathTex(
            r"\text{Lie Group}",
            r"\xrightarrow{\log}",
            r"\text{Lie Algebra}",
            r"\xrightarrow{\text{generators}}",
            r"\text{Physics}",
            font_size=36,
        )
        summary_eq[0].set_color(C["group"])
        summary_eq[2].set_color(C["algebra"])
        summary_eq[4].set_color(C["highlight"])
        self.play(Write(summary_eq, run_time=3))
        self.wait(1)

        final = Text(
            "Symmetry is not just beautiful.\nIt is the language of nature.",
            font_size=BODY_SIZE, color=C["highlight"], line_spacing=1.4,
        ).next_to(summary_eq, DOWN, buff=1)
        self.play(Write(final))
        self.wait(3)

        self.play(*[FadeOut(m) for m in self.mobjects])
