"""Static files and Nginx HTTP resource checks; does not control or render a browser."""
from html.parser import HTMLParser
from pathlib import Path
import os
import re
import urllib.error
import urllib.request

root=Path(__file__).resolve().parents[1]/'frontend'
base=os.environ.get('TEST_WEB_URL','http://127.0.0.1:18081')
checks=0
class PageParser(HTMLParser):
    def __init__(self):super().__init__();self.refs=[];self.page=None;self.language=None
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='html':self.language=attrs.get('lang')
        if tag=='body':self.page=attrs.get('data-page')
        if tag in ('script','link'):
            ref=attrs.get('src') or attrs.get('href')
            if ref:self.refs.append(ref)

for file in root.rglob('*'):
    if not file.is_file():continue
    route='/'+file.relative_to(root).as_posix()
    with urllib.request.urlopen(base+route,timeout=5) as response:
        data=response.read()
        assert response.status==200 and data==file.read_bytes(),route+' served content mismatch'
        assert response.headers.get('Server','').startswith('nginx/'),route+' is not served by nginx'
        if file.suffix=='.js':assert 'javascript' in response.headers['Content-Type']
        if file.suffix=='.css':assert 'text/css' in response.headers['Content-Type']
        if file.suffix=='.html':assert 'text/html' in response.headers['Content-Type']
    checks+=1
    if file.suffix=='.html':
        parser=PageParser();parser.feed(file.read_text(encoding='utf-8'))
        assert parser.language=='zh-CN' and parser.page,route+' missing document metadata'
        for ref in parser.refs:assert (root/ref.split('?')[0].lstrip('/')).is_file(),route+' broken dependency '+ref
        checks+=1
    if file.suffix=='.js':
        for ref in re.findall(r"(?:from\s*|import\()\s*['\"]([^'\"]+)['\"]",file.read_text(encoding='utf-8')):
            assert (file.parent/ref.split('?')[0]).is_file(),route+' broken module import '+ref
        checks+=1

for route in ['/missing-page.html','/assets/js/missing.js']:
    try:urllib.request.urlopen(base+route);raise AssertionError('Missing resource should return 404')
    except urllib.error.HTTPError as error:assert error.code==404
    checks+=1

# This is a transport/authorization check, not a browser interaction.
try:urllib.request.urlopen(base+'/api/courses');raise AssertionError('API must require authorization')
except urllib.error.HTTPError as error:assert error.code==401
checks+=1
print(f'PASS: {checks} static-source and Nginx HTTP checks. Browser rendering is not tested.')
