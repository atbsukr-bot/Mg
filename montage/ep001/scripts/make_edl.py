"""ep001 «بلاغ بلا عنوان» — beat sheet → public/edl.json"""
import json
W=json.load(open('scripts/words_out.json'))
F=lambda i: W[i]['f0']
VOICE_END=1779; SCENE_END=1899; END=1950
# caption chunks: (word indices, display text per word, highlighted position)
CH=[
 ([0,1,2,3],['في','عندنا','جريمة','قتل'],2),
 ([4,5,6],['موجودة','بحي','الطين'],1),
 ([7,8,9,10,11],['في','عالم','من','الأمن','والأمان'],3),
 ([12,13,14,15],['يا','ربي','لك','الحمد'],3),
 ([16,17,18,19],['نكتشف','إن','أصغر','التفاصيل'],3),
 ([20,21,22],['ممكن','تكشف','لنا'],1),
 ([23,24,25],['أسرار','عميقة','جدًا'],0),
 ([26,27,28,29],['مثل…','قصتنا','لهذا','اليوم'],1),
 ([30,31,32,33],['يعني','جا','في','يوم'],3),
 ([34,35,36],['من','الأيام','والدنيا'],1),
 ([37,38,39],['كانت','كلها','هدوء'],2),
 ([40,41,42,43],['والمركز','ما','فيه','بلاغات'],3),
 ([44,45,46,47],['ولا','في','أي','شي'],3),
 ([48,49],['جا','اتصال'],1),
 ([50,51,52],['ألو،','السلام','عليكم'],0),
 ([53,54,55,56],['في','عندنا','جريمة','قتل'],3),
 ([57,58,59],['موجودة','بحي','الطين'],1),
 ([60,61,62],['ماذا؟','حدّد','الموقع'],2),
 ([63,64,65,66,67],['لا','أعرف…','ما','حدّد','الموقع'],1),
 ([68,69,70],['فاتجه','رجال','الأمن'],1),
 ([71,72],['إلى','الموقع'],1),
 ([73,74,75],['فلقوا','جريمة','بشكل'],1),
 ([76,77,78,79,80],['لا','تتخيل','يا','عزيزي','المشاهد'],1),
 ([81,82,83],['لدرجة','إنه','من…'],0),
 ([84,85,86,87],['لا','أستطيع','أن','أصف لكم'],1),
 ([88,89],['المشهد','بالضبط'],0),
 ([90,91,92,93,94],['فأضع','لكم','صورة','تقريبية','للمشهد'],2),
]
caps=[]
for idx,txt,h in CH:
    caps.append([dict(text=t,start=W[i]['f0'],end=W[i]['f1'],**({'hl':True} if k==h else {})) for k,(i,t) in enumerate(zip(idx,txt))])
caps.append([dict(text='مسرح',start=VOICE_END+4,end=VOICE_END+30),dict(text='الجريمة',start=VOICE_END+10,end=SCENE_END-2,hl=True)])
def S(a,b,bg,**k):
    d=dict(from_=a,dur=b-a,bg=bg); d.update(k); d['from']=d.pop('from_'); return d
el=lambda typ,at,**p: dict(type=typ,at=at,props=p)
scenes=[
 S(0,141,'head',look='bw',transition='flash',zoomSteps=[dict(**{'from':0},scale=1.12,y=40),dict(**{'from':57},scale=1.0)],elements=[
   el('headline',F(2)-0,text='جريمة قتل',variant='giant',y=330,size=190),
   el('tape',F(4)-0,text='مسرح جريمة • ممنوع الاقتراب',y=1080,rotate=-7)]),
 S(141,300,'head',look='warm',transition='glitch',zoomSteps=[dict(**{'from':0},scale=1.0),dict(**{'from':F(10)-141},scale=1.14,y=40)],elements=[
   el('headline',F(10)-141,text='الأمن والأمان',variant='paper',y=1120,size=86),
   el('tag',F(15)-141,text='الحمد لله',x=800,y=960,rotate=-8)]),
 S(300,465,'paper',transition='glitch',elements=[
   el('magnifier',0,x=540,y=860),
   el('headline',F(18)-300,text='أصغر التفاصيل',variant='ink',y=340),
   el('headline',F(23)-300,text='أسرار',variant='stamp',x=780,y=1130,rotate=-10)]),
 S(465,556,'paper',transition='glitch',elements=[
   el('casefile',F(27)-465,x=540,y=820,stampAt=F(29)-F(27)),
   el('tag',F(29)-465,text='اليوم',x=820,y=1120,rotate=-8,size=60)]),
 S(556,714,'paper',transition='glitch',elements=[
   el('headline',F(33)-556,text='يوم من الأيام',variant='ink',y=360),
   el('flatline',F(36)-556,x=540,y=820,label='المركز هادي'),
   el('headline',F(39)-556,text='هدوء…',variant='stamp',x=720,y=1140)]),
 S(714,815,'dark',elements=[
   el('reportlog',F(43)-714,x=540,y=760),
   el('tag',F(47)-714,text='ولا أي شي',x=760,y=1120,rotate=-6,filled=True)]),
 S(815,953,'head',look='warm',transition='glitch',zoomSteps=[dict(**{'from':0},scale=1.0),dict(**{'from':F(50)-815},scale=1.16,y=40)],elements=[
   el('call',F(49)-815,x=540,y=330,answerAt=F(50)-F(49))]),
 S(953,1092,'head',look='bw',transition='flash',zoomSteps=[dict(**{'from':0},scale=1.18,y=50),dict(**{'from':F(57)-953},scale=1.05)],elements=[
   el('headline',F(55)-953,text='جريمة قتل',variant='stamp',x=540,y=1150,size=110),
   el('tape',F(57)-953,text='مسرح جريمة • ممنوع الاقتراب',y=280,rotate=6)]),
 S(1092,1213,'paper',transition='glitch',elements=[
   el('map',0,lostAt=F(63)-1092),
   el('tag',F(67)-1092,text='موقع مجهول',x=540,y=1200,rotate=-5,filled=True,size=60)]),
 S(1213,1360,'dark',transition='flash',elements=[
   el('paths',0),
   el('siren',0,strength=0.6),
   el('tag',F(69)-1213,text='رجال الأمن',x=330,y=330,rotate=-6,size=64),
   el('headline',F(72)-1213,text='إلى الموقع',variant='plain',x=540,y=1240,size=90)]),
 S(1360,1545,'head',look='warm',transition='glitch',zoomSteps=[dict(**{'from':0},scale=1.0),dict(**{'from':F(74)-1360},scale=1.12,y=30),dict(**{'from':F(77)-1360},scale=1.22,y=60)],elements=[
   el('headline',F(77)-1360,text='لا تتخيل',variant='plain',x=540,y=1130,size=110)]),
 S(1545,1700,'head',look='bw',transition='glitch-bw',zoomSteps=[dict(**{'from':0},scale=1.15,y=40),dict(**{'from':F(84)-1545},scale=1.0)],elements=[
   el('tag',F(85)-1545,text='ما أقدر أوصفه',x=760,y=1080,rotate=-6,size=56)]),
 S(1700,VOICE_END,'head',look='warm',zoomSteps=[dict(**{'from':0},scale=1.0),dict(**{'from':F(92)-1700},scale=1.15,y=30)],elements=[
   el('tag',F(92)-1700,text='صورة تقريبية',x=540,y=1100,rotate=-4,filled=True,size=64)]),
 S(VOICE_END,SCENE_END,'dark',transition='flash',elements=[el('crimescene',0)]),
 S(SCENE_END,END,'dark',transition='glitch',elements=[el('endcard',0)]),
]
sfx=[dict(src='sfx/static.wav',at=0,volume=.35),dict(src='sfx/hit.wav',at=F(2),volume=.6),dict(src='sfx/stamp.wav',at=F(4),volume=.45),
 dict(src='sfx/glitch.wav',at=141,volume=.3),dict(src='sfx/pop.wav',at=F(10),volume=.45),dict(src='sfx/pop.wav',at=F(15),volume=.4),
 dict(src='sfx/glitch.wav',at=300,volume=.3),dict(src='sfx/whoosh.wav',at=314,volume=.4),dict(src='sfx/pop.wav',at=F(18),volume=.45),dict(src='sfx/stamp.wav',at=F(23),volume=.55),
 dict(src='sfx/whoosh.wav',at=F(27),volume=.4),dict(src='sfx/stamp.wav',at=F(29),volume=.6),
 dict(src='sfx/glitch.wav',at=556,volume=.3),dict(src='sfx/pop.wav',at=F(33),volume=.4),dict(src='sfx/stamp.wav',at=F(39),volume=.45),
 dict(src='sfx/whoosh.wav',at=F(43),volume=.35)]+[dict(src='sfx/tick.wav',at=F(43)+4+k*2,volume=.25) for k in range(10)]+[
 dict(src='sfx/pop.wav',at=F(47),volume=.45),
 dict(src='sfx/ring.wav',at=F(49),volume=.4),
 dict(src='sfx/hit.wav',at=F(55),volume=.6),dict(src='sfx/stamp.wav',at=F(55)+2,volume=.5),
 dict(src='sfx/glitch.wav',at=1092,volume=.3),dict(src='sfx/whoosh.wav',at=1100,volume=.35),dict(src='sfx/pop.wav',at=F(63),volume=.4),dict(src='sfx/pop.wav',at=F(67),volume=.45),
 dict(src='sfx/siren.wav',at=1213,volume=.28),dict(src='sfx/pop.wav',at=F(69),volume=.45),
 dict(src='sfx/glitch.wav',at=1360,volume=.3),dict(src='sfx/hit.wav',at=F(77),volume=.45),
 dict(src='sfx/glitch.wav',at=1545,volume=.35),dict(src='sfx/pop.wav',at=F(85),volume=.4),
 dict(src='sfx/pop.wav',at=F(92),volume=.45),
 dict(src='sfx/shutter.wav',at=VOICE_END,volume=.6),dict(src='sfx/heartbeat.wav',at=VOICE_END+6,volume=.6),
 dict(src='sfx/stamp.wav',at=VOICE_END+34,volume=.4),dict(src='sfx/stamp.wav',at=VOICE_END+44,volume=.4),dict(src='sfx/stamp.wav',at=VOICE_END+54,volume=.4),
 dict(src='sfx/glitch.wav',at=SCENE_END,volume=.35),dict(src='sfx/hit.wav',at=SCENE_END+2,volume=.5)]
edl=dict(fps=30,durationInFrames=END,aroll='aroll.mp4',voiceEnd=VOICE_END,scenes=scenes,captions=caps,sfx=sfx,music=dict(src='bed.wav',volume=.07))
json.dump(edl,open('public/edl.json','w'),ensure_ascii=False,indent=1)
print(len(scenes),'scenes',len(caps),'chunks',len(sfx),'sfx')
