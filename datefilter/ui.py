import multiprocessing
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Callable


class UserInterface:
    def __init__(self, process_function: Callable[[str, str, str, Callable[[str], None]], None]):
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
                errors: multiprocessing.Queue[str] = multiprocessing.Queue()

                thread = multiprocessing.Process(
                    target=self.process_function,
                    args=(self.data_file_var.get(),
                          self.filter_file_var.get(),
                          output_file,
                          errors.put)
                )
                thread.start()

                def on_finish() -> None:
                    if (errors.empty()):
                        messagebox.showinfo('Done!', message='Finished processing files.')
                        self.data_file_var.set('')
                        self.filter_file_var.set('')
                    else:
                        error_list = []
                        while not errors.empty():
                            error_list.append(errors.get())
                        messagebox.showerror('A problem occurred', message='\n\n'.join(error_list))

                create_loading_window(self.root, thread, on_finish)


def create_loading_window(root: tk.Tk,
                          thread: multiprocessing.Process,
                          on_finish: Callable[[], None]) -> None:
    loading_window = tk.Toplevel(root)
    if sys.platform.startswith('linux'):
        loading_window.attributes('-type', 'dialog')
    elif sys.platform.startswith('windows'):
        loading_window.attributes('-toolwindow', True)
    loading_window.title('Processing')
    progress = ttk.Progressbar(loading_window, orient='horizontal', mode='indeterminate')
    progress.pack()
    progress.start(10)

    def check_if_running() -> None:
        if thread.is_alive():
            loading_window.after(10, check_if_running)
        else:
            loading_window.destroy()
            on_finish()

    loading_window.after(50, check_if_running)
    loading_window.mainloop()
