"""Embed Phosphor icons into a prototype page.

Usage: python3 -I brand/tools/embed_phosphor.py <phosphor-assets-dir> <page.html>
<phosphor-assets-dir> is the assets folder of @phosphor-icons/core@2.1.1 (npm pack, then tar -xzf).
The page declares the icons it needs on <script id="icon-data" data-names="house drop ...">.
Names ending in ":fill" also embed the fill weight. The block is filled with window.PH = {name: [viewBox, body], ...},
regular weight under the plain name and fill weight under "name:fill".
"""
import json, os, re, sys

ASSETS, PAGE = sys.argv[1], sys.argv[2]


def read(weight, name):
    suffix = '' if weight == 'regular' else f'-{weight}'
    path = os.path.join(ASSETS, weight, f'{name}{suffix}.svg')
    if not os.path.exists(path):
        sys.exit(f'missing icon: {weight}/{name}')
    svg = open(path).read()
    vb = re.search(r'viewBox="([^"]+)"', svg).group(1)
    body = re.sub(r'(?s)^.*?<svg[^>]*>', '', svg)
    body = re.sub(r'</svg>\s*$', '', body.strip())
    body = re.sub(r'<rect width="256" height="256" fill="none"\s*/>', '', body)
    return [vb, re.sub(r'\s+', ' ', body).strip()]


page = open(PAGE).read()
m = re.search(r'<script id="icon-data" data-names="([^"]+)">.*?</script>', page, flags=re.S)
if not m:
    sys.exit('icon-data block not found')
icons = {}
for token in m.group(1).split():
    name, _, extra = token.partition(':')
    icons[name] = read('regular', name)
    if extra == 'fill':
        icons[f'{name}:fill'] = read('fill', name)
js = '/* Phosphor 2.1.1 (MIT), embedded by brand/tools/embed_phosphor.py */\nwindow.PH = ' + json.dumps(icons, separators=(',', ':')) + ';\n'
block = f'<script id="icon-data" data-names="{m.group(1)}">\n{js}</script>'
page = page[:m.start()] + block + page[m.end():]
open(PAGE, 'w').write(page)
print(len(icons), 'icons,', len(js), 'bytes')
