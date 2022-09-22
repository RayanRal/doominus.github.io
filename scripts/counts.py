from dataclasses import dataclass, asdict
from typing import Any, Optional, List, Dict
from pyairtable import Table

import requests


@dataclass
class Losses:
    date_str: str = ""
    personnel: int = 0
    tanks: int = 0
    mlrs: int = 0
    artillery: int = 0
    acv: int = 0


def fetch_data(url: str) -> Optional[Dict[str, Any]]:
    url_response = requests.get(url)
    if url_response.status_code != 200:
        return None
    return url_response.json()['data']


def get_date_increments(date: str, daily_data: Dict[str, Any]) -> Losses:
    date_str = date.replace(".", "-")
    return Losses(
        date_str,
        daily_data.get('personnel', 0),
        daily_data.get('tanks', 0),
        daily_data.get('mlrs', 0),
        daily_data.get('artillery', 0),
        daily_data.get('apv', 0),
    )


def rollup_data(data):
    parsed = [get_date_increments(date, datum) for date, datum in data.items()]
    last_date = parsed[-1].date_str
    return Losses(
        last_date,
        personnel=sum([p.personnel for p in parsed]),
        tanks=sum([p.tanks for p in parsed]),
        acv=sum([p.acv for p in parsed]),
        artillery=sum([p.artillery for p in parsed]),
        mlrs=sum([p.mlrs for p in parsed]),
    )


def main():
    URL = "<url>"
    data = fetch_data(URL)
    rollup = rollup_data(data)
    save_to_db(rollup)


# Database
@dataclass
class DbEntry:
    date: str
    category: str
    count: int


def rollup_to_records(rollup: Losses) -> List[Dict[str, Any]]:
    entries = [
        DbEntry(rollup.date_str, "personnel", rollup.personnel),
        DbEntry(rollup.date_str, "tanks", rollup.tanks),
        DbEntry(rollup.date_str, "acv", rollup.acv),
        DbEntry(rollup.date_str, "artillery", rollup.artillery),
        DbEntry(rollup.date_str, "mlrs", rollup.mlrs),
    ]
    return [asdict(entry) for entry in entries]


def save_to_db(rollup: Losses) -> List[Dict[Any, Any]]:
    print(f"Will save to DB: {rollup}")
    api_key = '<api_key>'

    table = Table(api_key, '<table_id>', 'losses')
    records = rollup_to_records(rollup)
    return table.batch_create(records, typecast=True)


main()
