/**
 * ep002 «بلاغ بلا عنوان» — full-screen graphic inserts (2560x1440, 30 fps).
 * Identity (team/montage-log.md #002): night-green / cold teal / amber archive / bone paper / dried red,
 * Amiri for archive documents, Tajawal for headings. Slow, documentary motion. No glitch.
 * Each insert is its own composition and is cut into the A-roll by scripts/build.py.
 */
import React from 'react';
import {AbsoluteFill, Easing, Img, OffthreadVideo, interpolate, random, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from '@remotion/fonts';

export const C = {
  night: '#0A1210',
  teal: '#2C7A7B',
  amber: '#D9A441',
  bone: '#E8E2D6',
  red: '#7A1E1E',
  ink: '#1A1A16',
};
loadFont({family: 'Amiri', url: staticFile('fonts/Amiri-Regular.ttf'), weight: '400'});
loadFont({family: 'Amiri', url: staticFile('fonts/Amiri-Bold.ttf'), weight: '700'});
loadFont({family: 'Tajawal', url: staticFile('fonts/Tajawal-Black.ttf'), weight: '900'});
loadFont({family: 'Tajawal', url: staticFile('fonts/Tajawal-Bold.ttf'), weight: '700'});

const ease = Easing.bezier(0.25, 0.1, 0.25, 1);
const ramp = (f: number, a: number, n: number) =>
  interpolate(f, [a, a + n], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});

/* ---------- shared backdrop: dark room, slow light drift, film grain, vignette ---------- */
const Grain: React.FC<{o?: number}> = ({o = 0.07}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{opacity: o, mixBlendMode: 'overlay'}}>
      <svg width="100%" height="100%">
        <filter id={`g${f % 6}`}>
          <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={f % 6} />
        </filter>
        <rect width="100%" height="100%" filter={`url(#g${f % 6})`} />
      </svg>
    </AbsoluteFill>
  );
};
const Stage: React.FC<{children: React.ReactNode; tint?: string; warm?: boolean}> = ({children, tint = C.teal, warm}) => {
  const f = useCurrentFrame();
  const x = 50 + 8 * Math.sin(f / 90);
  return (
    <AbsoluteFill style={{background: C.night}}>
      <AbsoluteFill style={{background: `radial-gradient(ellipse at ${x}% 40%, ${warm ? C.amber : tint}33 0%, transparent 60%)`}} />
      {children}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 45%, rgba(0,0,0,.75) 100%)'}} />
      <Grain />
    </AbsoluteFill>
  );
};
/** slow push-in for the whole insert (documentary feel) */
const Push: React.FC<{children: React.ReactNode; from?: number; to?: number}> = ({children, from = 1, to = 1.06}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const s = interpolate(f, [0, durationInFrames], [from, to]);
  return <AbsoluteFill style={{transform: `scale(${s})`}}>{children}</AbsoluteFill>;
};
const Paper: React.FC<{w: number; h: number; rot?: number; children: React.ReactNode; style?: React.CSSProperties}> = ({w, h, rot = 0, children, style}) => (
  <div style={{position: 'absolute', left: '50%', top: '50%', width: w, height: h, transform: `translate(-50%,-50%) rotate(${rot}deg)`,
    background: `linear-gradient(160deg, ${C.bone} 0%, #D9D0BE 100%)`, boxShadow: '0 40px 90px rgba(0,0,0,.6)', borderRadius: 6, ...style}}>
    {children}
  </div>
);
/** typewriter reveal */
const Type: React.FC<{text: string; at: number; cps?: number; style?: React.CSSProperties}> = ({text, at, cps = 22, style}) => {
  const f = useCurrentFrame();
  const n = Math.max(0, Math.floor(((f - at) / 30) * cps));
  return <div style={{direction: 'rtl', ...style}}>{text.slice(0, n)}</div>;
};

/* ================= 1. chapter card ================= */
export const Chapter: React.FC<{num: string; title: string; time?: string}> = ({num, title, time}) => {
  const f = useCurrentFrame();
  const a = ramp(f, 4, 20), b = ramp(f, 16, 26), line = ramp(f, 10, 30);
  return (
    <Stage>
      <Push>
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', direction: 'rtl'}}>
          <div style={{fontFamily: 'Amiri', fontWeight: 700, fontSize: 70, color: C.amber, opacity: a, letterSpacing: 2, transform: `translateY(${(1 - a) * 20}px)`}}>{num}</div>
          <div style={{width: 900 * line, height: 3, background: C.amber, margin: '28px 0', opacity: 0.8}} />
          <div style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 150, color: C.bone, opacity: b, transform: `translateY(${(1 - b) * 30}px)`}}>{title}</div>
          {time && <div style={{fontFamily: 'Amiri', fontSize: 56, color: C.teal, marginTop: 30, opacity: ramp(f, 34, 20)}}>{time}</div>}
        </AbsoluteFill>
      </Push>
    </Stage>
  );
};

/* ================= 2. clock to 2:17 ================= */
export const Clock: React.FC<{label?: string; h?: number; m?: number}> = ({label = '2:17 الفجر', h = 2, m = 17}) => {
  const f = useCurrentFrame();
  const p = ramp(f, 0, 70);
  const totalMin = interpolate(p, [0, 1], [h * 60 + m - 95, h * 60 + m]);
  const mm = totalMin % 60, hh = (totalMin / 60) % 12;
  const tick = f > 70 && Math.floor(f / 15) % 2 === 0;
  const R = 420;
  return (
    <Stage>
      <Push from={1.02} to={1.1}>
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
          <svg width={1100} height={1100} viewBox="-550 -550 1100 1100">
            <circle r={R + 30} fill="#1d1b16" stroke={C.amber} strokeWidth={10} />
            <circle r={R} fill={C.bone} />
            {Array.from({length: 60}).map((_, i) => {
              const a = (i / 60) * Math.PI * 2, big = i % 5 === 0;
              return <line key={i} x1={Math.sin(a) * (R - (big ? 60 : 30))} y1={-Math.cos(a) * (R - (big ? 60 : 30))} x2={Math.sin(a) * (R - 12)} y2={-Math.cos(a) * (R - 12)} stroke={C.ink} strokeWidth={big ? 10 : 4} />;
            })}
            {Array.from({length: 12}).map((_, i) => {
              const a = ((i + 1) / 12) * Math.PI * 2;
              return <text key={i} x={Math.sin(a) * (R - 115)} y={-Math.cos(a) * (R - 115) + 26} textAnchor="middle" fontFamily="Amiri" fontWeight={700} fontSize={78} fill={C.ink}>{i + 1}</text>;
            })}
            <line x1={0} y1={0} x2={Math.sin((hh / 12) * 2 * Math.PI) * 220} y2={-Math.cos((hh / 12) * 2 * Math.PI) * 220} stroke={C.ink} strokeWidth={22} strokeLinecap="round" />
            <line x1={0} y1={0} x2={Math.sin((mm / 60) * 2 * Math.PI) * 340} y2={-Math.cos((mm / 60) * 2 * Math.PI) * 340} stroke={C.ink} strokeWidth={12} strokeLinecap="round" />
            {/* second hand never stops, so the insert never looks frozen */}
            <line x1={0} y1={60} x2={Math.sin((Math.floor(f / 30) / 60) * 2 * Math.PI) * 380} y2={-Math.cos((Math.floor(f / 30) / 60) * 2 * Math.PI) * 380} stroke={C.red} strokeWidth={5} />
            <circle r={22} fill={C.red} />
          </svg>
        </AbsoluteFill>
        <div style={{position: 'absolute', bottom: 110, width: '100%', textAlign: 'center', fontFamily: 'Tajawal', fontWeight: 900, fontSize: 120, color: tick ? C.amber : C.bone, opacity: ramp(f, 66, 12), direction: 'rtl'}}>{label}</div>
      </Push>
    </Stage>
  );
};

/* ================= 3. call record: number struck through ================= */
export const CallRecord: React.FC<{year?: string}> = ({year = '2016'}) => {
  const f = useCurrentFrame();
  const strike = ramp(f, 70, 18), stamp = ramp(f, 100, 8);
  const rows: [string, string][] = [['رقم المتصل', '011 ••• 2140'], ['نوع الخط', 'هاتف أرضي'], ['العنوان المسجّل', 'حي حطين — الرياض'], ['حالة الخط', 'مفصول']];
  return (
    <Stage warm>
      <Push>
        <Paper w={1500} h={1000} rot={-1.5}>
          <div style={{padding: '70px 90px', direction: 'rtl', fontFamily: 'Amiri', color: C.ink}}>
            <div style={{fontWeight: 700, fontSize: 74, borderBottom: `4px double ${C.ink}`, paddingBottom: 18}}>سجل الاتصالات — قسم الاتصالات</div>
            {rows.map(([k, v], i) => (
              <div key={i} style={{display: 'flex', justifyContent: 'space-between', fontSize: 62, marginTop: 44, opacity: ramp(f, 10 + i * 12, 12)}}>
                <span style={{opacity: 0.65}}>{k}</span>
                <span style={{position: 'relative', fontWeight: 700, direction: i === 0 ? 'ltr' : 'rtl', unicodeBidi: 'isolate'}}>
                  {v}
                  {i === 0 && <span style={{position: 'absolute', right: 0, top: '52%', height: 8, width: `${strike * 100}%`, background: C.red}} />}
                </span>
              </div>
            ))}
          </div>
          <div style={{position: 'absolute', left: 120, bottom: 90, transform: `rotate(-14deg) scale(${2 - stamp})`, opacity: stamp, border: `10px solid ${C.red}`, color: C.red,
            fontFamily: 'Tajawal', fontWeight: 900, fontSize: 96, padding: '10px 40px', borderRadius: 12}}>منفصل منذ {year}</div>
        </Paper>
      </Push>
    </Stage>
  );
};

/* ================= 4. rotary phone ringing (no cable) ================= */
export const Phone: React.FC<{caption?: string; ring?: boolean}> = ({caption = 'تلفون… بدون سلك', ring = true}) => {
  const f = useCurrentFrame();
  const shake = ring && f > 20 && Math.floor((f - 20) / 30) % 2 === 0 ? Math.sin(f * 2.4) * 6 : 0;
  const cut = ramp(f, 0, 30);
  return (
    <Stage>
      <Push from={1.0} to={1.08}>
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
          <svg width={1400} height={1100} viewBox="-700 -560 1400 1100" style={{transform: `rotate(${shake * 0.3}deg)`}}>
            {/* table shadow */}
            <ellipse cx={0} cy={330} rx={520} ry={60} fill="#000" opacity={0.5} />
            {/* body */}
            <path d="M-420 300 L-330 -40 Q0 -120 330 -40 L420 300 Z" fill="#141a18" stroke={C.teal} strokeWidth={6} />
            {/* handset (lifted & shaking) */}
            <g transform={`translate(0 ${-220 + shake}) rotate(${shake})`}>
              <path d="M-460 0 Q-470 -90 -360 -110 L360 -110 Q470 -90 460 0 L380 30 Q300 -40 0 -40 Q-300 -40 -380 30 Z" fill="#1d2523" stroke={C.teal} strokeWidth={6} />
            </g>
            {/* dial */}
            <circle cx={0} cy={140} r={170} fill={C.bone} />
            {Array.from({length: 10}).map((_, i) => {
              const a = -Math.PI * 0.15 - (i / 10) * Math.PI * 1.6;
              return <circle key={i} cx={Math.cos(a) * 120} cy={140 + Math.sin(a) * 120} r={30} fill="#141a18" />;
            })}
            <circle cx={0} cy={140} r={50} fill={C.amber} />
            {/* cut cable on the wall */}
            <path d={`M 420 260 Q 560 300 ${560 + 60 * cut} ${200 - 40 * cut}`} stroke="#5b5b52" strokeWidth={14} fill="none" strokeLinecap="round" />
            <circle cx={560 + 60 * cut} cy={200 - 40 * cut} r={12} fill={C.red} />
            {/* ring waves */}
            {ring && [0, 1, 2].map((k) => {
              const t = ((f + k * 12) % 36) / 36;
              return <circle key={k} cx={0} cy={-260} r={200 + t * 260} fill="none" stroke={C.amber} strokeWidth={6} opacity={(1 - t) * (f > 20 ? 0.7 : 0)} />;
            })}
          </svg>
        </AbsoluteFill>
        <div style={{position: 'absolute', bottom: 90, width: '100%', textAlign: 'center', fontFamily: 'Tajawal', fontWeight: 900, fontSize: 110, color: C.bone, direction: 'rtl', opacity: ramp(f, 30, 15)}}>{caption}</div>
      </Push>
    </Stage>
  );
};

/* ================= 5. map: station → house in Hittin ================= */
export const MapRoute: React.FC<{from?: string; to?: string}> = ({from = 'المركز', to = 'بيت حطين'}) => {
  const f = useCurrentFrame();
  const p = ramp(f, 20, 80);
  const A = {x: -650, y: 260}, B = {x: 620, y: -230};
  const path = `M ${A.x} ${A.y} C ${-200} ${-300}, ${200} ${400}, ${B.x} ${B.y}`;
  const len = 2200;
  return (
    <Stage>
      <Push from={1.0} to={1.1}>
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
          <svg width={2560} height={1440} viewBox="-1280 -720 2560 1440">
            {Array.from({length: 26}).map((_, i) => <line key={'v' + i} x1={-1300 + i * 105 + random('v' + i) * 30} y1={-720} x2={-1260 + i * 105} y2={720} stroke={C.teal} strokeOpacity={0.18} strokeWidth={random('w' + i) > 0.7 ? 10 : 3} />)}
            {Array.from({length: 15}).map((_, i) => <line key={'h' + i} x1={-1280} y1={-740 + i * 105} x2={1280} y2={-700 + i * 105 + random('h' + i) * 40} stroke={C.teal} strokeOpacity={0.18} strokeWidth={random('x' + i) > 0.7 ? 10 : 3} />)}
            <path d={path} fill="none" stroke={C.amber} strokeWidth={12} strokeDasharray="34 26" strokeDashoffset={0}
              style={{clipPath: 'none'}} opacity={0.95} pathLength={len}
              strokeLinecap="round" />
            <path d={path} fill="none" stroke={C.night} strokeWidth={20} pathLength={len} strokeDasharray={`${len} ${len}`} strokeDashoffset={-len * p} />
            {[{...A, t: from, c: C.teal, a: 0}, {...B, t: to, c: C.red, a: 0.95}].map((pt, i) => (
              <g key={i} opacity={i === 0 ? ramp(f, 4, 12) : ramp(f, 90, 12)}>
                <circle cx={pt.x} cy={pt.y} r={34} fill={pt.c} stroke={C.bone} strokeWidth={8} />
                <circle cx={pt.x} cy={pt.y} r={34 + ((f % 40) / 40) * 70} fill="none" stroke={pt.c} strokeWidth={5} opacity={1 - (f % 40) / 40} />
                <text x={pt.x} y={pt.y - 70} textAnchor="middle" fontFamily="Tajawal" fontWeight={900} fontSize={84} fill={C.bone}>{pt.t}</text>
              </g>
            ))}
          </svg>
        </AbsoluteFill>
      </Push>
    </Stage>
  );
};

/* ================= 6. crime scene with no body (chalk outline + evidence markers) ================= */
export const Scene: React.FC<{markers?: number; highlight?: number}> = ({markers = 3, highlight = 0}) => {
  const f = useCurrentFrame();
  const draw = ramp(f, 6, 60);
  const L = 3000;
  const marks = [{x: -420, y: -160}, {x: 380, y: -260}, {x: 260, y: 300}];
  return (
    <Stage>
      <Push from={1.0} to={1.12}>
        <AbsoluteFill style={{background: 'repeating-linear-gradient(90deg, #1b1611 0 120px, #17130f 120px 124px)', opacity: 0.9}} />
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center'}}>
          <svg width={2560} height={1440} viewBox="-1280 -720 2560 1440">
            <path pathLength={L} strokeDasharray={`${L} ${L}`} strokeDashoffset={L * (1 - draw)} fill="none" stroke="#efeae0" strokeWidth={14} strokeLinejoin="round" strokeLinecap="round"
              d="M -40 -330 C -120 -330 -130 -230 -60 -200 L -260 -150 L -420 -60 L -400 -20 L -230 -90 L -130 -60 L -150 120 L -260 330 L -200 350 L -60 160 L 40 160 L 170 350 L 230 320 L 120 120 L 110 -60 L 230 -90 L 400 -20 L 420 -60 L 260 -150 L 60 -200 C 130 -230 120 -330 40 -330 Z" />
            {marks.slice(0, markers).map((m, i) => {
              const a = ramp(f, 60 + i * 14, 10);
              const hl = highlight === i + 1;
              return (
                <g key={i} transform={`translate(${m.x} ${m.y - (1 - a) * 60})`} opacity={a}>
                  <path d="M -70 60 L 0 -70 L 70 60 Z" fill={C.amber} stroke={hl ? C.bone : '#7c5c18'} strokeWidth={hl ? 10 : 4} />
                  <text x={0} y={42} textAnchor="middle" fontFamily="Tajawal" fontWeight={900} fontSize={80} fill={C.ink}>{i + 1}</text>
                  {hl && <circle r={150 + 10 * Math.sin(f / 6)} fill="none" stroke={C.bone} strokeWidth={4} opacity={0.6} />}
                </g>
              );
            })}
          </svg>
        </AbsoluteFill>
        <div style={{position: 'absolute', top: 150, right: 260, fontFamily: 'Amiri', fontWeight: 700, fontSize: 60, color: C.bone, opacity: 0.75, direction: 'rtl'}}>صورة تقريبية للمشهد — لا توجد جثة</div>
      </Push>
    </Stage>
  );
};

/* ================= 7. year stamp for flashback ================= */
export const Year: React.FC<{year?: string; sub?: string}> = ({year = '2016', sub = 'قبل عشر سنين'}) => {
  const f = useCurrentFrame();
  const n = Math.round(interpolate(ramp(f, 0, 40), [0, 1], [2026, Number(year)]));
  return (
    <Stage warm>
      <Push>
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', direction: 'rtl', filter: 'sepia(.5)'}}>
          <div style={{fontFamily: 'Amiri', fontWeight: 700, fontSize: 360, color: C.amber, letterSpacing: 10}}>{n}</div>
          <div style={{fontFamily: 'Tajawal', fontWeight: 700, fontSize: 90, color: C.bone, opacity: ramp(f, 40, 16)}}>{sub}</div>
        </AbsoluteFill>
      </Push>
    </Stage>
  );
};

/* ================= 8. quote / key line (full-screen) ================= */
export const Quote: React.FC<{text: string; sub?: string; red?: boolean}> = ({text, sub, red}) => {
  const f = useCurrentFrame();
  return (
    <Stage tint={red ? C.red : C.teal}>
      <Push from={1.04} to={1.0}>
        <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', direction: 'rtl', padding: 200, textAlign: 'center'}}>
          <div style={{fontFamily: 'Amiri', fontSize: 200, color: C.amber, lineHeight: 0.4, opacity: ramp(f, 0, 12)}}>«</div>
          <Type text={text} at={6} cps={18} style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 130, color: red ? '#e9d3cf' : C.bone, lineHeight: 1.3}} />
          {sub && <div style={{fontFamily: 'Amiri', fontSize: 64, color: C.teal, marginTop: 40, opacity: ramp(f, 50, 15)}}>{sub}</div>}
        </AbsoluteFill>
      </Push>
    </Stage>
  );
};

/* ================= 9. end card ================= */
export const EndCard: React.FC = () => {
  const f = useCurrentFrame();
  const a = ramp(f, 0, 24);
  return (
    <Stage>
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', direction: 'rtl'}}>
        <Img src={staticFile('logo.png')} style={{width: 420, height: 420, borderRadius: '50%', opacity: a, transform: `scale(${0.9 + 0.1 * a})`, boxShadow: `0 0 120px ${C.teal}66`}} />
        <div style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 110, color: C.bone, marginTop: 60, opacity: ramp(f, 14, 16)}}>اشترك وفعّل الجرس 🔔</div>
        <div style={{fontFamily: 'Amiri', fontSize: 62, color: C.amber, marginTop: 24, opacity: ramp(f, 26, 16)}}>القصة درامية من تأليف الفريق — أي تشابه مع الواقع غير مقصود</div>
      </AbsoluteFill>
    </Stage>
  );
};

/* ================= 10. big red title over footage (cold-open title, Abu-Al-Sadiq style) ================= */
export const BigTitle: React.FC<{title: string; sub?: string; bg?: string}> = ({title, sub, bg = 'broll/police_lights.mp4'}) => {
  const f = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const hit = ramp(f, 6, 6);
  const shake = f > 6 && f < 16 ? (random('s' + f) - 0.5) * 24 : 0;
  const out = interpolate(f, [durationInFrames - 10, durationInFrames], [1, 0], {extrapolateLeft: 'clamp'});
  return (
    <AbsoluteFill style={{background: '#000', opacity: out}}>
      <AbsoluteFill style={{filter: 'grayscale(.6) contrast(1.2) brightness(.45)', transform: `scale(${1.05 + f / 900})`}}>
        <OffthreadVideo src={staticFile(bg)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 30%, rgba(0,0,0,.85) 100%)'}} />
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', direction: 'rtl', transform: `translate(${shake}px, ${shake / 2}px)`}}>
        <div style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 300, color: '#C0141B', letterSpacing: -4,
          textShadow: '0 0 40px rgba(192,20,27,.55), 0 12px 0 rgba(0,0,0,.6)', transform: `scale(${2.2 - 1.2 * hit})`, opacity: hit}}>{title}</div>
        {sub && <div style={{fontFamily: 'Amiri', fontWeight: 700, fontSize: 90, color: C.bone, marginTop: 10, opacity: ramp(f, 22, 14), letterSpacing: 6}}>{sub}</div>}
      </AbsoluteFill>
      <Grain o={0.12} />
    </AbsoluteFill>
  );
};
