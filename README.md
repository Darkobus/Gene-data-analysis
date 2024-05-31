\# Gene Data Analysis Tool

This Python script automates the analysis of gene databases stored in
Excel format. It is designed to identify and highlight genes related to
specific biological functions and their expression changes in
transcriptomics data sets. This tool is particularly useful for
researchers working with gene expression data, enabling them to quickly
filter and visually distinguish significant changes. As a student, I
created it to be helpful for myself and my project colleagues.

This program was specifically developed for the OPUS HTT project at the
University of Gdańsk - Faculty of Biology - Department of Molecular
Biology.

\## Features

\- \*\*Search Functionality\*\*: Targets specific phrases within gene
database columns, allowing for focused analysis of genes associated with
desired functions (e.g., autophagy, mitochondria). - \*\*Transcriptomics
Data Correlation\*\*: Correlates gene data with transcriptomics results
to isolate entries with significant expression changes, based on a
p-value threshold (\<0.05). - \*\*Visual Highlights\*\*: Enhances data
readability by coloring cells in the \'change\' column to indicate
positive (red) or negative (blue) changes.

\## How It Works

1\. \*\*Data Loading\*\*: The script reads gene database information and
transcriptomics results from specified Excel files. 2. \*\*Phrase
Searching\*\*: It filters the gene database to find entries containing a
specified phrase related to a biological function. 3. \*\*Data
Correlation\*\*: Filters and correlates these entries with
transcriptomics results, focusing on genes with significant expression
changes. 4. \*\*Visual Highlighting\*\*: Applies color coding to the
\'change\' column in the output Excel file, visually distinguishing
positive and negative changes.

\## Prerequisites

\- Python 3.x - Pandas: For data manipulation and analysis. - Openpyxl:
For reading, writing, and modifying Excel files in XLSX/XLSM/XLTX/XLTM
formats.

\## Installation

1\. Clone the repository: \`\`\`bash git clone
https://github.com/yourusername/genedata-analysis-tool.git cd
genedata-analysis-tool \`\`\`

2\. Install the required Python packages: \`\`\`bash pip install pandas
openpyxl \`\`\`

\## Usage

1\. Place your gene database file (e.g., \`go1.xls.xlsx\`) and
transcriptomics results file (e.g., \`all_compare1.xlsx\`) in the
\`Przekonwertowane\` directory. 2. Open the \`main.py\` script and
configure the following variables as needed:  - \`BASE_GO\`: Path to the
gene database file.  - \`BASE_ALL_COMPARED\`: Path to the
transcriptomics results file.  - \`INTERESTED_FUNCTION\`: The phrase you
are interested in (e.g., \'chaperon\').  - \`COMPARE\`: A list of
columns to compare in the transcriptomics results.

3\. Run the script: \`\`\`bash python main.py \`\`\`

4\. The output will be saved as \`Wyniki.xlsx\` with separate sheets for
each comparison, and a final file named based on the
\`INTERESTED_FUNCTION\` with color-coded changes.

\## Example

Here\'s an example configuration and output process:

1\. \*\*Configuration\*\* in \`main.py\`: \`\`\`python BASE_GO =
\'Przekonwertowane/go1.xls.xlsx\' BASE_ALL_COMPARED =
\'Przekonwertowane/all_compare1.xlsx\' INTERESTED_FUNCTION =
\'chaperon\' COMPARE = \[\'HEK41vsHEK_padj\', \'HEK41_G50vsHEK41_padj\',
\'HEK41_G50vsHEK_padj\', \'HEK84vsHEK_padj\', \'HEK84_G50vsHEK84_padj\',
\'HEK84_G50vsHEK_padj\'\] \`\`\`

2\. \*\*Running the script\*\*: \`\`\`bash python main.py \`\`\`

3\. \*\*Output\*\*:  - \`Wyniki.xlsx\`: Contains sheets for each column
specified in \`COMPARE\`.  - \`chaperon.xlsx\`: Contains color-coded
cells indicating positive (red) and negative (blue) changes.

\## Feedback

This is my first repository, so it may be missing some elements. If you
are willing, please provide feedback!
