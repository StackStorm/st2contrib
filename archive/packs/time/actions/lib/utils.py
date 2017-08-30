import time

__all__ = [
    'dt_to_timestamp'
]


def dt_to_timestamp(dt):
    timestamp = int(time.mktime(dt.timetuple()))
    return timestamp
