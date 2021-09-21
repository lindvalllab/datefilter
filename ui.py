import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


class UserInterface:
    def __init__(self, process_function):
        """
        process_function: function of the three filenames that performs the filtering
        """
        self.process_function = process_function

        self.root = tk.Tk()
        self.root.title("Date Filter")

        # Important variables
        self.data_file_var = tk.StringVar(value='')
        self.filter_file_var = tk.StringVar(value='')

        # Set up interface
        content = ttk.Frame(self.root)
        content.grid(column=0, row=0)
        frame = ttk.Frame(content, borderwidth=5, relief="ridge", width=600, height=200)
        frame.grid(column=0, row=0, columnspan=3, rowspan=4)

        data_file_label = ttk.Label(content, textvariable=self.data_file_var)
        filter_file_label = ttk.Label(content, textvariable=self.filter_file_var)
        data_file_button = ttk.Button(content,
                                      text="Select data file",
                                      command=self.open_file_name_to_var(self.data_file_var))
        filter_file_button = ttk.Button(content,
                                        text="Select filter file",
                                        command=self.open_file_name_to_var(self.filter_file_var))
        confirm_button = ttk.Button(content,
                                    text="Filter",
                                    command=self.process_files)

        data_file_label.grid(column=0, row=0, columnspan=2, sticky=tk.W, padx=10)
        filter_file_label.grid(column=0, row=1, columnspan=2, sticky=tk.W, padx=10)
        data_file_button.grid(column=2, row=0, sticky=tk.E, padx=10)
        filter_file_button.grid(column=2, row=1, sticky=tk.E, padx=10)
        confirm_button.grid(column=2, row=2, sticky=(tk.S, tk.E), padx=10)

        data_file_button.focus()

    def run(self):
        self.root.mainloop()

    @staticmethod
    def open_file_name_to_var(var):
        def get_file_name():
            filename = filedialog.askopenfilename(
                filetypes=[("Comma-separated files", "*.csv")]
            )
            if len(filename) > 0:
                var.set(filename)
        return get_file_name

    def get_data_file_name(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Comma-separated files", "*.csv")]
        )
        if len(filename) > 0:
            self.data_file_var.set(filename)

    def get_filter_file_name(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Comma-separated files", "*.csv")]
        )
        if len(filename) > 0:
            self.filter_file_var.set(filedialog.askopenfilename(
                filetypes=[("Comma-separated files", "*.csv")]
            ))

    def process_files(self):
        output_file = filedialog.asksaveasfilename(
            filetypes=[("Comma-separated files", "*.csv")],
            defaultextension=".csv"
        )
        self.process_function(self.data_file_var.get(), self.filter_file_var.get(), output_file)
