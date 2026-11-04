import React from 'react';
import {AbsoluteFill, Img, Sequence, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring, Easing, random} from 'remotion';
import {PaperBg, PaperTag, PaperList, PersonCard, VocabCard, TapedPhoto, DateStamp} from './Paper';
import {Caption, Keyword, Sparks, BeatWord, ImageCard} from './Graphics';
import {ChordsPanel, StringNames, TabSheet, ChordDiagram} from './Guitar';
import {RawCard, PromptBox, EditorUI, Checklist, PhoneClip, WideCard, Badge, Counter, NotesList, SkillFile, Branch, Notice, RefCard} from './Promo';

const RED = '#E3262A';
export type ShortSeg = {a: number; len: number; cx: number; cy: number; kind: string};
export type ShortSpec = {duration: number; title: string; title2?: string; segs: ShortSeg[]; captions: {from: number; to: number; words: string[]; hl: number}[]; items: any[]};

const W = 1080, H = 1920;
const REG: Record<string, React.FC<any>> = {paperBg: PaperBg, paperTag: PaperTag, paperList: PaperList, person: PersonCard, vocab: VocabCard, taped: TapedPhoto, date: DateStamp, keyword: Keyword, sparks: Sparks, beat: BeatWord, image: ImageCard, chords: ChordsPanel, strings: StringNames, tab: TabSheet,
  raw: RawCard, prompt: PromptBox, editor: EditorUI, checklist: Checklist, phone: PhoneClip, wide: WideCard, badge: Badge, counter: Counter, notes: NotesList, skill: SkillFile, branch: Branch, notice: Notice, ref: RefCard};

export const Short: React.FC<{spec: ShortSpec}> = ({spec}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  // which segment
  let acc = 0, seg = spec.segs[0], local = 0, si = 0;
  for (let i = 0; i < spec.segs.length; i++) {
    const s = spec.segs[i];
    if (f < acc + s.len) { seg = s; local = f - acc; si = i; break; }
    acc += s.len; seg = s; local = s.len - 1; si = i;
  }
  const src = staticFile(`frames/${String(seg.a + local).padStart(5, '0')}.jpg`);
  // camera: fill height, centre on subject, alternate punch every ~3 s, handheld drift
  const base = H / 1080; // 1.778
  const step = Math.floor(local / 90);
  const BIGT = ['raw', 'checklist', 'phone', 'wide', 'ref', 'prompt', 'editor', 'notes', 'skill', 'branch', 'notice'];
  const cardOn = spec.items.some((it: any) => BIGT.includes(it.type) && f >= it.from - 6 && f < it.from + it.dur + 4);
  const z = cardOn ? 1.0 : (seg.kind === 'wide' ? 1.12 : 1.0) * ([1.0, 1.1, 1.04, 1.16][(step + si) % 4]); // pull back under cards so they never sit on his face
  let punch = 0, bw = false, glitch = 0, shake = 0, flash = 0;
  for (const it of spec.items) {
    if (f < it.from || f >= it.from + it.dur) continue;
    const p = f - it.from;
    if (it.type === 'punch') punch += (it.amt ?? 0.06) * Math.exp(-p / (it.tau ?? 5)) * (p < 2 ? p / 2 : 1);
    if (it.type === 'bw') bw = true;
    if (it.type === 'glitch') glitch = 1 - p / it.dur;
    if (it.type === 'shake') shake = (it.amp ?? 14) * (1 - p / it.dur) ** 2;
    if (it.type === 'flash') flash = interpolate(p, [0, 2, it.dur], [0, 0.9, 0], {extrapolateRight: 'clamp'});
  }
  // segment joins: quick zoom-blur in
  const join = si > 0 && local < 6 ? 1 - local / 6 : 0;
  const s = base * z * (1 + punch + join * 0.15);
  const imgW = 1920 * s, imgH = 1080 * s;
  let left = W / 2 - seg.cx * imgW, top = H / 2 - seg.cy * imgH;
  left = Math.min(0, Math.max(W - imgW, left)); top = Math.min(0, Math.max(H - imgH, top));
  left += Math.sin(f / 47) * 6 + (random(`sx${f}`) - 0.5) * 2 * shake;
  top += Math.cos(f / 61) * 5 + (random(`sy${f}`) - 0.5) * 2 * shake;
  const filt = (bw ? 'grayscale(1) contrast(1.35) ' : 'saturate(1.08) contrast(1.04) ') + (join > 0 ? `blur(${join * 10}px)` : '');
  const imgStyle: React.CSSProperties = {position: 'absolute', left, top, width: imgW, height: imgH, filter: filt};

  const hook = spring({frame: f, fps, config: {damping: 9, stiffness: 200, mass: 0.7}});
  const hookOut = interpolate(f, [70, 80], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const barIn = spring({frame: f - 72, fps, config: {damping: 14}});
  const end = spec.duration;
  const subIn = spring({frame: f - (end - 75), fps, config: {damping: 9, stiffness: 200}});
  return (
    <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
      <Img src={src} style={imgStyle} />
      {glitch > 0 && (
        <>
          <Img src={src} style={{...imgStyle, left: left - 22 * glitch, mixBlendMode: 'screen', opacity: 0.38, filter: 'sepia(1) saturate(8) hue-rotate(-50deg)'}} />
          <Img src={src} style={{...imgStyle, left: left + 22 * glitch, mixBlendMode: 'screen', opacity: 0.3, filter: 'sepia(1) saturate(8) hue-rotate(160deg)'}} />
        </>
      )}
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0.55) 0%, rgba(0,0,0,0) 22%, rgba(0,0,0,0) 62%, rgba(0,0,0,0.6) 100%)'}} />

      {spec.items.filter((it) => REG[it.type]).map((it, i) => {
        const C = REG[it.type];
        return <Sequence key={i} from={it.from} durationInFrames={it.dur} layout="none"><C {...it} /></Sequence>;
      })}

      {/* captions: lower third of the screen */}
      <div style={{position: 'absolute', left: 0, top: 0, width: W, height: 1500}}>
        {f >= 80 && spec.captions.map((c, i) => (
          <Sequence key={'c' + i} from={c.from} durationInFrames={c.to - c.from} layout="none"><Caption words={c.words} hl={c.hl} /></Sequence>
        ))}
      </div>

      {/* hook headline (first 2.5 s) then a persistent title bar */}
      {f < 82 && (
        <>
          <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0, transform: `scale(${hook * hookOut})`, transformOrigin: '540px 1180px'}}>
            <path d={burst(540, 1180, 300, 420, 18, f / 30)} fill="#141414" transform="translate(12 16)" />
            <path d={burst(540, 1180, 300, 420, 18, f / 30)} fill="#FFD23F" stroke="#141414" strokeWidth={12} strokeLinejoin="round" />
            <path d={burst(540, 1180, 270, 360, 18, f / 30)} fill="#FF8A1F" opacity={0.35} />
          </svg>
          <div style={{position: 'absolute', left: W / 2, top: 1180, width: 960, transform: `translate(-50%,-50%) rotate(-5deg) scale(${(0.3 + 0.7 * hook) * hookOut})`, textAlign: 'center', direction: 'rtl'}}>
            <div style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: spec.title.length > 16 ? 96 : 116, lineHeight: 1.1, color: '#ffffff', WebkitTextStroke: '14px #141414', paintOrder: 'stroke fill', textShadow: '6px 12px 0 #141414', textWrap: 'balance' as any}}>{spec.title}</div>
            {spec.title2 && <div style={{display: 'inline-block', marginTop: 18, background: RED, color: '#fff', fontFamily: 'Tajawal', fontWeight: 900, fontSize: 60, padding: '8px 30px 0', borderRadius: 18, border: '7px solid #141414', boxShadow: '8px 10px 0 #141414', whiteSpace: 'nowrap', transform: 'rotate(3deg)'}}>{spec.title2}</div>}
          </div>
        </>
      )}
      {f >= 72 && (
        <div style={{position: 'absolute', left: 0, right: 0, top: 150, display: 'flex', justifyContent: 'center', transform: `translateY(${(1 - barIn) * -200}px)`}}>
          <div style={{background: '#141414', color: '#fff', fontFamily: 'Tajawal', fontWeight: 900, fontSize: 58, padding: '10px 34px 2px', borderRadius: 20, borderBottom: `8px solid ${RED}`, direction: 'rtl', maxWidth: 920, textAlign: 'center', boxShadow: '0 12px 30px rgba(0,0,0,0.45)'}}>{spec.title}</div>
        </div>
      )}
      {/* channel logo */}
      <Img src={staticFile('logo.png')} style={{position: 'absolute', right: 40, top: 300, width: 130, height: 130, transform: `rotate(${Math.sin(f / 38) * 5}deg)`, filter: 'drop-shadow(0 6px 14px rgba(0,0,0,0.55))'}} />
      {/* subscribe nudge at the end */}
      {f >= end - 75 && (
        <div style={{position: 'absolute', left: W / 2, top: 1640, transform: `translate(-50%,-50%) scale(${subIn})`, display: 'flex', alignItems: 'center', gap: 16, background: RED, borderRadius: 60, padding: '14px 40px 10px', boxShadow: `0 0 ${30 + 20 * Math.sin(f / 4)}px rgba(227,38,42,0.8)`}}>
          <Img src={staticFile('logo.png')} style={{width: 76, height: 76}} />
          <span style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 54, color: '#fff', direction: 'rtl', whiteSpace: 'nowrap'}}>اشترك عشان تشوف تطوري</span>
        </div>
      )}
      <div style={{position: 'absolute', left: 0, top: 0, height: 10, width: (W * f) / end, background: `linear-gradient(90deg, ${RED}, #FFD23F)`, boxShadow: '0 0 14px rgba(227,38,42,0.8)'}} />
      <AbsoluteFill style={{background: '#fff', opacity: flash, pointerEvents: 'none'}} />
    </AbsoluteFill>
  );
};

// ---------- THUMBNAIL ----------
export const Thumb: React.FC<{frame: number; cx?: number; arrow?: boolean}> = ({frame, cx = 0.42, arrow = false}) => {
  const src = staticFile(`frames/${String(frame).padStart(5, '0')}.jpg`);
  const s = 1.3, iw = 1280 * s, ih = 720 * s;
  const left = Math.min(0, Math.max(1280 - iw, 1280 * 0.33 - cx * iw));
  return (
    <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
      <Img src={src} style={{position: 'absolute', left, top: -ih * 0.1, width: iw, height: ih, filter: 'saturate(1.25) contrast(1.12) brightness(1.04)'}} />
      <AbsoluteFill style={{background: 'linear-gradient(270deg, rgba(10,5,5,0.92) 0%, rgba(10,5,5,0.75) 36%, rgba(10,5,5,0) 62%)'}} />
      <AbsoluteFill style={{boxShadow: `inset 0 0 0 10px ${RED}`}} />
      <div style={{position: 'absolute', right: 46, top: 40, direction: 'rtl', textAlign: 'right'}}>
        <div style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 168, lineHeight: 0.95, color: '#FFD23F', WebkitTextStroke: '10px #141414', paintOrder: 'stroke fill', textShadow: '0 10px 0 #141414'}}>١٠ أيام</div>
        <div style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 150, lineHeight: 1, color: '#fff', WebkitTextStroke: '10px #141414', paintOrder: 'stroke fill', textShadow: '0 10px 0 #141414'}}>قيتار!</div>
        <div style={{display: 'inline-block', marginTop: 18, background: RED, color: '#fff', fontFamily: 'Tajawal', fontWeight: 900, fontSize: 62, padding: '8px 28px 0', borderRadius: 16, transform: 'rotate(-3deg)', boxShadow: '0 10px 20px rgba(0,0,0,0.5)'}}>وش تعلمت؟</div>
      </div>
      <Img src={staticFile('logo.png')} style={{position: 'absolute', left: 26, top: 22, width: 128, height: 128, filter: 'drop-shadow(0 6px 12px rgba(0,0,0,0.6))'}} />
      <div style={{position: 'absolute', right: 60, bottom: 18, transform: 'rotate(8deg) scale(0.56)', transformOrigin: 'bottom right'}}><ChordDiagram name="Am" delay={0} active /></div>
      {/* red arrow from text to his face */}
      {arrow && <svg width={1280} height={720} style={{position: 'absolute', left: 0, top: 0, filter: 'drop-shadow(0 6px 8px rgba(0,0,0,0.6))'}}>
        <path d="M 760 600 Q 640 660 560 560" fill="none" stroke="#fff" strokeWidth={22} strokeLinecap="round" />
        <path d="M 760 600 Q 640 660 560 560" fill="none" stroke={RED} strokeWidth={12} strokeLinecap="round" />
        <g transform="translate(556 552) rotate(-125)"><path d="M 20 0 L -26 -26 L -14 0 L -26 26 Z" fill={RED} stroke="#fff" strokeWidth={5} strokeLinejoin="round" /></g>
      </svg>}
    </AbsoluteFill>
  );
};

// ---------- CARTOON THUMBNAIL ----------
function burst(cx: number, cy: number, r1: number, r2: number, n: number, rot = 0) {
  let d = '';
  for (let i = 0; i < n * 2; i++) {
    const a = (i / (n * 2)) * Math.PI * 2 + rot;
    const r = i % 2 ? r1 : r2 * (0.85 + 0.15 * Math.sin(i * 2.7));
    d += `${i ? 'L' : 'M'} ${cx + Math.cos(a) * r} ${cy + Math.sin(a) * r} `;
  }
  return d + 'Z';
};
const Note: React.FC<{x: number; y: number; s: number; r: number; c: string}> = ({x, y, s, r, c}) => (
  <g transform={`translate(${x} ${y}) rotate(${r}) scale(${s})`}>
    <path d="M10 44 a10 8 0 1 0 0.1 0 M20 44 V6 L50 0 V36 M50 36 a10 8 0 1 0 0.1 0" fill="none" stroke="#141414" strokeWidth={12} strokeLinejoin="round" strokeLinecap="round" />
    <path d="M10 44 a10 8 0 1 0 0.1 0 M20 44 V6 L50 0 V36 M50 36 a10 8 0 1 0 0.1 0" fill="none" stroke={c} strokeWidth={5} strokeLinejoin="round" strokeLinecap="round" />
    <ellipse cx={10} cy={44} rx={10} ry={8} fill={c} stroke="#141414" strokeWidth={4} /><ellipse cx={40} cy={36} rx={10} ry={8} fill={c} stroke="#141414" strokeWidth={4} />
  </g>
);
const Star: React.FC<{x: number; y: number; s: number; c: string}> = ({x, y, s, c}) => (
  <path transform={`translate(${x} ${y}) scale(${s})`} d="M0 -30 C4 -8 8 -4 30 0 C8 4 4 8 0 30 C-4 8 -8 4 -30 0 C-8 -4 -4 -8 0 -30Z" fill={c} stroke="#141414" strokeWidth={5} strokeLinejoin="round" />
);
export const Thumb2: React.FC<{frame: number; cx?: number}> = ({frame, cx = 0.5}) => {
  const src = staticFile(`frames/${String(frame).padStart(5, '0')}.jpg`);
  const s = 1.3, iw = 1280 * s, ih = 720 * s;
  const left = Math.min(0, Math.max(1280 - iw, 1280 * 0.33 - cx * iw)), top = -ih * 0.1;
  const L: React.CSSProperties = {position: 'absolute', left, top, width: iw, height: ih};
  const big: React.CSSProperties = {fontFamily: 'Tajawal', fontWeight: 900, lineHeight: 0.95, WebkitTextStroke: '14px #141414', paintOrder: 'stroke fill', textShadow: '6px 10px 0 #141414, 10px 16px 0 rgba(0,0,0,0.35)'};
  return (
    <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
      <Img src={src} style={{...L, filter: 'saturate(1.35) contrast(1.12) brightness(1.05)'}} />
      <svg width={1280} height={720} style={{position: 'absolute', left: 0, top: 0}}>
        <defs>
          <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="8" cy="8" r="3.2" fill="#E3262A" opacity="0.55" /></pattern>
          <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stopColor="#FFF4B0" /><stop offset="1" stopColor="#FFC21F" /></radialGradient>
        </defs>
        {/* comic rays + burst behind the title */}
        <g opacity={0.9}>{Array.from({length: 18}, (_, i) => { const a = (i / 18) * Math.PI * 2; return <path key={i} d={`M 1000 300 L ${1000 + Math.cos(a) * 900} ${300 + Math.sin(a) * 900} L ${1000 + Math.cos(a + 0.12) * 900} ${300 + Math.sin(a + 0.12) * 900} Z`} fill={i % 2 ? '#E3262A' : '#FF7A1A'} opacity={0.55} />; })}</g>
        <path d={burst(1000, 300, 330, 430, 16, 0.1)} fill="#141414" transform="translate(10 14)" />
        <path d={burst(1000, 300, 330, 430, 16, 0.1)} fill="url(#glow)" stroke="#141414" strokeWidth={10} strokeLinejoin="round" />
        <path d={burst(1000, 300, 330, 430, 16, 0.1)} fill="url(#dots)" />
      </svg>
      {/* sticker cut-out of Majed with thick cartoon outline */}
      <Img src={staticFile('thumb_outline.png')} style={L} />
      <Img src={staticFile('thumb_person.png')} style={{...L, filter: 'saturate(1.3) contrast(1.1) brightness(1.06)'}} />
      <svg width={1280} height={720} style={{position: 'absolute', left: 0, top: 0}}>
        <Note x={560} y={80} s={1.25} r={14} c="#FFD23F" />
        <Note x={70} y={230} s={1.0} r={-18} c="#ffffff" />
        <Star x={600} y={250} s={1.0} c="#ffffff" /><Star x={470} y={40} s={0.7} c="#FFD23F" /><Star x={150} y={130} s={0.6} c="#FFD23F" />
        {/* excitement marks near his head */}
        <g stroke="#141414" strokeWidth={9} strokeLinecap="round"><path d="M 515 150 L 560 120" /><path d="M 525 190 L 580 185" /><path d="M 520 230 L 565 250" /></g>
        <g stroke="#FFD23F" strokeWidth={4} strokeLinecap="round"><path d="M 515 150 L 560 120" /><path d="M 525 190 L 580 185" /><path d="M 520 230 L 565 250" /></g>
      </svg>
      <div style={{position: 'absolute', right: 70, top: 92, direction: 'rtl', textAlign: 'center', transform: 'rotate(-6deg)'}}>
        <div style={{...big, fontSize: 176, color: '#FFD23F'}}>١٠ أيام</div>
        <div style={{...big, fontSize: 160, color: '#ffffff', marginTop: -6}}>قيتار!</div>
      </div>
      <div style={{position: 'absolute', right: 150, top: 470, transform: 'rotate(4deg)', background: '#E3262A', color: '#fff', fontFamily: 'Tajawal', fontWeight: 900, fontSize: 64, padding: '8px 30px 0', borderRadius: 18, border: '7px solid #141414', boxShadow: '8px 10px 0 #141414', direction: 'rtl'}}>وش تعلمت؟</div>
      <div style={{position: 'absolute', right: 48, bottom: 14, transform: 'rotate(10deg) scale(0.5)', transformOrigin: 'bottom right', filter: 'drop-shadow(10px 12px 0 #141414)'}}><ChordDiagram name="Am" delay={0} active /></div>
      <Img src={staticFile('logo.png')} style={{position: 'absolute', left: 22, top: 18, width: 120, height: 120, filter: 'drop-shadow(5px 7px 0 #141414)'}} />
      <AbsoluteFill style={{boxShadow: 'inset 0 0 0 12px #141414'}} />
    </AbsoluteFill>
  );
};

// ---------- PRO THUMBNAIL (reference style: studio glow, big 3D title, sparkles) ----------
const extrude = (c: string, n: number) => Array.from({length: n}, (_, i) => `${i + 1}px ${i + 1}px 0 ${c}`).join(', ');
const Spark: React.FC<{x: number; y: number; s: number}> = ({x, y, s}) => (
  <path transform={`translate(${x} ${y}) scale(${s})`} d="M0 -30 C3 -7 7 -3 30 0 C7 3 3 7 0 30 C-3 7 -7 3 -30 0 C-7 -3 -3 -7 0 -30Z" fill="#FFE27A" stroke="#7A1022" strokeWidth={3} />
);
export const Thumb3: React.FC<{bg: string; person: string; cx?: number; cy?: number; zoom?: number; l1?: string; l2?: string; tag?: string; chord?: string; sticker?: string; px?: number; tsize?: number}> = ({bg, person, cx = 0.5, cy = 0.45, zoom = 1.28, l1 = '١٠ أيام', l2 = 'قيتار!', tag = 'وش تعلمت؟', chord = 'Am', sticker, px = 0.64, tsize = 168}) => {
  const iw = 1280 * zoom, ih = 720 * zoom;
  const left = Math.min(0, Math.max(1280 - iw, 1280 * px - cx * iw)), top = Math.min(0, Math.max(720 - ih, 720 * 0.5 - cy * ih));
  const L: React.CSSProperties = {position: 'absolute', left, top, width: iw, height: ih};
  const MAROON = '#7A1022';
  const title: React.CSSProperties = {fontFamily: 'Tajawal', fontWeight: 900, lineHeight: 0.98, WebkitTextStroke: `5px ${MAROON}`, paintOrder: 'stroke fill', textShadow: `${extrude(MAROON, 11)}, 14px 18px 22px rgba(0,0,0,0.45)`};
  return (
    <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
      <Img src={staticFile(bg)} style={{...L, filter: 'brightness(1.12) saturate(1.15) contrast(1.02)'}} />
      {/* studio lighting: warm red rim on the left, cool cyan on the right, airy brighten in the middle */}
      <AbsoluteFill style={{mixBlendMode: 'screen', background: 'radial-gradient(ellipse 45% 70% at 4% 60%, rgba(255,70,90,0.75), transparent 70%), radial-gradient(ellipse 40% 60% at 98% 55%, rgba(60,200,255,0.55), transparent 70%), radial-gradient(ellipse 60% 60% at 40% 30%, rgba(255,255,255,0.35), transparent 70%)'}} />
      <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(255,255,255,0.28) 0%, rgba(255,255,255,0.1) 45%, rgba(0,0,0,0) 60%)'}} />
      {/* subject: sharp, punchy, with a soft red rim glow */}
      <Img src={staticFile(person)} style={{...L, filter: 'saturate(1.3) contrast(1.15) brightness(1.08) drop-shadow(0 0 18px rgba(255,60,80,0.55)) drop-shadow(0 18px 28px rgba(0,0,0,0.35))'}} />
      <svg width={1280} height={720} style={{position: 'absolute', left: 0, top: 0}}>
        {/* action lines + sparkles + notes */}
        <g stroke="#ffffff" strokeWidth={7} strokeLinecap="round" fill="none" style={{filter: 'drop-shadow(0 3px 0 rgba(0,0,0,0.35))'}}>
          <path d="M 1035 60 L 1060 26" /><path d="M 1080 84 L 1122 62" /><path d="M 995 66 L 990 30" />
          <path d="M 640 330 Q 600 360 590 410" /><path d="M 612 318 Q 566 344 552 392" />
        </g>
        <Spark x={560} y={230} s={1.1} /><Spark x={520} y={180} s={0.55} /><Spark x={600} y={560} s={0.8} /><Spark x={70} y={640} s={0.7} />
        <g fill="#ffffff" stroke="#7A1022" strokeWidth={3}><ellipse cx={612} cy={640} rx={11} ry={8} /><ellipse cx={640} cy={632} rx={11} ry={8} /></g>
        <path d="M 622 640 V 600 L 650 594 V 632" fill="none" stroke="#ffffff" strokeWidth={6} />
      </svg>
      <div style={{position: 'absolute', left: 46, top: 40, direction: 'rtl', textAlign: 'center', transform: 'rotate(-5deg)'}}>
        <div style={{...title, fontSize: tsize, color: '#FFD23F'}}>{l1}</div>
        <div style={{...title, fontSize: tsize, color: '#ffffff', marginTop: 2}}>{l2}</div>
        <div style={{display: 'inline-block', marginTop: 22, background: MAROON, color: '#fff', fontFamily: 'Tajawal', fontWeight: 900, fontSize: 66, padding: '6px 34px 0', borderRadius: 20, border: '6px solid #fff', boxShadow: '0 12px 24px rgba(0,0,0,0.4)', transform: 'rotate(3deg)'}}>{tag}</div>
      </div>
      {sticker && <div style={{position: 'absolute', left: 52, bottom: 34, width: 170, height: 170, borderRadius: 36, background: '#fff', padding: 22, transform: 'rotate(-8deg)', boxShadow: '0 14px 22px rgba(0,0,0,0.45), 0 0 0 6px #E3262A'}}><Img src={staticFile(sticker)} style={{width: '100%', height: '100%', objectFit: 'contain'}} /></div>}
      {!sticker && chord && <div style={{position: 'absolute', left: 40, bottom: 16, transform: 'rotate(-8deg) scale(0.5)', transformOrigin: 'bottom left', filter: 'drop-shadow(0 14px 18px rgba(0,0,0,0.45))'}}><ChordDiagram name={chord} delay={0} active /></div>}
      <Img src={staticFile('logo.png')} style={{position: 'absolute', right: 22, bottom: 18, width: 112, height: 112, filter: 'drop-shadow(0 6px 12px rgba(0,0,0,0.5))'}} />
    </AbsoluteFill>
  );
};
