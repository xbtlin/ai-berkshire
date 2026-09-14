"""Fetch primary arXiv metadata and cache selected full texts for this survey.

Uses only the Python standard library. Cached pages are research inputs, not
part of the arXiv submission package. Re-running skips successful fetches.
"""
import concurrent.futures
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parent
PAPERS = {
    'goedel2003': 'cs/0309048',
    'learnoptimizer2016': '1606.04474',
    'alphazero2017': '1712.01815',
    'poet2019': '1901.01753',
    'automlzero2020': '2003.03384',
    'star2022': '2203.14465',
    'selfinstruct2022': '2212.10560',
    'selfrefine2023': '2303.17651',
    'reflexion2023': '2303.11366',
    'voyager2023': '2305.16291',
    'toolformer2023': '2302.04761',
    'stop2023': '2310.02304',
    'selfreward2024': '2401.10020',
    'spin2024': '2401.01335',
    'adas2024': '2408.08435',
    'goedelagent2024': '2410.04444',
    'scientist2024': '2408.06292',
    'scientistv22025': '2504.08066',
    'sica2025': '2504.15228',
    'dgm2025': '2505.22954',
    'alphaevolve2025': '2506.13131',
    'seal2025': '2506.10943',
    'gepa2025': '2507.19457',
    'azr2025': '2505.03335',
    'rzero2025': '2508.05004',
    'hgm2025': '2510.21614',
    'r12025': '2501.12948',
    'swebench2023': '2310.06770',
    'mlebench2024': '2410.07095',
    'rebench2024': '2411.15114',
    'evalplus2023': '2305.01210',
    'judge2023': '2306.05685',
    'intrinsic2023': '2310.01798',
    'intrinsicpositive2024': '2406.15673',
    'score2024': '2409.12917',
    'collapse2023': '2305.17493',
    'accumulate2024': '2404.01413',
    'rewardoveropt2022': '2210.10760',
    'adaptive2015': '1411.2664',
    'tampering2019': '1908.04734',
    'surveygao2025': '2507.21046',
    'surveyfang2025': '2508.07407',
    'surveychen2026': '2607.07663',
    'surveyren2026': '2607.13104',
    'surveycoding2026': '2608.03392',
    'selfedit2026': '2601.14532',
    'pastbench2026': '2608.04003',
    'rsidata2026': '2607.25886',
    'ai4ai2026': '2608.20318',
    'posttrain2026': '2603.08640',
}
FULL = {'goedel2003','stop2023','dgm2025','hgm2025','sica2025','seal2025',
        'azr2025','rzero2025','alphaevolve2025','selfedit2026',
        'pastbench2026','rsidata2026','ai4ai2026','posttrain2026','surveychen2026','surveyren2026'}

class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.meta = {}
        self.parts = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta' and attrs.get('name','').startswith('citation_'):
            self.meta.setdefault(attrs['name'],[]).append(attrs.get('content',''))
        if tag in ('script','style'): self.skip += 1
        if tag in ('p','div','section','h1','h2','h3','h4','li','tr'): self.parts.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script','style'): self.skip = max(0,self.skip-1)
    def handle_data(self, data):
        if not self.skip: self.parts.append(data)

def download(url, path):
    if path.exists(): return path.read_text()
    req = urllib.request.Request(url, headers={'User-Agent':'RSI literature review metadata retrieval'})
    with urllib.request.urlopen(req, timeout=40) as res:
        body = res.read().decode('utf-8')
    path.write_text(body)
    return body

def fetch(pair):
    key, ident = pair
    try:
        body = download('https://arxiv.org/abs/'+ident, ROOT/(key+'-'+ident.replace('/','_')+'.abs.html'))
        p = Parser(); p.feed(body)
        m = p.meta
        if not m.get('citation_title'): raise ValueError('Missing title metadata')
        version = re.findall(r'\[v(\d+)\]', body)
        latest = max(map(int, version),default=1)
        out = {'key':key,'id':ident,'url':'https://arxiv.org/abs/'+ident,
               'title':m['citation_title'][0], 'authors':m.get('citation_author',[]),
               'date':m.get('citation_date',[''])[0],
               'abstract':m.get('citation_abstract',[''])[0],
               'version':latest, 'accessed':'2026-09-06', 'read_depth':'abstract'}
        if key in FULL:
            try:
                full_url='https://arxiv.org/html/'+ident+'v'+str(latest)
                full=download(full_url,ROOT/(key+'.full.html'))
                f=Parser(); f.feed(full)
                txt=re.sub(r'\n[ \t\n]+','\n',''.join(f.parts))
                (ROOT/(key+'.full.txt')).write_text(txt)
                out['fulltext_url']=full_url
                out['read_depth']='full_text_available'
            except Exception as e: out['fulltext_error']=str(e)
        return out
    except Exception as e:
        return {'key':key,'id':ident,'error':str(e)}

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results=list(pool.map(fetch, PAPERS.items()))
    (ROOT/'sources.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
    for r in results:
        print(r['key'],r.get('date',''),r.get('version',''),r.get('title',r.get('error')),r.get('read_depth',''))
