Gene Data Analysis Tool

This Python script automates the analysis of gene databases stored in Excel format. It is designed to identify and highlight genes related to specific biological functions and their expression changes in transcriptomics data sets. 
It's particularly useful for researchers working with gene expression data, enabling them to quickly filter and visually distinguish significant changes. As student I made it to be helpful to me and my project colleauges. 

Features

Search Functionality: Targets specific phrases within gene database columns, allowing for the focused analysis of genes associated with desired functions (e.g., autophagy, mitochondria).
Transcriptomics Data Correlation: Correlates gene data with transcriptomics results to isolate entries with significant expression changes, based on a p-value threshold (>0.05).
Visual Highlights: Enhances data readability by coloring cells in the 'change' column to indicate positive (red) or negative (blue) changes.


How It Works

Data Loading: The script reads gene database information and transcriptomics results from specified Excel files.
Phrase Searching: It filters the gene database to find entries containing a specified phrase related to a biological function.
Data Correlation: Filters and correlates these entries with transcriptomics results, focusing on genes with significant expression changes.
Visual Highlighting: Applies color coding to the 'change' column in the output Excel file, visually distinguishing positive and negative changes.


Prerequisites

Python 3.x
Pandas: For data manipulation and analysis.
Openpyxl: For reading, writing, and modifying Excel files in XLSX/XLSM/XLTX/XLTM formats.