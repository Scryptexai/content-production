#!/usr/bin/env python3
"""Anchor subtitle words to measured voice-active spans.

This is intentionally not presented as ASR/forced alignment. It detects actual
speech/silence in the generated VO, projects the supplied spoken token sequence
through those measured active spans, and gives captions zero lead. The result
cannot run ahead through a detected silent pause, which is the failure corrected
for OS-EP04.

Usage: python3 work/build_vad_alignment.py <slug>
Requires work/<slug>/script_text.txt and case_cfg.py with VO_FILE.
"""
from __future__ import annotations
import importlib.util, json, re, subprocess, sys
from pathlib import Path
import imageio_ffmpeg

ROOT=Path(__file__).resolve().parents[1]
FF=imageio_ffmpeg.get_ffmpeg_exe()

def cfg(slug):
    p=ROOT/'work'/slug/'case_cfg.py'; spec=importlib.util.spec_from_file_location(slug,p)
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def main(slug):
    case=ROOT/'work'/slug; c=cfg(slug); audio=case/c.VO_FILE
    p=subprocess.run([FF,'-i',str(audio),'-af','silencedetect=noise=-39dB:d=0.18','-f','null','-'],capture_output=True,text=True,check=True)
    log=p.stderr
    dur=float(re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',log).group(1))*3600+float(re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',log).group(2))*60+float(re.search(r'Duration: (\d+):(\d+):(\d+\.\d+)',log).group(3))
    starts=[float(x) for x in re.findall(r'silence_start: ([0-9.]+)',log)]
    ends=[float(x) for x in re.findall(r'silence_end: ([0-9.]+)',log)]
    sil=[]
    for s,e in zip(starts,ends): sil.append((s,e))
    # speech spans are complement of measured silence; retain very short runs so
    # words appear only while voice is actually active.
    active=[]; cur=0.0
    for s,e in sil:
        if s>cur+0.035: active.append((cur,s))
        cur=max(cur,e)
    if cur<dur-0.035: active.append((cur,dur))
    active=[x for x in active if x[1]-x[0]>=0.06]
    text=(case/'script_text.txt').read_text(encoding='utf8')
    tokens=re.findall(r"[A-Za-zÀ-ÿ0-9]+(?:[-'][A-Za-zÀ-ÿ0-9]+)?[,.?!]?",text)
    # Convert cumulative speech time to a real timestamp inside measured active
    # spans, then give each token an equal local share (minimum 45 ms).
    total=sum(b-a for a,b in active)
    cumulative=[]; acc=0.0
    for a,b in active:
        cumulative.append((acc,acc+b-a,a,b)); acc+=b-a
    def real(t):
        for lo,hi,a,b in cumulative:
            if t<=hi or (lo,hi,a,b)==cumulative[-1]: return a+max(0,min(b-a,t-lo))
        return active[-1][1]
    words=[]
    for i,w in enumerate(tokens):
        st=real(total*i/len(tokens)); en=real(total*(i+1)/len(tokens))
        # guard punctuation/equal-time boundaries near a span change
        if en<=st: en=st+0.045
        words.append({'word':w,'start':round(st,3),'end':round(en,3)})
    out={'source':'VO internal voice-08; tokens projected through measured VAD active spans (bukan ASR forced alignment)','audio_seconds':round(dur,3),'active_spans':[[round(a,3),round(b,3)] for a,b in active],'words':words}
    (case/'vo_alignment.json').write_text(json.dumps(out,ensure_ascii=False,indent=1)+'\n',encoding='utf8')
    print(f'{slug}: {len(words)} kata, {len(active)} active spans, VO {dur:.3f}s')
if __name__=='__main__': main(sys.argv[1])
