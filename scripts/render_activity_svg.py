"""Play a cosmetic snake sweep once, then restore the exact contribution grid.

Uses self-contained SVG/SMIL: no script, external renderer or account token.
The snake follows a non-intersecting grid route. A day is eaten when the
head reaches it; the final state always restores the original day colors.
"""
import datetime as dt
import html
import json
from pathlib import Path

COLORS = ['#17232d','#1b435b','#286a8c','#55a6ce','#8ed8f8']
CELL, STEP, LEFT, TOP = 13,16,46,38

def render(data):
    days=data['days']
    first=dt.date.fromisoformat(days[0]['date'])
    start=first-dt.timedelta(days=(first.weekday()+1)%7)
    cells=[]
    months={}
    for day in days:
        date=dt.date.fromisoformat(day['date'])
        week=(date-start).days//7
        row=(date.weekday()+1)%7
        cells.append((week,row,day))
        if date.day<=7:
            months.setdefault(date.strftime('%Y-%m'),(week,date.strftime('%b')))
    weeks=max(c[0] for c in cells)+1
    width,height=LEFT+weeks*STEP+14,196
    route=[(x,0) for x in range(-6,0)]
    route += [(x,y) for y in range(7) for x in (range(weeks) if y%2==0 else range(weeks-1,-1,-1))]
    route += [(x,6) for x in range(weeks,weeks+9)]
    reached={point:i for i,point in enumerate(route)}
    frame=.04
    begin=.7
    duration=(len(route)-1)*frame
    restore=begin+duration+8*frame+.3
    def xy(point):
        x,y=point
        return LEFT+x*STEP+CELL/2,TOP+y*STEP+CELL/2
    motion=' '.join(('M' if i==0 else 'L')+f'{xy(point)[0]},{xy(point)[1]}' for i,point in enumerate(route))
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" font-family="Consolas,Menlo,monospace" font-size="12">',
        '<title>Snake animation followed by the contribution calendar</title>',
        '<desc>A pale blue snake sweeps the grid once. Contribution colors then return and remain visible. Click the image in the profile to inspect GitHub contribution details.</desc>',
        '<style>@media(prefers-reduced-motion:reduce){.snake{display:none}.dot{opacity:1!important}}</style>',
        f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="8" fill="#0d1117" stroke="#30363d"/>',
        f'<defs><clipPath id="grid"><rect x="{LEFT-2}" y="{TOP-2}" width="{weeks*STEP+2}" height="{7*STEP+2}"/></clipPath></defs>']
    for week,label in months.values():
        parts.append(f'<text x="{LEFT+week*STEP}" y="24" fill="#8b949e">{label}</text>')
    for row,label in [(1,'Mon'),(3,'Wed'),(5,'Fri')]:
        parts.append(f'<text x="10" y="{TOP+row*STEP+11}" fill="#8b949e">{label}</text>')
    for week,row,day in cells:
        attrs=f'x="{LEFT+week*STEP}" y="{TOP+row*STEP}" width="{CELL}" height="{CELL}" rx="3"'
        parts.append(f'<rect {attrs} fill="{COLORS[0]}"/>')
        if day['level']:
            eaten=begin+reached[(week,row)]*frame
            back=restore+week*.006
            label=html.escape(f"{day['date']}: {day['count']} contributions")
            parts.append(f'<rect class="dot" {attrs} fill="{COLORS[day["level"]]}"><title>{label}</title><set attributeName="opacity" to="0" begin="{eaten:.3f}s" fill="freeze"/><animate attributeName="opacity" from="0" to="1" begin="{back:.3f}s" dur=".6s" fill="freeze"/></rect>')
    parts.append('<g class="snake" clip-path="url(#grid)">')
    # Tail is drawn first; each segment traces the same route one cell behind.
    for segment in range(7,-1,-1):
        delay=begin+segment*frame
        fill=['#d9f4ff','#b5e8fc','#8ed8f8','#74c7e9','#60b1d4','#4892b4','#35728e','#28566d'][segment]
        parts.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{delay:.3f}s"/><animate attributeName="opacity" from="1" to="0" begin="{delay+duration:.3f}s" dur=".1s" fill="freeze"/><animateMotion path="{motion}" rotate="auto" begin="{delay:.3f}s" dur="{duration:.3f}s" calcMode="paced" fill="freeze"/><rect x="-6.5" y="-6.5" width="13" height="13" rx="4" fill="{fill}"/>')
        if segment==0:
            parts.append('<circle cx="3" cy="-2.7" r="1.2" fill="#173647"/><circle cx="3" cy="2.7" r="1.2" fill="#173647"/>')
        parts.append('</g>')
    parts.append('</g>')
    fy=height-16
    parts.append(f'<text x="{LEFT}" y="{fy}" fill="#c9d1d9">{sum(d["count"] for d in days):,} contributions in the last year</text>')
    legend=width-172
    parts.append(f'<text x="{legend-38}" y="{fy}" fill="#8b949e">Less</text>')
    for i,color in enumerate(COLORS):
        parts.append(f'<rect x="{legend+i*STEP}" y="{fy-11}" width="13" height="13" rx="3" fill="{color}"/>')
    parts.append(f'<text x="{legend+5*STEP+6}" y="{fy}" fill="#8b949e">More</text></svg>')
    return '\n'.join(parts)

def main():
    data=json.loads(Path('data/contributions.json').read_text())
    Path('assets/activity-snake.svg').write_text(render(data),encoding='utf-8')
    print('Built snake animation and final contribution calendar')

if __name__=='__main__':
    main()
