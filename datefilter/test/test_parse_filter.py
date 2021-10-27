import os
import datetime
import pytest
from parse_filter import parse_filter, ParseFilterException


@pytest.mark.parametrize('filter_path', [
    'files/filter_bad_header.csv',
    'files/filter_bad_date.csv',
    'files/filter_bad_before.csv',
    'files/filter_bad_after.csv',
    'files/filter_incomplete_row.csv',
    'files/filter_short_header.csv',
])
def test_parse_bad_filter(filter_path: str) -> None:
    with open(os.path.join(os.path.dirname(__file__), filter_path)) as file:
        errors = []

        def append_error(error: str) -> None:
            errors.append(error)

        with pytest.raises(ParseFilterException):
            parse_filter(file, append_error)

        # These should only present a single error to the user.
        assert len(errors) == 1


def test_parse_good_filter() -> None:
    with open(os.path.join(os.path.dirname(__file__), 'files/filter_good.csv')) as file:
        errors = []

        def append_error(error: str) -> None:
            errors.append(error)

        filter_dict = parse_filter(file, append_error).filter_dict

        assert len(errors) == 0
        assert len(filter_dict) == 3

        assert filter_dict['12'].anchor_date == datetime.date(1970, 1, 1)
        assert filter_dict['12'].days_before == datetime.timedelta(10)
        assert filter_dict['12'].days_after == datetime.timedelta(10)

        assert filter_dict['23'].anchor_date == datetime.date(1980, 1, 1)
        assert filter_dict['23'].days_before == datetime.timedelta(5)
        assert filter_dict['23'].days_after == datetime.timedelta(5)

        assert filter_dict['34'].anchor_date == datetime.date(1990, 5, 20)
        assert filter_dict['34'].days_before == datetime.timedelta(3)
        assert filter_dict['34'].days_after == datetime.timedelta(10)
