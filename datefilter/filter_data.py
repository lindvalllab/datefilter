import csv
import datetime
import os
from typing import Callable, Dict, TextIO

from parse_filter import ParsedFilter


def include_row(row: Dict[str, str],
                date_format: str,
                parsed_filter: ParsedFilter,
                include_missing: bool) -> bool:
    if row[parsed_filter.id_col] not in parsed_filter.filter_dict:
        return include_missing
    patient_date_info = parsed_filter.filter_dict[row[parsed_filter.id_col]]
    first_last_dates = [
        (info.anchor_date - info.days_before, info.anchor_date + info.days_after)
         for info in patient_date_info
    ]
    date_col = row[parsed_filter.date_col]  # .split()[0]
    try:
        row_date = datetime.datetime.strptime(date_col, date_format).date()
    except ValueError as e:
        # Check if the start of the string can be parsed.
        # https://stackoverflow.com/questions/5045210/
        if len(e.args) > 0 and e.args[0].startswith('unconverted data remains: '):
            extra_length = len(e.args[0]) - len('unconverted data remains: ')
            date_text = date_col[:-extra_length]
            row_date = datetime.datetime.strptime(date_text, date_format).date()
        else:
            raise
    return any(
        first_date <= row_date <= last_date for (first_date, last_date) in first_last_dates
    )


def filter_data(input_file: TextIO,
                output_file: TextIO,
                date_format: str,
                parsed_filter: ParsedFilter,
                include_missing: bool,
                append_error: Callable[[str], None]) -> None:
    # Allow very large field sizes in the csv.
    # https://stackoverflow.com/questions/15063936
    csv.field_size_limit(2147483647)

    reader = csv.DictReader(input_file)

    # For the type-checker. The field names shouldn't be None.
    field_names = reader.fieldnames if reader.fieldnames is not None else []
    if parsed_filter.id_col not in field_names:
        append_error(f'The column {parsed_filter.id_col} does not occur in the data file.')
        return
    if parsed_filter.date_col not in field_names:
        append_error(f'The column {parsed_filter.date_col} does not occur in the data file.')
        return

    writer = csv.DictWriter(output_file, field_names, lineterminator=os.linesep)
    writer.writeheader()
    for row in reader:
        if row[parsed_filter.id_col] is None or row[parsed_filter.date_col] is None:
            append_error('Some rows are incomplete.')
            return
        try:
            if include_row(row, date_format, parsed_filter, include_missing):
                writer.writerow(row)
        except ValueError:
            append_error(
                f'The date {row[parsed_filter.date_col]} is not of the form {date_format}.'
            )
            return
