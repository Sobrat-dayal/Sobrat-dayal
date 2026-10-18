"""Replace the skyline's commit-language pie with all public non-fork source languages."""
from pathlib import Path
from collections import Counter
import math
import xml.etree.ElementTree as ET
import json
from update_profile import fetch, USER

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
def element(parent, tag, **attrs):
    return ET.SubElement(parent, '{'+NS+'}'+tag, {k:str(v) for k,v in attrs.items()})
def label(parent,x,y,value,size=17):
    element(parent,'text',x=x,y=y,fill='#eeeeff',**{'font-size':size}).text=value

def main():
    totals=Counter()
    page=1
    while True:
        repos=json.loads(fetch(f'https://api.github.com/users/{USER}/repos?per_page=100&page={page}',True))
        for repo in repos:
            if not repo['fork']:
                totals.update(json.loads(fetch(repo['languages_url'],True)))
        if len(repos)<100: break
        page+=1
    if not totals: raise ValueError('No language data; preserving previous image')
    target=Path(__file__).resolve().parents[1]/'profile-3d-contrib/profile-night-green.svg'
    tree=ET.parse(target)
    root=tree.getroot()
    old=next((g for g in root if g.get('transform')=='translate(40, 520)'),None)
    if old is None: raise ValueError('Upstream layout changed; language panel not found')
    index=list(root).index(old)
    root.remove(old)
    panel=ET.Element('{'+NS+'}g',{'transform':'translate(40, 520)','id':'all-repository-languages'})
    root.insert(index,panel)
    label(panel,0,0,'LANGUAGES · PUBLIC SOURCE BYTES',16)
    colors={'TypeScript':'#3178c6','CSS':'#a78bfa','JavaScript':'#f1e05a','Python':'#55a9e8','HTML':'#e34c26'}
    palette=['#34d399','#f472b6','#fb923c','#22d3ee']
    total=sum(totals.values())
    cx,cy,r=110,130,92
    start=-math.pi/2
    items=totals.most_common()
    for i,(name,count) in enumerate(items):
        fraction=count/total
        color=colors.get(name,palette[i%len(palette)])
        end=start+fraction*2*math.pi
        x1,y1=cx+r*math.cos(start),cy+r*math.sin(start)
        x2,y2=cx+r*math.cos(end),cy+r*math.sin(end)
        if len(items)==1:
            shape=element(panel,'circle',cx=cx,cy=cy,r=r,fill=color)
        else:
            shape=element(panel,'path',d=f'M{cx},{cy} L{x1},{y1} A{r},{r} 0 {int(fraction>.5)},1 {x2},{y2} Z',fill=color)
        element(shape,'title').text=f'{name}: {count:,} bytes ({fraction:.2%})'
        y=55+i*min(35,190/max(len(items)-1,1))
        element(panel,'rect',x=240,y=y-13,width=13,height=13,fill=color)
        label(panel,264,y,f'{name}  {fraction:.2%}',17)
        start=end
    element(panel,'circle',cx=cx,cy=cy,r=54,fill='#000010')
    label(panel,0,256,'All languages shown · excludes forks',14)
    temp=target.with_suffix('.tmp')
    tree.write(temp,encoding='utf-8',xml_declaration=False)
    temp.replace(target)
    print('Updated language panel: '+', '.join(totals))

if __name__=='__main__': main()
