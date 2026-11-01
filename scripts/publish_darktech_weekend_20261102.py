"""Publish only four approved weekend posts; never touch Upload-Post jobs."""
import json,os,sys,time,urllib.request,urllib.parse,urllib.error
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path("artifacts/darktech-20261102")
STATE=Path("queue/darktech-weekend-20261102.json")
HEALTH=Path("logs/darktech-weekend-health.json")
BASE="https://raw.githubusercontent.com/taap1995-jpg/direitobinario-media/main/"
GRAPH="https://graph.facebook.com/v24.0"
EXPECTED_USER="direitobinario"
uid=os.environ.get("IG_USER_ID","")
token=os.environ.get("IG_ACCESS_TOKEN","")
def now():return datetime.now(timezone.utc).isoformat()
def save(path,value):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n")
def call(method,path,params=None):
 params=dict(params or {});params["access_token"]=token
 for attempt in range(3):
  url=GRAPH+"/"+path
  data=None
  if method=="GET":url+="?"+urllib.parse.urlencode(params)
  else:data=urllib.parse.urlencode(params).encode()
  req=urllib.request.Request(url,data=data,method=method)
  try:
   with urllib.request.urlopen(req,timeout=60) as r:return json.load(r)
  except urllib.error.HTTPError as e:
   if e.code==403 and attempt<2:
    print("HTTP 403; retry in 15 seconds.",flush=True);time.sleep(15);continue
   # Do not emit raw error messages, request URLs, or credentials.
   code=e.code
   raise RuntimeError("Graph API HTTP "+str(code)) from None
  except (TimeoutError,urllib.error.URLError):
   raise RuntimeError("Graph API network failure; reconcile before retrying a mutation.") from None
def identity():
 if not uid or not token:raise RuntimeError("IG_USER_ID/IG_ACCESS_TOKEN ausentes nos secrets do GitHub.")
 user=call("GET",uid,{"fields":"id,username"})
 if user.get("username","").lower()!=EXPECTED_USER:raise RuntimeError("A credencial não corresponde a @direitobinario.")
 return {"id":user["id"],"username":user["username"]}
def validate():
 try:
  user=identity()
  manifest=json.loads((ROOT/"manifest.json").read_text())
  weekend=[p for p in manifest if p["date"][:10] in ("2026-11-07","2026-11-08")]
  assert len(weekend)==4
  for p in weekend:
   for file in p["files"]:
    with urllib.request.urlopen(urllib.request.Request(BASE+file,method="HEAD"),timeout=30) as r:
     if r.status!=200:raise RuntimeError("Mídia indisponível.")
  result={"checked_at":now(),"status":"validated","username":user["username"],"posts":4}
  save(HEALTH,result);print(json.dumps(result));return 0
 except Exception as e:
  result={"checked_at":now(),"status":"blocked","error":str(e)}
  save(HEALTH,result);print(json.dumps(result));return 2
def log(p,status,post_id="",link="",error=""):
 line=f"{now()} | {p['date']} | {p['id']} | post_id={post_id} | {link} | {status}"
 if error:line+=" | "+error
 with open("published_posts.log","a") as f:f.write(line+"\n")
 print(line,flush=True)
def poll(cid):
 for attempt in range(30):
  time.sleep(10)
  status=call("GET",cid,{"fields":"status_code"}).get("status_code")
  if status=="FINISHED":return
  if status in ("ERROR","EXPIRED"):raise RuntimeError("Container "+str(status))
 raise RuntimeError("Container não ficou FINISHED em até 5 minutos.")
def main():
 if "--validate-only" in sys.argv:return validate()
 identity()
 state=json.loads(STATE.read_text())
 clock=datetime.now(timezone.utc)
 due=[p for p in state if p["status"]=="scheduled" and 0 <= (clock-datetime.fromisoformat(p["date"])).total_seconds() <= 2700]
 if not due:print("Nenhum post pendente nesta janela.");return 0
 for p in due:
  p.update(status="processing",started_at=now());save(STATE,state)
  try:
   if p["type"]=="REELS":
    cid=call("POST",uid+"/media",{"media_type":"REELS","video_url":BASE+p["files"][0],"caption":p["caption"],"share_to_feed":"true","cover_url":BASE+p["files"][0].replace("reel.mp4","scene-01.png")})["id"]
   else:
    children=[]
    for file in p["files"]:
     child=call("POST",uid+"/media",{"image_url":BASE+file,"is_carousel_item":"true"})["id"]
     children.append(child)
    p["children"]=children;save(STATE,state)
    cid=call("POST",uid+"/media",{"media_type":"CAROUSEL","children":",".join(children),"caption":p["caption"]})["id"]
    time.sleep(8)
   p["container_id"]=cid;save(STATE,state)
   poll(cid)
   p["status"]="publishing";save(STATE,state)
   # A lost response here must never cause a blind duplicate publication.
   mid=call("POST",uid+"/media_publish",{"creation_id":cid})["id"]
   p["post_id"]=mid;save(STATE,state)
   details=call("GET",mid,{"fields":"id,permalink"})
   p.update(status="published",published_at=now(),permalink=details.get("permalink",""))
   save(STATE,state);log(p,"PUBLICADO",mid,p["permalink"])
  except Exception as e:
   p.update(status="needs_review",error=str(e),failed_at=now())
   save(STATE,state);log(p,"FALHOU",p.get("post_id",""),p.get("permalink",""),str(e));return 2
 return 0
if __name__=="__main__":
 try:sys.exit(main())
 except Exception as e:print("BLOQUEADO: "+str(e));sys.exit(2)
