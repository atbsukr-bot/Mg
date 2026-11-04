import React from 'react';
import {AbsoluteFill, Img, Sequence, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring, Easing, random} from 'remotion';
import {PaperBg, PaperTag, PaperList, PersonCard, VocabCard, TapedPhoto, DateStamp} from './Paper';
import {Caption, Keyword, BeatWord, Sparks} from './Graphics';

// Vertical client clip (POV / no face): 1080x1920 frames, Majed-style edit.
const RED = '#E3262A';
const INK = '#141414';
const W = 1080, H = 1920;
const clamp = {extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const};

export type VertSpec = {
  duration: number; title: string; title2?: string; bar: string; cta: string;
  zooms: {f: number; s: number; cx?: number; cy?: number}[];
  captions: {from: number; to: number; words: string[]; hl: number}[];
  items: any[];
};

function burst(cx: number, cy: number, r1: number, r2: number, n: number, rot = 0) {
  let d = '';
  for (let i = 0; i < n * 2; i++) {
    const a = (i / (n * 2)) * Math.PI * 2 + rot;
    const r = i % 2 ? r1 : r2 * (0.85 + 0.15 * Math.sin(i * 2.7));
    d += `${i ? 'L' : 'M'} ${cx + Math.cos(a) * r} ${cy + Math.sin(a) * r} `;
  }
  return d + 'Z';
}

// ring + dot on the thing she points at
const Ping: React.FC<{dur: number; x: number; y: number}> = ({dur, x, y}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f, fps, config: {damping: 10, stiffness: 200, mass: 0.6}});
  const out = interpolate(f, [dur - 6, dur], [1, 0], clamp);
  const rings = [0, 12, 24].map((d) => ((f - d) % 36 + 36) % 36 / 36);
  return (
    <div style={{position: 'absolute', left: x, top: y, opacity: out}}>
      {rings.map((r, i) => (f >= [0, 12, 24][i] ? (
        <div key={i} style={{position: 'absolute', left: 0, top: 0, width: 260 * r, height: 260 * r, transform: 'translate(-50%,-50%)', borderRadius: '50%', border: `${10 * (1 - r)}px solid ${i % 2 ? '#FFD23F' : '#fff'}`, opacity: 1 - r}} />
      ) : null))}
      <div style={{position: 'absolute', left: 0, top: 0, width: 46, height: 46, transform: `translate(-50%,-50%) scale(${p})`, borderRadius: '50%', background: RED, border: '7px solid #fff', boxShadow: '0 6px 16px rgba(0,0,0,0.5)'}} />
    </div>
  );
};

export const Vert: React.FC<{spec: VertSpec}> = ({spec}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const fi = Math.min(spec.duration - 1, f);
  const src = staticFile(`frames/${String(fi).padStart(5, '0')}.jpg`);

  // camera: zoom steps (hard cuts, Khater style) + punch + whip + handheld drift
  let z = spec.zooms[0];
  for (const k of spec.zooms) if (k.f <= f) z = k;
  let punch = 0, bw = false, glitch = 0, shake = 0, flash = 0, whipX = 0, whipBlur = 0, whipS = 0;
  for (const it of spec.items) {
    if (f < it.from || f >= it.from + it.dur) continue;
    const p = f - it.from;
    if (it.type === 'punch') punch += (it.amt ?? 0.06) * Math.exp(-p / (it.tau ?? 5)) * (p < 2 ? p / 2 : 1);
    if (it.type === 'bw') bw = true;
    if (it.type === 'glitch') glitch = 1 - p / it.dur;
    if (it.type === 'shake') shake = (it.amp ?? 16) * (1 - p / it.dur) ** 2;
    if (it.type === 'flash') flash = interpolate(p, [0, 2, it.dur], [0, 0.85, 0], clamp);
    if (it.type === 'whip') {
      const q = p / it.dur, dir = it.dir ?? -1;
      whipX = q < 0.5 ? dir * Easing.in(Easing.cubic)(q * 2) * 900 : -dir * (1 - Easing.out(Easing.cubic)((q - 0.5) * 2)) * 900;
      whipBlur = 24 * Math.sin(Math.PI * q);
      whipS = 0.18 * Math.sin(Math.PI * q);
    }
  }
  const s = z.s * (1 + punch) + whipS;
  const iw = W * s, ih = H * s;
  let left = W / 2 - (z.cx ?? 0.5) * iw, top = H / 2 - (z.cy ?? 0.5) * ih;
  left = Math.min(0, Math.max(W - iw, left)); top = Math.min(0, Math.max(H - ih, top));
  const head = Math.max(0, (s - 1) * W / 2);
  left += Math.max(-head, Math.min(head, Math.sin(f / 47) * 6 + (random(`sx${f}`) - 0.5) * 2 * shake)) ;
  top += Math.max(-head, Math.min(head, Math.cos(f / 61) * 5 + (random(`sy${f}`) - 0.5) * 2 * shake));
  const filt = (bw ? 'grayscale(1) contrast(1.35) brightness(1.05)' : 'saturate(1.08) contrast(1.04)') + (whipBlur > 0.5 ? ` blur(${whipBlur}px)` : '');
  const imgStyle: React.CSSProperties = {position: 'absolute', left: left + whipX, top, width: iw, height: ih, filter: filt};

  const hook = spring({frame: f, fps, config: {damping: 9, stiffness: 200, mass: 0.7}});
  const hookOut = interpolate(f, [70, 80], [1, 0], clamp);
  const barIn = spring({frame: f - 72, fps, config: {damping: 14}});
  const end = spec.duration;
  const ctaIn = spring({frame: f - (end - 75), fps, config: {damping: 9, stiffness: 200}});
  const REG: Record<string, React.FC<any>> = {paperBg: PaperBg, paperTag: PaperTag, paperList: PaperList, person: PersonCard, vocab: VocabCard, taped: TapedPhoto, date: DateStamp, keyword: Keyword, beat: BeatWord, sparks: Sparks, ping: Ping};

  return (
    <AbsoluteFill style={{background: '#000', overflow: 'hidden'}}>
      <Img src={src} style={imgStyle} />
      {glitch > 0 && (
        <>
          <Img src={src} style={{...imgStyle, left: imgStyle.left as number - 24 * glitch, mixBlendMode: 'screen', opacity: 0.4, filter: 'sepia(1) saturate(8) hue-rotate(-50deg)'}} />
          <Img src={src} style={{...imgStyle, left: imgStyle.left as number + 24 * glitch, mixBlendMode: 'screen', opacity: 0.32, filter: 'sepia(1) saturate(8) hue-rotate(160deg)'}} />
          {Array.from({length: 5}, (_, i) => {
            const y = random(`gy${f}${i}`) * H, h = 30 + random(`gh${f}${i}`) * 120, x = (random(`gx${f}${i}`) - 0.5) * 140;
            return <div key={i} style={{position: 'absolute', left: 0, top: y, width: W, height: h, overflow: 'hidden'}}><Img src={src} style={{...imgStyle, top: (imgStyle.top as number) - y, left: (imgStyle.left as number) + x}} /></div>;
          })}
        </>
      )}
      <AbsoluteFill style={{background: 'linear-gradient(180deg, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0) 18%, rgba(0,0,0,0) 62%, rgba(0,0,0,0.55) 100%)'}} />

      {spec.items.filter((it) => REG[it.type]).map((it, i) => {
        const C = REG[it.type];
        return <Sequence key={i} from={it.from} durationInFrames={it.dur} layout="none"><C {...it} /></Sequence>;
      })}

      {/* captions: above the app UI zone */}
      <div style={{position: 'absolute', left: 0, top: 0, width: W, height: 1480}}>
        {spec.captions.map((c, i) => (
          <Sequence key={'c' + i} from={c.from} durationInFrames={c.to - c.from} layout="none"><Caption words={c.words} hl={c.hl} /></Sequence>
        ))}
      </div>

      {/* hook headline (first 2.5 s) */}
      {f < 82 && (
        <>
          <svg width={W} height={H} style={{position: 'absolute', left: 0, top: 0, transform: `scale(${hook * hookOut})`, transformOrigin: '540px 1000px'}}>
            <path d={burst(540, 1000, 340, 470, 18, f / 30)} fill={INK} transform="translate(12 16)" />
            <path d={burst(540, 1000, 340, 470, 18, f / 30)} fill="#FFD23F" stroke={INK} strokeWidth={12} strokeLinejoin="round" />
            <path d={burst(540, 1000, 270, 360, 18, f / 30)} fill="#FF8A1F" opacity={0.35} />
          </svg>
          <div style={{position: 'absolute', left: W / 2, top: 1000, width: 960, transform: `translate(-50%,-50%) rotate(-5deg) scale(${(0.3 + 0.7 * hook) * hookOut})`, textAlign: 'center', direction: 'rtl'}}>
            <div style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 94, lineHeight: 1.1, color: '#fff', WebkitTextStroke: `14px ${INK}`, paintOrder: 'stroke fill', textShadow: `6px 12px 0 ${INK}`}}>{spec.title}</div>
            {spec.title2 && <div style={{display: 'inline-block', marginTop: 18, background: RED, color: '#fff', fontFamily: 'Tajawal', fontWeight: 900, fontSize: 64, padding: '8px 30px 0', borderRadius: 18, border: `7px solid ${INK}`, boxShadow: `8px 10px 0 ${INK}`, whiteSpace: 'nowrap', transform: 'rotate(3deg)'}}>{spec.title2}</div>}
          </div>
        </>
      )}
      {f >= 72 && (
        <div style={{position: 'absolute', left: 0, right: 0, top: 150, display: 'flex', justifyContent: 'center', transform: `translateY(${(1 - barIn) * -200}px)`}}>
          <div style={{background: INK, color: '#fff', fontFamily: 'Tajawal', fontWeight: 900, fontSize: 58, padding: '10px 34px 2px', borderRadius: 20, borderBottom: `8px solid ${RED}`, direction: 'rtl', textAlign: 'center', boxShadow: '0 12px 30px rgba(0,0,0,0.45)'}}>{spec.bar}</div>
        </div>
      )}
      {f >= end - 75 && (
        <div style={{position: 'absolute', left: W / 2, top: 1600, transform: `translate(-50%,-50%) scale(${ctaIn})`, background: RED, borderRadius: 60, padding: '16px 46px 10px', boxShadow: `0 0 ${30 + 20 * Math.sin(f / 4)}px rgba(227,38,42,0.8)`}}>
          <span style={{fontFamily: 'Tajawal', fontWeight: 900, fontSize: 58, color: '#fff', direction: 'rtl', whiteSpace: 'nowrap'}}>{spec.cta}</span>
        </div>
      )}
      <div style={{position: 'absolute', left: 0, top: 0, height: 10, width: (W * f) / end, background: `linear-gradient(90deg, ${RED}, #FFD23F)`, boxShadow: '0 0 14px rgba(227,38,42,0.8)'}} />
      <AbsoluteFill style={{background: '#fff', opacity: flash, pointerEvents: 'none'}} />
      {spec.items.filter((x) => x.type === 'fadeout').map((it, i) => (
        <AbsoluteFill key={'fo' + i} style={{background: '#000', opacity: interpolate(f, [it.from, it.from + it.dur], [0, 1], clamp)}} />
      ))}
    </AbsoluteFill>
  );
};
