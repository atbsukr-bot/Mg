/**
 * Montage driver — turns an edit list (edl.json) into the finished short.
 * Put in src/Montage.tsx. Needs src/style/components.tsx from the
 * arabic-shorts-design skill.
 *
 * Layers, bottom → top:
 *   1. scene track   (talking head / paper stage / dark stage / b-roll, + its elements)
 *   2. caption track (continuous, independent of scenes)
 *   3. audio         (one continuous voice track + music bed + sfx)
 */
import React from 'react';
import {AbsoluteFill, Audio, Composition, OffthreadVideo, Sequence, staticFile} from 'remotion';
import {
  BalanceScene, CalendarCard, Caption, Card, ChatCard, Counter, FlashCut, Glitch, Headline,
  Look, PaperBackground, PathsScene, PlayerCard, ProgressBar, Sfx, Tag, TalkingHead, Vignette,
  WarningTape, Word, WordBurst, XMark, ZoomStep, T,
} from './style/components';
import {CaseFile, CrimeScene, EndCard, Flatline, IncomingCall, Magnifier, MapPin, ReportLog, SirenLights} from './style/crime';

/* ---------- edit list types ---------- */
export type ElementType =
  | 'headline' | 'tag' | 'card' | 'counter' | 'calendar' | 'player' | 'progress'
  | 'burst' | 'chat' | 'paths' | 'balance' | 'x' | 'tape' | 'text'
  | 'magnifier' | 'casefile' | 'flatline' | 'reportlog' | 'call' | 'map' | 'siren' | 'crimescene' | 'endcard';

export type El = {type: ElementType; at?: number; props: Record<string, any>};

export type Scene = {
  from: number; // absolute frame
  dur: number;
  bg: 'head' | 'paper' | 'dark' | 'broll';
  look?: Look; // head / broll grade
  trimBefore?: number; // head: frame in aroll.mp4 (default = from)
  zoomSteps?: ZoomStep[]; // head: jump-cut zooms (frames relative to scene)
  broll?: string; // broll: file in public/
  transition?: 'cut' | 'glitch' | 'glitch-bw' | 'flash';
  elements?: El[];
};

export type Edl = {
  fps: number;
  durationInFrames: number;
  aroll: string; // public/aroll.mp4 — silence-cut talking head
  scenes: Scene[];
  captions: Word[][]; // chunks; frames absolute
  sfx?: {src: string; at: number; volume?: number}[];
  music?: {src: string; volume?: number};
  voiceEnd?: number; // stop the A-roll voice here (frames)
};

/* ---------- element registry ---------- */
const Text: React.FC<{text: string; x: number; y: number; size?: number; color?: string}> = ({text, x, y, size = 64, color = T.ink}) => (
  <div style={{position: 'absolute', left: x, top: y, transform: 'translate(-50%,-50%)', fontFamily: T.head, fontWeight: 900, fontSize: size, color, direction: 'rtl', whiteSpace: 'nowrap'}}>{text}</div>
);

const REGISTRY: Record<ElementType, React.FC<any>> = {
  headline: Headline, tag: Tag, card: Card, counter: Counter, calendar: CalendarCard, player: PlayerCard,
  progress: ProgressBar, burst: WordBurst, chat: ChatCard, paths: PathsScene, balance: BalanceScene,
  x: XMark, tape: WarningTape, text: Text,
  magnifier: Magnifier, casefile: CaseFile, flatline: Flatline, reportlog: ReportLog, call: IncomingCall, map: MapPin,
  siren: SirenLights, crimescene: CrimeScene, endcard: EndCard,
};

/* ---------- one scene ---------- */
const SceneView: React.FC<{s: Scene; aroll: string}> = ({s, aroll}) => {
  const base =
    s.bg === 'head' ? (
      <TalkingHead src={aroll} trimBefore={s.trimBefore ?? s.from} dur={s.dur} look={s.look} zoomSteps={s.zoomSteps} />
    ) : s.bg === 'broll' && s.broll ? (
      <AbsoluteFill style={{filter: 'brightness(.55) saturate(.85)'}}>
        <OffthreadVideo src={staticFile(s.broll)} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        <Vignette strength={0.6} />
      </AbsoluteFill>
    ) : (
      <PaperBackground dark={s.bg === 'dark'} />
    );

  const body = (
    <AbsoluteFill>
      {base}
      {(s.elements ?? []).map((e, i) => {
        const C = REGISTRY[e.type];
        // card children may be given as `text` for convenience
        const {text, ...rest} = e.props;
        return (
          <Sequence key={i} from={e.at ?? 0} layout="none">
            {e.type === 'card' ? (
              <C {...rest}><div style={{padding: 24, fontFamily: T.head, fontWeight: 900, fontSize: rest.size ?? 60, color: T.ink, textAlign: 'center'}}>{text}</div></C>
            ) : (
              <C {...e.props} />
            )}
          </Sequence>
        );
      })}
      {s.transition === 'flash' && <FlashCut />}
    </AbsoluteFill>
  );

  return s.transition === 'glitch' || s.transition === 'glitch-bw' ? (
    <Glitch dur={s.dur} bw={s.transition === 'glitch-bw'}>{body}</Glitch>
  ) : (
    body
  );
};

/* ---------- the composition ---------- */
export const Montage: React.FC<{edl: Edl}> = ({edl}) => (
  <AbsoluteFill style={{background: '#000'}}>
    {edl.scenes.map((s, i) => (
      <Sequence key={i} from={s.from} durationInFrames={s.dur}>
        <SceneView s={s} aroll={edl.aroll} />
      </Sequence>
    ))}

    {edl.captions.map((chunk, i) => {
      const from = chunk[0].start;
      const to = edl.captions[i + 1]?.[0].start ?? chunk[chunk.length - 1].end + 8;
      const local = chunk.map((w) => ({...w, start: w.start - from, end: w.end - from}));
      return (
        <Sequence key={`c${i}`} from={from} durationInFrames={Math.max(1, to - from)}>
          <Caption words={local} />
        </Sequence>
      );
    })}

    {/* voice: continuous, never cut by scene changes */}
    <Sequence durationInFrames={edl.voiceEnd ?? edl.durationInFrames} layout="none"><Audio src={staticFile(edl.aroll)} /></Sequence>
    {edl.music && <Audio src={staticFile(edl.music.src)} volume={edl.music.volume ?? 0.08} loop />}
    {(edl.sfx ?? []).map((x, i) => <Sfx key={i} {...x} />)}
  </AbsoluteFill>
);

/* ---------- Root (src/Root.tsx) ---------- */
// import edl from '../public/edl.json';
// export const RemotionRoot = () => (
//   <Composition id="Short" component={Montage} defaultProps={{edl: edl as Edl}}
//     durationInFrames={edl.durationInFrames} fps={30} width={1080} height={1920} />
// );
export {Composition};
