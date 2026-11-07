import React from "react";
import brand from "../brand.json";

/**
 * The marks are outlines from tools/brand.py — no live text, no font dependency,
 * identical geometry to the SVG masters in 01_LOGO/.
 */

/** Monogram, sized by ink width. The ink box is 91.065 x 54 units inside the 100 box. */
export const Monogram: React.FC<{ width: number; color?: string; style?: React.CSSProperties }> = ({
  width,
  color = brand.colors.ivory,
  style,
}) => {
  const [x0, y0, x1, y1] = brand.monogram.inkBox;
  const w = x1 - x0;
  const h = y1 - y0;
  return (
    <svg
      width={width}
      height={(width * h) / w}
      viewBox={`${x0} ${y0} ${w} ${h}`}
      style={style}
      aria-label="ODDCHAPTER monogram"
    >
      <path d={brand.monogram.d} fill={color} fillRule="evenodd" />
    </svg>
  );
};

/** ODDCHAPTER as outlines, sized by cap height (100 units in the source path). */
export const Wordmark: React.FC<{ capHeight: number; color?: string; style?: React.CSSProperties }> = ({
  capHeight,
  color = brand.colors.ivory,
  style,
}) => {
  const w = brand.wordmark.width;
  return (
    <svg
      width={(capHeight * w) / 100}
      height={capHeight * 1.02}
      viewBox={`0 -100 ${w} 100`}
      style={style}
      aria-label="ODDCHAPTER wordmark"
    >
      <path d={brand.wordmark.d} fill={color} />
    </svg>
  );
};

/** Tagline as outlines. */
export const Tagline: React.FC<{ width: number; color?: string; style?: React.CSSProperties }> = ({
  width,
  color = brand.colors.sage,
  style,
}) => {
  const w = brand.tagline.width;
  return (
    <svg
      width={width}
      height={(width * 26) / w}
      viewBox={`0 -26 ${w} 26`}
      style={style}
      aria-label="Kisah nyata. Di luar dugaan."
    >
      <path d={brand.tagline.d} fill={color} />
    </svg>
  );
};
