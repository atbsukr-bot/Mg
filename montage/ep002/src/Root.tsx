import React from 'react';
import {Composition} from 'remotion';
import {PaperScene} from './Paper';
import {SubscribeOverlay} from './Subscribe';
import {Chapter, Clock, CallRecord, Phone, MapRoute, Scene, Year, Quote, EndCard, BigTitle, Black} from './Inserts';

// every insert takes {dur} (frames) so build.py can size it to the narration it covers
const meta = ({props}: {props: any}) => ({durationInFrames: Math.max(1, Math.round(props.dur ?? 150))});
const items: [string, React.FC<any>, any][] = [
  ['Chapter', Chapter, {num: 'الجزء الأول', title: 'الليلة الهادية'}],
  ['Clock', Clock, {}],
  ['CallRecord', CallRecord, {}],
  ['Phone', Phone, {}],
  ['MapRoute', MapRoute, {}],
  ['Scene', Scene, {}],
  ['Year', Year, {}],
  ['Quote', Quote, {text: 'لا تفتحون الباب الرابع'}],
  ['EndCard', EndCard, {}],
  ['BigTitle', BigTitle, {title: 'بلاغ بلا عنوان'}],
  ['Black', Black, {}],
  ['PaperScene', PaperScene, {}],
  ['SubscribeOverlay', SubscribeOverlay, {}],   // no default content: build.py props would merge over it
];
export const RemotionRoot: React.FC = () => (
  <>
    {items.map(([id, C, p]) => (
      <Composition key={id} id={id} component={C} defaultProps={{dur: 150, ...p}} calculateMetadata={meta}
        durationInFrames={150} fps={30} width={2560} height={1440} />
    ))}
  </>
);
