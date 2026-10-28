import { Composition } from "remotion";
import { KnotShort, ShortProps } from "./Short";
import { LongForm, LongProps } from "./LongForm";
import { SHOTS } from "./shots";
import { LONG } from "./shots-long";

const FPS = 30;

export const RemotionRoot: React.FC = () => (
  <>
    {Object.entries(SHOTS).map(([id, props]) => (
      <Composition
        key={id}
        id={`KT-${id}`}
        component={KnotShort}
        durationInFrames={Math.max(1, props.beats.length ? props.beats[props.beats.length - 1].to : 1)}
        fps={FPS}
        width={1080}
        height={1920}
        defaultProps={props as ShortProps}
      />
    ))}

    <Composition
      id="KTL-benchmark"
      component={LongForm}
      durationInFrames={Math.max(1, LONG.blocks.length ? LONG.blocks[LONG.blocks.length - 1].to : 1)}
      fps={FPS}
      width={1920}
      height={1080}
      defaultProps={LONG as LongProps}
    />
  </>
);
