/**
 * The owner's subscribe / bell / like / share animation, from his montage kit (montage/kit/app/src/Graphics.tsx).
 * ep002 renders it as a transparent overlay (2560x1440) that build.py lays over the face shot, below the face.
 */
import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig, spring, interpolate, Easing} from 'remotion';

const RED = '#E3262A';
const INK = '#141414';
const pop = (f: number, fps: number, delay = 0, damping = 11, stiffness = 170) =>
  spring({frame: f - delay, fps, config: {damping, stiffness, mass: 0.7}});
const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};

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


export const SubscribeOverlay: React.FC<{dur: number}> = ({dur}) => (
  <AbsoluteFill style={{background: 'transparent'}}>
    <div style={{position: 'absolute', inset: 0, transform: 'scale(1.3333)', transformOrigin: '0 0', width: 1920, height: 1080}}>
      <Subscribe dur={dur} x={960} y={770} />
    </div>
  </AbsoluteFill>
);
