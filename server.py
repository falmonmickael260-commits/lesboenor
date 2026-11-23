import hmac, json, os, re, sqlite3, unicodedata
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from questions import boards

ROOT = Path(__file__).resolve().parent
directory = Path(os.getenv("RAILWAY_VOLUME_MOUNT_PATH") or os.getenv("DATA_DIR", ROOT/"data"))
directory.mkdir(parents=True, exist_ok=True)
db = directory/"plateau.sqlite3"
secret = os.environ.get("HOST_KEY", "")
if len(secret) < 12:
    raise SystemExit("Définissez HOST_KEY avec au moins 12 caractères.")
def fresh():
    return dict(i=0,team=None,phase="start",found=[],pot=0,errors=0,scores=[0,0],history=[],msg="Choisissez l’équipe qui prend la main.")
with sqlite3.connect(db) as c:
    c.execute("CREATE TABLE IF NOT EXISTS game(id INTEGER PRIMARY KEY, rev INTEGER, body TEXT)")
    c.execute("INSERT OR IGNORE INTO game VALUES(1,0,?)",(json.dumps(fresh()),))

teams=["Bleus","Rouges"]
def norm(s):
    s=unicodedata.normalize("NFKD",s.lower().replace("œ","oe"))
    words=re.findall("[a-z0-9]+","".join(c for c in s if not unicodedata.combining(c)))
    return " ".join(w for w in words if w not in {"le","la","les","un","une","des","du","de","d","l","je","j","mon","ma","mes","au","a","en"})
def close(a,b):
    if a==b: return True
    if min(len(a),len(b))<5 or abs(len(a)-len(b))>1: return False
    if len(a)==len(b): return sum(x!=y for x,y in zip(a,b))==1
    short,long=sorted((a,b),key=len)
    return any(long[:i]+long[i+1:]==short for i in range(len(long)))
def public(s,rev):
    rosters=s.get("rosters",[[],[]])
    duel=[names[s["i"]%len(names)] if names else None for names in rosters]
    q=boards[s["i"]]
    slots=[]
    for i,(label,pts,_) in enumerate(q["rows"]):
        rank=1+sum(p>pts for _,p,_ in q["rows"])
        slots.append(dict(rank=rank,label=label,pts=pts) if i in s["found"] else None)
    return {**s,"rosters":rosters,"duel":duel,"slots":slots,"question":q["question"],"source":q["source"] if s["phase"]=="end" else [q["source"][0]],"rev":rev,"total":len(boards)}
def finish(s,winner,stolen):
    s["scores"][winner]+=s["pot"]
    outcome=("Vol réussi" if stolen else "Manche remportée")+f' · {teams[winner]} +{s["pot"]} points'
    s["history"].append(outcome)
    s.update(phase="end",msg=outcome)
def act(s,a):
    phase=s["phase"]
    op=a.get("op")
    if op=="rosters" and phase=="start":
        groups=a.get("rosters")
        if not isinstance(groups,list) or len(groups)!=2: raise ValueError()
        for names in groups:
            if not isinstance(names,list) or not 1<=len(names)<=30: raise ValueError()
            if any(not isinstance(n,str) or not 1<=len(n.strip())<=40 for n in names): raise ValueError()
        s["rosters"]=[[n.strip() for n in names] for names in groups]
    elif op=="start" and phase=="start" and a.get("team") in (0,1):
        s.update(team=a["team"],phase="play",msg="Lisez la question, puis saisissez la première réponse.")
    elif op=="next" and phase=="end":
        if s["i"]==len(boards)-1: return {**fresh(),"rosters":s.get("rosters",[[],[]])}
        s.update(i=s["i"]+1,team=None,phase="start",found=[],pot=0,errors=0,msg="Choisissez l’équipe qui prend la main.")
    elif op=="retry" and phase=="review":
        s.update(phase=s.pop("previous"),msg="Demandez une précision, puis reformulez la réponse.")
    elif op=="miss" and phase=="review":
        prev=s.pop("previous")
        if prev=="steal": finish(s,s["team"],False)
        else:
            s["errors"]+=1
            steal=s["errors"]==3
            s.update(phase="steal" if steal else "play",msg=("Tentative de vol des "+teams[1-s["team"]] if steal else "Hors du tableau · une erreur."))
    elif op=="answer" and phase in ("play","steal"):
        raw=a.get("value","")
        if not isinstance(raw,str) or not 0<len(raw.strip())<=180: raise ValueError()
        v=norm(raw)
        rows=boards[s["i"]]["rows"]
        matches=[i for i,(label,_,alts) in enumerate(rows) if any(close(v,norm(t)) for t in [label,*alts.split("|")])]
        if len(matches)!=1:
            s.update(previous=phase,phase="review",msg=f'« {raw.strip()} » · Aucune correspondance certaine. Précisez ou comptez une erreur.')
        elif matches[0] in s["found"]:
            s["msg"]="Déjà trouvée · reformulez ou proposez une autre réponse."
        else:
            i=matches[0]
            label,pts,_=rows[i]
            rank=1+sum(p>pts for _,p,_ in rows)
            s["found"].append(i)
            s["pot"]+=pts
            s["msg"]=f'{label} · '+("Top réponse !" if rank==1 else f'Nº {rank}')+f' · +{pts} points'
            if phase=="steal" or len(s["found"])==len(rows):
                result=s["msg"]
                finish(s,1-s["team"] if phase=="steal" else s["team"],phase=="steal")
                s["msg"]=result+" — "+s["msg"]
    else: raise ValueError()
    return s

class Handler(BaseHTTPRequestHandler):
    def send(self,status,data,kind="application/json"):
        if kind=="application/json": data=json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type",kind)
        self.send_header("Cache-Control","no-store")
        self.send_header("Content-Length",str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def authorized(self):
        return hmac.compare_digest(self.headers.get("Authorization","").encode(),("Bearer "+secret).encode())
    def do_GET(self):
        files={"/":("index.html","text/html; charset=utf-8"),"/app.js":("app.js","text/javascript"),"/style.css":("style.css","text/css")}
        if self.path in files:
            name,kind=files[self.path]
            return self.send(200,(ROOT/"public"/name).read_bytes(),kind)
        if self.path=="/health": return self.send(200,{"ok":True})
        if self.path!="/api": return self.send(404,{})
        if not self.authorized(): return self.send(401,{})
        with sqlite3.connect(db) as c:
            rev,body=c.execute("SELECT rev,body FROM game WHERE id=1").fetchone()
        self.send(200,public(json.loads(body),rev))
    def do_POST(self):
        if self.path!="/api": return self.send(404,{})
        if not self.authorized(): return self.send(401,{})
        try:
            size=int(self.headers.get("Content-Length","0"))
            if not 0<size<=16384: raise ValueError()
            a=json.loads(self.rfile.read(size))
            if not isinstance(a,dict): raise ValueError()
            with sqlite3.connect(db) as c:
                c.execute("BEGIN IMMEDIATE")
                rev,body=c.execute("SELECT rev,body FROM game WHERE id=1").fetchone()
                s=json.loads(body)
                if a.get("rev")!=rev: return self.send(409,public(s,rev))
                s=act(s,a)
                c.execute("UPDATE game SET rev=?,body=? WHERE id=1",(rev+1,json.dumps(s)))
            self.send(200,public(s,rev+1))
        except (ValueError,TypeError): self.send(400,{})
if __name__=="__main__":
    ThreadingHTTPServer(("0.0.0.0",int(os.getenv("PORT","8080"))),Handler).serve_forever()
