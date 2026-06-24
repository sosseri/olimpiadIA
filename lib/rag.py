import json
import re
import os

_CHUNKS_CACHE = None
_IMAGES_CACHE = None


def _load_chunks():
    global _CHUNKS_CACHE
    if _CHUNKS_CACHE is None:
        path = os.path.join(os.path.dirname(__file__), "..", "data", "olimpiada_chunks.json")
        with open(path, "r", encoding="utf-8") as f:
            _CHUNKS_CACHE = json.load(f)
        img_chunks = _build_image_chunks()
        _CHUNKS_CACHE = _CHUNKS_CACHE + img_chunks
    return _CHUNKS_CACHE


def _load_images():
    global _IMAGES_CACHE
    if _IMAGES_CACHE is None:
        path = os.path.join(os.path.dirname(__file__), "..", "data", "images_metadata.json")
        with open(path, "r", encoding="utf-8") as f:
            _IMAGES_CACHE = json.load(f)
    return _IMAGES_CACHE


def _build_image_chunks():
    images = _load_images()
    chunks = []
    for img in images:
        fname = img["file"]
        caption = img["caption"]
        source = img.get("source_site", "")
        # derive keywords from filename and caption
        words = re.findall(r'\w+', (fname + " " + caption).lower())
        keywords = list({w for w in words if len(w) > 3})
        chunks.append({
            "id": f"img_{fname}",
            "category": "olimpiada",
            "keywords": keywords,
            "title": f"Imatge: {caption}",
            "text": f"Hi ha una fotografia disponible: {caption} (Font: {source}). "
                    f"Pots mostrar-la amb [IMATGE:{fname}]",
            "image_file": fname,
            "is_image": True,
        })
    return chunks


def _score(chunk, query):
    q = query.lower()
    words = re.findall(r'\w+', q)
    score = 0
    for kw in chunk.get("keywords", []):
        if kw in q:
            score += 3
    for w in words:
        if len(w) > 3:
            text = (chunk["title"] + " " + chunk["text"]).lower()
            if w in text:
                score += 1
    return score


def retrieve(query, top_k=3):
    chunks = _load_chunks()
    scored = [(c, _score(c, query)) for c in chunks]
    scored.sort(key=lambda x: x[1], reverse=True)
    top = [c for c, s in scored[:top_k] if s > 0]
    return top


def format_context(chunks):
    if not chunks:
        return ""
    lines = []
    for c in chunks:
        lines.append(f"### {c['title']}\n{c['text']}")
    return "\n\n".join(lines)
