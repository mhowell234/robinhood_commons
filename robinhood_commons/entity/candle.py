from __future__ import annotations

from dataclasses import dataclass
from json import JSONEncoder


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


class CandleEncoder(JSONEncoder):
    def default(self, other):
        return other.__dict__


def main() -> None:
    candle = Candle(current=1.0, open=1.0, close=2.0, high=4.0, low=0.5, day_high=1.0, day_low=0.5, day_open=0.0)
    print(candle)


if __name__ == '__main__':
    main()
