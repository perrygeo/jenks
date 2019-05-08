import json
from jenks import jenks

def test_json():
    data = json.load(open('test.json'))
    breaks = jenks(data, 5)
    assert [round(float(v), 5) for v in breaks] == \
        [0.00281, 2.09355, 4.2055, 6.17815, 8.09176, 9.99798]

def test_short():
    data = [1, 2, 3, 100]
    breaks = jenks(data, 2)
    assert [round(v, 5) for v in breaks] == [1.0, 3.0, 100.0]
