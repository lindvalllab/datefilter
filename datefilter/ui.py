import multiprocessing
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Callable, Optional

from config import DatefilterConfig


class UserInterface:
    def __init__(
        self,
        process_function: Callable[
            [str, str, str, DatefilterConfig, Callable[[str], None]], None
        ],
        config: DatefilterConfig,
        write_config: Callable[[DatefilterConfig], None],
    ):
        """
        process_function: function that performs the filtering
        config: user-specified settings
        write_config: function to save settings to disk
        """
        self.process_function = process_function
        self.config = config
        self.write_config = write_config

        self.root = tk.Tk()
        self.root.title("Date Filter")

        # Important variables
        self.data_file_var = tk.StringVar(value='')
        self.filter_file_var = tk.StringVar(value='')
        self.include_missing_var = tk.BooleanVar(value=self.config.include_missing)
        self.date_format_var = tk.StringVar(value=self.config.date_format)

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
        self.data_file_button = ttk.Button(
            content,
            text="Select data file",
            command=self.open_file_name_to_var(self.data_file_var))
        self.filter_file_button = ttk.Button(
            content,
            text="Select filter file",
            command=self.open_file_name_to_var(self.filter_file_var))
        self.settings_button = ttk.Button(
            content,
            text="Settings...",
            command=self.create_settings_window)
        self.confirm_button = ttk.Button(
            content,
            text="Filter",
            command=self.process_files)

        data_file_label.grid(column=0, row=0, sticky='ew', padx=10, pady=10)
        filter_file_label.grid(column=0, row=1, sticky='ew', padx=10, pady=10)
        self.data_file_button.grid(column=1, row=0, sticky='e', padx=10, pady=10)
        self.filter_file_button.grid(column=1, row=1, sticky='e', padx=10, pady=10)
        self.settings_button.grid(column=0, row=2, sticky='sw', padx=10, pady=10)
        self.confirm_button.grid(column=1, row=2, sticky='sew', padx=10, pady=10)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        content.columnconfigure(0, weight=1)
        content.columnconfigure(1, weight=0)
        content.rowconfigure(0, weight=1)
        content.rowconfigure(1, weight=1)
        content.rowconfigure(2, weight=1)

        self.data_file_button.focus()

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
                self.data_file_button['state'] = tk.DISABLED
                self.filter_file_button['state'] = tk.DISABLED
                self.confirm_button['state'] = tk.DISABLED
                errors: multiprocessing.Queue[str] = multiprocessing.Queue()

                thread = multiprocessing.Process(
                    target=self.process_function,
                    args=(self.data_file_var.get(),
                          self.filter_file_var.get(),
                          output_file,
                          self.config,
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

                    self.data_file_button['state'] = tk.NORMAL
                    self.filter_file_button['state'] = tk.NORMAL
                    self.confirm_button['state'] = tk.NORMAL

                create_loading_window(self.root, thread, on_finish)

    def create_settings_window(self) -> None:
        settings_window = tk.Toplevel(self.root)
        settings_window.title('Settings')
        if sys.platform.startswith('linux'):
            settings_window.attributes('-type', 'dialog')

        self.update_settings_vars()

        def destroy_window() -> None:
            # The traces in the variables need to be reset each time the window opens
            for trace in self.date_format_var.trace_info():
                for trace_type in trace[0]:
                    self.date_format_var.trace_remove(trace_type, trace[1])
            for trace in self.include_missing_var.trace_info():
                for trace_type in trace[0]:
                    self.include_missing_var.trace_remove(trace_type, trace[1])
            settings_window.destroy()

        include_missing_check = ttk.Checkbutton(
            settings_window,
            text="Include entries missing from filter file",
            variable=self.include_missing_var)
        date_format_label = ttk.Label(settings_window, text='Date format:')
        date_format_text = ttk.Entry(
            settings_window,
            textvariable=self.date_format_var,
        )
        set_default_button = ttk.Button(settings_window,
                                        text='Restore defaults',
                                        command=self.reset_settings)
        cancel_button = ttk.Button(settings_window,
                                   text='Close',
                                   command=destroy_window)
        apply_button = ttk.Button(settings_window,
                                  text='Apply',
                                  command=self.apply_settings,
                                  state=tk.DISABLED)

        def check_settings_change(x: str, y: str, z: str) -> None:
            if self.config.date_format != self.date_format_var.get() or\
                    self.config.include_missing != self.include_missing_var.get():
                apply_button['state'] = tk.NORMAL
            else:
                apply_button['state'] = tk.DISABLED

        self.date_format_var.trace_add('write', check_settings_change)
        self.include_missing_var.trace_add('write', check_settings_change)

        include_missing_check.grid(row=0, column=0, sticky='nw', columnspan=3, padx=10, pady=10)
        date_format_label.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        date_format_text.grid(row=1, column=1, sticky='w', padx=10, pady=10, columnspan=2)
        set_default_button.grid(row=2, column=0, sticky='sw', padx=10, pady=10)
        cancel_button.grid(row=2, column=1, sticky='se', padx=10, pady=10)
        apply_button.grid(row=2, column=2, sticky='se', padx=10, pady=10)
        settings_window.columnconfigure(0, weight=0)
        settings_window.columnconfigure(1, weight=1)
        settings_window.columnconfigure(2, weight=1)
        settings_window.rowconfigure(0, weight=1)
        settings_window.rowconfigure(1, weight=1)
        settings_window.rowconfigure(2, weight=1)

    def reset_settings(self) -> None:
        self.update_settings_vars(DatefilterConfig())

    def update_settings_vars(self, config: Optional[DatefilterConfig] = None) -> None:
        if config is None:
            config = self.config
        self.include_missing_var.set(config.include_missing)
        self.date_format_var.set(config.date_format)

    def apply_settings(self) -> None:
        self.config.include_missing = self.include_missing_var.get()
        self.config.date_format = self.date_format_var.get()
        self.write_config(self.config)


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
