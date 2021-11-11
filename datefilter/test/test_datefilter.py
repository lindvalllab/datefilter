import filecmp
import os

import pytest

from datefilter import create_process


@pytest.mark.parametrize('sample_name', [
    'files/full_example_1',
    'files/full_example_2',
])
def test_process(sample_name: str) -> None:
    errors = []

    def append_error(error: str) -> None:
        errors.append(error)

    prefix = os.path.join(os.path.dirname(__file__), sample_name)

    process = create_process('%m/%d/%Y')

    process(prefix + '_data.csv',
            prefix + '_filter.csv',
            prefix + '_test_output.csv',
            append_error)

    assert filecmp.cmp(prefix + '_test_output.csv',
                       prefix + '_expected_output.csv')

    assert len(errors) == 0
