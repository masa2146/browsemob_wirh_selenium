import json
from haralyzer import HarParser, HarPage

with open('giris_hepsiburada_com.har', 'r') as f:
    har_parser = HarParser(json.loads(f.read()))

print(har_parser.har_data)
# {u'name': u'Firefox', u'version': u'25.0.1'}

print(har_parser.hostname)
# 'humanssuck.net'

for page in har_parser.pages:
    assert isinstance(page, HarPage, None)
    # returns True for each