"""Outline Orbitron headings so they render without external font loading.

Install scripts/requirements-art.txt before rebuilding profile artwork.
The font's SIL Open Font License is retained in assets/fonts/OFL.txt.
"""
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

def main():
    font=instantiateVariableFont(TTFont('assets/fonts/Orbitron.ttf'),{'wght':500},inplace=True)
    glyphs=font.getGlyphSet()
    cmap=font.getBestCmap()
    scale=14/font['head'].unitsPerEm
    for word in ('activity','about'):
        label='~/'+word
        names=[cmap[ord(c)] for c in label]
        width=sum(glyphs[name].width for name in names)*scale
        x=(740-width)/2
        paths=[]
        for name in names:
            pen=SVGPathPen(glyphs)
            glyphs[name].draw(TransformPen(pen,(scale,0,0,-scale,x,19)))
            paths.append(pen.getCommands())
            x+=glyphs[name].width*scale
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="740" height="28" viewBox="0 0 740 28"><title>{label}</title><path fill="#8ed8f8" d="'+ ' '.join(paths)+'"/></svg>'
        Path(f'assets/{word}-orbitron.svg').write_text(svg,encoding='utf-8')
        print('Built Orbitron heading:',label)

if __name__=='__main__':
    main()
