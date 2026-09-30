const fs=require('fs'),path=require('path'),crypto=require('crypto');
const {chromium}=require('playwright');
(async()=>{
 const dir=__dirname, html=fs.readFileSync(path.join(dir,'newsletter.html'),'utf8');
 const browser=await chromium.launch({headless:true,executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'});
 const results=[];
 for(const width of [600,320,390,430]){
  for(const stripped of [false,true]){
   const page=await browser.newPage({viewport:{width,height:900},deviceScaleFactor:1});
   await page.route('https://raw.githubusercontent.com/elaiskai/insanefits-email-assets/main/campaigns/2026-09/proteino-receptu-knyga/**', route=>{
    const relative=new URL(route.request().url()).pathname.split('/proteino-receptu-knyga/')[1];
    return route.fulfill({path:path.join(dir,relative)});
   });
   await page.goto('file://'+path.join(dir,'newsletter.html'));
   if(stripped)await page.evaluate(()=>document.querySelectorAll('head style,head link').forEach(e=>e.remove()));
   await page.evaluate(()=>document.fonts.ready);
   const name=`${width}${stripped?'-stripped':''}`;
   await page.screenshot({path:path.join(dir,name+'.jpg'),fullPage:true,type:'jpeg',quality:85});
   results.push({name,...await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,images:[...document.images].every(i=>i.complete&&i.naturalWidth),cta:[...document.querySelectorAll('.cta')].map(a=>a.getBoundingClientRect().height),dashes:/[\u2010-\u2015\u2212-]/.test(document.body.innerText)}))});
   await page.close();
  }
 }
 fs.writeFileSync(path.join(dir,'qa.json'),JSON.stringify({sha256:crypto.createHash('sha256').update(html).digest('hex'),results},null,2));
 console.log(results);await browser.close();
 if(results.some(r=>r.overflow||!r.images||r.dashes||r.cta.some(h=>h<44)))process.exitCode=1;
})();
