const D = 13.0;
const tl = gsap.timeline({paused:true});
const IN = {opacity:0, y:90, scale:1.5, filter:'blur(20px)'};
function words(sel, t, st=0.11, dur=0.38){ tl.from(sel+' .w', {...IN, duration:dur, ease:'back.out(2.2)', stagger:st}, t); }
function shake(t, k=1){ tl.to('#cam', {keyframes:[{x:-16*k,y:10*k},{x:14*k,y:-8*k},{x:-8*k,y:5*k},{x:4*k,y:-2*k},{x:0,y:0}], duration:0.28, ease:'none'}, t); }
function flash(t, a=0.85){ tl.fromTo('#flash',{opacity:0},{opacity:a,duration:0.07,ease:'none'},t).to('#flash',{opacity:0,duration:0.35,ease:'power2.out'},t+0.07); }
function show(s,t){ tl.set(s,{visibility:'visible'},t); } function hide(s,t){ tl.set(s,{visibility:'hidden'},t); }
function out(s,t){ tl.to(s,{opacity:0,scale:0.8,filter:'blur(16px)',duration:0.2,ease:'power2.in'},t); }
tl.to('#prog',{scaleX:1,duration:D,ease:'none'},0);
// HOOK on plain bag (desaturated) 0-2.8
tl.set('#A .photo img',{filter:'saturate(0.25) brightness(0.85)'},0);
tl.fromTo('#A .photo img',{scale:1.3},{scale:1.0,duration:3.0,ease:'power1.out'},0);
words('#q1',0.05,0.12,0.36); shake(0.35,1.2);
words('#q1b',0.5,0.13,0.36); shake(0.85,0.8); flash(0.84,0.35);
tl.from('#q2 .w',{opacity:0,y:40,filter:'blur(12px)',duration:0.3,stagger:0.09},1.35);
// TRANSFORM 2.75
out(['#q1','#q1b','#q2'],2.6);
show('#B',2.75);
tl.fromTo('#B',{clipPath:'polygon(0% 0%, 0% 0%, 0% 100%, 0% 100%)'},{clipPath:'polygon(0% 0%, 130% 0%, 100% 100%, -30% 100%)',duration:0.55,ease:'power3.inOut'},2.75);
flash(3.15,0.9); shake(3.2,1.4); hide('#A',3.4);
tl.fromTo('#B .photo img',{scale:1.35},{scale:1.0,duration:3.6,ease:'power1.out'},2.75);
tl.fromTo('#B .streak',{x:-1500},{x:1500,duration:0.8,ease:'power2.inOut'},3.3);
show('#b1',3.4); show('#b2',3.4); words('#b1',3.45,0.14); words('#b2',3.8,0.14);
show('#k1',4.5); words('#k1',4.5,0.1,0.32); tl.to('#B .photo img',{scale:'+=0.06',duration:0.12,yoyo:true,repeat:1},4.52); shake(4.55,0.6); out('#k1',5.15);
show('#k2',5.25); words('#k2',5.25,0.1,0.32); tl.to('#B .photo img',{scale:'+=0.06',duration:0.12,yoyo:true,repeat:1},5.27); shake(5.3,0.6); out('#k2',5.9);
show('#k3',6.0); words('#k3',6.0,0.12,0.34); shake(6.1,0.6);
// WHIP to carton 6.9
out(['#b1','#b2','#k3'],6.75);
tl.to('#B',{x:-1150,filter:'blur(30px)',duration:0.3,ease:'power3.in'},6.85);
show('#C',7.0); tl.from('#C',{x:1150,filter:'blur(30px)',duration:0.38,ease:'power3.out'},7.0); flash(7.05,0.6); hide('#B',7.2);
tl.fromTo('#C .photo img',{scale:1.3},{scale:1.0,duration:2.6,ease:'power1.out'},7.0);
tl.fromTo('#C .streak',{x:-1500},{x:1500,duration:0.8,ease:'power2.inOut'},7.8);
show('#c1',7.3); show('#c2',7.3); words('#c1',7.35,0.13); words('#c2',7.7,0.13); shake(7.75,0.6);
// END 9.6
out(['#c1','#c2'],9.35);
tl.to('#C',{scale:0.85,opacity:0,filter:'blur(18px)',duration:0.35,ease:'power2.in'},9.4);
show('#end',9.6); hide('#C',9.85);
tl.from('#plate',{scale:0.4,opacity:0,filter:'blur(20px)',duration:0.45,ease:'back.out(2)'},9.65); flash(9.67,0.45);
words('#e1',9.9,0.12); words('#e2',10.25,0.13);
tl.from('#pill',{scale:0,opacity:0,duration:0.45,ease:'back.out(3)'},10.65);
tl.to('#pill',{scale:1.07,duration:0.3,yoyo:true,repeat:2,ease:'sine.inOut'},11.2);
tl.from('#e3',{opacity:0,y:30,duration:0.35},10.95);
window.seek = t => { tl.seek(t, false); };
window.READY = true;
