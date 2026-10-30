import React from 'react';
import { Composition } from 'remotion';
import { Film, DURATION } from './Main';

export const RemotionRoot: React.FC = () => (
  <Composition
    id="KnotTheory"
    component={Film}
    durationInFrames={DURATION}
    fps={30}
    width={1080}
    height={1920}
  />
);
