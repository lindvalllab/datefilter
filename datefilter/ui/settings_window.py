import sys
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

import _version
from config import DatefilterConfig


class SettingsWindow:
    def __init__(self,
                 config: DatefilterConfig,
                 write_config: Callable[[DatefilterConfig], None],
                 root: tk.Tk):
        self.config = config
        self.write_config = write_config
        self.include_missing_var = tk.BooleanVar(value=self.config.include_missing)
        self.date_format_var = tk.StringVar(value=self.config.date_format)

        self.window = tk.Toplevel(root)
        self.window.title('Settings')
        self.window.withdraw()  # invisible at start

        if sys.platform.startswith('linux'):
            self.window.attributes('-type', 'dialog')

        title_label = ttk.Label(self.window,
                                text=f'Date Filter v{_version.__version__}',
                                font=('default', 10, 'bold'))

        include_missing_check = ttk.Checkbutton(
            self.window,
            text='Include entries missing from filter file',
            variable=self.include_missing_var,
        )
        date_format_label = ttk.Label(self.window, text='Date format:')
        date_format_text = ttk.Entry(
            self.window,
            textvariable=self.date_format_var
        )
        set_default_button = ttk.Button(self.window,
                                        text='Restore defaults',
                                        command=self.reset_settings)
        cancel_button = ttk.Button(self.window,
                                   text='Close',
                                   command=self.window.withdraw)
        self.apply_button = ttk.Button(self.window,
                                       text='Apply',
                                       command=self.apply_settings,
                                       state=tk.DISABLED)

        title_label.grid(row=0, column=0, sticky='n', columnspan=3, padx=10, pady=10)
        include_missing_check.grid(row=1, column=0, sticky='nw', columnspan=3, padx=10, pady=10)
        date_format_label.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        date_format_text.grid(row=2, column=1, sticky='w', padx=10, pady=10, columnspan=2)
        set_default_button.grid(row=3, column=0, sticky='sw', padx=10, pady=10)
        cancel_button.grid(row=3, column=1, sticky='se', padx=10, pady=10)
        self.apply_button.grid(row=3, column=2, sticky='se', padx=10, pady=10)
        self.window.columnconfigure(0, weight=0)
        self.window.columnconfigure(1, weight=1)
        self.window.columnconfigure(2, weight=1)
        self.window.rowconfigure(0, weight=0)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
        self.window.rowconfigure(3, weight=1)

        self.date_format_var.trace_add('write', self.check_settings_change)
        self.include_missing_var.trace_add('write', self.check_settings_change)

    def apply_settings(self) -> None:
        self.config.include_missing = self.include_missing_var.get()
        self.config.date_format = self.date_format_var.get()
        self.write_config(self.config)
        self.check_settings_change()

    def check_settings_change(self, *args: str) -> None:
        if self.config.date_format != self.date_format_var.get() or\
                self.config.include_missing != self.include_missing_var.get():
            self.apply_button['state'] = tk.NORMAL
        else:
            self.apply_button['state'] = tk.DISABLED

    def update_settings_vars(self, config: Optional[DatefilterConfig] = None) -> None:
        if config is None:
            config = self.config
        self.include_missing_var.set(config.include_missing)
        self.date_format_var.set(config.date_format)

    def reset_settings(self) -> None:
        self.update_settings_vars(DatefilterConfig())

    def show(self) -> None:
        self.window.deiconify()
