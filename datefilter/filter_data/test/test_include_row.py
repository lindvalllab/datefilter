import datetime

from date_info import DateInfo
from ..filter_data import include_row


def test_include_row_true() -> None:
    row = {
        'EMPI': '12',
        'Report_Date_Time': '05/01/2010',
        'Report_Text': 'Lorem Ipsum'
    }
    date_info = {
        '12': DateInfo(datetime.date(2010, 5, 3), datetime.timedelta(2), datetime.timedelta(0))
    }
    assert include_row(row, date_info)


def test_include_row_false() -> None:
    row = {
        'EMPI': '12',
        'Report_Date_Time': '04/30/2010',
        'Report_Text': 'Lorem Ipsum'
    }
    date_info = {
        '12': DateInfo(datetime.date(2010, 5, 3), datetime.timedelta(2), datetime.timedelta(0))
    }
    assert not include_row(row, date_info)


def test_include_row_negative_before() -> None:
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
        '12': DateInfo(datetime.date(2010, 4, 28), datetime.timedelta(-3), datetime.timedelta(4))
    }
    assert not include_row(too_early_row, date_info)
    assert not include_row(too_late_row, date_info)
    assert include_row(included_row, date_info)


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
        '12': DateInfo(datetime.date(2010, 5, 2), datetime.timedelta(1), datetime.timedelta(-1))
    }

    assert not include_row(too_early_row, date_info)
    assert not include_row(too_late_row, date_info)
    assert include_row(included_row, date_info)
