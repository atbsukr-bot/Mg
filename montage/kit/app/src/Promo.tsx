// Promo / explainer UI graphics (video 2: the skill promo). All motion is frame-driven (no CSS animation).
import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, spring, interpolate, Easing, random} from 'remotion';

const RED = '#E3262A';
const INK = '#141414';
const YEL = '#FFD23F';
const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
const pop = (f: number, fps: number, delay = 0, damping = 12, stiffness = 180) =>
  spring({frame: f - delay, fps, config: {damping, stiffness, mass: 0.7}});
const useInOut = (dur: number, damping = 13) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = pop(f, fps, 0, damping);
  const out = interpolate(f, [dur - 8, dur], [1, 0], clamp);
  return {f, fps, p, out};
};
const card: React.CSSProperties = {background: '#fff', borderRadius: 30, boxShadow: '0 24px 50px rgba(0,0,0,0.42), 0 0 0 1px rgba(0,0,0,0.05)'};
const chip = (bg: string, fg = '#fff'): React.CSSProperties => ({display: 'inline-block', background: bg, color: fg, fontFamily: 'Tajawal', fontWeight: 900, fontSize: 30, padding: '4px 20px 0', borderRadius: 999, direction: 'rtl', whiteSpace: 'nowrap'});
const Wrap: React.FC<{x: number; y: number; p: number; out: number; tilt?: number; k?: number; from?: 'up' | 'down' | 'left' | 'right' | 'scale'; children: React.ReactNode}> = ({x, y, p, out, tilt = 0, k = 1, from = 'scale', children}) => {
  const dx = from === 'left' ? -900 : from === 'right' ? 900 : 0;
  const dy = from === 'up' ? -700 : from === 'down' ? 700 : 0;
  const sc = from === 'scale' ? 0.3 + 0.7 * p : 1;
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(calc(-50% + ${(1 - p) * dx}px), calc(-50% + ${(1 - p) * dy}px)) scale(${k * sc * (0.9 + 0.1 * out)}) rotate(${tilt + (1 - p) * (from === 'scale' ? -6 : 0)}deg)`, opacity: Math.min(1, p * 2) * out}}>
      {children}
    </div>
  );
};

// ---------- 1. RAW FOOTAGE CARD ----------
export const RawCard: React.FC<{dur: number; x?: number; y?: number; img?: string; time?: string; label?: string}> = ({dur, x = 1430, y = 470, img = 'frames/00100.jpg', time = '٤:٥٢', label = 'الخام'}) => {
  const {f, p, out} = useInOut(dur);
  const W = 560;
  return (
    <Wrap x={x} y={y} p={p} out={out} tilt={2} from="right">
      <div style={{...card, width: W, padding: 18}}>
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12, direction: 'rtl'}}>
          <span style={chip(RED)}>{label}</span>
          <span style={{fontFamily: 'Cairo', fontWeight: 800, fontSize: 24, color: '#888', letterSpacing: 2}}>RAW · {time}</span>
        </div>
        <div style={{position: 'relative', width: W - 36, height: (W - 36) * 9 / 16, borderRadius: 18, overflow: 'hidden'}}>
          <Img src={staticFile(img)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'saturate(0.85)'}} />
          <div style={{position: 'absolute', left: '50%', top: '50%', width: 86, height: 86, transform: 'translate(-50%,-50%)', borderRadius: '50%', background: 'rgba(255,255,255,0.92)', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <svg width="38" height="38" viewBox="0 0 24 24"><path d="M7 4l13 8-13 8z" fill={INK} /></svg>
          </div>
        </div>
        <svg width={W - 36} height={56} style={{marginTop: 10}}>
          {Array.from({length: 46}, (_, i) => {
            const h = 8 + 40 * Math.abs(Math.sin(i * 1.7 + f / 3) * random(`w${i}`));
            return <rect key={i} x={i * ((W - 36) / 46)} y={28 - h / 2} width={6} height={h} rx={3} fill={i / 46 < interpolate(f, [6, dur - 10], [0, 1], clamp) ? RED : '#d6d6d6'} />;
          })}
        </svg>
      </div>
    </Wrap>
  );
};

// ---------- 2. PROMPT BOX (text types itself, then "send") ----------
export const PromptBox: React.FC<{dur: number; x?: number; y?: number; text: string; label?: string; typeStart?: number; cps?: number}> = ({dur, x = 960, y = 300, text, label = 'جملة وحدة', typeStart = 8, cps = 18}) => {
  const {f, fps, p, out} = useInOut(dur);
  const chars = Math.max(0, Math.floor(((f - typeStart) / fps) * cps));
  const shown = text.slice(0, chars);
  const done = chars >= text.length;
  const sendAt = typeStart + Math.ceil((text.length / cps) * fps) + 6;
  const sent = f >= sendAt;
  const press = f >= sendAt && f < sendAt + 5 ? 0.85 : 1 + (sent ? 0.12 * Math.exp(-(f - sendAt - 5) / 4) : 0);
  const ring = interpolate(f, [sendAt, sendAt + 16], [0, 1], clamp);
  const caret = !done && Math.floor(f / 8) % 2 === 0;
  return (
    <Wrap x={x} y={y} p={p} out={out} from="up">
      <div style={{...card, width: 980, padding: '22px 26px', direction: 'rtl'}}>
        <div style={{marginBottom: 14}}><span style={chip(RED)}>{label}</span></div>
        <div style={{display: 'flex', alignItems: 'center', gap: 18, border: `3px solid ${done ? RED : '#e2e2e2'}`, borderRadius: 22, padding: '14px 20px'}}>
          <div style={{flex: 1, fontFamily: 'Cairo', fontWeight: 800, fontSize: 50, color: INK, minHeight: 70, lineHeight: '70px', whiteSpace: 'nowrap', overflow: 'hidden'}}>
            {shown}<span style={{display: 'inline-block', width: 5, height: 52, background: RED, marginRight: 6, verticalAlign: 'middle', opacity: caret ? 1 : 0}} />
          </div>
          <div style={{position: 'relative', width: 78, height: 78, borderRadius: '50%', background: done ? RED : '#cfcfcf', display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${press})`}}>
            <svg width="40" height="40" viewBox="0 0 24 24"><path d="M12 4l7 7h-5v9h-4v-9H5z" fill="#fff" /></svg>
            {ring > 0 && ring < 1 && <div style={{position: 'absolute', left: '50%', top: '50%', width: 200 * ring, height: 200 * ring, transform: 'translate(-50%,-50%)', borderRadius: '50%', border: `${8 * (1 - ring)}px solid ${RED}`, opacity: 1 - ring}} />}
          </div>
        </div>
      </div>
    </Wrap>
  );
};

// ---------- 3. EDITOR / TIMELINE UI ----------
export const EditorUI: React.FC<{dur: number; x?: number; y?: number; scale?: number; thumbs?: string[]; title?: string}> = ({dur, x = 1380, y = 460, scale = 1, thumbs = ['frames/00300.jpg', 'frames/01200.jpg', 'frames/02400.jpg', 'frames/03600.jpg', 'frames/04800.jpg'], title = 'المونتاج'}) => {
  const {f, p, out} = useInOut(dur);
  const prog = interpolate(f, [10, dur - 12], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
  const W = 860, TL = 120, TW = W - TL - 40;
  const track = (label: string, y0: number, kind: 'video' | 'cap' | 'sfx' | 'music', color: string) => (
    <g key={label}>
      <text x={W - 30} y={y0 + 30} textAnchor="end" fontFamily="Cairo" fontWeight={800} fontSize={22} fill="#9a9a9a">{label}</text>
      <rect x={20} y={y0} width={TW} height={44} rx={10} fill="#262626" />
      {kind === 'video' && thumbs.map((t, i) => {
        const w = TW / thumbs.length;
        return (i + 0.2) / thumbs.length <= prog + 0.02 ? <image key={i} href={staticFile(t)} x={20 + i * w + 2} y={y0 + 2} width={w - 4} height={40} preserveAspectRatio="xMidYMid slice" /> : null;
      })}
      {kind === 'cap' && Array.from({length: 11}, (_, i) => {
        const a = (i * 0.09) + 0.01, w = 0.06 + 0.02 * random(`c${i}`);
        return a < prog ? <rect key={i} x={20 + a * TW} y={y0 + 9} width={w * TW} height={26} rx={7} fill={color} /> : null;
      })}
      {kind === 'sfx' && Array.from({length: 16}, (_, i) => {
        const a = i / 16 + 0.02 * random(`s${i}`);
        return a < prog ? <circle key={i} cx={20 + a * TW} cy={y0 + 22} r={9} fill={color} /> : null;
      })}
      {kind === 'music' && (
        <path d={Array.from({length: 90}, (_, i) => `${i ? 'L' : 'M'} ${20 + (i / 89) * TW * prog} ${y0 + 22 + Math.sin(i * 0.9) * 12 * random(`m${i}`)}`).join(' ')} stroke={color} strokeWidth={3} fill="none" />
      )}
    </g>
  );
  return (
    <Wrap x={x} y={y} p={p} out={out} from="right" tilt={-1.5} k={scale}>
      <div style={{width: W, borderRadius: 28, background: INK, boxShadow: '0 26px 60px rgba(0,0,0,0.55)', padding: '18px 0 14px', direction: 'rtl'}}>
        <div style={{display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 26px 12px'}}>
          <span style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 40, color: '#fff'}}>{title}</span>
          <span style={{display: 'flex', alignItems: 'center', gap: 10, background: '#2b2b2b', borderRadius: 999, padding: '4px 16px 4px 8px'}}>
            <Img src={staticFile('claude.png')} style={{width: 36, height: 36, objectFit: 'contain'}} />
            <span style={{fontFamily: 'Cairo', fontWeight: 800, fontSize: 22, color: '#ddd', direction: 'ltr'}}>{Math.round(prog * 100)}%</span>
          </span>
        </div>
        <svg width={W} height={260}>
          {track('الفيديو', 10, 'video', RED)}
          {track('الكتابة', 70, 'cap', RED)}
          {track('المؤثرات', 130, 'sfx', YEL)}
          {track('الموسيقى', 190, 'music', '#7ad7ff')}
          <rect x={20 + prog * TW - 2} y={2} width={4} height={244} rx={2} fill="#fff" />
          <circle cx={20 + prog * TW} cy={4} r={8} fill={RED} />
        </svg>
      </div>
    </Wrap>
  );
};

// ---------- 4. CHECKLIST (each item ticks at its own frame) ----------
export const Checklist: React.FC<{dur: number; x?: number; y?: number; title?: string; items: string[]; at: number[]; neg?: boolean}> = ({dur, x = 1460, y = 470, title = 'سواها كلاود', items, at}) => {
  const {f, fps, p, out} = useInOut(dur);
  return (
    <Wrap x={x} y={y} p={p} out={out} from="right" tilt={1.5}>
      <div style={{...card, width: 520, padding: '20px 26px 16px', direction: 'rtl'}}>
        <div style={{display: 'flex', alignItems: 'center', gap: 12, marginBottom: 10}}>
          <Img src={staticFile('claude.png')} style={{width: 44, height: 44, objectFit: 'contain'}} />
          <span style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 42, color: INK}}>{title}</span>
        </div>
        {items.map((t, i) => {
          const a = at[i] ?? 10 + i * 12;
          const shown = pop(f, fps, a - 4, 13);
          const tick = pop(f, fps, a, 9, 220);
          return (
            <div key={i} style={{display: 'flex', alignItems: 'center', gap: 16, padding: '8px 0', borderTop: i ? '2px solid #f0f0f0' : 'none', opacity: 0.35 + 0.65 * Math.min(1, shown), transform: `translateX(${(1 - shown) * -30}px)`}}>
              <div style={{width: 46, height: 46, borderRadius: 14, background: f >= a ? RED : '#eee', display: 'flex', alignItems: 'center', justifyContent: 'center', flex: 'none'}}>
                <svg width="34" height="34" viewBox="0 0 60 60" style={{transform: `scale(${f >= a ? tick : 0})`}}><path fill="none" stroke="#fff" strokeWidth={9} strokeLinecap="round" strokeLinejoin="round" d="M12 31 l12 12 l24 -26" /></svg>
              </div>
              <span style={{fontFamily: 'Cairo', fontWeight: 800, fontSize: 38, color: INK}}>{t}</span>
            </div>
          );
        })}
      </div>
    </Wrap>
  );
};

// ---------- 5. PHONE showing a screen recording (frames in public/clips/<dir>/0001.jpg…) ----------
export const PhoneClip: React.FC<{dur: number; x?: number; y?: number; dir: string; n: number; rate?: number; start?: number; height?: number; label?: string}> = ({dur, x = 1450, y = 540, dir, n, rate = 1, start = 1, height = 860, label}) => {
  const {f, fps, p, out} = useInOut(dur);
  const idx = Math.min(n, Math.max(1, start + Math.floor(f * rate)));
  const W = height * 0.4625;
  const lab = pop(f, fps, 8, 10);
  return (
    <Wrap x={x} y={y} p={p} out={out} from="down" tilt={4}>
      <div style={{position: 'relative', width: W + 28, height: height + 28, borderRadius: 64, background: '#0b0b0b', padding: 14, boxShadow: '0 30px 60px rgba(0,0,0,0.55), inset 0 0 0 3px #333'}}>
        <div style={{width: W, height, borderRadius: 52, overflow: 'hidden', background: '#000'}}>
          <Img src={staticFile(`clips/${dir}/${String(idx).padStart(4, '0')}.jpg`)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        </div>
        {label && <div style={{position: 'absolute', left: '50%', top: -30, transform: `translateX(-50%) rotate(-4deg) scale(${lab})`, ...chip(RED), fontSize: 40, padding: '6px 26px 0', boxShadow: '0 10px 20px rgba(0,0,0,0.4)'}}>{label}</div>}
      </div>
    </Wrap>
  );
};

// ---------- 6. WIDE IMAGE CARD (16:9 thumbnail etc.) ----------
export const WideCard: React.FC<{dur: number; img: string; x: number; y: number; w?: number; label?: string; tilt?: number}> = ({dur, img, x, y, w = 620, label, tilt = -3}) => {
  const {f, fps, p, out} = useInOut(dur, 10);
  const ring = interpolate(f, [0, 16], [0, 1], clamp);
  const lab = pop(f, fps, 6, 10);
  const float = Math.sin(f / 10) * 5;
  return (
    <Wrap x={x} y={y + float} p={p} out={out} tilt={tilt}>
      {ring < 1 && <div style={{position: 'absolute', left: '50%', top: '50%', width: w * 1.6 * ring, height: w * 1.6 * ring, transform: 'translate(-50%,-50%)', borderRadius: '50%', border: `${10 * (1 - ring)}px solid #fff`, opacity: 1 - ring}} />}
      <div style={{width: w, padding: 12, borderRadius: 26, background: '#fff', boxShadow: '0 22px 46px rgba(0,0,0,0.5), 0 0 0 6px rgba(227,38,42,0.95)'}}>
        <Img src={staticFile(img)} style={{width: '100%', aspectRatio: '16 / 9', objectFit: 'cover', borderRadius: 16, display: 'block'}} />
      </div>
      {label && <div style={{position: 'absolute', left: '50%', bottom: -40, transform: `translateX(-50%) rotate(-2deg) scale(${lab})`, ...chip(RED), fontSize: 42, padding: '4px 26px 0', boxShadow: '0 10px 20px rgba(0,0,0,0.4)'}}>{label}</div>}
    </Wrap>
  );
};

// ---------- 7. BADGE for full-screen inserts (قبل / بعد / ٣ شورتات) ----------
export const Badge: React.FC<{dur: number; text: string; sub?: string; color?: string; x?: number; y?: number}> = ({dur, text, sub, color = RED, x = 960, y = 120}) => {
  const {f, fps, p, out} = useInOut(dur, 9);
  const s2 = pop(f, fps, 6, 11);
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) scale(${(0.3 + 0.7 * p) * out}) rotate(${(1 - p) * 8 - 2}deg)`, display: 'flex', alignItems: 'center', gap: 16, direction: 'rtl'}}>
      <div style={{background: color, color: color === YEL ? INK : '#fff', fontFamily: 'Tajawal', fontWeight: 900, fontSize: 92, lineHeight: 1.1, padding: '8px 44px 0', borderRadius: 24, border: '6px solid #fff', boxShadow: '0 16px 34px rgba(0,0,0,0.5)'}}>{text}</div>
      {sub && <div style={{background: INK, color: '#fff', fontFamily: 'Cairo', fontWeight: 800, fontSize: 40, padding: '6px 24px', borderRadius: 16, transform: `scale(${s2})`, boxShadow: '0 10px 24px rgba(0,0,0,0.45)'}}>{sub}</div>}
    </div>
  );
};

// ---------- 8. COUNTER (e.g. 11:00 → 5:24) ----------
const ar = (s: string) => s.replace(/[0-9]/g, (d) => '٠١٢٣٤٥٦٧٨٩'[+d]);
export const Counter: React.FC<{dur: number; x?: number; y?: number; fromSec: number; toSec: number; label?: string; runFrom?: number; runFor?: number}> = ({dur, x = 1600, y = 900, fromSec, toSec, label, runFrom = 6, runFor = 40}) => {
  const {f, fps, p, out} = useInOut(dur, 10);
  const t = interpolate(f, [runFrom, runFrom + runFor], [fromSec, toSec], {...clamp, easing: Easing.out(Easing.cubic)});
  const mm = Math.floor(t / 60), ss = Math.floor(t % 60);
  const landed = f >= runFrom + runFor;
  const bump = landed ? 1 + 0.15 * Math.exp(-(f - runFrom - runFor) / 5) : 1;
  return (
    <Wrap x={x} y={y} p={p} out={out} tilt={-2}>
      <div style={{display: 'flex', alignItems: 'center', gap: 14, direction: 'rtl'}}>
        {label && <span style={{...chip(INK), fontSize: 36}}>{label}</span>}
        <div style={{background: landed ? RED : '#fff', color: landed ? '#fff' : INK, fontFamily: 'Cairo', fontWeight: 800, fontSize: 84, padding: '0 30px', borderRadius: 22, transform: `scale(${bump})`, boxShadow: '0 14px 30px rgba(0,0,0,0.45)', direction: 'ltr'}}>{ar(`${mm}:${String(ss).padStart(2, '0')}`)}</div>
      </div>
    </Wrap>
  );
};

// ---------- 9. REVISION NOTES (each gets struck = done) ----------
export const NotesList: React.FC<{dur: number; x?: number; y?: number; title?: string; items: string[]; at: number[]}> = ({dur, x = 1450, y = 470, title = 'التعديلات', items, at}) => {
  const {f, fps, p, out} = useInOut(dur);
  return (
    <Wrap x={x} y={y} p={p} out={out} from="right" tilt={2}>
      <div style={{...card, width: 520, padding: '18px 26px', direction: 'rtl', background: '#fffbe8'}}>
        <div style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 42, color: INK, marginBottom: 6}}>{title}</div>
        {items.map((t, i) => {
          const a = at[i];
          const sh = pop(f, fps, a, 12);
          const strike = interpolate(f, [a + 8, a + 16], [0, 1], clamp);
          return (
            <div key={i} style={{position: 'relative', display: 'flex', alignItems: 'center', gap: 12, padding: '6px 0', opacity: Math.min(1, sh * 1.5), transform: `translateY(${(1 - sh) * 20}px)`}}>
              <span style={{fontFamily: 'Cairo', fontWeight: 800, fontSize: 26, color: RED, direction: 'ltr'}}>{ar(`0:${String(12 + i * 17).padStart(2, '0')}`)}</span>
              <span style={{fontFamily: 'Cairo', fontWeight: 800, fontSize: 38, color: strike > 0.5 ? '#999' : INK}}>{t}</span>
              <div style={{position: 'absolute', right: 70, top: '52%', height: 5, borderRadius: 3, background: RED, width: `${strike * 62}%`}} />
            </div>
          );
        })}
      </div>
    </Wrap>
  );
};

// ---------- 10. SKILL FILE (the saved style) ----------
export const SkillFile: React.FC<{dur: number; x?: number; y?: number; title?: string; parts?: string[]}> = ({dur, x = 1430, y = 480, title = 'مونتاج على طريقة ماجد', parts = ['المؤثرات', 'الأصوات', 'الخطوط', 'الشعار']}) => {
  const {f, fps, p, out} = useInOut(dur);
  const seal = pop(f, fps, 14 + parts.length * 6 + 4, 8, 220);
  return (
    <Wrap x={x} y={y} p={p} out={out} from="up" tilt={-2}>
      <div style={{position: 'relative', width: 560, direction: 'rtl'}}>
        <div style={{width: 230, height: 46, background: RED, borderRadius: '20px 20px 0 0', marginRight: 30}} />
        <div style={{...card, borderRadius: '0 26px 26px 26px', background: '#fff', padding: '24px 26px', borderTop: `10px solid ${RED}`}}>
          <div style={{fontFamily: 'Cairo', fontWeight: 800, fontSize: 24, color: '#999'}}>مهارة · SKILL</div>
          <div style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 52, color: INK, lineHeight: 1.15, marginBottom: 14}}>{title}</div>
          <div style={{display: 'flex', flexWrap: 'wrap', gap: 10}}>
            {parts.map((t, i) => {
              const d = pop(f, fps, 14 + i * 6, 9, 220);
              return <span key={t} style={{...chip(i % 2 ? INK : '#f1f1f1', i % 2 ? '#fff' : INK), fontSize: 30, transform: `translateY(${(1 - d) * -120}px) scale(${d})`}}>{t}</span>;
            })}
          </div>
        </div>
        <div style={{position: 'absolute', left: -30, bottom: -30, width: 130, height: 130, borderRadius: '50%', background: YEL, border: '6px solid #fff', display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${seal}) rotate(${(1 - seal) * -90 - 12}deg)`, boxShadow: '0 12px 24px rgba(0,0,0,0.4)'}}>
          <span style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 30, color: INK, textAlign: 'center', lineHeight: 1}}>محفوظة<br />✓</span>
        </div>
      </div>
    </Wrap>
  );
};

// ---------- 11. BRANCH: one sentence → 3 outputs ----------
export const Branch: React.FC<{dur: number; x?: number; y?: number; scale?: number; source?: string; outs?: {t: string; img?: string}[]}> = ({dur, x = 1380, y = 500, scale = 1, source = 'مونتاج على طريقة ماجد', outs = [{t: 'فيديو كامل'}, {t: 'صورة مصغرة'}, {t: '٣ شورتات'}]}) => {
  const {f, fps, p, out} = useInOut(dur);
  const draw = interpolate(f, [10, 24], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const H = 520, W = 760;
  const ys = outs.map((_, i) => 120 + i * 160);
  return (
    <Wrap x={x} y={y} p={p} out={out} from="right" k={scale}>
      <div style={{position: 'relative', width: W, height: H}}>
        <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0}}>
          {ys.map((yy, i) => (
            <path key={i} d={`M ${W - 300} 270 C ${W - 380} 270, ${W - 380} ${yy}, ${W - 470} ${yy}`} fill="none" stroke="#fff" strokeWidth={10} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} style={{filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.5))'}} />
          ))}
        </svg>
        <div style={{position: 'absolute', right: 0, top: 270, transform: 'translateY(-50%)', background: RED, color: '#fff', fontFamily: 'Tajawal', fontWeight: 900, fontSize: 40, padding: '18px 22px 10px', borderRadius: 22, width: 280, textAlign: 'center', lineHeight: 1.15, border: '5px solid #fff', boxShadow: '0 14px 30px rgba(0,0,0,0.5)', direction: 'rtl'}}>{source}</div>
        {outs.map((o, i) => {
          const s = pop(f, fps, 20 + i * 7, 10, 200);
          return (
            <div key={i} style={{position: 'absolute', left: 0, top: ys[i], transform: `translateY(-50%) scale(${s})`, transformOrigin: 'right center', display: 'flex', alignItems: 'center', gap: 12, background: '#fff', borderRadius: 20, padding: '10px 22px 4px', boxShadow: '0 12px 26px rgba(0,0,0,0.45)', direction: 'rtl', width: 270}}>
              <svg width="40" height="40" viewBox="0 0 60 60"><path fill="none" stroke={RED} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" d="M12 31 l12 12 l24 -26" /></svg>
              <span style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 42, color: INK, whiteSpace: 'nowrap'}}>{o.t}</span>
            </div>
          );
        })}
      </div>
    </Wrap>
  );
};

// ---------- 12. BIG NOTICE (disclaimer that must be read) ----------
export const Notice: React.FC<{dur: number; title?: string; text: string; sub?: string; x?: number; y?: number; scale?: number}> = ({dur, title = 'ملاحظة مهمة', text, sub, x = 960, y = 500, scale = 1}) => {
  const {f, fps, p, out} = useInOut(dur, 10);
  const t2 = pop(f, fps, 6, 12);
  const pulse = 1 + 0.03 * Math.sin(f / 4);
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0) 35%, rgba(0,0,0,0.55) 100%)', opacity: Math.min(1, p * 1.5) * out}} />
      <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) scale(${(0.4 + 0.6 * p) * out * pulse * scale}) rotate(${(1 - p) * -8 - 1.5}deg)`, width: 1300, background: YEL, borderRadius: 40, border: `10px solid ${INK}`, boxShadow: '0 30px 70px rgba(0,0,0,0.6)', padding: '34px 56px 30px', direction: 'rtl', textAlign: 'center'}}>
        <div style={{display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 20}}>
          <svg width="96" height="96" viewBox="0 0 24 24"><path d="M12 2L1 21h22z" fill={INK} /><rect x="11" y="9" width="2" height="6" fill={YEL} /><rect x="11" y="16.5" width="2" height="2" fill={YEL} /></svg>
          <span style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 92, color: INK}}>{title}</span>
        </div>
        <div style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 84, color: RED, lineHeight: 1.2, marginTop: 8, transform: `scale(${t2})`, WebkitTextStroke: `2px ${INK}`}}>{text}</div>
        {sub && <div style={{fontFamily: 'Cairo', fontWeight: 800, fontSize: 40, color: INK, marginTop: 10, opacity: t2}}>{sub}</div>}
      </div>
    </AbsoluteFill>
  );
};

// ---------- 13. REFERENCE CARD ("a montage you liked") ----------
export const RefCard: React.FC<{dur: number; x?: number; y?: number; label?: string}> = ({dur, x = 1430, y = 470, label = 'مقطع عجبك'}) => {
  const {f, fps, p, out} = useInOut(dur);
  const heart = pop(f, fps, 14, 7, 240);
  return (
    <Wrap x={x} y={y} p={p} out={out} from="left" tilt={-2}>
      <div style={{...card, width: 540, padding: 18, direction: 'rtl'}}>
        <div style={{marginBottom: 12}}><span style={chip(INK)}>{label}</span></div>
        <div style={{position: 'relative', height: 270, borderRadius: 18, overflow: 'hidden', background: 'linear-gradient(135deg,#3a1d1d,#1a1a2e 60%,#2d1b10)'}}>
          {Array.from({length: 7}, (_, i) => (
            <div key={i} style={{position: 'absolute', left: `${10 + i * 12}%`, top: `${20 + 40 * random(`r${i}`)}%`, width: 70 + 60 * random(`rw${i}`), height: 18, borderRadius: 9, background: [RED, YEL, '#fff'][i % 3], opacity: 0.55, transform: `translateX(${Math.sin(f / 9 + i) * 14}px)`}} />
          ))}
          <div style={{position: 'absolute', left: '50%', top: '50%', width: 86, height: 86, transform: 'translate(-50%,-50%)', borderRadius: '50%', background: 'rgba(255,255,255,0.92)', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
            <svg width="38" height="38" viewBox="0 0 24 24"><path d="M7 4l13 8-13 8z" fill={INK} /></svg>
          </div>
          <svg width="90" height="90" viewBox="0 0 24 24" style={{position: 'absolute', left: 20, bottom: 14, transform: `scale(${heart})`}}><path d="M12 21s-8-5.3-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.7-8 11-8 11z" fill={RED} stroke="#fff" strokeWidth="1.5" /></svg>
        </div>
      </div>
    </Wrap>
  );
};
