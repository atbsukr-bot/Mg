import React from 'react';
import {Composition, staticFile} from 'remotion';
import {Main, Edl} from './Main';
import {Short, Thumb, Thumb2, Thumb3} from './Short';
import {Vert} from './Vert';
import {AdCard} from './Ad';
import {PaperDemo} from './PaperDemo';
export const Root: React.FC = () => (
  <>
    <Composition id="Main" component={Main as any} width={1920} height={1080} fps={30}
      durationInFrames={300}
      defaultProps={{edlFile: 'edl.json'}}
      calculateMetadata={async ({props}) => {
        const edl: Edl = await (await fetch(staticFile((props as any).edlFile))).json();
        return {durationInFrames: edl.duration, props: {...props, edl}};
      }}
    />
    <Composition id="Short" component={Short as any} width={1080} height={1920} fps={30}
      durationInFrames={300}
      defaultProps={{specFile: 'short1.json'}}
      calculateMetadata={async ({props}) => {
        const spec = await (await fetch(staticFile((props as any).specFile))).json();
        return {durationInFrames: spec.duration, props: {...props, spec}};
      }}
    />
    <Composition id="Vert" component={Vert as any} width={1080} height={1920} fps={30}
      durationInFrames={300}
      defaultProps={{specFile: 'edl.json'}}
      calculateMetadata={async ({props}) => {
        const spec = await (await fetch(staticFile((props as any).specFile))).json();
        return {durationInFrames: spec.duration, props: {...props, spec}};
      }}
    />
    <Composition id="PaperDemo" component={PaperDemo} width={1080} height={1920} fps={30} durationInFrames={360} />
    <Composition id="AdCard" component={AdCard} width={1080} height={1080} fps={30} durationInFrames={1} />
    <Composition id="Thumb3" component={Thumb3 as any} width={1280} height={720} fps={30} durationInFrames={60} defaultProps={{bg: 't3_bg.jpg', person: 't3_person.png', cx: 0.5, cy: 0.42}} />
    <Composition id="Thumb2" component={Thumb2 as any} width={1280} height={720} fps={30} durationInFrames={60} defaultProps={{frame: 4200, cx: 0.5}} />
    <Composition id="Thumb" component={Thumb as any} width={1280} height={720} fps={30} durationInFrames={60} defaultProps={{frame: 9045, cx: 0.5}} />
  </>
);
