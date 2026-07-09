from datetime import datetime
from threading import Lock

_lock = Lock()

_data = {
    "total_all": 0,
    "today_count": 0,
    "today_date": datetime.now().strftime("%Y-%m-%d"),
    "history": {},
    "last_sent": None,
}

def increment():
    with _lock:
        today = datetime.now().strftime("%Y-%m-%d")
        if _data["today_date"] != today:
            _data["today_date"] = today
            _data["today_count"] = 0
        _data["today_count"] += 1
        _data["total_all"] += 1
        _data["history"][today] = _data["today_count"]
        _data["last_sent"] = datetime.now().strftime("%H:%M:%S")

def get_stats():
    with _lock:
        today = datetime.now().strftime("%Y-%m-%d")
        if _data["today_date"] != today:
            _data["today_date"] = today
            _data["today_count"] = 0
        return {
            "today": _data["today_count"],
            "total": _data["total_all"],
            "last_sent": _data["last_sent"],
            "history": dict(sorted(_data["history"].items(), reverse=True)),
            "date": today,
        }
