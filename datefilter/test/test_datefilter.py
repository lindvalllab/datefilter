import filecmp
import os

import pytest

from datefilter import process
from config import DatefilterConfig


@pytest.mark.parametrize('sample_name,date_format', [
    ('files/full_example_1', '%m/%d/%Y'),
    ('files/full_example_2', '%d %b, %Y'),
    ('files/multiple_ranges_1', '%m/%d/%Y'),
])
def test_process(sample_name: str, date_format: str) -> None:
    errors = []

    def append_error(error: str) -> None:
        errors.append(error)

    prefix = os.path.join(os.path.dirname(__file__), sample_name)
    config = DatefilterConfig(
        date_format=date_format,
        include_missing=False
    )

    process(prefix + '_data.csv',
            prefix + '_filter.csv',
            prefix + '_test_output.csv',
            config,
            append_error)

    assert filecmp.cmp(prefix + '_test_output.csv',
                       prefix + '_expected_output.csv')

    assert len(errors) == 0


def test_process_include_exclude_missing() -> None:
    errors = []

    def append_error(error: str) -> None:
        errors.append(error)

    prefix = os.path.join(os.path.dirname(__file__), 'files/missing_patient')

    include_config = DatefilterConfig(
        date_format='%m/%d/%Y',
        include_missing=True
    )

    process(prefix + '_data.csv',
            prefix + '_filter.csv',
            prefix + '_include_test_output.csv',
            include_config,
            append_error)

    assert len(errors) == 0
    assert filecmp.cmp(prefix + '_include_test_output.csv',
                       prefix + '_include_expected_output.csv')

    exclude_config = DatefilterConfig(
        date_format='%m/%d/%Y',
        include_missing=False
    )
    process(prefix + '_data.csv',
            prefix + '_filter.csv',
            prefix + '_exclude_test_output.csv',
            exclude_config,
            append_error)

    assert len(errors) == 0
    assert filecmp.cmp(prefix + '_exclude_test_output.csv',
                       prefix + '_exclude_expected_output.csv')


@pytest.mark.parametrize('sample_name,date_format', [
    ('files/full_example_1', '%m/%d/%Y'),
    ('files/full_example_2', '%d %b, %Y'),
])
def test_process_windows(sample_name: str, date_format: str) -> None:
    """
    Test handling of windows carriage returns and BOM characters.
    """
    errors = []

    def append_error(error: str) -> None:
        errors.append(error)

    prefix = os.path.join(os.path.dirname(__file__), sample_name)
    config = DatefilterConfig(
        date_format=date_format,
        include_missing=False
    )

    process(prefix + '_data.csv',
            prefix + '_filter_windows.csv',
            prefix + '_test_output.csv',
            config,
            append_error)

    assert filecmp.cmp(prefix + '_test_output.csv',
                       prefix + '_expected_output.csv')

    assert len(errors) == 0
