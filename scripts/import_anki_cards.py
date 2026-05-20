#!/usr/bin/env python3
import argparse, csv, json, urllib.request
URL="http://127.0.0.1:8765"
MODEL_FIELDS=["Front","Back","Extra","SourceTopicID","SourceTopicName","SourceFile","KnowledgeDomain","CardType","Importance","ExamUse","RelatedQuestionIDs","TagsText","Checksum"]
def call(action, **params):
    data=json.dumps({"action":action,"version":6,"params":params}).encode()
    req=urllib.request.Request(URL,data=data,headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=20) as r:
        res=json.loads(r.read())
    if res.get("error"):
        raise RuntimeError(res["error"])
    return res.get("result")
def note_from(row):
    return {
        "deckName": row["Deck"],
        "modelName": "RuankaoTopicCard",
        "fields": {k: row.get(k,"") for k in MODEL_FIELDS},
        "tags": row.get("TagsText","").split(),
        "options": {"allowDuplicate": False, "duplicateScope": "deck"},
    }
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--dry-run", action="store_true")
    args=ap.parse_args()
    rows=list(csv.DictReader(open(args.csv_path,encoding="utf-8-sig")))
    notes=[note_from(r) for r in rows if r.get("QualityStatus")=="final"]
    print(f"notes ready: {len(notes)}")
    if args.dry_run:
        print(json.dumps(notes[:3],ensure_ascii=False,indent=2))
        return
    for deck in sorted({n["deckName"] for n in notes}):
        call("createDeck", deck=deck)
    added=call("addNotes", notes=notes)
    ok=sum(1 for x in added if x)
    print(f"added: {ok}; failed/skipped: {len(added)-ok}")
if __name__=="__main__":
    main()
