import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from typing import Callable


class UserInterface:
    def __init__(self, process_function: Callable[[str, str, str], None]):
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
        content.grid(column=0, row=0, sticky='nsew')
        frame = ttk.Frame(content, borderwidth=5, relief="ridge")
        frame.grid(column=0, row=0, columnspan=2, rowspan=4, sticky='nsew')

        data_file_label = ttk.Entry(content,
                                    textvariable=self.data_file_var,
                                    state='readonly',
                                    font=('default', 10),
                                    width=40)
        filter_file_label = ttk.Entry(content,
                                      textvariable=self.filter_file_var,
                                      state='readonly',
                                      font=('default', 10),
                                      width=40)
        data_file_button = ttk.Button(content,
                                      text="Select data file",
                                      command=self.open_file_name_to_var(self.data_file_var))
        filter_file_button = ttk.Button(content,
                                        text="Select filter file",
                                        command=self.open_file_name_to_var(self.filter_file_var))
        confirm_button = ttk.Button(content,
                                    text="Filter",
                                    command=self.process_files)

        data_file_label.grid(column=0, row=0, sticky='ew', padx=10, pady=10)
        filter_file_label.grid(column=0, row=1, sticky='ew', padx=10, pady=10)
        data_file_button.grid(column=1, row=0, sticky='e', padx=10, pady=10)
        filter_file_button.grid(column=1, row=1, sticky='e', padx=10, pady=10)
        confirm_button.grid(column=1, row=2, sticky='sew', padx=10, pady=10)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=0)
        content.rowconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)
        content.rowconfigure(2, weight=1)

        data_file_button.focus()

    def run(self) -> None:
        self.root.mainloop()

    @staticmethod
    def open_file_name_to_var(var: tk.StringVar) -> Callable[[], None]:
        def get_file_name() -> None:
            filename = filedialog.askopenfilename(
                filetypes=[("Comma-separated files", "*.csv")]
            )
            if len(filename) > 0:
                var.set(filename)
        return get_file_name

    def process_files(self) -> None:
        if self.data_file_var.get() == '':
            messagebox.showinfo('No data file selected.', message='Please select a data file')
        elif self.filter_file_var.get() == '':
            messagebox.showinfo('No filter file selected.', message='Please select a filter file')
        else:
            output_file = filedialog.asksaveasfilename(
                filetypes=[("Comma-separated files", "*.csv")],
                defaultextension=".csv"
            )
            if output_file != '':
                loading_window = create_loading_window(self.root)
                self.process_function(
                    self.data_file_var.get(), self.filter_file_var.get(), output_file
                )
                loading_window.destroy()
                messagebox.showinfo('Done!', message='Finished processing files.')
                self.data_file_var.set('')
                self.filter_file_var.set('')


def create_loading_window(root: tk.Tk) -> tk.Toplevel:
    loading_window = tk.Toplevel(root)
    loading_window.attributes('-type', 'dialog')
    return loading_window
