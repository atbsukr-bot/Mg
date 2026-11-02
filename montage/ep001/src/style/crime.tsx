/**
 * ep001 «بلاغ بلا عنوان» — custom crime-file graphics.
 * Same rules as components.tsx: 1080x1920, spring pops, hard shadows, lines draw on.
 */
import React from 'react';
import {AbsoluteFill, Easing, interpolate, random, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import {T, ramp, usePop} from './components';

const mono = 'DejaVu Sans Mono, monospace';

/* ---------- fingerprint under a magnifying glass ---------- */
export const Magnifier: React.FC<{x?: number; y?: number}> = ({x = 540, y = 820}) => {
  const f = useCurrentFrame();
  const draw = ramp(f, 2, 26);
  const slide = spring({frame: f - 14, fps: 30, config: {damping: 13, stiffness: 120}});
  const ridges = Array.from({length: 11}, (_, i) => i);
  const gx = interpolate(slide, [0, 1], [380, 40]);
  const gy = interpolate(slide, [0, 1], [320, 30]);
  return (
    <svg style={{position: 'absolute', left: x - 330, top: y - 330}} width={660} height={660} viewBox="-330 -330 660 660">
      <defs>
        <clipPath id="lens"><circle cx={gx} cy={gy} r={150} /></clipPath>
      </defs>
      <rect x={-250} y={-290} width={500} height={580} rx={18} fill={T.paper} />
      <rect x={-232} y={-272} width={464} height={544} rx={10} fill="none" stroke={T.ink} strokeWidth={3} />
      {ridges.map((i) => {
        const rx = 30 + i * 17, ry = 44 + i * 20;
        const L = 2 * Math.PI * Math.sqrt((rx * rx + ry * ry) / 2);
        return <ellipse key={i} cx={0} cy={10} rx={rx} ry={ry} fill="none" stroke={T.ink} strokeWidth={7}
          strokeDasharray={`${L * 0.78} ${L}`} strokeDashoffset={L * (1 - draw) + i * 23} strokeLinecap="round" opacity={0.85} />;
      })}
      {/* lens: the same print, bigger and in tape yellow */}
      <g clipPath="url(#lens)">
        <circle cx={gx} cy={gy} r={150} fill={T.ink} />
        {ridges.map((i) => {
          const rx = (30 + i * 17) * 1.6, ry = (44 + i * 20) * 1.6;
          return <ellipse key={i} cx={gx * -0.6} cy={10 + gy * -0.6} rx={rx} ry={ry} fill="none" stroke={T.tape} strokeWidth={10} strokeDasharray="160 40" />;
        })}
      </g>
      <circle cx={gx} cy={gy} r={150} fill="none" stroke={T.ink} strokeWidth={22} />
      <line x1={gx + 106} y1={gy + 106} x2={gx + 230} y2={gy + 230} stroke={T.ink} strokeWidth={42} strokeLinecap="round" />
    </svg>
  );
};

/* ---------- case file folder ---------- */
export const CaseFile: React.FC<{x?: number; y?: number; no?: string; title?: string; stampAt?: number; rotate?: number}> = ({
  x = 540, y = 1060, no = '#001', title = 'ملف القضية', stampAt = 30, rotate = -3,
}) => {
  const f = useCurrentFrame();
  const s = usePop(0, 12);
  const st = spring({frame: f - stampAt, fps: 30, config: {damping: 9, stiffness: 260}});
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) translateY(${(1 - s) * 500}px) rotate(${rotate}deg)`, width: 640, height: 400}}>
      <div style={{position: 'absolute', right: 40, top: -46, width: 230, height: 60, background: '#D9B977', borderRadius: '14px 14px 0 0'}} />
      <div style={{position: 'absolute', inset: 0, background: '#E2C485', borderRadius: 14, boxShadow: T.shadow, direction: 'rtl', padding: 34}}>
        <div style={{fontFamily: T.file, fontWeight: 700, fontSize: 70, color: T.ink}}>{title}</div>
        <div style={{fontFamily: mono, fontSize: 46, color: T.ink, marginTop: 10, direction: 'ltr', textAlign: 'right'}}>CASE {no}</div>
        <div style={{position: 'absolute', left: 34, right: 34, bottom: 60, height: 6, background: T.ink, opacity: 0.25}} />
        <div style={{position: 'absolute', left: 34, right: 200, bottom: 100, height: 6, background: T.ink, opacity: 0.25}} />
      </div>
      {f >= stampAt && (
        <div style={{position: 'absolute', left: 40, top: 150, transform: `rotate(-14deg) scale(${2.2 - 1.2 * st})`, opacity: Math.min(1, st * 2),
          border: `8px solid ${T.red}`, color: T.red, fontFamily: T.head, fontWeight: 900, fontSize: 72, padding: '0 26px 10px', borderRadius: 10, direction: 'rtl'}}>سرّي</div>
      )}
    </div>
  );
};

/* ---------- calm monitor: flat line ---------- */
export const Flatline: React.FC<{x?: number; y?: number; label?: string}> = ({x = 540, y = 820, label = 'لا شيء'}) => {
  const f = useCurrentFrame();
  const s = usePop(0, 12);
  const draw = ramp(f, 6, 40, Easing.linear);
  const blip = 'M0,150 L300,150 L330,120 L350,170 L370,150 L760,150';
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) scale(${0.6 + 0.4 * s}) rotate(2deg)`, opacity: s,
      width: 820, height: 420, background: T.ui, borderRadius: 26, boxShadow: T.shadow, padding: 30, boxSizing: 'border-box'}}>
      <svg width={760} height={300}>
        {[0, 1, 2, 3, 4].map((i) => <line key={i} x1={0} x2={760} y1={i * 75} y2={i * 75} stroke="#2c3850" strokeWidth={2} />)}
        <path d={blip} fill="none" stroke={T.tape} strokeWidth={8} strokeDasharray={900} strokeDashoffset={900 * (1 - draw)} strokeLinejoin="round" />
      </svg>
      <div style={{position: 'absolute', bottom: 22, right: 36, fontFamily: T.file, fontWeight: 700, fontSize: 46, color: '#9fb0cf', direction: 'rtl'}}>{label}</div>
      <div style={{position: 'absolute', bottom: 30, left: 36, fontFamily: mono, fontSize: 34, color: '#9fb0cf'}}>00 / 24</div>
    </div>
  );
};

/* ---------- empty report log with a counter that lands on 0 ---------- */
export const ReportLog: React.FC<{x?: number; y?: number}> = ({x = 540, y = 820}) => {
  const f = useCurrentFrame();
  const s = usePop(0, 12);
  const n = Math.round(interpolate(f, [4, 26], [9, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)}));
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) translateY(${(1 - s) * -200}px) rotate(-2deg)`, opacity: s,
      width: 760, background: T.paper, borderRadius: 12, boxShadow: T.shadow, padding: 34, direction: 'rtl'}}>
      <div style={{fontFamily: T.file, fontWeight: 700, fontSize: 60, color: T.ink, borderBottom: `4px solid ${T.ink}`, paddingBottom: 10}}>سجل البلاغات</div>
      {[0, 1, 2].map((i) => <div key={i} style={{height: 54, borderBottom: `3px dashed ${T.line}`}} />)}
      <div style={{display: 'flex', alignItems: 'baseline', gap: 24, marginTop: 20}}>
        <span style={{fontFamily: T.head, fontWeight: 900, fontSize: 52, color: T.ink}}>بلاغات اليوم</span>
        <span style={{fontFamily: T.head, fontWeight: 900, fontSize: 180, lineHeight: 1, color: T.red, fontVariantNumeric: 'tabular-nums'}}>{n}</span>
      </div>
    </div>
  );
};

/* ---------- incoming call ---------- */
export const IncomingCall: React.FC<{x?: number; y?: number; caller?: string; answerAt?: number; scale?: number}> = ({x = 540, y = 1060, caller = 'رقم مجهول', answerAt, scale = 1}) => {
  const f = useCurrentFrame();
  const s = usePop(0, 12);
  const answered = answerAt !== undefined && f >= answerAt;
  const shake = answered ? 0 : Math.sin(f * 2.2) * 5 * (Math.floor(f / 8) % 2);
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) translateY(${(1 - s) * 600}px) scale(${scale}) rotate(${-2 + shake * 0.4}deg) translateX(${shake}px)`,
      width: 760, height: 330, background: T.ui, borderRadius: 40, boxShadow: T.shadow, direction: 'rtl', padding: '36px 44px', boxSizing: 'border-box'}}>
      <div style={{fontFamily: T.body, fontWeight: 800, fontSize: 36, color: '#9fb0cf'}}>{answered ? 'جارٍ الاتصال… 00:0' + Math.min(9, Math.floor((f - (answerAt ?? 0)) / 30)) : 'مكالمة واردة'}</div>
      <div style={{fontFamily: T.head, fontWeight: 900, fontSize: 74, color: T.white, marginTop: 6}}>{caller}</div>
      <div style={{position: 'absolute', bottom: 34, right: 44, left: 44, display: 'flex', justifyContent: 'space-between'}}>
        {[{c: '#2f9e44', r: 0}, {c: T.red, r: 135}].map((b, i) => {
          const ring = (f % 24) / 24;
          return (
            <div key={i} style={{position: 'relative', width: 96, height: 96}}>
              {!answered && i === 0 && <div style={{position: 'absolute', inset: -30 * ring, borderRadius: '50%', border: `5px solid ${b.c}`, opacity: 1 - ring}} />}
              <div style={{position: 'absolute', inset: 0, borderRadius: '50%', background: b.c, display: 'grid', placeItems: 'center'}}>
                <svg width={50} height={50} viewBox="0 0 24 24" style={{transform: `rotate(${b.r}deg)`}}><path fill={T.white} d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z" /></svg>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

/* ---------- map with a pin that can't find the place ---------- */
export const MapPin: React.FC<{lostAt?: number}> = ({lostAt = 32}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const card = usePop(0, 12);
  const pin = spring({frame: f - 8, fps, config: {damping: 8, stiffness: 160}});
  const lost = f >= lostAt;
  const wander = lost ? Math.sin((f - lostAt) / 5) * 70 : 0;
  const streets = ['M80,260 L940,300', 'M60,520 L980,470', 'M120,780 L900,820', 'M300,80 L260,980', 'M640,60 L700,1000', 'M80,980 L980,120'];
  return (
    <AbsoluteFill>
      <div style={{position: 'absolute', left: 60, top: 300, width: 960, height: 1000, transform: `scale(${0.7 + 0.3 * card}) rotate(2deg)`, opacity: card,
        background: '#E9E1CC', borderRadius: 18, boxShadow: T.shadow, overflow: 'hidden'}}>
        <svg width={960} height={1000}>
          {[[150, 330, 160, 140], [380, 330, 200, 120], [740, 340, 160, 110], [150, 560, 220, 190], [420, 560, 230, 200], [760, 540, 150, 230], [380, 850, 240, 120]].map(([x, y, w, h], i) => (
            <rect key={i} x={x} y={y} width={w} height={h} rx={8} fill="#D9CFB6" />
          ))}
          {streets.map((d, i) => <path key={i} d={d} stroke={T.white} strokeWidth={30} fill="none" strokeLinecap="round" />)}
          {lost && <circle cx={480} cy={520} r={150 + ((f - lostAt) % 30) * 6} fill="none" stroke={T.blue} strokeWidth={6} strokeDasharray="20 16" opacity={1 - ((f - lostAt) % 30) / 30} />}
        </svg>
        <svg style={{position: 'absolute', left: 480 - 60 + wander, top: 520 - 150 - (1 - pin) * 500}} width={120} height={160} viewBox="0 0 120 160">
          <path d="M60,156 C20,100 6,78 6,56 a54,54 0 0 1 108,0 c0,22 -14,44 -54,100z" fill={T.red} stroke={T.ink} strokeWidth={6} />
          <circle cx={60} cy={56} r={20} fill={T.paper} />
        </svg>
        {lost && ['؟', '؟', '؟'].map((q, i) => {
          const qs = spring({frame: f - lostAt - i * 5, fps, config: {damping: 9, stiffness: 200}});
          return <div key={i} style={{position: 'absolute', left: [250, 640, 470][i], top: [260, 280, 760][i], fontFamily: T.head, fontWeight: 900, fontSize: 150, color: T.blue,
            transform: `scale(${qs}) rotate(${[-14, 12, -4][i]}deg)`}}>{q}</div>;
        })}
      </div>
    </AbsoluteFill>
  );
};

/* ---------- red / blue siren wash ---------- */
export const SirenLights: React.FC<{strength?: number}> = ({strength = 0.55}) => {
  const f = useCurrentFrame();
  const phase = Math.floor(f / 6) % 2;
  return (
    <AbsoluteFill style={{mixBlendMode: 'screen', pointerEvents: 'none'}}>
      <AbsoluteFill style={{background: `radial-gradient(circle at ${phase ? 0 : 100}% 0%, ${phase ? T.red : T.blue} 0%, transparent 55%)`, opacity: strength}} />
      <AbsoluteFill style={{background: `radial-gradient(circle at ${phase ? 100 : 0}% 100%, ${phase ? T.blue : T.red} 0%, transparent 50%)`, opacity: strength * 0.6}} />
    </AbsoluteFill>
  );
};

/* ---------- the "approximate picture" of the scene (no gore) ---------- */
export const CrimeScene: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const push = interpolate(f, [0, 120], [1.08, 1.0], {extrapolateRight: 'clamp'});
  const beam = 0.85 + 0.15 * Math.sin(f / 3.1) * (random(`fl${Math.floor(f / 4)}`) > 0.85 ? 1 : 0.2);
  const chalk = ramp(f, 10, 40, Easing.inOut(Easing.cubic));
  const markers = [{x: 300, y: 1290, n: '1', at: 34}, {x: 760, y: 1180, n: '2', at: 44}, {x: 610, y: 1480, n: '3', at: 54}];
  const outline = 'M540,1010 a46,46 0 1 1 0.1,0 M540,1104 L548,1300 M548,1300 L470,1470 M548,1300 L640,1460 M540,1140 L420,1210 M540,1140 L660,1080';
  return (
    <AbsoluteFill style={{background: '#06080d', overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${push})`}}>
        <svg width={1080} height={1920}>
          <defs>
            <radialGradient id="beam" cx="50%" cy="62%" r="55%">
              <stop offset="0%" stopColor="#F5EBD0" stopOpacity={0.55 * beam} />
              <stop offset="60%" stopColor="#F5EBD0" stopOpacity={0.12 * beam} />
              <stop offset="100%" stopColor="#F5EBD0" stopOpacity={0} />
            </radialGradient>
          </defs>
          {/* floor in perspective */}
          <path d="M0,760 L1080,760 L1080,1920 L0,1920 Z" fill="#141a26" />
          {Array.from({length: 9}, (_, i) => <line key={i} x1={540 + (i - 4) * 60} y1={760} x2={540 + (i - 4) * 420} y2={1920} stroke="#1f2738" strokeWidth={4} />)}
          {Array.from({length: 7}, (_, i) => { const yy = 760 + Math.pow(i / 6, 1.7) * 1160; return <line key={i} x1={0} x2={1080} y1={yy} y2={yy} stroke="#1f2738" strokeWidth={4} />; })}
          <path d="M0,0 L1080,0 L1080,760 L0,760 Z" fill="#0b0f17" />
          <rect x={700} y={250} width={220} height={330} fill="#111827" stroke="#222c40" strokeWidth={8} />
          <ellipse cx={540} cy={1250} rx={620} ry={560} fill="url(#beam)" />
          {/* chalk outline draws on */}
          <path d={outline} transform="translate(540 1060) scale(1.35) translate(-540 -1240)" fill="none" stroke="#F3F0E8" strokeWidth={11} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={1800} strokeDashoffset={1800 * (1 - chalk)} opacity={0.92} />
          {/* footprints */}
          {[0, 1, 2, 3].map((i) => <ellipse key={i} cx={820 - i * 70} cy={1700 - i * 110} rx={20} ry={36} fill="#2a3346" opacity={ramp(f, 60 + i * 6, 6)} transform={`rotate(-20 ${820 - i * 70} ${1700 - i * 110})`} />)}
        </svg>
        {markers.map((m) => {
          const s = spring({frame: f - m.at, fps, config: {damping: 9, stiffness: 220}});
          if (f < m.at) return null;
          return (
            <div key={m.n} style={{position: 'absolute', left: m.x, top: m.y, transform: `translate(-50%,-100%) scale(${s})`, transformOrigin: 'bottom'}}>
              <svg width={110} height={100} viewBox="0 0 110 100"><path d="M10,96 L35,8 L75,8 L100,96 Z" fill={T.tape} stroke={T.ink} strokeWidth={6} /></svg>
              <div style={{position: 'absolute', top: 34, width: '100%', textAlign: 'center', fontFamily: T.head, fontWeight: 900, fontSize: 50, color: T.ink}}>{m.n}</div>
            </div>
          );
        })}
      </AbsoluteFill>
      {/* police tape in the foreground */}
      {[{y: 560, r: -9, at: 0}, {y: 1640, r: 7, at: 6}].map((t, i) => {
        const p = ramp(f, t.at, 10);
        return (
          <div key={i} style={{position: 'absolute', left: -200, top: t.y, width: 1480, transform: `rotate(${t.r}deg) translateX(${(1 - p) * (i ? -1500 : 1500)}px)`,
            background: T.tape, color: T.ink, fontFamily: T.head, fontWeight: 900, fontSize: 46, padding: '6px 0 12px', whiteSpace: 'nowrap', overflow: 'hidden',
            borderTop: `8px solid ${T.ink}`, borderBottom: `8px solid ${T.ink}`, direction: 'rtl'}}>
            {Array(8).fill('مسرح جريمة • ممنوع الاقتراب').join('  •  ')}
          </div>
        );
      })}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 55%, transparent 40%, rgba(0,0,0,.7) 100%)'}} />
    </AbsoluteFill>
  );
};

/* ---------- end card ---------- */
export const EndCard: React.FC<{handle?: string}> = ({handle = '@mncousins'}) => {
  const f = useCurrentFrame();
  const a = usePop(0), b = usePop(10, 12);
  const dots = '.'.repeat(1 + (Math.floor(f / 8) % 3));
  return (
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 42%, #1f2a40 0%, #07090f 100%)'}}>
      <div style={{position: 'absolute', top: 640, width: '100%', textAlign: 'center', fontFamily: T.head, fontWeight: 900, fontSize: 210, color: T.tape,
        transform: `scale(${0.5 + 0.5 * a})`, direction: 'rtl', textShadow: '0 10px 0 rgba(0,0,0,.4)'}}>يتبع{dots}</div>
      <div style={{position: 'absolute', left: 140, right: 140, top: 1000, height: 120, borderRadius: 60, background: T.paper, boxShadow: T.shadow,
        transform: `translateY(${(1 - b) * 300}px)`, opacity: b, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 46px'}}>
        <svg width={56} height={56} viewBox="0 0 24 24"><circle cx={10} cy={10} r={7} fill="none" stroke={T.ink} strokeWidth={3} /><line x1={15} y1={15} x2={22} y2={22} stroke={T.ink} strokeWidth={3} strokeLinecap="round" /></svg>
        <span style={{fontFamily: mono, fontSize: 56, color: T.ink, fontWeight: 700}}>{handle}</span>
      </div>
    </AbsoluteFill>
  );
};
