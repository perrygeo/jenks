import json
from pprint import pprint as pp
from jenks3 import jenks

def main():
    pp(jenks(json.load(open('test.json')), 5))

if __name__ == "__main__":
    main()
