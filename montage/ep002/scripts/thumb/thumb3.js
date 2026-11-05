// usage: node thumb3.js name "line1" "line2" "tag" photo.jpg [left top width font tagTop]
const {chromium}=require('playwright');const fs=require('fs');
const [n,l1,l2,tag,photo,L='190px',T='40px',W='1450px',FS='122px',TT='330px']=process.argv.slice(2);
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});
 const gl=(parseInt(L)-520)+'px';
 let h=fs.readFileSync('thumb3.html','utf8').replace('L1',l1).replace('L2',l2).replace('TAG',tag).replace('PHOTO',photo)
  .replace(/VAR_L/g,L).replace('VAR_GL',gl).replace('VAR_T',T).replace(/VAR_W/g,W).replace('VAR_FS',FS).replace('VAR_TT',TT)
  .replace('VAR_C1',(parseInt(TT)-34)+'px').replace('VAR_C2',(parseInt(TT)+92)+'px');
 fs.writeFileSync('t3_'+n+'.html',h);await p.goto('file://'+process.cwd()+'/t3_'+n+'.html');await p.waitForTimeout(300);
 await p.screenshot({path:'thumb_'+n+'.png'});await b.close();})();
