import React from 'react';
import {AbsoluteFill, Audio, OffthreadVideo, Sequence, Img, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring, Easing, random} from 'remotion';
import {ChordsPanel, TabSheet, StringNames} from './Guitar';
import {RawCard, PromptBox, EditorUI, Checklist, PhoneClip, WideCard, Badge, Counter, NotesList, SkillFile, Branch, Notice, RefCard} from './Promo';
import {PaperBg, PaperTag, PaperList, PersonCard, VocabCard, TapedPhoto, DateStamp} from './Paper';
import {LogoIntro, LogoCorner, Subscribe, Keyword, LowerThird, Sparks, Caption, ImageCard, Arrow, BeatWord} from './Graphics';


export type Cam = {f: number; s: number; x: number; y: number; mode?: 'cut' | 'ease'; dur?: number};
export type Cap = {from: number; to: number; words: string[]; hl: number};
export type Item = {type: string; from: number; dur: number; [k: string]: any};
export type Edl = {
  duration: number; video: string; cam: Cam[]; captions: Cap[]; items: Item[];
  sfx: {f: number; name: string; v?: number}[]; music: {f: number; v: number}[]; musicFile: string;
};

const camAt = (cam: Cam[], f: number) => {
  let i = 0;
  while (i + 1 < cam.length && cam[i + 1].f <= f) i++;
  const a = cam[i];
  const b = cam[i + 1];
  // an 'ease' keyframe starts moving `dur` frames before its f
  if (b && b.mode === 'ease') {
    const d = b.dur ?? 20;
    if (f > b.f - d) {
      const t = Easing.inOut(Easing.cubic)(Math.min(1, (f - (b.f - d)) / d));
      return {s: a.s + (b.s - a.s) * t, x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t};
    }
  }
  return {s: a.s, x: a.x, y: a.y};
};

const fxActive = (items: Item[], type: string, f: number) =>
  items.filter((it) => it.type === type && f >= it.from && f < it.from + it.dur);

export const Main: React.FC<{edl: Edl; noAudio?: boolean}> = ({edl, noAudio}) => {
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const c = camAt(edl.cam, f);

  // shake
  let sx = 0, sy = 0, rot = 0;
  for (const it of fxActive(edl.items, 'shake', f)) {
    const p = (f - it.from) / it.dur;
    const amp = (it.amp ?? 18) * (1 - p) ** 2;
    sx += (random(`sx${f}`) - 0.5) * 2 * amp;
    sy += (random(`sy${f}`) - 0.5) * 2 * amp;
    rot += (random(`r${f}`) - 0.5) * amp * 0.08;
  }
  // punch: quick scale bump that settles (beat zoom)
  let punch = 0;
  for (const it of fxActive(edl.items, 'punch', f)) {
    const p = f - it.from;
    punch += (it.amt ?? 0.06) * Math.exp(-p / (it.tau ?? 5)) * (p < 2 ? p / 2 : 1);
  }
  // handheld drift – soft, always on
  const dx = Math.sin(f / 47) * 7 + Math.sin(f / 23) * 2.5;
  const dy = Math.cos(f / 61) * 5 + Math.sin(f / 31) * 1.5;
  const dr = Math.sin(f / 89) * 0.22;
  let whipX = 0, whipBlur = 0, whipS = 0;
  for (const it of fxActive(edl.items, 'whip', f)) {
    const p = (f - it.from) / it.dur;
    const dir = it.dir ?? -1;
    if (p < 0.5) { const q = Easing.in(Easing.cubic)(p * 2); whipX = dir * q * 1500; }
    else { const q = 1 - Easing.out(Easing.cubic)((p - 0.5) * 2); whipX = -dir * q * 1500; }
    whipBlur = 26 * Math.sin(Math.PI * p);
    whipS = 0.25 * Math.sin(Math.PI * p);
  }
  const scale = c.s * (1 + punch) + whipS;
  // keep frame filled: clamp translation by available headroom
  const maxX = ((scale - 1) * width) / 2, maxY = ((scale - 1) * height) / 2;
  const tx = Math.max(-maxX, Math.min(maxX, c.x * scale + dx + sx));
  const ty = Math.max(-maxY, Math.min(maxY, c.y * scale + dy + sy));

  const bw = fxActive(edl.items, 'bw', f).length > 0;
  const glitch = fxActive(edl.items, 'glitch', f);
  const vidStyle: React.CSSProperties = {
    width, height, position: 'absolute',
    filter: (bw ? 'grayscale(1) contrast(1.35) brightness(1.05)' : 'saturate(1.08) contrast(1.04)') + (whipBlur > 0.5 ? ` blur(${whipBlur}px)` : ''),
  };
  const transform = `translate(${tx + whipX}px, ${ty}px) scale(${scale}) rotate(${dr + rot}deg)`;
  const fi = Math.min(edl.duration - 1, f);
  const vSrc = staticFile(`frames/${String(fi).padStart(5, '0')}.jpg`);

  return (
    <AbsoluteFill style={{backgroundColor: '#000', overflow: 'hidden'}}>
      <AbsoluteFill style={{transform, transformOrigin: '50% 50%'}}>
        <Img src={vSrc} style={vidStyle} />
        
        {glitch.length > 0 && <GlitchLayer src={vSrc} f={f} it={glitch[0]} />}
      </AbsoluteFill>
      {/* soft vignette for depth – background itself untouched */}
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 62%, rgba(0,0,0,0.28) 100%)', pointerEvents: 'none'}} />

      {edl.items.map((it, i) => {
        const C = REG[it.type];
        if (!C) return null;
        return (
          <Sequence key={i} from={it.from} durationInFrames={it.dur} layout="none">
            <C {...it} />
          </Sequence>
        );
      })}

      {edl.captions.map((cp, i) => (
        <Sequence key={'c' + i} from={cp.from} durationInFrames={cp.to - cp.from} layout="none">
          <Caption words={cp.words} hl={cp.hl} />
        </Sequence>
      ))}

      {fxActive(edl.items, 'nologo', f).length === 0 && <LogoCorner start={(edl as any).logoStart ?? (edl.items.find((x) => x.type === 'logoIntro') ? (edl.items.find((x) => x.type === 'logoIntro')!.from + 62) : 0)} />}

      {edl.items.filter((x) => x.type === 'flash').map((it, i) => (
        <Sequence key={'fl' + i} from={it.from} durationInFrames={it.dur} layout="none"><Flash dur={it.dur} color={it.color} /></Sequence>
      ))}
      {edl.items.filter((x) => x.type === 'fadeout').map((it, i) => (
        <AbsoluteFill key={'fo' + i} style={{background: '#000', opacity: interpolate(f, [it.from, it.from + it.dur], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}), pointerEvents: 'none'}} />
      ))}
      {edl.items.filter((x) => x.type === 'leak').map((it, i) => (
        <Sequence key={'lk' + i} from={it.from} durationInFrames={it.dur} layout="none"><Leak dur={it.dur} /></Sequence>
      ))}

      {!noAudio && (<>
      <Audio src={staticFile('voice.wav')} />
      <Audio src={staticFile(edl.musicFile)} loop volume={(fr) => musicVol(edl.music, fr)} />
      {edl.sfx.map((s, i) => (
        <Sequence key={'s' + i} from={s.f} durationInFrames={90} layout="none">
          <Audio src={staticFile(`sfx/${s.name}.wav`)} volume={s.v ?? 0.5} />
        </Sequence>
      ))}
      </>)}
    </AbsoluteFill>
  );
};

const musicVol = (kf: {f: number; v: number}[], f: number) => {
  if (!kf.length) return 0.08;
  let i = 0;
  while (i + 1 < kf.length && kf[i + 1].f <= f) i++;
  const a = kf[i], b = kf[i + 1];
  if (!b) return a.v;
  return interpolate(f, [a.f, b.f], [a.v, b.v], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
};

const GlitchLayer: React.FC<{src: string; f: number; it: Item}> = ({src, f, it}) => {
  const {width, height} = useVideoConfig();
  const k = f - it.from;
  const off = 18 * (1 - k / it.dur) + 6;
  const slices = Array.from({length: 6}, (_, i) => {
    const y = random(`gy${f}${i}`) * height;
    const h = 20 + random(`gh${f}${i}`) * 90;
    const x = (random(`gx${f}${i}`) - 0.5) * 120;
    return {y, h, x};
  });
  return (
    <>
      <Img src={src} style={{width, height, position: 'absolute', transform: `translateX(${-off}px)`, mixBlendMode: 'screen', opacity: 0.38, filter: 'sepia(1) saturate(8) hue-rotate(-50deg)'}} />
      <Img src={src} style={{width, height, position: 'absolute', transform: `translateX(${off}px)`, mixBlendMode: 'screen', opacity: 0.3, filter: 'sepia(1) saturate(8) hue-rotate(160deg)'}} />
      {slices.map((s, i) => (
        <div key={i} style={{position: 'absolute', left: 0, top: s.y, width, height: s.h, overflow: 'hidden'}}>
          <Img src={src} style={{width, height, position: 'absolute', top: -s.y, left: s.x}} />
        </div>
      ))}
      <AbsoluteFill style={{background: 'repeating-linear-gradient(0deg, rgba(0,0,0,0.12) 0 2px, transparent 2px 4px)'}} />
    </>
  );
};

const Flash: React.FC<{dur: number; color?: string}> = ({dur, color}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [0, 2, dur], [0, 0.9, 0], {extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{background: color ?? '#fff', opacity: o, pointerEvents: 'none'}} />;
};

const Leak: React.FC<{dur: number}> = ({dur}) => {
  const f = useCurrentFrame();
  const p = f / dur;
  const o = interpolate(p, [0, 0.25, 0.7, 1], [0, 0.85, 0.5, 0]);
  const x = interpolate(p, [0, 1], [-20, 120]);
  return (
    <AbsoluteFill style={{mixBlendMode: 'screen', opacity: o, pointerEvents: 'none',
      background: `radial-gradient(ellipse 45% 70% at ${x}% 40%, rgba(255,140,40,0.95), rgba(255,60,30,0.5) 40%, transparent 70%)`}} />
  );
};

const REG: Record<string, React.FC<any>> = {
  paperBg: PaperBg, paperTag: PaperTag, paperList: PaperList, person: PersonCard, vocab: VocabCard, taped: TapedPhoto, date: DateStamp,
  logoIntro: LogoIntro,
  subscribe: Subscribe,
  keyword: Keyword,
  lower: LowerThird,
  sparks: Sparks,
  chords: ChordsPanel,
  tab: TabSheet,
  strings: StringNames,
  image: ImageCard,
  arrow: Arrow,
  beat: BeatWord,
  raw: RawCard, prompt: PromptBox, editor: EditorUI, checklist: Checklist, phone: PhoneClip, wide: WideCard,
  badge: Badge, counter: Counter, notes: NotesList, skill: SkillFile, branch: Branch, notice: Notice, ref: RefCard,
};
