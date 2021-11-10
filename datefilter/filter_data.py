import csv
import datetime
import os
from typing import Callable, Dict, TextIO

from parse_filter import ParsedFilter


def include_row(row: Dict[str, str], parsed_filter: ParsedFilter, include_missing: bool) -> bool:
    if row[parsed_filter.id_col] not in parsed_filter.filter_dict:
        return include_missing
    patient_date_info = parsed_filter.filter_dict[row[parsed_filter.id_col]]
    first_date = patient_date_info.anchor_date - patient_date_info.days_before
    last_date = patient_date_info.anchor_date + patient_date_info.days_after
    stripped_date = row[parsed_filter.date_col].split()[0]
    row_date = datetime.datetime.strptime(stripped_date, '%m/%d/%Y').date()
    return first_date <= row_date <= last_date


def filter_data(input_file: TextIO,
                output_file: TextIO,
                parsed_filter: ParsedFilter,
                include_missing: bool,
                append_error: Callable[[str], None]) -> None:
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
            if include_row(row, parsed_filter, include_missing):
                writer.writerow(row)
        except ValueError:
            append_error(f'The date {row[parsed_filter.date_col]} is not'
                         'of the form month/day/year.')
            return
