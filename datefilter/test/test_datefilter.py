import datetime
import filecmp
import os

import pytest

from datefilter import process


@pytest.mark.parametrize('sample_name', [
    'files/full_example',
])
def test_process(sample_name: str) -> None:
    errors = []

    def append_error(error: str) -> None:
        errors.append(error)

    process(sample_name + '_data.csv',
            sample_name + '_filter.csv',
            sample_name + '_test_output.csv',
            append_error)

    assert filecmp.cmp(sample_name + '_test_output.csv',
                       sample_name + '_expected_output.csv')

    # with open(sample_name + '_expected_output.csv') as expected_output:
    #     with open(sample_name + '_test_output.csv') as test_output:
    #         assert filecmp.cmp(test_output, expected_output)
