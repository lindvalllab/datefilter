import datetime
from dataclasses import dataclass


@dataclass
class DateInfo:
    anchor_date: datetime.date
    days_before: datetime.timedelta
    days_after: datetime.timedelta
