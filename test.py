import json
from jenks import jenks

if __name__ == "__main__":
    jenks(json.load(open('test.json')), 5)
