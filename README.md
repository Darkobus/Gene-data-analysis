# Gene data analysis — GO-term filter for transcriptomics

Finds genes with a given biological function among the significant hits of an RNA-seq
differential-expression experiment, and writes a colour-coded Excel report per comparison.

Built during my molecular biology studies for the OPUS HTT project
(University of Gdańsk, Faculty of Biology, Department of Molecular Biology), where
it replaced manual filtering of DESeq2 tables in Excel.

```
go.xlsx (gene_id, go_term) ──► genes whose GO term contains "chaperone"
                                          │
all_compare.xlsx (DESeq2 export) ─────────┴─► padj < 0.05 per comparison ──► result.xlsx
                                                                              one sheet per comparison,
                                                                              log2FC: blue = up, red = down
```

## Quick start

```bash
pip install -r requirements.txt
python examples/make_example_data.py          # synthetic input files
python gene_filter.py examples/go.xlsx examples/all_compare.xlsx \
    --phrase chaperone --comparisons HEK84_G50vsHEK HEK41vsHEK --out result.xlsx
```

```
8 GO annotations match 'chaperone'
HEK84_G50vsHEK: 2 significant genes
HEK41vsHEK: 4 significant genes
Saved result.xlsx
```

Or with a window: `python main.py` (Tkinter form with the same inputs).

## Input format

- **GO table** — `gene_id`, `go_term`.
- **Comparison table** — DESeq2-style export: for each comparison `<name>` the columns
  `…, <read count A>, <read count B>, <name>_log2FoldChange, <name>_pvalue, <name>_padj`
  in this order, plus optional annotation columns (`gene_name`, `gene_chr`, `gene_start`,
  `gene_end`, `gene_strand`, `gene_length`, `gene_biotype`, `gene_description`, `Family`).

## Files

| File | |
|---|---|
| `gene_filter.py` | filtering and Excel report (CLI) |
| `main.py` | Tkinter front-end |
| `examples/make_example_data.py` | generates synthetic `go.xlsx` / `all_compare.xlsx` |
| `tests/` | pytest: GO matching, padj filter, cell colouring |

## Tests

```bash
pip install -r requirements-dev.txt
pytest -q
```
