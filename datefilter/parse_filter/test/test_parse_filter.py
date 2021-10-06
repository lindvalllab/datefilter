import os
import pytest
from ..parse_filter import parse_filter, ParseFilterException


@pytest.mark.parametrize('filter_path', [
    'files/filter_bad_header.csv',
    'files/filter_bad_date.csv'
])
def test_parse_filter_bad_empi(filter_path: str) -> None:
    with open(os.path.join(os.path.dirname(__file__), filter_path)) as file:
        errors = []

        def append_error(error: str) -> None:
            errors.append(error)

        with pytest.raises(ParseFilterException):
            parse_filter(file, append_error)

        assert len(errors) > 0
