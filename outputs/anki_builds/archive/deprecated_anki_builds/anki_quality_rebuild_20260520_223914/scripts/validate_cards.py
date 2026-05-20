#!/usr/bin/env python3
import csv, json, pathlib, re, sys
root=pathlib.Path(__file__).resolve().parents[1]
cards=list(csv.DictReader(open(root/'25_final_all_cards.csv',encoding='utf-8-sig')))
source=json.load(open(root/'03_source_map.json',encoding='utf-8'))
source_ids={s['source_id'] for s in source}
bad=[]
for c in cards:
    if not c['front'] or not c['back']: bad.append(('empty',c['front']))
    if not c['source_topic_id']: bad.append(('no_topic',c['front']))
    ids=[x for x in c['source_ids'].split(';') if x]
    if not ids or any(x not in source_ids for x in ids): bad.append(('bad_source',c['front']))
    if '这个专题应该怎样转化为 Anki' in c['front']+c['back']+c['extra']: bad.append(('meta',c['front']))
    if c['card_type']=='真题刷题卡':
        if not re.search(r'\nA\. .+\nB\. .+\nC\. .+\nD\. ', c['front'], re.S): bad.append(('bad_options',c['front']))
        if not re.search(r'答案：[A-D]', re.sub(r'<[^>]+>','',c['back'])): bad.append(('bad_answer',c['front']))
if len(cards)!=len({c['checksum'] for c in cards}): bad.append(('checksum_duplicate',''))
print(f'cards={len(cards)} bad={len(bad)}')
for x in bad[:30]: print(x)
sys.exit(1 if bad else 0)
