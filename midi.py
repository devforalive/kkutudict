
from midiutil import MIDIFile

# ══════════════════════════════════════════════════════════
#  〈 static 〉 완성본 — 실리카겔 스타일, 약 3분
#  BPM 92 / Key: E minor / 4트랙
#  Intro → Verse1 → PreCh1 → Chorus1 →
#  Verse2 → PreCh2 → Chorus2 → Bridge →
#  Final Chorus → Outro
# ══════════════════════════════════════════════════════════

midi = MIDIFile(4)
BPM  = 92
SW   = 0.06   # 스윙 오프셋 → 흐느적거리는 핵심
B    = 2      # beats per chord slot

for t in range(4):
    midi.addTempo(t, 0, BPM)

# ── 채널 ────────────────────────────────────────────────
CHORD_CH = 0
BASS_CH  = 1
DRUM_CH  = 9   # GM 드럼 채널 (고정)
MEL_CH   = 2

# ── GM 드럼 노트 ─────────────────────────────────────────
KICK  = 36; SNARE = 38; HIHAT = 42
HH_OP = 46; CRASH = 49; RIDE  = 51
TOM_H = 48; TOM_M = 47; TOM_L = 45

# ── 코드 보이싱 ──────────────────────────────────────────
CHORDS = {
    "Em":    [52, 55, 59],
    "Em7":   [52, 55, 59, 62],        # 더 부드럽고 둥근 Em
    "Bm":    [47, 50, 54],
    "C":     [48, 52, 55],
    "Cmaj7": [48, 52, 55, 59],        # 색채감 있는 C
    "G":     [43, 47, 50],
    "Gadd9": [43, 47, 50, 57],        # 열린 느낌의 G
    "Am":    [45, 48, 52],
    "F":     [41, 45, 48],
    "B7":    [47, 51, 54, 57],        # 긴장감 높은 B7
}

BASS_NOTE = {
    "Em": 40, "Em7": 40,              # E2
    "Bm": 47,                         # B2
    "C": 36,  "Cmaj7": 36,           # C2
    "G": 43,  "Gadd9": 43,           # G2
    "Am": 45,                         # A2
    "F": 41,                          # F2
    "B7": 47,                         # B2
}

# ── 헬퍼 ─────────────────────────────────────────────────
def n(track, ch, pitch, t, dur, vol):
    midi.addNote(track, ch, pitch, t, dur, max(1, min(127, int(vol))))

def chord_on(t, name, vol=80, dur=1.8):
    for p in CHORDS.get(name, CHORDS["Em"]):
        n(0, CHORD_CH, p, t, dur, vol)

def bass_on(t, name, style="walk", v=95):
    r = BASS_NOTE.get(name, 40)
    if   style == "sparse":  n(1,BASS_CH,r,t,1.8,v-5)
    elif style == "walk":
        n(1,BASS_CH,r,    t,    0.9, v)
        n(1,BASS_CH,r+7,  t+1.0,0.9, v-17)
    elif style == "active":
        n(1,BASS_CH,r,    t+0.0,0.9, v)
        n(1,BASS_CH,r+12, t+1.0,0.45,v-12)
        n(1,BASS_CH,r+7,  t+1.5,0.45,v-15)
    elif style == "drive":
        n(1,BASS_CH,r,    t+0.0,0.45,v)
        n(1,BASS_CH,r,    t+0.5,0.45,v-10)
        n(1,BASS_CH,r,    t+1.0,0.45,v-5)
        n(1,BASS_CH,r+7,  t+1.5,0.45,v-15)
    elif style == "bridge":  n(1,BASS_CH,r,t,1.5,v-8)

def drums_on(t, style="verse"):
    if style == "silent": return
    elif style == "sparse":
        n(2,DRUM_CH,HIHAT,t,      0.5,40)
        n(2,DRUM_CH,HIHAT,t+1.0,  0.5,35)
        n(2,DRUM_CH,KICK, t,      0.5,62)
    elif style == "build":
        n(2,DRUM_CH,HIHAT,t+0.0,    0.5,52)
        n(2,DRUM_CH,HIHAT,t+0.5+SW, 0.5,40)
        n(2,DRUM_CH,HIHAT,t+1.0,    0.5,52)
        n(2,DRUM_CH,HIHAT,t+1.5+SW, 0.5,38)
        n(2,DRUM_CH,KICK, t,        0.5,80)
        n(2,DRUM_CH,SNARE,t+1.0,    0.5,72)
    elif style == "verse":
        # 스윙 하이햇 — 흐느적거리는 핵심
        n(2,DRUM_CH,HIHAT,t+0.0,    0.5,65)
        n(2,DRUM_CH,HIHAT,t+0.5+SW, 0.5,48)
        n(2,DRUM_CH,HIHAT,t+1.0,    0.5,62)
        n(2,DRUM_CH,HIHAT,t+1.5+SW, 0.5,45)
        n(2,DRUM_CH,KICK, t+0.0,    0.5,100)
        n(2,DRUM_CH,SNARE,t+1.0,    0.5,88)
    elif style == "prechorus":
        n(2,DRUM_CH,HIHAT,t+0.0,0.5,68)
        n(2,DRUM_CH,HIHAT,t+0.5,0.5,55)
        n(2,DRUM_CH,HIHAT,t+1.0,0.5,68)
        n(2,DRUM_CH,HH_OP,t+1.5,0.5,60)   # 4박에 오픈 → 긴장 고조
        n(2,DRUM_CH,KICK, t+0.0,0.5,105)
        n(2,DRUM_CH,SNARE,t+1.0,0.5,92)
    elif style == "chorus":
        # 전부 오픈 하이햇 + 엇박 킥
        for h in [0.0,0.5,1.0,1.5]:
            n(2,DRUM_CH,HH_OP,t+h,0.5,72 if h%1==0 else 55)
        n(2,DRUM_CH,KICK, t+0.0,0.5,112)
        n(2,DRUM_CH,KICK, t+1.5,0.5,92)   # 엇박 킥
        n(2,DRUM_CH,SNARE,t+1.0,0.5,100)
    elif style == "bridge":
        n(2,DRUM_CH,RIDE, t+0.0,0.5,58)
        n(2,DRUM_CH,RIDE, t+1.0,0.5,52)
        n(2,DRUM_CH,KICK, t+0.0,0.5,80)
        n(2,DRUM_CH,SNARE,t+1.0,0.5,70)
    elif style == "bridge_build":
        n(2,DRUM_CH,HIHAT,t+0.0,    0.5,62)
        n(2,DRUM_CH,HIHAT,t+0.5+SW, 0.5,48)
        n(2,DRUM_CH,HIHAT,t+1.0,    0.5,62)
        n(2,DRUM_CH,HH_OP,t+1.5,    0.5,58)
        n(2,DRUM_CH,KICK, t+0.0,    0.5,92)
        n(2,DRUM_CH,SNARE,t+1.0,    0.5,82)
    elif style == "outro":
        n(2,DRUM_CH,HIHAT,t,    0.5,38)
        n(2,DRUM_CH,KICK, t,    0.5,65)
        n(2,DRUM_CH,SNARE,t+1.0,0.5,52)

def fill(t, style="snare"):
    if style == "snare":
        for i,off in enumerate([0.5,0.75,1.0,1.25,1.5,1.75]):
            n(2,DRUM_CH,SNARE,t+off,0.25,85+i*4)
    elif style == "crash":
        n(2,DRUM_CH,CRASH,t,0.5,118)
    elif style == "tom":
        n(2,DRUM_CH,TOM_H,t+0.5, 0.25,90)
        n(2,DRUM_CH,TOM_M,t+0.75,0.25,90)
        n(2,DRUM_CH,TOM_L,t+1.0, 0.25,90)
        for i,off in enumerate([1.25,1.5,1.75]):
            n(2,DRUM_CH,SNARE,t+off,0.25,92+i*5)

def mel(t, pattern, vol=78):
    for (pitch, off, dur) in pattern:
        n(3, MEL_CH, pitch, t+off, dur, vol)

# ══════════════════════════════════════════════════════════
# 멜로디 패턴 (2박 단위, E minor)
# E(64) F#(66) G(67) A(69) B(71) C(72) D(74) E(76)
# ══════════════════════════════════════════════════════════

# [Verse 1] — 흐르듯 내려오는, 멍한 느낌
V1 = {
    "Em":  [(76,0.0,0.8),(74,0.8,0.5),(71,1.3,0.7)],  # E5 D5 B4
    "Bm":  [(71,0.0,1.1),(69,1.1,0.9)],               # B4 A4
    "C":   [(67,0.0,1.5),(69,1.5,0.5)],               # G4 A4
    "G":   [(71,0.0,0.8),(67,0.8,1.2)],               # B4 G4
}

# [Verse 2] — 약간 더 불안하게, 역방향/싱코페이션
V2 = {
    "Em":  [(74,0.0,0.5),(76,0.5,0.8),(74,1.3,0.7)],  # D5 E5 D5
    "Bm":  [(71,0.0,0.5),(69,0.5,0.5),(66,1.0,1.0)],  # B4 A4 F#4
    "C":   [(67,0.5,1.0),(69,1.5,0.5)],               # (쉬고) G4 A4
    "G":   [(67,0.0,0.8),(71,0.8,1.2)],               # G4 B4 (상승)
}

# [Pre-Chorus] — 점점 올라가며 긴장
PC = {
    "Am":  [(69,0.0,0.5),(72,0.5,1.5)],               # A4 C5 (도약)
    "F":   [(72,0.0,0.8),(74,0.8,1.2)],               # C5 D5 (계속 상승)
    "Am2": [(74,0.0,0.5),(72,0.5,0.5),(71,1.0,1.0)],  # D5 C5 B4 (정점→하강)
    "B7":  [(71,0.0,2.0)],                             # B4 홀드 (긴장 유지)
}

# [Chorus] — 정점, 불안정하게 떨어지는
CH = {
    "Am":  [(69,0.0,0.5),(72,0.5,0.5),(74,1.0,1.0)],  # A4 C5 D5 (soar)
    "F":   [(72,0.0,0.8),(69,0.8,1.2)],               # C5 A4
    "Bm":  [(66,0.0,0.5),(64,0.5,0.5),(62,1.0,1.0)], # F#4 E4 D4 (불협 하강)
    "Em":  [(64,0.0,2.0)],                             # E4 홀드 (허탈한 해결)
}

# [Bridge part A] — 조각난, 공간감
BRA = {
    "C":   [(72,0.0,1.0),(71,1.0,1.0)],               # C5 B4
    "G":   [(67,0.0,2.0)],                             # G4 홀드
    "Am":  [(69,0.0,0.5),(67,0.5,1.5)],               # A4 G4
    "Em":  [(64,0.0,2.0)],                             # E4 홀드
}

# [Bridge part B] — 반음계로 긴장 극대화
BRB = {
    "C":   [(67,0.5,1.5)],                             # G4 (늦게 등장)
    "G":   [(74,0.0,2.0)],                             # D5 (한 옥타브 위)
    "B7a": [(62,0.0,0.5),(63,0.5,1.5)],               # D4 Eb4 (반음↑ 불협!)
    "B7b": [(71,0.0,2.0)],                             # B4 홀드
}

# [Outro] — 흩어지는 파편들
OT = {
    "Em":  [(64,0.0,1.4),(62,1.4,0.6)],               # E4 D4 (흘러내림)
    "Em2": [(64,0.5,1.5)],                             # 늦게 들어오는 E4
    "Bm":  [(62,0.0,2.0)],                             # D4
    "B7":  [(62,0.0,2.0)],                             # D4 긴장
}

# ══════════════════════════════════════════════════════════
#  곡 구조  (140 슬롯 × 1.304초 ≈ 182.5초 ≈ 3분 2초)
# ══════════════════════════════════════════════════════════

time = 0

# ─────────────────────────────────────────────
# [INTRO] 16 슬롯 ≈ 20.9초
# Phase 1: 베이스만 (고요한 시작)
for ch in ["Em","Em","Em","Em"]:
    bass_on(time, ch, "sparse", 65)
    drums_on(time, "sparse")
    time += B

# Phase 2: 베이스 + 드럼 빌드업
for ch in ["Em","Bm","C","G"]:
    bass_on(time, ch, "walk", 78)
    drums_on(time, "build")
    time += B

# Phase 3: 코드 희미하게 등장
for ch in ["Em","Bm","C","G","Em","Bm","C","G"]:
    chord_on(time, ch, 55, 1.7)
    bass_on(time, ch, "walk", 83)
    drums_on(time, "build")
    time += B

# ─────────────────────────────────────────────
# [VERSE 1] 16 슬롯 ≈ 20.9초
fill(time-B, "snare")
fill(time,   "crash")

for _ in range(4):
    for ch in ["Em","Bm","C","G"]:
        chord_on(time, ch, 72)
        bass_on(time,  ch, "walk")
        drums_on(time, "verse")
        mel(time, V1[ch], 68)
        time += B

# ─────────────────────────────────────────────
# [PRE-CHORUS 1] 8 슬롯 ≈ 10.4초
fill(time-B, "snare")

for _ in range(2):
    for ch,mk in [("Am","Am"),("F","F"),("Am","Am2"),("B7","B7")]:
        chord_on(time, ch, 83)
        bass_on(time,  ch, "active")
        drums_on(time, "prechorus")
        mel(time, PC[mk], 78)
        time += B

# ─────────────────────────────────────────────
# [CHORUS 1] 16 슬롯 ≈ 20.9초
fill(time-B, "tom")
fill(time,   "crash")

for _ in range(4):
    for ch,mk in [("Am","Am"),("F","F"),("Bm","Bm"),("Em","Em")]:
        chord_on(time, ch, 95)
        bass_on(time,  ch, "drive")
        drums_on(time, "chorus")
        mel(time, CH[mk], 88)
        time += B

# ─────────────────────────────────────────────
# [VERSE 2] 16 슬롯 ≈ 20.9초  (더 풍성한 코드 보이싱)
fill(time-B, "snare")

for _ in range(4):
    for ch,vch in [("Em","Em7"),("Bm","Bm"),("C","Cmaj7"),("G","Gadd9")]:
        chord_on(time, vch, 78)
        bass_on(time,  ch,  "walk")
        drums_on(time, "verse")
        mel(time, V2[ch], 74)
        time += B

# ─────────────────────────────────────────────
# [PRE-CHORUS 2] 8 슬롯 ≈ 10.4초  (더 강하게)
fill(time-B, "snare")

for _ in range(2):
    for ch,mk in [("Am","Am"),("F","F"),("Am","Am2"),("B7","B7")]:
        chord_on(time, ch, 90)
        bass_on(time,  ch, "active")
        drums_on(time, "prechorus")
        mel(time, PC[mk], 85)
        time += B

# ─────────────────────────────────────────────
# [CHORUS 2] 16 슬롯 ≈ 20.9초
fill(time-B, "tom")
fill(time,   "crash")

for _ in range(4):
    for ch,mk in [("Am","Am"),("F","F"),("Bm","Bm"),("Em","Em")]:
        chord_on(time, ch, 100)
        bass_on(time,  ch, "drive", 100)
        drums_on(time, "chorus")
        mel(time, CH[mk], 93)
        time += B

# ─────────────────────────────────────────────
# [BRIDGE] 16 슬롯 ≈ 20.9초  (분위기 전환 — 라이드+공간)
fill(time-B, "snare")

# Part A: C G Am Em × 2 (해체, 낯선 공간)
for ch,mk in [("C","C"),("G","G"),("Am","Am"),("Em","Em")] * 2:
    chord_on(time, ch, 65)
    bass_on(time,  ch, "bridge")
    drums_on(time, "bridge")
    mel(time, BRA[mk], 62)
    time += B

# Part B: C G B7 B7 × 2 (긴장 고조, 반음계 멜로디)
for ch,mk in [("C","C"),("G","G"),("B7","B7a"),("B7","B7b")] * 2:
    chord_on(time, ch, 75)
    bass_on(time,  ch, "bridge")
    drums_on(time, "bridge_build")
    mel(time, BRB.get(mk, BRB["B7b"]), 70)
    time += B

# ─────────────────────────────────────────────
# [FINAL CHORUS] 16 슬롯 ≈ 20.9초  (최대 강도)
fill(time-B, "tom")
fill(time,   "crash")

for _ in range(4):
    for ch,mk in [("Am","Am"),("F","F"),("Bm","Bm"),("Em","Em")]:
        chord_on(time, ch, 108)
        bass_on(time,  ch, "drive", 105)
        drums_on(time, "chorus")
        mel(time, CH[mk], 100)
        time += B

# ─────────────────────────────────────────────
# [OUTRO] 12 슬롯 ≈ 15.6초  (점점 흩어짐)
fill(time-B, "snare")

outro_seq = [
    ("Em","Em"),  ("Em","Em"),  ("Em","Em"),  ("Bm","Bm"),
    ("Em","Em"),  ("Em","Em2"), ("B7","B7"),  ("Em","Em"),
    ("Em","Em2"), ("Em","Em"),  ("Em","Em2"), ("Em","Em"),
]
for idx,(ch,mk) in enumerate(outro_seq):
    fade = max(80 - idx*7, 20)
    chord_on(time, ch, fade, 1.5)
    bass_on(time,  ch, "sparse", max(fade, 25))
    drums_on(time, "outro")
    if mk in OT:
        mel(time, OT[mk], max(fade-10, 14))
    time += B

# ══════════════════════════════════════════════════════════
out = "./static.master.mid"
with open(out,"wb") as f:
    midi.writeFile(f)

sec = time * (60/BPM)
slots = time // B
print(f"✅  완성: {out}")
print(f"BPM {BPM}  |  총 {sec:.1f}초 ({sec/60:.2f}분)  |  {slots}슬롯")
print("""
구간별 구성:
  [Intro]         16슬롯  ≈ 20.9초
  [Verse 1]       16슬롯  ≈ 20.9초
  [Pre-Chorus 1]   8슬롯  ≈ 10.4초
  [Chorus 1]      16슬롯  ≈ 20.9초
  [Verse 2]       16슬롯  ≈ 20.9초
  [Pre-Chorus 2]   8슬롯  ≈ 10.4초
  [Chorus 2]      16슬롯  ≈ 20.9초
  [Bridge]        16슬롯  ≈ 20.9초
  [Final Chorus]  16슬롯  ≈ 20.9초
  [Outro]         12슬롯  ≈ 15.6초
  ──────────────────────────────────
  합계            140슬롯 ≈ 182.5초
""")
