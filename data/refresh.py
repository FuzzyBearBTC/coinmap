#!/usr/bin/python
import os
import json
import json.encoder
from overpass import parser as overpass_parser

scriptdir = os.path.dirname(os.path.abspath(__file__))

coins = {
	'Bitcoin': 'XBT',
	'Litecoin': 'XLT',
}

parsers = {
	'overpass': overpass_parser,
}

# update data/currencies
with open(scriptdir + '/coins.js', 'w') as f:
	f.write('function get_coins() { return ["%s"]; }\n' % '", "'.join(sorted(coins.keys())))

# call individual parsers
for name, parser in parsers.iteritems():
	for coin in coins:
		coinlower = coin.lower()
		pts = parser.get_points(coinlower,coins[coin])
		json.encoder.FLOAT_REPR = lambda x: str(x) # fix for 52.1989256 showing as 52.198925299999999
		json.dump(pts, open(scriptdir + '/data-%s-%s.json' % (name, coinlower), 'w'), separators = (',', ':'))
