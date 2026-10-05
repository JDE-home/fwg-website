const burger=document.querySelector('.burger'),menu=document.querySelector('.menu');
burger?.addEventListener('click',()=>{const o=menu.classList.toggle('open');burger.setAttribute('aria-expanded',o)});
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
document.querySelectorAll('[data-count]').forEach(el=>{const t=+el.dataset.count,s=el.dataset.suffix||'';let n=0;const o=new IntersectionObserver(([e])=>{if(!e.isIntersecting)return;o.disconnect();const st=performance.now();(function f(now){const p=Math.min((now-st)/1400,1);el.textContent=Math.round(t*(1-Math.pow(1-p,3)))+s;if(p<1)requestAnimationFrame(f)})(st)});o.observe(el)});
document.querySelectorAll('form[data-demo]').forEach(f=>f.addEventListener('submit',e=>{e.preventDefault();f.querySelector('.success').style.display='block';f.reset()}));
