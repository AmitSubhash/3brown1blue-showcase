"""Scene 06 -- Utilization and Waiting (DUAL_PANEL template).

Left panel: bar chart of station utilization (A=50%, B=80%, C=40%).
Right panel: hockey-stick curve showing waiting time vs utilization.
Key insight: waiting time explodes as utilization approaches 100%.
"""

from manim import *

from style import *


class UtilizationAndWaiting(Scene):
    def construct(self) -> None:
        # ── Title ──────────────────────────────────────────────────────
        title = section_title("Utilization and Waiting")
        self.play(Write(title))
        self.wait(0.5)

        # ── Divider ───────────────────────────────────────────────────
        divider = DashedLine(
            start=UP * 2.5, end=DOWN * 2.5,
            dash_length=0.15, color=DIMMED, stroke_width=1.5,
        )
        self.play(Create(divider), run_time=0.5)

        # ==============================================================
        # LEFT PANEL: Utilization Bar Chart  x in [-6, -0.8]
        # ==============================================================
        left_subtitle = safe_text(
            "Utilization", font_size=HEADING_SIZE, color=RATE_GREEN,
        )
        left_subtitle.move_to(np.array([-3.4, 2.2, 0]))
        self.play(Write(left_subtitle), run_time=0.6)

        # Axes for bar chart
        left_ax = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 100, 20],
            x_length=4.0,
            y_length=3.2,
            axis_config={"color": WHITE, "stroke_width": 2, "include_ticks": True},
            y_axis_config={
                "numbers_to_include": [0, 20, 40, 60, 80, 100],
                "font_size": 18,
            },
            tips=False,
        )
        left_ax.move_to(np.array([-3.4, -0.1, 0]))

        # Y-axis label
        y_label = label_text("%", color=WHITE)
        y_label.next_to(left_ax.y_axis, UP, buff=0.15)

        self.play(Create(left_ax), FadeIn(y_label), run_time=0.8)

        # Station utilization data
        bar_data = [
            {"name": "A", "util": 50, "color": RATE_GREEN},
            {"name": "B", "util": 80, "color": BOTTLENECK_RED},
            {"name": "C", "util": 40, "color": RATE_GREEN},
        ]

        bars: list[Rectangle] = []
        bar_labels: list[Text] = []
        bar_pct_labels: list[Text] = []

        bar_width = 0.7

        for i, bd in enumerate(bar_data):
            # Bar bottom at y=0, height proportional to utilization
            x_pos = i + 1  # x positions 1, 2, 3 on the axes
            bottom_point = left_ax.c2p(x_pos, 0)
            top_point = left_ax.c2p(x_pos, bd["util"])
            bar_height = top_point[1] - bottom_point[1]

            bar = Rectangle(
                width=bar_width,
                height=bar_height,
                fill_color=bd["color"],
                fill_opacity=0.75,
                color=bd["color"],
                stroke_width=1.5,
            )
            bar.move_to(bottom_point + UP * bar_height / 2)
            bars.append(bar)

            # Station label below bar
            stn_label = label_text(bd["name"], color=WHITE)
            stn_label.next_to(bar, DOWN, buff=0.15)
            bar_labels.append(stn_label)

            # Percentage label on top of bar
            pct_label = label_text(f"{bd['util']}%", color=bd["color"])
            pct_label.next_to(bar, UP, buff=0.1)
            bar_pct_labels.append(pct_label)

        # Dashed line at 100%
        max_left = left_ax.c2p(0, 100)
        max_right = left_ax.c2p(4, 100)
        max_line = DashedLine(
            start=max_left, end=max_right,
            dash_length=0.12, color=ACCENT, stroke_width=2,
        )
        max_label = label_text("Max", color=ACCENT)
        max_label.next_to(max_line, RIGHT, buff=0.15)

        # Animate bars growing from bottom
        bar_anims = []
        for bar in bars:
            bar.save_state()
            bar.stretch(0, 1, about_edge=DOWN)
            bar_anims.append(Restore(bar))

        self.play(
            LaggedStart(*bar_anims, lag_ratio=0.3),
            run_time=1.2,
        )
        self.play(
            LaggedStart(
                *[FadeIn(lbl) for lbl in bar_labels],
                lag_ratio=0.15,
            ),
            LaggedStart(
                *[FadeIn(pct) for pct in bar_pct_labels],
                lag_ratio=0.15,
            ),
            run_time=0.8,
        )
        self.play(Create(max_line), FadeIn(max_label), run_time=0.6)
        self.wait(0.4)

        # Equation below left axes
        eq = MathTex(
            r"\text{Utilization} = \frac{R}{\text{Capacity}}",
            font_size=SMALL_EQ,
            color=WHITE,
        )
        eq.next_to(left_ax, DOWN, buff=0.5)
        # Clamp within left panel bounds
        if eq.get_right()[0] > -0.8:
            eq.shift(LEFT * (eq.get_right()[0] - (-0.9)))
        self.play(Write(eq), run_time=0.8)
        self.wait(0.5)

        # ==============================================================
        # RIGHT PANEL: Hockey-Stick Curve   x in [0.8, 6]
        # ==============================================================
        right_subtitle = safe_text(
            "Waiting Time", font_size=HEADING_SIZE, color=TIME_ORANGE,
        )
        right_subtitle.move_to(np.array([3.4, 2.2, 0]))
        self.play(Write(right_subtitle), run_time=0.6)

        # Axes for waiting-time curve
        right_ax = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 10, 2],
            x_length=4.0,
            y_length=3.2,
            axis_config={"color": WHITE, "stroke_width": 2, "include_ticks": True},
            x_axis_config={
                "numbers_to_include": [0, 20, 40, 60, 80, 100],
                "font_size": 18,
            },
            tips=False,
        )
        right_ax.move_to(np.array([3.4, -0.1, 0]))

        # Axis labels
        x_ax_label = label_text("Utilization %", color=WHITE)
        x_ax_label.scale(0.8)
        x_ax_label.next_to(right_ax.x_axis, DOWN, buff=0.35)

        y_ax_label = label_text("Wait", color=WHITE)
        y_ax_label.next_to(right_ax.y_axis, UP, buff=0.15)

        self.play(Create(right_ax), FadeIn(x_ax_label), FadeIn(y_ax_label), run_time=0.8)

        # Hockey-stick curve: y = 1/(1 - x/100) - 1, clipped at x=95
        # Scale so it fits nicely: at x=80 -> y=4, at x=95 -> y=19 (clip to ~9)
        def waiting_func(x: float) -> float:
            """Waiting time proportional to rho/(1-rho) where rho = x/100."""
            rho = x / 100.0
            if rho >= 0.95:
                rho = 0.95
            return rho / (1.0 - rho)

        # We need to scale the output to fit y_range [0, 10]
        # At rho=0.95: 0.95/0.05 = 19, so let's scale by 0.5
        def scaled_waiting(x: float) -> float:
            return min(waiting_func(x) * 0.5, 9.5)

        curve = right_ax.plot(
            scaled_waiting,
            x_range=[0, 95, 1],
            color=TIME_ORANGE,
            stroke_width=3,
        )

        self.play(Create(curve), run_time=1.5)
        self.wait(0.3)

        # Operating point at x=80%
        op_x = 80
        op_y = scaled_waiting(op_x)
        op_point = right_ax.c2p(op_x, op_y)

        op_dot = Dot(
            point=op_point, radius=0.12,
            color=QUEUE_YELLOW, fill_opacity=1.0,
        )

        # Vertical dashed line from dot down to x-axis
        x_axis_point = right_ax.c2p(op_x, 0)
        vert_dash = DashedLine(
            start=op_point, end=x_axis_point,
            dash_length=0.1, color=QUEUE_YELLOW, stroke_width=2,
        )

        # Label for the operating point
        op_label = label_text("B: 80%", color=QUEUE_YELLOW)
        op_label.next_to(op_dot, UR, buff=0.15)
        # Make sure label stays in bounds
        if op_label.get_right()[0] > 5.5:
            op_label.next_to(op_dot, UL, buff=0.15)

        self.play(
            FadeIn(op_dot, scale=1.5),
            Create(vert_dash),
            FadeIn(op_label),
            run_time=0.8,
        )
        self.play(Indicate(op_dot, color=QUEUE_YELLOW, scale_factor=1.8), run_time=0.8)
        self.wait(0.5)

        # ── Bottom Note ───────────────────────────────────────────────
        note = bottom_note(
            "As utilization approaches 100%, waiting time explodes"
        )
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.6)
        self.wait(2.0)

        # ── Cleanup ───────────────────────────────────────────────────
        all_elements = VGroup(
            title, divider,
            left_subtitle, left_ax, y_label,
            *bars, *bar_labels, *bar_pct_labels,
            max_line, max_label, eq,
            right_subtitle, right_ax, x_ax_label, y_ax_label,
            curve, op_dot, vert_dash, op_label,
            note,
        )
        self.play(FadeOut(all_elements), run_time=1.0)
        self.wait(0.3)
