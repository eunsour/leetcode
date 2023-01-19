from datetime import datetime, timedelta

DEFAULT_FORMAT = "%Y-%m-%d %H:%M:%S"


def get_epoch_ms(dt: datetime = datetime.now()) -> int:
    return int(dt.timestamp() * 1000)


def epoch_ms_to_date_str(epoch_ms: int, fmt: str = DEFAULT_FORMAT) -> str:
    return datetime.fromtimestamp(epoch_ms / 1000).strftime(fmt)


def get_kst_now(fmt: str = DEFAULT_FORMAT) -> str:
    return (datetime.utcnow() + timedelta(hours=9)).strftime(fmt)


def get_kst_today(dt: datetime = datetime.now()) -> str:
    return dt.strftime("%Y년 %m월 %d일")
