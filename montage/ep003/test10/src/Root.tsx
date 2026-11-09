import React from 'react';
import {Composition} from 'remotion';
import {Test} from './Test';
export const RemotionRoot: React.FC = () => (
  <Composition id="Test" component={Test} durationInFrames={300} fps={30} width={1920} height={1080} />
);
