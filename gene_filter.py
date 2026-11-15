"""Filter DESeq2-style transcriptomics results by a GO-term phrase.

Steps:
1. pick genes whose GO annotation contains a phrase (e.g. "autophagy", "chaperone");
2. for each comparison, keep those genes with padj < 0.05;
3. write one Excel sheet per comparison, with log2FoldChange coloured
   (blue = up, red = down).

Usage:
    python gene_filter.py go.xlsx all_compare.xlsx --phrase chaperone \
        --comparisons HEK84_G50vsHEK HEK41vsHEK --out result.xlsx
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from openpyxl.styles import Alignment, Border, PatternFill, Side
from openpyxl.utils import get_column_letter

PADJ_THRESHOLD = 0.05
UP_FILL = PatternFill(start_color="ADD8E6", end_color="ADD8E6", fill_type="solid")
DOWN_FILL = PatternFill(start_color="FF6347", end_color="FF6347", fill_type="solid")
HEADER_FILL = PatternFill(start_color="FFFFE0", end_color="FFFFE0", fill_type="solid")
HEADER_BORDER = Border(bottom=Side(style="thin", color="C2B280"))
ANNOTATION_COLUMNS = [
    "gene_name", "gene_chr", "gene_start", "gene_end", "gene_strand",
    "gene_length", "gene_biotype", "gene_description", "Family",
]
COLUMN_WIDTHS = {
    "gene_id": 20, "gene_name": 15, "gene_chr": 10, "gene_start": 15, "gene_end": 10,
    "gene_strand": 15, "gene_length": 15, "gene_biotype": 20, "gene_description": 30,
    "Family": 10, "go_term": 30,
}


def genes_with_go_phrase(go: pd.DataFrame, phrase: str) -> pd.DataFrame:
    """Rows of the GO table whose go_term contains the phrase (case-insensitive)."""
    go = go[["gene_id", "go_term"]].copy()
    go["go_term"] = go["go_term"].astype(str)
    return go[go["go_term"].str.contains(phrase, case=False, na=False, regex=False)]


def comparison_table(compare: pd.DataFrame, go_hits: pd.DataFrame, comparison: str,
                     padj_threshold: float = PADJ_THRESHOLD) -> pd.DataFrame:
    """Significant GO-matching genes for one comparison.

    Columns are taken by position around ``<comparison>_log2FoldChange``, as in DESeq2
    exports: two read-count columns before it, pvalue and padj after it.
    """
    lfc = f"{comparison}_log2FoldChange"
    if lfc not in compare.columns:
        raise KeyError(f"column {lfc!r} not found in comparison table")
    i = compare.columns.get_loc(lfc)
    cols = compare.columns
    before = [cols[j] for j in (i - 2, i - 1) if j >= 1]
    after = [cols[j] for j in (i + 1, i + 2) if j < len(cols)]
    padj = after[1] if len(after) == 2 else None

    table = compare[compare["gene_id"].isin(go_hits["gene_id"])]
    table = table.merge(go_hits, on="gene_id", how="left")
    if padj is not None:
        table = table[table[padj] < padj_threshold]
    keep = ["gene_id", *before, lfc, *after,
            *[c for c in ANNOTATION_COLUMNS if c in table.columns], "go_term"]
    return table[keep].reset_index(drop=True)


def _style_sheet(ws, table: pd.DataFrame, lfc: str) -> None:
    lfc_col = table.columns.get_loc(lfc) + 1
    for r, value in enumerate(table[lfc], start=2):
        if value > 0:
            ws.cell(row=r, column=lfc_col).fill = UP_FILL
        elif value < 0:
            ws.cell(row=r, column=lfc_col).fill = DOWN_FILL
    for row in ws.iter_rows(min_row=1, max_row=len(table) + 1, max_col=len(table.columns)):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True)
    for c, name in enumerate(table.columns, start=1):
        ws.cell(row=1, column=c).fill = HEADER_FILL
        ws.cell(row=1, column=c).border = HEADER_BORDER
        width = COLUMN_WIDTHS.get(name, 33 if name == lfc else 24)
        ws.column_dimensions[get_column_letter(c)].width = width


def run(go_path, compare_path, phrase, comparisons, out_path, log=print) -> Path:
    go = pd.read_excel(go_path, usecols=["gene_id", "go_term"])
    compare = pd.read_excel(compare_path)
    hits = genes_with_go_phrase(go, phrase)
    log(f"{len(hits)} GO annotations match '{phrase}'")
    out_path = Path(out_path)
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        for comparison in comparisons:
            table = comparison_table(compare, hits, comparison)
            sheet = comparison[:31]
            table.to_excel(writer, index=False, sheet_name=sheet)
            _style_sheet(writer.sheets[sheet], table, f"{comparison}_log2FoldChange")
            log(f"{comparison}: {len(table)} significant genes")
    log(f"Saved {out_path}")
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description="Filter transcriptomics results by GO-term phrase")
    ap.add_argument("go", help="GO annotation table (.xlsx with gene_id, go_term)")
    ap.add_argument("compare", help="comparison table (.xlsx, DESeq2-style columns)")
    ap.add_argument("--phrase", required=True, help="GO-term phrase, e.g. chaperone")
    ap.add_argument("--comparisons", nargs="+", required=True, help="e.g. HEK84_G50vsHEK")
    ap.add_argument("--out", default="result.xlsx")
    args = ap.parse_args()
    run(args.go, args.compare, args.phrase, args.comparisons, args.out)


if __name__ == "__main__":
    main()
