"""Scene 07: Optimization Strategies -- Three techniques to improve process throughput."""
from manim import *

from style import *


class OptimizationTechniques(Scene):
    """Three BUILD_UP phases: reduce bottleneck, add parallel server, line balancing."""

    def construct(self) -> None:
        # ---- Title ----
        title = section_title("Optimization Strategies")
        self.play(Write(title))
        self.wait(0.5)
        self.play(FadeOut(title))
        self.wait(0.3)

        # ======== Phase 1: Reduce Bottleneck Time ========
        self._phase_reduce_bottleneck()

        # ======== Phase 2: Add Parallel Server ========
        self._phase_parallel_server()

        # ======== Phase 3: Line Balancing ========
        self._phase_line_balancing()

    # -----------------------------------------------------------------
    # Helpers to build + connect the standard 3-station process
    # -----------------------------------------------------------------
    def _build_process(
        self,
        a_time: str = "5 min",
        b_time: str = "8 min",
        c_time: str = "4 min",
        b_color: str = BOTTLENECK_RED,
    ) -> tuple[VGroup, VGroup, VGroup, Arrow, Arrow]:
        """Return (station_a, station_b, station_c, arrow_ab, arrow_bc)."""
        station_a = make_station("A", a_time, color=STATION_FILL)
        station_b = make_station("B", b_time, color=b_color)
        station_c = make_station("C", c_time, color=STATION_FILL)

        row = VGroup(station_a, station_b, station_c).arrange(RIGHT, buff=1.8)
        row.move_to(UP * 0.3)

        arrow_ab = connect_stations(station_a, station_b)
        arrow_bc = connect_stations(station_b, station_c)

        return station_a, station_b, station_c, arrow_ab, arrow_bc

    def _show_process(
        self,
        station_a: VGroup,
        station_b: VGroup,
        station_c: VGroup,
        arrow_ab: Arrow,
        arrow_bc: Arrow,
    ) -> None:
        """Fade in all three stations and arrows."""
        self.play(
            FadeIn(station_a, shift=UP * 0.3),
            FadeIn(station_b, shift=UP * 0.3),
            FadeIn(station_c, shift=UP * 0.3),
            run_time=0.6,
        )
        self.play(GrowArrow(arrow_ab), GrowArrow(arrow_bc), run_time=0.4)

    # -----------------------------------------------------------------
    # Phase 1: Reduce Bottleneck Time
    # -----------------------------------------------------------------
    def _phase_reduce_bottleneck(self) -> None:
        heading = safe_text(
            "1. Reduce Bottleneck Time", font_size=HEADING_SIZE, color=FLOW_BLUE
        )
        heading.to_edge(UP, buff=0.5)
        self.play(Write(heading))
        self.wait(0.3)

        # Build the original process: A=5, B=8 (red), C=4
        sa, sb, sc, ab, bc = self._build_process()
        self._show_process(sa, sb, sc, ab, bc)
        self.wait(0.5)

        # Highlight B's border
        sb_rect = sb[0]
        self.play(sb_rect.animate.set_stroke(BOTTLENECK_RED, width=4), run_time=0.4)
        self.wait(0.4)

        # Animate B's time text changing: "8 min" -> "5 min"
        old_time = sb[2]  # time_label is index 2 in make_station VGroup
        new_time = Text("5 min", font_size=18, color=ACCENT)
        new_time.move_to(old_time.get_center())

        self.play(
            Transform(old_time, new_time),
            sb_rect.animate.set_fill(OPTIMIZE_GREEN, opacity=0.8)
            .set_stroke(WHITE, width=2),
            run_time=0.8,
        )
        self.wait(0.3)

        # Label below the process
        improve_label = safe_text(
            "Improve the slowest step",
            font_size=LABEL_SIZE,
            color=OPTIMIZE_GREEN,
        )
        improve_label.next_to(
            VGroup(sa, sb, sc), DOWN, buff=0.6
        )
        self.play(FadeIn(improve_label, shift=UP * 0.2), run_time=0.5)
        self.wait(1.5)

        # Cleanup
        fade_all(self, heading, sa, sb, sc, ab, bc, improve_label)
        self.wait(0.3)

    # -----------------------------------------------------------------
    # Phase 2: Add Parallel Server
    # -----------------------------------------------------------------
    def _phase_parallel_server(self) -> None:
        heading = safe_text(
            "2. Add Parallel Server", font_size=HEADING_SIZE, color=FLOW_BLUE
        )
        heading.to_edge(UP, buff=0.5)
        self.play(Write(heading))
        self.wait(0.3)

        # Build original process again
        sa, sb, sc, ab, bc = self._build_process()
        self._show_process(sa, sb, sc, ab, bc)
        self.wait(0.5)

        # Highlight B
        sb_rect = sb[0]
        self.play(sb_rect.animate.set_stroke(BOTTLENECK_RED, width=4), run_time=0.4)
        self.wait(0.3)

        # Create a second station B' below B
        sb_prime = make_station("B'", "8 min", color=BOTTLENECK_RED)
        sb_prime.next_to(sb, DOWN, buff=0.8)

        self.play(FadeIn(sb_prime, shift=DOWN * 0.4), run_time=0.6)
        self.wait(0.3)

        # Split arrow from A to B and B'
        # Remove old arrow A->B, create two new ones
        split_top = Arrow(
            sa[0].get_right(), sb[0].get_left(),
            buff=0.1, color=WHITE, stroke_width=3,
        )
        split_bot = Arrow(
            sa[0].get_right(), sb_prime[0].get_left(),
            buff=0.1, color=WHITE, stroke_width=3,
        )

        # Merge arrows from B and B' to C
        merge_top = Arrow(
            sb[0].get_right(), sc[0].get_left(),
            buff=0.1, color=WHITE, stroke_width=3,
        )
        merge_bot = Arrow(
            sb_prime[0].get_right(), sc[0].get_left(),
            buff=0.1, color=WHITE, stroke_width=3,
        )

        self.play(
            ReplacementTransform(ab, split_top),
            GrowArrow(split_bot),
            ReplacementTransform(bc, merge_top),
            GrowArrow(merge_bot),
            run_time=0.7,
        )
        self.wait(0.3)

        # Combined capacity label between B and B'
        combined_label = safe_text(
            "Combined: 15/hr", font_size=LABEL_SIZE, color=RATE_GREEN
        )
        combined_label.next_to(
            VGroup(sb, sb_prime), RIGHT, buff=0.3
        )
        # Shift left if it would exceed safe bounds
        if combined_label.get_right()[0] > 5.5:
            combined_label.next_to(VGroup(sb, sb_prime), DOWN, buff=0.3)

        self.play(FadeIn(combined_label, shift=LEFT * 0.2), run_time=0.5)
        self.wait(0.3)

        # Bottom note
        note = bottom_note("Double the capacity at the bottleneck")
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.5)
        self.wait(1.5)

        # Cleanup
        fade_all(
            self, heading, sa, sb, sc, sb_prime,
            split_top, split_bot, merge_top, merge_bot,
            combined_label, note,
        )
        self.wait(0.3)

    # -----------------------------------------------------------------
    # Phase 3: Line Balancing
    # -----------------------------------------------------------------
    def _phase_line_balancing(self) -> None:
        heading = safe_text(
            "3. Line Balancing", font_size=HEADING_SIZE, color=FLOW_BLUE
        )
        heading.to_edge(UP, buff=0.5)
        self.play(Write(heading))
        self.wait(0.3)

        # Build original process
        sa, sb, sc, ab, bc = self._build_process()
        self._show_process(sa, sb, sc, ab, bc)
        self.wait(0.5)

        # Animate time labels changing simultaneously:
        # A: 5 -> 5 (stays), B: 8 -> 6, C: 4 -> 6
        old_b_time = sb[2]
        old_c_time = sc[2]

        new_b_time = Text("6 min", font_size=18, color=ACCENT)
        new_c_time = Text("6 min", font_size=18, color=ACCENT)
        new_b_time.move_to(old_b_time.get_center())
        new_c_time.move_to(old_c_time.get_center())

        # Also recolor all stations to balanced green
        sa_rect = sa[0]
        sb_rect = sb[0]
        sc_rect = sc[0]

        balanced_color = OPTIMIZE_GREEN

        self.play(
            Transform(old_b_time, new_b_time),
            Transform(old_c_time, new_c_time),
            sa_rect.animate.set_fill(balanced_color, opacity=0.8),
            sb_rect.animate.set_fill(balanced_color, opacity=0.8)
            .set_stroke(WHITE, width=2),
            sc_rect.animate.set_fill(balanced_color, opacity=0.8),
            run_time=1.0,
        )
        self.wait(0.3)

        # "Balanced" label
        balanced_label = safe_text(
            "All stations balanced", font_size=LABEL_SIZE, color=OPTIMIZE_GREEN
        )
        balanced_label.next_to(VGroup(sa, sb, sc), DOWN, buff=0.6)
        self.play(FadeIn(balanced_label, shift=UP * 0.2), run_time=0.5)
        self.wait(0.3)

        # Bottom note
        note = bottom_note("Redistribute work evenly")
        self.play(FadeIn(note, shift=UP * 0.2), run_time=0.5)
        self.wait(2.0)

        # Final cleanup
        fade_all(self, heading, sa, sb, sc, ab, bc, balanced_label, note)
        self.wait(0.3)
