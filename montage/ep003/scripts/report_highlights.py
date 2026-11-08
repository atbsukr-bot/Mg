# Render report pages and highlight the quoted phrases (yellow), save to public/evidence.
import subprocess, re, sys, cv2, numpy as np, xml.etree.ElementTree as ET
PDF='work/dl/pma.pdf'; OUT='public/evidence/'; DPI=170
jobs=[(1,None,'08_report_cover.png'),
      (24,['1,031 lives lost','387 persons','710 are missing'],'09_report_toll_map.png'),
      (68,['The fire alarm detected at the panel was reset','avoid sounding the alarm'],'10_report_alarm.png'),
      (43,['turn off the lights of the bridge','vessels in the vicinity from seeing them'],'11_report_lights.png'),
      (42,['do not disturb us, lets us work'],'11b_report_dont_disturb.png'),
      (50,['just wait','send a may day send may day','The ship sank at 2333 hours'],'12_report_mayday.png'),
      (70,['The master did not accept the recommendations of his officers to','contact vessels in the vicinity, the company, or the authorities.','he ignored the recommendations to abandon ship.','The master also refused to be seen by other vessels in the vicinity,','The abandon ship operation was neither ordered nor carried out at'],'13_report_conclusions.png')]
for page,phr,name in jobs:
    subprocess.run(['pdftoppm','-f',str(page),'-l',str(page),'-r',str(DPI),'-png','-singlefile',PDF,'/tmp/pg'],check=True)
    im=cv2.imread('/tmp/pg.png'); H,W=im.shape[:2]
    if phr:
        x=subprocess.run(['pdftotext','-f',str(page),'-l',str(page),'-bbox','-q',PDF,'-'],capture_output=True,text=True).stdout
        x=re.sub(r'<!DOCTYPE[^>]*>','',x); root=ET.fromstring(x.replace('xmlns="http://www.w3.org/1999/xhtml"',''))
        pg=root.find('.//page'); pw=float(pg.get('width')); s=W/pw
        words=[(w.text or '',*(float(w.get(k))*s for k in ('xMin','yMin','xMax','yMax'))) for w in pg.iter('word')]
        toks=[w[0].lower().strip('.,:;"“”') for w in words]
        ov=im.copy(); hits=0
        for p in phr:
            pt=[t.lower().strip('.,:;"“”') for t in p.split()]
            for i in range(len(toks)-len(pt)+1):
                if toks[i:i+len(pt)]==pt:
                    for w in words[i:i+len(pt)]:
                        cv2.rectangle(ov,(int(w[1])-2,int(w[2])-2),(int(w[3])+2,int(w[4])+2),(80,230,255),-1); hits+=1
        im=cv2.addWeighted(ov,0.45,im,0.55,0)
        print(name,'highlighted words',hits)
    cv2.imwrite(OUT+name,im)
