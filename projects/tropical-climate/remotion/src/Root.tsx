import React from 'react';
import {Composition} from 'remotion';
import {Film, FilmScenesOnly, SCENE_FRAMES, makeScene, TOTAL_FRAMES, FILM_FRAMES} from './film/Film';

/**
 * Semua <Composition> didaftarkan di SATU komponen Root.
 * Jangan pernah memberi registerRoot sebuah Fragment (<>) — esbuild gagal.
 */
export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="TropicalFilm"
        component={Film}
        durationInFrames={TOTAL_FRAMES}
        fps={30}
        width={1080}
        height={1920}
      />
      <Composition
        id="TropicalScenes"
        component={FilmScenesOnly}
        durationInFrames={FILM_FRAMES}
        fps={30}
        width={1080}
        height={1920}
      />
      {SCENE_FRAMES.map((d, i) => (
        <Composition
          key={i}
          id={`S${String(i + 1).padStart(2, '0')}`}
          component={makeScene(i + 1)}
          durationInFrames={d}
          fps={30}
          width={1080}
          height={1920}
        />
      ))}
    </>
  );
};
