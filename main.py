from filter_data import filter_data
from parse_filter import parse_filter
from ui import UserInterface


def process(data_file_path: str, filter_file_path: str, output_file_path: str) -> None:
    with open(filter_file_path) as filter_file:
        date_info = parse_filter(filter_file)
    with open(data_file_path) as data_file:
        with open(output_file_path, 'w') as output_file:
            filter_data(data_file, output_file, date_info)


if __name__ == '__main__':
    ui = UserInterface(process)
    ui.run()
