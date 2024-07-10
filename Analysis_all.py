import pandas as pd
from collections import Counter

#dane
all_compared = pd.read_excel('all_compare3.xlsx')
#all_compared = pd.read_excel('all_comparemice.xls.xlsx')
#go = pd.read_excel('gomice.xls.xlsx')
go = pd.read_excel('go3.xlsx')

columns_to_analyze = [
    #('R61_G50vsR61_padj', 'R61_G50vsR61_log2FoldChange'),
    #('R61_G50vsWT_padj', 'R61_G50vsWT_log2FoldChange'),
    #('R61vsWT_padj', 'R61vsWT_log2FoldChange'),
    #('WT_G50vsWT_padj', 'WT_G50vsWT_log2FoldChange'),
    ('HEK84_G50vsHEK_padj', 'HEK84_G50vsHEK_log2FoldChange'),
    ('HEK84_G50vsHEK84_padj', 'HEK84_G50vsHEK84_log2FoldChange'),
    ('HEK41_G50vsHEK_padj', 'HEK41_G50vsHEK_log2FoldChange'),
    ('HEK41_G50vsHEK41_padj', 'HEK41_G50vsHEK41_log2FoldChange'),
    ('HEK41vsHEK_padj', 'HEK41vsHEK_log2FoldChange'),
    ('HEK84vsHEK_padj', 'HEK84vsHEK_log2FoldChange')
]

extended_keywords = [
    'autophagy', 'lysosome', 'phagophore', 'autophagosome', 'autolysosome', 'macroautophagy',
    'microautophagy', 'chaperone-mediated autophagy', 'mitophagy', 'aggrephagy', 'lipophagy',
    'xenophagy', 'pexophagy', 'reticulophagy', 'ER-phagy', 'ATG5', 'ATG7', 'Beclin1', 'LC3', 'ULK1',
    'p62', 'SQSTM1', 'chaperone', 'Hsp70', 'Hsp90', 'Hsc', 'co-chaperone', 'GroEL', 'GroES', 'DnaK',
    'DnaJ', 'ClpB', 'sHsp', 'protein folding', 'UPR', 'ER stress', 'molecular chaperone',
    'client proteins', 'folding intermediates', 'protein aggregation', 'disaggregation', 'refolding',
    'proteostasis', 'chaperon'
]


def count_occurrences(word, genes):
    return filtered_go[filtered_go['gene_id'].isin(genes) & filtered_go['go_term'].str.contains(word, na=False)].shape[
        0]


all_results = []
all_gene_details = []

for padj_col, log2fc_col in columns_to_analyze:
    filtered_all_compared = all_compared[all_compared[padj_col] < 0.05]

    gene_numbers = filtered_all_compared['gene_id'].tolist()

    filtered_go = go[go['gene_id'].isin(gene_numbers)]

    all_descriptions = ' '.join(filtered_go['go_term'].tolist())

    words = all_descriptions.split()

    word_counts = Counter(words)

    common_words_df = pd.DataFrame(word_counts.items(), columns=['Word', 'Count'])

    filtered_extended_keywords_df = common_words_df[common_words_df['Word'].isin(extended_keywords)].copy()

    positive_genes = filtered_all_compared[filtered_all_compared[log2fc_col] > 0]['gene_id']
    negative_genes = filtered_all_compared[filtered_all_compared[log2fc_col] < 0]['gene_id']

    filtered_extended_keywords_df['Count_Positive'] = [
        count_occurrences(word, positive_genes) for word in filtered_extended_keywords_df['Word']
    ]

    filtered_extended_keywords_df['Count_Negative'] = [
        count_occurrences(word, negative_genes) for word in filtered_extended_keywords_df['Word']
    ]

    filtered_extended_keywords_df['Total_Count'] = (
            filtered_extended_keywords_df['Count_Positive'] + filtered_extended_keywords_df['Count_Negative']
    )

    filtered_extended_keywords_df['Padj_Column'] = padj_col
    filtered_extended_keywords_df['Log2FC_Column'] = log2fc_col

    all_results.append(filtered_extended_keywords_df)

final_results_df = pd.concat(all_results)

with pd.ExcelWriter('wyniki.xlsx') as writer:
    final_results_df.to_excel(writer, sheet_name='Keyword Counts', index=False)

print("Wyniki zapisane do pliku filtered_extended_common_words_with_counts_and_details.xlsx")
