import os
import pytest
from ..parse_filter import parse_filter, ParseFilterException


@pytest.mark.parametrize('filter_path', [
    'files/filter_bad_header.csv',
    'files/filter_bad_date.csv',
    'files/filter_bad_before.csv',
    'files/filter_bad_after.csv',
    'files/filter_incomplete_row.csv',
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

        assert len(parse_filter(file, append_error)) == 3

        assert len(errors) == 0
