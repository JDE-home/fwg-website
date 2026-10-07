const burger=document.querySelector('.burger'),menu=document.querySelector('.menu');
burger?.addEventListener('click',()=>{const o=menu.classList.toggle('open');burger.setAttribute('aria-expanded',o)});
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
document.querySelectorAll('[data-count]').forEach(el=>{const t=+el.dataset.count,s=el.dataset.suffix||'';let n=0;const o=new IntersectionObserver(([e])=>{if(!e.isIntersecting)return;o.disconnect();const st=performance.now();(function f(now){const p=Math.min((now-st)/1400,1);el.textContent=Math.round(t*(1-Math.pow(1-p,3)))+s;if(p<1)requestAnimationFrame(f)})(st)});o.observe(el)});
// Kontaktformulare -> api/contact.php
document.querySelectorAll('form[data-contact]').forEach(f=>{
  const ts=f.querySelector('[name=ts]'),status=f.querySelector('.form-status'),btn=f.querySelector('button[type=submit]');
  ts.value=Date.now();
  const show=(m,ok)=>{status.textContent=m;status.className='form-status '+(ok?'ok':'err')};
  f.addEventListener('submit',async e=>{
    e.preventDefault();
    f.querySelectorAll('.invalid').forEach(x=>x.classList.remove('invalid'));
    if(!f.checkValidity()){const bad=f.querySelector(':invalid');bad.classList.add('invalid');bad.focus();show(bad.name==='privacy'?'Bitte stimmen Sie der Datenschutzerklärung zu.':'Bitte füllen Sie alle Pflichtfelder korrekt aus.',false);return}
    btn.disabled=true;const label=btn.textContent;btn.textContent='Wird gesendet …';show('',true);
    try{
      const r=await fetch(f.action,{method:'POST',body:new FormData(f),headers:{Accept:'application/json'}});
      let d={};try{d=await r.json()}catch{}
      if(r.ok&&d.ok){show(d.message,true);f.reset();ts.value=Date.now()}
      else{if(d.errors)for(const k in d.errors)f.querySelector(`[name=${k}]`)?.classList.add('invalid');show(d.message||'Das Senden ist fehlgeschlagen.',false)}
    }catch{show('Keine Verbindung zum Server. Bitte schreiben Sie uns an info@fwg-oelde.de.',false)}
    btn.disabled=false;btn.textContent=label;
  });
});
