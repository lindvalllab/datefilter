import json
import dataclasses
import os

import appdirs


@dataclasses.dataclass
class DatefilterConfig:
    date_format: str = '%m/%d/%Y'
    include_missing: bool = False


def parse_config() -> DatefilterConfig:
    config_dir = appdirs.user_config_dir('datefilter')
    config_path = os.path.join(config_dir, 'config.json')
    try:
        with open(config_path) as config_file:
            config_dict = json.load(config_file)
            return DatefilterConfig(**config_dict)
    except Exception:
        # Write a default config file.
        write_config(DatefilterConfig())
        return DatefilterConfig()


def write_config(config: DatefilterConfig) -> None:
    config_dir = appdirs.user_config_dir('datefilter')
    config_path = os.path.join(config_dir, 'config.json')
    os.makedirs(config_dir, exist_ok=True)
    config_dict = dataclasses.asdict(config)
    with open(config_path, 'w') as config_file:
        json.dump(config_dict, config_file, indent=1)
