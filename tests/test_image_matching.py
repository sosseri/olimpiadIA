import json
import re

META_PATH = "data/images_metadata.json"

with open(META_PATH, "r", encoding="utf-8") as f:
    meta = json.load(f)


def find_best_image_filename(requested: str, meta_list):
    tokens_req = re.findall(r"[a-z0-9]+", requested.split(".")[0].lower())
    tokens_req = [t for t in tokens_req if len(t) > 2]
    if not tokens_req:
        return None
    best = None
    best_score = 0
    for m in meta_list:
        fname = m.get("file", "")
        tokens_meta = re.findall(r"[a-z0-9]+", fname.split(".")[0].lower())
        tokens_meta = [t for t in tokens_meta if len(t) > 2]
        if not tokens_meta:
            continue
        overlap = len(set(tokens_req) & set(tokens_meta))
        if overlap > best_score:
            best_score = overlap
            best = fname
    return best if best_score > 0 else None


samples = [
    "atletes_francesos_barcelona_olimpiada.jpg",
    "atletes_francesos_olimpiada.jpg",
    "atletes_francesos.jpg",
    "atletes_francesos_estacio.jpg",
    "atletes_francesos_barcelona.jpg",
    "vpa_olimpiada_popular_beteve.jpg",
    "vpa_olimpiada.jpg",
    "programa_olimpiada_popular_barcelona_arxiu.jpg",
]

for s in samples:
    match = find_best_image_filename(s, meta)
    print(f"Requested: {s} -> Matched: {match}")
