import random
import threading, time
import hmac, json, os, re, sqlite3, unicodedata
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from questions import boards, six_boards

ROOT = Path(__file__).resolve().parent
directory = Path(os.getenv("RAILWAY_VOLUME_MOUNT_PATH") or os.getenv("DATA_DIR", ROOT/"data"))
directory.mkdir(parents=True, exist_ok=True)
db = directory/"plateau.sqlite3"
secret = os.environ.get("HOST_KEY", "")
if len(secret) < 12:
    raise SystemExit("Définissez HOST_KEY avec au moins 12 caractères.")
ROUNDS = 8

def deal(deck, remaining):
    deck, pool = list(deck), list(remaining)
    while len(deck) < ROUNDS:
        if not pool:
            eligible = [i for i in range(len(six_boards)) if i not in deck]
            random.SystemRandom().shuffle(eligible)
            deferred = list(deck)
            random.SystemRandom().shuffle(deferred)
            pool = eligible + deferred
        deck.append(pool.pop(0))
    return deck, pool

def fresh(remaining=None):
    deck,pool=deal([],remaining or [])
    return dict(deck=deck,remaining=pool,i=0,team=None,phase="start",found=[],pot=0,errors=0,scores=[0,0],history=[],msg="Choisissez l’équipe qui prend la main.")
def draw_duel(s, keep=False):
    groups=s.get("rosters",[[],[]])
    history=s.setdefault("called",[[],[]])
    old=s.get("pair",[None,None])
    pair=[]
    for team,names in enumerate(groups):
        if keep and old[team] in names:
            pair.append(old[team])
            continue
        eligible=[n for n in names if n not in history[team]]
        if not eligible and names:
            previous=history[team][-1:] 
            history[team]=[]
            eligible=[n for n in names if n not in previous] or names
        pair.append(random.SystemRandom().choice(eligible) if eligible else None)
    s["pair"]=pair
    return s

with sqlite3.connect(db) as c:
    c.execute("CREATE TABLE IF NOT EXISTS game(id INTEGER PRIMARY KEY, rev INTEGER, body TEXT)")
    c.execute("INSERT OR IGNORE INTO game VALUES(1,0,?)",(json.dumps(fresh()),))
    rev,body=c.execute("SELECT rev,body FROM game WHERE id=1").fetchone()
    old=json.loads(body)
    if "deck" not in old and (old.get("six") or old["phase"]=="start"):
        prefix=list(range(old["i"]+1))
        rest=list(range(len(prefix),len(six_boards)))
        random.SystemRandom().shuffle(rest)
        cycle=prefix+rest
        old.update(deck=cycle[:6],remaining=cycle[6:])
        c.execute("UPDATE game SET body=?,rev=? WHERE id=1",(json.dumps(old),rev+1))

    if old["phase"] not in ("qualify","private","verdict") and len(old.get("deck",[])) < ROUNDS:
        deck=old.get("deck",list(range(6)))
        old["deck"],old["remaining"]=deal(deck,old.get("remaining",[]))
        c.execute("UPDATE game SET body=?,rev=rev+1 WHERE id=1",(json.dumps(old),))

    if "pair" not in old:
        groups=old.get("rosters",[[],[]])
        old["captains"]=[g[0] if g else None for g in groups]
        completed=old["i"]+int(old["phase"]!="start")
        old["called"]=[[g[j%len(g)] for j in range(completed)] if g else [] for g in groups]
        draw_duel(old)
        c.execute("UPDATE game SET body=?,rev=rev+1 WHERE id=1",(json.dumps(old),))

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
# Survey percentages used as points. Only the prompts are sent before the reveal.
final_questions = [
    ("Quel fromage figure dans le top 10 des Français de l’enquête YouGov 2015 ?",
     "https://yougov.com/fr-fr/articles/12592-les-fromages-preferes-des-francais-le-top10-decouv",
     [("Camembert",41,"camember"),("Chèvre",36,"fromage de chevre|buche de chevre"),("Comté",32,"comte"),
      ("Roquefort",29,"roquefort"),("Emmental",21,"emmenthal"),("Gruyère",20,"gruyere"),
      ("Brie",19,"brie"),("Bleu",11,"fromage bleu"),("Parmesan",11,"parmigiano"),("Gorgonzola",7,"gorgonzola")]),
    ("Quelle garniture sucrée pour crêpes figure sur le podium français de 2021 ?",
     "https://yougov.com/fr-fr/articles/33824-les-francais-sont-ils-des-fans-de-crepes",
     [("Sucre",23,"sucre en poudre|du sucre"),("Pâte à tartiner",16,"nutella|pate a tartiner au chocolat"),
      ("Confiture",15,"confiture de fraise|confiture de fruits")]),
    ("Quelle garniture de pizza figure parmi les cinq favorites du sondage YouGov Pizza ?",
     "https://docs.cdn.yougov.com/fdemdtp8no/Pizza_poll_results.pdf",
     [("Pepperoni",24,"peperoni"),("Saucisse",13,"saucisses|chair a saucisse"),
      ("Supplément fromage",11,"double fromage|extra fromage|fromage supplementaire|extra cheese"),
      ("Champignons",9,"champignon"),("Poulet",6,"chicken")])]
goal = 100

def final_action(s,a):
    f=s["final"]
    op=a.get("op")
    if op=="choose" and s["phase"]=="qualify" and a.get("team") in (0,1):
        s["phase"]="private"
        f["team"]=a["team"]
    elif op=="seal" and s["phase"]=="private" and a.get("session")==f["id"]:
        seat=a.get("seat")
        name=a.get("name")
        answers=a.get("answers")
        if seat not in (0,1) or f["sheets"][seat] is not None: raise ValueError()
        if not isinstance(name,str) or not 1<=len(name.strip())<=40: raise ValueError()
        if not isinstance(answers,list) or len(answers)!=len(final_questions): raise ValueError()
        if any(not isinstance(x,str) or not 1<=len(x.strip())<=180 for x in answers): raise ValueError()
        if any(sheet and sheet["name"].casefold()==name.strip().casefold() for sheet in f["sheets"]): raise ValueError()
        roster=s.get("rosters",[[],[]])[f["team"]]
        if len(set(roster))>=2 and name.strip() not in roster: raise ValueError()
        f["sheets"][seat]={"name":name.strip(),"answers":[x.strip() for x in answers]}
    elif op=="reveal" and s["phase"]=="private" and all(f["sheets"]):
        total=0
        rows=[]
        for i,(question,source,options) in enumerate(final_questions):
            used=set()
            results=[]
            for sheet in f["sheets"]:
                raw=sheet["answers"][i]
                hits=[(label,points) for label,points,aliases in options if any(close(norm(raw),norm(alias)) for alias in [label,*aliases.split("|")])]
                label,points=hits[0] if len(hits)==1 else ("Hors tableau",0)
                duplicate=label in used and points>0
                used.add(label)
                if duplicate: points=0
                results.append(dict(name=sheet["name"],raw=raw,label=label,points=points,duplicate=duplicate))
                total+=points
            rows.append(dict(question=question,source=source,answers=results))
        f.update(total=total,rows=rows)
        s["phase"]="verdict"
    else: raise ValueError()
    return s


def current_board(s):
    if "deck" in s: return six_boards[s["deck"][s["i"]]]
    bank=six_boards if s.get("six") or s["phase"]=="start" else boards
    return bank[s["i"]]

def public(s,rev):
    s=s.copy()
    if 'final' in s:
        f=dict(s['final'])
        f['sealed']=[sheet['name'] if sheet else None for sheet in f.pop('sheets')]
        f.update(goal=goal,prompts=[q[0] for q in final_questions])
        s['final']=f
    rosters=s.get("rosters",[[],[]])
    duel=s.get("pair",[None,None])
    q=current_board(s)
    round_count=len(s.get("deck",boards))
    s.pop("deck",None)
    s.pop("remaining",None)
    stage=s.get("previous") if s["phase"]=="review" else s["phase"]
    team=s["team"]
    speaker=None
    if stage=="buzz":
        team=s["buzzTeam"]
        speaker=duel[team]
    elif stage=="steal":
        team=1-team
        speaker=s.get("captains",[None,None])[team]
    elif stage=="play" and team is not None and rosters[team]:
        names=rosters[team]
        start=names.index(duel[team]) if duel[team] in names else 0
        speaker=names[(start+s.get("turnOffset",len(s["found"])+s["errors"]))%len(names)]
    s.update(speaker=speaker,speakerTeam=team)
    slots=[]
    for i,(label,pts,_) in enumerate(q["rows"]):
        rank=1+sum(p>pts for _,p,_ in q["rows"])
        slots.append(dict(rank=rank,label=label,pts=pts) if i in s["found"] or s["phase"]=="end" else None)
    return {**s,"rosters":rosters,"duel":duel,"slots":slots,"question":q["question"],"source":q["source"] if s["phase"]=="end" else [q["source"][0]],"rev":rev,"total":round_count}
def finish(s,winner,stolen):
    s["scores"][winner]+=s["pot"]
    outcome=("Vol réussi" if stolen else "Manche remportée")+f' · {teams[winner]} +{s["pot"]} points'
    s["history"].append(outcome)
    s.update(phase="end",msg=outcome)
def resolve_buzz(s,points):
    team=s["buzzTeam"]
    winner=team if points else 1-team
    s.update(team=winner,phase="play",turnOffset=1 if points else 0,errors=0)
    s.pop("firstBuzz",None)
    s["msg"]+=" · Les "+teams[winner]+" prennent la main."

def act(s,a):
    if a.get("op")=="restart":
        return draw_duel({**fresh(s.get("remaining",list(range(6,len(six_boards))))),"rosters":s.get("rosters",[[],[]]),"captains":s.get("captains",[None,None])})
    phase=s["phase"]
    op=a.get("op")
    if phase in ("qualify","private","verdict"): return final_action(s,a)
    if op=="rosters" and phase=="start":
        groups=a.get("rosters")
        if not isinstance(groups,list) or len(groups)!=2: raise ValueError()
        for names in groups:
            if not isinstance(names,list) or not 1<=len(names)<=30: raise ValueError()
            if any(not isinstance(n,str) or not 1<=len(n.strip())<=40 for n in names): raise ValueError()
        groups=[[n.strip() for n in names] for names in groups]
        captains=a.get("captains",[g[0] for g in groups])
        if not isinstance(captains,list) or len(captains)!=2: raise ValueError()
        if any(captains[i] not in names or len(set(n.casefold() for n in names))!=len(names) for i,names in enumerate(groups)): raise ValueError()
        s.update(rosters=groups,captains=captains)
        draw_duel(s,keep=True)
    elif op=="start" and phase=="start" and a.get("team") in (0,1):
        for team,name in enumerate(s.get("pair",[])):
            if name: s["called"][team].append(name)
        s["six"]=True
        s.pop("firstBuzz",None)
        s.update(team=None,buzzTeam=a["team"],phase="buzz",turnOffset=0,msg="Saisissez la réponse de la personne qui a buzzé.")
    elif op=="next" and phase=="end":
        if s["i"]==len(s.get("deck",boards))-1:
            blue,red=s["scores"]
            s["phase"]="qualify" if blue==red else "private"
            s["final"]=dict(id=os.urandom(12).hex(),team=None if blue==red else int(red>blue),sheets=[None,None])
            return s
        s.update(i=s["i"]+1,team=None,phase="start",found=[],pot=0,errors=0,msg="Choisissez l’équipe qui prend la main.")
        draw_duel(s)
    elif op=="retry" and phase=="review":
        s.update(phase=s.pop("previous"),msg="Demandez une précision, puis reformulez la réponse.")
    elif op=="miss" and phase=="review":
        prev=s.pop("previous")
        if prev=="buzz":
            s["msg"]="Hors du tableau au buzzer."
            resolve_buzz(s,0)
        elif prev=="steal": finish(s,s["team"],False)
        else:
            s["turnOffset"]=s.get("turnOffset",len(s["found"])+s["errors"])+1
            s["errors"]+=1
            steal=s["errors"]==3
            s.update(phase="steal" if steal else "play",msg=("Tentative de vol des "+teams[1-s["team"]] if steal else "Hors du tableau · une erreur."))
    elif op=="answer" and phase in ("buzz","play","steal"):
        raw=a.get("value","")
        if not isinstance(raw,str) or not 0<len(raw.strip())<=180: raise ValueError()
        v=norm(raw)
        rows=current_board(s)["rows"]
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
            if phase=="buzz":
                resolve_buzz(s,pts)
                return s
            if phase=="play": s["turnOffset"]=s.get("turnOffset",len(s["found"])-1+s["errors"])+1
            if phase=="steal" or len(s["found"])==len(rows):
                result=s["msg"]
                finish(s,1-s["team"] if phase=="steal" else s["team"],phase=="steal")
                s["msg"]=result+" — "+s["msg"]
    else: raise ValueError()
    return s

room_pin = os.getenv("ROOM_PIN", "")
room_invite = os.getenv("ROOM_INVITE", "")
pin_lock = threading.Lock()
with sqlite3.connect(db) as c:
    c.execute("CREATE TABLE IF NOT EXISTS pin_attempts (at REAL)")

class Handler(BaseHTTPRequestHandler):
    def send(self,status,data,kind="application/json"):
        if kind=="application/json": data=json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type",kind)
        self.send_header("Referrer-Policy","no-referrer")
        self.send_header("Cache-Control","no-store")
        self.send_header("Content-Length",str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def log_request(self, code="-", size="-"):
        if not self.path.startswith("/invitation/"):
            super().log_request(code,size)

    def authorized(self):
        header = self.headers.get("Authorization", "")
        if hmac.compare_digest(header.encode(), ("Bearer "+secret).encode()): return True
        if not re.fullmatch(r"Bearer [0-9]{4}", header) or not re.fullmatch(r"[0-9]{4}", room_pin): return False
        if len(room_invite) < 24 or not hmac.compare_digest(self.headers.get("X-Room-Invite", "").encode(), room_invite.encode()): return False
        with pin_lock, sqlite3.connect(db) as c:
            now = time.time()
            c.execute("DELETE FROM pin_attempts WHERE at < ?", (now-900,))
            if c.execute("SELECT COUNT(*) FROM pin_attempts").fetchone()[0] >= 5: return False
            if hmac.compare_digest(header[7:], room_pin): return True
            c.execute("INSERT INTO pin_attempts VALUES (?)", (now,))
            return False
    def do_GET(self):
        files={"/":("index.html","text/html; charset=utf-8"),"/app.js":("app.js","text/javascript"),"/style.css":("style.css","text/css")}
        if re.fullmatch(r"/invitation/[A-Za-z0-9_-]{24,128}/?(?:\?[^ ]*)?",self.path):
            return self.send(200,(ROOT/"public/index.html").read_bytes(),"text/html; charset=utf-8")
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
                if a.get("rev")!=rev and not (a.get("op")=="seal" and s["phase"]=="private" and a.get("session")==s["final"]["id"]): return self.send(409,public(s,rev))
                s=act(s,a)
                c.execute("UPDATE game SET rev=?,body=? WHERE id=1",(rev+1,json.dumps(s)))
            self.send(200,public(s,rev+1))
        except (ValueError,TypeError): self.send(400,{})
if __name__=="__main__":
    ThreadingHTTPServer(("0.0.0.0",int(os.getenv("PORT","8080"))),Handler).serve_forever()




