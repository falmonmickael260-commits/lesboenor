function readInvite(value){
  try{
    const url=new URL(value);
    if(url.origin!==location.origin)return "";
    const token=new URLSearchParams(url.hash.slice(1)).get("salle")||url.pathname.match(/^\/invitation\/([\w-]+)\/?$/)?.[1]||"";
    return /^[\w-]{24,128}$/.test(token)?token:"";
  }catch{return ""}
}
let roomInvite=readInvite(location.href)||sessionStorage.getItem("roomInvite")||localStorage.getItem("roomInvite")||"";
if(roomInvite)sessionStorage.setItem("roomInvite",roomInvite);
const $=id=>document.getElementById(id);
let key=sessionStorage.getItem("regie")||"", state=null, busy=false;
const teams=["Bleus","Rouges"];
let rosterBase=null;
$("inviteBox").hidden=!!roomInvite;
function render(s){
  if(state && s.rev<state.rev)return;
  const changed=!state || s.rev!==state.rev;
  const rosterChange=JSON.stringify(state?.rosters)!==JSON.stringify(s.rosters)||JSON.stringify(state?.captains)!==JSON.stringify(s.captains);
  state=s;
  $("players").hidden=s.phase!=="start";
  $("duel").hidden=s.phase!=="start";
  $("pair").textContent=s.duel.every(Boolean)?s.duel[0]+" (Bleus) et "+s.duel[1]+" (Rouges)":"Renseignez les prénoms dans la composition des équipes.";
  const stage=s.phase==="review"?s.previous:s.phase;
  const calling=["buzz","play","steal"].includes(stage);
  $("duel").hidden=s.phase!=="start"&&!calling;
  $("duel").querySelector("small").textContent=stage==="buzz"?"AU BUZZER":stage==="play"?"À TOI DE RÉPONDRE":stage==="steal"?"VOL · PAROLE AU CHEF":"À APPELER AU BUZZER";
  if(calling)$("pair").textContent=[s.speaker,teams[s.speakerTeam]].filter(Boolean).join(" · ");
  for(const b of document.querySelectorAll("[data-team]")){
    const team=Number(b.dataset.team);
    b.textContent=(s.duel[team]||"Les "+teams[team])+" · premier buzzer";
  }
  for(const [i,color] of ["blue","red"].entries()){
    const card=$(color).parentElement;
    let badge=card.querySelector(".chief");
    if(!badge){badge=document.createElement("span");badge.className="chief";badge.style.cssText="display:block;font-size:12px;letter-spacing:0;overflow-wrap:anywhere";card.append(badge)}
    badge.textContent=s.captains?.[i]?"Chef · "+s.captains[i]:"";
  }
  if(rosterChange){
    s.rosters.forEach(drawNames);
    rosterBase=null;
    $("players").open=!s.duel.every(Boolean);
  }
  $("login").hidden=true; $("game").hidden=false; $("status").textContent="● Synchronisé";
  if(!changed)return;
  if($("finale")){
    $("regular").hidden=!!s.final;
    $("finale").hidden=!s.final;
    if(s.final)renderFinal(s);
  }
  for(const [id,value] of Object.entries({blue:s.scores[0],red:s.scores[1],pot:s.pot,round:"MANCHE "+(s.i+1)+" / "+s.total,question:s.question,instruction:s.slots.length+" réponses à trouver",message:s.msg,strikes:s.errors+" / 3 erreurs"}))$(id).textContent=value;
  $("turn").textContent=s.phase==="end"?"Manche terminée":stage==="buzz"?"Duel · "+teams[s.speakerTeam]:s.team===null?"Prise de main":(s.phase==="steal"||s.previous==="steal"?"Vol · "+teams[1-s.team]:"À la main · "+teams[s.team]);
  $("board").replaceChildren(...s.slots.map((v,i)=>{
    const el=document.createElement("div"),number=document.createElement("b"),label=document.createElement("span");
    el.className="slot"+(v?" hit":"");
    number.textContent=String(v?v.rank:i+1);label.textContent=v?v.label:"";
    if(v && s.phase==="end"){
      const found=s.found.includes(i),status=document.createElement("small");
      status.style.cssText="display:block;letter-spacing:0;font-size:12px;color:inherit";
      status.textContent=found?"✓ Trouvée":"Non trouvée";
      label.append(status);
      if(!found)el.className="slot";
      if(!found)label.style.cssText="height:auto;width:auto;background:none";
    }
    el.setAttribute("aria-label",v?v.label+" "+v.pts+" points":"Réponse "+(i+1)+" masquée");
    el.append(number,label);
    if(v){const pts=document.createElement("strong");pts.textContent=v.pts;el.append(pts)}
    return el;
  }));
  $("instruction").textContent=(s.phase==="end"?"Classement final · ":"")+s.found.length+" / "+s.slots.length+" réponses trouvées";
  $("strikes").textContent="Erreurs "+("✕ ".repeat(s.errors))+("○ ".repeat(3-s.errors));
  for(const [id,on] of Object.entries({start:s.phase==="start",entry:["buzz","play","steal"].includes(s.phase),review:s.phase==="review",next:s.phase==="end"}))$(id).hidden=!on;
  const last=s.i===s.total-1;
  $("next").textContent=last?"Passer à la finale":"Question suivante →";
  if(last && s.phase==="end")$("turn").textContent=s.scores[0]===s.scores[1]?"Égalité finale": "Qualification des "+teams[Number(s.scores[1]>s.scores[0])];
  $("source").textContent=s.source[0]+" · Points du sondage. ";
  if(s.source[1]){const link=document.createElement("a");link.href=s.source[1];link.target="_blank";link.rel="noopener";link.textContent="Consulter l’étude";$("source").append(link)}
  $("history").replaceChildren(...s.history.map(x=>{const el=document.createElement("li");el.textContent=x;return el}));
}
async function sync(action){
  if(!key)return;
  if(busy){if(action)$("notice").textContent="Synchronisation en cours. Validez de nouveau dans un instant.";return}
  busy=true;
  try{
    const r=await fetch("/api",{method:action?"POST":"GET",headers:{Authorization:"Bearer "+key,"X-Room-Invite":roomInvite},body:action?JSON.stringify({...action,rev:action.rev??state.rev}):undefined});
    if(r.status===401){$("inviteBox").hidden=false;key="";sessionStorage.removeItem("regie");state=null;$("game").hidden=true;$("login").hidden=false;throw Error(!roomInvite?"Ouvrez le lien privé complet reçu de votre coanimateur, puis saisissez le code.":"Accès refusé. Vérifiez le code et le lien privé. Après cinq essais incorrects, attendez 15 minutes.")}
    if(r.status===400 && action?.op==="seal"){ $("notice").textContent="Vérifiez le prénom dans l’équipe qualifiée et choisissez deux finalistes différents. Si cette fiche est déjà scellée, ouvrez l’autre.";return}
    if(!r.ok && r.status!==409)throw Error("Connexion interrompue. Vérifiez le panneau avant de réessayer.");
    render(await r.json());if(roomInvite)localStorage.setItem("roomInvite",roomInvite);sessionStorage.setItem("regie",key);
    if(r.status===409)$("notice").textContent="Le panneau a changé sur l’autre appareil. Vérifiez avant de valider.";
    else if(action){if(action.op==="rosters"){rosterBase=null;$("players").open=false}$("notice").textContent="";$("answer").value=""}
  }catch(e){$("notice").textContent=e.message;$("status").textContent="Hors connexion"}
  finally{busy=false}
}
$("access").onsubmit=async e=>{e.preventDefault();key=$("key").value.trim();
  if($("inviteText").value.trim())roomInvite=readInvite($("inviteText").value.trim());
  if(!roomInvite && /^\d{4}$/.test(key)){
    key="";$("inviteBox").hidden=false;$("inviteText").focus();$("notice").textContent="Collez le lien privé dans le premier champ, puis appuyez sur Entrer.";return;
  }
  await sync();if(state){$("key").value="";$("notice").textContent=""}};
$("entry").onsubmit=e=>{e.preventDefault();sync({op:"answer",value:$("answer").value})};
document.querySelectorAll("[data-team]").forEach(b=>b.onclick=()=>sync({op:"start",team:Number(b.dataset.team)}));
document.querySelectorAll("[data-op]").forEach(b=>b.onclick=()=>{sync({op:b.dataset.op})});
$("share").onclick=async()=>{try{await navigator.clipboard.writeText(location.origin+(roomInvite?"/invitation/"+encodeURIComponent(roomInvite):""));$("notice").textContent="Lien copié. Transmettez aussi votre code à votre coanimatrice."}catch{$("notice").textContent=location.origin+(roomInvite?"/invitation/"+encodeURIComponent(roomInvite):"")}};
$("exit").onclick=()=>{sessionStorage.removeItem("regie");location.reload()};
bootFinal();sync();setInterval(()=>{if(!document.hidden)sync()},1000);

function addName(team,value="",focus=false){
  const list=$("list"+team), index=list.children.length+1;
  if(index>30)return;
  const label=document.createElement("label"), number=document.createElement("span"), input=document.createElement("input");
  number.textContent=String(index).padStart(2,"0");input.value=value;
  input.placeholder="Prénom ou pseudo";input.maxLength=40;input.autocomplete="off";
  input.setAttribute("aria-label",teams[team]+" · joueur "+index);
  input.onkeydown=e=>{
    if(e.key!=="Enter")return;
    e.preventDefault();
    const next=label.nextElementSibling;
    if(next)next.querySelector("input").focus();else if(input.value.trim())addName(team,"",true);
  };
  label.append(number,input);list.append(label);
  $("add"+team).disabled=index===30;
  if(focus)input.focus();
}
function drawNames(names,team){
  const list=$("list"+team);
  let select=$("chief"+team);
  if(!select){
    const label=document.createElement("label");label.textContent="Chef d’équipe";
    select=document.createElement("select");select.id="chief"+team;select.style.cssText="display:block;width:100%;min-height:44px;padding:6px;font:inherit;margin:4px 0 12px";
    label.append(select);list.before(label);
  }
  function choices(preferred){
    const selected=preferred||select.value;
    const values=Array.from(list.querySelectorAll("input"),x=>x.value.trim()).filter(Boolean);
    select.replaceChildren(...values.map(n=>new Option(n,n)));
    if(values.includes(selected))select.value=selected;
  }
  list.oninput=()=>choices();
  $("names"+team).hidden=true;
  $("list"+team).replaceChildren();
  $("add"+team).hidden=false;
  $("add"+team).onclick=()=>addName(team,"",true);
  for(let i=0;i<Math.max(7,names.length);i++)addName(team,names[i]||"");
  choices(state.captains?.[team]);
}
$("rosterForm").oninput=()=>{if(rosterBase===null)rosterBase=state.rev};
$("rosterForm").onsubmit=e=>{
  e.preventDefault();
  const rosters=[0,1].map(i=>Array.from($("list"+i).querySelectorAll("input"),input=>input.value.trim()).filter(Boolean));
  if(rosters.some(group=>!group.length||group.length>30||group.some(n=>n.length>40))){
    $("notice").textContent="Indiquez entre 1 et 30 joueurs par équipe, avec 40 caractères maximum par prénom.";return;
  }
  if(rosters.some(group=>new Set(group.map(n=>n.toLowerCase())).size!==group.length)){
    $("notice").textContent="Pour distinguer deux joueurs dans une équipe, ajoutez une initiale ou un pseudo.";return;
  }
  sync({op:"rosters",rosters,captains:[0,1].map(i=>$("chief"+i).value),rev:rosterBase??state.rev});
};


function bootFinal(){
  if(!$("finale"))return;
  for(const b of document.querySelectorAll("[data-qual]"))b.onclick=()=>sync({op:"choose",team:Number(b.dataset.qual)});
  for(const seat of [0,1])$("seat"+seat).onclick=()=>{
    sessionStorage.setItem("finalSeat-"+state.final.id,String(seat));
    renderFinal(state);
  };
  $("privateForm").oninput=()=>{const id=state.final.id,seat=sessionStorage.getItem("finalSeat-"+id);
    sessionStorage.setItem("draft-"+id+seat,JSON.stringify([$("finalName").value,...Array.from($("finalFields").querySelectorAll("input"),x=>x.value)]))};
  $("privateForm").onsubmit=e=>{e.preventDefault();
    const f=state.final,seat=Number(sessionStorage.getItem("finalSeat-"+f.id));
    if(!confirm("Sceller définitivement la fiche de "+$("finalName").value+" ?"))return;
    sync({op:"seal",session:f.id,seat,name:$("finalName").value,answers:Array.from($("finalFields").querySelectorAll("input"),x=>x.value)});
  };
  $("reveal").onclick=()=>sync({op:"reveal"});
  $("restart").onclick=()=>{if(confirm("Effacer les scores et recommencer ?"))sync({op:"restart"})};
}
function renderFinal(s){
  const f=s.final, playing=s.phase==="private", done=s.phase==="verdict", group=teams[f.team]||"";
  $("finalTitle").textContent=done?(f.total>=f.goal?"Finale gagnée par les "+group+" !":"Finale perdue par les "+group):"Finale "+(group?"des "+group:"à départager");
  $("finalGuide").textContent=done?f.total+" points sur un objectif de "+f.goal:"Chacun contacte un joueur de l’équipe qualifiée par message privé et ouvre une fiche différente. Posez les trois mêmes questions. Objectif : 100 points à deux. Une réponse identique compte une seule fois.";
  $("tie").hidden=s.phase!=="qualify";$("privatePanel").hidden=!playing;$("restart").hidden=!done;
  $("results").replaceChildren();
  if(done){for(const row of f.rows){
    const title=document.createElement("h3");title.textContent=row.question;$("results").append(title);
    for(const a of row.answers){const p=document.createElement("p");p.textContent=a.name+" · "+a.raw+" → "+a.label+" · "+a.points+" pts"+(a.duplicate?" (doublon)":"");$("results").append(p)}
    const link=document.createElement("a");link.href=row.source;link.target="_blank";link.rel="noopener";link.textContent="Voir le sondage";$("results").append(link)
  }}
  if(!playing)return;
  const choice=sessionStorage.getItem("finalSeat-"+f.id),seat=Number(choice),open=choice!==null&&!f.sealed[seat];
  $("sealed").textContent=f.sealed.map((n,i)=>"Fiche "+(i+1)+" · "+(n?n+" ✓":"à remplir")).join(" / ");
  $("reveal").hidden=!f.sealed.every(Boolean);$("privateForm").hidden=!open;
  for(const i of [0,1]){$("seat"+i).disabled=!!f.sealed[i];$("seat"+i).textContent=(choice===String(i)?"Ma fiche ":"Ouvrir la fiche ")+(i+1)}
  const form=$("privateForm"),draftKey="draft-"+f.id+seat;
  if(!open||form.dataset.key===draftKey)return;
  form.dataset.key=draftKey;
  const draft=JSON.parse(sessionStorage.getItem(draftKey)||"[]");
  $("finalName").value=draft[0]||"";$("finalPlayers").replaceChildren(...s.rosters[f.team].map(n=>new Option(n)));
  $("finalFields").replaceChildren(...f.prompts.map((q,i)=>{const label=document.createElement("label"),input=document.createElement("input");label.textContent=(i+1)+". "+q;input.required=true;input.maxLength=180;input.value=draft[i+1]||"";input.placeholder="Réponse du joueur";input.style.cssText="display:block;width:100%;margin:5px 0 14px";label.append(input);return label}));
}




