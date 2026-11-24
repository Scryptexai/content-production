#!/usr/bin/env python3
"""Create a restrained original ambience and loudness-normalized master for AK-EP11."""
from pathlib import Path
import json
import subprocess
import wave
import numpy as np
import imageio_ffmpeg

CASE = Path(__file__).resolve().parent
FF = imageio_ffmpeg.get_ffmpeg_exe()
END = 35.490
SR = 48000


def run(cmd):
    p = subprocess.run(cmd, text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(" ".join(map(str, cmd)) + "\n" + p.stderr[-5000:])
    return p


def make_bed():
    n = round(END * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(211)
    # Original low-key sea-like ambience—not a music track and not a siren/scream effect.
    low = 0.32*np.sin(2*np.pi*55*t) + 0.17*np.sin(2*np.pi*82.5*t+0.4) + 0.08*np.sin(2*np.pi*110*t+1.1)
    noise = rng.standard_normal(n)
    wind = np.convolve(noise, np.ones(820)/820, mode="same")
    swell = 0.55 + 0.45*np.sin(2*np.pi*0.052*t-0.5)
    bed = low*(0.72+0.28*np.sin(2*np.pi*0.042*t)) + wind*0.85*swell
    for at, amp in ((0.1,0.18),(8.37,0.22),(17.74,0.26),(24.29,0.28),(32.35,0.16)):
        i=int(at*SR); ln=min(int(1.1*SR), n-i); tt=np.arange(ln)/SR
        bed[i:i+ln] += amp*np.sin(2*np.pi*47*tt)*np.exp(-3.8*tt)
    bed[:int(0.55*SR)] *= np.linspace(0,1,int(0.55*SR))
    bed[-int(1.1*SR):] *= np.linspace(1,0,int(1.1*SR))
    bed = bed/(np.max(np.abs(bed))+1e-9)*0.27
    stereo=np.stack([bed, np.roll(bed, int(0.006*SR))],axis=1)
    audio=CASE/'audio'; audio.mkdir(exist_ok=True)
    with wave.open(str(audio/'bed.wav'),'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(stereo,-1,1)*32767).astype('<i2').tobytes())


def mix():
    audio=CASE/'audio'
    voice=CASE/'vo_internal'/'AK-EP11_smong-simeulue_voice-08_fast.wav'
    raw=audio/'mix_raw.wav'
    filt=(
        "[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
        "volume=1.95,highpass=f=70,lowpass=f=13500,"
        "acompressor=threshold=0.13:ratio=2.5:attack=12:release=160,apad=whole_dur=35.490,atrim=duration=35.490,asplit=2[vo][side];"
        "[1:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
        "volume=0.72,apad=whole_dur=35.490,atrim=duration=35.490[bed];"
        "[bed][side]sidechaincompress=threshold=0.055:ratio=7:attack=18:release=280[duck];"
        "[vo][duck]amix=inputs=2:duration=longest:normalize=0:dropout_transition=0,"
        "alimiter=limit=0.88:level=false[out]"
    )
    run([FF,'-y','-i',str(voice),'-i',str(audio/'bed.wav'),'-filter_complex',filt,'-map','[out]',
         '-ar','48000','-ac','2','-t',f'{END:.3f}',str(raw)])
    probe=run([FF,'-hide_banner','-nostats','-i',str(raw),'-af','loudnorm=I=-15:TP=-1.5:LRA=9:print_format=json','-f','null','-'])
    found=probe.stderr[probe.stderr.rfind('{'):probe.stderr.rfind('}')+1]
    m=json.loads(found)
    loud=(f"loudnorm=I=-15:TP=-1.5:LRA=9:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    master=audio/'master.wav'
    run([FF,'-y','-i',str(raw),'-af',loud+',alimiter=limit=0.89:level=false','-ar','48000','-ac','2','-t',f'{END:.3f}',str(master)])
    # Keep QC facts, including values that describe the input to normalization.
    (audio/'loudnorm_measurement.json').write_text(json.dumps(m,indent=2)+"\n")

if __name__ == '__main__':
    make_bed(); mix()
