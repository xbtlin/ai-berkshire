"""Save public official model cards and licenses, without downloading weights."""
import concurrent.futures
import json
from pathlib import Path
import re
import sys
import subprocess

OUT = Path(__file__).parent

def fetch(repo):
    stem = repo.replace('/', '__')
    result = {'repo': repo, 'url': 'https://huggingface.co/' + repo}
    for filename in ('README.md', 'LICENSE'):
        url = f'https://huggingface.co/{repo}/raw/main/{filename}'
        try:
            response = subprocess.run(['curl', '-L', '--max-time', '25', '-sS', '-w', '\n%{http_code}', url], capture_output=True, text=True, check=True)
            body, status = response.stdout.rsplit('\n', 1)
            result[filename + '_status'] = int(status)
            if status == '200':
                (OUT / (stem + '__' + filename)).write_text(body)
                if filename == 'README.md':
                    result['excerpts'] = [line[:700] for line in body.splitlines()
                        if re.search(r'license:|parameters|parameter count|total.*active|active.*total|context.*(?:[0-9]|million)|commercial|non-commercial', line, re.I)][:18]
                else:
                    result['license_head'] = body[:450]
        except (subprocess.SubprocessError, ValueError) as exc:
            result[filename + '_error'] = str(exc)
    return result

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as pool:
        for item in pool.map(fetch, sys.argv[1:]):
            (OUT / (item['repo'].replace('/', '__') + '.json')).write_text(json.dumps(item, ensure_ascii=False, indent=2))
            print(json.dumps(item, ensure_ascii=False))
