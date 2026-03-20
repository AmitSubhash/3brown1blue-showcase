# Performance Grade Bitumen for Airport Runways

3Blue1Brown-style animated explainer generated from a 60-slide L&T/HINCOL presentation.

## Video

**Duration:** 3:40 (9 scenes, 179 animations, 1080p60)

**Core question:** How do you engineer a material that survives 200-tonne aircraft, jet fuel spills, and temperature swings from -22C to +76C on a single strip of pavement?

## Scenes

1. **RunwayForces** - Contact pressure comparison: aircraft vs highway trucks
2. **TemperatureProblem** - Thermal cycling and why bitumen cracks
3. **WhatIsBitumen** - Molecular structure of bitumen
4. **PolymerModification** - How SBR/EVA polymers reinforce the binder
5. **PGGradingSystem** - Performance Grade notation (PG 76-22)
6. **FuelResistance** - Jet fuel attack and polymer defense
7. **ThicknessReduction** - PMB allows thinner pavement layers
8. **TestingPipeline** - Lab characterization (DSR, BBR, RTFOT)
9. **Synthesis** - Full pavement system integration

## Generation

```bash
3brown1blue from-slides "LnT 190326.pptx" --provider claude-code
```

- Extraction: text mode (auto-detected, 126 chars/slide avg)
- Planning: Opus
- Code generation: Opus
- Rendering: manim -qh (1080p60)
