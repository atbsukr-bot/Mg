import React from 'react';
import {AbsoluteFill} from 'remotion';

const RED = '#E3262A', INK = '#141414', Y = '#FFD23F';

function burst(cx: number, cy: number, r1: number, r2: number, n: number) {
  let d = '';
  for (let i = 0; i < n * 2; i++) {
    const a = (i / (n * 2)) * Math.PI * 2;
    const r = i % 2 ? r1 : r2 * (0.85 + 0.15 * Math.sin(i * 2.7));
    d += `${i ? 'L' : 'M'} ${cx + Math.cos(a) * r} ${cy + Math.sin(a) * r} `;
  }
  return d + 'Z';
}

const Check: React.FC<{t: string}> = ({t}) => (
  <div style={{display: 'flex', alignItems: 'center', gap: 16, direction: 'rtl'}}>
    <div style={{width: 50, height: 50, borderRadius: 14, background: RED, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>
      <svg width="34" height="34" viewBox="0 0 60 60"><path fill="none" stroke="#fff" strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" d="M12 31 l12 12 l24 -26" /></svg>
    </div>
    <span style={{fontFamily: 'Cairo', fontWeight: 800, fontSize: 40, color: '#fff', whiteSpace: 'nowrap'}}>{t}</span>
  </div>
);

export const AdCard: React.FC = () => {
  const PW = 330, PH = 640;
  return (
    <AbsoluteFill style={{background: INK, overflow: 'hidden'}}>
      {/* rays */}
      <svg width={1080} height={1080} style={{position: 'absolute'}}>
        {Array.from({length: 20}, (_, i) => { const a = (i / 20) * Math.PI * 2, b = a + 0.13; return <path key={i} d={`M 250 600 L ${250 + Math.cos(a) * 1500} ${600 + Math.sin(a) * 1500} L ${250 + Math.cos(b) * 1500} ${600 + Math.sin(b) * 1500} Z`} fill="#fff" opacity={0.035} />; })}
        <circle cx={250} cy={600} r={330} fill={RED} opacity={0.22} />
      </svg>

      {/* headline */}
      <div style={{position: 'absolute', right: 56, top: 54, direction: 'rtl', textAlign: 'right'}}>
        <div style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 116, lineHeight: 1.0, color: Y, WebkitTextStroke: `6px ${INK}`, paintOrder: 'stroke fill', textShadow: `0 8px 0 ${RED}`}}>مونتاج</div>
        <div style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 84, lineHeight: 1.1, color: '#fff', marginTop: 6}}>ريلز وفلوقات</div>
        <div style={{display: 'inline-block', marginTop: 16, background: RED, color: '#fff', fontFamily: 'Tajawal', fontWeight: 900, fontSize: 46, padding: '6px 26px 0', borderRadius: 14, transform: 'rotate(-2deg)'}}>يخلي مقطعك ينشاف</div>
      </div>

      {/* features */}
      <div style={{position: 'absolute', right: 56, top: 430, display: 'flex', flexDirection: 'column', gap: 18}}>
        <Check t="كتابة على الشاشة بلهجتك" />
        <Check t="زوم ومؤثرات وأصوات" />
        <Check t="موسيقى بدون حقوق" />
        <Check t="فلوقات يوتيوب كاملة" />
        <Check t="تعديل مجاني مرة" />
      </div>

      {/* phone mockup (illustration, no real footage) */}
      <div style={{position: 'absolute', left: 60, top: 200, width: PW, height: PH, borderRadius: 52, background: '#0b0b0b', border: '10px solid #2b2b2b', boxShadow: `0 30px 60px rgba(0,0,0,0.6), 0 0 0 4px ${RED}`, transform: 'rotate(-6deg)', overflow: 'hidden'}}>
        <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(160deg, #ff9a8b 0%, #ff6a88 40%, #6a5cff 100%)'}} />
        <svg width={PW} height={PH} style={{position: 'absolute', left: -10, top: -10}}>
          <path d={burst(170, 250, 95, 135, 14)} fill={INK} transform="translate(5 7)" />
          <path d={burst(170, 250, 95, 135, 14)} fill={Y} stroke={INK} strokeWidth={6} strokeLinejoin="round" />
          <rect x={14} y={16} width={150} height={7} rx={3} fill={RED} /><rect x={164} y={16} width={160} height={7} rx={3} fill="rgba(255,255,255,0.4)" />
        </svg>
        <div style={{position: 'absolute', left: 0, right: 0, top: 205, textAlign: 'center', fontFamily: 'Tajawal', fontWeight: 900, fontSize: 52, color: '#fff', WebkitTextStroke: `8px ${INK}`, paintOrder: 'stroke fill', transform: 'rotate(-5deg)', direction: 'rtl'}}>واو!</div>
        <div style={{position: 'absolute', left: 0, right: 0, top: 440, display: 'flex', justifyContent: 'center', gap: 8, direction: 'rtl'}}>
          <span style={{fontFamily: 'Cairo', fontWeight: 800, fontSize: 30, color: '#fff', WebkitTextStroke: '2px #000', paintOrder: 'stroke fill'}}>شوفوا</span>
          <span style={{fontFamily: 'Cairo', fontWeight: 800, fontSize: 30, color: '#fff', background: RED, padding: '0 10px 3px', borderRadius: 8}}>الفرق</span>
        </div>
        <div style={{position: 'absolute', left: 30, right: 30, top: 515, height: 40, display: 'flex', alignItems: 'center', gap: 5}}>
          {Array.from({length: 26}, (_, i) => <div key={i} style={{flex: 1, height: 8 + 28 * Math.abs(Math.sin(i * 1.7)), background: 'rgba(255,255,255,0.85)', borderRadius: 3}} />)}
        </div>
      </div>

      {/* price badge */}
      <div style={{position: 'absolute', left: 270, top: 110, width: 230, height: 230, transform: 'rotate(10deg)'}}>
        <svg width={230} height={230} style={{position: 'absolute'}}>
          <path d={burst(115, 115, 92, 112, 16)} fill={RED} stroke="#fff" strokeWidth={6} strokeLinejoin="round" />
        </svg>
        <div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', direction: 'rtl', color: '#fff', fontFamily: 'Tajawal', fontWeight: 900}}>
          <div style={{fontSize: 30, lineHeight: 1}}>يبدأ من</div>
          <div style={{fontSize: 76, lineHeight: 1}}>٧٩</div>
          <div style={{fontSize: 30, lineHeight: 1}}>ريال</div>
        </div>
      </div>

      {/* bottom bar */}
      <div style={{position: 'absolute', left: 0, right: 0, bottom: 0, height: 120, background: Y, display: 'flex', alignItems: 'center', justifyContent: 'center', direction: 'rtl', gap: 22}}>
        <span style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 52, color: INK}}>أرسل مقطعك الخام</span>
        <span style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 52, color: '#fff', background: RED, padding: '4px 22px 0', borderRadius: 14}}>واستلمه جاهز</span>
      </div>
    </AbsoluteFill>
  );
};
