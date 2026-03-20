# DOT Explainer: Deep Research Document

## Sources Consulted

### Core Papers & Reviews
1. [Diffuse Optics for Tissue Monitoring and Tomography (Durduran et al., PMC4482362)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4482362/)
2. [Tutorial on Monte Carlo simulation of photon transport (PMC9979671)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9979671/)
3. [High-density DOT for imaging brain function (Eggebrecht/Culver, RSI 2019)](https://pubmed.ncbi.nlm.nih.gov/31153254/)
4. [DOT to investigate the newborn brain (Pediatric Research)](https://www.nature.com/articles/pr2017107)
5. [Functional Imaging of Developing Brain at Bedside (PMC4785947)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4785947/)
6. [A Review of Image Reconstruction Algorithms for DOT (MDPI 2023)](https://www.mdpi.com/2076-3417/13/8/5016)
7. [Revisiting the Rytov approximation (Scientific Reports 2024)](https://www.nature.com/articles/s41598-024-82682-3)
8. [Depth of the banana and impulse stripe illumination](https://arxiv.org/html/2208.07718)
9. [Age-related changes in DOT sensitivity profiles in infancy (PLOS ONE)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0252036)
10. [Direct approach to compute Jacobians using perturbation MC (PMC6179418)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6179418/)
11. [Modified Beer-Lambert law revisited](https://pubmed.ncbi.nlm.nih.gov/16481677/)
12. [OpenFNIRS Modified Beer-Lambert tutorial](https://openfnirs.org/2024/01/01/modified-beer-lambert-law/)
13. [Optical properties of biological tissues review (Jacques 2013)](https://omlc.org/news/dec14/Jacques_PMB2013/Jacques_PMB2013.pdf)
14. [Advancing Image Reconstruction: Regularization Methods (2025)](https://link.springer.com/article/10.1007/s11220-025-00574-w)
15. [CW-DOT in Human Brain Mapping review (Sensors 2025)](https://www.mdpi.com/1424-8220/25/7/2040)

### Tutorials & Explainers
- [Radiative transfer & diffusion theory (Wikipedia)](https://en.wikipedia.org/wiki/Radiative_transfer_equation_and_diffusion_theory_for_photon_transport_in_biological_tissue)
- [fNIRS Wikipedia](https://en.wikipedia.org/wiki/Functional_near-infrared_spectroscopy)
- [Artinis NIRS Theory](https://www.artinis.com/theory-of-nirs)
- [Avantier: How DOT Works](https://avantierinc.com/resources/knowledge-center/diffuse-optical-tomography/)
- [Lessons from Grant Sanderson](https://www.antoinebuteau.com/lessons-from-grant-sanderson/)

---

## Domain Knowledge: Complete Chain

### Level 0: The Big Picture
DOT is a medical imaging technique that uses near-infrared light (650-950nm) to see inside living tissue, especially neonatal brains. It's non-invasive, portable, bedside-ready, and safe. It measures changes in blood oxygenation (hemodynamics) which correlate with brain activity.

**Why NIR light?** There's an "optical window" between 650-950nm where:
- Water absorption is low
- Hemoglobin absorption is moderate (measurable but not total)
- Light can penetrate several centimeters into tissue
- Below 650nm: blood absorbs too strongly
- Above 950nm: water absorbs too strongly

### Level 1: Tissue-Light Interaction

**Two things happen to photons in tissue:**

1. **Scattering** (dominant): photon bounces off cellular structures (mitochondria, membranes, nuclei). Described by scattering coefficient mu_s [cm^-1]. In brain tissue: mu_s' ~ 8-12 cm^-1 (reduced scattering). The anisotropy factor g ~ 0.9 (strongly forward-scattering).

2. **Absorption** (what we measure): photon is absorbed by chromophores (mainly HbO2 and HbR). Described by absorption coefficient mu_a [cm^-1]. In brain tissue: mu_a ~ 0.1-0.3 cm^-1. Much smaller than scattering => diffusion regime.

**Key ratio: mu_s' >> mu_a** (scattering dominates by ~50x). This means light doesn't travel in straight lines -- it DIFFUSES through tissue like heat through a conductor. This is the "diffusion regime."

**Henyey-Greenstein phase function**: p(cos_theta) = (1-g^2) / (4pi * (1+g^2 - 2g*cos_theta)^(3/2))
- g = 0: isotropic scattering
- g = 0.9: strongly forward (typical for tissue)
- g = 1: no scattering (ballistic)

### Level 2: The Transport Hierarchy

**Full story: Radiative Transfer Equation (RTE)**
The most general equation governing photon transport. Tracks radiance L(r, s_hat, t) at position r, direction s_hat, time t. Too complex to solve analytically for most geometries.

**Simplification 1: Monte Carlo**
Don't solve the equation -- simulate individual photons. Launch millions, track each one's random walk (hop -> drop -> spin -> check). Statistical sampling gives accurate results. This is the "ground truth" for DOT forward modeling.

MC process per photon:
1. Launch: position + direction + weight=1
2. HOP: step size s = -ln(RND)/mu_t where mu_t = mu_a + mu_s
3. DROP: deposit weight W*(1-exp(-mu_a*s)) at current voxel
4. SPIN: sample new direction via Henyey-Greenstein, update direction cosines
5. CHECK: Russian roulette if weight < threshold
6. Repeat until photon exits or is terminated

**Simplification 2: Diffusion Equation**
When mu_s' >> mu_a, the radiance becomes nearly isotropic after many scattering events. The P1 approximation of the RTE gives the diffusion equation:

(1/c) * d_phi/dt - D * nabla^2(phi) + mu_a * phi = S(r,t)

where:
- phi(r,t) = fluence rate [W/cm^2]
- D = 1/(3*(mu_a + mu_s')) = diffusion coefficient [cm]
- c = speed of light in medium [cm/s]
- S = source term

For CW (continuous wave, steady state): D * nabla^2(phi) - mu_a * phi = -S(r)

### Level 3: Green's Functions and the Banana

**Green's function G(r_s, r)**: The fluence rate at position r due to a point source at r_s. For infinite homogeneous medium:

G(r_s, r) = exp(-mu_eff * |r - r_s|) / (4*pi*D*|r - r_s|)

where mu_eff = sqrt(mu_a / D) = effective attenuation coefficient.

**THE BANANA SHAPE**: For a source-detector pair (r_s, r_d), the sensitivity of the measurement to a perturbation at point r is:

J(r) = G(r_s, r) * G(r, r_d)

This is the PRODUCT of two Green's functions:
- G(r_s, r): how much light from the source reaches point r
- G(r, r_d): how much light from point r reaches the detector (by reciprocity)

The product peaks in a banana-shaped region between source and detector because:
- Near the surface: both Green's functions are large, but the overlap is narrow
- Deep inside: the Green's functions spread out and overlap broadly, but each is weaker
- The product creates a curved region of maximum sensitivity

**Banana depth**: approximately 0.2 * d_SD (source-detector separation)
- Close S-D (10mm): shallow sensitivity (scalp, skull)
- Medium S-D (30mm): cortical sensitivity
- Far S-D (40mm+): deep brain, but very weak signal

### Level 4: The Forward Model and A Matrix

**Linearized forward model (Born/Rytov approximation):**

delta_y = A * delta_x

where:
- delta_y [M x 1]: changes in log-intensity at M source-detector pairs
- A [M x N]: sensitivity (Jacobian) matrix, M measurements x N voxels
- delta_x [N x 1]: changes in optical properties (mu_a) at N voxels

**Each ROW of A** = one source-detector pair's banana-shaped sensitivity profile, discretized onto the voxel grid.

**Each COLUMN of A** = one voxel's influence on all measurements.

**Building A**: For each of M source-detector pairs:
1. Compute G_source(r) for all voxels (forward Green's function)
2. Compute G_detector(r) for all voxels (adjoint Green's function, same form by reciprocity)
3. A[m, n] = G_source(r_n) * G_detector(r_n) * volume_n

This can be done analytically (diffusion model) or numerically (Monte Carlo).

### Level 5: Why Two Wavelengths? Hemoglobin Spectroscopy

**The point of DOT**: We measure changes in absorption. But absorption comes from TWO chromophores:
- HbO2 (oxyhemoglobin): has specific absorption spectrum
- HbR (deoxyhemoglobin): has different absorption spectrum
- Isosbestic point: 805nm (both absorb equally)

**Using two wavelengths** (e.g., 690nm and 830nm):
- At 690nm: HbR absorbs more than HbO2
- At 830nm: HbO2 absorbs more than HbR

delta_mu_a(lambda) = epsilon_HbO2(lambda) * delta[HbO2] + epsilon_HbR(lambda) * delta[HbR]

Two wavelengths, two unknowns => solvable!

This gives us maps of delta[HbO2] and delta[HbR], which relate to:
- Neural activation (neurovascular coupling): increased HbO2, decreased HbR
- Blood volume changes
- Oxygen metabolism

### Level 6: Flat Field and Calibration

**The problem**: Raw measurements include systematic confounds:
- Optode-scalp coupling (how well the fiber touches skin)
- Source power variations
- Detector gain differences
- Hair, skin pigmentation

**Flat field approach**:
1. Measure baseline y_0 when brain is at rest (no task/stimulus)
2. Measure y_task during brain activity
3. Compute delta_y = ln(y_task / y_0) -- this cancels coupling factors!

This is why DOT measures CHANGES, not absolute values. The ratio/log subtraction eliminates all the messy calibration factors.

**Modified Beer-Lambert Law**:
delta_OD = -ln(I/I_0) = sum_i(epsilon_i * delta_c_i * DPF * d) + G

where DPF = differential pathlength factor (accounts for scattering increasing path length)

### Level 7: Image Reconstruction

**The inverse problem**: Given delta_y and A, find delta_x.

Problem: A is M x N where typically N >> M (more voxels than measurements). The system is:
- **Underdetermined**: infinitely many solutions
- **Ill-posed**: small noise in measurements -> large artifacts in image
- **Ill-conditioned**: A has many near-zero singular values

**Solution: Regularized pseudoinverse**

delta_x = (A^T A + lambda * L^T L)^(-1) * A^T * delta_y

where:
- lambda = regularization parameter (controls smoothness vs fidelity)
- L = regularization operator (identity for Tikhonov-0, gradient for Tikhonov-1)
- Small lambda: faithful to data, but noisy
- Large lambda: smooth, but loses spatial detail

**Depth compensation**: The sensitivity of DOT falls off with depth. Without correction, activations are "pulled" toward the surface. A depth compensation matrix M weights deeper voxels more:

delta_x = M * (A^T A + lambda * I)^(-1) * A^T * delta_y

### Level 8: HD-DOT (High Density)

**The innovation**: Instead of sparse optode arrays (fNIRS: ~20 channels), use DENSE overlapping arrays (HD-DOT: ~1000+ channels).

**Why density matters**:
- More source-detector pairs = more rows in A
- Overlapping measurements at multiple S-D distances = information at multiple depths
- Short-separation channels (~8mm) measure superficial (scalp blood flow)
- Long-separation channels (~30mm) measure cortical signal
- Can REGRESS OUT scalp hemodynamics!

**Result**: HD-DOT approaches fMRI spatial resolution (~1cm) while being:
- Portable (can go to the NICU)
- Silent (no scanner noise)
- Baby-friendly (no sedation, no immobilization)
- Continuous (can monitor for hours)

---

## Curriculum Design

### The "Aha" Moment
The surprising connection: "The sensitivity pattern (banana shape) is literally the PRODUCT of two Green's functions -- light traveling from source to voxel, times light traveling from voxel to detector. The math IS the physics."

### Scene Plan (15 minutes total)

**Scene 1: Why Light? The Optical Window (1.5 min)**
- Show electromagnetic spectrum
- Zoom into NIR window (650-950nm)
- Show water absorption curve + hemoglobin curves
- The sweet spot where we can see but not destroy

**Scene 2: Scattering vs Absorption (2 min)**
- Single photon enters tissue
- Show scattering: bouncing off cell structures (random walk)
- Show absorption: photon disappears (weight drops)
- Parameter sweep: mu_s slider changes how jagged the path is
- Parameter sweep: mu_a slider changes how many photons survive
- Key insight: scattering >> absorption means DIFFUSION

**Scene 3: From Random Walk to Diffusion (2 min)**
- Show many photons simultaneously (Monte Carlo)
- As more photons accumulate, the DENSITY field emerges
- The density field IS the solution to the diffusion equation
- Morph: particle simulation -> smooth fluence field
- Show diffusion equation, link each term to what we just saw

**Scene 4: Two Wavelengths, Two Chromophores (1.5 min)**
- Show HbO2 and HbR absorption spectra (actual curves)
- Highlight: at 690nm HbR dominates, at 830nm HbO2 dominates
- Isosbestic point at 805nm
- Two equations, two unknowns -> solvable
- Dual view: both wavelength measurements side by side

**Scene 5: The Banana Shape (2 min)**
- Source on surface, detector on surface
- Show Green's function from source (decaying sphere)
- Show Green's function from detector (another decaying sphere)
- MULTIPLY THEM: banana shape emerges!
- This is the KEY visual proof: banana = G_s * G_d
- Parameter sweep: move detector farther -> banana goes deeper
- Show actual banana depth rule: depth ~ 0.2 * separation

**Scene 6: Building the A Matrix (2 min)**
- Array of sources and detectors on head
- Each pair has a banana -> show all bananas overlapping
- Stack bananas as rows of a matrix -> A matrix emerges
- The matrix IS the collection of all banana shapes
- Dual view: physical bananas on left, matrix heatmap on right
- Column view: one voxel's influence across all measurements

**Scene 7: Flat Field and Why We Measure Changes (1.5 min)**
- Show messy raw signal (coupling, noise, hair)
- Baseline measurement: y_0
- Task measurement: y_task
- Divide: y_task/y_0 cancels the mess!
- What remains: the CHANGE in absorption
- delta_y = A * delta_x

**Scene 8: Solving the Inverse Problem (2 min)**
- Show the equation delta_y = A * delta_x
- Problem: more unknowns than equations (underdetermined)
- Visual: infinite solutions exist (show several)
- Regularization: add a smoothness constraint
- lambda slider: too small (noisy), too large (blurry), just right
- Final reconstructed image appears

**Scene 9: HD-DOT and the Neonatal Brain (1 min)**
- Show dense array on baby head
- Many overlapping bananas at different depths
- Short channels: see scalp
- Long channels: see cortex
- Regress out scalp -> clean cortical signal
- Show actual-looking reconstructed activation map

**Scene 10: The Full Pipeline (0.5 min)**
- Light -> Tissue -> Scatter -> Measure -> Subtract baseline -> Multiply A^dagger -> Image
- "Non-invasive. Portable. Safe for babies."
- Final frame
