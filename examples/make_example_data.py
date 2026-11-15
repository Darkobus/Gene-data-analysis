"""Generate small synthetic input files (not real experimental data)."""
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(0)
out = Path(__file__).parent
n = 40
genes = [f"ENSG{i:011d}" for i in range(1, n + 1)]
terms = ["protein folding; chaperone binding", "macroautophagy; autophagosome assembly",
         "mitochondrial respiratory chain", "mRNA splicing", "heat shock protein binding"]

go = pd.DataFrame({"gene_id": genes, "go_term": [terms[i % len(terms)] for i in range(n)]})

compare = pd.DataFrame({"gene_id": genes})
for cmp in ["HEK84_G50vsHEK", "HEK41vsHEK"]:
    compare[f"{cmp}_readcount_a"] = rng.integers(50, 5000, n)
    compare[f"{cmp}_readcount_b"] = rng.integers(50, 5000, n)
    compare[f"{cmp}_log2FoldChange"] = rng.normal(0, 1.5, n).round(3)
    compare[f"{cmp}_pvalue"] = rng.uniform(0, 0.1, n).round(4)
    compare[f"{cmp}_padj"] = (compare[f"{cmp}_pvalue"] * 1.5).clip(upper=1).round(4)
compare["gene_name"] = [f"GENE{i}" for i in range(1, n + 1)]
compare["gene_chr"] = rng.integers(1, 23, n)
compare["gene_start"] = rng.integers(1_000_000, 90_000_000, n)
compare["gene_end"] = compare["gene_start"] + rng.integers(1_000, 50_000, n)
compare["gene_strand"] = rng.choice(["+", "-"], n)
compare["gene_length"] = compare["gene_end"] - compare["gene_start"]
compare["gene_biotype"] = "protein_coding"
compare["gene_description"] = "synthetic gene"
compare["Family"] = rng.choice(["HSP", "ATG", "NDUF", "SRSF"], n)

go.to_excel(out / "go.xlsx", index=False)
compare.to_excel(out / "all_compare.xlsx", index=False)
print("Wrote examples/go.xlsx and examples/all_compare.xlsx")
