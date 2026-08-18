import os
import json
import requests


def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    meta_path = os.path.join(repo_root, "data", "images_metadata.json")
    out_dir = os.path.join(repo_root, "assets", "images")
    os.makedirs(out_dir, exist_ok=True)

    with open(meta_path, "r", encoding="utf-8") as f:
        metas = json.load(f)

    results = []
    for m in metas:
        fname = m.get("file")
        url = m.get("source_url")
        if not fname:
            results.append((None, "no-filename", None))
            continue
        out_path = os.path.join(out_dir, fname)
        if os.path.isfile(out_path):
            results.append((fname, "exists", out_path))
            continue
        if not url:
            results.append((fname, "no-source-url", None))
            continue
        try:
            print(f"Downloading {fname} from {url}...")
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200 and resp.content:
                with open(out_path, "wb") as out_f:
                    out_f.write(resp.content)
                results.append((fname, "downloaded", out_path))
            else:
                results.append((fname, f"http-{resp.status_code}", url))
        except Exception as e:
            results.append((fname, "error", str(e)))

    print("\nSummary:\n")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
