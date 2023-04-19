import datetime

from date_info import DateInfo
from filter_data import include_row
from parse_filter import ParsedFilter


def test_include_row_true() -> None:
    row = {
        'EMPI': '12',
        'Report_Date_Time': '05/01/2010',
        'Report_Text': 'Lorem Ipsum'
    }
    date_info = {
        '12': [DateInfo(datetime.date(2010, 5, 3), datetime.timedelta(2), datetime.timedelta(0))]
    }
    parsed_filter = ParsedFilter(
        id_col='EMPI',
        date_col='Report_Date_Time',
        filter_dict=date_info,
    )
    assert include_row(row, '%m/%d/%Y', parsed_filter, False)


def test_include_row_false() -> None:
    row = {
        'EMPI': '12',
        'Report_Date_Time': '04/30/2010',
        'Report_Text': 'Lorem Ipsum'
    }
    date_info = {
        '12': [DateInfo(datetime.date(2010, 5, 3), datetime.timedelta(2), datetime.timedelta(0))]
    }
    parsed_filter = ParsedFilter(
        id_col='EMPI',
        date_col='Report_Date_Time',
        filter_dict=date_info,
    )
    assert not include_row(row, '%m/%d/%Y', parsed_filter, False)


def test_include_row_negative_before() -> None:
    included_row = {
        'MRN': '12',
        'Date_Time': '05/01/2010',
        'Report_Text': 'Lorem Ipsum'
    }
    too_early_row = {
        'MRN': '12',
        'Date_Time': '04/30/2010',
        'Report_Text': 'Lorem Ipsum'
    }
    too_late_row = {
        'MRN': '12',
        'Date_Time': '05/03/2010',
        'Report_Text': 'Lorem Ipsum'
    }
    date_info = {
        '12': [DateInfo(datetime.date(2010, 4, 28), datetime.timedelta(-3), datetime.timedelta(4))]
    }
    parsed_filter = ParsedFilter(
        id_col='MRN',
        date_col='Date_Time',
        filter_dict=date_info,
    )

    assert not include_row(too_early_row, '%m/%d/%Y', parsed_filter, False)
    assert not include_row(too_late_row, '%m/%d/%Y', parsed_filter, False)
    assert include_row(included_row, '%m/%d/%Y', parsed_filter, False)


def test_include_row_negative_after() -> None:
    included_row = {
        'EMPI': '12',
        'Report_Date_Time': '05/01/2010',
        'Report_Text': 'Lorem Ipsum'
    }
    too_early_row = {
        'EMPI': '12',
        'Report_Date_Time': '04/30/2010',
        'Report_Text': 'Lorem Ipsum'
    }
    too_late_row = {
        'EMPI': '12',
        'Report_Date_Time': '05/03/2010',
        'Report_Text': 'Lorem Ipsum'
    }
    date_info = {
        '12': [DateInfo(datetime.date(2010, 5, 2), datetime.timedelta(1), datetime.timedelta(-1))]
    }
    parsed_filter = ParsedFilter(
        id_col='EMPI',
        date_col='Report_Date_Time',
        filter_dict=date_info,
    )

    assert not include_row(too_early_row, '%m/%d/%Y', parsed_filter, False)
    assert not include_row(too_late_row, '%m/%d/%Y', parsed_filter, False)
    assert include_row(included_row, '%m/%d/%Y', parsed_filter, False)
