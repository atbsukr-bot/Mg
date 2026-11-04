import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, spring, interpolate, Easing} from 'remotion';

// "Archive / scrapbook" explainer style: paper strip labels, index cards, taped photos, typewriter dates.
// Fonts: Amiri (Arabic naskh), Special Elite (typewriter), Courier Prime.
const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};
export const TONES: Record<string, {bg: string; fg: string; edge: string}> = {
  blue: {bg: '#CFE3EE', fg: '#22343F', edge: '#A9C6D6'},
  cream: {bg: '#F1E7D2', fg: '#2B2418', edge: '#D9C9A6'},
  green: {bg: '#D7E8C8', fg: '#22311A', edge: '#B5CDA0'},
  paper: {bg: '#F6F3EC', fg: '#2A2A2A', edge: '#DCD6C8'},
  yellow: {bg: '#F4E6A6', fg: '#2E2810', edge: '#DCCB7E'},
  red: {bg: '#D8463C', fg: '#FFFFFF', edge: '#B23128'},
};
const AR = 'Amiri', TYPE = 'Special Elite';
const isLatin = (s: string) => /^[\x00-\x7F•·\s]*$/.test(s);
const out = (f: number, dur: number) => interpolate(f, [dur - 7, dur], [1, 0], clamp);

// paper grain (static per 2 frames)
const Grain: React.FC<{id: string; o?: number}> = ({id, o = 0.18}) => {
  const f = useCurrentFrame();
  return (
    <svg width="100%" height="100%" style={{position: 'absolute', inset: 0, opacity: o, mixBlendMode: 'multiply', pointerEvents: 'none'}}>
      <filter id={id}><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves={2} seed={Math.floor(f / 2) % 7} /><feColorMatrix values="0 0 0 0 0.35  0 0 0 0 0.3  0 0 0 0 0.25  0 0 0 0.9 0" /></filter>
      <rect width="100%" height="100%" filter={`url(#${id})`} />
    </svg>
  );
};

// ---------- full-frame paper canvas (explainer scene) ----------
export const PaperBg: React.FC<{dur: number; sheets?: boolean}> = ({dur, sheets = true}) => {
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const o = interpolate(f, [0, 6, dur - 6, dur], [0, 1, 1, 0], clamp);
  const push = 1 + 0.04 * (f / Math.max(1, dur)); // slow push-in
  return (
    <AbsoluteFill style={{opacity: o, overflow: 'hidden'}}>
      <AbsoluteFill style={{transform: `scale(${push})`, background: 'radial-gradient(ellipse at 50% 45%, #F3EFE6 0%, #E7E1D4 70%, #D9D1C0 100%)'}}>
        {sheets && [[0.06, 0.12, -3], [0.7, 0.58, 4], [0.03, 0.62, 2]].map(([x, y, r], i) => (
          <div key={i} style={{position: 'absolute', left: width * x, top: height * y, width: width * 0.24, height: height * 0.34, background: 'repeating-linear-gradient(180deg, #F8F6F0 0 26px, #DCE3EA 26px 27px)', transform: `rotate(${r}deg)`, boxShadow: '0 4px 14px rgba(0,0,0,0.08)', opacity: 0.55}} />
        ))}
        <Grain id="pbg" o={0.22} />
      </AbsoluteFill>
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 50%, transparent 60%, rgba(60,40,20,0.18) 100%)'}} />
    </AbsoluteFill>
  );
};

// ---------- paper strip label ----------
export const PaperTag: React.FC<{dur: number; text: string; x: number; y: number; tone?: string; size?: number; tilt?: number; delay?: number; bullet?: boolean; font?: 'ar' | 'type'; tape?: boolean}> =
  ({dur, text, x, y, tone = 'cream', size = 46, tilt = 0, delay = 0, bullet = true, font, tape = false}) => {
  const f = useCurrentFrame() - delay;
  const {fps} = useVideoConfig();
  if (f < 0) return null;
  const T = TONES[tone] ?? TONES.cream;
  const latin = font ? font === 'type' : isLatin(text);
  const wipe = interpolate(f, [0, 9], [0, 100], {...clamp, easing: Easing.out(Easing.cubic)});
  const p = spring({frame: f, fps, config: {damping: 14, stiffness: 180, mass: 0.6}});
  const o = out(f + delay, dur);
  // rtl reveals from the right edge, latin from the left
  const clip = latin ? `inset(0 ${100 - wipe}% 0 0)` : `inset(0 0 0 ${100 - wipe}%)`;
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) rotate(${tilt}deg) scale(${0.94 + 0.06 * p})`, opacity: o, filter: 'drop-shadow(0 5px 6px rgba(40,30,15,0.28))'}}>
      <div style={{clipPath: clip, position: 'relative', background: T.bg, color: T.fg, border: `1.5px solid ${T.edge}`, padding: latin ? `${size * 0.22}px ${size * 0.5}px ${size * 0.16}px` : `${size * 0.05}px ${size * 0.5}px ${size * 0.2}px`, borderRadius: 3,
        fontFamily: latin ? TYPE : AR, fontWeight: latin ? 400 : 700, fontSize: size, lineHeight: 1.25, whiteSpace: 'nowrap', direction: latin ? 'ltr' : 'rtl', letterSpacing: latin ? 2 : 0}}>
        {bullet && <span style={{marginInlineEnd: size * 0.3, opacity: 0.8}}>•</span>}{text}
        <Grain id={`pt${x}${y}`} o={0.2} />
      </div>
      {tape && <div style={{position: 'absolute', left: '50%', top: -size * 0.28, width: size * 1.6, height: size * 0.5, transform: 'translateX(-50%) rotate(-4deg)', background: 'rgba(235,225,195,0.75)', boxShadow: '0 1px 2px rgba(0,0,0,0.12)', opacity: wipe / 100}} />}
    </div>
  );
};

// ---------- stacked bullet list (one tag per spoken point) ----------
export const PaperList: React.FC<{dur: number; x: number; y: number; items: {text: string; tone?: string; at: number}[]; gap?: number; size?: number; align?: 'right' | 'left'}> = ({dur, x, y, items, gap = 92, size = 46}) => (
  <>
    {items.map((it, i) => (
      <PaperTag key={i} dur={dur} text={it.text} tone={it.tone ?? (i % 2 ? 'blue' : 'cream')} x={x} y={y + i * gap} delay={it.at} size={size} tilt={[0.6, -0.8, 0.4, -0.5][i % 4]} />
    ))}
  </>
);

// ---------- index card: person / place ----------
export const PersonCard: React.FC<{dur: number; x: number; y: number; img?: string; name: string; latin?: string; note?: string; scale?: number; tilt?: number}> = ({dur, x, y, img, name, latin, note, scale = 1, tilt = -1.5}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f, fps, config: {damping: 13, stiffness: 150, mass: 0.7}});
  const typed = latin ? latin.slice(0, Math.max(0, Math.floor((f - 10) / 1.6))) : '';
  const W = 620, H = 250;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: W, height: H, transform: `translate(-50%,-50%) translateY(${(1 - p) * 60}px) rotate(${tilt + (1 - p) * 5}deg) scale(${scale})`, opacity: Math.min(1, p * 1.6) * out(f, dur), filter: 'drop-shadow(0 10px 12px rgba(40,30,15,0.3))'}}>
      <div style={{position: 'absolute', right: 40, top: -26, width: 150, height: 30, background: '#E9DDBF', borderRadius: '8px 8px 0 0', border: '1.5px solid #D2C29C', borderBottom: 'none'}} />
      <div style={{position: 'absolute', inset: 0, background: 'linear-gradient(180deg, #F3E9D3, #EBDFC3)', border: '1.5px solid #D2C29C', borderRadius: 4, overflow: 'hidden'}}>
        <div style={{position: 'absolute', left: 0, right: 0, top: 38, height: 1.5, background: '#D9A5A0'}} />
        {[0, 1, 2, 3].map((k) => <div key={k} style={{position: 'absolute', left: 0, right: 0, top: 86 + k * 44, height: 1, background: '#C9D3DC', opacity: 0.6}} />)}
        <div style={{position: 'absolute', left: 24, top: 8, fontFamily: TYPE, fontSize: 18, color: '#8A7B5C', letterSpacing: 3}}>FILE · NO. 07</div>
        {img && <div style={{position: 'absolute', left: 26, top: 56, width: 150, height: 170, background: '#fff', padding: 7, boxShadow: '0 3px 6px rgba(0,0,0,0.2)', transform: 'rotate(-2deg)'}}><Img src={staticFile(img)} style={{width: '100%', height: '100%', objectFit: 'cover', filter: 'grayscale(1) sepia(0.35) contrast(1.1)'}} /></div>}
        <div style={{position: 'absolute', right: 34, top: 64, direction: 'rtl', fontFamily: AR, fontWeight: 700, fontSize: 54, color: '#2B2418'}}>• {name}</div>
        {latin && <div style={{position: 'absolute', right: 40, top: 142, fontFamily: TYPE, fontSize: 30, color: '#6E6450', letterSpacing: 3}}>{typed}<span style={{opacity: f % 16 < 8 ? 1 : 0}}>|</span></div>}
        {note && <div style={{position: 'absolute', right: 40, top: 188, direction: 'rtl', fontFamily: AR, fontSize: 30, color: '#8A2B22'}}>{note}</div>}
        <Grain id={`pc${x}`} o={0.25} />
      </div>
    </div>
  );
};

// ---------- vocab card: english word + arabic meaning ----------
export const VocabCard: React.FC<{dur: number; x: number; y: number; word: string; meaning: string; head?: string; scale?: number}> = ({dur, x, y, word, meaning, head = 'كلمة من الدرس', scale = 1}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f, fps, config: {damping: 13, stiffness: 160, mass: 0.6}});
  return (
    <div style={{position: 'absolute', left: x, top: y, width: 560, height: 230, transform: `translate(-50%,-50%) rotate(${-1 + (1 - p) * -6}deg) scale(${(0.85 + 0.15 * p) * scale})`, opacity: Math.min(1, p * 1.6) * out(f, dur), filter: 'drop-shadow(0 10px 12px rgba(40,30,15,0.3))'}}>
      <div style={{position: 'absolute', left: 30, top: -24, background: '#DCE8EF', border: '1.5px solid #B7CCD8', padding: '0 14px', fontFamily: TYPE, fontSize: 18, color: '#3D5563', letterSpacing: 3}}>VOCAB</div>
      <div style={{position: 'absolute', inset: 0, background: '#F4EEDF', border: '1.5px solid #D6CAAA', borderRadius: 4, overflow: 'hidden'}}>
        <div style={{position: 'absolute', right: 22, top: 10, direction: 'rtl', fontFamily: AR, fontSize: 22, color: '#7B6E52'}}>{head}</div>
        <div style={{position: 'absolute', left: 30, top: 44, fontFamily: 'Courier Prime', fontWeight: 700, fontSize: 64, color: '#22343F'}}><span style={{color: '#4A78B0'}}>• </span>{word}</div>
        <Grain id={`vc${x}`} o={0.25} />
      </div>
      <PaperTag dur={dur} text={meaning} x={400} y={172} tone="green" size={44} bullet={false} delay={12} />
    </div>
  );
};

// ---------- taped photo / clipping ----------
export const TapedPhoto: React.FC<{dur: number; x: number; y: number; img: string; w?: number; h?: number; caption?: string; tilt?: number; bw?: boolean}> = ({dur, x, y, img, w = 420, h = 300, caption, tilt = 2, bw = true}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f, fps, config: {damping: 12, stiffness: 140, mass: 0.8}});
  const tapeIn = interpolate(f, [8, 14], [0, 1], clamp);
  const typed = caption ? caption.slice(0, Math.max(0, Math.floor((f - 14) / 1.2))) : '';
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) translateY(${(1 - p) * -90}px) rotate(${tilt + (1 - p) * -10}deg) scale(${1.15 - 0.15 * p})`, opacity: Math.min(1, p * 2) * out(f, dur)}}>
      <div style={{background: '#FBF9F3', padding: 14, boxShadow: '0 14px 22px rgba(40,30,15,0.35)'}}>
        <Img src={staticFile(img)} style={{width: w, height: h, objectFit: 'cover', display: 'block', filter: bw ? 'grayscale(1) sepia(0.3) contrast(1.08)' : 'sepia(0.15)'}} />
      </div>
      {[[-1, -1, -38], [1, -1, 38]].map(([sx, sy, r], i) => (
        <div key={i} style={{position: 'absolute', left: sx < 0 ? -26 : undefined, right: sx > 0 ? -26 : undefined, top: -12, width: 110, height: 34, transform: `rotate(${r}deg)`, background: 'rgba(232,222,190,0.82)', boxShadow: '0 1px 3px rgba(0,0,0,0.15)', opacity: tapeIn}} />
      ))}
      {caption && <div style={{marginTop: 10, textAlign: 'center', fontFamily: TYPE, fontSize: 22, color: '#5E564A', letterSpacing: 2, direction: isLatin(caption) ? 'ltr' : 'rtl'}}>{typed}</div>}
    </div>
  );
};

// ---------- typewriter date / place stamp ----------
export const DateStamp: React.FC<{dur: number; x: number; y: number; text: string; tone?: string; size?: number}> = ({dur, x, y, text, tone = 'blue', size = 58}) => {
  const f = useCurrentFrame();
  const T = TONES[tone] ?? TONES.blue;
  const n = Math.max(0, Math.floor((f - 3) / 2));
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: 'translate(-50%,-50%) rotate(-1deg)', opacity: out(f, dur), filter: 'drop-shadow(0 5px 6px rgba(40,30,15,0.28))'}}>
      <div style={{position: 'relative', background: T.bg, border: `1.5px solid ${T.edge}`, padding: `${size * 0.18}px ${size * 0.45}px ${size * 0.1}px`, fontFamily: TYPE, fontSize: size, color: T.fg, letterSpacing: 4, whiteSpace: 'nowrap', direction: 'ltr', minWidth: size * 2}}>
        • {text.slice(0, n)}<span style={{opacity: n < text.length || f % 16 < 8 ? 1 : 0}}>_</span>
        <Grain id={`ds${x}${y}`} o={0.2} />
      </div>
    </div>
  );
};
