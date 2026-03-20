# Manim Showcase

Animated explainer videos generated from slide decks using [`3brown1blue`](https://pypi.org/project/3brown1blue/).

## Pipeline

```
PowerPoint slides -> text extraction -> Opus plans the video -> Opus generates Manim code -> render
```

## Projects

| Project | Source | Duration | Scenes |
|---------|--------|----------|--------|
| [Performance Grade Bitumen for Airport Runways](lnt-runway-bitumen/) | 60-slide L&T deck | 3:40 | 9 |

## How it works

```bash
pip install '3brown1blue[slides,anthropic]'
3brown1blue from-slides deck.pptx --provider claude-code --render
```

The `from-slides` command:
1. Extracts text + speaker notes from PPTX (auto-detects if vision is needed for diagrams)
2. Plans the video scene-by-scene with a detailed prompt
3. Shows you the plan for review/edit
4. Generates complete Manim Python code
5. Renders to 1080p video

Built with [Manim Community Edition](https://www.manim.community/).
