# Manim Showcase

Animated explainer videos built with [Manim](https://www.manim.community/), generated using the [`3brown1blue`](https://pypi.org/project/3brown1blue/) skill package.

**Updated:** 2026-03-22 | **3brown1blue version:** v0.2.3

## Projects

| Project | Topic | Duration | Video |
|---------|-------|----------|-------|
| [Transformer](transformer/) | Attention Is All You Need (Vaswani et al., 2017) -- full 10-scene deep dive | ~8 min | [mp4](transformer/media/Transformer_Explainer.mp4) |
| [Attention Mechanism](attention-mechanism/) | Attention Is All You Need (Transformers) | ~2 min | [mp4](attention-mechanism/media/Attention_Is_All_You_Need.mp4) |
| [DOT Explainer](dot-explainer/) | Diffuse Optical Tomography | ~5 min | [mp4](dot-explainer/media/DOT_Complete_Explainer.mp4) |
| [FORCE Explainer](force-explainer/) | FORCE fNIRS Processing Pipeline | ~5 min | [mp4](force-explainer/media/FORCE_Complete_Explainer.mp4) |
| [Lie Algebra](lie-algebra/) | Lie Groups and Algebras | ~2 min | [mp4](lie-algebra/media/Lie_Groups_and_Algebras.mp4) |
| [Process Analysis](process-analysis/) | Operations Process Analysis | ~3 min | [mp4](process-analysis/media/Process_Analysis.mp4) |
| [Solar Panel Delamination](solar-panel-delamination/) | Mechanical delamination methods | 2:20 | [mp4](solar-panel-delamination/media/Solar_Panel_Delamination.mp4) |
| [Runway Bitumen](lnt-runway-bitumen/) | Performance Grade Bitumen for Airport Runways | 3:40 | [mp4](lnt-runway-bitumen/media/LnT_Performance_Grade_Bitumen_Final.mp4) |

## Pipeline

The latest project (Runway Bitumen) was generated end-to-end from a 60-slide PowerPoint deck:

```bash
pip install '3brown1blue[slides]'
3brown1blue from-slides deck.pptx --provider claude-code
```

1. **Extract** slide text + speaker notes (auto-detects if vision is needed for diagrams)
2. **Plan** the video scene-by-scene (Opus)
3. **Review** the plan (approve / edit / quit)
4. **Generate** complete Manim code (Opus)
5. **Render** to 1080p video

## License

MIT
