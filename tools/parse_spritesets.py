import re
import sys
from collections import defaultdict
from pprint import pprint

RX_SPRITESET = re.compile(r'spriteset\((\w+), "([\w\/\.]+)"\)\s+{\s+template_(\w+)\((\d+),\s+(\d+)\)\s+}', re.MULTILINE)
RX_GRAPHICS_SUBTYPE_SWITCH = re.compile(r'switch\(FEAT_TRAINS,\s*SELF,\s*(\w+),\s*cargo_subtype\){([^}]*)}', re.MULTILINE)
RX_GRAPHICS_ITEM = re.compile(r'(\d+):\s*spriteset_\w+_(\w+);', re.MULTILINE)

RX_STRINGS_SUBTYPE_SWITCH = re.compile(r'switch\(FEAT_TRAINS,\s*SELF,\s*(\w+)_cargo_subtype_text,\s*cargo_subtype\){([^}]*)\s*return CB_RESULT_NO_TEXT;\s*}', re.MULTILINE)
RX_STRINGS_ITEM = re.compile(r'(\d+):\s*return string\((\w+)\);', re.MULTILINE)


file = sys.argv[1]


res = defaultdict(dict)
string_orders = defaultdict(dict)
graphics_orders = defaultdict(dict)
with open(file) as f:
	data = f.read()
	n = data.count('spriteset(')
	m = RX_SPRITESET.findall(data)
	assert len(m) == n, (m, n)

	for set_id, file, template, x, y in m:
		if set_id.endswith('Purchase'):
			continue
		set_id = set_id[len('spriteset_BR158a_'):]
		# res[file][set_id] = (template, int(x), int(y))
		res[file][set_id] = (template, int(x), int(y))

	for sid, s in RX_STRINGS_SUBTYPE_SWITCH.findall(data):
		string_orders[sid] = [(int(i), n) for i, n in RX_STRINGS_ITEM.findall(s)]

	for sid, s in RX_GRAPHICS_SUBTYPE_SWITCH.findall(data):
		if sid.endswith('cargo_subtype_text'):
			continue
		graphics_orders[sid] = [(int(i), n) for i, n in RX_GRAPHICS_ITEM.findall(s)]

string_order = next(iter(string_orders.values()))
assert all(string_order == v for v in string_orders.values())
string_order.sort()
print('String order:')
pprint(string_order)

graphics_order = next(iter(graphics_orders.values()))
assert all(graphics_order == v for v in graphics_orders.values())
graphics_order.sort()
print('Graphics order:')
pprint(graphics_order)

assert len(string_order) == len(graphics_order)

graphics_idx = {s: i for i, s in graphics_order}

for k, v in res.items():
	templates = set(x[0] for x in v.values())
	assert len(templates) == 1
	assert all(x[1] == 0 for x in v.values())
	assert all(x[2] % 25 == 13 for x in v.values())
	template = next(iter(templates))
	print(f'File: {k}')
	print(f'Template: {template}')

	# pprint({
	# 	s: (v[graphics_order[i][1]][2] - 13) // 25
	# 	for i, s in string_order
	# })

	for i, s in string_order:
		name = s[4:]
		slot = (v[graphics_order[i][1]][2] - 13) // 25
		print(f'{name!r}: {slot},')

	# pprint({
	# 	name: (data[2] - 13) // 25
	# 	for name, data in v.items()
	# })
	print()

	for name, data in v.items():
		if name not in graphics_idx:
			print('Spriteset in graphics: ', name, (data[2] - 13) // 25)

# l = list(res.values())
# print('Equal: ', l[0] == l[1])
