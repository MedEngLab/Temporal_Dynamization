# Forward and reverse dynamization of a locking plate construct: simulation output data and rule base

Simulation output and the tissue-differentiation rule base in machine-readable form for the article:

> Anders J. Wilhem, Magnus B Madsen, Gargi Shankar Nayak, Sasa Cukovic, Jan Duedal Rolfing, Karupppasamy Subburaj (2026). Forward and Reverse Dynamization of Lockling Plate Constructs: a 3D Mechanobiological Simulation of Osteotomy Healing. *Journal of the Mechanical Behavior of Biomedical Materials*. [DOI]

Dataset: [Authors] (2026). Zenodo. [DOI]. License: CC BY 4.0 (see `LICENSE`).

The article simulated 56 days of healing of a plated 3 mm transverse osteotomy with a three-dimensional finite element model coupled with a fuzzy-logic model of tissue differentiation. It compared constant rigid fixation, constant flexible fixation, forward dynamization (rigid to flexible) and reverse dynamization (flexible to rigid), with two flexible constructs (M, plate modulus 5.09 GPa; H, 0.63 GPa) and switch days 8 and 15. Section, equation and table numbers below refer to the article and its Supplementary Material. The simulation code is not part of this package.

## Contents

```
rule_base/            reference rule base and high-threshold variant (.fis), membership functions, rules
constructs/           empty-gap axial stiffness against plate modulus; the three constructs
simulations/
  runs.csv            the 47 reported simulations and their parameters
  daily/              one CSV per simulation: daily values on days 1 to 56
  daily_columns.csv   definition and unit of every column in daily/
  endpoints_day56.csv day-56 endpoints and eta on day 35
  callus_tests_loading_modes.csv   callus stiffness with the fixator removed in four further loading modes
  comparisons_mesh_decision.csv    ratios of eta between configurations, mesh decision rule, robustness
element_fields/       per-element tissue state and strains of the 22 main simulations on days 1, 8, 15, 21, 35, 56
mesh/                 finite element meshes (Gmsh 4.1) with gap element sizes 0.60, 0.45 and 0.35 mm
examples/read_data.py minimal reading example (Python, NumPy)
```

## Simulations (`simulations/runs.csv`)

47 simulations, 56 days each:

| Analysis | Rule base | Gap element size | Simulations |
|---|---|---|---|
| main | reference | 0.60 mm | 11 configurations |
| mesh refinement | reference | 0.45 mm / 0.35 mm | 7 / 3 |
| main | high-threshold variant | 0.60 mm | 11 configurations |
| mesh refinement | high-threshold variant | 0.45 mm | 3 |
| growth reference length (0.6 and 1.0 mm) | reference | 0.60 mm | 8 |
| initial soft-tissue modulus (1 MPa) | reference | 0.60 mm | 4 |

Run identifiers combine the rule base (`reference`, `variant`) and the configuration name used in the figures: `Rigid`, `Flex-M`, `Flex-H`, `Fwd-M15` (forward dynamization, construct M, switch on day 15), `Fwd-M8`, `Rev-M15`, `Rev-M8`, `Fwd-H15`, `Fwd-H8`, `Rev-H15`, `Rev-H8`. Suffixes mark the parameter that differs from the main simulations: `_h0.45` and `_h0.35` (gap element size, mm), `_lref0.6` and `_lref1.0` (growth reference length, mm; main value 0.8 mm), `_Esoft1` (initial soft-tissue modulus 1 MPa; main value 3 MPa). Columns of `runs.csv`: rule base, strategy, construct, switch day, plate modulus before and after the switch (MPa), gap element size, growth reference length, initial soft-tissue modulus, analysis, and whether element fields are included.

## Daily values (`simulations/daily/<run_id>.csv`)

One row per day. `daily_columns.csv` defines every column. Quantities with the plate in place (gap closure, construct stiffness, plate load share, element strains, stimulated volume) come from the solution of that day with the tissue state at the start of the day. Tissue fractions, perfusion, eta and bridging refer to the tissue state after that day's update. Strains are fractions (0.001 = 0.1%). Hydrostatic strain is the mean of the principal strains; distortional strain is (1/sqrt 2) [(e1 - e2)^2 + (e1 - e3)^2 + (e2 - e3)^2]^(1/2) (article Eq. 2). All gap quantities are volume-weighted means over the gap elements unless stated otherwise.

## Tables

- `endpoints_day56.csv`: eta on days 35 and 56, tissue fractions, near- and far-half bone fraction, first day of bony bridging (empty: no bridging by day 56), bridged bony area, plate load share and construct stiffness relative to the intact bone on day 56, for all 47 simulations (article Table 2; Supplementary Tables S4a, S4b, S6).
- `callus_tests_loading_modes.csv`: callus stiffness with the fixator removed (plate modulus 1 MPa) on days 35 and 56 in axial compression without tilt (prescribed axial displacement of 0.01 mm of the loaded face; load = reaction force), bending in the plane of the plate (near-far), bending in the perpendicular plane, and torsion (moment 1000 N mm). Stiffness = load divided by the relative displacement or rotation of the two bone faces of the gap; eta = stiffness divided by the same test with a bone-filled gap (Supplementary Sect. S2.1, Table S5). The axial test with the loaded face free to tilt is the primary test and is in `daily/` (column `eta`).
- `comparisons_mesh_decision.csv`: ratios R = eta_numerator / eta_denominator on day 56 on the 0.6, 0.45 and 0.35 mm meshes, for the comparisons reported in the article. Paired comparisons (both configurations also computed on a finer mesh) are resolved if |R_0.6 - 1| exceeds `mesh_bound` = max |R_0.6 - R_h|; unpaired comparisons if |R_0.6 - 1| exceeds `mesh_bound` = delta R_0.6, with delta the largest relative change among the paired comparisons of the same rule base (article Sect. 2.6, Eqs. 7 and 8). `direction`: 1 if R > 1, -1 if R < 1. `robust`: resolved with both rule bases in the same direction.

## Constructs (`constructs/`)

- `plate_modulus_calibration.csv`: axial stiffness of the construct with an empty gap (gap modulus 0.001 MPa) for five plate moduli, and the reduction factor relative to the rigid construct (article Sect. 2.3).
- `constructs.csv`: the rigid construct and constructs M and H: plate modulus, empty-gap axial stiffness, reduction factor, gap closure at the near and far cortex under 200 N with an empty gap (micrometers), and interfragmentary strain and plate load share on day 1 with soft tissue in the gap (3 MPa) (article Table 1).

The plate modulus sets the construct stiffness; it does not represent a plate material.

## Rule base (`rule_base/`)

- `reference_rule_base.fis` (19 rules) and `high_threshold_variant.fis` (rules 1 to 17, wider low strain sets): Mamdani systems in the text format of the MATLAB Fuzzy Logic Toolbox (minimum for conjunction and implication, maximum for aggregation, centroid defuzzification; the article evaluated the centroid on 193 points per output range). Variable names follow the article: inputs `cartilage_fraction`, `bone_fraction`, `hydrostatic_strain`, `distortional_strain`, `perfusion`, `max_neighbor_perfusion`, `max_neighbor_bone_fraction`; outputs `perfusion_change`, `bone_fraction_change`, `cartilage_fraction_change` (daily changes). In the rule lines, a negative index means "not" (complement of the membership).
- `membership_functions.csv`: all sets with shape (trapezoid a, b, c, d or triangle a, b, c) and parameters (Supplementary Tables S1 and S2).
- `rules.csv`: all rules with the input conditions and output sets (Supplementary Table S3). Empty cell: input not used or output not affected.

Daily changes of bone fraction and perfusion were multiplied by l_ref / l_el outside the band of elements within 0.6 mm of a bone face; in that band, neighbor perfusion and neighbor bone fraction were set to 1 (article Sect. 2.4).

## Element fields (`element_fields/`)

- `gap_elements_0.60mm.csv`: the 47,584 gap elements of the 0.60 mm mesh: centroid coordinates (mm), volume (mm^3), `near_half` (1 for the half of the gap next to the plate, x > 0) and `bone_face_band` (1 for elements whose centroid lies within 0.6 mm of a bone face). Coordinates: z along the bone axis, gap between z = 100 and 103 mm, plate on the +x side.
- `<run_id>.npz` (22 main simulations, both rule bases; NumPy compressed archive): `days` (1, 8, 15, 21, 35, 56) and arrays of shape (6, 47584), float32, in the element order of `gap_elements_0.60mm.csv`: `bone_fraction`, `cartilage_fraction`, `soft_tissue_fraction`, `perfusion`, `modulus_MPa` (article Eq. 4), `hydrostatic_strain`, `distortional_strain`. Tissue fractions and modulus are after the update of that day; strains are from the solution of that day. Read with `numpy.load`.

## Meshes (`mesh/`)

Gmsh 4.1 meshes of the model (quadratic displacement elements were used on these linear tetrahedral meshes). Physical groups: volumes 1 bone, 2 gap, 3 plate, 4 screws, 5 plate segment spanning the gap; surfaces 11 loaded face, 12 fixed face, 13 proximal bone face of the gap, 14 distal bone face of the gap. The 0.60 mm mesh was used for all main simulations; the gap element order of `element_fields/` is not the cell order of the `.msh` file (match by centroid if needed).

## Checksums

`SHA256SUMS` lists the SHA-256 checksum of every file.
