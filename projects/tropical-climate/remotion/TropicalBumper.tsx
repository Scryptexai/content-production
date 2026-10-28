import React from 'react';
import { AbsoluteFill } from 'remotion';
import { VisualThemeProvider } from './themes/visual-theme';
import { PaperTitleCard } from './aifl/PaperTitleCard';

/** Bumper judul — memakai komponen PaperTitleCard dari video-shotcraft,
 *  di-reskin ke palet film "Kulit Tropis, Formula Subtropis". */
const Bumper: React.FC = () => {
  return (
    <VisualThemeProvider theme="ink-press">
      <AbsoluteFill style={{ backgroundColor: '#0B0C0A' }}>
        <PaperTitleCard
          duration={150}
          words={[{ text: 'KULIT' }, { text: 'TROPIS.', accent: true }]}
          sub="formula subtropis"
          fontSize={132}
          ink="#EDE4D3"
          accent="#C0603A"
          muted="#8B8577"
          paper="#0B0C0A"
        />
      </AbsoluteFill>
    </VisualThemeProvider>
  );
};

export { Bumper };
