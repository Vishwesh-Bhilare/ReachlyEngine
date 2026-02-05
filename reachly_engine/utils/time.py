from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_timestamp() -> str:
    """
    Return compact UTC timestamp for filenames.
    """
    return utc_now().strftime("%Y%m%d_%H%M%S")

