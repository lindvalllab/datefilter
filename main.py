import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class UserInterface:
    def __init__(self):
        # Set up interface
        self.root = tk.Tk()
        self.root.title("Date Filter")
        content = ttk.Frame(self.root)
        content.grid(column=0, row=0)
        frame = ttk.Frame(content, borderwidth=5, relief="ridge", width=600, height=200)
        frame.grid(column=0, row=0, columnspan=3, rowspan=4)
        data_file_label = ttk.Label(content, text="Data file")
        filter_file_label = ttk.Label(content, text="Filter file")
        data_file_button = ttk.Button(content,
                                      text="Select data file",
                                      command=self.get_data_file_name)
        filter_file_button = ttk.Button(content,
                                        text="Select filter file",
                                        command=self.get_filter_file_name)
        confirm_button = ttk.Button(content,
                                    text="Filter",
                                    command=self.process_files)

        data_file_label.grid(column=0, row=0, columnspan=2, sticky=tk.W, padx=10)
        filter_file_label.grid(column=0, row=1, columnspan=2, sticky=tk.W, padx=10)
        data_file_button.grid(column=2, row=0, sticky=tk.E, padx=10)
        filter_file_button.grid(column=2, row=1, sticky=tk.E, padx=10)
        confirm_button.grid(column=2, row=2, sticky=(tk.S, tk.E), padx=10)

        data_file_button.focus()

        self.data_file_name = ''
        self.filter_file_name = ''

    def run(self):
        self.root.mainloop()

    def get_data_file_name(self):
        self.data_file_name = filedialog.askopenfilename(
            filetypes=[("Comma-separated files", "*.csv")]
        )

    def get_filter_file_name(self):
        self.filter_file_name = filedialog.askopenfilename(
            filetypes=[("Comma-separated files", "*.csv")]
        )

    def process_files(self):
        output_file = filedialog.asksaveasfilename()
        print('a', self.data_file_name, 'b', self.filter_file_name, 'c', output_file)

interface = UserInterface()

interface.run()
