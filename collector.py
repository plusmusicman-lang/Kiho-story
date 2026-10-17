"""Optional local same-origin collector. Python standard library only."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, unquote
from urllib.request import Request, urlopen
from html.parser import HTMLParser
import json, re

class Extract(HTMLParser):
 def __init__(self):
  super().__init__(); self.parts=[]; self.skip=0; self.foot=[]; self.hidden=[]; self.in_note=0; self.in_hidden=0
 def handle_starttag(self,tag,attrs):
  a=dict(attrs); cls=a.get('class',''); style=a.get('style','').lower()
  if tag in ('script','style','noscript'): self.skip+=1
  if tag in ('p','div','li','tr','h1','h2','h3','h4','br'): self.parts.append('\n')
  if tag=='a' and ('fn-' in a.get('href','') or 'fn-' in a.get('id','')): self.parts.append(' [각주] ')
  if 'footnote' in cls.lower() or re.search(r'\bfn-\d+',a.get('id','')): self.in_note+=1
  if tag in ('details','summary') or 'display:none' in style.replace(' ','') or 'fold' in cls.lower(): self.in_hidden+=1
 def handle_endtag(self,tag):
  if tag in ('script','style','noscript'): self.skip=max(0,self.skip-1)
  if tag in ('details','summary') and self.in_hidden:self.in_hidden-=1
 def handle_data(self,data):
  t=data.strip()
  if not t or self.skip:return
  self.parts.append(t+' ')
  if self.in_note:self.foot.append(t)
  if self.in_hidden:self.hidden.append(t)

class Handler(SimpleHTTPRequestHandler):
 def do_POST(self):
  if self.path!='/api/collect': self.send_error(404);return
  try:
   n=int(self.headers.get('Content-Length','0'))
   if n>20000:raise ValueError('요청이 너무 큽니다')
   u=json.loads(self.rfile.read(n))['url'];p=urlparse(u)
   if p.scheme!='https' or p.hostname not in ('namu.wiki','www.namu.wiki') or not p.path.startswith('/w/') or p.username or p.password or p.port:raise ValueError('나무위키 문서 주소만 허용합니다')
   req=Request(u,headers={'User-Agent':'Mozilla/5.0 (compatible; KIHOResearch/1.1)','Accept':'text/html'})
   with urlopen(req,timeout=18) as resp:
    if urlparse(resp.url).hostname not in ('namu.wiki','www.namu.wiki'):raise ValueError('다른 사이트로 이동되어 수집 중단')
    raw=resp.read(6_000_001)
    if len(raw)>6_000_000:raise ValueError('문서 크기 제한 초과')
    charset=resp.headers.get_content_charset() or 'utf-8'
   html=raw.decode(charset,errors='replace');x=Extract();x.feed(html)
   txt=' '.join(x.parts);txt=re.sub(r'[ \t]+',' ',txt);txt=re.sub(r'\n\s*\n+', '\n',txt).strip()
   if len(txt)<250:raise ValueError('본문이 충분히 추출되지 않았습니다. 접근 제한 또는 동적 렌더링일 수 있습니다.')
   self.reply(200,{'url':u,'text':txt[:450000],'footnotes':' '.join(x.foot)[:90000],'hidden':' '.join(x.hidden)[:90000],'truncated':len(txt)>450000,'warning':'HTML에서 확인된 텍스트만 수집했습니다. 동적 접힘 영역이나 일부 각주는 누락될 수 있습니다.'})
  except Exception as e:self.reply(422,{'error':str(e)})
 def reply(self,code,obj):
  data=json.dumps(obj,ensure_ascii=False).encode();self.send_response(code);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
if __name__=='__main__':
 print('KIHO local collector: http://127.0.0.1:8765');ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
