# TheHuzz: Research Notes

## Paper Metadata
- **Title**: TheHuzz: Instruction Fuzzing of Processors Using Golden-Reference Models for Finding Software-Exploitable Vulnerabilities
- **Authors**: Rahul Kande, Addison Crump, Garrett Persyn (Texas A&M); Patrick Jauernig, Ahmad-Reza Sadeghi (TU Darmstadt); Aakash Tyagi, Jeyavijayan Rajendran (Texas A&M)
- **Venue**: USENIX Security 2022
- **PDF**: https://www.usenix.org/system/files/sec22-kande.pdf
- **arXiv**: 2201.09941

## Core Problem
Modern processors are massively complex. Bugs baked into silicon CANNOT be patched post-fabrication. Existing verification approaches all have critical gaps:
- **Formal verification**: State-space explosion (JasperGold found only 48% of bugs in a competition)
- **Information flow tracking**: Label pollution, manual assignment, false positives
- **Prior hardware fuzzers (RFUZZ, DifuzzRTL)**: Limited HDL support, limited coverage metrics, miss bugs in combinational logic

## Key Insight (3 Combined Ideas)
1. **Fuzz at the ISA abstraction level**: Generate assembly instructions (the natural processor input), not raw signals
2. **Use ISA simulators as golden-reference oracles**: Differential testing -- run same instructions on RTL (DUT) and golden model (Spike/or1ksim), any mismatch = bug
3. **6 comprehensive coverage metrics**: Statement, branch, condition, expression, toggle, FSM -- captures signal transitions, floating wires, combinational logic that prior fuzzers miss

## Architecture (Pipeline)
1. **Seed Generator**: Produces C programs with Configuration Instructions (CIs, baremetal setup) + 20 Test Instructions (TIs, the fuzzing payload). Compiled via GCC.
2. **Stimulus Generator**: Mutates TIs using 12 AFL-inspired mutations (bitflips, arithmetic, random byte, delete, clone, opcode overwrite). Two types: Type 1 (data bits only), Type 2 (data + opcode bits -- generates illegal instructions).
3. **RTL Simulation**: Run mutated binary on DUT via Synopsys VCS or ModelSim. Collect 6 coverage metrics + instruction trace.
4. **Golden Reference Execution**: Run same binary on Spike (RISC-V) or or1ksim (OpenRISC). Collect instruction trace.
5. **Comparator**: Compare traces instruction-by-instruction. Mismatch in register values, flags, or memory = potential bug.
6. **Feedback Loop**: Coverage data guides mutation engine (keep best instruction-mutation pairs, discard underperformers).
7. **Optimizer**: Solves set-cover problem (IBM CPLEX) to find minimal subset of instruction-mutation pairs covering all coverage points. Produces weights fed back to generators.

## 12 Mutation Techniques
M0-M4: Bitflips (1/1, 2/1, 4/1, 8/8, 16/8)
M5-M7: Arithmetic (8/8, 16/8, 32/8) -- +/- value 0-35
M8: Random byte overwrite
M9: Delete instruction
M10: Clone instruction
M11: Opcode bits overwrite (generates illegal instructions)

## 6 Coverage Metrics
1. **Statement**: Every line of RTL executed
2. **Branch**: Every if/else tested true and false
3. **Condition**: Every sub-condition in compound expressions tested independently
4. **Expression**: All combinational logic blocks tested for all input combinations. Covers MUX select lines.
5. **Toggle**: Every DFF toggles between 0, 1, and z (tristate)
6. **FSM**: All state register values and transitions covered

Key point: DifuzzRTL only uses control-register coverage (misses combinational logic). RFUZZ only uses mux-coverage (misses MUXes implemented as gates, not control flow).

## Results
- **4 processors tested**: Ariane (RISC-V, 20K LOC), Rocket Core (RISC-V, 10K LOC), mor1kx (OpenRISC, 22K LOC), or1200 (OpenRISC, 31K LOC)
- **11 bugs found** (8 new, 3 known)
- **5 CVEs filed**: CVE-2021-41612, CVE-2021-41614, CVE-2021-41613, CVE-2021-40506, CVE-2021-40507
- **2 full exploits demonstrated**: Arbitrary code execution (Ariane FENCE.I), Privilege escalation (mor1kx EPCR)
- **1.98x faster** than industry random regression
- **3.33x faster** than DifuzzRTL for same coverage

## Key Bugs
- **B1 (Ariane)**: FENCE.I decode incorrectly requires imm/rs1=0. Valid instructions declared illegal.
- **B3 (Ariane)**: Illegal instructions allowed to execute (undocumented feature)
- **B4 (Ariane)**: Cache coherency violation not detected without FENCE.I
- **B5 (mor1kx)**: Carry flag wrong for subtract -- corrupts crypto. CVE-2021-41612
- **B6 (mor1kx)**: No privilege check on EPCR register -- user-mode escalation. CVE-2021-41614
- **B9/B10 (or1200)**: Overflow flag wrong for multiply/subtract. CVE-2021-40506/40507

## Exploit: FENCE.I on Ariane
1. Attacker has "safe" JIT compiler
2. Loads code into instruction cache
3. Overwrites memory region with malicious payload
4. Executes FENCE.I (should flush cache, but Ariane rejects it)
5. Processor runs stale cache = attacker's original code
6. Stack overflow -> arbitrary code execution
- Spike (golden model) correctly flushes cache. Ariane does not. Mismatch detected.

## Exploit: EPCR on mor1kx
1. User-mode process writes to EPCR (Exception Program Counter Register)
2. No privilege check = write succeeds
3. Trigger exception return
4. Processor loads PC from EPCR (attacker-controlled)
5. Execution jumps to attacker function at supervisor privilege
6. Privilege escalation achieved

## Why Prior Fuzzers Miss Bugs (Cache Controller Case Study, Fig 2)
- Circuit has: 7 input DFFs, 2 MUXes, combinational logic blocks, state DFF, output DFFs
- DifuzzRTL: Only sees MUXes as control-flow constructs (when/if). Misses MUXes implemented as AND/OR/NOT gates. Detected 1 MUX + 2 control registers. Missed sel1 and all combinational logic.
- RFUZZ: Only tracks 2:1 MUX select signals. Also misses gate-level MUXes. Detected 1 select signal.
- TheHuzz: 6 coverage metrics cover ALL of these. Expression coverage catches combinational logic. Toggle coverage catches all DFFs.
