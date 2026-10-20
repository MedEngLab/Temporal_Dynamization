"""Minimal reading example (Python 3 with NumPy; Matplotlib optional). Run from the package root:
    python examples/read_data.py
"""
import csv
import numpy as np

runs = list(csv.DictReader(open("simulations/runs.csv")))
main = [r["run_id"] for r in runs if r["analysis"] == "main" and r["rule_base"] == "reference rule base"]

# eta on day 56 for the 11 configurations with the reference rule base
for rid in main:
    rows = list(csv.DictReader(open(f"simulations/daily/{rid}.csv")))
    print(f"{rid:24s} eta(day 56) = {float(rows[-1]['eta']):.4f}")

# element fields: stimulated volume on day 8 from the element strains (article Eq. 5)
el = list(csv.DictReader(open("element_fields/gap_elements_0.60mm.csv")))
vol = np.array([float(e["volume_mm3"]) for e in el])
z = np.load("element_fields/reference_Flex-M.npz")
k = list(z["days"]).index(8)
stim = (np.abs(z["hydrostatic_strain"][k]) >= 2e-4) & (z["distortional_strain"][k] >= 3e-4)
print("reference_Flex-M, day 8: stimulated volume =", round(float(vol[stim].sum() / vol.sum()), 4))

try:
    import matplotlib.pyplot as plt
    for rid in main:
        rows = list(csv.DictReader(open(f"simulations/daily/{rid}.csv")))
        plt.plot([int(r["day"]) for r in rows], [float(r["eta"]) for r in rows], label=rid.split("_", 1)[1])
    plt.yscale("log"); plt.xlabel("Day"); plt.ylabel("eta"); plt.legend(fontsize=7); plt.show()
except ImportError:
    pass
