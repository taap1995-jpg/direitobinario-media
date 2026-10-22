import json, os, re, sys, time, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone
from urllib.parse import urlparse

GRAPH = "https://graph.facebook.com/v21.0"
QUEUE = "queue/posts.json"
EXPECTED_USER = os.environ.get("EXPECTED_IG_USER_ID", "39241822288794396")
MIN_QA_SCORE = 8

def load():
    with open(QUEUE, encoding="utf-8") as f:
        q = json.load(f)
    if not isinstance(q, list):
        raise RuntimeError("Fila inválida: queue/posts.json deve conter uma lista.")
    return q

def save(q):
    with open(QUEUE, "w", encoding="utf-8") as f:
        json.dump(q, f, ensure_ascii=False, indent=2)
        f.write("\n")

def call(method, path, params):
    params = dict(params)
    if method == "GET":
        req = urllib.request.Request(f"{GRAPH}/{path}?" + urllib.parse.urlencode(params), method="GET")
    else:
        req = urllib.request.Request(f"{GRAPH}/{path}", data=urllib.parse.urlencode(params).encode(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Instagram Graph API retornou HTTP {e.code} em {path}. Verifique credencial e permissões.") from None

def validate_media(post):
    url = post.get("image_url", "")
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname != "raw.githubusercontent.com":
        raise RuntimeError("Mídia bloqueada: image_url precisa ser HTTPS público no raw.githubusercontent.com.")
    if parsed.query or parsed.fragment or not parsed.path.lower().endswith((".jpg", ".jpeg", ".png")):
        raise RuntimeError("Mídia bloqueada: URL deve ser direta, sem query/fragmento e apontar para JPG/PNG.")
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "direitobinario-publisher/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            mime = response.headers.get_content_type()
            size = int(response.headers.get("Content-Length", "0") or "0")
            if response.status != 200 or mime not in ("image/jpeg", "image/png") or size <= 0:
                raise RuntimeError(f"Mídia bloqueada: resposta inválida (HTTP {response.status}, tipo {mime}, bytes {size}).")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Mídia bloqueada: URL pública respondeu HTTP {e.code}.") from None

def validate_post(post, now):
    if not post.get("id") or not post.get("caption", "").strip():
        raise RuntimeError("Post sem ID ou legenda.")
    try:
        scheduled = datetime.fromisoformat(post["scheduled_for"])
    except (KeyError, TypeError, ValueError):
        raise RuntimeError("Post sem scheduled_for válido em ISO 8601.") from None
    if scheduled.tzinfo is None:
        raise RuntimeError("scheduled_for precisa conter fuso horário explícito.")
    if scheduled.astimezone(timezone.utc) > now:
        raise RuntimeError("Post ainda não venceu.")
    if post.get("qa_score", 0) < MIN_QA_SCORE:
        raise RuntimeError(f"Post bloqueado: qa_score precisa ser >= {MIN_QA_SCORE}.")
    if not isinstance(post.get("sources"), list) or not post["sources"]:
        raise RuntimeError("Post bloqueado: inclua sources (fontes verificáveis) antes de aprovar.")
    if post.get("approval_status") != "ready":
        raise RuntimeError("Post bloqueado: approval_status deve ser 'ready' após passar pelos gates de qualidade.")
    validate_media(post)

def main():
    uid = os.environ.get("IG_USER_ID")
    tok = os.environ.get("IG_ACCESS_TOKEN")
    if not uid or not tok:
        print("BLOQUEADO: secrets IG_USER_ID/IG_ACCESS_TOKEN ausentes.", file=sys.stderr)
        return 2
    if uid != EXPECTED_USER:
        print("BLOQUEADO: IG_USER_ID não corresponde à conta @direitobinario configurada.", file=sys.stderr)
        return 2
    q = load()
    now = datetime.now(timezone.utc)
    due = [p for p in q if p.get("status") == "approved"]
    due.sort(key=lambda p: p.get("scheduled_for", ""))
    if not due:
        print("Nenhum post com status approved na fila.")
        return 0
    post = due[0]
    try:
        validate_post(post, now)
    except Exception as e:
        print(f"BLOQUEADO ({post.get('id', 'sem-id')}): {e}", file=sys.stderr)
        return 2
    post["status"] = "publishing"
    post["publish_started_at"] = now.isoformat()
    save(q)
    try:
        c = call("POST", f"{uid}/media", {
            "image_url": post["image_url"], "caption": re.sub(r"%23", "#", post["caption"], flags=re.IGNORECASE), "access_token": tok
        })
        cid = c["id"]
        post["container_id"] = cid
        save(q)
        for _ in range(20):
            s = call("GET", cid, {"fields": "status_code", "access_token": tok}).get("status_code")
            print("Status do container:", s)
            if s == "FINISHED":
                break
            if s in ("ERROR", "EXPIRED"):
                raise RuntimeError(f"container {s}")
            time.sleep(5)
        else:
            raise RuntimeError("container não ficou pronto no prazo; verificar estado antes de nova tentativa")
        m = call("POST", f"{uid}/media_publish", {"creation_id": cid, "access_token": tok})
        mid = m["id"]
        details = call("GET", mid, {"fields": "permalink", "access_token": tok})
        perm = details.get("permalink")
        if not perm:
            raise RuntimeError("API não retornou permalink; reconciliar estado antes de repetir.")
        post.update(status="published", ig_media_id=mid, permalink=perm,
                    published_at=datetime.now(timezone.utc).isoformat(), error=None)
        print("PUBLICADO:", perm)
        save(q)
        return 0
    except Exception as e:
        post.update(status="error", error=str(e), last_attempt_at=datetime.now(timezone.utc).isoformat())
        save(q)
        print(f"FALHA ({post.get('id')}): {e}. Não repetir automaticamente; reconciliar no Instagram antes de tentar novamente.", file=sys.stderr)
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"FALHA DE PRÉ-EXECUÇÃO: {exc}", file=sys.stderr)
        sys.exit(1)
