import csv
import datetime
from typing import Dict, TextIO
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


def filter_data(input_file: TextIO, output_file: TextIO, date_info: Dict[str, DateInfo]) -> None:
    reader = csv.DictReader(input_file)

    # For the type-checker. The field names shouldn't be None.
    field_names = reader.fieldnames if reader.fieldnames is not None else []
    writer = csv.DictWriter(output_file, field_names)
    writer.writeheader()
    for row in reader:
        if include_row(row, date_info):
            writer.writerow(row)


with open('../rpdr/out.csv') as file:
    with open('new.csv', 'w') as file2:
        filter_data(file, file2, {})
