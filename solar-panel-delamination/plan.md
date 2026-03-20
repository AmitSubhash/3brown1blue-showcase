# Solar Panel Mechanical Delamination -- Manim Video Plan

---

## STEP 1: RESEARCH -- Deep Concept Analysis

### Core Question the Video Answers
**"How do you take apart something engineered never to come apart?"**

Solar panels are designed for 25+ years of outdoor survival -- every layer is bonded with EVA (ethylene-vinyl acetate) adhesive cured at 150 degrees C into a monolithic slab. Mechanical delamination reverses this by exploiting the thermomechanical weakness of EVA: its glass transition at ~65 degrees C and softening above 200 degrees C.

### Solar Panel Layer Structure (top to bottom)
| Layer | Material | Thickness | Mass % | Value |
|---|---|---|---|---|
| Superstrate | Tempered glass | 3.2 mm | ~70% | $0.50/kg |
| Front encapsulant | EVA | 0.45 mm | ~7% | negligible |
| Cell layer | Crystalline Si + Ag busbars + Cu ribbons | 0.18 mm | ~4% | HIGH |
| Rear encapsulant | EVA | 0.45 mm | ~7% | negligible |
| Backsheet | Tedlar-PET-Tedlar (TPT) | 0.30 mm | ~4% | negligible |
| Frame | Aluminum | 35 mm profile | ~8% | $1.80/kg |

### Key Physics

**Peel adhesion energy** (the central equation):
$$G = \frac{F}{w}(1 - \cos\theta)$$
where G = adhesion energy (J/m^2), F = peel force (N), w = specimen width (m), theta = peel angle (rad).

At theta = 90 degrees: G = F/w (simplest case).
At theta = 180 degrees: G = 2F/w (maximum mechanical advantage).

**EVA thermomechanics:**
- Glass transition T_g ~ 65 degrees C (becomes rubbery)
- Onset of decomposition ~ 300 degrees C (acetic acid release)
- Hot-knife operating window: 200-350 degrees C
- Peel force drops ~10x between 25 degrees C and 200 degrees C

**Fracture mechanics at interface:**
Crack propagation along EVA-glass interface follows:
$$G_{applied} \geq G_c(\theta, T, \dot{a})$$
where G_c is the critical energy release rate, dependent on peel angle, temperature, and crack speed.

### Concrete Data Points
- Global PV waste by 2050: ~78 million tonnes (IRENA)
- Current recycling rate: < 10% globally
- Typical panel: 60 cells, 1.65 m x 0.99 m, 18.5 kg
- Silver per panel: ~15-20 g (worth ~$15 at $800/kg spot)
- Hot-knife speed: 5-15 mm/s
- Roller throughput: ~20 panels/hour
- Glass recovery: 85-98% (method-dependent)
- Silicon recovery: 70-95% (method-dependent)
- Peel force at 25 degrees C: ~8 N/mm; at 200 degrees C: ~0.8 N/mm

---

## STEP 2: CURRICULUM -- 8-Scene Sequence (~5 min)

| # | Phase | Scene | Duration | Core Idea |
|---|---|---|---|---|
| 1 | Hook | S01_Hook | 12s | Show the waste crisis, then the hidden treasure inside a panel |
| 2 | Problem | S02_Problem | 30s | EVA makes panels permanent -- show the bonding that resists separation |
| 3 | Background | S03_Anatomy | 40s | Build the cross-section layer by layer with thicknesses and values |
| 4 | Background | S04_Adhesion | 45s | Peel test physics: the adhesion energy equation and temperature dependence |
| 5 | Method | S05_HotKnife | 50s | Animated hot-knife delamination -- the dominant mechanical method |
| 6 | Method | S06_RollerCrush | 45s | Roller crushing + electrostatic separation as alternative pathway |
| 7 | Results | S07_Recovery | 45s | Bar charts of recovery rates and cost-benefit analysis |
| 8 | Takeaway | S08_Circular | 15s | Closing: designed for service AND end-of-life |

**Surprising connection:** The same property that makes solar panels survive hailstorms for 25 years (EVA adhesion) is the enemy of recycling -- and the same variable (temperature) that cures the bond can break it.

---

## STEP 3: SCENE PLANS

### Scene 1: S01_Hook (~12s)
**Template:** FULL_CENTER
**Content:**
- CENTER: A stylized solar panel (blue rectangle with grid lines) with a large counter "78 MILLION TONNES BY 2050" fading in above it
- Then: panel "explodes" into its layers (glass, EVA, cells, EVA, backsheet separate vertically), revealing silver and silicon values as small colored labels
- BOTTOM: "What if we could recover what's inside?"
**Visual anchors:** The exploded cross-section becomes the recurring motif
**Cleanup:** FadeOut all; the exploded view returns in Scene 3
**Equations:** None
**Data:** 78 million tonnes (IRENA 2016), ~$15 silver per panel, 18.5 kg total mass

---

### Scene 2: S02_Problem (~30s)
**Template:** DUAL_PANEL
**Content:**
- LEFT: Cross-section showing EVA as glowing orange "glue" between layers, with wavy adhesion force arrows pulling inward (use small Arrow mobjects). Label: "EVA cured at 150 degrees C"
- RIGHT: Attempted separation animation -- a hand/force arrow pulls on the backsheet, the panel resists, snaps back. Text: "Peel force: 8 N/mm at room temp"
- Question frame: "How do you undo a bond designed to last 25 years?" (yellow, 2.5s hold)
- BOTTOM: "Ethylene-Vinyl Acetate (EVA) -- the adhesive that won't let go"
**Visual anchors:** EVA layers shown in ORANGE throughout entire video
**Cleanup:** FadeOut both panels and question
**Equations:** None yet (introduced in Scene 4)
**Data:** 150 degrees C cure temp, 8 N/mm peel force, 25-year design life

---

### Scene 3: S03_Anatomy (~40s)
**Template:** BUILD_UP
**Content:**
- Build the panel cross-section bottom-to-top, one layer at a time:
  1. Backsheet (gray, 0.30 mm, labeled "TPT Backsheet")
  2. Rear EVA (orange, 0.45 mm, labeled "EVA Encapsulant")
  3. Cell layer (blue with silver lines, 0.18 mm, labeled "Si Cells + Ag Busbars")
  4. Front EVA (orange, 0.45 mm)
  5. Glass (light blue/transparent, 3.2 mm, labeled "Tempered Glass")
- Each layer FadeIn with shift=UP, thickness label on right with Brace
- After all layers built: value annotations appear on right side:
  - Glass: "70% mass, $0.50/kg"
  - Cells: "4% mass, ~$15 Ag per panel"
  - Al frame (shown at edge): "8% mass, $1.80/kg"
- BOTTOM: "Total: 18.5 kg per standard 60-cell panel"
**Visual anchors:** The stacked cross-section (will be reused as persistent context in Scenes 5-6)
**Cleanup:** Scale down to 40% and move to UL corner for Scene 4
**Equations:** None
**Data:** All thicknesses, mass percentages, dollar values from research table

---

### Scene 4: S04_Adhesion (~45s)
**Template:** TOP_PERSISTENT_BOTTOM_CONTENT
**Content:**
- TOP: Miniaturized cross-section from Scene 3 at 40% scale, y=[2.2, 3.2], EVA layers highlighted
- SUBTITLE: "Peel Test: Measuring Adhesion" at y=1.5
- MAIN: Animated peel test diagram:
  - Specimen (horizontal rectangle) adhered to substrate
  - Force arrow pulling at angle theta from horizontal
  - Angle arc labeled theta
  - Width w labeled with brace
- After geometry established, dim and reveal the equation:
  - Full equation: G = (F/w)(1 - cos(theta))
  - Reveal G (green): "Adhesion energy (J/m^2) -- energy to separate 1 m^2"
  - Reveal F/w (red): "Peel force per unit width"
  - Reveal (1 - cos theta) (blue): "Geometric factor -- peel angle matters!"
- Then: show temperature sweep -- a ValueTracker sweeps T from 25 to 300 degrees C, and a linked bar/curve shows peel force dropping from 8 to 0.5 N/mm
- BOTTOM: "EVA softens above T_g ~ 65 degrees C -- peel force drops 10x"
**Visual anchors:** Miniaturized cross-section in UL
**Cleanup:** FadeOut peel diagram and equation; keep mini cross-section
**Equations:**
- `G = \frac{F}{w}(1 - \cos\theta)`
- `G_{\text{applied}} \geq G_c(\theta, T, \dot{a})`
**Data:** G_c ~ 200-800 J/m^2 for EVA-glass, T_g = 65 degrees C, peel force 8 -> 0.8 N/mm

---

### Scene 5: S05_HotKnife (~50s)
**Template:** TOP_PERSISTENT_BOTTOM_CONTENT
**Content:**
- TOP: Miniaturized cross-section (persistent context), with EVA layers glowing
- SUBTITLE: "Method 1: Hot-Knife Delamination"
- MAIN: Side-view animation of the process:
  1. Full panel cross-section (larger, ~60% frame width)
  2. A triangular blade shape (red-orange gradient, labeled "300-350 degrees C") enters from the left
  3. Blade slides horizontally between glass and cell layer through the EVA
  4. As blade passes each point, the EVA changes color (orange -> dark gray "decomposed")
  5. Behind the blade, the glass layer separates upward with a small gap opening
  6. Speed label: "5-15 mm/s"
- After full pass: separated layers shown with gap, labels "Glass (intact)" and "Cell layer (recoverable)"
- Temperature profile inset (small axes, lower right): T vs. distance from blade tip, showing 350 degrees C at tip dropping to ~100 degrees C at 20 mm behind
- BOTTOM: "Hot knife exploits EVA's thermal weakness: 300 degrees C decomposes the adhesive"
**Visual anchors:** Mini cross-section in UL, blade shape (reappears conceptually)
**Cleanup:** FadeOut all main content; keep mini cross-section
**Equations:** None (physics was covered in Scene 4)
**Data:** 300-350 degrees C blade temp, 5-15 mm/s speed, EVA decomp at ~300 degrees C

---

### Scene 6: S06_RollerCrush (~45s)
**Template:** TOP_PERSISTENT_BOTTOM_CONTENT
**Content:**
- TOP: Miniaturized cross-section (persistent)
- SUBTITLE: "Method 2: Roller Crushing + Separation"
- MAIN: Two-stage animation:
  - Stage A (left half): Two counter-rotating rollers (gray circles with rotation arrows). Panel rectangle fed in from left. As it passes through, glass layer cracks into fragments (small irregular pieces scatter). Cell layer and backsheet pass through wrinkled but intact. Labels: "Controlled crushing"
  - Stage B (right half): Conveyor belt with mixed fragments. An electrostatic separator (two parallel plates, +/- labeled) above the belt. Glass fragments (light blue) fall straight. Si fragments (dark blue) deflect toward + plate. Cu fragments (copper color) deflect toward - plate. Labels on bins below: "Glass 95%", "Si 85%", "Cu 90%"
- Arrow connecting Stage A output to Stage B input
- BOTTOM: "Throughput: ~20 panels/hour -- faster but lower cell integrity"
**Visual anchors:** Mini cross-section, roller shapes
**Cleanup:** FadeOut all
**Equations:** None
**Data:** 20 panels/hour throughput, recovery rates per material

---

### Scene 7: S07_Recovery (~45s)
**Template:** CHART_FOCUS
**Content:**
- TITLE: "Material Recovery Rates by Method"
- MAIN: Grouped bar chart (Axes spanning frame):
  - X-axis: Material categories (Glass, Silicon, Silver, Copper)
  - Y-axis: Recovery rate 0-100%
  - Bar groups: Hot Knife (red-orange), Roller Crush (gray-blue), Chemical (green, for reference)
  - Concrete values labeled on each bar:
    - Glass: 95%, 98%, 90%
    - Silicon: 85%, 70%, 95%
    - Silver: 80%, 60%, 92%
    - Copper: 88%, 90%, 85%
  - Bars animate in with LaggedStart per group
- After bars shown, highlight the trade-off:
  - SurroundingRectangle around Hot Knife silicon bar (85%) vs Roller silicon bar (70%)
  - Annotation arrow: "Hot knife preserves wafer integrity"
  - SurroundingRectangle around Roller glass bar (98%) vs Hot Knife glass bar (95%)
  - Annotation arrow: "Roller maximizes glass yield"
- BOTTOM: "No single method wins everywhere -- hybrid approaches emerging"
**Visual anchors:** None (standalone data scene)
**Cleanup:** FadeOut all
**Equations:** None
**Data:** All recovery percentages from literature survey (IEA-PVPS, Deng et al. 2019, Fiandra et al. 2019)

---

### Scene 8: S08_Circular (~15s)
**Template:** FULL_CENTER
**Content:**
- CENTER: The exploded panel from Scene 1 reassembles in reverse (layers come together)
- Text morphs: "25 years of service" -> "Then a second life for every layer"
- Final frame: circular arrow around the panel icon with text "Design for Deconstruction"
- BOTTOM: (none -- clean ending)
**Visual anchors:** Callback to Scene 1's exploded view
**Cleanup:** Hold final frame 3s
**Equations:** None
**Data:** 25-year service life, 78M tonnes recoverable

---

## STEP 4: STYLE CONTRACT

```python
"""style.py -- Shared visual constants for solar panel delamination video."""

from manim import *
import numpy as np

# -- Semantic Color Palette --
# Each color carries ONE consistent meaning throughout the video.
GLASS_COLOR = "#7EC8E3"       # light blue -- tempered glass
EVA_COLOR = "#FF8C42"         # orange -- EVA encapsulant (the antagonist)
CELL_COLOR = "#2E5090"        # deep blue -- silicon cells
SILVER_COLOR = "#C0C0C0"      # silver -- Ag busbars
COPPER_COLOR = "#B87333"      # copper -- Cu ribbons
BACKSHEET_COLOR = "#888888"   # gray -- TPT backsheet
FRAME_COLOR = "#A8A8A8"       # aluminum frame

HEAT_LOW = "#3B82F6"          # blue -- cool temperature
HEAT_MID = "#F59E0B"         # amber -- warm
HEAT_HIGH = "#EF4444"         # red -- hot (blade, decomposition)

HOTKNIFE_COLOR = "#EF4444"    # red-orange -- hot knife method
ROLLER_COLOR = "#6B7280"      # gray-blue -- roller method
CHEMICAL_COLOR = "#10B981"    # green -- chemical method (reference)

HIGHLIGHT = "#FACC15"         # yellow -- current focus / question frames
DIMMED = "#4B5563"            # dark gray -- dimmed context
POSITIVE = "#22C55E"          # green -- good values, recovery
DANGER = "#EF4444"            # red -- waste, problem

BG_COLOR = "#0F172A"          # dark navy -- background

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
SAFE_HEIGHT = 6.0
MINI_SCALE = 0.4          # scale factor for persistent mini cross-section

# -- Timing --
HOLD_SHORT = 1.0
HOLD_MEDIUM = 2.0
HOLD_LONG = 3.0

# -- Layer Thicknesses (relative heights for cross-section) --
# Scaled so total cross-section is ~4.5 Manim units tall
LAYER_SCALE = 0.8  # multiplier for visual thickness
LAYERS = [
    ("Backsheet (TPT)", BACKSHEET_COLOR, 0.30, 0.4),   # name, color, mm, visual_height
    ("EVA", EVA_COLOR, 0.45, 0.5),
    ("Si Cells + Ag", CELL_COLOR, 0.18, 0.6),           # slightly taller for visibility
    ("EVA", EVA_COLOR, 0.45, 0.5),
    ("Tempered Glass", GLASS_COLOR, 3.20, 1.5),
]


# -- Helper Functions --

def section_title(text: str, color=WHITE) -> Text:
    """Create a styled section title positioned at top."""
    return Text(text, font_size=TITLE_SIZE, color=color).move_to(
        UP * TITLE_Y
    )


def safe_text(
    text: str,
    font_size: int = BODY_SIZE,
    color=WHITE,
    max_width: float = SAFE_WIDTH,
    **kwargs,
) -> Text:
    """Create text that auto-scales to fit within max_width."""
    t = Text(text, font_size=font_size, color=color, **kwargs)
    if t.width > max_width:
        t.scale_to_fit_width(max_width)
    return t


def bottom_note(text: str, color=HIGHLIGHT) -> Text:
    """Create a bottom-of-screen note, width-capped."""
    t = Text(text, font_size=LABEL_SIZE, color=color)
    if t.width > SAFE_WIDTH:
        t.scale_to_fit_width(SAFE_WIDTH)
    return t.to_edge(DOWN, buff=0.5)


def fade_all(scene: Scene, run_time: float = 0.8) -> None:
    """Fade out every mobject currently in the scene."""
    if scene.mobjects:
        scene.play(
            *[FadeOut(m) for m in scene.mobjects],
            run_time=run_time,
        )


def build_cross_section(width: float = 5.0) -> VGroup:
    """Build the standard panel cross-section as a VGroup of labeled layers.

    Returns a VGroup where each child is VGroup(Rectangle, Text_label).
    Layers ordered bottom-to-top matching LAYERS list.
    """
    layers = VGroup()
    for name, color, thickness_mm, visual_h in LAYERS:
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
        if label.width > rect.width - 0.2:
            label.scale_to_fit_width(rect.width - 0.2)
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
```

---

## STEP 5: VISUAL DESIGN PRINCIPLES APPLIED

### Principle Mapping

| Principle | Application in This Video |
|---|---|
| **Geometry before algebra** | Scene 4: show the peel test diagram (geometry) BEFORE revealing G = F/w(1-cos theta) |
| **Opacity layering** | Mini cross-section at 0.7 opacity in UL during method scenes; dimmed equation terms at 0.3 during reveal |
| **Persistent context** | The panel cross-section appears in S01, builds in S03, persists as mini in S04-S06, reassembles in S08 |
| **Question frames** | S02: "How do you undo a bond designed to last 25 years?" held 2.5s before any method is shown |
| **Annotations ON objects** | Thickness braces directly on layer rectangles; temperature labels on the blade; peel force arrow at the peel point |
| **Color as semantic data** | EVA is ALWAYS orange. Glass is ALWAYS light blue. Heat is ALWAYS red. No decorative color. |
| **Concrete values** | Every layer has mm thickness, every bar has a %, every temperature is in degrees C, silver is "$15/panel" not "valuable" |
| **Progressive complexity** | S01: 1 panel icon -> S03: 5 layers -> S04: layers + equation -> S05: layers + blade + temperature profile |
| **Linked dual representations** | S04: ValueTracker sweeps temperature; left panel shows thermometer, right panel shows peel force curve -- both update simultaneously |
| **Emotional anchoring** | "78 MILLION TONNES" in red in S01; "the adhesive that won't let go" in S02 |
| **Density ramp** | S01 has 2 elements; S05 has 8+ elements (mini section, blade, layers, gap, speed label, temp profile, annotations) |
| **Per-scene skeleton** | S03-S06: the cross-section is the skeleton. S07: the axes are the skeleton. |

### Color Consistency Contract

| Element | Color | Hex | Scenes Used |
|---|---|---|---|
| Glass | Light blue | `#7EC8E3` | ALL (S01-S08) |
| EVA | Orange | `#FF8C42` | ALL |
| Silicon cells | Deep blue | `#2E5090` | S01, S03-S07 |
| Hot knife / heat | Red | `#EF4444` | S04-S07 |
| Roller method | Gray-blue | `#6B7280` | S06-S07 |
| Highlights / questions | Yellow | `#FACC15` | S02, S04, S07 |
| Waste / danger | Red | `#EF4444` | S01, S02 |
| Recovery / positive | Green | `#22C55E` | S07, S08 |

### Animation Timing Budget

| Scene | Animations | Total run_time | Waits | Scene Duration |
|---|---|---|---|---|
| S01_Hook | 4 | ~5s | ~7s | 12s |
| S02_Problem | 6 | ~10s | ~20s | 30s |
| S03_Anatomy | 8 | ~14s | ~26s | 40s |
| S04_Adhesion | 10 | ~18s | ~27s | 45s |
| S05_HotKnife | 8 | ~20s | ~30s | 50s |
| S06_RollerCrush | 8 | ~18s | ~27s | 45s |
| S07_Recovery | 7 | ~16s | ~29s | 45s |
| S08_Circular | 3 | ~6s | ~9s | 15s |
| **Total** | | | | **~282s (~4:42)** |

---

## Agent Dispatch Summary

Each scene file imports from `style.py` and follows its assigned template. The persistent cross-section (`build_cross_section()` and `mini_cross_section()`) is the shared visual thread. Scene agents receive:

1. **Context block:** Paper topic, style.py path
2. **Rules block:** 10 mandatory layout/lifecycle rules (identical for all)
3. **Scene plan:** The specific plan from Step 3 above
4. **Scene description:** Creative direction from the curriculum

**Dependency graph:**
```
style.py (write first)
    |
    +-- S01_Hook (independent)
    +-- S02_Problem (independent)
    +-- S03_Anatomy (independent, defines cross-section visual)
    +-- S04_Adhesion (independent)
    +-- S05_HotKnife (independent)
    +-- S06_RollerCrush (independent)
    +-- S07_Recovery (independent)
    +-- S08_Circular (references S01 visual callback)
```

All scenes are independent of each other (they all import `build_cross_section` from style.py). They can be dispatched to parallel agents.