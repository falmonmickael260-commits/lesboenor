const inviteFromLink=new URLSearchParams(location.hash.slice(1)).get("salle");
if(inviteFromLink){sessionStorage.setItem("roomInvite",inviteFromLink);history.replaceState(null,"",location.pathname)}
const roomInvite=sessionStorage.getItem("roomInvite")||"";
const $=id=>document.getElementById(id);
let key=sessionStorage.getItem("regie")||"", state=null, busy=false;
const teams=["Bleus","Rouges"];
let rosterBase=null;
function render(s){
  if(state && s.rev<state.rev)return;
  const changed=!state || s.rev!==state.rev;
  const rosterChange=JSON.stringify(state?.rosters)!==JSON.stringify(s.rosters);
  state=s;
  $("players").hidden=s.phase!=="start";
  $("duel").hidden=s.phase!=="start";
  $("pair").textContent=s.duel.every(Boolean)?s.duel[0]+" (Bleus) et "+s.duel[1]+" (Rouges)":"Renseignez les prénoms dans la composition des équipes.";
  if(rosterChange){
    s.rosters.forEach((names,i)=>$("names"+i).value=names.join("\n"));
    rosterBase=null;
    $("players").open=!s.duel.every(Boolean);
  }
  $("login").hidden=true; $("game").hidden=false; $("status").textContent="● Synchronisé";
  if(!changed)return;
  for(const [id,value] of Object.entries({blue:s.scores[0],red:s.scores[1],pot:s.pot,round:"MANCHE "+(s.i+1)+" / "+s.total,question:s.question,instruction:s.slots.length+" réponses à trouver",message:s.msg,strikes:s.errors+" / 3 erreurs"}))$(id).textContent=value;
  $("turn").textContent=s.phase==="end"?"Manche terminée":s.team===null?"Prise de main":(s.phase==="steal"||s.previous==="steal"?"Vol · "+teams[1-s.team]:"À la main · "+teams[s.team]);
  $("board").replaceChildren(...s.slots.map((v,i)=>{const el=document.createElement("div");el.className="slot"+(v?" hit":"");el.textContent=v?"Nº "+v.rank+" · "+v.label+" · "+v.pts+" pts":"Case "+(i+1)+"　 —";return el}));
  for(const [id,on] of Object.entries({start:s.phase==="start",entry:["play","steal"].includes(s.phase),review:s.phase==="review",next:s.phase==="end"}))$(id).hidden=!on;
  const last=s.i===s.total-1;
  $("next").textContent=last?"Nouvelle partie":"Question suivante →";
  if(last && s.phase==="end")$("turn").textContent=s.scores[0]===s.scores[1]?"Égalité finale":"Victoire des "+teams[Number(s.scores[1]>s.scores[0])];
  $("source").textContent=s.source[0]+" · 1 % = 1 point. ";
  if(s.source[1]){const link=document.createElement("a");link.href=s.source[1];link.target="_blank";link.rel="noopener";link.textContent="Consulter l’étude";$("source").append(link)}
  $("history").replaceChildren(...s.history.map(x=>{const el=document.createElement("li");el.textContent=x;return el}));
}
async function sync(action){
  if(!key)return;
  if(busy){if(action)$("notice").textContent="Synchronisation en cours. Validez de nouveau dans un instant.";return}
  busy=true;
  try{
    const r=await fetch("/api",{method:action?"POST":"GET",headers:{Authorization:"Bearer "+key,"X-Room-Invite":roomInvite},body:action?JSON.stringify({...action,rev:action.rev??state.rev}):undefined});
    if(r.status===401){key="";sessionStorage.removeItem("regie");state=null;$("game").hidden=true;$("login").hidden=false;throw Error("Code incorrect.")}
    if(!r.ok && r.status!==409)throw Error("Connexion interrompue. Vérifiez le panneau avant de réessayer.");
    render(await r.json());sessionStorage.setItem("regie",key);
    if(r.status===409)$("notice").textContent="Le panneau a changé sur l’autre appareil. Vérifiez avant de valider.";
    else if(action){if(action.op==="rosters"){rosterBase=null;$("players").open=false}$("notice").textContent="";$("answer").value=""}
  }catch(e){$("notice").textContent=e.message;$("status").textContent="Hors connexion"}
  finally{busy=false}
}
$("access").onsubmit=async e=>{e.preventDefault();key=$("key").value;await sync();if(state){$("key").value="";$("notice").textContent=""}};
$("entry").onsubmit=e=>{e.preventDefault();sync({op:"answer",value:$("answer").value})};
document.querySelectorAll("[data-team]").forEach(b=>b.onclick=()=>sync({op:"start",team:Number(b.dataset.team)}));
document.querySelectorAll("[data-op]").forEach(b=>b.onclick=()=>{if(b.id==="next" && state.i===state.total-1 && !confirm("Recommencer avec les scores à zéro ?"))return;sync({op:b.dataset.op})});
$("share").onclick=async()=>{try{await navigator.clipboard.writeText(location.origin+(roomInvite?"#salle="+encodeURIComponent(roomInvite):""));$("notice").textContent="Lien copié. Transmettez aussi votre code à votre coanimatrice."}catch{$("notice").textContent=location.origin+(roomInvite?"#salle="+encodeURIComponent(roomInvite):"")}};
$("exit").onclick=()=>{sessionStorage.removeItem("regie");location.reload()};
sync();setInterval(()=>{if(!document.hidden)sync()},1000);

$("rosterForm").oninput=()=>{if(rosterBase===null)rosterBase=state.rev};
$("rosterForm").onsubmit=e=>{
  e.preventDefault();
  const rosters=[0,1].map(i=>$("names"+i).value.split(/\n/).map(n=>n.trim()).filter(Boolean));
  if(rosters.some(group=>!group.length||group.length>30||group.some(n=>n.length>40))){
    $("notice").textContent="Indiquez entre 1 et 30 joueurs par équipe, avec 40 caractères maximum par prénom.";return;
  }
  sync({op:"rosters",rosters,rev:rosterBase??state.rev});
};
