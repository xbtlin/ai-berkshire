"""Build both survey editions and a minimal English arXiv source archive."""
from pathlib import Path
import re, subprocess, shutil, zipfile
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
ARX=ROOT/'arxiv'
OUT=REPO/'output'/'pdf'
TMP=REPO/'tmp'/'pdfs'/'rsi'
OUT.mkdir(parents=True,exist_ok=True); TMP.mkdir(parents=True,exist_ok=True)
def run(args,cwd=ARX):
 p=subprocess.run(args,cwd=cwd,text=True,errors="replace",stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if p.returncode:
  print(p.stdout[-10000:]); raise RuntimeError('Failed: '+' '.join(args))
 return p.stdout

for lang in ('en','zh'):
 name='main' if lang=='en' else 'main-zh'
 run(['pandoc',str(ROOT/('manuscript-'+lang+'.md')),'-f','markdown+raw_tex','-t','latex','--standalone','--natbib','--bibliography=references.bib','--number-sections','--top-level-division=section','-V','documentclass=article','-V','fontsize=11pt','-V','geometry:margin=25mm','-V','biblio-style=unsrtnat','-H',str(ARX/('preamble-'+lang+'.tex')),'-o',name+'.tex'])
 tex=(ARX/(name+'.tex')).read_text()
 # Numeric references save space and allow synchronized citation keys.
 tex=tex.replace(r'\usepackage[]{natbib}',r'\usepackage[numbers,sort&compress]{natbib}')
 tex=tex.replace(r'\bibliographystyle{unsrtnat}',r'\bibliographystyle{unsrtnat}')
 tex=tex.replace(r'\bibliography{references.bib}',r'\clearpage'+'\n'+r'\bibliography{references.bib}')
 (ARX/(name+'.tex')).write_text(tex)
 engine='pdflatex' if lang=='en' else 'xelatex'
 for stage in [0,1,2,3]:
  if stage==1: output=run(['bibtex',name])
  else: output=run([engine,'-interaction=nonstopmode','-halt-on-error','-file-line-error',name+'.tex'])
  (TMP/(name+'-'+str(stage)+'.build.txt')).write_text(output)
 log=(ARX/(name+'.log')).read_text(errors='replace')
 problems=[l for l in log.splitlines() if any(t in l for t in ['Overfull','undefined','Missing character','LaTeX Error'])]
 print(lang,'layout/citation warnings:',problems)
 shutil.copy2(ARX/(name+'.pdf'),OUT/('rsi-survey-'+lang+'-20260906.pdf'))
# Archive only the English paper's inputs, never cached papers or build output.
with zipfile.ZipFile(ROOT/'rsi-survey-arxiv-source.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in ['main.tex','main.bbl','references.bib','figure-loop.tex']:
  z.write(ARX/f,f)
print('Built English and Chinese PDF editions and English source ZIP.')
