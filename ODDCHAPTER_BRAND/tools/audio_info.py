"""
audio_info.py — read MPEG audio duration without ffprobe.

ffprobe is not installed on this host, so duration is parsed from the stream itself:
ID3v2 tag is skipped, the first frame header gives sample rate, and either the Xing/Info
frame count (VBR) or a full frame walk (CBR) gives the length. Prints one line per file.

Usage: python3 tools/audio_info.py 08_AUDIO/assets/*.mp3
"""
import sys
from pathlib import Path

BITRATES = {
    (1, 1): [0, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448],
    (1, 2): [0, 32, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 384],
    (1, 3): [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320],
}
BITRATES[(2, 1)] = BITRATES[(1, 2)]
BITRATES[(2, 2)] = BITRATES[(1, 3)]
# MPEG2 / MPEG2.5 Layer III uses its own table — half-rate indices, not the MPEG1 one
BITRATES[(2, 3)] = [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160]
RATES = {3: [44100, 48000, 32000], 2: [22050, 24000, 16000], 0: [11025, 12000, 8000]}


def parse_wav(path):
    """RIFF/WAVE header: byte rate at 28, data size at 40 → exact duration."""
    b = Path(path).read_bytes()[:64]
    if b[:4] != b"RIFF" or b[8:12] != b"WAVE":
        return None
    byte_rate = int.from_bytes(b[28:32], "little")
    channels = int.from_bytes(b[22:24], "little")
    rate = int.from_bytes(b[24:28], "little")
    size = Path(path).stat().st_size
    i = b.find(b"data")
    data_len = int.from_bytes(Path(path).read_bytes()[i+4:i+8], "little") if i >= 0 else size - 44
    if not byte_rate:
        return None
    return dict(duration=data_len / byte_rate, rate=rate, bitrate=byte_rate * 8 // 1000,
                channels=channels, mode="WAV/PCM", frames=0, byte_est=data_len / byte_rate)


def parse(path):
    if Path(path).suffix.lower() == ".wav":
        return parse_wav(path)
    data = Path(path).read_bytes()
    i = 0
    if data[:3] == b"ID3":
        size = (data[6] << 21) | (data[7] << 14) | (data[8] << 7) | data[9]
        i = 10 + size
    start = None
    for j in range(i, min(len(data) - 4, i + 200000)):
        if data[j] == 0xFF and (data[j + 1] & 0xE0) == 0xE0:
            start = j
            break
    if start is None:
        return None
    h = data[start:start + 4]
    ver = (h[1] >> 3) & 0x03          # 3 = MPEG1, 2 = MPEG2, 0 = MPEG2.5
    layer = 4 - ((h[1] >> 1) & 0x03)  # 1, 2, 3
    br_i = (h[2] >> 4) & 0x0F
    sr_i = (h[2] >> 2) & 0x03
    pad = (h[2] >> 1) & 0x01
    chan = 1 if ((h[3] >> 6) & 0x03) == 3 else 2
    ver_key = 1 if ver == 3 else 2
    table = BITRATES.get((ver_key, layer))
    if not table or sr_i == 3 or br_i in (0, 15):
        return None
    bitrate = table[br_i] * 1000
    rate = RATES[ver][sr_i]
    spf = 1152 if ver == 3 else 576

    # Xing / Info header → exact frame count
    side = (17 if chan == 1 else 32) if ver == 3 else (9 if chan == 1 else 17)
    xing_at = start + 4 + side
    if data[xing_at:xing_at + 4] in (b"Xing", b"Info"):
        flags = int.from_bytes(data[xing_at + 4:xing_at + 8], "big")
        if flags & 0x0001:
            frames = int.from_bytes(data[xing_at + 8:xing_at + 12], "big")
            return dict(duration=frames * spf / rate, rate=rate, bitrate=bitrate,
                        channels=chan, mode="Info/Xing header", frames=frames,
                        byte_est=(len(data) - start) * 8 / bitrate)

    # chain-validated frame walk: a frame counts only if the next sync lands exactly on its end
    pos = start
    frames = 0
    spf_total = 0.0
    brs = set()
    while pos + 4 <= len(data):
        if data[pos] != 0xFF or (data[pos + 1] & 0xE0) != 0xE0:
            pos += 1
            continue
        fh = data[pos:pos + 4]
        b_i, s_i = (fh[2] >> 4) & 0x0F, (fh[2] >> 2) & 0x03
        p_bit = (fh[2] >> 1) & 0x01
        if s_i == 3 or b_i in (0, 15):
            pos += 1
            continue
        f_br = table[b_i] * 1000
        f_rate = RATES[ver][s_i]
        f_spf = 1152 if ver == 3 else 576
        length = int(f_spf / 8 * f_br / f_rate) + p_bit
        nxt = pos + length
        chained = (nxt + 1 >= len(data)) or (data[nxt] == 0xFF and (data[nxt + 1] & 0xE0) == 0xE0)
        if chained and length > 4:
            frames += 1
            spf_total += f_spf
            brs.add(f_br)
            pos = nxt
        else:
            pos += 1
    dur = spf_total / rate
    audio_bytes = len(data) - start
    mode = "VBR" if len(brs) > 1 else "CBR"
    return dict(duration=dur, rate=rate, bitrate=bitrate, channels=chan,
                mode=f"{mode} · {len(brs)} rate(s)", frames=frames,
                byte_est=audio_bytes * 8 / bitrate)


if __name__ == "__main__":
    for f in sys.argv[1:]:
        info = parse(f)
        if not info:
            print(f"{f}: could not parse")
            continue
        size = Path(f).stat().st_size / 1024
        eff = (Path(f).stat().st_size * 8) / info["duration"] / 1000
        bpf = Path(f).stat().st_size / max(info["frames"], 1)
        print(f"{Path(f).name:30} {info['duration']:6.2f} s  "
              f"{info['frames']:4d} frames @ {bpf:5.1f} B/frame  "
              f"{info['rate']} Hz  {info['channels']} ch  "
              f"~{eff:5.1f} kbps  {size:5.1f} KB  {info['mode']}")
