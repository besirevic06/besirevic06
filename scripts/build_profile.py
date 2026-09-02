"""Build terminal SVGs from editable profile data and ASCII art."""
import html
import json
from pathlib import Path

BG, PANEL, BORDER = '#0d1117', '#101820', '#263743'
FG, DIM, BLUE = '#dbe7ef', '#8b9fac', '#8ed8f8'
FONT = 'Consolas,Menlo,DejaVu Sans Mono,monospace'
data = json.loads(Path('profile.json').read_text(encoding='utf-8'))
lines = Path('assets/portrait.txt').read_text().splitlines()

def text(x,y,value,size=16,color=FG,extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {extra}>{html.escape(value)}</text>'

def build(mobile=False):
    w,h = (580,1070) if mobile else (1060,640)
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="{FONT}">',
      '<title>Kadir Can — besirevic06</title>',
      '<style>.info{animation:appear .6s ease-out backwards}@keyframes appear{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}@media(prefers-reduced-motion:reduce){.info{animation:none}}</style>',
      f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="{BG}" stroke="{BORDER}"/>']
    for x,c in [(24,'#ff6b65'),(44,'#e6b85c'),(64,'#62c98b')]:
        parts.append(f'<circle cx="{x}" cy="24" r="5" fill="{c}"/>')
    parts += [text(w/2,29,'besirevic06@github',13,DIM,'text-anchor="middle"'),
      f'<path d="M1 47H{w-1}" stroke="{BORDER}"/>',text(28,84,'~ $ whoami',16,BLUE)]
    x0,y0=(155,112) if mobile else (84,112)
    char_w,char_h=3.2,6
    parts.append('<defs>')
    for i in range(len(lines)):
        parts.append(f'<clipPath id="r{i}"><rect width="0" height="8"><animate attributeName="width" from="0" to="400" dur=".4s" begin="{i*.035:.3f}s" fill="freeze"/></rect></clipPath>')
    parts.append('</defs>')
    for i,line in enumerate(lines):
        if line.strip():
            parts.append(f'<g transform="translate({x0},{y0+i*char_h})" clip-path="url(#r{i})">'+text(0,5.6,line,6.5,FG,f'xml:space="preserve" textLength="{len(line)*char_w}" lengthAdjust="spacingAndGlyphs"')+'</g>')
    cx,cy=(24,640) if mobile else (438,150)
    cw=w-cx-24
    parts += [f'<rect x="{cx}" y="{cy}" width="{cw}" height="376" rx="10" fill="{PANEL}" stroke="{BORDER}"/>',
      text(cx+24,cy+37,'besirevic06@github',19,BLUE),text(cx+24,cy+61,'──────────────────────',15,DIM)]
    for i,key in enumerate(['name','location','role','focus','interests','tools','status']):
        y=cy+99+i*36
        parts += [f'<g class="info" style="animation-delay:{.25+i*.14:.2f}s">',text(cx+24,y,key,15,BLUE),text(cx+132,y,data[key],14 if mobile else 15),'</g>']
    for i,c in enumerate(['#193546','#24546d','#357c9d','#62b4d7','#8ed8f8','#c5ecfc']):
        parts.append(f'<rect x="{cx+24+i*25}" y="{cy+345}" width="25" height="7" fill="{c}"/>')
    parts += [text(28,h-25,'draw. design. learn. repeat.',13,DIM),'</svg>']
    target='profile-mobile.svg' if mobile else 'profile.svg'
    Path('assets',target).write_text('\n'.join(parts),encoding='utf-8')
    print('Built',target)

build()
build(True)

