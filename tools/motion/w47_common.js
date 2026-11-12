// shared motion helpers (GSAP timeline, seekable by render.js)
const tl = gsap.timeline({paused:true});
const IN = {opacity:0, y:90, scale:1.5, filter:'blur(20px)'};
function words(sel, t, st=0.11, dur=0.38){ tl.from(sel+' .w', {...IN, duration:dur, ease:'back.out(2.2)', stagger:st}, t); }
function shake(t, k=1){ tl.to('#cam', {keyframes:[{x:-16*k,y:10*k},{x:14*k,y:-8*k},{x:-8*k,y:5*k},{x:4*k,y:-2*k},{x:0,y:0}], duration:0.28, ease:'none'}, t); }
function flash(t, a=0.85){ tl.fromTo('#flash',{opacity:0},{opacity:a,duration:0.07,ease:'none'},t).to('#flash',{opacity:0,duration:0.35,ease:'power2.out'},t+0.07); }
function show(s,t){ tl.set(s,{visibility:'visible'},t); } function hide(s,t){ tl.set(s,{visibility:'hidden'},t); }
function enter(s,t,how){
  show(s,t);
  if(how==='x') tl.from(s,{x:1150,filter:'blur(30px)',duration:0.36,ease:'power3.out'},t);
  if(how==='-x') tl.from(s,{x:-1150,filter:'blur(30px)',duration:0.36,ease:'power3.out'},t);
  if(how==='y') tl.from(s,{y:1920,filter:'blur(30px)',duration:0.36,ease:'power3.out'},t);
  if(how==='z') tl.from(s,{scale:2.2,opacity:0,filter:'blur(30px)',duration:0.4,ease:'expo.out'},t);
}
function leave(s,t,how){
  if(how==='x') tl.to(s,{x:-1150,filter:'blur(30px)',duration:0.28,ease:'power3.in'},t);
  else tl.to(s,{opacity:0,filter:'blur(24px)',scale:0.9,duration:0.28,ease:'power2.in'},t);
  hide(s,t+0.3);
}
function base(D){
  tl.to('#prog',{scaleX:1,duration:D,ease:'none'},0);
  tl.fromTo('#grid',{backgroundPosition:'0px 0px'},{backgroundPosition:'0px 540px',duration:D,ease:'none'},0);
}
function endCard(t){
  show('#end',t-0.05);
  tl.from('#plate',{scale:0.4,opacity:0,filter:'blur(20px)',duration:0.45,ease:'back.out(2)'},t); flash(t+0.02,0.45);
  words('#e1',t+0.25,0.12); words('#e2',t+0.6,0.13);
  tl.from('#pill',{scale:0,opacity:0,duration:0.45,ease:'back.out(3)'},t+1.0);
  tl.to('#pill',{scale:1.07,duration:0.3,yoyo:true,repeat:1,ease:'sine.inOut'},t+1.55);
  tl.from('#e3',{opacity:0,y:30,duration:0.35},t+1.3);
}
function finish(){ window.seek = t => { tl.seek(t, false); }; window.READY = true; }
