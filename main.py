import tkinter as tk
from tkinter import ttk


def calculate(event=None):
    try:
        value = float(feet.get())
        meters.set(int(0.3048 * value * 10000.5) / 10000)
    except ValueError:
        pass


root = tk.Tk()
root.title("Date Filter")
content = ttk.Frame(root)
content.grid(column=0, row=0)
frame = ttk.Frame(content, borderwidth=5, relief="ridge", width=400, height=200)
frame.grid(column=0, row=0, columnspan=3, rowspan=5)
data_file_label = ttk.Label(content, text="Data file")
filter_file_label = ttk.Label(content, text="Filter file")
output_file_label = ttk.Label(content, text="Output file")
data_file_button = ttk.Button(content, text="Find")
filter_file_button = ttk.Button(content, text="Find")
output_file_button = ttk.Button(content, text="Find")
confirm_button = ttk.Button(content, text="Filter")

data_file_label.grid(column=0, row=0, columnspan=2)
filter_file_label.grid(column=0, row=1, columnspan=2)
output_file_label.grid(column=0, row=2, columnspan=2)
data_file_button.grid(column=2, row=0)
filter_file_button.grid(column=2, row=1)
output_file_button.grid(column=2, row=2)
confirm_button.grid(column=2, row=3)

# mainframe = ttk.Frame(root, padding="3 3 12 12")
# mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)
# 
# feet = tk.StringVar()
# feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
# feet_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))
# 
# meters = tk.StringVar()
# ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(tk.W, tk.E))
# 
# ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=tk.W)
# 
# ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=tk.W)
# ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=tk.E)
# ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=tk.W)
# 
# for child in mainframe.winfo_children():
#     child.grid_configure(padx=5, pady=5)
# 
# feet_entry.focus()
# root.bind("<Return>", calculate)

root.mainloop()
