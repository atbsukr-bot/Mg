const {chromium}=require('playwright');const fs=require('fs');
const V=[['v1','اتصال من','رقم مفصول!','الساعة 2:17 الفجر'],['v2','لا تفتحون','الباب الرابع!','بلاغ بلا عنوان']];
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1280,height:720}});
for(const [n,l1,l2,tag] of V){let h=fs.readFileSync('thumb.html','utf8').replace('L1',l1).replace('L2',l2).replace('TAG',tag)
 .replace('VAR_L','190px').replace('VAR_T','40px').replace('VAR_W','1450px').replace('VAR_FS','104px').replace('VAR_TT','355px');
 fs.writeFileSync('t_'+n+'.html',h);await p.goto('file://'+process.cwd()+'/t_'+n+'.html');await p.waitForTimeout(300);
 await p.screenshot({path:'thumb_'+n+'.png'});}
await b.close();})();
