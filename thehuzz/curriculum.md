# TheHuzz: Curriculum Design

## Target: ~12-15 minute explainer video
## Audience: CS/security-aware viewer who may not know hardware verification

## Concept Sequence (12 Scenes)

### Act I: The Problem (Scenes 1-3, ~3 min)

**Scene 1: Hook** (~30s)
- Punchline first: "This tool found 11 bugs in real processors, 5 CVEs, and demonstrated actual exploits"
- Show processor chip -> cracks appear -> bug icons emerge
- "How do you find bugs in silicon that can't be patched?"

**Scene 2: Why Hardware Bugs Are Different** (~60s)
- Dual panel: Software bug (patch deployed, fixed) vs Hardware bug (stuck in billions of chips forever)
- The cost: Intel Pentium FDIV bug ($475M recall), Spectre/Meltdown (unfixable in deployed chips)
- Key point: The stakes are enormous. You must find bugs BEFORE tapeout.

**Scene 3: The Verification Gap** (~90s)
- Show three existing approaches as columns, each with a fatal flaw:
  - Formal verification: State space explosion (show exponential growth, 10^58 states)
  - Manual review: JasperGold found only 48% of bugs
  - Prior fuzzers: RFUZZ/DifuzzRTL miss combinational logic
- Visual: "coverage map" where large dark regions = unexplored areas
- Transition: "What if we had an answer key?"

### Act II: The Idea (Scenes 4-5, ~3 min)

**Scene 4: The Golden Reference Model** (~90s)
- "Aha" moment: Every ISA has a software simulator that defines correct behavior
- Visual: Split screen -- same instruction sequence feeds into DUT (chip) and Golden Model (software)
- Outputs compared: match = OK, mismatch = BUG
- Like having the teacher's answer key for every possible test
- Show Spike (RISC-V) and or1ksim (OpenRISC) as concrete examples

**Scene 5: TheHuzz Architecture Overview** (~90s)
- Full pipeline diagram with labeled boxes, built up progressively:
  Seeds -> Stimulus Generator -> [DUT | Golden Model] -> Comparator -> Bug
  with feedback loop from coverage back to stimulus generator
- Each box lights up as it's explained
- Keep this as persistent header for subsequent detail scenes

### Act III: How It Works (Scenes 6-9, ~5 min)

**Scene 6: Seed Generation and Mutation** (~90s)
- Show a test program: CIs (setup, grayed out) + 20 TIs (the payload, highlighted)
- Mutation visualization: Take a binary instruction, apply bitflips, arithmetic mods
- Key insight: Type 2 mutations can create ILLEGAL instructions (opcode bits change)
- Show instruction morphing from valid ADD to something not in the ISA spec
- "Testing what happens when the processor sees something unexpected"

**Scene 7: The 6 Coverage Metrics** (~90s)
- Gate-level circuit diagram (from paper's Fig 2, simplified)
- Light up different parts as each metric is explained:
  - Statement: which lines execute (light up RTL code lines)
  - Branch: both sides of if/else (fork in path)
  - Expression: combinational logic gates tested (AND/OR gates glow)
  - Toggle: flip-flops toggling 0/1/z (binary display animation)
  - FSM: state machine transitions (state diagram with edges)
- Dual panel comparison: What DifuzzRTL sees (sparse) vs What TheHuzz sees (comprehensive)

**Scene 8: The Optimization Loop** (~60s)
- Set cover visualization: Grid of coverage points (dots)
- Each instruction-mutation pair covers some dots (colored circles)
- Problem: Find minimum number of circles to cover all dots
- Animation: Greedy/optimal selection, dots getting covered
- Output: Weights assigned to each instruction and mutation type

**Scene 9: Bug Detection -- Trace Comparison** (~60s)
- Two parallel instruction traces scrolling (DUT vs Golden Model)
- Instructions match, match, match... then MISMATCH (highlighted red)
- Zoom into the mismatch: register value differs
- "The golden model says the carry flag should be 1. The processor says 0."
- This is bug B5 (mor1kx carry flag, CVE-2021-41612)

### Act IV: Results and Impact (Scenes 10-12, ~3 min)

**Scene 10: Results Dashboard** (~60s)
- Chart: Coverage over time -- TheHuzz vs DifuzzRTL vs Random (from paper's Fig 5)
- Table: 4 processors, 11 bugs, 5 CVEs
- Highlight: 3.33x faster than DifuzzRTL, 1.98x faster than random regression
- Bug B5 found in only 20 instructions

**Scene 11: Exploit Walkthrough** (~90s)
- Pick the FENCE.I exploit (most visual):
  1. Show instruction cache and memory as two boxes
  2. JIT compiler loads code into cache
  3. Memory overwritten with malicious payload
  4. FENCE.I issued (should flush cache)
  5. Split: Spike flushes cache (correct) vs Ariane rejects FENCE.I (incorrect)
  6. Ariane runs stale cache = attacker's code
  7. Arrow: arbitrary code execution
- "TheHuzz found this by detecting the mismatch between Spike and Ariane's FENCE.I handling"

**Scene 12: Takeaway** (~30s)
- TheHuzz pipeline fades back in (from Scene 5)
- Key numbers overlay: 11 bugs, 5 CVEs, 2 exploits, 3.33x faster
- "Golden reference models turn hardware verification into a searchable problem"
- Paper citation and USENIX Security 2022

## "Aha" Moments
1. Scene 4: The golden model concept -- you already HAVE the answer key
2. Scene 7: Why more coverage metrics catch more bugs -- the gate-level revelation
3. Scene 9: The trace comparison mismatch -- simple but powerful
4. Scene 11: How a single decode bug enables arbitrary code execution
