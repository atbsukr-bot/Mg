import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, spring, interpolate, Easing, random} from 'remotion';

const RED = '#E3262A';
const INK = '#141414';
const pop = (f: number, fps: number, delay = 0, damping = 11, stiffness = 170) =>
  spring({frame: f - delay, fps, config: {damping, stiffness, mass: 0.7}});
const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};

// ---------------- LOGO ----------------
const CORNER = {x: 1920 - 112, y: 108, size: 150};

export const LogoIntro: React.FC<{dur: number}> = ({dur}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const BIG = 520;
  const slam = interpolate(f, [0, 7], [4.2, 1], {...clamp, easing: Easing.in(Easing.cubic)});
  const settle = f >= 7 ? 1 + 0.08 * Math.exp(-(f - 7) / 4) * Math.cos((f - 7) / 1.6) : 1;
  const fly = interpolate(f, [48, 62], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
  const sizeNow = BIG + (CORNER.size - BIG) * fly;
  const cx = 960 + (CORNER.x - 960) * fly, cy = 540 + (CORNER.y - 540) * fly;
  const spin = interpolate(f, [7, 48], [-14, 6], clamp) + fly * 354;
  const blur = f < 7 ? (7 - f) * 2.2 : 0;
  const dark = interpolate(f, [0, 3, 46, 60], [0, 0.62, 0.55, 0], clamp);
  const ring = interpolate(f, [7, 30], [0, 1], clamp);
  const glow = 0.55 + 0.45 * Math.sin(f / 3);
  if (f >= 62) return null;
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <AbsoluteFill style={{background: 'radial-gradient(circle at 50% 50%, rgba(60,0,0,0.55), rgba(0,0,0,0.95) 75%)', opacity: dark}} />
      {/* shockwave rings */}
      {[0, 6].map((d, i) => {
        const r = interpolate(f, [7 + d, 30 + d], [0, 1], clamp);
        return r > 0 && r < 1 ? (
          <div key={i} style={{position: 'absolute', left: 960, top: 540, width: 1500 * r, height: 1500 * r, transform: 'translate(-50%,-50%)', borderRadius: '50%', border: `${14 * (1 - r)}px solid ${i ? '#fff' : RED}`, opacity: 1 - r, boxShadow: `0 0 60px ${RED}`}} />
        ) : null;
      })}
      {f >= 7 && f < 40 && <Bolts cx={960} cy={540} r={330} f={f} seed="intro" n={9} />}
      <div style={{position: 'absolute', left: cx, top: cy, width: sizeNow, height: sizeNow, transform: `translate(-50%,-50%) scale(${slam * settle}) rotate(${spin}deg)`, filter: `blur(${blur}px) drop-shadow(0 0 ${30 * glow * (1 - fly)}px rgba(227,38,42,0.95))`}}>
        <Img src={staticFile('logo.png')} style={{width: '100%', height: '100%'}} />
        {/* shine sweep */}
        <div style={{position: 'absolute', inset: 0, borderRadius: '50%', overflow: 'hidden'}}>
          <div style={{position: 'absolute', top: '-20%', left: `${interpolate(f, [12, 30], [-80, 160], clamp)}%`, width: '35%', height: '140%', transform: 'rotate(20deg)', background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.65), transparent)'}} />
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const LogoCorner: React.FC<{start: number}> = ({start}) => {
  const f = useCurrentFrame();
  if (f < start) return null;
  const k = f - start;
  const land = k < 10 ? 1 + 0.18 * Math.exp(-k / 3) * Math.cos(k / 1.4) : 1;
  const cyc = k % 450; // every 15 s: a little flip + shine
  const flip = cyc < 24 ? interpolate(cyc, [0, 24], [0, 360], {easing: Easing.inOut(Easing.cubic)}) : 0;
  const sway = Math.sin(k / 38) * 4;
  const bob = Math.sin(k / 29) * 3;
  const shine = interpolate(cyc, [24, 44], [-80, 160], clamp);
  return (
    <div style={{position: 'absolute', left: CORNER.x, top: CORNER.y + bob, width: CORNER.size, height: CORNER.size, transform: `translate(-50%,-50%) scale(${land}) rotateY(${flip}deg) rotate(${sway}deg)`, filter: 'drop-shadow(0 6px 14px rgba(0,0,0,0.55))'}}>
      <Img src={staticFile('logo.png')} style={{width: '100%', height: '100%'}} />
      <div style={{position: 'absolute', inset: 0, borderRadius: '50%', overflow: 'hidden'}}>
        <div style={{position: 'absolute', top: '-20%', left: `${shine}%`, width: '30%', height: '140%', transform: 'rotate(20deg)', background: 'linear-gradient(90deg, transparent, rgba(255,255,255,0.55), transparent)'}} />
      </div>
    </div>
  );
};

// ---------------- LIGHTNING / SPARKS ----------------
const Bolts: React.FC<{cx: number; cy: number; r: number; f: number; seed: string; n: number; color?: string}> = ({cx, cy, r, f, seed, n, color = '#ffe9a8'}) => {
  const step = Math.floor(f / 2); // re-randomise every 2 frames: flicker
  return (
    <svg style={{position: 'absolute', left: 0, top: 0}} width={1920} height={1080}>
      <defs><filter id={`bg${seed}`}><feGaussianBlur stdDeviation="6" result="b" /><feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge></filter></defs>
      {Array.from({length: n}, (_, i) => {
        const a = (i / n) * Math.PI * 2 + random(`${seed}a${i}${step}`) * 0.5;
        const r0 = r * 0.55, r1 = r * (1 + random(`${seed}l${i}${step}`) * 0.5);
        let d = `M ${cx + Math.cos(a) * r0} ${cy + Math.sin(a) * r0}`;
        const segs = 6;
        for (let s = 1; s <= segs; s++) {
          const rr = r0 + ((r1 - r0) * s) / segs;
          const j = (random(`${seed}j${i}${s}${step}`) - 0.5) * 0.35;
          d += ` L ${cx + Math.cos(a + j) * rr} ${cy + Math.sin(a + j) * rr}`;
        }
        const on = random(`${seed}o${i}${step}`) > 0.25;
        return on ? <path key={i} d={d} stroke={color} strokeWidth={4} fill="none" filter={`url(#bg${seed})`} strokeLinejoin="round" /> : null;
      })}
    </svg>
  );
};

export const Sparks: React.FC<{dur: number; x: number; y: number; r?: number}> = ({dur, x, y, r = 160}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 2, dur - 4, dur], [0, 1, 1, 0], clamp);
  const s = interpolate(f, [0, 6], [0.4, 1], clamp);
  return (
    <AbsoluteFill style={{opacity: o, pointerEvents: 'none'}}>
      <div style={{position: 'absolute', left: x, top: y, width: r * 1.6 * s, height: r * 1.6 * s, transform: 'translate(-50%,-50%)', borderRadius: '50%', background: 'radial-gradient(circle, rgba(255,240,180,0.9), rgba(255,170,40,0.45) 35%, transparent 70%)', mixBlendMode: 'screen'}} />
      <Bolts cx={x} cy={y} r={r * s} f={f} seed={`sp${x}${y}`} n={10} />
    </AbsoluteFill>
  );
};

// ---------------- CAPTION ----------------
export const Caption: React.FC<{words: string[]; hl: number}> = ({words, hl}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = pop(f, fps, 0, 13, 220);
  return (
    <div style={{position: 'absolute', left: 0, right: 0, bottom: 64, display: 'flex', justifyContent: 'center', pointerEvents: 'none'}}>
      <div style={{direction: 'rtl', display: 'flex', gap: 14, alignItems: 'center', transform: `scale(${0.82 + 0.18 * p}) translateY(${(1 - p) * 16}px)`, opacity: Math.min(1, p * 2)}}>
        {words.map((w, i) => i === hl ? (
          <span key={i} style={{fontFamily: 'Cairo', fontWeight: 800, fontSize: 58, color: '#fff', background: RED, padding: '0 18px 6px', borderRadius: 12, boxShadow: '0 6px 0 rgba(0,0,0,0.35)', transform: `rotate(-2deg) scale(${1 + 0.12 * Math.max(0, 1 - f / 8)})`, display: 'inline-block'}}>{w}</span>
        ) : (
          <span key={i} style={{fontFamily: 'Cairo', fontWeight: 800, fontSize: 58, color: '#fff', WebkitTextStroke: '3px rgba(0,0,0,0.85)', paintOrder: 'stroke fill', textShadow: '0 0 4px #000, 0 0 10px rgba(0,0,0,0.85), 0 4px 0 rgba(0,0,0,0.9), 0 6px 18px rgba(0,0,0,0.6)'}}>{w}</span>
        ))}
      </div>
    </div>
  );
};

// ---------------- KEYWORD POP (Khater style) ----------------
const ICONS: Record<string, (c: string) => React.ReactNode> = {
  guitar: (c) => (<g fill="none" stroke={c} strokeWidth={4} strokeLinecap="round"><circle cx="20" cy="36" r="10" /><circle cx="30" cy="27" r="7" /><path d="M33 24 L50 7" /><path d="M46 5 l6 6" /><circle cx="22" cy="34" r="2.5" fill={c} /></g>),
  note: (c) => (<g fill={c}><ellipse cx="18" cy="42" rx="9" ry="7" /><ellipse cx="42" cy="36" rx="9" ry="7" /><path d="M25 42 V12 L51 6 V36 h-3 V14 L28 19 V42z" /></g>),
  fire: (c) => (<path fill={c} d="M30 4c4 10 14 14 14 28a14 14 0 0 1-28 0c0-8 5-12 7-17 1 5 3 7 6 8-2-7 0-13 1-19z" />),
  check: (c) => (<path fill="none" stroke={c} strokeWidth={7} strokeLinecap="round" strokeLinejoin="round" d="M12 30 l12 12 l24 -26" />),
  star: (c) => (<path fill={c} d="M30 5l7 16 17 2-13 11 4 17-15-9-15 9 4-17L6 23l17-2z" />),
  clock: (c) => (<g fill="none" stroke={c} strokeWidth={5} strokeLinecap="round"><circle cx="30" cy="30" r="22" /><path d="M30 16v15l10 6" /></g>),
  mic: (c) => (<g fill="none" stroke={c} strokeWidth={5} strokeLinecap="round"><rect x="21" y="6" width="18" height="30" rx="9" fill={c} /><path d="M13 28a17 17 0 0 0 34 0M30 45v9" /></g>),
  hand: (c) => (<path fill={c} d="M22 52c-6-4-12-14-12-20 0-3 4-4 6-1l5 7V12a3.5 3.5 0 0 1 7 0v14V8a3.5 3.5 0 0 1 7 0v18-14a3.5 3.5 0 0 1 7 0v16-9a3.5 3.5 0 0 1 7 0v17c0 9-5 16-12 16z" />),
  up: (c) => (<path fill={c} d="M30 6l20 22H38v24H22V28H10z" />),
  bulb: (c) => (<g fill={c}><path d="M30 6a17 17 0 0 0-10 31c2 2 3 4 3 7h14c0-3 1-5 3-7A17 17 0 0 0 30 6z" /><rect x="23" y="47" width="14" height="5" rx="2" /></g>),
};
export const Keyword: React.FC<{dur: number; text: string; x: number; y: number; color?: 'red' | 'white' | 'dark' | 'yellow'; icon?: string; tilt?: number; size?: number}> = ({dur, text, x, y, color = 'red', icon, tilt = -3, size = 64}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = pop(f, fps, 0, 10, 200);
  const ip = pop(f, fps, 4, 8, 200);
  const out = interpolate(f, [dur - 6, dur], [1, 0], clamp);
  const pal = {red: [RED, '#fff', '#fff'], white: ['#fff', INK, RED], dark: [INK, '#fff', RED], yellow: ['#FFD23F', INK, INK]}[color];
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) rotate(${tilt + (1 - p) * 10}deg) scale(${p * out})`, display: 'flex', alignItems: 'center', gap: 14, direction: 'rtl', filter: 'drop-shadow(0 10px 18px rgba(0,0,0,0.45))'}}>
      {icon && ICONS[icon] && (
        <div style={{width: size * 1.25, height: size * 1.25, borderRadius: '50%', background: pal[1] === '#fff' ? '#fff' : RED, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: `scale(${ip}) rotate(${(1 - ip) * -90}deg)`}}>
          <svg width={size * 0.8} height={size * 0.8} viewBox="0 0 60 60">{ICONS[icon](pal[1] === '#fff' ? RED : '#fff')}</svg>
        </div>
      )}
      <div style={{background: pal[0], color: pal[1], fontFamily: 'Tajawal', fontWeight: 900, fontSize: size, lineHeight: 1.25, padding: `${size * 0.12}px ${size * 0.42}px ${size * 0.02}px`, borderRadius: size * 0.28, whiteSpace: 'nowrap', borderBottom: `${size * 0.09}px solid ${pal[2] === pal[1] ? 'rgba(0,0,0,0.25)' : pal[2]}`}}>{text}</div>
    </div>
  );
};

// ---------------- LOWER THIRD ----------------
export const LowerThird: React.FC<{dur: number; name?: string; sub?: string}> = ({dur, name = 'ماجد خالد', sub = 'MN COUSINS'}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const bar = pop(f, fps, 0, 14);
  const t1 = pop(f, fps, 5, 13);
  const t2 = pop(f, fps, 10, 13);
  const out = interpolate(f, [dur - 10, dur], [0, 1], {...clamp, easing: Easing.in(Easing.cubic)});
  return (
    <div style={{position: 'absolute', right: 90, bottom: 200, direction: 'rtl', transform: `translateX(${out * 700}px)`}}>
      <div style={{display: 'flex', alignItems: 'stretch'}}>
        <div style={{width: 14, background: RED, transform: `scaleY(${bar})`, borderRadius: 4}} />
        <div style={{overflow: 'hidden', paddingRight: 18}}>
          <div style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 64, color: '#fff', background: INK, padding: '6px 26px 0', transform: `translateX(${(1 - t1) * 500}px)`, borderRadius: '0 0 0 0'}}>{name}</div>
          <div style={{fontFamily: 'Cairo', fontWeight: 800, fontSize: 28, color: '#fff', background: RED, display: 'inline-block', padding: '0 20px', letterSpacing: 4, transform: `translateX(${(1 - t2) * 500}px)`}}>{sub}</div>
        </div>
      </div>
    </div>
  );
};

// ---------------- SUBSCRIBE / LIKE / SHARE ----------------
export const Subscribe: React.FC<{dur: number; x?: number; y?: number}> = ({dur, x = 960, y = 800}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const inP = pop(f, fps, 0, 12);
  const out = interpolate(f, [dur - 10, dur], [1, 0], clamp);
  const CLICK_SUB = 30, CLICK_BELL = 52, CLICK_LIKE = 72, CLICK_SHARE = 92;
  const subbed = f >= CLICK_SUB;
  const press = (c: number) => (f >= c && f < c + 6 ? 0.88 : 1) * (f >= c + 6 ? 1 + 0.12 * Math.exp(-(f - c - 6) / 4) : 1);
  // cursor path
  const pts = [[1000, 260, 0], [727, 60, CLICK_SUB - 4], [491, 60, CLICK_BELL - 4], [322, 60, CLICK_LIKE - 4], [100, 60, CLICK_SHARE - 4], [100, 300, dur]];
  let cx = pts[0][0], cy = pts[0][1];
  for (let i = 0; i < pts.length - 1; i++) {
    const [x0, y0, t0] = pts[i], [x1, y1, t1] = pts[i + 1];
    const s0 = i === 0 ? 8 : t0 + 8;
    if (f >= s0) {
      const t = interpolate(f, [s0, t1], [0, 1], {...clamp, easing: Easing.inOut(Easing.cubic)});
      cx = x0 + (x1 - x0) * t; cy = y0 + (y1 - y0) * t;
    }
  }
  const clicking = [CLICK_SUB, CLICK_BELL, CLICK_LIKE, CLICK_SHARE].some((c) => f >= c - 2 && f < c + 4);
  const bellRot = f >= CLICK_BELL ? Math.sin((f - CLICK_BELL) * 1.4) * 28 * Math.exp(-(f - CLICK_BELL) / 12) : 0;
  const liked = f >= CLICK_LIKE, shared = f >= CLICK_SHARE;
  const glow = 0.5 + 0.5 * Math.sin(f / 4);
  const pill = (bg: string): React.CSSProperties => ({height: 96, borderRadius: 48, background: bg, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: `0 10px 24px rgba(0,0,0,0.35), 0 0 ${18 + 22 * glow}px rgba(255,${bg === '#fff' ? 255 : 60},${bg === '#fff' ? 255 : 60},${0.45 + 0.35 * glow})`});
  const bounceIn = (i: number) => { const b = spring({frame: f - 4 - i * 4, fps, config: {damping: 7, stiffness: 220, mass: 0.6}}); return `scale(${0.4 + 0.6 * b}) translateY(${(1 - b) * 60}px)`; };
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) scale(${inP * out})`, opacity: out}}>
      <div style={{position: 'relative', display: 'flex', gap: 22, alignItems: 'center', direction: 'ltr'}}>
        {/* share */}
        <div style={{...pill(shared ? RED : '#fff'), width: 200, gap: 10, transform: `${bounceIn(3)} scale(${press(CLICK_SHARE)})`}}>
          <svg width="44" height="44" viewBox="0 0 24 24"><path fill={shared ? '#fff' : INK} d="M14 5l7 7-7 7v-4c-5 0-8.5 1.6-11 5 1-5 4-10 11-11z" /></svg>
          <span style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 40, color: shared ? '#fff' : INK}}>شير</span>
        </div>
        {/* like */}
        <div style={{...pill(liked ? RED : '#fff'), width: 200, gap: 10, transform: `${bounceIn(2)} scale(${press(CLICK_LIKE)})`}}>
          <svg width="46" height="46" viewBox="0 0 24 24"><path fill={liked ? '#fff' : INK} d="M2 21h4V9H2v12zm20-11c0-1.1-.9-2-2-2h-6.3l1-4.6v-.3c0-.4-.2-.8-.4-1.1L13.2 1 6.6 7.6C6.2 8 6 8.5 6 9v10c0 1.1.9 2 2 2h9c.8 0 1.5-.5 1.8-1.2l3-7.1c.1-.2.2-.5.2-.7v-2z" /></svg>
          <span style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 40, color: liked ? '#fff' : INK}}>لايك</span>
        </div>
        {/* bell */}
        <div style={{...pill(f >= CLICK_BELL ? '#FFD23F' : '#fff'), width: 96, transform: `${bounceIn(1)} scale(${press(CLICK_BELL)})`}}>
          <svg width="50" height="50" viewBox="0 0 24 24" style={{transform: `rotate(${bellRot}deg)`, transformOrigin: '50% 10%'}}><path fill={INK} d="M12 22a2 2 0 0 0 2-2h-4a2 2 0 0 0 2 2zm6-6V11c0-3.1-1.6-5.6-4.5-6.3V4a1.5 1.5 0 0 0-3 0v.7C7.6 5.4 6 7.9 6 11v5l-2 2v1h16v-1l-2-2z" /></svg>
        </div>
        {/* subscribe */}
        <div style={{...pill(subbed ? '#3a3a3a' : RED), width: 330, gap: 14, transform: `${bounceIn(0)} scale(${press(CLICK_SUB)})`}}>
          <Img src={staticFile('logo.png')} style={{width: 66, height: 66}} />
          <span style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 46, color: '#fff', direction: 'rtl'}}>{subbed ? 'مشترك ✓' : 'اشترك'}</span>
        </div>
        {/* burst rings on clicks */}
        {[[CLICK_SUB, 727], [CLICK_BELL, 491], [CLICK_LIKE, 322], [CLICK_SHARE, 100]].map(([c, px], i) => {
          const r = interpolate(f, [c, c + 14], [0, 1], clamp);
          return r > 0 && r < 1 ? <div key={i} style={{position: 'absolute', left: px, top: 48, width: 220 * r, height: 220 * r, transform: 'translate(-50%,-50%)', borderRadius: '50%', border: `${8 * (1 - r)}px solid ${i === 1 ? '#FFD23F' : RED}`, opacity: 1 - r}} /> : null;
        })}
        {/* cursor hand */}
        <svg width="74" height="74" viewBox="0 0 60 60" style={{position: 'absolute', left: cx - 26, top: cy, transform: `scale(${clicking ? 0.85 : 1})`, filter: 'drop-shadow(0 4px 6px rgba(0,0,0,0.5))'}}>
          <path fill="#fff" stroke={INK} strokeWidth={3} strokeLinejoin="round" d="M22 56c-6-4-12-14-12-20 0-3 4-4 6-1l5 7V8a3.5 3.5 0 0 1 7 0v20V18a3.5 3.5 0 0 1 7 0v12-8a3.5 3.5 0 0 1 7 0v10-5a3.5 3.5 0 0 1 7 0v15c0 9-5 16-12 16z" />
        </svg>
      </div>
    </div>
  );
};

// ---------------- IMAGE CARD (pointed-at picture) ----------------
export const ImageCard: React.FC<{dur: number; img: string; x: number; y: number; size?: number; label?: string}> = ({dur, img, x, y, size = 300, label}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = pop(f, fps, 0, 9, 190);
  const out = interpolate(f, [dur - 8, dur], [1, 0], clamp);
  const ring = interpolate(f, [0, 16], [0, 1], clamp);
  const float = Math.sin(f / 9) * 6;
  return (
    <div style={{position: 'absolute', left: x, top: y + float, transform: `translate(-50%,-50%) scale(${p * out}) rotate(${(1 - p) * -25 + 3}deg)`}}>
      {ring < 1 && <div style={{position: 'absolute', left: '50%', top: '50%', width: size * 2.4 * ring, height: size * 2.4 * ring, transform: 'translate(-50%,-50%)', borderRadius: '50%', border: `${10 * (1 - ring)}px solid #fff`, opacity: 1 - ring}} />}
      <div style={{width: size, height: size, borderRadius: 40, background: '#fff', padding: 18, boxShadow: '0 18px 40px rgba(0,0,0,0.45), 0 0 0 6px rgba(227,38,42,0.9)'}}>
        <Img src={staticFile(img)} style={{width: '100%', height: '100%', objectFit: 'contain'}} />
      </div>
      {label && <div style={{position: 'absolute', left: '50%', bottom: -34, transform: 'translateX(-50%) rotate(-3deg)', background: RED, color: '#fff', fontFamily: 'Tajawal', fontWeight: 900, fontSize: 40, padding: '2px 22px 0', borderRadius: 12, whiteSpace: 'nowrap'}}>{label}</div>}
    </div>
  );
};

// ---------------- ARROW ----------------
export const Arrow: React.FC<{dur: number; x1: number; y1: number; x2: number; y2: number; label?: string; bend?: number}> = ({dur, x1, y1, x2, y2, label, bend = 120}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const draw = interpolate(f, [0, 12], [0, 1], {...clamp, easing: Easing.out(Easing.cubic)});
  const head = pop(f, fps, 10, 8, 220);
  const lab = pop(f, fps, 2, 10, 200);
  const out = interpolate(f, [dur - 6, dur], [1, 0], clamp);
  const mx = (x1 + x2) / 2 - ((y2 - y1) * bend) / 400, my = (y1 + y2) / 2 + ((x2 - x1) * bend) / 400;
  const d = `M ${x1} ${y1} Q ${mx} ${my} ${x2} ${y2}`;
  const ang = (Math.atan2(y2 - my, x2 - mx) * 180) / Math.PI;
  const wob = Math.sin(f / 4) * 6;
  const hx = x2 + Math.cos((ang * Math.PI) / 180) * wob, hy = y2 + Math.sin((ang * Math.PI) / 180) * wob;
  return (
    <AbsoluteFill style={{opacity: out, pointerEvents: 'none'}}>
      <svg width={1920} height={1080} style={{position: 'absolute', filter: 'drop-shadow(0 6px 8px rgba(0,0,0,0.5))'}}>
        <path d={d} fill="none" stroke="#fff" strokeWidth={22} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />
        <path d={d} fill="none" stroke={RED} strokeWidth={12} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />
        <g transform={`translate(${hx} ${hy}) rotate(${ang}) scale(${head})`}>
          <path d="M 18 0 L -30 -30 L -18 0 L -30 30 Z" fill={RED} stroke="#fff" strokeWidth={6} strokeLinejoin="round" />
        </g>
      </svg>
      {label && <div style={{position: 'absolute', left: x1, top: y1, transform: `translate(-50%,-115%) rotate(-4deg) scale(${lab})`, background: RED, color: '#fff', fontFamily: 'Tajawal', fontWeight: 900, fontSize: 56, padding: '6px 26px 0', borderRadius: 16, borderBottom: '6px solid rgba(0,0,0,0.25)', whiteSpace: 'nowrap', boxShadow: '0 10px 20px rgba(0,0,0,0.4)'}}>{label}</div>}
    </AbsoluteFill>
  );
};

// ---------------- BIG BEAT WORD ----------------
export const BeatWord: React.FC<{dur: number; text: string; x?: number; y?: number; color?: string; size?: number; tilt?: number}> = ({dur, text, x = 960, y = 470, color = '#FFD23F', size = 230, tilt = -6}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f, fps, config: {damping: 8, stiffness: 260, mass: 0.6}});
  const out = interpolate(f, [dur - 5, dur], [1, 0], clamp);
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) rotate(${tilt}deg) scale(${0.3 + 0.7 * p})`, opacity: out,
      fontFamily: 'Tajawal', fontWeight: 900, fontSize: size, color, lineHeight: 1, whiteSpace: 'nowrap', direction: 'rtl',
      WebkitTextStroke: '12px #141414', paintOrder: 'stroke fill', textShadow: '0 14px 0 #141414, 0 22px 40px rgba(0,0,0,0.5)'}}>{text}</div>
  );
};
