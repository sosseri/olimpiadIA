import json
import re

META_PATH = "data/images_metadata.json"
with open(META_PATH, "r", encoding="utf-8") as f:
    meta = json.load(f)

requested = "atletes_francesos_barcelona_olimpiada.jpg"
req_tokens = re.findall(r"[a-z0-9]+", requested.split('.')[0].lower())
req_tokens = [t for t in req_tokens if len(t) > 2]
print('Requested tokens:', req_tokens)

for m in meta:
    fname = m.get('file','')
    if 'atletes' in fname:
        meta_tokens = re.findall(r"[a-z0-9]+", fname.split('.')[0].lower())
        meta_tokens = [t for t in meta_tokens if len(t) > 2]
        overlap = set(req_tokens) & set(meta_tokens)
        print('Meta:', fname)
        print('  tokens:', meta_tokens)
        print('  overlap:', overlap)
        print('  overlap_len:', len(overlap))
