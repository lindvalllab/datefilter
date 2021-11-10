import multiprocessing
from typing import Callable

from filter_data import filter_data
from parse_filter import ParseFilterException, parse_filter
from ui import UserInterface


def process(data_file_path: str,
            filter_file_path: str,
            output_file_path: str,
            include_missing: bool,
            append_error: Callable[[str], None]) -> None:
    try:
        with open(filter_file_path, newline='') as filter_file:
            date_info = parse_filter(filter_file, append_error)
        with open(data_file_path, newline='') as data_file:
            with open(output_file_path, 'w') as output_file:
                filter_data(data_file, output_file, date_info, include_missing, append_error)
    except ParseFilterException:
        pass
    except Exception as e:
        append_error('An unknown error occurred. The following information may be useful.\n'
                     + type(e).__name__ + ': ' + str(e))


if __name__ == '__main__':
    # Required for building on Windows
    # https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Multiprocessing
    multiprocessing.freeze_support()

    ui = UserInterface(process)
    ui.run()
