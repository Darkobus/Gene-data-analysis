import pandas as pd
from openpyxl import load_workbook

import gene_filter as gf


def _compare():
    return pd.DataFrame({
        "gene_id": ["g1", "g2", "g3", "g4"],
        "X_count_a": [10, 20, 30, 40],
        "X_count_b": [11, 21, 31, 41],
        "X_log2FoldChange": [1.5, -2.0, 0.7, 3.0],
        "X_pvalue": [0.001, 0.002, 0.2, 0.001],
        "X_padj": [0.01, 0.03, 0.4, 0.02],
        "gene_name": ["A", "B", "C", "D"],
    })


def test_go_phrase_is_case_insensitive_and_literal():
    go = pd.DataFrame({"gene_id": ["g1", "g2", "g3"],
                       "go_term": ["Chaperone binding", "autophagy", "chaperone (HSP70)"]})
    hits = gf.genes_with_go_phrase(go, "chaperone")
    assert list(hits["gene_id"]) == ["g1", "g3"]
    assert list(gf.genes_with_go_phrase(go, "(HSP70)")["gene_id"]) == ["g3"]


def test_comparison_table_filters_go_and_padj():
    hits = pd.DataFrame({"gene_id": ["g1", "g2", "g3"], "go_term": ["t"] * 3})
    table = gf.comparison_table(_compare(), hits, "X")
    assert list(table["gene_id"]) == ["g1", "g2"]  # g3 has padj 0.4, g4 not in GO hits
    assert list(table.columns[:6]) == ["gene_id", "X_count_a", "X_count_b",
                                       "X_log2FoldChange", "X_pvalue", "X_padj"]


def test_run_writes_coloured_sheet(tmp_path):
    go = pd.DataFrame({"gene_id": ["g1", "g2", "g4"], "go_term": ["chaperone"] * 3})
    go.to_excel(tmp_path / "go.xlsx", index=False)
    _compare().to_excel(tmp_path / "cmp.xlsx", index=False)
    out = gf.run(tmp_path / "go.xlsx", tmp_path / "cmp.xlsx", "chaperone", ["X"],
                 tmp_path / "out.xlsx", log=lambda _: None)
    ws = load_workbook(out)["X"]
    fills = [ws.cell(row=r, column=4).fill.start_color.rgb[-6:] for r in range(2, 5)]
    assert fills == ["ADD8E6", "FF6347", "ADD8E6"]  # up, down, up
