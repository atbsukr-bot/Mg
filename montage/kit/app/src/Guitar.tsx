import React from 'react';
import {useCurrentFrame, useVideoConfig, spring, interpolate, Easing} from 'remotion';

const RED = '#E3262A';
const INK = '#141414';

// low E → high e ; -1 = muted, 0 = open
const SHAPES: Record<string, {frets: number[]; fingers: number[]}> = {
  Am: {frets: [-1, 0, 2, 2, 1, 0], fingers: [0, 0, 2, 3, 1, 0]},
  Em: {frets: [0, 2, 2, 0, 0, 0], fingers: [0, 2, 3, 0, 0, 0]},
  E: {frets: [0, 2, 2, 1, 0, 0], fingers: [0, 2, 3, 1, 0, 0]},
  E7: {frets: [0, 2, 0, 1, 0, 0], fingers: [0, 2, 0, 1, 0, 0]},
};
const NAMES = ['E', 'A', 'D', 'G', 'B', 'e'];

const pop = (f: number, fps: number, delay = 0, damping = 11) =>
  spring({frame: f - delay, fps, config: {damping, stiffness: 170, mass: 0.7}});

export const ChordDiagram: React.FC<{name: string; delay: number; active?: boolean}> = ({name, delay, active}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const sh = SHAPES[name];
  const W = 250, H = 330;
  const gx = 50, gy = 112, sp = 30, fr = 40, nF = 5;
  const card = pop(f, fps, delay);
  const draw = interpolate(f - delay, [4, 16], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  return (
    <div style={{width: W, height: H, transform: `scale(${card}) rotate(${(1 - card) * -8}deg)`, opacity: Math.min(1, card * 1.5)}}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
        <defs>
          <filter id={`sh${name}`} x="-20%" y="-20%" width="140%" height="140%">
            <feDropShadow dx="0" dy="8" stdDeviation="8" floodColor="#000" floodOpacity="0.35" />
          </filter>
        </defs>
        <rect x={6} y={6} width={W - 12} height={H - 12} rx={26} fill="#fff" filter={`url(#sh${name})`} stroke={active ? RED : 'rgba(0,0,0,0.06)'} strokeWidth={active ? 6 : 2} />
        <text x={W / 2} y={70} textAnchor="middle" fontFamily="Tajawal" fontWeight={900} fontSize={58} fill={RED}>{name}</text>
        {/* open / mute marks */}
        {sh.frets.map((v, i) => (
          v <= 0 ? (
            <text key={'o' + i} x={gx + i * sp} y={gy - 12} textAnchor="middle" fontFamily="Cairo" fontWeight={800} fontSize={20}
              fill={v < 0 ? '#999' : INK} opacity={draw}>{v < 0 ? '×' : '○'}</text>
          ) : null
        ))}
        {/* nut */}
        <rect x={gx - 3} y={gy - 4} width={(sp * 5 + 6) * draw} height={8} rx={3} fill={INK} />
        {/* frets */}
        {Array.from({length: nF}, (_, k) => (
          <line key={'f' + k} x1={gx} x2={gx + sp * 5 * draw} y1={gy + (k + 1) * fr} y2={gy + (k + 1) * fr} stroke="#9a9a9a" strokeWidth={2.5} />
        ))}
        {/* strings */}
        {NAMES.map((_, i) => (
          <line key={'s' + i} x1={gx + i * sp} x2={gx + i * sp} y1={gy} y2={gy + nF * fr * draw} stroke={INK} strokeWidth={1.6 + (5 - i) * 0.35} />
        ))}
        {/* string names */}
        {NAMES.map((n, i) => (
          <text key={'n' + i} x={gx + i * sp} y={gy + nF * fr + 26} textAnchor="middle" fontFamily="Cairo" fontWeight={800} fontSize={17} fill="#777" opacity={draw}>{n}</text>
        ))}
        {/* finger dots */}
        {sh.frets.map((v, i) => {
          if (v <= 0) return null;
          const order = sh.fingers[i];
          const p = pop(f, fps, delay + 14 + order * 4, 9);
          const cx = gx + i * sp, cy = gy + (v - 0.5) * fr;
          return (
            <g key={'d' + i} transform={`translate(${cx} ${cy}) scale(${p})`}>
              <circle r={13.5} fill={RED} />
              <text y={6.5} textAnchor="middle" fontFamily="Cairo" fontWeight={800} fontSize={17} fill="#fff">{sh.fingers[i]}</text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};

export const ChordsPanel: React.FC<{dur: number; x?: number; y?: number; scale?: number; chords?: string[]; active?: string; title?: string; cols?: number; stagger?: number}> = ({dur, x = 1450, y = 520, scale = 0.9, chords = ['Am', 'Em', 'E', 'E7'], active, title = 'الكوردات', cols = 2, stagger = 7}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const out = interpolate(f, [dur - 8, dur], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const head = pop(f, fps, 0);
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%,-50%) scale(${scale * (0.85 + 0.15 * out)})`, opacity: out}}>
      <div style={{display: 'flex', justifyContent: 'center', marginBottom: 14, transform: `translateY(${(1 - head) * -40}px)`, opacity: head}}>
        <div style={{background: RED, color: '#fff', fontFamily: 'Tajawal', fontWeight: 900, fontSize: 44, padding: '6px 34px 2px', borderRadius: 16, direction: 'rtl', boxShadow: '0 8px 22px rgba(0,0,0,.35)'}}>{title}</div>
      </div>
      <div style={{display: 'grid', gridTemplateColumns: `repeat(${cols}, 250px)`, gap: 18}}>
        {chords.map((c, i) => <ChordDiagram key={c} name={c} delay={6 + i * stagger} active={active === c} />)}
      </div>
    </div>
  );
};

// ---------- TAB ----------
type N = {s: number; fr: number; col: number}; // s: 0=e (top) … 5=E
const seq: [number, number][] = [
  [0, 6], [0, 7], [0, 4], [0, 2], [0, 1], [1, 2], [1, 4],
  [0, 6], [0, 4], [0, 2], [0, 1], [1, 2], [1, 4],
  [0, 6], [0, 4], [0, 2], [0, 1], [1, 2], [1, 4], [1, 6], [1, 2], [2, 4], [2, 3],
];
const NOTES: N[] = (() => {
  let col = 0;
  return seq.map(([s, fr], i) => {
    if (i === 7 || i === 13) col += 1; // phrase gaps
    return {s, fr, col: col++};
  });
})();

export const TabSheet: React.FC<{dur: number; x?: number; y?: number; scale?: number; npf?: number; startAt?: number; title?: string}> = ({dur, x = 960, y = 300, scale = 1, npf = 9, startAt = 22, title = 'المعزوفة'}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const W = 1240, H = 360, left = 96, colW = 45, top = 108, ls = 38;
  const card = pop(f, fps, 0, 13);
  const out = interpolate(f, [dur - 8, dur], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const lines = interpolate(f, [6, 22], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
  const playIdx = (f - startAt) / npf; // fractional note index
  const lastCol = NOTES[NOTES.length - 1].col;
  const loopIdx = playIdx; // play once, then hold
  const curNote = Math.floor(loopIdx);
  const headCol = curNote < 0 ? -1 : curNote >= NOTES.length ? lastCol + 1.2 : NOTES[curNote].col + (loopIdx - curNote) * ((NOTES[curNote + 1]?.col ?? lastCol + 1) - NOTES[curNote].col);
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(-50%, calc(-50% + ${(1 - card) * -700}px)) scale(${scale * (0.9 + 0.1 * out)})`, opacity: out}}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
        <defs>
          <filter id="tabsh" x="-10%" y="-20%" width="120%" height="150%"><feDropShadow dx="0" dy="10" stdDeviation="12" floodColor="#000" floodOpacity="0.38" /></filter>
          <linearGradient id="ph" x1="0" x2="1"><stop offset="0" stopColor={RED} stopOpacity="0" /><stop offset="1" stopColor={RED} stopOpacity="0.35" /></linearGradient>
        </defs>
        <rect x={8} y={8} width={W - 16} height={H - 16} rx={28} fill="#fff" filter="url(#tabsh)" />
        <rect x={8} y={8} width={W - 16} height={62} rx={28} fill={INK} />
        <rect x={8} y={44} width={W - 16} height={26} fill={INK} />
        <text x={W - 40} y={52} textAnchor="end" fontFamily="Tajawal" fontWeight={900} fontSize={34} fill="#fff">{title}</text>
        <text x={40} y={52} fontFamily="Cairo" fontWeight={800} fontSize={22} fill={RED}>TAB</text>
        {['E', 'B', 'G', 'D', 'A', 'E'].map((n, i) => (
          <g key={i}>
            <text x={50} y={top + i * ls + 8} textAnchor="middle" fontFamily="Cairo" fontWeight={800} fontSize={22} fill={INK} opacity={lines}>{n}</text>
            <line x1={left - 10} x2={left - 10 + (W - left - 40) * lines} y1={top + i * ls} y2={top + i * ls} stroke="#b8b8b8" strokeWidth={2} />
          </g>
        ))}
        <line x1={left - 10} x2={left - 10} y1={top} y2={top + 5 * ls} stroke={INK} strokeWidth={4} opacity={lines} />
        {/* playhead */}
        {headCol >= 0 && (
          <g transform={`translate(${left + 20 + headCol * colW} 0)`} opacity={curNote >= NOTES.length + 6 ? 0 : 1}>
            <rect x={-40} y={top - 22} width={40} height={5 * ls + 44} fill="url(#ph)" />
            <rect x={-2} y={top - 22} width={4} height={5 * ls + 44} rx={2} fill={RED} />
          </g>
        )}
        {NOTES.map((n, i) => {
          const intro = pop(f, fps, 14 + i * 1.2, 12);
          const reached = f >= startAt + i * npf - 2;
          const appear = reached ? 1 : intro;
          if (!reached) {
            const cx0 = left + 20 + n.col * colW, cy0 = top + n.s * ls;
            return (
              <g key={i} transform={`translate(${cx0} ${cy0}) scale(${appear})`} opacity={0.9}>
                <circle r={19} fill="#fff" stroke="#d0d0d0" strokeWidth={2} />
                <text y={9} textAnchor="middle" fontFamily="Cairo" fontWeight={800} fontSize={29} fill="#9a9a9a">{n.fr}</text>
              </g>
            );
          }
          const hit = Math.max(0, 1 - (f - (startAt + i * npf)) / 10);
          const cx = left + 20 + n.col * colW, cy = top + n.s * ls;
          return (
            <g key={i} transform={`translate(${cx} ${cy}) scale(${appear * (1 + hit * 0.35)})`}>
              <circle r={19} fill={hit > 0 ? RED : '#fff'} />
              <text y={9} textAnchor="middle" fontFamily="Cairo" fontWeight={800} fontSize={29} fill={hit > 0 ? '#fff' : INK}>{n.fr}</text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};
export const TAB_NOTES = NOTES.length;

// ---------- STRING NAMES ----------
export const StringNames: React.FC<{dur: number; x?: number; y?: number; scale?: number; title?: string}> = ({dur, x = 1450, y = 520, scale = 1, title = 'أسماء الأوتار'}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const card = pop(f, fps, 0, 15);
  const out = interpolate(f, [dur - 8, dur], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  // thick (6th, low E) at bottom → thin (1st, high e) at top, like looking at the guitar neck
  const rows = [
    {n: 1, note: 'E', th: 1.6}, {n: 2, note: 'B', th: 2.2}, {n: 3, note: 'G', th: 2.8},
    {n: 4, note: 'D', th: 3.6}, {n: 5, note: 'A', th: 4.4}, {n: 6, note: 'E', th: 5.4},
  ];
  const W = 560, H = 470;
  return (
    <div style={{position: 'absolute', left: x, top: y, transform: `translate(calc(-50% + ${(1 - card) * 900}px),-50%) scale(${scale * (0.9 + 0.1 * out)}) rotate(${(1 - card) * 8}deg)`, opacity: out, filter: 'drop-shadow(0 22px 30px rgba(0,0,0,0.45))'}}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
        <defs><filter id="snsh" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="10" stdDeviation="12" floodColor="#000" floodOpacity="0.38" /></filter>
          <linearGradient id="neck" x1="0" x2="0" y1="0" y2="1"><stop offset="0" stopColor="#5a3a22" /><stop offset="1" stopColor="#3d2614" /></linearGradient></defs>
        <rect x={8} y={8} width={W - 16} height={H - 16} rx={28} fill="#fff" filter="url(#snsh)" />
        <rect x={8} y={8} width={W - 16} height={70} rx={28} fill={RED} /><rect x={8} y={50} width={W - 16} height={28} fill={RED} />
        <text x={W / 2} y={57} textAnchor="middle" fontFamily="Tajawal" fontWeight={900} fontSize={40} fill="#fff">{title}</text>
        <rect x={150} y={100} width={330} height={340} rx={10} fill="url(#neck)" />
        {[230, 330, 430].map((fx) => <rect key={fx} x={fx} y={100} width={5} height={340} fill="#c9c9c9" />)}
        <rect x={150} y={100} width={12} height={340} fill="#efe6d2" />
        {rows.map((r, i) => {
          const d = 10 + i * 6;
          const p = pop(f, fps, d, 10);
          const len = interpolate(f - d, [0, 10], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic)});
          const yy = 128 + i * 57;
          const ping = Math.max(0, 1 - (f - d) / 12);
          return (
            <g key={i}>
              <line x1={150} x2={150 + 330 * len} y1={yy} y2={yy} stroke="#e8e0cc" strokeWidth={r.th} />
              <g transform={`translate(90 ${yy}) scale(${p * (1 + ping * 0.3)})`}>
                <circle r={26} fill={ping > 0 ? RED : INK} />
                <text y={11} textAnchor="middle" fontFamily="Cairo" fontWeight={800} fontSize={32} fill="#fff">{r.note}</text>
              </g>
              <text x={515} y={yy + 9} textAnchor="middle" fontFamily="Cairo" fontWeight={800} fontSize={24} fill="#888" opacity={p}>{r.n}</text>
            </g>
          );
        })}
      </svg>
    </div>
  );
};
