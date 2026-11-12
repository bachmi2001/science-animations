#!/usr/bin/env python3
"""掃描 animations 下的 HTML，依可選 metadata.json 產生 catalog.json。僅用標準函式庫。"""
from pathlib import Path
import json, re
from html import unescape

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
 t=text.lower();scores={k:sum(1 for w in ws if w.lower() in t) for k,ws in RULES.items()}
 return max(scores,key=scores.get) if max(scores.values(),default=0)>0 else 'other'
def title_from_html(p):
 try:
  head=p.read_text(encoding='utf-8',errors='replace')[:20000]
  m=re.search(r'<title[^>]*>(.*?)</title>',head,re.I|re.S)
  if m:return re.sub(r'\s+',' ',unescape(re.sub('<[^>]+>','',m.group(1)))).strip()
 except OSError:pass
 return p.stem.replace('_',' ').replace('-',' ')
def main():
 entries=[]
 for p in sorted(ANIM.rglob('*.html')):
  if p.name.lower()!='index.html' and (p.parent/'index.html').exists():continue
  meta_path=p.parent/'metadata.json' if p.name.lower()=='index.html' else p.with_suffix('.json')
  meta={}
  if meta_path.exists():
   try:meta=json.loads(meta_path.read_text(encoding='utf-8'))
   except (OSError,ValueError) as e:print(f'警告：{meta_path} 無法讀取：{e}')
  title=str(meta.get('title') or title_from_html(p));category=meta.get('category') or guess(title+' '+str(p.parent))
  if category not in LABELS:category='other'
  entry={'title':title,'category':category,'categoryLabel':LABELS[category],
   'topic':str(meta.get('topic') or '互動探索'),
   'description':str(meta.get('description') or '透過互動動畫探索科學概念。'),
   'tags':meta.get('tags',[]) if isinstance(meta.get('tags',[]),list) else [],
   'icon':str(meta.get('icon') or ''),
   'url':p.relative_to(ROOT).as_posix()}
  entries.append(entry)
 out=ROOT/'catalog.json';out.write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(f'已產生 {out}，共 {len(entries)} 個動畫')
if __name__=='__main__':main()
