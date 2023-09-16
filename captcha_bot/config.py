import json
import os


def parse_config(path: str) -> dict[str, str | int | list]:
    """Return a dict with specified config file keys and values. If file isn't found create a new one."""
    try:
        with open(path, 'r', encoding='UTF-8') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        config = {
            'token': '',
            'owner_id': 0,
            'include_directories': [],
            'exclude_directories': []
        }

        with open(path, 'w', encoding='UTF-8') as config_file:
            json.dump(config, config_file, indent=4, ensure_ascii=False)

        raise FileNotFoundError(f'{os.path.basename(path)} file wasn\'t found. Fill the fields in the created file.')