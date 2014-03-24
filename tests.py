import json
from jenks import jenks

def test_json():
    data = json.load(open('test.json'))
    breaks = jenks(data, 5)
    assert [round(v, 6) for v in breaks] == [0.002811,
                                             2.093548,
                                             4.205495,
                                             6.178148,
                                             8.091759,
                                             9.997983]
