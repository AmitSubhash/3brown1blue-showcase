# Video Plan: Performance Grade Bitumen for Airport Runways

## Title
**"Why Runway Asphalt is Different: The Engineering of Performance Grade Bitumen"**

### Core Question
*How do you engineer a material that survives 200-tonne aircraft, jet fuel spills, and temperature swings from -22°C to +76°C -- all on a single strip of pavement?*

---

## Color Semantics (consistent across all scenes)

| Color | Hex | Meaning |
|---|---|---|
| `ASPHALT_BLACK` | `#2C2C2C` | Base bitumen / pavement layers |
| `POLYMER_BLUE` | `#4A90D9` | Polymer modification / PMB |
| `HEAT_RED` | `#E74C3C` | High temperature, rutting failure |
| `COLD_CYAN` | `#00BCD4` | Low temperature, cracking failure |
| `STRESS_YELLOW` | `#F1C40F` | Load/force/stress indicators |
| `SUCCESS_GREEN` | `#2ECC71` | Passing spec, good performance |
| `FUEL_ORANGE` | `#E67E22` | Jet fuel resistance |
| `CONTEXT_GRAY` | `#7F8C8D` at 40% opacity | Dimmed context elements |

### Persistent Visual Motifs
1. **Temperature number line** -- horizontal axis from -30°C to +80°C, reappears in Scenes 2, 4, 5, 7 as the unifying conceptual spine
2. **Runway cross-section** -- layered rectangle (GSB → WMM → DBM → BC) shown as a persistent sidebar when discussing materials
3. **Molecular chain diagram** -- short wiggly lines (bitumen) vs long interconnected chains (polymer-modified), referenced in Scenes 3, 5, 6

---

## Scene-by-Scene Plan

### Scene 1: `RunwayForces` (~45s)
**Template:** FULL_CENTER → BUILD_UP

**Key Animation Idea:**
A top-down runway view (simple gray rectangle with dashed center line). An aircraft silhouette (simplified geometric shape) lands. On touchdown, concentric stress rings radiate from the landing gear (like sonar pulses) in `STRESS_YELLOW`. A force arrow grows downward: label shows "200+ tonnes." Then animate the tire contact patch -- a small rectangle with `MathTex(r"P = \frac{F}{A}")` showing the concentrated pressure (~1.5 MPa). Compare to a car (~0.2 MPa) with a much smaller arrow beside it. The ratio "7.5×" pulses.

**Narration Focus:**
"When a Boeing 777 touches down, each tire presses the pavement with seven times the pressure of your car. But pressure is only half the problem..."

**Cleanup:** FadeOut aircraft and pressure comparison. Keep the runway rectangle as context for Scene 2.

---

### Scene 2: `TemperatureProblem` (~50s)
**Template:** FULL_CENTER with persistent temperature number line

**Key Animation Idea:**
Introduce the **temperature number line** (the video's throughline visual). Animate a `ValueTracker` sweeping from -22°C to +76°C. At the cold end, show a pavement cross-section rectangle that develops a crack (a jagged `Line` splits it apart) colored `COLD_CYAN`. At the hot end, the same rectangle deforms -- the top surface sags into a rut (morph the rectangle's top edge into a concave curve) colored `HEAT_RED`.

A bracket labeled "Usable Range" appears spanning maybe 0°C to 40°C for conventional bitumen (small span, `CONTEXT_GRAY`). Then a second bracket for PG bitumen spans the full -22 to +76 range in `SUCCESS_GREEN`.

Display: `MathTex(r"\text{PG } {{76}} \text{-} {{22}}")` where `76` is colored `HEAT_RED` and `-22` is colored `COLD_CYAN`. Animate arrows from the numbers to the corresponding temperature line positions.

**Narration Focus:**
"The PG grading system encodes the answer right in the name. PG 76-22 means: this binder won't rut above 76°C and won't crack below -22°C."

**Cleanup:** Dim the temperature line to 15% opacity; it stays as a persistent reference.

---

### Scene 3: `WhatIsBitumen` (~40s)
**Template:** DUAL_PANEL

**Key Animation Idea:**
LEFT PANEL: Zoom into a pavement layer. Show aggregate particles (irregular polygons, gray) with dark fill between them (bitumen). Label: "Bitumen = the glue."

RIGHT PANEL: Molecular view. Draw short, squiggly `CubicBezier` chains (asphaltenes, maltenes) in `ASPHALT_BLACK`. Animate them as a loose tangle. Apply heat (`HEAT_RED` background wash) -- the chains start sliding past each other (updater shifts them slowly apart). Apply cold (`COLD_CYAN` wash) -- the chains lock rigid, then a crack propagates through.

This sets up WHY polymer modification is needed: the base molecules can't handle both extremes.

**Narration Focus:**
"Bitumen is a tangle of hydrocarbon molecules. Heat makes them slide -- your runway ruts. Cold makes them brittle -- your runway cracks. The molecule itself is the problem."

---

### Scene 4: `PolymerModification` (~60s)
**Template:** BUILD_UP with molecular chain motif

**Key Animation Idea:**
Start with the loose bitumen chains from Scene 3 (right panel, now centered). Introduce long polymer chains (`POLYMER_BLUE`, thicker `CubicBezier` curves) that weave through the bitumen network -- animate them threading in with `MoveAlongPath`. The network visually tightens. Label: "SBS Polymer Network."

Now replay the temperature test: apply heat -- the polymer chains act as elastic tethers (they stretch but don't let the bitumen chains slide away, shown as spring-like oscillation). Apply cold -- the polymer chains remain flexible (gentle wave motion), preventing the rigid lock-up.

Below, show two bars side by side animating with `GrowFromEdge`:
- "Rutting Resistance" bar grows tall in `SUCCESS_GREEN`
- "Crack Resistance" bar grows tall in `SUCCESS_GREEN`

Equation: `MathTex(r"G^*/\sin\delta \geq 1.0 \text{ kPa}")` (rutting parameter) fades in, then `MathTex(r"S \leq 300 \text{ MPa}, \; m \geq 0.300")` (cracking parameter).

**Narration Focus:**
"Polymer-modified bitumen is not just 'better bitumen.' It's an engineered network. The polymer chains create elastic bridges that resist both flow and fracture."

---

### Scene 5: `PGGradingSystem` (~55s)
**Template:** TOP_PERSISTENT_BOTTOM_CONTENT (temperature line persistent at top)

**Key Animation Idea:**
Bring the temperature number line back to full opacity at the top. Below it, build a table/grid of PG grades used in the slide deck:

| Grade | High Temp | Low Temp | Use Case |
|---|---|---|---|
| PG 76-22 | 76°C | -22°C | Airport Runway (tropical) |
| PG 76E-10 | 76°C | -10°C | Expressway (India) |

Each row animates in with `LaggedStart`. As each row appears, a colored span on the temperature line highlights that grade's range. The airport grade (`PG 76-22`) gets the widest span and a `SurroundingRectangle` in `STRESS_YELLOW`.

Then animate a map of Asia (simplified polygon outlines) with dots at airports from the slide deck (Vietnam, Malaysia, Indonesia, Cambodia, India). Each dot pulses as its project name appears briefly. Counter in corner: "23 airports, 6 countries, 45,000 tonnes PMB."

**Narration Focus:**
"Across Asia, from Hanoi to Hyderabad, PG 76-22 has become the standard. But the grade alone doesn't tell you if the mix will survive jet fuel."

---

### Scene 6: `FuelResistance` (~40s)
**Template:** FULL_CENTER

**Key Animation Idea:**
Show a runway cross-section (the persistent motif, now at full size). A stylized fuel droplet (`FUEL_ORANGE` teardrop shape) falls onto the surface. For standard bitumen: the surface dissolves (the top layer rectangle's fill_opacity animates to 0, edges become ragged). For fuel-resistant PMB: the droplet sits on the surface, beads up (surface tension animation -- droplet morphs into a more spherical shape), and the pavement stays intact.

Split-screen comparison using `DUAL_PANEL` transition: LEFT = standard (damaged), RIGHT = fuel-resistant (intact). Label: "PG 76 Fuel Resistant."

**Narration Focus:**
"Jet fuel is a solvent. It dissolves ordinary bitumen on contact. Fuel-resistant PMB uses cross-linked polymers that the fuel simply cannot penetrate."

---

### Scene 7: `ThicknessReduction` (~50s)
**Template:** DUAL_PANEL (this is directly from slide 35)

**Key Animation Idea:**
LEFT: Pavement cross-section using VG40 bitumen. Four stacked rectangles (GSB 230mm, WMM 250mm, DBM 150mm, BC 40mm) with heights proportional to thickness. Total height labeled.

RIGHT: Same structure but with HIPB. DBM layer is visibly thinner (120mm vs 150mm). Animate the compression: the DBM layer shrinks with `mob.animate.stretch(0.8, 1)` while a brace on the side shows "30mm saved."

Below both: `MathTex(r"E_{\text{HIPB}} = 4000 \text{ MPa} > E_{\text{VG40}} = 3000 \text{ MPa}")` -- the higher stiffness modulus is WHY less thickness is needed.

Animate a cost savings counter: fewer materials → less construction time → runway available sooner. Use `DecimalNumber` counting up savings.

**Narration Focus:**
"Higher stiffness means you can build thinner. HIPB's 4000 MPa modulus saves 30mm of DBM -- that's thousands of tonnes of material on a full runway."

---

### Scene 8: `TestingPipeline` (~45s)
**Template:** BUILD_UP

**Key Animation Idea:**
Show the quality assurance pipeline as a horizontal flowchart that builds left to right:

1. **Binder Selection** (beaker icon) → 
2. **Lab Testing** (DSR, BBR equipment silhouettes at COLAS Paris / HINCOL R&D) →
3. **Mix Design** (Marshall/Superpave specimen cylinder) →
4. **Field Trials** (runway segment) →
5. **Full Construction** (complete runway)

Each node appears with `GrowFromCenter`, connected by arrows that `GrowArrow`. At the "Lab Testing" node, briefly show the rheology test: a `ValueTracker`-driven animation of a parallel plate (DSR) oscillating, with `G*/sin(δ)` updating in real time.

Reference the Hyderabad and Bangalore case studies: "First customized PMB on Indian airport runways, 2006-07."

**Narration Focus:**
"Every runway starts in a lab in Paris or Haldia. The binder is characterized, the mix is optimized, and only then does it touch the tarmac."

---

### Scene 9: `Synthesis` (~35s)
**Template:** FULL_CENTER → final density ramp

**Key Animation Idea:**
Bring back ALL the key visuals simultaneously as a density ramp climax:

1. Temperature number line (top, full opacity)
2. PG 76-22 label with color-coded numbers (center-left)
3. Polymer network diagram (center-right, small)
4. Runway cross-section (bottom-left)
5. Asia airport map dots (bottom-right, pulsing)

All elements connected by thin `DashedLine` connectors showing the logical flow: Temperature Range → PG Grade → Polymer Chemistry → Pavement Design → Deployed Worldwide.

Final equation (the conceptual throughline): 
`MathTex(r"\text{PG } T_{\max}\text{-}|T_{\min}| \implies \text{Safe Runway}")`

Fade everything to black except the equation, which pulses once in `SUCCESS_GREEN`.

**Narration Focus:**
"Two numbers. That's all PG grading is. But behind those two numbers lies polymer chemistry, rheological testing, and thirty years of airport engineering across six countries."

---

## Mathematical/Conceptual Throughline

The **temperature number line** is the spine. Every scene either:
- Introduces a problem on that line (cracking at cold end, rutting at hot end)
- Shows a solution that widens the usable range on that line (polymer modification)
- Maps real projects onto that line (PG grades)

The viewer should internalize: **the wider the PG range, the more extreme conditions the binder survives**, and polymer modification is the mechanism that achieves that width.

---

## Implementation Notes for Manim Developer

1. **style.py** must define all colors, the `temperature_number_line()` factory function, the `runway_cross_section()` factory, and the `polymer_chain()` bezier generator
2. **All text** via `safe_text()` wrapper; all equations via `MathTex` (no `$` delimiters)
3. **Persistent elements** (temperature line, cross-section) should be created once in `style.py` and imported -- never recreated
4. Use `Write()` for all text/equations, `Create()` for geometric shapes, `GrowArrow()` for arrows
5. Target render: `manim -qh` (1080p60) for final, `manim -pql` for development
6. Estimated total duration: ~6 minutes (360s across 9 scenes)
7. Each scene is an independent `Scene` subclass for parallel development