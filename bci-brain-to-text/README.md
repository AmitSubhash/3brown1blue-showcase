# Brain-to-Text BCI for Pontine Stroke

A 3Blue1Brown-style animated explainer of a groundbreaking brain-computer interface study that restores speech in a person with pontine stroke-induced dysarthria.

## The Paper

**Restoring brain-to-text communication in a person with dysarthria from pontine stroke using an intracortical brain-computer interface**

Nason-Tomaszewski, Deevi, Rabbani et al. (2026) -- BrainGate2 Clinical Trial

Paper: [https://www.medrxiv.org/content/10.64898/2026.02.19.26346583v1.full.pdf](https://www.medrxiv.org/content/10.64898/2026.02.19.26346583v1.full.pdf)

### What the paper shows

- A single 64-channel microelectrode array (3.2 x 3.2 mm) placed in orofacial motor cortex can decode mimed speech into text
- Achieved 19.6% word error rate on a 125,000-word vocabulary
- 60.8% reduction in WER compared to prior surface electrode (ECoG) approaches
- Enabled real conversational Q&A at 27.7 words per minute
- Stable neural decoding over 736 days (2+ years) with rapid recalibration

## The Video

`BCI_Explainer_Full.mp4` -- 3 minutes 30 seconds, 8 animated scenes built with Manim (Community Edition).

### Scenes

| # | Scene | What it covers |
|---|-------|---------------|
| 1 | Hook | Neural spikes decoded into text, key result reveal |
| 2 | The Problem | Pontine stroke, dysarthria, preserved cortex |
| 3 | Prior Art | ECoG vs intracortical BCI landscape |
| 4 | Array Placement | MRI-guided targeting of area 6v, 64-channel electrode grid |
| 5 | Decoding Pipeline | Neural signals to features to RNN phoneme decoder to language model |
| 6 | Results | WER across vocabulary sizes, example sentences, conversational Q&A |
| 7 | Stability | 736-day recording stability, cross-session drift, rapid recalibration |
| 8 | Takeaway | Key findings and future directions |

## Status: Beta

This is a beta version. Planned improvements:

- Voice narration synced to animations
- Improved frame compositions and visual polish
- More detailed zoom-ins on the RNN architecture and language model pipeline
- Animated data flowing through the electrode grid
- Side-by-side comparison with real figure panels from the paper

The goal is to explain cutting-edge research to a broad audience in the clearest, most engaging way possible. Science should be accessible to everyone.

## Built With

- [Manim Community Edition](https://www.manim.community/) -- mathematical animation engine
- 3Brown1Blue skill system -- shared style contracts, production quality rules, visual design principles from 3Blue1Brown frame analysis
