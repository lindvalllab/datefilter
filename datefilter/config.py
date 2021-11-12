from dataclasses import dataclass

import appdirs


@dataclass
class DatefilterConfig:
    date_format: str


def parse_config() -> DatefilterConfig:
    appdirs.user_config_dir('datefilter')
    return DatefilterConfig('%m/%d/%Y')
