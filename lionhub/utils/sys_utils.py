
import datetime

def timestamp_to_datetime(timestamp: int) -> str:
    if isinstance(timestamp, str):
        try:
            timestamp = int(timestamp)
        except:
            return timestamp
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
