#!/usr/bin/env python3
"""Combine locally hosted animations and external links into catalog.json."""
from pathlib import Path
from html import unescape
from urllib.parse import urlsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ANIM = ROOT / 'animations'
LABELS = {'physics':'物理','chemistry':'化學','earth':'地球科學','biology':'生物','math':'數學','other':'其他'}
RULES = {
 'physics':['力學','速度','加速度','齒輪','槓桿','電路','電流','光學','折射','聲波','f1','physics','gear','motion','force'],
 'chemistry':['化學','元素','原子','分子','酸鹼','反應','chemistry','atom','molecule'],
 'earth':['地球','板塊','地震','太陽系','月球','重力軌跡','天文','氣象','earth','solar','space','planet'],
 'biology':['生物','細胞','人體','遺傳','生態','光合作用','biology','cell','dna'],
 'math':['三角形','幾何','角度','函數','數學','triangle','geometry','math']
}
def guess(text):
 t=text.lower(); scores={k:sum(w.lower() in t for w in ws) for k,ws in RULES.items()}
 return max(scores,key=scores.get) if max(scores.values(),default=0)>0 else 'other'
def title_from_html(p):
 try:
  head=p.read_text(encoding='utf-8',errors='replace')[:20000]
  m=re.search(r'<title[^>]*>(.*?)</title>',head,re.I|re.S)
  if m:return re.sub(r'\s+',' ',unescape(re.sub('<[^>]+>','',m.group(1)))).strip()
 except OSError:pass
 return p.stem.replace('_',' ').replace('-',' ')
def load_json(path):
 return json.loads(path.read_text(encoding='utf-8'))
def main():
 entries=[]
 if ANIM.exists():
  for p in sorted(ANIM.rglob('*.html')):
   if p.name.lower()!='index.html' and (p.parent/'index.html').exists():continue
   meta_path=p.parent/'metadata.json' if p.name.lower()=='index.html' else p.with_suffix('.json')
   meta=load_json(meta_path) if meta_path.exists() else {}
   if not isinstance(meta,dict):raise ValueError(f'{meta_path}: metadata must be object')
   title=str(meta.get('title') or title_from_html(p))
   category=meta.get('category') or guess(title+' '+str(p.parent))
   if category not in LABELS:category='other'
   entries.append({'title':title,'category':category,'categoryLabel':LABELS[category],
    'topic':str(meta.get('topic') or '互動探索'),
    'description':str(meta.get('description') or '透過互動動畫探索科學概念。'),
    'tags':meta.get('tags',[]) if isinstance(meta.get('tags',[]),list) else [],
    'icon':str(meta.get('icon') or ''),'source':'local',
    'url':p.relative_to(ROOT).as_posix()})
 external_file=ROOT/'external-links.json'
 external=load_json(external_file) if external_file.exists() else []
 if not isinstance(external,list):raise ValueError('external-links.json must contain an array')
 for i,meta in enumerate(external,1):
  if not isinstance(meta,dict):raise ValueError(f'external link {i} must be an object')
  url=str(meta.get('url') or '').strip()
  parsed=urlsplit(url)
  if parsed.scheme!='https' or not parsed.netloc or parsed.username or parsed.password:
   raise ValueError(f'external link {i}: use an absolute https URL')
  title=str(meta.get('title') or '').strip()
  if not title:raise ValueError(f'external link {i}: title required')
  category=meta.get('category') or guess(title)
  if category not in LABELS:category='other'
  entries.append({'title':title,'category':category,'categoryLabel':LABELS[category],
   'topic':str(meta.get('topic') or '外部教學資源'),
   'description':str(meta.get('description') or '前往原作者網站探索。'),
   'tags':meta.get('tags',[]) if isinstance(meta.get('tags',[]),list) else [],
   'icon':str(meta.get('icon') or ''),'source':'external',
   'author':str(meta.get('author') or ''),'url':url})
 (ROOT/'catalog.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(f'已產生 catalog.json：本站 {sum(x["source"]=="local" for x in entries)} 筆、外部 {sum(x["source"]=="external" for x in entries)} 筆')
if __name__=='__main__':main()
