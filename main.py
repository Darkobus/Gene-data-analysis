"""Desktop front-end for gene_filter.py (Tkinter)."""
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

import gene_filter


def browse_file(entry):
    filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    entry.delete(0, tk.END)
    entry.insert(0, filename)


def browse_directory(entry):
    directory = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, directory)


def start_process():
    def log(msg):
        log_text.insert(tk.END, msg + "\n")
        log_text.see(tk.END)

    comparisons = [c.strip() for c in entry_columns.get().split(';') if c.strip()]
    try:
        gene_filter.run(
            go_path=entry_file1.get(),
            compare_path=entry_file2.get(),
            phrase=entry_function.get(),
            comparisons=comparisons,
            out_path=Path(entry_dir.get()) / "result.xlsx",
            log=log,
        )
    except Exception as exc:  # show the error in the window instead of a silent thread crash
        log(f"Error: {exc}")


def start_process_threaded():
    threading.Thread(target=start_process).start()


root = tk.Tk()
root.title("Transcryptomic filter")
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(6, weight=1)

label_file1 = tk.Label(root, text="File go.xlsx:")
label_file1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_file1 = tk.Entry(root, width=50)
entry_file1.grid(row=0, column=1, padx=10, pady=10)
browse_file_button1 = tk.Button(root, text="...", command=lambda: browse_file(entry_file1))
browse_file_button1.grid(row=0, column=2, padx=10, pady=10)

label_file2 = tk.Label(root, text="File all_compare.xlsx:")
label_file2.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_file2 = tk.Entry(root, width=50)
entry_file2.grid(row=1, column=1, padx=10, pady=10)
browse_file_button2 = tk.Button(root, text="...", command=lambda: browse_file(entry_file2))
browse_file_button2.grid(row=1, column=2, padx=10, pady=10)

label_function = tk.Label(root, text="Function: (ie. Chaperon)")
label_function.grid(row=2, column=0, padx=10, pady=10, sticky="w")
entry_function = tk.Entry(root, width=50)
entry_function.grid(row=2, column=1, padx=10, pady=10)

label_columns = tk.Label(root, text="Comparisons, ; separated (ie. HEK84_G50vsHEK)")
label_columns.grid(row=3, column=0, padx=10, pady=10, sticky="w")
entry_columns = tk.Entry(root, width=50)
entry_columns.grid(row=3, column=1, padx=10, pady=10)

label_dir = tk.Label(root, text="Saving dir:")
label_dir.grid(row=4, column=0, padx=10, pady=10, sticky="w")
entry_dir = tk.Entry(root, width=50)
entry_dir.grid(row=4, column=1, padx=10, pady=10)
browse_dir_button = tk.Button(root, text="...", command=lambda: browse_directory(entry_dir))
browse_dir_button.grid(row=4, column=2, padx=10, pady=10)

start_button = tk.Button(root, text="Start", command=start_process_threaded)
start_button.grid(row=5, column=0, columnspan=3, pady=20)

log_text = tk.Text(root, height=5, width=70)
log_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

root.mainloop()
