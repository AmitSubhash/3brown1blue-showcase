"""Scenes 1-3: Optical Window, Scattering/Absorption, Random Walk to Diffusion."""

from __future__ import annotations

import random
from pathlib import Path

import numpy as np
from manim import *

sys_module = __import__("sys")
sys_module.path.insert(0, str(Path(__file__).resolve().parent))
from style import *


# ---------------------------------------------------------------------------
# Helper: generate a 2-D random walk path
# ---------------------------------------------------------------------------

def _random_walk_path(
    start: np.ndarray,
    n_steps: int,
    mean_free_path: float,
    seed: int | None = None,
) -> list[np.ndarray]:
    """Return list of 3-D points for a 2-D random walk."""
    rng = np.random.default_rng(seed)
    pts = [start.copy()]
    angle = rng.uniform(0, TAU)
    for _ in range(n_steps):
        step_len = rng.exponential(mean_free_path)
        angle += rng.normal(0, 0.8)
        dx = step_len * np.cos(angle)
        dy = step_len * np.sin(angle)
        pts.append(pts[-1] + np.array([dx, dy, 0.0]))
    return pts


# ===================================================================
# Scene 1 -- "Why Light? The Optical Window"
# ===================================================================

class OpticalWindow(Scene):
    """Show the NIR optical window in the electromagnetic spectrum.

    Flow
    ----
    1. Draw EM spectrum number line (400-2000 nm).
    2. Color the visible band with a rainbow gradient.
    3. Plot water and total-hemoglobin absorption curves.
    4. Highlight the NIR sweet spot (650-950 nm).
    5. Zoom in: separate HbO2 / HbR spectra, mark isosbestic point.
    """

    def construct(self) -> None:
        # ---- section: title --------------------------------------------------
        self.next_section("Title")
        title = Text("Why Light? The Optical Window", font_size=TITLE_SIZE)
        self.play(Write(title))
        self.wait(HOLD)
        self.play(title.animate.scale(0.5).to_corner(UL))

        # ---- section: EM spectrum axis ----------------------------------------
        self.next_section("EM Spectrum")
        axes = Axes(
            x_range=[400, 2000, 200],
            y_range=[0, 1.05, 0.2],
            x_length=11,
            y_length=4.5,
            axis_config={"include_numbers": True, "font_size": 18},
            tips=False,
        ).shift(DOWN * 0.3)
        x_label = axes.get_x_axis_label(
            Tex(r"Wavelength (nm)", font_size=LABEL_SIZE), direction=DOWN,
        )
        y_label = axes.get_y_axis_label(
            Tex(r"Relative absorption", font_size=LABEL_SIZE), direction=LEFT,
        )
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.5)

        # ---- rainbow band for visible (400-700 nm) ---------------------------
        vis_colors = [
            PURPLE_A, BLUE_C, TEAL_C, GREEN_C, YELLOW_C, ORANGE, RED_C,
        ]
        n_stripes = len(vis_colors)
        vis_start, vis_end = 400, 700
        stripe_w = (vis_end - vis_start) / n_stripes
        rainbow_rects = VGroup()
        for i, col in enumerate(vis_colors):
            lx = vis_start + i * stripe_w
            rx = lx + stripe_w
            bl = axes.c2p(lx, 0)
            tr = axes.c2p(rx, 1.05)
            rect = Rectangle(
                width=abs(tr[0] - bl[0]),
                height=abs(tr[1] - bl[1]),
                fill_color=col,
                fill_opacity=0.20,
                stroke_width=0,
            ).move_to((np.array(bl) + np.array(tr)) / 2)
            rainbow_rects.add(rect)
        vis_label = Tex("Visible", font_size=LABEL_SIZE, color=C["label"])
        vis_label.move_to(axes.c2p(550, 0.95))
        self.play(
            LaggedStart(*[FadeIn(r) for r in rainbow_rects], lag_ratio=0.08),
            Write(vis_label),
            run_time=1.5,
        )
        self.wait(1)

        # ---- absorption curves -----------------------------------------------
        self.next_section("Absorption Curves")

        # Water: low in 650-950 window, rises sharply after ~950
        def water_abs(lam: float) -> float:
            x = (lam - 400) / 1600
            base = 0.02
            if lam < 950:
                return base + 0.03 * np.exp((lam - 950) / 200)
            return base + 0.9 * (1 - np.exp(-(lam - 950) / 250))

        # Total hemoglobin: high below 650, drops in NIR, moderate above
        def hb_total_abs(lam: float) -> float:
            return 0.85 * np.exp(-((lam - 420) ** 2) / (2 * 60**2)) + \
                   0.15 * np.exp(-((lam - 550) ** 2) / (2 * 40**2)) + \
                   0.08 + 0.25 * np.exp(-((lam - 400) ** 2) / (2 * 80**2)) + \
                   0.06 * np.exp(-((lam - 760) ** 2) / (2 * 30**2)) + \
                   0.05 * np.exp(-((lam - 900) ** 2) / (2 * 40**2))

        water_graph = axes.plot(
            water_abs, x_range=[400, 2000, 5], color=BLUE_C, stroke_width=3,
        )
        hb_graph = axes.plot(
            hb_total_abs, x_range=[400, 2000, 5], color=RED_C, stroke_width=3,
        )
        water_label = Tex(
            r"Water", font_size=LABEL_SIZE, color=BLUE_C,
        ).move_to(axes.c2p(1600, 0.75))
        hb_label = Tex(
            r"Hemoglobin", font_size=LABEL_SIZE, color=RED_C,
        ).move_to(axes.c2p(500, 0.85))

        self.play(Create(water_graph), Write(water_label), run_time=2)
        self.play(Create(hb_graph), Write(hb_label), run_time=2)
        self.wait(HOLD)

        # ---- NIR window highlight --------------------------------------------
        self.next_section("NIR Window")
        nir_bl = axes.c2p(650, 0)
        nir_tr = axes.c2p(950, 1.05)
        nir_rect = Rectangle(
            width=abs(nir_tr[0] - nir_bl[0]),
            height=abs(nir_tr[1] - nir_bl[1]),
            fill_color=GREEN,
            fill_opacity=0.18,
            stroke_color=GREEN,
            stroke_width=2,
        ).move_to((np.array(nir_bl) + np.array(nir_tr)) / 2)

        nir_label = Tex(
            r"NIR Window\\650--950\,nm",
            font_size=LABEL_SIZE,
            color=GREEN,
        ).move_to(axes.c2p(800, 0.55))

        annotation = Text(
            "The sweet spot: light penetrates tissue here.",
            font_size=LABEL_SIZE,
            color=C["highlight"],
        ).next_to(axes, DOWN, buff=0.4)

        self.play(FadeIn(nir_rect), Write(nir_label), run_time=1.5)
        self.play(Write(annotation), run_time=1.5)
        self.wait(HOLD)

        # ---- transition: clear and zoom into HbO2 / HbR ----------------------
        self.next_section("HbO2 vs HbR")
        old_stuff = VGroup(
            axes, x_label, y_label, rainbow_rects, vis_label,
            water_graph, hb_graph, water_label, hb_label,
            nir_rect, nir_label, annotation,
        )
        self.play(FadeOut(old_stuff), run_time=1)

        # New axes zoomed into 650-950
        ax2 = Axes(
            x_range=[650, 950, 50],
            y_range=[0, 1.05, 0.2],
            x_length=10,
            y_length=4.5,
            axis_config={"include_numbers": True, "font_size": 20},
            tips=False,
        ).shift(DOWN * 0.3)
        x2_label = ax2.get_x_axis_label(
            Tex(r"Wavelength (nm)", font_size=LABEL_SIZE), direction=DOWN,
        )
        y2_label = ax2.get_y_axis_label(
            Tex(r"$\varepsilon$ (molar absorptivity)", font_size=LABEL_SIZE),
            direction=LEFT,
        )
        self.play(Create(ax2), Write(x2_label), Write(y2_label), run_time=1.5)

        # HbR: peaks around 760
        def hbr_spec(lam: float) -> float:
            return 0.85 * np.exp(-((lam - 760) ** 2) / (2 * 45**2)) + 0.10

        # HbO2: peaks around 900-920
        def hbo2_spec(lam: float) -> float:
            return 0.70 * np.exp(-((lam - 900) ** 2) / (2 * 50**2)) + 0.12

        hbr_graph = ax2.plot(
            hbr_spec, x_range=[650, 950, 2], color=BLUE_C, stroke_width=3,
        )
        hbo2_graph = ax2.plot(
            hbo2_spec, x_range=[650, 950, 2], color=RED_C, stroke_width=3,
        )

        hbr_label = Tex(
            r"HbR (deoxy)", font_size=LABEL_SIZE, color=BLUE_C,
        ).next_to(ax2.c2p(720, hbr_spec(720)), UP, buff=0.15)
        hbo2_label = Tex(
            r"HbO$_2$ (oxy)", font_size=LABEL_SIZE, color=RED_C,
        ).next_to(ax2.c2p(920, hbo2_spec(920)), UP, buff=0.15)

        self.play(Create(hbr_graph), Write(hbr_label), run_time=1.5)
        self.play(Create(hbo2_graph), Write(hbo2_label), run_time=1.5)
        self.wait(1.0)

        # Isosbestic point ~ 805 nm
        iso_x = 805
        iso_y = hbr_spec(iso_x)
        iso_dot = Dot(ax2.c2p(iso_x, iso_y), radius=0.10, color=C["highlight"])
        iso_label = Tex(
            r"Isosbestic\\$\sim$805\,nm", font_size=LABEL_SIZE, color=C["highlight"],
        ).next_to(iso_dot, UR, buff=0.15)

        self.play(FadeIn(iso_dot, scale=2), Write(iso_label), run_time=1)
        self.wait(1)

        # Arrows marking chosen wavelengths on either side
        lam1_x, lam2_x = 690, 830
        arr1 = Arrow(
            ax2.c2p(lam1_x, -0.12), ax2.c2p(lam1_x, 0.05),
            color=BLUE_C, stroke_width=3, max_tip_length_to_length_ratio=0.3,
        )
        arr2 = Arrow(
            ax2.c2p(lam2_x, -0.12), ax2.c2p(lam2_x, 0.05),
            color=RED_C, stroke_width=3, max_tip_length_to_length_ratio=0.3,
        )
        arr1_lbl = Tex(
            r"690\,nm", font_size=LABEL_SIZE, color=BLUE_C,
        ).next_to(arr1, DOWN, buff=0.05)
        arr2_lbl = Tex(
            r"830\,nm", font_size=LABEL_SIZE, color=RED_C,
        ).next_to(arr2, DOWN, buff=0.05)

        self.play(
            GrowFromCenter(arr1), GrowFromCenter(arr2),
            Write(arr1_lbl), Write(arr2_lbl), run_time=1.5,
        )

        insight = Text(
            "Pick wavelengths on either side of 805 nm\n"
            "to distinguish oxy from deoxy hemoglobin.",
            font_size=LABEL_SIZE - 2,
            color=C["highlight"],
        ).next_to(ax2, DOWN, buff=0.5)
        self.play(Write(insight), run_time=1.5)
        self.wait(HOLD)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ===================================================================
# Scene 2 -- "Scattering vs Absorption"
# ===================================================================

class ScatteringAbsorption(Scene):
    """Demonstrate scattering and absorption of photons in tissue.

    Flow
    ----
    1. Single photon random walk with scatter flashes.
    2. Absorption: photon dims/shrinks along path.
    3. Parameter sweep mu_s (scattering coefficient).
    4. Parameter sweep mu_a (absorption coefficient).
    5. Key insight text.
    """

    def construct(self) -> None:
        # ---- title -----------------------------------------------------------
        self.next_section("Title")
        title = Text(
            "Scattering vs Absorption", font_size=TITLE_SIZE,
        )
        subtitle = Text(
            "What happens to photons in tissue",
            font_size=BODY_SIZE, color=C["label"],
        ).next_to(title, DOWN, buff=0.3)
        self.play(Write(title), FadeIn(subtitle, shift=UP * 0.3))
        self.wait(HOLD)
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- Phase 1: tissue slab + one photon random walk --------------------
        self.next_section("Single photon scatter")
        slab = Rectangle(
            width=9, height=5, fill_color=C["tissue"],
            fill_opacity=0.12, stroke_color=C["tissue"], stroke_width=2,
        )
        slab_label = Tex(
            r"Tissue", font_size=LABEL_SIZE, color=C["tissue"],
        ).next_to(slab, UP, buff=0.1)
        self.play(FadeIn(slab), Write(slab_label))

        # Generate a random walk
        start = np.array([-4.0, 0.0, 0.0])
        path_pts = _random_walk_path(start, 28, mean_free_path=0.35, seed=42)
        # Clip to slab bounds
        for i, pt in enumerate(path_pts):
            path_pts[i] = np.array([
                np.clip(pt[0], -4.3, 4.3),
                np.clip(pt[1], -2.3, 2.3),
                0.0,
            ])

        photon = Dot(start, radius=0.08, color=C["photon"])
        self.play(FadeIn(photon, scale=3))

        scatter_label = Tex(
            r"Scattering: photon bounces off cell structures",
            font_size=LABEL_SIZE, color=C["scatter"],
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(scatter_label))

        # Animate the walk segment by segment
        for i in range(1, min(len(path_pts), 26)):
            seg = Line(path_pts[i - 1], path_pts[i], color=C["photon"], stroke_width=1.5)
            flash = Circle(
                radius=0.12, color=C["scatter"], fill_opacity=0.5, stroke_width=0,
            ).move_to(path_pts[i])
            self.play(
                photon.animate.move_to(path_pts[i]),
                Create(seg),
                run_time=0.12,
            )
            self.add(flash)
            self.play(FadeOut(flash), run_time=0.08)

        self.wait(1)

        # ---- Phase 2: absorption -- photon dims along path --------------------
        self.next_section("Absorption")
        self.play(FadeOut(scatter_label))
        # Clear path segments
        to_remove = [m for m in self.mobjects if isinstance(m, Line)]
        if to_remove:
            self.play(*[FadeOut(m) for m in to_remove], run_time=0.5)

        abs_label = Tex(
            r"Absorption: photon loses energy at each step",
            font_size=LABEL_SIZE, color=C["absorb"],
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(abs_label))

        # Reset photon
        photon2 = Dot(start, radius=0.10, color=C["photon"])
        self.play(FadeOut(photon), FadeIn(photon2, scale=2))

        path_pts2 = _random_walk_path(start, 20, mean_free_path=0.4, seed=99)
        for i, pt in enumerate(path_pts2):
            path_pts2[i] = np.array([
                np.clip(pt[0], -4.3, 4.3),
                np.clip(pt[1], -2.3, 2.3),
                0.0,
            ])

        weight = 1.0
        for i in range(1, len(path_pts2)):
            weight *= 0.88  # each step loses ~12 %
            new_r = max(0.02, 0.10 * weight)
            seg = Line(
                path_pts2[i - 1], path_pts2[i],
                color=C["photon"], stroke_width=max(0.3, 2 * weight),
                stroke_opacity=weight,
            )
            self.play(
                photon2.animate.move_to(path_pts2[i]).scale(0.88),
                Create(seg),
                run_time=0.12,
            )
        self.wait(1)
        self.play(FadeOut(abs_label))

        # ---- Phase 3: parameter sweep mu_s ------------------------------------
        self.next_section("mu_s sweep")
        # Clear previous
        old_mobs = [m for m in self.mobjects if m not in (slab, slab_label)]
        if old_mobs:
            self.play(*[FadeOut(m) for m in old_mobs], run_time=0.5)

        mus_tracker = ValueTracker(2.0)  # controls jaggedness

        mus_label = always_redraw(
            lambda: Tex(
                r"$\mu_s' = "
                + f"{mus_tracker.get_value():.0f}"
                + r"\;\mathrm{cm}^{-1}$",
                font_size=BODY_SIZE,
                color=C["scatter"],
            ).to_corner(UR, buff=0.5)
        )

        sweep_title = Tex(
            r"Scattering coefficient $\mu_s'$: how jagged is the path?",
            font_size=LABEL_SIZE, color=C["scatter"],
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(sweep_title))
        self.add(mus_label)

        # Pre-compute paths at different mu_s values (for always_redraw)
        rng_seed = 77
        path_cache: dict[int, list[np.ndarray]] = {}
        for mus_int in range(1, 52):
            mfp = 3.0 / mus_int  # mean free path inversely proportional
            pts = _random_walk_path(
                np.array([-4.0, 0.0, 0.0]), 40, mfp, seed=rng_seed,
            )
            for j, pt in enumerate(pts):
                pts[j] = np.array([
                    np.clip(pt[0], -4.3, 4.3),
                    np.clip(pt[1], -2.3, 2.3),
                    0.0,
                ])
            path_cache[mus_int] = pts

        def _build_path_mob() -> VMobject:
            mus_val = int(np.clip(mus_tracker.get_value(), 1, 50))
            pts = path_cache.get(mus_val, path_cache[2])
            path_mob = VMobject(color=C["photon"], stroke_width=2)
            path_mob.set_points_as_corners(pts)
            return path_mob

        photon_path = always_redraw(_build_path_mob)
        self.add(photon_path)

        # Sweep low -> high
        self.play(
            mus_tracker.animate.set_value(5),
            run_time=2, rate_func=linear,
        )
        self.wait(0.5, frozen_frame=False)
        self.play(
            mus_tracker.animate.set_value(25),
            run_time=3, rate_func=linear,
        )
        self.wait(0.5, frozen_frame=False)
        self.play(
            mus_tracker.animate.set_value(50),
            run_time=2, rate_func=linear,
        )
        self.wait(1, frozen_frame=False)

        # Sweep back to moderate
        self.play(
            mus_tracker.animate.set_value(10),
            run_time=2, rate_func=smooth,
        )
        self.wait(1, frozen_frame=False)

        self.play(
            FadeOut(photon_path), FadeOut(mus_label), FadeOut(sweep_title),
            run_time=0.8,
        )
        self.remove(photon_path, mus_label)

        # ---- Phase 4: parameter sweep mu_a ------------------------------------
        self.next_section("mu_a sweep")
        mua_tracker = ValueTracker(0.05)

        mua_label = always_redraw(
            lambda: Tex(
                r"$\mu_a = "
                + f"{mua_tracker.get_value():.2f}"
                + r"\;\mathrm{cm}^{-1}$",
                font_size=BODY_SIZE,
                color=C["absorb"],
            ).to_corner(UR, buff=0.5)
        )

        sweep2_title = Tex(
            r"Absorption coefficient $\mu_a$: how many photons survive?",
            font_size=LABEL_SIZE, color=C["absorb"],
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(sweep2_title))
        self.add(mua_label)

        # Create a group of 12 photon dots
        n_photons = 12
        rng = np.random.default_rng(123)
        photon_dots = VGroup()
        for k in range(n_photons):
            pos = np.array([
                rng.uniform(-3.5, 3.5),
                rng.uniform(-1.8, 1.8),
                0.0,
            ])
            d = Dot(pos, radius=0.10, color=C["photon"])
            photon_dots.add(d)
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in photon_dots], lag_ratio=0.05))

        # Each dot fades as mu_a increases (threshold based on random draw)
        thresholds = sorted(rng.uniform(0.05, 0.5, n_photons))
        for dot, thresh in zip(photon_dots, thresholds):
            dot.threshold = thresh

        for dot in photon_dots:
            dot.add_updater(
                lambda m, t=mua_tracker: m.set_opacity(
                    np.clip(1.0 - (t.get_value() - m.threshold) / 0.15, 0.0, 1.0)
                )
            )

        self.play(
            mua_tracker.animate.set_value(0.15),
            run_time=2, rate_func=linear,
        )
        self.wait(0.5, frozen_frame=False)
        self.play(
            mua_tracker.animate.set_value(0.35),
            run_time=2, rate_func=linear,
        )
        self.wait(0.5, frozen_frame=False)
        self.play(
            mua_tracker.animate.set_value(0.50),
            run_time=2, rate_func=linear,
        )
        self.wait(1, frozen_frame=False)

        for dot in photon_dots:
            dot.clear_updaters()
        self.play(
            FadeOut(photon_dots), FadeOut(mua_label), FadeOut(sweep2_title),
            run_time=0.8,
        )
        self.remove(mua_label)

        # ---- Phase 5: key insight ---------------------------------------------
        self.next_section("Key Insight")
        insight_lines = VGroup(
            Tex(
                r"In tissue: $\mu_s' \gg \mu_a$ (scattering $\sim$50$\times$ absorption)",
                font_size=BODY_SIZE, color=C["highlight"],
            ),
            Tex(
                r"Light \textbf{diffuses} like heat through a conductor.",
                font_size=BODY_SIZE, color=WHITE,
            ),
        ).arrange(DOWN, buff=0.5)
        box = SurroundingRectangle(
            insight_lines, color=C["highlight"], buff=0.4, corner_radius=0.15,
        )
        self.play(FadeOut(slab), FadeOut(slab_label))
        self.play(Write(insight_lines[0]), run_time=1.5)
        self.play(Write(insight_lines[1]), run_time=1.5)
        self.play(Create(box))
        self.wait(HOLD)
        self.play(*[FadeOut(m) for m in self.mobjects])


# ===================================================================
# Scene 3 -- "From Random Walk to Diffusion"
# ===================================================================

class RandomWalkToDiffusion(Scene):
    """Bridge from particle picture to continuum diffusion equation.

    Flow
    ----
    1. Simulate 40 photon random walks from a source point.
    2. Show endpoints as dots; morph into smooth fluence gradient.
    3. Dim-and-reveal the CW diffusion equation.
    4. Green's function solution + decaying exponential.
    """

    def construct(self) -> None:
        # ---- title -----------------------------------------------------------
        self.next_section("Title")
        title = Text(
            "From Random Walk to Diffusion", font_size=TITLE_SIZE,
        )
        self.play(Write(title))
        self.wait(HOLD)
        self.play(title.animate.scale(0.5).to_corner(UL))

        # ---- Phase 1: many photon random walks --------------------------------
        self.next_section("Many photons")
        source_pos = np.array([-4.5, 0.0, 0.0])
        source_dot = Dot(source_pos, radius=0.14, color=C["source"])
        source_label = Tex(
            r"Source", font_size=LABEL_SIZE, color=C["source"],
        ).next_to(source_dot, DOWN, buff=0.15)
        self.play(FadeIn(source_dot, scale=2), Write(source_label))

        n_walks = 40
        all_paths: list[list[np.ndarray]] = []
        for i in range(n_walks):
            pts = _random_walk_path(source_pos, 30, mean_free_path=0.35, seed=i + 200)
            for j, pt in enumerate(pts):
                pts[j] = np.array([
                    np.clip(pt[0], -6.5, 6.5),
                    np.clip(pt[1], -3.5, 3.5),
                    0.0,
                ])
            all_paths.append(pts)

        # Build VMobject paths
        path_mobs = VGroup()
        for pts in all_paths:
            pm = VMobject(
                color=C["photon"], stroke_width=1.0, stroke_opacity=0.4,
            )
            pm.set_points_as_corners(pts)
            path_mobs.add(pm)

        self.play(
            LaggedStart(
                *[Create(pm, run_time=0.8) for pm in path_mobs],
                lag_ratio=0.04,
            ),
            run_time=4,
        )
        self.wait(1)

        # ---- Phase 2: endpoints -> fluence gradient ---------------------------
        self.next_section("Endpoints to fluence")
        # Collect endpoints
        endpoint_dots = VGroup()
        endpoints = []
        for pts in all_paths:
            ep = pts[-1]
            endpoints.append(ep)
            d = Dot(ep, radius=0.06, color=C["photon"])
            endpoint_dots.add(d)

        # Fade paths, show endpoints
        self.play(
            path_mobs.animate.set_stroke(opacity=0.08),
            LaggedStart(*[FadeIn(d, scale=1.5) for d in endpoint_dots], lag_ratio=0.02),
            run_time=2,
        )
        self.wait(1)

        # Build fluence gradient as a series of concentric rectangles
        # radiating from source, color encodes intensity
        n_grad = 18
        grad_rects = VGroup()
        max_r = 9.0
        for i in range(n_grad):
            frac = i / n_grad
            r = max_r * (frac + 1 / n_grad)
            # Intensity decays with distance from source
            intensity = np.exp(-1.8 * frac)
            col = interpolate_color(BLACK, C["sensitivity"], intensity)
            rect = Rectangle(
                width=r * 0.6,
                height=max(0.3, 5.5 * (1 - 0.5 * frac)),
                fill_color=col,
                fill_opacity=0.35 * intensity,
                stroke_width=0,
            ).move_to(source_pos + RIGHT * r * 0.3)
            grad_rects.add(rect)

        # Sort so widest (dimmest) render first
        grad_rects = VGroup(*reversed(list(grad_rects)))

        fluence_label = Tex(
            r"Fluence rate $\Phi(\mathbf{r})$",
            font_size=BODY_SIZE, color=C["sensitivity"],
        ).to_edge(UP, buff=0.6).shift(RIGHT * 1.5)

        self.play(
            FadeOut(path_mobs),
            FadeOut(endpoint_dots),
            LaggedStart(*[FadeIn(r) for r in grad_rects], lag_ratio=0.05),
            run_time=3,
        )
        self.play(Write(fluence_label))

        morph_note = Text(
            "Discrete particles become a continuous field",
            font_size=LABEL_SIZE, color=C["label"],
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(morph_note))
        self.wait(HOLD)

        # ---- Phase 3: diffusion equation (dim-and-reveal) ---------------------
        self.next_section("Diffusion equation")
        self.play(
            FadeOut(grad_rects), FadeOut(fluence_label), FadeOut(morph_note),
            FadeOut(source_dot), FadeOut(source_label),
        )

        eq = MathTex(
            r"{{ D }}",
            r"{{ \nabla^2 \Phi }}",
            r"{{ - }}",
            r"{{ \mu_a }}",
            r"{{ \Phi }}",
            r"{{ = }}",
            r"{{ -S(\mathbf{r}) }}",
            font_size=EQ_SIZE,
        )
        eq_intro = Text(
            "The CW diffusion equation", font_size=BODY_SIZE, color=C["label"],
        ).to_edge(UP, buff=0.5)
        self.play(Write(eq_intro))
        self.play(Write(eq), run_time=2)
        self.wait(HOLD)

        # Dim everything
        self.play(eq.animate.set_opacity(0.25), run_time=0.8)

        terms = [
            (
                [r"D", r"\nabla^2 \Phi"],
                BLUE_C,
                "How light spreads (the diffusion we just watched)",
            ),
            (
                [r"\mu_a", r"\Phi"],
                RED_C,
                "Light lost to absorption (the fading dots)",
            ),
            (
                [r"-S(\mathbf{r})"],
                C["source"],
                "The source (where photons start)",
            ),
        ]

        for tex_keys, color, description in terms:
            parts = VGroup(*[
                eq.get_part_by_tex(tk) for tk in tex_keys
                if eq.get_part_by_tex(tk) is not None
            ])
            box = SurroundingRectangle(parts, color=color, buff=0.1)
            desc = Text(
                description, font_size=LABEL_SIZE, color=color,
            ).next_to(eq, DOWN, buff=0.6)
            self.play(
                *[p.animate.set_opacity(1.0) for p in parts],
                Create(box), run_time=0.8,
            )
            self.play(Write(desc), run_time=1)
            self.wait(1.5)
            self.play(
                *[p.animate.set_color(color) for p in parts],
                FadeOut(box), FadeOut(desc), run_time=0.8,
            )

        # Un-dim
        self.play(eq.animate.set_opacity(1.0), run_time=0.8)
        self.wait(1.5)

        # ---- Phase 4: Green's function solution + exponential curve -----------
        self.next_section("Greens function")
        self.play(eq.animate.scale(0.7).to_edge(UP, buff=0.5), FadeOut(eq_intro))

        gf_eq = MathTex(
            r"G(\mathbf{r}) = "
            r"\frac{e^{-\mu_{\mathrm{eff}} \, r}}{4\pi D \, r}",
            font_size=EQ_SIZE,
        ).next_to(eq, DOWN, buff=0.5)
        gf_label = Text(
            "Green's function: what ONE source looks like after diffusion",
            font_size=LABEL_SIZE, color=C["label"],
        ).next_to(gf_eq, DOWN, buff=0.3)
        self.play(Write(gf_eq), run_time=2)
        self.play(Write(gf_label), run_time=1.5)
        self.wait(1)

        # Decaying exponential plot
        ax_gf = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1.1, 0.2],
            x_length=7,
            y_length=3,
            axis_config={"include_numbers": True, "font_size": 18},
            tips=False,
        ).shift(DOWN * 1.3)
        ax_gf_xl = ax_gf.get_x_axis_label(
            Tex(r"$r$ (cm)", font_size=LABEL_SIZE), direction=DOWN,
        )
        ax_gf_yl = ax_gf.get_y_axis_label(
            Tex(r"$G(r)$", font_size=LABEL_SIZE), direction=LEFT,
        )

        mu_eff = 1.5
        green_curve = ax_gf.plot(
            lambda r: np.exp(-mu_eff * max(r, 0.05)) / max(r, 0.05) * 0.05,
            x_range=[0.15, 5, 0.05],
            color=C["recon"],
            stroke_width=3,
        )

        self.play(Create(ax_gf), Write(ax_gf_xl), Write(ax_gf_yl), run_time=1)
        self.play(Create(green_curve), run_time=2)

        decay_note = Tex(
            r"Exponential decay $\times\; 1/r$: "
            r"light falls off rapidly with distance",
            font_size=LABEL_SIZE, color=C["recon"],
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(decay_note), run_time=1.5)
        self.wait(HOLD)

        # Final cleanup
        self.play(*[FadeOut(m) for m in self.mobjects])
