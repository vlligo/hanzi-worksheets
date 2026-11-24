"""Build the offline generator. Python fontTools is required for this build only."""
import base64
import json
from pathlib import Path
from xml.etree import ElementTree

from fontTools.pens.recordingPen import RecordingPen
from fontTools.svgLib.path import parse_path

from fontTools.ttLib import TTFont

HERE = Path(__file__).resolve().parent
assets = HERE / 'data'
data = json.loads((assets / 'strokes.json').read_text(encoding='utf-8'))
licenses = json.loads((assets / 'licenses.json').read_text(encoding='utf-8'))
licenses['DejaVu Sans — Bitstream Vera license'] = (HERE / 'DejaVuSans-LICENSE.txt').read_text(encoding='utf-8')

font_path = HERE / 'DejaVuSans.ttf'
font_bytes = font_path.read_bytes()
with TTFont(font_path) as font:
    head = font['head']
    hhea = font['hhea']
    def points(value):
        return round(value * 1000 / head.unitsPerEm)

    font_info = {
        'chars': {
            chr(code): [font.getGlyphID(name), points(font['hmtx'][name][0])]
            for code, name in font.getBestCmap().items()
        },
        'bounds': [points(n) for n in (head.xMin, head.yMin, head.xMax, head.yMax)],
        'ascent': points(hhea.ascent),
        'descent': points(hhea.descent),
    }

def embedded(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')

def brand_mark():
    android = '{http://schemas.android.com/apk/res/android}'
    vector = ElementTree.parse(HERE / 'chinlearn-brand-mark.xml').getroot()
    commands = {'moveTo': 'M', 'lineTo': 'L', 'qCurveTo': 'Q', 'curveTo': 'C', 'closePath': 'Z'}
    paths = []
    for container in [vector, *vector.findall('group')]:
        dx = float(container.get(android + 'translateX', 0))
        dy = float(container.get(android + 'translateY', 0))
        for path in container.findall('path'):
            pen = RecordingPen()
            parse_path(path.attrib[android + 'pathData'], pen)
            parts = [
                [commands[op], *(axis for x, y in points for axis in (x + dx, y + dy))]
                for op, points in pen.value if op != 'endPath'
            ]
            stroke = path.get(android + 'strokeColor')
            paths.append({
                'parts': parts,
                'color': stroke or path.attrib[android + 'fillColor'],
                'width': float(path.get(android + 'strokeWidth', 0)),
            })
    return {'size': float(vector.attrib[android + 'viewportWidth']), 'paths': paths}

output = HERE / 'hanzi-worksheets.html'
html = (HERE / 'template.html').read_text(encoding='utf-8')
replacements = {
    '__DATA__': embedded(data),
    '__LICENSES__': embedded('\n\n'.join(f'{k}\n{v}' for k, v in licenses.items())),
    '__FONT_INFO__': embedded(font_info),
    '__FONT_BYTES__': base64.b64encode(font_bytes).decode('ascii'),
    '__BRAND_MARK__': embedded(brand_mark()),
}
for key, value in replacements.items():
    html = html.replace(key, value)
output.write_text(html, encoding='utf-8')
(HERE / 'index.html').write_text(html, encoding='utf-8')
print(f'{output}: {output.stat().st_size / 1e6:.1f} MB; {len(data)} characters')
