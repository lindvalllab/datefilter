import csv
import datetime
from dataclasses import dataclass
from typing import Dict, TextIO


@dataclass
class DateInfo:
    anchor_date: datetime.date
    days_before: datetime.timedelta
    days_after: datetime.timedelta


def parse_filter(input_file: TextIO) -> Dict[str, DateInfo]:
    reader = csv.DictReader(input_file)
    out = {}

    for row in reader:
        out[row['EMPI']] = DateInfo(
            anchor_date=datetime.datetime.strptime(row['anchor_date'], '%m/%d/%Y').date(),
            days_before=datetime.timedelta(int(row['days_before'])),
            days_after=datetime.timedelta(int(row['days_after'])),
        )
    return out
