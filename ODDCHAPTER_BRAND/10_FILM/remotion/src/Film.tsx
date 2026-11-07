import React from "react";
import { AbsoluteFill, Audio, Sequence, Series, staticFile } from "remotion";
import { C, T, VO, FPS } from "./theme";
import { Build } from "./scenes/Build";
import { SciencePlate } from "./scenes/SciencePlate";
import { EndCard } from "./scenes/EndCard";
import { SCENE_1_LINES, SCENE_2_LINES, Statement } from "./scenes/Statement";

/**
 * ODDCHAPTER_PILOT_001 — 29.2 s, 1080x1920, 30 fps.
 * Hard cuts only (Series, not TransitionSeries): the brand forbids dissolves.
 * Narration is placed in absolute time so the cut never drifts from the voice.
 */
export const Film: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: C.ink }}>
      <Series>
        <Series.Sequence durationInFrames={T.build.dur}>
          <Build />
        </Series.Sequence>
        <Series.Sequence durationInFrames={T.scene1.dur}>
          <Statement eyebrow="SETIAP MINGGU" lines={SCENE_1_LINES} />
        </Series.Sequence>
        <Series.Sequence durationInFrames={T.scene2.dur}>
          <Statement eyebrow="YANG SEBENARNYA TERJADI" eyebrowTracking={0.2} lines={SCENE_2_LINES} />
        </Series.Sequence>
        <Series.Sequence durationInFrames={T.plate.dur}>
          <SciencePlate />
        </Series.Sequence>
        <Series.Sequence durationInFrames={T.end.dur}>
          <EndCard />
        </Series.Sequence>
      </Series>

      <Sequence from={Math.round(VO.vo1 * FPS)}>
        <Audio src={staticFile("audio/vo_01.wav")} />
      </Sequence>
      <Sequence from={Math.round(VO.vo2 * FPS)}>
        <Audio src={staticFile("audio/vo_02.wav")} />
      </Sequence>
      <Sequence from={Math.round(VO.vo3 * FPS)}>
        <Audio src={staticFile("audio/vo_03.wav")} />
      </Sequence>
      <Sequence from={Math.round(VO.signature * FPS)}>
        <Audio src={staticFile("audio/signature.wav")} />
      </Sequence>
    </AbsoluteFill>
  );
};
