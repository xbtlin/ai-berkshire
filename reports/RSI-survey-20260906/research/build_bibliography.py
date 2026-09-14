import json, re, unicodedata
from pathlib import Path
R=Path(__file__).resolve().parent
items=json.loads((R/'sources.json').read_text())
for x in items:
 if 'error' in x: raise RuntimeError(x)
 x['year']=x['date'][:4]
 x['type']='misc'
 x['note']='arXiv preprint; version '+str(x['version'])+' consulted'
 if x['key']=='collapse2023':
  x.update(title='AI models collapse when trained on recursively generated data',year='2024',type='article',journal='Nature',volume='631',pages='755--759',doi='10.1038/s41586-024-07566-y',url='https://www.nature.com/articles/s41586-024-07566-y',note='Corrected version of record consulted; correction DOI: 10.1038/s41586-025-08905-3')
items += [
 {'key':'good1965','title':'Speculations Concerning the First Ultraintelligent Machine','authors':['Good, Irving John'],'year':'1965','type':'incollection','booktitle':'Advances in Computers','volume':'6','pages':'31--88','publisher':'Academic Press','doi':'10.1016/S0065-2458(08)60418-0','url':'https://www.sciencedirect.com/science/article/pii/S0065245808604180','read_depth':'publisher_record','accessed':'2026-09-06'},
 {'key':'funsearch2024','title':'Mathematical discoveries from program search with large language models','authors':['Romera-Paredes, Bernardino','Barekatain, Mohammadamin','Novikov, Alexander','Balog, Matej','Kumar, M. Pawan','Dupont, Emilien','Ruiz, Francisco J. R.','Ellenberg, Jordan S.','Wang, Pengming','Fawzi, Omar','Kohli, Pushmeet','Fawzi, Alhussein'],'year':'2024','type':'article','journal':'Nature','volume':'625','pages':'468--475','doi':'10.1038/s41586-023-06924-6','url':'https://www.nature.com/articles/s41586-023-06924-6','read_depth':'full_text_sections','note':'Published online 14 December 2023','accessed':'2026-09-06'},
 {'key':'surveyliu2026','title':'The Path to Recursive Self-Improving Agents: Foundation, Framework, and Future Directions','authors':['Liu, Shuaiqi','Lin, Zhengkai','Zhang, Yuxiang','Ren, Yuanyi','Wu, Yue','Li, Yongbin','Wang, Zheng','Fu, Zhihang','Ye, Jieping'],'year':'2026','type':'misc','doi':'10.20944/preprints202608.0051.v1','url':'https://www.preprints.org/manuscript/202608.0051','read_depth':'full_text_sections','note':'Preprints.org preprint, version 1','accessed':'2026-09-06'}
]
# BibTeX is ASCII so the same bibliography compiles with pdfLaTeX and XeLaTeX.
acc={'\u0301':"'",'\u0300':'`','\u0302':'^','\u0303':'~','\u0308':'"','\u030c':'v','\u0327':'c','\u0328':'k','\u0304':'=','\u0306':'u','\u0307':'.','\u030b':'H'}
def tex(s):
 s=s.replace('&',r'\&').replace('%',r'\%').replace('_',r'\_')
 s=s.replace('ß',r'{\ss}').replace('ł',r'{\l}').replace('Ł',r'{\L}').replace('ø',r'{\o}').replace('æ',r'{\ae}').replace('’',"'").replace('–','--').replace('—','---')
 n=unicodedata.normalize('NFD',s); out='';i=0
 while i<len(n):
  c=n[i]
  if i+1<len(n) and unicodedata.combining(n[i+1]):
   marks=[];j=i+1
   while j<len(n) and unicodedata.combining(n[j]): marks.append(n[j]);j+=1
   for mark in marks: c='{\\'+acc.get(mark,'')+'{'+c+'}}'
   out+=c;i=j
  else: out+=c;i+=1
 return out
bib=[]
for x in items:
 a=x['authors']
 if len(a)>8: a=a[:6]+['others']
 fields={'title':'{'+tex(x['title'])+'}','author':' and '.join(tex(a0) for a0 in a),'year':x['year']}
 for f in ['journal','booktitle','volume','pages','publisher','note']:
  if x.get(f): fields[f]=tex(x[f])
 for f in ['doi','url']:
  if x.get(f): fields[f]=x[f]
 if x.get('id') and x['type']=='misc': fields.update(eprint=x['id'],archivePrefix='arXiv')
 bib.append('@'+x['type']+'{'+x['key']+',\n'+',\n'.join('  '+k+' = {'+v+'}' for k,v in fields.items())+'\n}\n')
(R.parent/'arxiv'/'references.bib').write_text('\n'.join(bib))
(R/'bibliography_metadata.json').write_text(json.dumps(items,ensure_ascii=False,indent=2))
lines=['# Verified source register','', 'Access date: 2026-09-06. These are selected references, not the yield of an exhaustive systematic search. Bibliographic dates follow the first arXiv posting except when a version of record is cited. Cached full text availability does not mean every appendix was reviewed.','', '| Key | Year | Primary record | Consultation basis |','|---|---|---|---|']
for x in items: lines.append('| '+x['key']+' | '+x['year']+' | ['+x['title'].replace('|','/')+']('+x['url']+') | '+x['read_depth']+' |')
(R/'source_register.md').write_text('\n'.join(lines)+'\n')
print('Verified bibliography records:',len(items))
