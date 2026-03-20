"""Scene 01: What is a Process? -- Coffee shop 3-station pipeline with flowing dots."""
from manim import *

from style import *

# -- Customer dot colors --
DOT_COLORS = [FLOW_BLUE, RATE_GREEN, TIME_ORANGE, BOTTLENECK_RED]


class WhatIsAProcess(Scene):
    def construct(self) -> None:
        # ---- Title ----
        title = section_title("What is a Process?")
        self.play(Write(title))
        self.wait(0.5)

        # ---- Build 3-station pipeline ----
        order_stn = make_station("Order", "2 min", color=STATION_FILL)
        make_stn = make_station("Make", "5 min", color=STATION_FILL)
        serve_stn = make_station("Serve", "1 min", color=STATION_FILL)

        # Arrange horizontally, centered at ORIGIN
        stations = VGroup(order_stn, make_stn, serve_stn).arrange(RIGHT, buff=1.5)
        stations.move_to(ORIGIN)

        arrow_1 = connect_stations(order_stn, make_stn)
        arrow_2 = connect_stations(make_stn, serve_stn)
        arrows = VGroup(arrow_1, arrow_2)

        # Animate stations appearing one by one, then arrows
        for stn in [order_stn, make_stn, serve_stn]:
            self.play(FadeIn(stn, shift=UP * 0.3), run_time=0.4)
        self.play(Create(arrow_1), Create(arrow_2), run_time=0.5)
        self.wait(0.4)

        # ---- Animate customer dots flowing through ----
        # Waypoints: left of first station -> center of each station -> right of last
        entry_x = order_stn[0].get_left()[0] - 0.8
        exit_x = serve_stn[0].get_right()[0] + 0.8
        station_centers = [
            order_stn[0].get_center(),
            make_stn[0].get_center(),
            serve_stn[0].get_center(),
        ]
        dot_y = ORIGIN[1]  # stay on same horizontal line as stations

        # Pause durations at each station (proportional to activity time)
        pause_durations = [0.25, 0.5, 0.15]

        # Create 4 dots with slight vertical offsets so they don't overlap
        dots = []
        for i, col in enumerate(DOT_COLORS):
            d = Dot(
                point=np.array([entry_x, dot_y + (i - 1.5) * 0.15, 0]),
                radius=0.12,
                color=col,
                fill_opacity=0.9,
            )
            dots.append(d)

        # Flow dots through with staggered timing
        for i, dot in enumerate(dots):
            self.play(FadeIn(dot, shift=RIGHT * 0.3), run_time=0.25)

            # Animate through each station
            for j, center in enumerate(station_centers):
                self.play(
                    dot.animate(run_time=0.35).move_to(
                        center + UP * (i - 1.5) * 0.15
                    ),
                )
                self.wait(pause_durations[j])

            # Exit right
            self.play(
                dot.animate(run_time=0.3).move_to(
                    np.array([exit_x, dot_y + (i - 1.5) * 0.15, 0])
                ),
            )
            self.play(FadeOut(dot), run_time=0.2)

        self.wait(0.3)

        # ---- Bottom note ----
        note = bottom_note("Any sequence of activities that transforms inputs into outputs")
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.5)
        self.wait(1.5)

        # ---- Cleanup: FadeOut everything ----
        fade_all(self, title, stations, arrows, note)
        self.wait(0.3)
