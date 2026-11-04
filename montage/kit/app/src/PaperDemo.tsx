import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {PaperBg, PaperTag, PaperList, PersonCard, VocabCard, TapedPhoto, DateStamp} from './Paper';

// 12 s vertical demo of the archive/scrapbook style (1080x1920)
export const PaperDemo: React.FC = () => (
  <AbsoluteFill style={{background: '#000'}}>
    <PaperBg dur={360} />
    {/* scene 1: date + person card */}
    <Sequence from={6} durationInFrames={150} layout="none"><DateStamp dur={150} x={330} y={330} text="OCT 2026" /></Sequence>
    <Sequence from={20} durationInFrames={136} layout="none"><PaperTag dur={136} text="المدينة · السعودية" x={720} y={450} tone="yellow" tape size={44} tilt={1.5} /></Sequence>
    <Sequence from={40} durationInFrames={116} layout="none"><PersonCard dur={116} x={540} y={760} img="logo.png" name="ماجد خالد" latin="MAJED KHALID" note="صاحب قناة MN Cousins" /></Sequence>
    <Sequence from={70} durationInFrames={86} layout="none"><PaperList dur={86} x={560} y={1060} size={54} items={[
      {text: 'بدأ يتعلم القيتار', tone: 'cream', at: 0},
      {text: 'وصوّر كل يوم', tone: 'blue', at: 22},
      {text: '١٠ أيام بس', tone: 'red', at: 44},
    ]} /></Sequence>
    {/* scene 2: vocab + taped photo + key number */}
    <Sequence from={170} durationInFrames={190} layout="none"><DateStamp dur={190} x={300} y={330} text="DAY 10" tone="cream" /></Sequence>
    <Sequence from={185} durationInFrames={175} layout="none"><TapedPhoto dur={175} x={540} y={680} img="claude.png" w={420} h={300} caption="AI EDITOR · CLAUDE" tilt={-2} bw={false} /></Sequence>
    <Sequence from={225} durationInFrames={135} layout="none"><VocabCard dur={135} x={540} y={1080} word="montage" meaning="مونتاج" /></Sequence>
    <Sequence from={265} durationInFrames={95} layout="none"><PaperList dur={95} x={540} y={1330} size={54} items={[
      {text: 'بدون ما يلمس الجوال', tone: 'green', at: 0},
      {text: 'المونتاج كله جاهز', tone: 'red', at: 24},
    ]} /></Sequence>
  </AbsoluteFill>
);
