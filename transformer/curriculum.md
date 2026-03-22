# Attention Is All You Need -- Video Curriculum

**Target Duration:** 12-15 minutes
**Audience:** ML-literate viewers who know basic neural networks but haven't deeply understood Transformers
**Central Question:** How does the Transformer process sequences without any recurrence?

---

## Scene Plan (10 Scenes)

### Scene 01: The Sequential Bottleneck (90s)
**Layout:** FULL_CENTER -> DUAL_PANEL
**Concept:** Why RNNs fail at long sequences. The information bottleneck problem.
**Visuals:**
- Sentence "The cat sat on the mat because it was tired" flows through an RNN pipeline
- Each token passes through a narrow hidden state bottleneck (funnel metaphor)
- Color-coded information from early tokens fades as it travels through the chain
- Side-by-side: RNN (sequential, narrow pipe) vs Transformer (all-to-all web)
- Key metric: O(n) sequential steps vs O(1) path length
**Transition:** "What if every word could talk to every other word directly?"

### Scene 02: The Attention Mechanism -- Soft Lookup (90s)
**Layout:** BUILD_UP -> FULL_CENTER
**Concept:** Attention as a soft dictionary lookup. Q, K, V intuition.
**Visuals:**
- Start with a hard dictionary: query -> exact key match -> value returned
- Soften it: query partially matches multiple keys, weighted combination of values
- Animate the attention weight bars (softmax output) summing to 1
- Library analogy: spotlight (query) illuminating books (keys) with varying brightness
- Introduce Q, K, V: same embedding projected through 3 lenses
- Show the dot product between one query and all keys forming a row of scores

### Scene 03: Scaled Dot-Product Attention (90s)
**Layout:** FULL_CENTER -> DUAL_PANEL
**Concept:** The attention formula. Why scale by sqrt(d_k).
**Visuals:**
- Write out: Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V
- Highlight each component step by step
- QK^T: n x n attention matrix forming (animate grid filling with dot products)
- Temperature analogy: show softmax curve, plot where unscaled vs scaled dot products land
- Unscaled (left): softmax saturates -> near one-hot -> vanishing gradients
- Scaled (right): softmax stays in gradient-rich region -> soft distribution
- The variance argument: d_k=64 means std_dev=8, divide by sqrt(64)=8 to normalize

### Scene 04: Multi-Head Attention (90s)
**Layout:** FULL_CENTER -> grid display
**Concept:** Why use multiple attention heads. What different heads learn.
**Visuals:**
- Single 512-dim embedding splits into 8 x 64-dim subspaces (colored slices)
- Each head computes attention independently (8 small attention matrices in parallel)
- Show different heads learning different patterns on the sentence "The animal didn't cross the street because it was too tired":
  - Head 1: diagonal pattern (local/adjacent attention)
  - Head 2: "it" strongly attends to "animal" (coreference)
  - Head 3: verb-subject connection pattern
- Concatenate all head outputs -> project through W^O
- Formula: MultiHead = Concat(head_1,...,head_h) W^O

### Scene 05: Positional Encoding (90s)
**Layout:** BUILD_UP -> FULL_CENTER
**Concept:** How Transformers know word order without recurrence.
**Visuals:**
- Problem statement: permute input tokens, attention gives same result (show this)
- Solution: add position information to embeddings
- Stack of sinusoids at different frequencies (like binary counting but continuous)
- Show how position 0, 1, 2, ... sample different points on each wave
- Low-frequency waves: coarse position (beginning vs end)
- High-frequency waves: fine position (token 5 vs 6)
- The rotation matrix property: PE(pos+k) = M_k * PE(pos)
- Animate: embedding + positional encoding = position-aware embedding

### Scene 06: The Encoder Block (90s)
**Layout:** TOP_PERSISTENT_BOTTOM_CONTENT
**Concept:** Full encoder architecture. Residual connections and layer norm.
**Visuals:**
- Persistent element: the encoder block diagram (self-attention + FFN + add&norm)
- Zoom into each component:
  - Self-attention layer (reference scenes 2-4)
  - Add & Norm: residual stream + layer normalization
  - FFN: position-wise feed-forward (ReLU sandwich, 512 -> 2048 -> 512)
  - Add & Norm again
- The residual stream metaphor: river of information with tributaries
- Show 6 encoder layers stacked, information refining through each
- Trace one word's representation evolving through all 6 layers

### Scene 07: The Decoder and Masking (90s)
**Layout:** DUAL_PANEL -> FULL_CENTER
**Concept:** Decoder architecture. Causal masking. Cross-attention.
**Visuals:**
- Three types of attention:
  1. Encoder self-attention (bidirectional, already covered)
  2. Masked decoder self-attention (the new thing)
  3. Encoder-decoder cross-attention (how decoder reads input)
- Causal mask animation: n x n grid, upper triangle filled with -inf
- After softmax, masked positions become 0 (animate this transition)
- Show autoregressive generation: token by token, mask grows
- Cross-attention: decoder queries attend to encoder keys/values
- "Translating": French words attend to relevant English words

### Scene 08: The Full Architecture (120s)
**Layout:** FULL_CENTER (architecture diagram)
**Concept:** Everything together. End-to-end forward pass.
**Visuals:**
- The iconic Transformer architecture diagram (simplified but complete)
- Trace a translation example end-to-end:
  - Input: "I love learning" -> tokenize -> embed -> add PE
  - Encoder: 6 layers of self-attention + FFN
  - Start decoding: "<start>" -> masked self-attn -> cross-attn -> FFN -> "J'"
  - Continue: "<start> J'" -> predict "aime"
  - Continue until "</end>"
- Highlight the three attention types in different colors on the diagram
- Show parameter counts: base model ~65M params

### Scene 09: Why It Works -- Computational Advantages (60s)
**Layout:** DUAL_PANEL -> BUILD_UP
**Concept:** Parallelization. Training speed. BLEU scores.
**Visuals:**
- Complexity comparison table animated:
  - Self-attention: O(n^2 d), O(1) sequential, O(1) path length
  - RNN: O(n d^2), O(n) sequential, O(n) path length
- Parallelization: RNN processes tokens one by one (slow queue)
  - Transformer processes all tokens simultaneously (instant grid)
- BLEU score comparison bar chart:
  - GNMT: 24.6, ConvS2S: 25.16, Transformer: 28.4
  - Training cost: Transformer uses 1/10th the FLOPs
- "Faster AND better"

### Scene 10: The Legacy (60s)
**Layout:** BUILD_UP
**Concept:** Impact on AI. BERT, GPT, vision, protein folding.
**Visuals:**
- Timeline from 2017 to 2025:
  - 2017: Attention Is All You Need
  - 2018: BERT (encoder-only), GPT (decoder-only)
  - 2020: GPT-3 (175B params), ViT (vision)
  - 2021: AlphaFold 2 (protein structure)
  - 2022-25: ChatGPT, Claude, Gemini, Stable Diffusion
- The 8 authors -> 7 companies founded
- Final frame: "100,000+ citations. One architecture. Every modality."
- Paper title card with all author names
