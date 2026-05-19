import json

FILE = "data.json"


def load():
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_schedule(day):
    data = load()
    return data["schedule"].get(day.lower(), [])


def get_homework(subject):
    data = load()
    return data["homework"].get(subject.lower(), [])


def get_deadlines():
    data = load()
    return data["deadlines"]