"""Fetch exact public calendar counts and render the contribution calendar."""
import json
import re
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
import render_heatmap_svg as renderer
import render_activity_svg

class Calendar(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days,self.counts=[],{}
        self.target,self.tip=None,''
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='td' and a.get('data-date'):
            self.days.append({'date':a['data-date'],'level':int(a.get('data-level',0)),'id':a.get('id','')})
        if tag=='tool-tip':
            self.target,self.tip=a.get('for'),''
    def handle_data(self,value):
        if self.target:
            self.tip+=value
    def handle_endtag(self,tag):
        if tag=='tool-tip' and self.target:
            match=re.search(r'(No|[\d,]+) contributions?',self.tip)
            if match:
                self.counts[self.target]=0 if match[1]=='No' else int(match[1].replace(',',''))
            self.target=None

username=json.loads(Path('profile.json').read_text())['username']
request=urllib.request.Request(f'https://github.com/users/{username}/contributions',headers={'User-Agent':'GitHub-profile-calendar'})
with urllib.request.urlopen(request,timeout=30) as response:
    parser=Calendar()
    parser.feed(response.read().decode())
days=sorted(parser.days,key=lambda d:d['date'])
if len(days)<350:
    raise RuntimeError('Calendar incomplete; preserving the existing graphic.')
for day in days:
    identity=day.pop('id')
    if identity not in parser.counts and day['level']>0:
        raise RuntimeError('Missing exact count; preserving the existing graphic.')
    day['count']=parser.counts.get(identity,0)
Path('data').mkdir(exist_ok=True)
Path('data/contributions.json').write_text(json.dumps({'days':days,'total':sum(d['count'] for d in days),'current_streak':0}))
renderer.PALETTE=['#17232d','#1b435b','#286a8c','#55a6ce','#8ed8f8','#c5ecfc']
renderer.main()
Path('assets/contributions.svg').write_text(Path('contrib-heatmap.svg').read_text(encoding='utf-8'),encoding='utf-8')
Path('contrib-heatmap.svg').unlink()
render_activity_svg.main()
print('Updated exact public contribution counts for',username)
