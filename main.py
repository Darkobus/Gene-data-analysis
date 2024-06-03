Oczywiście, poniżej znajduje się zaktualizowany kod z komunikatami `print` przetłumaczonymi na język angielski:

```python
import os
import pandas as pd
from openpyxl import load_workbook, Workbook
from openpyxl.styles import PatternFill
from pathlib import Path

# Quick Config

BASE_GO = 'path.xlsx'
BASE_ALL_COMPARED = 'path.xlsx'
INTERESTED_FUNCTION = 'chaperon'
COMPARE = ['HEK41vsHEK_padj', 'HEK41_G50vsHEK41_padj','HEK41_G50vsHEK_padj','HEK84vsHEK_padj','HEK84_G50vsHEK84_padj','HEK84_G50vsHEK_padj','HEK53vsHEK_padj', 'HEK453_G50vsHEK53_padj','HEK53_G50vsHEK_padj']

CHUNK_SIZE = 1000

def generate_unique_filename(base_filename):
    """
    Generates a unique filename by appending a numerical suffix if the specified base filename already exists.
    :param base_filename: The base name of the file, including the path and extension.
    :return: A unique filename with a numerical suffix if necessary.
    """
    filename = Path(base_filename)
    counter = 1  # Start counter for suffix
    new_filename = filename  # Initialize with the original name

    # Loop until a unique filename is found
    while new_filename.exists():
        new_filename = filename.with_name(f"{filename.stem}({counter}){filename.suffix}")
        counter += 1

    return new_filename

def process_chunk(chunk, expected_columns):
    """Process each chunk: verify columns and perform further processing."""
    if not set(expected_columns).issubset(chunk.columns):
        raise ValueError("Missing one or more expected columns in the Excel file.")
    # Placeholder for further chunk processing
    print(chunk.head())  # Example action: Print the first few rows

def read_excel_file_in_chunks(file_path, chunk_size):
    try:
        # Attempt to initialize a chunked reader
        reader = pd.read_excel(file_path, chunksize=chunk_size)
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return

    expected_columns = ['gene_id', 'go_term']
    try:
        for chunk in reader:
            process_chunk(chunk, expected_columns)
    except ValueError as e:
        print(e)
        return

def analyze_column(df_go, df_all_compared, col):
    print(f"Analyzing column: {col}")
    filtered_go = df_go[df_go['go_term'].str.contains(INTERESTED_FUNCTION, case=False)]

    count_filtered = filtered_go.shape[0]
    print(f"Number of cells containing the phrase '{INTERESTED_FUNCTION}': {count_filtered}")

    filtered_all_compared = df_all_compared[df_all_compared['gene_id'].isin(filtered_go['gene_id'])]

    condition = filtered_all_compared[col] < 0.05
    filtered_df = filtered_all_compared[condition]

    count_condition = filtered_df.shape[0]
    print(f"Number of results meeting the condition: {count_condition}")

    return filtered_df

def color_columns(workbook, sheet_name, compare_col_index):
    ws = workbook[sheet_name]
    red_fill = PatternFill(start_color='FFFF0000', end_color='FFFF0000', fill_type='solid')
    blue_fill = PatternFill(start_color='FF0000FF', end_color='FF0000FF', fill_type='solid')

    target_col_index = compare_col_index - 2
    for row in range(2, ws.max_row + 1):
        target_cell = ws.cell(row=row, column=target_col_index)
        compare_cell = ws.cell(row=row, column=compare_col_index)

        # Make sure to check if the compare_cell has a value
        if compare_cell.value is not None:
            if compare_cell.value > 0:
                target_cell.fill = red_fill
            elif compare_cell.value < 0:
                target_cell.fill = blue_fill

def main():
    print(f"Loading database {BASE_GO}...")
    cols_to_read = ['gene_id', 'go_term']
    df_go = pd.read_excel(BASE_GO, usecols=cols_to_read)

    print(f"Loading data from {BASE_ALL_COMPARED}...")
    df_all_compared = pd.read_excel(BASE_ALL_COMPARED, engine='openpyxl')
    print("Data loading completed.")

    unique_wyniki = generate_unique_filename("Wyniki.xlsx")
    with pd.ExcelWriter(unique_wyniki, engine='openpyxl') as writer:
        for col in COMPARE:
            filtered_df = analyze_column(df_go, df_all_compared, col)
            filtered_df.to_excel(writer, sheet_name=col, index=False)
    print("All data has been saved to separate sheets.")

    # Load the workbook to apply coloring
    wb = load_workbook(unique_wyniki)
    for col in COMPARE:
        ws = wb[col]
        compare_col_index = ws[1].index([cell for cell in ws[1] if cell.value == col][0]) + 1
        color_columns(wb, col, compare_col_index)

    unique_filename = generate_unique_filename(f'{INTERESTED_FUNCTION}.xlsx')
    print(f"Saving colored '{unique_filename}'...")
    wb.save(unique_filename)
    print("Saving completed. Cheers!")

if __name__ == "__main__":
    main()
```
