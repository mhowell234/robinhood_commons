from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from json import JSONEncoder
from typing import Dict, List, Union


@dataclass
class Candle:
    current: float = 0.0
    open: float = 0.0
    close: float = 0.0
    high: float = 0.0
    low: float = 0.0
    day_high: float = 0.0
    day_low: float = 0.0
    day_open: float = 0.0


def to_picklable(candles: Dict[str, Dict[str, Candle]]) -> List[Dict[str, Union[str, Candle]]]:
    data = []

    for symbol, candle_data in candles.items():
        cdata = deepcopy(candle_data)
        cdata['symbol'] = symbol
        data.append(cdata)
    return data


def from_picklable(candles: List[Dict[str, Union[str, Candle]]]) -> Dict[str, Dict[str, Candle]]:
    data = defaultdict(lambda: defaultdict(Candle))

    for candle_data in candles:
        symbol = candle_data['symbol']
        del candle_data['symbol']

        data[symbol] = candle_data
    return data


class CandleEncoder(JSONEncoder):
    def default(self, other):
        return other.__dict__


def main() -> None:
    candle = Candle(current=1.0, open=1.0, close=2.0, high=4.0, low=0.5, day_high=1.0, day_low=0.5, day_open=0.0)
    print(candle)


if __name__ == '__main__':
    main()
