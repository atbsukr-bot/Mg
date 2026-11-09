// ep003 «عبّارة السلام 98» — 10 s look test: paper cut-out collage (owner reference, 9 Nov 2026)
// Palette (ep003 only): sea navy, paper, fire orange, ink, card white. Accent = fire orange (not red).
import React from 'react';
import {AbsoluteFill, Easing, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {loadFont} from '@remotion/fonts';

loadFont({family: 'Cairo', url: staticFile('fonts/Cairo.ttf'), weight: '400 900'});

const C = {sea: '#0E2A47', paper: '#E6DCC8', fire: '#D9541E', ink: '#111111', card: '#F7F3EA'};
const F = 'Cairo';

const pop = (f: number, fps: number, at: number) => spring({frame: f - at, fps, config: {damping: 13, stiffness: 180, mass: 0.6}});

// paper grain + soft vignette over a flat colour
const Ground: React.FC<{bg: string}> = ({bg}) => (
  <AbsoluteFill style={{background: bg}}>
    <svg width="100%" height="100%" style={{position: 'absolute', opacity: 0.18, mixBlendMode: 'multiply'}}>
      <filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="7" /><feColorMatrix type="saturate" values="0" /></filter>
      <rect width="100%" height="100%" filter="url(#g)" />
    </svg>
    <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,.28) 100%)'}} />
  </AbsoluteFill>
);

// black sticker label (headline)
const Label: React.FC<{text: string; at: number; x: number; y: number; size?: number; rot?: number; bg?: string; fg?: string}> =
  ({text, at, x, y, size = 64, rot = -2, bg = C.ink, fg = C.card}) => {
    const f = useCurrentFrame(); const {fps} = useVideoConfig(); const s = pop(f, fps, at);
    return (
      <div style={{position: 'absolute', right: x, top: y, transform: `rotate(${rot}deg) scale(${s})`, transformOrigin: 'right center',
        background: bg, color: fg, fontFamily: F, fontWeight: 900, fontSize: size, padding: '6px 26px 14px', direction: 'rtl',
        boxShadow: '6px 8px 0 rgba(0,0,0,.25)', whiteSpace: 'nowrap', opacity: s > 0.02 ? 1 : 0}}>{text}</div>
    );
  };

// caption strip under the chin zone: white box, keyword on the accent colour
const Caption: React.FC<{pre: string; key_: string; post?: string; at: number}> = ({pre, key_, post = '', at}) => {
  const f = useCurrentFrame(); const o = interpolate(f, [at, at + 6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', bottom: 70, left: 0, right: 0, display: 'flex', justifyContent: 'center', opacity: o}}>
      <div style={{background: C.card, color: C.ink, fontFamily: F, fontWeight: 700, fontSize: 40, padding: '4px 22px 10px', direction: 'rtl', boxShadow: '4px 5px 0 rgba(0,0,0,.25)'}}>
        {pre} <span style={{background: C.fire, color: C.card, padding: '0 10px'}}>{key_}</span> {post}
      </div>
    </div>
  );
};

const Card: React.FC<{src: string; at: number; x: number; y: number; w: number; rot: number}> = ({src, at, x, y, w, rot}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const s = pop(f, fps, at);
  const drift = interpolate(f, [at, at + 100], [0, -14]);
  return <Img src={staticFile(src)} style={{position: 'absolute', left: x, top: y + drift, width: w,
    transform: `translateY(${(1 - s) * 260}px) rotate(${rot + (1 - s) * 8}deg)`}} />;
};

const BigNum: React.FC<{n: number; at: number; x: number; y: number; suffix?: string}> = ({n, at, x, y, suffix = ''}) => {
  const f = useCurrentFrame(); const {fps} = useVideoConfig(); const s = pop(f, fps, at);
  const v = Math.round(interpolate(f, [at, at + 24], [0, n], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)}));
  return <div style={{position: 'absolute', right: x, top: y, fontFamily: F, fontWeight: 900, fontSize: 230, lineHeight: 1, color: C.fire,
    transform: `scale(${s})`, transformOrigin: 'right top', textShadow: '8px 10px 0 rgba(0,0,0,.3)', direction: 'ltr'}}>{v.toLocaleString('en-US')}{suffix}</div>;
};

// 1) the ship and the number of people on board
const S1: React.FC = () => (
  <AbsoluteFill>
    <Ground bg={C.sea} />
    <Card src="ship.png" at={2} x={90} y={170} w={1000} rot={-3} />
    <Label text="ضبا ← سفاجا" at={14} x={110} y={150} size={58} />
    <BigNum n={1418} at={26} x={120} y={330} />
    <Label text="إنسان على السفينة" at={44} x={120} y={600} size={60} bg={C.card} fg={C.ink} rot={1.5} />
    <Caption pre="ألف وأربعمية وثمانطعش" key_="إنسان" at={30} />
  </AbsoluteFill>
);

// 2) route map redrawn by us: Duba → Safaga, fire at 28 NM, sinking at 41 NM
const S2: React.FC = () => {
  const f = useCurrentFrame();
  const duba = [1380, 360], safaga = [520, 700];
  const p = (t: number) => [duba[0] + (safaga[0] - duba[0]) * t, duba[1] + (safaga[1] - duba[1]) * t];
  const L = Math.hypot(safaga[0] - duba[0], safaga[1] - duba[1]);
  const draw = interpolate(f, [8, 50], [0, 41 / 98], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic)});
  const fire = p(28 / 98), sink = p(41 / 98);
  const fireO = interpolate(f, [30, 36], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const sinkS = spring({frame: f - 52, fps: 30, config: {damping: 10, stiffness: 200}});
  return (
    <AbsoluteFill>
      <Ground bg={C.paper} />
      <svg width={1920} height={1080} style={{position: 'absolute'}}>
        <path d="M1560,0 C1470,180 1400,300 1395,380 C1390,520 1500,760 1620,1080 L1920,1080 L1920,0 Z" fill="#CDBF9F" />
        <path d="M0,0 L330,0 C420,260 470,520 505,700 C530,840 600,960 640,1080 L0,1080 Z" fill="#CDBF9F" />
        <text x={960} y={1000} textAnchor="middle" fontFamily="Cairo" fontWeight={700} fontSize={34} fill="#8C7D60">البحر الأحمر</text>
        <line x1={duba[0]} y1={duba[1]} x2={safaga[0]} y2={safaga[1]} stroke={C.ink} strokeOpacity={0.25} strokeWidth={5} strokeDasharray="4 16" strokeLinecap="round" />
        <line x1={duba[0]} y1={duba[1]} x2={safaga[0]} y2={safaga[1]} stroke={C.ink} strokeWidth={7} strokeDasharray={`${L * draw} ${L}`} strokeLinecap="round" />
        {[duba, safaga].map(([x, y], i) => <circle key={i} cx={x} cy={y} r={16} fill={C.ink} />)}
        <circle cx={fire[0]} cy={fire[1]} r={26 + 6 * Math.sin(f / 4)} fill={C.fire} opacity={fireO * 0.9} />
        <g transform={`translate(${sink[0]},${sink[1]}) scale(${sinkS}) rotate(45)`}>
          <rect x={-40} y={-9} width={80} height={18} fill={C.fire} /><rect x={-9} y={-40} width={18} height={80} fill={C.fire} />
        </g>
      </svg>
      <div style={{position: 'absolute', left: duba[0] + 30, top: duba[1] - 40, fontFamily: F, fontWeight: 900, fontSize: 52, color: C.ink}}>ضبا</div>
      <div style={{position: 'absolute', left: safaga[0] - 210, top: safaga[1] - 40, fontFamily: F, fontWeight: 900, fontSize: 52, color: C.ink}}>سفاجا</div>
      <Label text="مكان الغرق" at={56} x={1920 - sink[0] - 40} y={sink[1] + 70} size={54} rot={2} />
      <div style={{position: 'absolute', left: 110, top: 110}}>
        <div style={{position: 'relative', width: 700, height: 300}}><BigNum n={41} at={58} x={250} y={0} /></div>
        <Label text="ميل بحري من ضبا" at={70} x={190} y={250} size={50} bg={C.card} fg={C.ink} rot={-1.5} />
      </div>
      <Caption pre="غرقت على بعد" key_="41 ميل بحري" post="من ضبا" at={56} />
    </AbsoluteFill>
  );
};

// 3) the captain's reply, and the claim the report does not support (struck through)
const S3: React.FC = () => {
  const f = useCurrentFrame();
  const strike = interpolate(f, [58, 72], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  return (
    <AbsoluteFill>
      <Ground bg="#3A1A10" />
      <AbsoluteFill style={{background: `radial-gradient(ellipse at 25% 60%, ${C.fire}66 0%, transparent 60%)`}} />
      <Card src="ir.png" at={2} x={120} y={260} w={760} rot={3} />
      <Label text="«لا تزعجونا… خلونا نشتغل»" at={14} x={110} y={200} size={70} />
      <Label text="رد غرفة القيادة على الراكب — 10:16 م" at={28} x={110} y={330} size={40} bg={C.card} fg={C.ink} rot={1} />
      <div style={{position: 'absolute', right: 110, top: 560, transform: 'rotate(-1.5deg)'}}>
        <div style={{position: 'relative', background: C.card, color: C.ink, fontFamily: F, fontWeight: 700, fontSize: 52, padding: '6px 26px 14px', direction: 'rtl',
          opacity: interpolate(f, [40, 46], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})}}>
          «الشركة أمرت القبطان يكمّل»
          <div style={{position: 'absolute', right: 14, top: '52%', height: 10, width: `calc(${strike * 100}% - 28px)`, background: C.fire, transform: 'rotate(-2deg)'}} />
        </div>
      </div>
      <Label text="التقرير الرسمي ما يثبتها" at={76} x={150} y={680} size={50} bg={C.fire} fg={C.card} rot={-3} />
      <Caption pre="رد القبطان على" key_="الراكب" at={14} />
    </AbsoluteFill>
  );
};

export const Test: React.FC = () => {
  const f = useCurrentFrame();
  // quick paper slide between scenes
  const wipe = (at: number) => interpolate(f, [at - 6, at, at + 6], [1920, 0, -1920], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{background: C.ink}}>
      <Sequence durationInFrames={100}><S1 /></Sequence>
      <Sequence from={100} durationInFrames={100}><S2 /></Sequence>
      <Sequence from={200} durationInFrames={100}><S3 /></Sequence>
      {[100, 200].map(at => <AbsoluteFill key={at} style={{background: C.paper, transform: `translateX(${wipe(at)}px)`, boxShadow: '0 0 40px rgba(0,0,0,.5)'}} />)}
    </AbsoluteFill>
  );
};
