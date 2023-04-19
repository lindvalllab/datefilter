from collections import defaultdict
import csv
import datetime
from dataclasses import dataclass
from typing import Callable, Dict, List, TextIO

from date_info import DateInfo


class ParseFilterException(Exception):
    """
    By throwing this, we alert users that we have already passed on the errors, so no
    further exception handling needs to be done.
    """


@dataclass
class ParsedFilter:
    id_col: str
    date_col: str
    filter_dict: Dict[str, List[DateInfo]]


def parse_filter(input_file: TextIO,
                 date_format: str,
                 append_error: Callable[[str], None]) -> ParsedFilter:
    reader = csv.DictReader(input_file)
    filter_dict = defaultdict(list)

    if reader.fieldnames is None:
        append_error('There appears to be a problem with the filter file. '
                     'Please check that the field names are correct')
        raise ParseFilterException('None field names')
    elif len(reader.fieldnames) != 4:
        append_error('The filter file has an incorrect number of columns. There should be four.')
        raise ParseFilterException('Bad number of columns')
    elif reader.fieldnames[2] != 'days_before' or reader.fieldnames[3] != 'days_after':
        append_error('The third and fourth columns must be\n'
                     'days_before,days_after')
        raise ParseFilterException('days_before,days_after')

    id_col = reader.fieldnames[0]
    date_col = reader.fieldnames[1]

    for row in reader:
        try:
            anchor_date = datetime.datetime.strptime(row[date_col], date_format).date()
        except ValueError:
            append_error(f'The date {row[date_col]} is incorrectly formatted.')
            raise ParseFilterException
        except TypeError:
            append_error(f'The row for patient {row[id_col]} is missing an anchor date')
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

        filter_dict[row[id_col]].append(DateInfo(
            anchor_date=anchor_date,
            days_before=days_before,
            days_after=days_after
        ))
    return ParsedFilter(
        id_col=id_col,
        date_col=date_col,
        filter_dict=filter_dict,
    )
