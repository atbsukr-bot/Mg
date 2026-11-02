/**
 * Arabic Shorts style — Remotion component library.
 * Copy this file to src/style/components.tsx and the fonts from
 * assets/fonts/ to public/fonts/ of the Remotion project.
 *
 * Canvas: 1080 x 1920, 30 fps. All sizes below are in that canvas.
 * Requires: remotion, @remotion/fonts (same version as remotion).
 */
import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Easing,
  Img,
  OffthreadVideo,
  Sequence,
  interpolate,
  random,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import {loadFont} from '@remotion/fonts';

/* ------------------------------------------------------------------ */
/* 1. Design tokens                                                    */
/* ------------------------------------------------------------------ */
/* ep001 «بلاغ بلا عنوان» palette — crime-file look (see team/montage-log.md) */
export const T = {
  red: '#C8261E', // siren red: stamps, routes
  redDeep: '#F1C21B', // caption keyword box = crime-scene tape yellow
  hlText: '#0F1318', // text inside the caption keyword box
  tape: '#F1C21B', // police tape
  blue: '#1E4FD8', // police blue (siren, pins)
  ink: '#0F1318', // labels, text on paper
  paper: '#EEE6D3', // case-file paper
  paper2: '#E7DFCB', // caption strip
  line: '#BFB6A0', // inner borders, dashed paths
  bgLight: '#D8CDB4', // manila stage centre
  bgEdge: '#9F957D', // manila stage edges
  ui: '#1B2230', // dark UI
  white: '#FFFFFF',
  head: 'Tajawal', // headlines, stamps, numbers (weight 900)
  body: 'Cairo', // captions, card sub-text (weight 700-800)
  file: 'Reem Kufi', // ep001 secondary face: case-file labels
  shadow: '0 10px 0 rgba(0,0,0,.16), 0 18px 40px rgba(0,0,0,.22)',
};

loadFont({family: 'Tajawal', url: staticFile('fonts/Tajawal-Black.ttf'), weight: '900'});
loadFont({family: 'Tajawal', url: staticFile('fonts/Tajawal-Bold.ttf'), weight: '700'});
loadFont({family: 'Cairo', url: staticFile('fonts/Cairo.ttf'), weight: '200 1000'});
loadFont({family: 'Reem Kufi', url: staticFile('fonts/ReemKufi-Bold.ttf'), weight: '700'});

/* ------------------------------------------------------------------ */
/* 2. Motion helpers                                                   */
/* ------------------------------------------------------------------ */
/** Snappy pop with a little overshoot — the default entrance for everything. */
export const usePop = (delay = 0, damping = 11) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return spring({frame: f - delay, fps, config: {damping, stiffness: 190, mass: 0.6}});
};

/** 0→1 over n frames starting at `at`, clamped. */
export const ramp = (f: number, at: number, n: number, ease = Easing.out(Easing.cubic)) =>
  interpolate(f, [at, at + n], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: ease});

/** Deterministic torn-paper polygon for label edges. */
const torn = (seed: string, teeth = 14, depth = 3) => {
  const top: string[] = [];
  const bottom: string[] = [];
  for (let i = 0; i <= teeth; i++) {
    const x = (i / teeth) * 100;
    top.push(`${x}% ${random(`${seed}t${i}`) * depth}%`);
    bottom.unshift(`${x}% ${100 - random(`${seed}b${i}`) * depth}%`);
  }
  return `polygon(${[...top, ...bottom].join(',')})`;
};

/* ------------------------------------------------------------------ */
/* 3. Backgrounds & looks                                              */
/* ------------------------------------------------------------------ */
export const Grain: React.FC<{opacity?: number}> = ({opacity = 0.16}) => {
  const f = useCurrentFrame();
  const id = `grain-${f}`;
  return (
    <AbsoluteFill style={{opacity, mixBlendMode: 'multiply', pointerEvents: 'none'}}>
      <svg width="100%" height="100%">
        <filter id={id}>
          <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={Math.floor(f / 2)} />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter={`url(#${id})`} />
      </svg>
    </AbsoluteFill>
  );
};

/** Beige paper stage used for every explainer graphic. `dark` = the moody scale/flame stage. */
export const PaperBackground: React.FC<{dark?: boolean}> = ({dark}) => (
  <AbsoluteFill
    style={{
      background: dark
        ? 'radial-gradient(ellipse at 50% 42%, #1f2a40 0%, #10151f 60%, #07090f 100%)'
        : `radial-gradient(ellipse at 50% 45%, ${T.bgLight} 0%, #CBBFA9 60%, ${T.bgEdge} 100%)`,
    }}
  >
    <Grain opacity={dark ? 0.1 : 0.2} />
  </AbsoluteFill>
);

export type Look = 'warm' | 'bw' | 'flashback' | 'dim';
const LOOK_FILTER: Record<Look, string> = {
  warm: 'saturate(1.12) contrast(1.06)',
  bw: 'grayscale(1) contrast(1.25) brightness(0.95)',
  flashback: 'sepia(0.45) saturate(0.7) contrast(0.92) brightness(1.04)',
  dim: 'brightness(0.45) saturate(0.8) blur(2px)', // B-roll behind cards
};

export type ZoomStep = {from: number; scale: number; x?: number; y?: number};

/**
 * Talking-head A-roll. Jump-cut zooms come from `zoomSteps` (hard steps, no easing),
 * plus a slow push-in across the clip.
 */
export const TalkingHead: React.FC<{
  src: string; // file in public/, e.g. 'raw/take1.mp4'
  trimBefore?: number; // frames to skip in the source
  dur: number;
  look?: Look;
  zoomSteps?: ZoomStep[];
}> = ({src, trimBefore = 0, dur, look = 'warm', zoomSteps = []}) => {
  const f = useCurrentFrame();
  const step = [...zoomSteps].reverse().find((s) => f >= s.from) ?? {scale: 1, x: 0, y: 0};
  const push = interpolate(f, [0, dur], [1, 1.04]);
  return (
    <AbsoluteFill style={{overflow: 'hidden', background: '#000'}}>
      <AbsoluteFill
        style={{
          transform: `translate(${step.x ?? 0}px, ${step.y ?? 0}px) scale(${step.scale * push})`,
          filter: LOOK_FILTER[look],
        }}
      >
        {/* muted: the voice plays from one continuous audio track in the Montage, so it never drops during graphic scenes */}
        <OffthreadVideo src={staticFile(src)} trimBefore={trimBefore} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </AbsoluteFill>
      {look === 'flashback' && <FlashbackOverlay />}
      <Vignette strength={look === 'flashback' ? 0.75 : 0.45} />
    </AbsoluteFill>
  );
};

export const Vignette: React.FC<{strength?: number}> = ({strength = 0.45}) => (
  <AbsoluteFill style={{background: `radial-gradient(ellipse at 50% 45%, transparent 45%, rgba(0,0,0,${strength}) 100%)`, pointerEvents: 'none'}} />
);

/** "Old tape" look for flashback lines ("أنا كنت كذا"). */
export const FlashbackOverlay: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Grain opacity={0.35} />
      <div style={{position: 'absolute', top: 120, left: 70, color: 'rgba(255,255,255,.85)', fontFamily: 'monospace', fontSize: 34, letterSpacing: 3}}>
        ▶ PLAY
      </div>
      <div style={{position: 'absolute', left: 0, right: 0, top: (f * 37) % 1920, height: 6, background: 'rgba(255,255,255,.06)'}} />
    </AbsoluteFill>
  );
};

/* ------------------------------------------------------------------ */
/* 4. Text systems                                                     */
/* ------------------------------------------------------------------ */
export type Word = {text: string; start: number; end: number; hl?: boolean};

/**
 * Bottom caption strip — always on screen, in every scene.
 * One chunk = 2–5 words, shown whole when the chunk starts (no empty gaps).
 * The `hl` word turns into the red box on its own start frame; each word nudges up as it is spoken.
 */
export const Caption: React.FC<{words: Word[]; y?: number}> = ({words, y = 1330}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  if (!words.length || f < words[0].start) return null;
  const inS = spring({frame: f - words[0].start, fps, config: {damping: 14, stiffness: 240}});
  return (
    <div style={{position: 'absolute', top: y, left: 0, right: 0, display: 'flex', justifyContent: 'center'}}>
      <div
        style={{
          direction: 'rtl',
          display: 'flex',
          gap: 16,
          alignItems: 'center',
          background: T.paper2,
          padding: '12px 24px',
          boxShadow: '0 6px 0 rgba(0,0,0,.18)',
          fontFamily: T.body,
          fontWeight: 800,
          fontSize: 50,
          lineHeight: 1.25,
          color: T.ink,
          transform: `scale(${0.85 + 0.15 * inS})`,
        }}
      >
        {words.map((w, i) => {
          const s = spring({frame: f - w.start, fps, config: {damping: 13, stiffness: 260}});
          return (
            <span
              key={i}
              style={{
                display: 'inline-block',
                transform: `translateY(${f >= w.start ? -(1 - s) * 8 : 0}px)`,
                background: w.hl && f >= w.start ? T.redDeep : 'transparent',
                color: w.hl && f >= w.start ? T.hlText : T.ink,
                padding: w.hl ? '0 12px' : 0,
              }}
            >
              {w.text}
            </span>
          );
        })}
      </div>
    </div>
  );
};

export type HeadlineVariant = 'ink' | 'stamp' | 'plain' | 'giant' | 'paper';

/**
 * The big mid-frame word(s). Variants seen in the reference:
 *  ink   — white text on torn black label ("كل يوم")
 *  stamp — red text, paper fill, thick red border, tilted ("بكرة", "اليوم")
 *  plain — white bold text with heavy shadow, straight on the video ("إنك تعرف")
 *  paper — black text on paper card ("أنا كنت كذا")
 *  giant — 230px red word across the top, behind/over the head ("المشكلة")
 */
export const Headline: React.FC<{
  text: string;
  variant?: HeadlineVariant;
  x?: number; // centre x
  y?: number; // centre y
  rotate?: number;
  size?: number;
  delay?: number;
  exitAt?: number; // frame (relative) to pop out
}> = ({text, variant = 'ink', x = 540, y = 760, rotate, size, delay = 0, exitAt}) => {
  const f = useCurrentFrame();
  const s = usePop(delay);
  const out = exitAt !== undefined ? ramp(f, exitAt, 5, Easing.in(Easing.cubic)) : 0;
  const rot = rotate ?? ({ink: -2, stamp: -6, plain: 0, giant: 0, paper: 2} as const)[variant];
  const fs = size ?? ({ink: 92, stamp: 96, plain: 84, giant: 230, paper: 80} as const)[variant];
  if (f < delay) return null;
  const base: React.CSSProperties = {
    position: 'absolute',
    left: x,
    top: y,
    transform: `translate(-50%,-50%) rotate(${rot + (1 - s) * -8}deg) scale(${(0.5 + 0.5 * s) * (1 - out)})`,
    opacity: Math.min(1, s * 1.5) * (1 - out),
    fontFamily: T.head,
    fontWeight: 900,
    fontSize: fs,
    lineHeight: 1.15,
    direction: 'rtl',
    whiteSpace: 'nowrap',
  };
  const styles: Record<HeadlineVariant, React.CSSProperties> = {
    ink: {background: T.ink, color: T.white, padding: '18px 44px 26px', clipPath: torn(text), boxShadow: T.shadow},
    stamp: {background: T.paper, color: T.red, padding: '6px 34px 14px', border: `8px solid ${T.red}`, borderRadius: 10, boxShadow: T.shadow},
    plain: {color: T.white, textShadow: '0 6px 0 rgba(0,0,0,.35), 0 0 30px rgba(0,0,0,.5)'},
    paper: {background: T.paper, color: T.ink, padding: '10px 40px 18px', boxShadow: T.shadow},
    giant: {color: T.red, letterSpacing: -4, textShadow: '0 8px 30px rgba(0,0,0,.35)'},
  };
  return <div style={{...base, ...styles[variant]}}>{text}</div>;
};

/** Small tilted label that sticks to a card corner ("اليوم", "بعده", "شكله أحسن"). */
export const Tag: React.FC<{text: string; x: number; y: number; rotate?: number; delay?: number; size?: number; filled?: boolean}> = ({
  text, x, y, rotate = -8, delay = 0, size = 48, filled,
}) => {
  const s = usePop(delay, 9);
  if (useCurrentFrame() < delay) return null;
  return (
    <div
      style={{
        position: 'absolute', left: x, top: y, direction: 'rtl', fontFamily: T.head, fontWeight: 900, fontSize: size,
        color: filled ? T.white : T.red, background: filled ? T.red : T.paper, border: `5px solid ${T.red}`,
        padding: '0 18px 6px', borderRadius: 6, boxShadow: '0 6px 0 rgba(0,0,0,.18)',
        transform: `translate(-50%,-50%) rotate(${rotate}deg) scale(${0.3 + 0.7 * s})`,
      }}
    >
      {text}
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* 5. Cards & props                                                    */
/* ------------------------------------------------------------------ */
type From = 'top' | 'bottom' | 'left' | 'right' | 'drop' | 'pop';

/** Paper card with double border and hard drop shadow. Slides/drops in on a spring. */
export const Card: React.FC<{
  x: number; y: number; w: number; h?: number; rotate?: number; from?: From; delay?: number;
  children?: React.ReactNode; dark?: boolean; framed?: boolean;
}> = ({x, y, w, h, rotate = 0, from = 'drop', delay = 0, children, dark, framed = true}) => {
  const f = useCurrentFrame();
  const s = usePop(delay, 12);
  if (f < delay) return null;
  const off = 1 - s;
  const move: Record<From, string> = {
    top: `translateY(${-700 * off}px)`, bottom: `translateY(${900 * off}px)`, left: `translateX(${-900 * off}px)`,
    right: `translateX(${900 * off}px)`, drop: `translateY(${-120 * off}px) scale(${1 + 0.25 * off})`, pop: `scale(${0.4 + 0.6 * s})`,
  };
  return (
    <div
      style={{
        position: 'absolute', left: x, top: y, width: w, height: h, direction: 'rtl',
        background: dark ? T.ui : T.paper, borderRadius: 10, boxShadow: T.shadow,
        transform: `${move[from]} rotate(${rotate}deg)`, opacity: Math.min(1, s * 2),
        padding: framed ? 14 : 0, boxSizing: 'border-box',
      }}
    >
      <div style={{width: '100%', height: '100%', border: framed && !dark ? `3px solid ${T.ink}` : 'none', outline: framed && !dark ? `2px solid ${T.line}` : 'none', outlineOffset: 6, boxSizing: 'border-box', position: 'relative'}}>
        {children}
      </div>
    </div>
  );
};

/** Big number that counts up (0 → 365 "يوم"). */
export const Counter: React.FC<{from?: number; to: number; dur: number; x: number; y: number; size?: number; label?: string; color?: string; delay?: number}> = ({
  from = 0, to, dur, x, y, size = 200, label, color = T.white, delay = 0,
}) => {
  const f = useCurrentFrame();
  if (f < delay) return null;
  const v = Math.round(interpolate(f - delay, [0, dur], [from, to], {extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)}));
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: 'translate(-50%,-50%)', textAlign: 'center', fontFamily: T.head, fontWeight: 900, color, textShadow: '0 6px 24px rgba(0,0,0,.35)'}}>
      <div style={{fontSize: size, lineHeight: 1, fontVariantNumeric: 'tabular-nums'}}>{v}</div>
      {label && <div style={{fontSize: size * 0.32, marginTop: -size * 0.05}}>{label}</div>}
    </div>
  );
};

/** Tear-off calendar: red header, counting day number. */
export const CalendarCard: React.FC<{x: number; y: number; to: number; dur: number; delay?: number; rotate?: number}> = ({x, y, to, dur, delay = 0, rotate = 4}) => {
  const f = useCurrentFrame();
  const s = usePop(delay);
  if (f < delay) return null;
  const v = Math.max(1, Math.round(interpolate(f - delay, [0, dur], [1, to], {extrapolateRight: 'clamp'})));
  return (
    <div style={{position: 'absolute', left: x, top: y, width: 250, height: 330, background: T.paper, borderRadius: 14, boxShadow: T.shadow, overflow: 'hidden', transform: `rotate(${rotate}deg) scale(${0.5 + 0.5 * s})`, fontFamily: T.head, textAlign: 'center'}}>
      <div style={{height: 70, background: T.red}} />
      <div style={{fontSize: 130, fontWeight: 900, color: T.ink, lineHeight: 1.3}}>{v}</div>
      <div style={{fontSize: 44, fontWeight: 700, color: T.ink, marginTop: -20}}>يوم</div>
    </div>
  );
};

/** Mini video-player card (dark top with red play button). */
export const PlayerCard: React.FC<{x: number; y: number; w?: number; delay?: number; rotate?: number; title?: string}> = ({x, y, w = 620, delay = 0, rotate = -3, title}) => (
  <Card x={x} y={y} w={w} h={w * 0.66} rotate={rotate} from="left" delay={delay} framed={false}>
    <div style={{height: '68%', background: T.ui, borderRadius: '10px 10px 0 0', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
      <div style={{width: 170, height: 120, background: T.red, borderRadius: 30, display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <div style={{width: 0, height: 0, borderTop: '28px solid transparent', borderBottom: '28px solid transparent', borderLeft: `46px solid ${T.white}`, marginLeft: 10}} />
      </div>
    </div>
    <div style={{padding: '16px 28px', fontFamily: T.head, fontWeight: 900, fontSize: 44, color: T.ink}}>{title}</div>
    <div style={{position: 'absolute', bottom: 30, left: 40, right: 40, height: 12, borderRadius: 6, background: T.line}} />
  </Card>
);

/** Labelled progress bar ("شي جديد 38%"). */
export const ProgressBar: React.FC<{label: string; value: number; x: number; y: number; w?: number; delay?: number; drainAt?: number; active?: boolean}> = ({
  label, value, x, y, w = 760, delay = 0, drainAt, active,
}) => {
  const f = useCurrentFrame();
  const s = usePop(delay);
  if (f < delay) return null;
  const fill = interpolate(f - delay, [6, 30], [0, value], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  const drained = drainAt !== undefined ? fill * (1 - ramp(f, drainAt, 10)) : fill;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: w, transform: `scale(${0.6 + 0.4 * s})`, opacity: s, background: T.paper, borderRadius: 18, padding: '18px 30px 26px', boxShadow: T.shadow, border: active ? `5px solid ${T.red}` : 'none', direction: 'rtl', fontFamily: T.head}}>
      <div style={{display: 'flex', justifyContent: 'space-between', fontWeight: 900, fontSize: 46, color: T.ink}}>
        <span>{label}</span>
        <span style={{fontFamily: 'monospace', fontSize: 34, color: active ? T.red : T.ink, direction: 'ltr'}}>{Math.round(drained)}%</span>
      </div>
      <div style={{marginTop: 12, height: 22, background: T.line, borderRadius: 11, overflow: 'hidden', direction: 'ltr'}}>
        <div style={{width: `${drained}%`, height: '100%', background: active ? T.red : T.ink, borderRadius: 11}} />
      </div>
    </div>
  );
};

/** Label explosion — a cloud of small tags flying out from the centre ("كورس، ورشة، تطبيق…"). */
export const WordBurst: React.FC<{words: string[]; cx?: number; cy?: number; radius?: number; delay?: number}> = ({words, cx = 540, cy = 420, radius = 380, delay = 0}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <>
      {words.map((w, i) => {
        const d = delay + i * 1;
        if (f < d) return null;
        const s = spring({frame: f - d, fps, config: {damping: 14, stiffness: 160}});
        const a = random(`a${i}`) * Math.PI * 2;
        const r = radius * (0.45 + 0.55 * random(`r${i}`));
        const kind = i % 3;
        return (
          <div key={i} style={{
            position: 'absolute', left: cx + Math.cos(a) * r * s, top: cy + Math.sin(a) * r * 0.6 * s, direction: 'rtl',
            transform: `translate(-50%,-50%) rotate(${(random(`t${i}`) - 0.5) * 30}deg) scale(${s})`,
            fontFamily: T.head, fontWeight: 900, fontSize: 40, padding: '2px 16px 8px',
            background: kind === 0 ? T.ink : kind === 1 ? T.paper : T.red, color: kind === 1 ? T.ink : T.white, boxShadow: '0 4px 0 rgba(0,0,0,.25)',
          }}>{w}</div>
        );
      })}
    </>
  );
};

/** DM / chat mock-up card (name, online status, red message bubble, typing dots). */
export const ChatCard: React.FC<{name: string; avatar?: string; messages: {text: string; at: number; me?: boolean}[]; x?: number; y?: number; delay?: number}> = ({
  name, avatar, messages, x = 90, y = 700, delay = 0,
}) => {
  const f = useCurrentFrame();
  const s = usePop(delay, 13);
  if (f < delay) return null;
  return (
    <div style={{position: 'absolute', left: x, top: y, width: 900, background: T.white, borderRadius: 26, boxShadow: T.shadow, padding: 30, direction: 'rtl', fontFamily: T.body, transform: `translateY(${(1 - s) * 300}px)`, opacity: s}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 18, borderBottom: `2px solid ${T.line}`, paddingBottom: 18}}>
        <div style={{width: 80, height: 80, borderRadius: 40, background: T.line, overflow: 'hidden'}}>{avatar && <Img src={staticFile(avatar)} style={{width: '100%', height: '100%', objectFit: 'cover'}} />}</div>
        <div>
          <div style={{fontWeight: 900, fontSize: 40, color: T.ink}}>{name}</div>
          <div style={{fontSize: 26, color: '#2f9e44'}}>متصل الآن</div>
        </div>
      </div>
      {messages.filter((m) => f >= m.at).map((m, i) => {
        const ms = spring({frame: f - m.at, fps: 30, config: {damping: 12, stiffness: 220}});
        return (
          <div key={i} style={{display: 'flex', justifyContent: m.me ? 'flex-start' : 'flex-end', marginTop: 22}}>
            <div style={{maxWidth: 640, padding: '14px 26px', borderRadius: 24, fontSize: 36, fontWeight: 800, background: m.me ? T.red : '#EEE9DF', color: m.me ? T.white : T.ink, transform: `scale(${ms})`, transformOrigin: m.me ? 'right' : 'left'}}>{m.text}</div>
          </div>
        );
      })}
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* 6. Diagram scenes (SVG)                                             */
/* ------------------------------------------------------------------ */
/** Many grey dashed routes fanning out + one red route drawn to a flag ("طريق واحد"). */
export const PathsScene: React.FC<{delay?: number; crossAt?: number}> = ({delay = 0, crossAt}) => {
  const f = useCurrentFrame() - delay;
  const ox = 540, oy = 1180;
  const greys = [-420, -320, -230, -150, 150, 230, 320, 420].map((dx, i) => `M${ox},${oy} C${ox + dx * 0.2},${oy - 200} ${ox + dx * 0.9},${oy - 350 - i * 25} ${ox + dx},${oy - 650 - (i % 3) * 90}`);
  const draw = ramp(f, 8, 22);
  return (
    <AbsoluteFill>
      <svg width={1080} height={1920}>
        {greys.map((d, i) => (
          <path key={i} d={d} fill="none" stroke="#9c958a" strokeWidth={7} strokeDasharray="22 16" opacity={ramp(f, i, 8)} />
        ))}
        <path d={`M${ox},${oy} L${ox},${oy - 880}`} fill="none" stroke={T.red} strokeWidth={22} strokeLinecap="round" strokeDasharray={900} strokeDashoffset={900 * (1 - draw)} />
        <circle cx={ox} cy={oy + 10} r={26} fill={T.ink} />
        <rect x={ox - 30} y={oy + 46} width={60} height={34} rx={14} fill={T.ink} />
        {draw > 0.95 && <path d={`M${ox},${oy - 880} l0,-60 l70,20 l-70,22`} fill={T.red} stroke={T.ink} strokeWidth={6} />}
        {crossAt !== undefined && greys.map((_, i) => {
          const c = ramp(f, crossAt + i * 2, 5);
          const px = ox + [-420, -320, -230, -150, 150, 230, 320, 420][i] * 0.75, py = oy - 520 - (i % 3) * 60;
          return <g key={i} opacity={c} transform={`translate(${px},${py}) scale(${c})`}><path d="M-28,-28 L28,28 M28,-28 L-28,28" stroke={T.red} strokeWidth={12} strokeLinecap="round" /></g>;
        })}
      </svg>
    </AbsoluteFill>
  );
};

/** Balance scale; `tilt` in degrees (positive = right pan down). */
export const BalanceScene: React.FC<{left: string; right: string; tilt: number; tiltAt?: number}> = ({left, right, tilt, tiltAt = 0}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = spring({frame: f - tiltAt, fps, config: {damping: 7, stiffness: 90}}) * tilt;
  const cx = 540, cy = 700, arm = 360;
  const rad = (t * Math.PI) / 180;
  const pan = (side: -1 | 1, label: string) => {
    const px = cx + side * arm * Math.cos(rad), py = cy + side * arm * Math.sin(rad);
    return (
      <g>
        <line x1={px} y1={py} x2={px - 110} y2={py + 220} stroke="#bbb" strokeWidth={3} />
        <line x1={px} y1={py} x2={px + 110} y2={py + 220} stroke="#bbb" strokeWidth={3} />
        <path d={`M${px - 140},${py + 220} Q${px},${py + 300} ${px + 140},${py + 220} Z`} fill={side > 0 ? T.red : '#d8d2c6'} />
        <text x={px} y={py + 200} textAnchor="middle" fontFamily={T.head} fontWeight={900} fontSize={54} fill={T.white} style={{direction: 'rtl'}}>{label}</text>
      </g>
    );
  };
  return (
    <AbsoluteFill>
      <svg width={1080} height={1920}>
        <path d={`M${cx - 40},${cy} L${cx - 90},${cy + 620} L${cx + 90},${cy + 620} L${cx + 40},${cy} Z`} fill="#efe9de" />
        <rect x={cx - 200} y={cy + 610} width={400} height={40} rx={10} fill="#efe9de" />
        <line x1={cx - arm * Math.cos(rad)} y1={cy - arm * Math.sin(rad)} x2={cx + arm * Math.cos(rad)} y2={cy + arm * Math.sin(rad)} stroke="#f4efe6" strokeWidth={24} strokeLinecap="round" />
        <circle cx={cx} cy={cy} r={22} fill={T.red} />
        {pan(-1, left)}
        {pan(1, right)}
      </svg>
    </AbsoluteFill>
  );
};

/** Red X drawn in two strokes (for "لازم تبعد عنها"). */
export const XMark: React.FC<{x: number; y: number; size?: number; delay?: number}> = ({x, y, size = 140, delay = 0}) => {
  const f = useCurrentFrame();
  const a = ramp(f, delay, 4), b = ramp(f, delay + 3, 4);
  const L = size * 1.42;
  return (
    <svg style={{position: 'absolute', left: x - size / 2, top: y - size / 2, overflow: 'visible'}} width={size} height={size}>
      <line x1={0} y1={0} x2={size} y2={size} stroke={T.red} strokeWidth={size * 0.14} strokeLinecap="round" strokeDasharray={L} strokeDashoffset={L * (1 - a)} />
      <line x1={size} y1={0} x2={0} y2={size} stroke={T.red} strokeWidth={size * 0.14} strokeLinecap="round" strokeDasharray={L} strokeDashoffset={L * (1 - b)} />
    </svg>
  );
};

/** Hazard tape that slides across the frame with repeating text. */
export const WarningTape: React.FC<{text: string; y: number; rotate?: number; delay?: number}> = ({text, y, rotate = -12, delay = 0}) => {
  const f = useCurrentFrame();
  const p = ramp(f, delay, 8);
  if (f < delay) return null;
  return (
    <div style={{position: 'absolute', left: -200, top: y, width: 1480, transform: `rotate(${rotate}deg) translateX(${(1 - p) * 1500}px)`, background: T.tape, color: T.ink, fontFamily: T.head, fontWeight: 900, fontSize: 44, padding: '6px 0 12px', whiteSpace: 'nowrap', overflow: 'hidden', borderTop: `8px solid ${T.ink}`, borderBottom: `8px solid ${T.ink}`, boxShadow: T.shadow, direction: 'rtl'}}>
      {Array(8).fill(text).join('  •  ')}
    </div>
  );
};

/* ------------------------------------------------------------------ */
/* 7. Transitions                                                      */
/* ------------------------------------------------------------------ */
const CHANNEL = {r: '1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0', g: '0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0', b: '0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0'};

/**
 * RGB-split glitch on the first `inFrames` / last `outFrames` of a scene.
 * Wrap the WHOLE scene in it. Children render 3× only during the glitch frames.
 * `bw` turns the glitch frames grey (used on "ولا ريال" negative beats).
 */
export const Glitch: React.FC<{dur: number; inFrames?: number; outFrames?: number; strength?: number; bw?: boolean; children: React.ReactNode}> = ({
  dur, inFrames = 4, outFrames = 3, strength = 26, bw, children,
}) => {
  const f = useCurrentFrame();
  const t = Math.max(f < inFrames ? 1 - f / inFrames : 0, f >= dur - outFrames ? (f - (dur - outFrames) + 1) / outFrames : 0);
  if (t <= 0) return <AbsoluteFill>{children}</AbsoluteFill>;
  const dir = random(`gd${f}`) > 0.5 ? 1 : -1;
  const dx = strength * t * dir;
  const dy = (random(`gy${f}`) - 0.5) * 18 * t;
  return (
    <AbsoluteFill style={{background: '#000', filter: bw ? 'grayscale(1) contrast(1.3)' : undefined}}>
      <svg width={0} height={0} style={{position: 'absolute'}}>
        {(['r', 'g', 'b'] as const).map((c) => (
          <filter key={c} id={`ch-${c}`}><feColorMatrix type="matrix" values={CHANNEL[c]} /></filter>
        ))}
      </svg>
      {(['r', 'g', 'b'] as const).map((c, i) => (
        <AbsoluteFill key={c} style={{filter: `url(#ch-${c})`, mixBlendMode: 'screen', transform: `translate(${(i - 1) * dx}px, ${i === 1 ? 0 : dy}px)`}}>
          {children}
        </AbsoluteFill>
      ))}
      <div style={{position: 'absolute', left: 0, right: 0, top: random(`gs${f}`) * 1700, height: 40 + 120 * t, background: 'rgba(255,255,255,.07)', transform: `translateX(${dx * 2}px)`}} />
    </AbsoluteFill>
  );
};

/** One-frame white flash + tiny zoom — use on hard cuts into a punchline. */
export const FlashCut: React.FC<{frames?: number}> = ({frames = 3}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, frames], [0.85, 0], {extrapolateRight: 'clamp'});
  return o > 0 ? <AbsoluteFill style={{background: T.white, opacity: o}} /> : null;
};

/* ------------------------------------------------------------------ */
/* 8. Sound                                                            */
/* ------------------------------------------------------------------ */
/** Sound effect at a frame. Put files in public/sfx/ (pop.mp3, whoosh.mp3, glitch.mp3, tick.mp3, ding.mp3, typing.mp3). */
export const Sfx: React.FC<{src: string; at: number; volume?: number}> = ({src, at, volume = 0.55}) => (
  <Sequence from={at} layout="none">
    <Audio src={staticFile(src)} volume={volume} />
  </Sequence>
);
