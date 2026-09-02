"""Build a compact portrait and neofetch card, based on navi3582's template."""
import html
import json
from pathlib import Path
import make_info_card as card

profile=json.loads(Path('profile.json').read_text(encoding='utf-8'))
lines=Path('assets/portrait.txt').read_text().splitlines()
card.TITLE=profile['username']+'@github'
card.W=620
card.ROWS=[('', '')]+[(key.title(),profile[key]) for key in ['name','location','role','focus','interests','tools','status']]
card.main()
Path('assets/info-card.svg').write_text(Path('info-card.svg').read_text(encoding='utf-8'),encoding='utf-8')
Path('info-card.svg').unlink()

cw,ch=7.2,13.5
w,h=round(84*cw+24),round(len(lines)*ch+24)
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Consolas,Menlo,monospace" font-size="13">',
       '<title>Animated ASCII caricature</title>',f'<rect width="{w}" height="{h}" rx="8" fill="#0d1117"/>','<defs>']
for i in range(len(lines)):
    parts.append(f'<clipPath id="r{i}"><rect width="0" height="16"><animate attributeName="width" from="0" to="{w}" begin="{i*.035:.3f}s" dur=".45s" fill="freeze"/></rect></clipPath>')
parts.append('</defs>')
for i,line in enumerate(lines):
    if not line.strip():
        continue
    parts.append(f'<g transform="translate(12,{12+i*ch})" clip-path="url(#r{i})"><text y="12" fill="#c9d1d9" xml:space="preserve" textLength="{len(line)*cw}" lengthAdjust="spacingAndGlyphs">{html.escape(line)}</text></g>')
parts.append('</svg>')
Path('assets/ascii-portrait.svg').write_text('\n'.join(parts),encoding='utf-8')
