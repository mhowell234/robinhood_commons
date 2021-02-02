from datetime import datetime, timedelta, time
from typing import Tuple

from robinhood_commons.util.date_utils import to_date, tz_localize
from robinhood_commons.util.market_utils import in_extended_hours_market_time_window, in_market_time_window, \
    in_post_extended_hours_market_time_window, in_pre_extended_hours_market_time_window, in_post_market_time_window, \
    in_pre_market_time_window, is_extended_hours_market_open, is_market_open, time_til_extended_close, \
    time_til_extended_open, time_til_regular_close, time_til_regular_open, CLOSE_TIME, OPEN_TIME, \
    PRE_MARKET_OPEN_TIME, POST_MARKET_CLOSE_TIME

ONE_MINUTE: timedelta = timedelta(minutes=1)

# Wednesday, no holiday
MARKET_OPEN_DATE: datetime = to_date(date_str='20210127')
# Next Saturday
WEEKEND_DATE: datetime = MARKET_OPEN_DATE + timedelta(days=3)
# Previous MLK day
HOLIDAY_DATE: datetime = MARKET_OPEN_DATE - timedelta(days=9)


def test_is_market_open_regular_date_is_open_during_expected_times():
    _, after_market_open = generate_date_times(a_date=MARKET_OPEN_DATE, a_time=OPEN_TIME)
    before_market_close, _ = generate_date_times(a_date=MARKET_OPEN_DATE, a_time=CLOSE_TIME)

    assert is_market_open(after_market_open)
    assert is_market_open(before_market_close)


def test_is_market_open_regular_date_is_closed_during_expected_times():
    before_market_open, _ = generate_date_times(a_date=MARKET_OPEN_DATE, a_time=OPEN_TIME)
    _, after_market_close = generate_date_times(a_date=MARKET_OPEN_DATE, a_time=CLOSE_TIME)

    assert not is_market_open(before_market_open)
    assert not is_market_open(after_market_close)


def test_is_market_open_weekend_date_is_closed_during_expected_times():
    before_market_open, after_market_open = generate_date_times(a_date=WEEKEND_DATE, a_time=OPEN_TIME)
    before_market_close, after_market_close = generate_date_times(a_date=WEEKEND_DATE, a_time=CLOSE_TIME)

    assert not is_market_open(before_market_open)
    assert not is_market_open(after_market_open)
    assert not is_market_open(before_market_close)
    assert not is_market_open(after_market_close)


def test_is_market_open_holiday_date_is_closed_during_expected_times():
    before_market_open, after_market_open = generate_date_times(a_date=HOLIDAY_DATE, a_time=OPEN_TIME)
    before_market_close, after_market_close = generate_date_times(a_date=HOLIDAY_DATE, a_time=CLOSE_TIME)

    assert not is_market_open(before_market_open)
    assert not is_market_open(after_market_open)
    assert not is_market_open(before_market_close)
    assert not is_market_open(after_market_close)


def test_is_extended_hours_market_open_regular_date_is_open_during_expected_times():
    _, after_after_hours_market_open = generate_date_times(a_date=MARKET_OPEN_DATE, a_time=PRE_MARKET_OPEN_TIME)
    before_after_hours_market_close, _ = generate_date_times(a_date=MARKET_OPEN_DATE, a_time=POST_MARKET_CLOSE_TIME)

    assert is_extended_hours_market_open(after_after_hours_market_open)
    assert is_extended_hours_market_open(before_after_hours_market_close)


def test_is_extended_hours_market_open_regular_date_is_closed_during_expected_times():
    before_after_hours_market_open, _ = generate_date_times(a_date=MARKET_OPEN_DATE, a_time=PRE_MARKET_OPEN_TIME)
    _, after_after_hours_market_close = generate_date_times(a_date=MARKET_OPEN_DATE, a_time=POST_MARKET_CLOSE_TIME)

    assert not is_extended_hours_market_open(before_after_hours_market_open)
    assert not is_extended_hours_market_open(after_after_hours_market_close)


def test_is_extended_hours_market_open_weekend_date_is_closed_during_expected_times():
    before_after_hours_market_open, after_after_hours_market_open = generate_date_times(a_date=WEEKEND_DATE,
                                                                                        a_time=PRE_MARKET_OPEN_TIME)
    before_after_hours_market_close, after_after_hours_market_close = generate_date_times(a_date=WEEKEND_DATE,
                                                                                          a_time=POST_MARKET_CLOSE_TIME)

    assert not is_extended_hours_market_open(before_after_hours_market_open)
    assert not is_extended_hours_market_open(after_after_hours_market_open)
    assert not is_extended_hours_market_open(before_after_hours_market_close)
    assert not is_extended_hours_market_open(after_after_hours_market_close)


def test_is_extended_hours_market_open_holiday_date_is_closed_during_expected_times():
    before_after_hours_market_open, after_after_hours_market_open = generate_date_times(a_date=HOLIDAY_DATE,
                                                                                        a_time=PRE_MARKET_OPEN_TIME)
    before_after_hours_market_close, after_after_hours_market_close = generate_date_times(a_date=HOLIDAY_DATE,
                                                                                          a_time=POST_MARKET_CLOSE_TIME)

    assert not is_extended_hours_market_open(before_after_hours_market_open)
    assert not is_extended_hours_market_open(after_after_hours_market_open)
    assert not is_extended_hours_market_open(before_after_hours_market_close)
    assert not is_extended_hours_market_open(after_after_hours_market_close)


def test_time_til_regular_close_market_not_open_max_time():
    before_market_open, _ = generate_date_times(a_date=MARKET_OPEN_DATE, a_time=OPEN_TIME)

    assert timedelta.max == time_til_regular_close(a_date=before_market_open)


def test_time_til_regular_close_market_open_expected_time():
    one_hour_before = tz_localize(datetime.combine(MARKET_OPEN_DATE, CLOSE_TIME) - timedelta(hours=1))

    assert timedelta(hours=1) == time_til_regular_close(a_date=one_hour_before)


def test_time_til_extended_close_market_not_open_max_time():
    before_after_hours_market_open, _ = generate_date_times(a_date=MARKET_OPEN_DATE, a_time=PRE_MARKET_OPEN_TIME)

    assert timedelta.max == time_til_extended_close(a_date=before_after_hours_market_open)


def test_time_til_regular_open_market_not_open_expected_time():
    one_hour_before = tz_localize(datetime.combine(MARKET_OPEN_DATE, OPEN_TIME) - timedelta(hours=1))

    assert timedelta(hours=1) == time_til_regular_open(a_date=one_hour_before)


def test_time_til_regular_open_market_open_expected_time():
    one_hour_after = tz_localize(datetime.combine(MARKET_OPEN_DATE, OPEN_TIME) + timedelta(hours=1))

    assert timedelta.min == time_til_regular_open(a_date=one_hour_after)


def test_time_til_extended_open_market_not_open_expected_time():
    one_hour_before = tz_localize(datetime.combine(MARKET_OPEN_DATE, PRE_MARKET_OPEN_TIME) - timedelta(hours=1))

    assert timedelta(hours=1) == time_til_extended_open(a_date=one_hour_before)


def test_in_market_time_window_pre_time_window():
    before_market_open, after_market_open = generate_date_times(a_date=MARKET_OPEN_DATE, a_time=OPEN_TIME)

    assert not in_market_time_window(before_market_open)
    assert in_market_time_window(after_market_open)


def test_in_market_time_window_post_time_window():
    before_market_close, after_market_close = generate_date_times(a_date=MARKET_OPEN_DATE, a_time=CLOSE_TIME)

    assert in_market_time_window(before_market_close)
    assert not in_market_time_window(after_market_close)


def test_in_extended_hours_time_window_pre_post_time_window():
    before_pre_market_open, after_pre_market_open = generate_date_times(a_date=MARKET_OPEN_DATE,
                                                                        a_time=PRE_MARKET_OPEN_TIME)

    assert not in_extended_hours_market_time_window(before_pre_market_open)
    assert in_extended_hours_market_time_window(after_pre_market_open)


def test_in_extended_hours_time_window_post_time_window():
    before_post_market_close, after_post_market_close = generate_date_times(a_date=MARKET_OPEN_DATE,
                                                                            a_time=POST_MARKET_CLOSE_TIME)

    assert in_extended_hours_market_time_window(before_post_market_close)
    assert not in_extended_hours_market_time_window(after_post_market_close)


def test_in_market_time_window_pre_market():
    pre_market, during_market = generate_date_times(a_date=MARKET_OPEN_DATE, a_time=OPEN_TIME)

    assert in_pre_market_time_window(pre_market)
    assert not in_pre_market_time_window(during_market)


def test_in_market_time_window_post_market():
    during_market, post_market = generate_date_times(a_date=MARKET_OPEN_DATE, a_time=CLOSE_TIME)

    assert not in_post_market_time_window(during_market)
    assert in_post_market_time_window(post_market)


def test_in_pre_extended_hours_market_time_window_pre_market():
    before_pre_extended_market, during_extended_market = generate_date_times(a_date=MARKET_OPEN_DATE,
                                                                             a_time=PRE_MARKET_OPEN_TIME)

    assert not in_pre_extended_hours_market_time_window(before_pre_extended_market)
    assert in_pre_extended_hours_market_time_window(during_extended_market)


def test_in_post_extended_hours_market_time_window_post_market():
    during_extended_market, post_extended_market = generate_date_times(a_date=MARKET_OPEN_DATE,
                                                                       a_time=POST_MARKET_CLOSE_TIME)

    assert in_post_extended_hours_market_time_window(during_extended_market)
    assert not in_post_extended_hours_market_time_window(post_extended_market)


def generate_date_times(a_date: datetime, a_time: time) -> Tuple[datetime, datetime]:
    return datetime.combine(a_date, a_time) - ONE_MINUTE, datetime.combine(a_date, a_time) + ONE_MINUTE
