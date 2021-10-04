import csv
import datetime
from typing import Callable, Dict, TextIO
from parse_filter import DateInfo


def include_row(row: Dict[str, str], date_info: Dict[str, DateInfo]) -> bool:
    if row['EMPI'] not in date_info:
        return True
    patient_date_info = date_info[row['EMPI']]
    first_date = patient_date_info.anchor_date - patient_date_info.days_before
    last_date = patient_date_info.anchor_date + patient_date_info.days_after
    stripped_date = row['Report_Date_Time'].split()[0]
    row_date = datetime.datetime.strptime(stripped_date, '%m/%d/%Y').date()
    return first_date <= row_date <= last_date


def filter_data(input_file: TextIO,
                output_file: TextIO,
                date_info: Dict[str, DateInfo],
                append_error: Callable[[str], None]) -> None:
    reader = csv.DictReader(input_file)

    # For the type-checker. The field names shouldn't be None.
    field_names = reader.fieldnames if reader.fieldnames is not None else []
    if 'EMPI' not in field_names:
        append_error('The data file is missing an EMPI column.')
        return
    if 'Report_Date_Time' not in field_names:
        append_error('The data file is missing a Report_Date_Time column.')
        return

    writer = csv.DictWriter(output_file, field_names)
    writer.writeheader()
    for row in reader:
        if row['EMPI'] is None or row['Report_Date_Time'] is None:
            append_error('Some rows are incomplete.')
            return
        try:
            if include_row(row, date_info):
                writer.writerow(row)
        except ValueError:
            append_error('The date ' + row['Report_Date_Time'] + ' is not of the '
                         'form month/day/year.')
            return
