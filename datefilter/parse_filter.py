import csv
import datetime
from typing import Callable, Dict, TextIO
from date_info import DateInfo


class ParseFilterException(Exception):
    """
    By throwing this, we alert users that we have already passed on the errors, so no
    further exception handling needs to be done.
    """


def parse_filter(input_file: TextIO, append_error: Callable[[str], None]) -> Dict[str, DateInfo]:
    reader = csv.DictReader(input_file)
    out = {}

    if reader.fieldnames is None:
        append_error('There appears to be a problem with the filter file. '
                     'Please check that the field names are correct')
        raise ParseFilterException('None field names')
    elif set(reader.fieldnames) != {'EMPI', 'anchor_date', 'days_before', 'days_after'}:
        append_error('The filter file has incorrect field names\n"'
                     + ', '.join(reader.fieldnames) + '".\n'
                     'They should be\n"EMPI, anchor_date, days_before, days_after".')
        raise ParseFilterException('Bad field names')

    for row in reader:
        try:
            anchor_date = datetime.datetime.strptime(row['anchor_date'], '%m/%d/%Y').date()
        except ValueError:
            append_error(f'The date {row["anchor_date"]} is incorrectly formatted.')
            raise ParseFilterException
        except TypeError:
            append_error(f'The row for patient {row["EMPI"]} is missing an anchor date')
            raise ParseFilterException
        try:
            days_before = datetime.timedelta(int(row['days_before']))
        except ValueError:
            append_error(f'The row days_before={row["days_before"]} is incorrectly formatted.')
            raise ParseFilterException
        try:
            days_after = datetime.timedelta(int(row['days_after']))
        except ValueError:
            append_error(f'The row days_after={row["days_after"]} is incorrectly formatted.')
            raise ParseFilterException

        out[row['EMPI']] = DateInfo(
            anchor_date=anchor_date,
            days_before=days_before,
            days_after=days_after
        )
    return out
