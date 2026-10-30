import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile} from 'remotion';
import {Bumper} from './Bumper';
import {
  Scene01,
  Scene02,
  Scene03,
  Scene04,
  Scene05,
  Scene06,
  Scene07,
  Scene08,
  Scene09,
  Scene10,
} from './scenes';
import {C, FontGate} from './atoms';

export const BUMPER_FRAMES = 152;

/**
 * Durasi tiap adegan = lead + durasi VO + tail, dibulatkan ke frame (30 fps).
 * Angka ini identik dengan render.py supaya audio (mix.wav) tetap sinkron.
 */
export const SCENE_FRAMES = [463, 431, 323, 386, 602, 751, 895, 616, 933, 357];
export const SCENE_STARTS = SCENE_FRAMES.reduce<number[]>((acc, d, i) => {
  acc.push(i === 0 ? 0 : acc[i - 1] + SCENE_FRAMES[i - 1]);
  return acc;
}, []);
export const FILM_FRAMES = SCENE_FRAMES.reduce((a, b) => a + b, 0);
export const TOTAL_FRAMES = BUMPER_FRAMES + FILM_FRAMES;

const SCENES: React.ComponentType<any>[] = [
  Scene01,
  Scene02,
  Scene03,
  Scene04,
  Scene05,
  Scene06,
  Scene07,
  Scene08,
  Scene09,
  Scene10,
];

const VO = [
  'audio/vo-01.mp3',
  'audio/vo-02.mp3',
  'audio/vo-03.mp3',
  'audio/vo-04.mp3',
  'audio/vo-05.mp3',
  'audio/vo-06.mp3',
  'audio/vo-07.mp3',
  'audio/vo-08.mp3',
  'audio/vo-09.mp3',
  'audio/vo-10.mp3',
];

/** Lead-in tiap adegan (detik) — narasi mulai setelah jeda ini. */
const LEAD = [1.6, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3];

export const Film: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: C.bg}}>
    <FontGate />
    <Sequence durationInFrames={BUMPER_FRAMES}>
      <Bumper />
    </Sequence>

    {SCENES.map((S, i) => (
      <Sequence
        key={i}
        from={BUMPER_FRAMES + SCENE_STARTS[i]}
        durationInFrames={SCENE_FRAMES[i]}
        name={`S${String(i + 1).padStart(2, '0')}`}
      >
        <S dur={SCENE_FRAMES[i]} />
        <Sequence from={Math.round(LEAD[i] * 30)}>
          <Audio src={staticFile(VO[i])} />
        </Sequence>
      </Sequence>
    ))}
  </AbsoluteFill>
);

/** Film tanpa bumper — dipakai untuk QA cepat per bagian. */
export const FilmScenesOnly: React.FC = () => (
  <AbsoluteFill style={{backgroundColor: C.bg}}>
    <FontGate />
    {SCENES.map((S, i) => (
      <Sequence key={i} from={SCENE_STARTS[i]} durationInFrames={SCENE_FRAMES[i]}>
        <S dur={SCENE_FRAMES[i]} />
      </Sequence>
    ))}
  </AbsoluteFill>
);

/** Satu adegan saja, untuk memeriksa layout tanpa render penuh. */
export const makeScene = (n: number): React.FC => {
  const S = SCENES[n - 1];
  return () => (
    <AbsoluteFill style={{backgroundColor: C.bg}}>
      <FontGate />
      <S dur={SCENE_FRAMES[n - 1]} />
    </AbsoluteFill>
  );
};
