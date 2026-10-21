import json, os, sys, time, urllib.parse, urllib.request
from datetime import datetime, timezone

GRAPH = "https://graph.facebook.com/v21.0"
QUEUE = "queue/posts.json"


def load():
    with open(QUEUE, encoding="utf-8") as f:
        return json.load(f)


def save(q):
    with open(QUEUE, "w", encoding="utf-8") as f:
        json.dump(q, f, ensure_ascii=False, indent=2)
        f.write("\n")


def call(method, path, params):
    params = dict(params)
    if method == "GET":
        url = f"{GRAPH}/{path}?" + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, method="GET")
    else:
        data = urllib.parse.urlencode(params).encode()
        req = urllib.request.Request(f"{GRAPH}/{path}", data=data, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def main():
    uid = os.environ.get("IG_USER_ID")
    tok = os.environ.get("IG_ACCESS_TOKEN")
    if not uid or not tok:
        print("Segredos IG_USER_ID/IG_ACCESS_TOKEN ausentes. Nada foi publicado.")
        return 0

    q = load()
    now = datetime.now(timezone.utc)
    due = [p for p in q if p.get("status") == "approved"
           and datetime.fromisoformat(p["scheduled_for"]) <= now]
    if not due:
        print("Nenhum post aprovado e vencido.")
        return 0

    post = min(due, key=lambda p: p["scheduled_for"])
    post["status"] = "publishing"
    save(q)  # marca antes da chamada para nunca publicar duas vezes
    try:
        c = call("POST", f"{uid}/media", {"image_url": post["image_url"],
                                          "caption": post["caption"],
                                          "access_token": tok})
        cid = c["id"]
        for _ in range(20):
            s = call("GET", cid, {"fields": "status_code", "access_token": tok}).get("status_code")
            if s == "FINISHED":
                break
            if s in ("ERROR", "EXPIRED"):
                raise RuntimeError(f"container {s}")
            time.sleep(5)
        else:
            raise RuntimeError("container não ficou pronto no prazo")
        m = call("POST", f"{uid}/media_publish", {"creation_id": cid, "access_token": tok})
        mid = m["id"]
        perm = call("GET", mid, {"fields": "permalink", "access_token": tok}).get("permalink")
        post.update(status="published", ig_media_id=mid, permalink=perm, error=None)
        print("Publicado:", perm)
    except Exception as e:
        post.update(status="error", error=str(e))
        print("Erro (não será repetido automaticamente):", e)
    finally:
        save(q)
    return 0


if __name__ == "__main__":
    sys.exit(main())
