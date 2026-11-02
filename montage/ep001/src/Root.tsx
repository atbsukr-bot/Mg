import React from 'react';
import {Composition} from 'remotion';
import {Montage, Edl} from './Montage';
import edl from '../public/edl.json';

export const RemotionRoot: React.FC = () => (
  <Composition id="Short" component={Montage} defaultProps={{edl: edl as unknown as Edl}}
    durationInFrames={(edl as any).durationInFrames} fps={30} width={1080} height={1920} />
);
