# -*- coding: utf-8 -*-
import json, os, hashlib
from recipes_data import R

OUT = os.path.dirname(os.path.abspath(__file__))

# ---- normalizacja nazw do filtra skladnikow ----
NORM = {
    "jajko":"jajka",
    "indyk mielony":"indyk",
    "cielęcina mielona":"cielęcina",
    "kurczak mielony":"kurczak",
}
# skladniki-staple, ktorych NIE pokazujemy jako filtry
EXCLUDE = {
    "sól","cynamon","wanilia","koperek","natka","majeranek","tymianek","liść laurowy",
    "lubczyk","bazylia","oliwa","olej rzepakowy","masło","woda","miód",
    "mąka orkiszowa","mąka ziemniaczana","mąka kukurydziana","bułka tarta",
    "oregano","kurkuma",
}
GROUPS = {
    # Mieso i jaja
    "indyk":"Mięso i jaja","cielęcina":"Mięso i jaja","królik":"Mięso i jaja","kurczak":"Mięso i jaja",
    "chuda wołowina":"Mięso i jaja","jajka":"Mięso i jaja",
    "schab":"Mięso i jaja","polędwiczka wieprzowa":"Mięso i jaja",
    # Ryby
    "łosoś":"Ryby","dorsz":"Ryby","pstrąg":"Ryby","sandacz":"Ryby","mintaj":"Ryby","morszczuk":"Ryby",
    # Nabial
    "mleko":"Nabiał","jogurt naturalny":"Nabiał","kefir":"Nabiał","maślanka":"Nabiał",
    "twaróg półtłusty":"Nabiał","serek wiejski":"Nabiał","ser żółty łagodny":"Nabiał","mozzarella":"Nabiał",
    # Kasze i pieczywo
    "płatki owsiane":"Kasze i pieczywo","kasza jaglana":"Kasze i pieczywo","kasza gryczana":"Kasze i pieczywo",
    "kasza manna":"Kasze i pieczywo","ryż":"Kasze i pieczywo","ryż basmati":"Kasze i pieczywo","makaron":"Kasze i pieczywo",
    "pieczywo orkiszowe":"Kasze i pieczywo","chleb pszenny":"Kasze i pieczywo","chleb żytni":"Kasze i pieczywo",
    "chleb na zakwasie":"Kasze i pieczywo","kajzerka":"Kasze i pieczywo","pieczywo graham":"Kasze i pieczywo",
    "wafle ryżowe":"Kasze i pieczywo",
    # Warzywa
    "marchew":"Warzywa","cukinia":"Warzywa","dynia":"Warzywa","ziemniaki":"Warzywa","batat":"Warzywa",
    "ogórek":"Warzywa","sałata":"Warzywa","buraki":"Warzywa","pietruszka":"Warzywa","szpinak":"Warzywa",
    "seler":"Warzywa","pomidor":"Warzywa","papryka":"Warzywa","rukola":"Warzywa","roszponka":"Warzywa",
    "szparagi":"Warzywa","bakłażan":"Warzywa","rzodkiewka":"Warzywa",
    # Owoce
    "jabłko":"Owoce","gruszka":"Owoce","banan":"Owoce","borówki":"Owoce","brzoskwinia":"Owoce",
    "śliwka":"Owoce","winogrona":"Owoce",
    # Tluszcze i orzechy
    "awokado":"Tłuszcze i orzechy","orzechy włoskie":"Tłuszcze i orzechy","migdały":"Tłuszcze i orzechy",
    "orzechy laskowe":"Tłuszcze i orzechy",
}

def norm(name):
    return NORM.get(name, name)

# ---- budowa listy przepisow z id i tagami ----
recipes = []
for i, r in enumerate(R):
    tags = []
    for name, amt in r["ing"]:
        n = norm(name)
        if n in EXCLUDE:
            continue
        if n not in tags:
            tags.append(n)
    recipes.append({
        "id": "r%03d" % (i+1),
        "num": i+1,
        "t": r["t"],
        "m": r["m"],
        "c": r["c"],
        "al": r["al"],
        "kcal": r["kcal"],
        "ing": [[n, a] for n, a in r["ing"]],
        "steps": r["steps"],
        "tags": tags,
    })

# upewnij sie, ze kazdy tag ma grupe
for rec in recipes:
    for t in rec["tags"]:
        if t not in GROUPS:
            GROUPS[t] = "Inne"

MEALS = [
    {"key":"s1","label":"Pierwsze śniadanie","emoji":"🌅"},
    {"key":"s2","label":"Drugie śniadanie","emoji":"🥪"},
    {"key":"ob","label":"Obiad","emoji":"🍲"},
    {"key":"pw","label":"Podwieczorek","emoji":"🍎"},
    {"key":"ko","label":"Kolacja","emoji":"🌙"},
]

APP_DATA = {"recipes": recipes, "groups": GROUPS, "meals": MEALS}
data_json = json.dumps(APP_DATA, ensure_ascii=False)

# =================== SZABLON APLIKACJI ===================
HTML = r"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#7E463C">
<meta name="description" content="Nasza Kuchnia — proste przepisy zgodne z dietą mamy karmiącej. Duże przyciski, czytelne komunikaty.">
<link rel="manifest" href="manifest.webmanifest">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<title>Nasza Kuchnia</title>
<style>
  :root{
    --paper:#FBF6F0; --surface:#FFFFFF; --border:#E7DACE; --ink:#2E2A25; --muted:#6E655C;
    --clay:#9E5F52; --clay-dark:#7E463C; --clay-soft:#F4E6DD;
    --green:#4F6A3F; --green-soft:#E9F1E4; --danger:#B24A2E; --focus:#1E63C4;
    --radius:18px;
  }
  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;background:var(--paper);}
  body{
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
    font-size:20px; line-height:1.5; color:var(--ink);
    -webkit-text-size-adjust:100%;
  }
  h1,h2,h3{font-family:Georgia,"Times New Roman",serif; line-height:1.2;}
  .app{max-width:640px; margin:0 auto; min-height:100vh; background:var(--paper);
       display:flex; flex-direction:column;}
  /* ---- pasek gorny ---- */
  .appbar{position:sticky; top:0; z-index:10; background:var(--clay-dark); color:#FBF6F0;
    display:flex; align-items:center; gap:10px; padding:14px 14px;
    padding-top:calc(14px + env(safe-area-inset-top)); box-shadow:0 2px 10px rgba(0,0,0,.12);}
  .appbar .title{font-family:Georgia,serif; font-size:1.35rem; font-weight:700; flex:1; text-align:center;}
  .iconbtn{min-width:52px; min-height:52px; border:none; background:rgba(255,255,255,.14);
    color:#FBF6F0; border-radius:14px; font-size:1.5rem; cursor:pointer; line-height:1;}
  .iconbtn:active{background:rgba(255,255,255,.28);}
  .iconbtn.ghost{background:transparent;}
  .spacer{min-width:52px;}
  /* ---- tresc ---- */
  main{flex:1; padding:20px 16px calc(28px + env(safe-area-inset-bottom));}
  .kicker{font-size:1rem; color:var(--muted); margin:0 0 4px;}
  h1.screen{font-size:1.7rem; margin:0 0 6px;}
  h2.screen{font-size:1.5rem; margin:0 0 14px;}
  .lead{color:var(--muted); font-size:1.02rem; margin:0 0 18px;}
  /* ---- duze przyciski posilkow ---- */
  .meal-btn{display:flex; align-items:center; gap:16px; width:100%; min-height:88px;
    background:var(--surface); border:2px solid var(--border); border-radius:var(--radius);
    padding:16px 20px; margin-bottom:14px; font-size:1.25rem; font-weight:600; color:var(--ink);
    cursor:pointer; text-align:left;}
  .meal-btn .emoji{font-size:2rem; line-height:1;}
  .meal-btn .arrow{margin-left:auto; color:var(--clay); font-size:1.6rem;}
  .meal-btn:active{background:var(--clay-soft); border-color:var(--clay);}
  .saved-entry{margin-top:6px;}
  .saved-entry .meal-btn{border-style:dashed;}
  /* ---- przyciski akcji ---- */
  .primary-btn{display:block; width:100%; min-height:70px; background:var(--clay-dark); color:#FBF6F0;
    border:none; border-radius:var(--radius); font-size:1.2rem; font-weight:700; cursor:pointer;
    margin-top:8px;}
  .primary-btn:active{background:#6a3a31;}
  .ghost-btn{display:block; width:100%; min-height:62px; background:var(--surface);
    border:2px solid var(--clay); color:var(--clay-dark); border-radius:var(--radius);
    font-size:1.1rem; font-weight:700; cursor:pointer; margin-top:12px;}
  .ghost-btn:active{background:var(--clay-soft);}
  .search-input{width:100%; min-height:64px; font-size:1.3rem; padding:14px 18px; border:2px solid var(--border);
    border-radius:var(--radius); margin-bottom:14px; background:var(--surface); color:var(--ink);}
  .search-input:focus-visible{outline:3px solid var(--focus); outline-offset:2px;}
  .search-error{color:var(--danger); font-weight:600; margin-top:14px;}
  /* ---- skladniki (chipsy) ---- */
  .selbar{position:sticky; top:calc(80px + env(safe-area-inset-top)); z-index:5;
    background:var(--paper); padding:6px 0 12px; margin-bottom:6px;}
  .selcount{font-size:1rem; color:var(--muted);}
  .grouplabel{font-size:.95rem; font-weight:700; color:var(--clay-dark); text-transform:uppercase;
    letter-spacing:.5px; margin:18px 0 8px;}
  .chips{display:flex; flex-wrap:wrap; gap:10px;}
  .chip{min-height:56px; display:inline-flex; align-items:center; gap:8px; padding:10px 18px;
    background:var(--surface); border:2px solid var(--border); border-radius:999px;
    font-size:1.05rem; color:var(--ink); cursor:pointer;}
  .chip .tick, .chip .cross{display:none; font-weight:800;}
  .chip.on{background:var(--clay); border-color:var(--clay); color:#fff;}
  .chip.on .tick{display:inline;}
  .chip.excl{background:#F7ECE7; border-color:var(--danger); color:var(--danger); text-decoration:line-through;}
  .chip.excl .cross{display:inline;}
  /* ---- karty przepisow ---- */
  .card{display:block; width:100%; text-align:left; background:var(--surface); border:2px solid var(--border);
    border-radius:var(--radius); padding:18px 18px; margin-bottom:14px; cursor:pointer;}
  .card:active{border-color:var(--clay);}
  .card h3{font-size:1.3rem; margin:0 0 10px; color:var(--clay-dark);}
  .metarow{display:flex; flex-wrap:wrap; gap:8px; align-items:center;}
  .badge{background:var(--green-soft); color:var(--green); border-radius:999px; padding:5px 14px;
    font-size:.95rem; font-weight:700;}
  .catbadge{background:var(--clay-soft); color:var(--clay-dark); border-radius:999px; padding:5px 14px;
    font-size:.9rem; font-weight:700;}
  .card .go{color:var(--clay); font-weight:700; margin-top:12px; font-size:1.05rem;}
  /* ---- szczegol przepisu ---- */
  .rtitle{font-size:1.6rem; margin:0 0 12px; color:var(--clay-dark);}
  .infogrid{display:flex; flex-wrap:wrap; gap:8px; margin-bottom:6px;}
  .seclabel{font-size:.95rem; font-weight:700; color:var(--clay-dark); text-transform:uppercase;
    letter-spacing:.5px; margin:22px 0 8px; border-bottom:2px solid var(--clay-soft); padding-bottom:6px;}
  .alerts{display:flex; flex-wrap:wrap; gap:8px; margin-top:4px;}
  .alert-pill{background:#F7ECE7; color:#9a4a2c; border:1px solid #e6c3b4; border-radius:999px;
    padding:5px 14px; font-size:.95rem; font-weight:600;}
  .alert-none{color:var(--green); font-weight:700;}
  ul.ing{list-style:none; padding:0; margin:0;}
  ul.ing li{display:flex; justify-content:space-between; gap:12px; padding:11px 2px;
    border-bottom:1px dotted var(--border); font-size:1.08rem;}
  ul.ing li .amt{color:var(--clay-dark); font-weight:700; white-space:nowrap;}
  ol.steps{padding-left:26px; margin:0;}
  ol.steps li{margin-bottom:12px; font-size:1.08rem;}
  .actions{display:flex; flex-direction:column; gap:12px; margin-top:26px;}
  .btn-send{min-height:72px; background:var(--clay-dark); color:#fff; border:none; border-radius:var(--radius);
    font-size:1.25rem; font-weight:800; cursor:pointer;}
  .btn-send:active{background:#6a3a31;}
  .btn-save{min-height:66px; background:var(--green-soft); color:var(--green); border:2px solid #bcd6b0;
    border-radius:var(--radius); font-size:1.15rem; font-weight:800; cursor:pointer;}
  .btn-save.saved{background:#eef3ec;}
  .btn-remove{min-height:60px; background:#F7ECE7; color:var(--danger); border:2px solid #e6c3b4;
    border-radius:var(--radius); font-size:1.05rem; font-weight:700; cursor:pointer;}
  /* ---- zapisane ---- */
  .saved-group h2{font-size:1.25rem; color:var(--clay-dark); margin:22px 0 10px;}
  .saved-item{display:flex; align-items:center; gap:12px; background:var(--surface);
    border:2px solid var(--border); border-radius:14px; padding:14px 16px; margin-bottom:10px;}
  .saved-item .name{flex:1; font-size:1.1rem; font-weight:600; cursor:pointer;}
  .saved-item .mini{min-width:48px; min-height:48px; border-radius:12px; border:none; cursor:pointer;
    font-size:1.2rem;}
  .mini.open{background:var(--clay-soft); color:var(--clay-dark);}
  .mini.del{background:#F7ECE7; color:var(--danger);}
  .empty{text-align:center; color:var(--muted); padding:40px 10px;}
  .empty .big{font-size:3rem; display:block; margin-bottom:10px;}
  /* ---- toast + modal ---- */
  .toast{position:fixed; left:50%; bottom:calc(24px + env(safe-area-inset-bottom));
    transform:translateX(-50%) translateY(20px); background:var(--ink); color:#fff;
    padding:16px 22px; border-radius:14px; font-size:1.05rem; font-weight:600; max-width:90%;
    text-align:center; opacity:0; pointer-events:none; transition:opacity .25s, transform .25s; z-index:50;}
  .toast.show{opacity:1; transform:translateX(-50%) translateY(0);}
  .modal{position:fixed; inset:0; background:rgba(0,0,0,.5); display:flex; align-items:center;
    justify-content:center; padding:20px; z-index:60;}
  .modal .box{background:var(--surface); border-radius:18px; padding:20px; max-width:520px; width:100%;}
  .modal h3{margin:0 0 12px; color:var(--clay-dark);}
  .modal textarea{width:100%; height:220px; font-size:1rem; padding:12px; border:2px solid var(--border);
    border-radius:12px; resize:none;}
  /* ---- focus ---- */
  button:focus-visible, .card:focus-visible{outline:3px solid var(--focus); outline-offset:2px;}
  @media (prefers-reduced-motion: reduce){ *{transition:none !important;} }
</style>
</head>
<body>
<div class="app">
  <header class="appbar">
    <button class="iconbtn ghost" id="backBtn" data-action="back" aria-label="Wstecz" style="visibility:hidden">‹</button>
    <div class="title" id="barTitle">Nasza Kuchnia</div>
    <button class="iconbtn" id="homeBtn" data-action="home" aria-label="Ekran główny">⌂</button>
  </header>
  <main id="main" aria-live="polite"></main>
</div>
<div class="toast" id="toast" role="status"></div>

<script>
const APP_DATA = @@APP_DATA@@;
const RECIPES = APP_DATA.recipes;
const GROUPS = APP_DATA.groups;
const MEALS = APP_DATA.meals;
const byId = Object.fromEntries(RECIPES.map(r=>[r.id,r]));
const mealLabel = Object.fromEntries(MEALS.map(m=>[m.key,m.label]));
const GROUP_ORDER = ["Mięso i jaja","Ryby","Nabiał","Kasze i pieczywo","Warzywa","Owoce","Tłuszcze i orzechy","Inne"];
const AL_LABEL = {gluten:"gluten", mleko:"nabiał / mleko", jaja:"jaja", ryby:"ryby", orzechy:"orzechy"};

/* ---------- pamiec (localStorage z awaryjnym trybem) ---------- */
const store = (()=>{
  let mem={}; let has=false;
  try{ const k="__t"; localStorage.setItem(k,"1"); localStorage.removeItem(k); has=true; }catch(e){ has=false; }
  return {
    get(k){ try{ if(has){ const v=localStorage.getItem(k); return v?JSON.parse(v):null; } }catch(e){} return (k in mem)?mem[k]:null; },
    set(k,v){ try{ if(has){ localStorage.setItem(k,JSON.stringify(v)); return; } }catch(e){} mem[k]=v; }
  };
})();
const getSaved = ()=> store.get("mk_saved") || [];
const setSaved = (a)=> store.set("mk_saved", a);
const isSaved = (id)=> getSaved().some(r=>r.id===id);

/* ---------- stan + nawigacja ---------- */
let stack=[{view:"home"}];
let ctx={ meal:null, selected:new Set(), excluded:new Set(), results:[], offset:0 };
const main=document.getElementById("main");

function go(view, opts={}){ stack.push(Object.assign({view},opts)); render(); window.scrollTo(0,0); }
function back(){ if(stack.length>1){ stack.pop(); render(); window.scrollTo(0,0);} }
function home(){ stack=[{view:"home"}]; ctx.selected=new Set(); ctx.excluded=new Set(); render(); window.scrollTo(0,0); }

function render(){
  const top=stack[stack.length-1];
  document.getElementById("backBtn").style.visibility = stack.length>1 ? "visible":"hidden";
  const titles={home:"Nasza Kuchnia", meal:"Wybierz składniki", results:"Propozycje", recipe:"Przepis", saved:"Moje przepisy", search:"Szukaj po numerze"};
  document.getElementById("barTitle").textContent = titles[top.view]||"Nasza Kuchnia";
  if(top.view==="home") return renderHome();
  if(top.view==="meal") return renderMeal(top.meal);
  if(top.view==="results") return renderResults();
  if(top.view==="recipe") return renderRecipe(top.id);
  if(top.view==="saved") return renderSaved();
  if(top.view==="search") return renderSearch();
}
function numStr(n){ return String(n).padStart(3,"0"); }

/* ---------- ekran glowny ---------- */
function renderHome(){
  let h = '<p class="kicker">Co dziś gotujemy?</p>';
  h += '<h1 class="screen">Wybierz posiłek</h1>';
  h += '<p class="lead">Dotknij posiłek, potem zaznacz produkty, które masz. Pokażę 3 przepisy do wyboru.</p>';
  MEALS.forEach(m=>{
    h += '<button class="meal-btn" data-action="open-meal" data-meal="'+m.key+'">'+
         '<span class="emoji">'+m.emoji+'</span><span>'+m.label+'</span><span class="arrow">›</span></button>';
  });
  const n=getSaved().length;
  h += '<div class="saved-entry"><button class="meal-btn" data-action="go-saved">'+
       '<span class="emoji">⭐</span><span>Moje przepisy'+(n?(' ('+n+')'):'')+'</span><span class="arrow">›</span></button></div>';
  h += '<div class="saved-entry"><button class="meal-btn" data-action="go-search">'+
       '<span class="emoji">🔍</span><span>Szukaj po numerze</span><span class="arrow">›</span></button></div>';
  main.innerHTML=h;
}

/* ---------- wyszukiwarka po numerze ---------- */
function renderSearch(){
  let h='<h2 class="screen">Szukaj po numerze</h2>';
  h+='<p class="lead">Każdy przepis, który wysyłasz w wiadomości, ma swój numer. Wpisz go tutaj, aby szybko go odnaleźć.</p>';
  h+='<input class="search-input" id="searchNum" type="number" inputmode="numeric" min="1" placeholder="Numer przepisu, np. 042">';
  h+='<button class="primary-btn" data-action="do-search">Szukaj</button>';
  if(ctx.searchError!=null){
    h+='<p class="search-error">Nie znaleziono przepisu o numerze „'+ctx.searchError+'”. Sprawdź numer i spróbuj ponownie.</p>';
  }
  main.innerHTML=h;
  const inp=document.getElementById("searchNum");
  if(inp){
    inp.focus();
    inp.addEventListener("keydown", (e)=>{ if(e.key==="Enter"){ e.preventDefault(); doSearch(); } });
  }
}
function doSearch(){
  const inp=document.getElementById("searchNum");
  const raw=inp?inp.value.trim():"";
  const num=parseInt(raw,10);
  const found=RECIPES.find(r=>r.num===num);
  if(found){ ctx.searchError=null; go("recipe",{id:found.id}); }
  else{ ctx.searchError=raw||"?"; renderSearch(); }
}

/* ---------- ekran skladnikow ---------- */
function renderMeal(meal){
  ctx.meal=meal; ctx.selected=new Set(); ctx.excluded=new Set();
  const recipes=RECIPES.filter(r=>r.m.includes(meal));
  // zbierz dostepne skladniki (tagi) z przepisow tego posilku
  const tagset=new Set(); recipes.forEach(r=>r.tags.forEach(t=>tagset.add(t)));
  // pogrupuj
  const grouped={};
  [...tagset].forEach(t=>{ const g=GROUPS[t]||"Inne"; (grouped[g]=grouped[g]||[]).push(t); });
  let h='<h2 class="screen">'+mealLabel[meal]+'</h2>';
  h+='<p class="lead">Dotknij raz, aby zaznaczyć „mam w domu”. Dotknij ponownie, aby wykluczyć składnik, którego nie chcesz w przepisie. Trzeci dotyk czyści wybór. Nie musisz nic zaznaczać — wtedy pokażę propozycje dnia.</p>';
  h+='<div class="selbar"><div class="selcount" id="selcount">Mam: 0 · Bez: 0</div></div>';
  GROUP_ORDER.forEach(g=>{
    if(!grouped[g]) return;
    grouped[g].sort((a,b)=>a.localeCompare(b));
    h+='<div class="grouplabel">'+g+'</div><div class="chips">';
    grouped[g].forEach(t=>{
      h+='<button class="chip" data-action="toggle-ing" data-ing="'+t+'" aria-pressed="false">'+
         '<span class="tick">✓</span><span class="cross">✕</span>'+t+'</button>';
    });
    h+='</div>';
  });
  h+='<button class="primary-btn" data-action="show-results">Pokaż 3 przepisy</button>';
  main.innerHTML=h;
}
function updateSelCount(){
  const el=document.getElementById("selcount");
  if(el) el.textContent="Mam: "+ctx.selected.size+" · Bez: "+ctx.excluded.size;
}

/* ---------- dopasowanie + wyniki ---------- */
function rankRecipes(meal, selected, excluded){
  let list=RECIPES.filter(r=>r.m.includes(meal));
  if(excluded && excluded.size>0){
    list=list.filter(r=> !r.tags.some(t=>excluded.has(t)));
  }
  if(selected.size===0){ return shuffle(list.slice()); }
  return list.map(r=>{
    let score=0; r.tags.forEach(t=>{ if(selected.has(t)) score++; });
    return {r,score};
  }).sort((a,b)=> b.score-a.score || a.r.t.localeCompare(b.r.t)).map(x=>x.r);
}
function shuffle(a){ for(let i=a.length-1;i>0;i--){ const j=Math.floor(Math.random()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; }

function showResults(){
  ctx.results=rankRecipes(ctx.meal, ctx.selected, ctx.excluded);
  ctx.offset=0;
  go("results");
}
function threeNow(){
  const n=ctx.results.length, out=[];
  for(let i=0;i<Math.min(3,n);i++){ out.push(ctx.results[(ctx.offset+i)%n]); }
  return out;
}
function renderResults(){
  if(ctx.results.length===0){
    let h='<h2 class="screen">Wybierz przepis</h2>';
    h+='<div class="empty"><span class="big">🙈</span>Nie znalazłam przepisu bez wybranych składników.<br>Spróbuj odznaczyć któryś z wykluczonych produktów.</div>';
    h+='<button class="primary-btn" data-action="back">Wróć i zmień wybór</button>';
    main.innerHTML=h; return;
  }
  const three=threeNow();
  let h='<h2 class="screen">Wybierz przepis</h2>';
  const parts=[];
  if(ctx.selected.size>0) parts.push('Dopasowane do: '+[...ctx.selected].join(", "));
  if(ctx.excluded.size>0) parts.push('Bez: '+[...ctx.excluded].join(", "));
  if(parts.length){
    h+='<p class="lead">'+parts.join(" · ")+'.</p>';
  }else{
    h+='<p class="lead">Trzy propozycje na '+mealLabel[ctx.meal].toLowerCase()+'.</p>';
  }
  three.forEach(r=>{
    h+='<button class="card" data-action="open-recipe" data-id="'+r.id+'">'+
       '<h3>'+r.t+'</h3><div class="metarow">'+
       '<span class="badge">ok. '+r.kcal+' kcal</span>'+
       '<span class="catbadge">'+r.c+'</span>'+ allergTiny(r) +
       '</div><div class="go">Zobacz przepis ›</div></button>';
  });
  h+='<button class="ghost-btn" data-action="more-results">Pokaż inne propozycje ↻</button>';
  main.innerHTML=h;
}
function allergTiny(r){
  if(!r.al.length) return '<span class="badge" style="background:#E9F1E4;color:#4F6A3F;">bez alergenów</span>';
  return '<span class="catbadge">alergeny: '+r.al.map(a=>AL_LABEL[a]).join(", ")+'</span>';
}

/* ---------- szczegol przepisu ---------- */
function renderRecipe(id){
  const r=byId[id]; const saved=isSaved(id);
  let h='<h1 class="rtitle">'+r.t+'</h1>';
  h+='<div class="infogrid"><span class="badge">ok. '+r.kcal+' kcal · 1 porcja</span>'+
     '<span class="catbadge">Nr '+numStr(r.num)+'</span>'+
     '<span class="catbadge">'+r.c+'</span>'+
     '<span class="catbadge">'+r.m.map(m=>mealLabel[m]).join(" · ")+'</span></div>';
  h+='<div class="seclabel">Alergeny</div>';
  if(r.al.length){
    h+='<div class="alerts">'+r.al.map(a=>'<span class="alert-pill">'+AL_LABEL[a]+'</span>').join("")+'</div>';
  }else{
    h+='<div class="alert-none">Brak typowych alergenów</div>';
  }
  h+='<div class="seclabel">Składniki (na 1 osobę)</div><ul class="ing">';
  r.ing.forEach(([n,a])=>{ h+='<li><span>'+n+'</span><span class="amt">'+a+'</span></li>'; });
  h+='</ul>';
  h+='<div class="seclabel">Przygotowanie</div><ol class="steps">';
  r.steps.forEach(s=>{ h+='<li>'+s+'</li>'; });
  h+='</ol>';
  h+='<div class="actions">';
  h+='<button class="btn-send" data-action="share" data-id="'+id+'">📤 Wyślij przepis</button>';
  if(saved){
    h+='<button class="btn-save saved" disabled>✓ Zapisano w „Moje przepisy”</button>';
    h+='<button class="btn-remove" data-action="remove-saved" data-id="'+id+'">Usuń z zapisanych</button>';
  }else{
    h+='<button class="btn-save" data-action="save" data-id="'+id+'">⭐ Zapisz przepis</button>';
  }
  h+='</div>';
  main.innerHTML=h;
}

/* ---------- moje przepisy ---------- */
function renderSaved(){
  const saved=getSaved();
  if(!saved.length){
    main.innerHTML='<h2 class="screen">Moje przepisy</h2>'+
      '<div class="empty"><span class="big">⭐</span>Nie masz jeszcze zapisanych przepisów.<br>'+
      'Otwórz dowolny przepis i dotknij „Zapisz przepis”.</div>'+
      '<button class="primary-btn" data-action="home">Wróć do wyboru posiłku</button>';
    return;
  }
  // grupuj po kategorii
  const groups={};
  saved.forEach(r=>{ (groups[r.c]=groups[r.c]||[]).push(r); });
  let h='<h2 class="screen">Moje przepisy</h2>';
  h+='<p class="lead">Zapisane przepisy, uporządkowane w kategoriach.</p>';
  Object.keys(groups).sort((a,b)=>a.localeCompare(b)).forEach(cat=>{
    h+='<div class="saved-group"><h2>'+cat+'</h2>';
    groups[cat].forEach(r=>{
      h+='<div class="saved-item">'+
         '<span class="name" data-action="open-recipe" data-id="'+r.id+'">'+r.t+'</span>'+
         '<button class="mini open" data-action="open-recipe" data-id="'+r.id+'" aria-label="Otwórz">›</button>'+
         '<button class="mini del" data-action="remove-saved" data-id="'+r.id+'" aria-label="Usuń">🗑</button>'+
         '</div>';
    });
    h+='</div>';
  });
  main.innerHTML=h;
}

/* ---------- wysylanie ---------- */
function recipeText(r){
  const L=[];
  L.push(r.t);
  L.push("Numer przepisu: "+numStr(r.num));
  L.push("Kaloryczność: ok. "+r.kcal+" kcal (1 porcja)");
  L.push("Alergeny: "+(r.al.length? r.al.map(a=>AL_LABEL[a]).join(", "):"brak typowych"));
  L.push("");
  L.push("Składniki (na 1 osobę):");
  r.ing.forEach(([n,a])=>L.push("• "+n+" — "+a));
  L.push("");
  L.push("Przygotowanie:");
  r.steps.forEach((s,i)=>L.push((i+1)+". "+s));
  L.push("");
  L.push("Ten przepis znajdziesz w aplikacji, wpisując numer "+numStr(r.num)+" w wyszukiwarce.");
  L.push("— Nasza Kuchnia");
  return L.join("\n");
}
async function shareRecipe(id){
  const r=byId[id]; const text=recipeText(r);
  if(navigator.share){
    try{ await navigator.share({title:r.t, text:text}); return; }
    catch(e){ if(e && e.name==="AbortError") return; }
  }
  try{ await navigator.clipboard.writeText(text); toast("Skopiowano przepis — wklej w wiadomości"); return; }catch(e){}
  showCopyModal(text);
}
function showCopyModal(text){
  const wrap=document.createElement("div");
  wrap.className="modal"; wrap.id="copyModal";
  wrap.innerHTML='<div class="box"><h3>Skopiuj przepis</h3>'+
    '<textarea readonly>'+text.replace(/</g,"&lt;")+'</textarea>'+
    '<button class="primary-btn" data-action="close-modal">Gotowe</button></div>';
  document.body.appendChild(wrap);
  const ta=wrap.querySelector("textarea"); ta.focus(); ta.select();
}

/* ---------- toast ---------- */
let toastT=null;
function toast(msg){
  const t=document.getElementById("toast");
  t.textContent=msg; t.classList.add("show");
  clearTimeout(toastT); toastT=setTimeout(()=>t.classList.remove("show"), 2600);
}

/* ---------- delegacja klikniec ---------- */
document.body.addEventListener("click", (e)=>{
  const t=e.target.closest("[data-action]"); if(!t) return;
  const a=t.dataset.action;
  if(a==="back") return back();
  if(a==="home") return home();
  if(a==="open-meal") return go("meal",{meal:t.dataset.meal});
  if(a==="go-saved") return go("saved");
  if(a==="go-search"){ ctx.searchError=null; return go("search"); }
  if(a==="do-search") return doSearch();
  if(a==="toggle-ing"){
    const ing=t.dataset.ing;
    if(ctx.selected.has(ing)){
      ctx.selected.delete(ing); ctx.excluded.add(ing);
      t.classList.remove("on"); t.classList.add("excl"); t.setAttribute("aria-pressed","true");
    } else if(ctx.excluded.has(ing)){
      ctx.excluded.delete(ing);
      t.classList.remove("excl"); t.setAttribute("aria-pressed","false");
    } else {
      ctx.selected.add(ing);
      t.classList.add("on"); t.setAttribute("aria-pressed","true");
    }
    return updateSelCount();
  }
  if(a==="show-results") return showResults();
  if(a==="more-results"){ const n=ctx.results.length; ctx.offset=(ctx.offset+3)%(n||1); return renderResults(); }
  if(a==="open-recipe") return go("recipe",{id:t.dataset.id});
  if(a==="share") return shareRecipe(t.dataset.id);
  if(a==="save"){ const s=getSaved(); if(!s.some(r=>r.id===t.dataset.id)){ s.push(byId[t.dataset.id]); setSaved(s);} toast('Zapisano w „Moje przepisy” ✓'); return renderRecipe(t.dataset.id); }
  if(a==="remove-saved"){ setSaved(getSaved().filter(r=>r.id!==t.dataset.id)); toast("Usunięto przepis");
     const top=stack[stack.length-1]; if(top.view==="saved") return renderSaved(); return renderRecipe(t.dataset.id); }
  if(a==="close-modal"){ const m=document.getElementById("copyModal"); if(m) m.remove(); return; }
});

/* ---------- PWA: service worker ---------- */
if("serviceWorker" in navigator){
  window.addEventListener("load", ()=>{ navigator.serviceWorker.register("sw.js").catch(()=>{}); });
}

render();
</script>
</body>
</html>
"""

html = HTML.replace("@@APP_DATA@@", data_json)
with open(os.path.join(OUT,"index.html"),"w",encoding="utf-8") as f:
    f.write(html)

# ---- manifest ----
manifest = {
    "name":"Nasza Kuchnia","short_name":"Nasza Kuchnia",
    "description":"Proste przepisy zgodne z dietą mamy karmiącej.",
    "start_url":"./","scope":"./","display":"standalone",
    "background_color":"#FBF6F0","theme_color":"#7E463C","lang":"pl","orientation":"portrait",
    "icons":[
        {"src":"icon-192.png","sizes":"192x192","type":"image/png","purpose":"any"},
        {"src":"icon-512.png","sizes":"512x512","type":"image/png","purpose":"any"},
        {"src":"icon-maskable-512.png","sizes":"512x512","type":"image/png","purpose":"maskable"}
    ]
}
with open(os.path.join(OUT,"manifest.webmanifest"),"w",encoding="utf-8") as f:
    json.dump(manifest,f,ensure_ascii=False,indent=2)

# ---- service worker ----
# nazwa cache zalezy od hasha wygenerowanego index.html, wiec kazda zmiana
# tresci (przepisy, kod) automatycznie unieważnia stary cache PWA u uzytkownikow
sw_version = hashlib.sha1(html.encode("utf-8")).hexdigest()[:10]
sw = """const CACHE="nasza-kuchnia-@@SW_VERSION@@";
const ASSETS=["./","./index.html","./manifest.webmanifest",
  "./icon-192.png","./icon-512.png","./icon-maskable-512.png","./apple-touch-icon.png"];
self.addEventListener("install",e=>{
  e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)).then(()=>self.skipWaiting()));
});
self.addEventListener("activate",e=>{
  e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim()));
});
self.addEventListener("fetch",e=>{
  if(e.request.method!=="GET") return;
  e.respondWith(
    caches.match(e.request).then(hit=> hit || fetch(e.request).then(res=>{
      const copy=res.clone();
      caches.open(CACHE).then(c=>c.put(e.request,copy)).catch(()=>{});
      return res;
    }).catch(()=>caches.match("./index.html")))
  );
});
""".replace("@@SW_VERSION@@", sw_version)
with open(os.path.join(OUT,"sw.js"),"w",encoding="utf-8") as f:
    f.write(sw)

print("OK — przepisów:", len(recipes))
print("Pliki:", [f for f in os.listdir(OUT) if not f.endswith(".py")])
