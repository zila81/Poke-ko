(()=>{const $=x=>document.getElementById(x);let D=null,F="kd",S=12,P="basic",Z=3;
function bits(h,w){let a=[];for(let i=0;i<h.length;i+=2){let b=parseInt(h.slice(i,i+2),16);for(let k=7;k>=0;k--)a.push((b>>k)&1)}return a.slice(0,w)}
function G(font,ch){return font.glyphs[String(ch.codePointAt(0))]}
function width(font,t){let n=0;for(const ch of t){let g=G(font,ch);n+=g?g.advance:Math.ceil(font.size/2)}return n}
function text(c,font,t,x,y,z){let pen=x;for(const ch of t){let g=G(font,ch);if(!g){pen+=Math.ceil(font.size/2)*z;continue}
let[w,h,xo,yo]=g.bbx;for(let r=0;r<g.rows.length;r++){let b=bits(g.rows[r],w);for(let q=0;q<w;q++)if(b[q])c.fillRect(pen+(xo+q)*z,y-(yo+h)*z+r*z,z,z)}pen+=g.advance*z}}
function render(){if(!D)return;let font=D.fonts[F+S],cv=$("koFontCanvas"),c=cv.getContext("2d");c.imageSmoothingEnabled=false;c.fillStyle="#050505";c.fillRect(0,0,cv.width,cv.height);c.fillStyle="#fff";let y=44;
for(const line of D.samples[P]){let w=width(font,line)*Z;text(c,font,line,Math.max(10,(cv.width-w)/2),y,Z);y+=(font.size+8)*Z}
$("koCoverage").innerHTML=`<b>${font.family} ${font.size}px</b> · glyph ${font.glyphCount} · `+(font.missing.length?`<span style="color:#d33">누락 ${font.missing.length} ❌</span>`:`<span style="color:#17833f">필수문자 누락 0 ✅</span>`);
$("koMissing").textContent=font.missing.length?font.missing.map(x=>x.codepoint+" "+x.char).join("  "):"BDF 필수 한국어 문자 전체 존재";}
async function init(){try{D=await(await fetch("font-preview.json",{cache:"no-store"})).json();$("koFamily").onchange=e=>{F=e.target.value;render()};$("koSize").onchange=e=>{S=+e.target.value;render()};$("koPreset").onchange=e=>{P=e.target.value;render()};$("koScale").oninput=e=>{Z=+e.target.value;render()};render()}catch(e){$("koCoverage").textContent="폰트 데이터 오류: "+e.message}}
document.readyState==="loading"?document.addEventListener("DOMContentLoaded",init):init()})();