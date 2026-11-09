#!/usr/bin/env python3
"""Render We bloom in blue with an UNMODIFIED checkout of Chimera.

Usage: CHIMERA_REPO=/path/to/chimera-vocal-synth python3 render.py DIST_DIR
Requires Chimera's release CLI and ffmpeg. Emits JSON, WAV masters and MP3 previews.
# The written lyrics are preserved in `display_lyrics`; `lyrics` adds two vowel
# continuations to "blue" for the three-note ending.
"""
from pathlib import Path
import argparse, json, os, subprocess, wave, math, hashlib, shutil

BPM = 96
T0 = 0.3
# D major; one note per syllable. Rests split the four six-beat vocal phrases.
# "blue" rises D5 -> E5 -> F#5 and holds on the mediant.
PHRASES = [
    ("A sprite holds the greenhouse door.", [
        (62, .5), (64, .5), (66, 1), (67, .5), (69, .5), (67, 1), (62, 2)]),
    ("I bring one seed and you bring two.", [
        (66, 1), (64, .5), (62, .5), (66, .5), (67, .5), (66, 1), (64, .5), (59, 1.5)]),
    ("My copper roots curl round yours.", [
        (62, .5), (64, .5), (66, 1), (69, 1), (67, .5), (66, 1), (62, 1.5)]),
    ("We bloom in blue.", [
        (64, 1), (66, 1.5), (67, .5), (74, 1), (76, 1), (78, 3)]),
]

def main():
    p = argparse.ArgumentParser(); p.add_argument('dist', type=Path); args = p.parse_args()
    repo = Path(os.environ['CHIMERA_REPO']).resolve()
    cli = repo / 'target/release/chimera'
    if not cli.exists():
        subprocess.run(['cargo', 'build', '--release', '-p', 'chimera-cli'], cwd=repo, check=True)
    dist = args.dist.resolve(); audio = dist / 'audio'; audio.mkdir(parents=True, exist_ok=True)
    notes, timeline = [[0, 1]], []
    t = T0
    for phrase, line in PHRASES:
        for midi, beats in line:
            notes.append([midi, beats]); timeline.append({'midi': midi, 'beats': beats, 't0': round(t, 4), 't1': round(t + beats * 60 / BPM, 4)})
            t += beats * 60 / BPM
        notes.append([0, 1]); t += 60 / BPM
    # 26 words become 28 lyric events: copper splits in two, and blue has two holds.
    lyric_words = 'A sprite holds the greenhouse door. I bring one seed and you bring two. My copper roots curl round yours. We bloom in blue ~ ~ .'
    note_names = ['D4','E4','F#4','G4','A4','G4','D4',
                  'F#4','E4','D4','F#4','G4','F#4','E4','B3',
                  'D4','E4','F#4','A4','G4','F#4','D4', 'E4','F#4','G4','D5','E5','F#5']
    assert len(timeline) == len(note_names) == 28, (len(timeline), len(note_names))
    melody = {'bpm': BPM, 't0': T0, 'vibrato': 28, 'lyrics': lyric_words,
              'display_lyrics': [x[0] for x in PHRASES], 'notes': notes,
              'composition': {'key': 'D major', 'meter': '6/4', 'written_words': 26,
                              'lyric_events': 28, 'note_names': note_names}}
    for i, n in enumerate(timeline):
        n['note'] = melody['composition']['note_names'][i]
        n['line'] = 0 if i < 7 else 1 if i < 15 else 2 if i < 22 else 3
        n['melisma'] = i >= 26
    (dist / 'melody.json').write_text(json.dumps(melody, indent=2) + '\n')
    (dist / 'timeline.json').write_text(json.dumps({'bpm': BPM, 't0': T0, 'notes': timeline}, indent=2) + '\n')
    report = {'chimera_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip(), 'voices': {}, 'notes': len(timeline)}
    for body in ['female', 'male', 'child']:
        wav = audio / f'greenhouse-{body}.wav'
        subprocess.run([str(cli), 'render', 'notes', str(dist / 'melody.json'), str(wav), body], cwd=repo, check=True)
        with wave.open(str(wav)) as f:
            frames = f.readframes(f.getnframes()); width = f.getsampwidth(); rate = f.getframerate()
            vals = [int.from_bytes(frames[i:i+width], 'little', signed=True) for i in range(0, len(frames), width)]
            peak = max(abs(v) for v in vals) / 32768
            rms = math.sqrt(sum((v / 32768)**2 for v in vals) / len(vals))
            assert vals and 0 < peak < 1 and rms > .001, (body, peak, rms)
            duration = len(vals) / rate
        mp3 = audio / f'greenhouse-{body}.mp3'
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(wav),
                        '-af', 'highpass=f=70,alimiter=limit=0.94,afade=t=out:st=%.3f:d=0.2' % max(0, duration - .2),
                        '-codec:a', 'libmp3lame', '-b:a', '128k', str(mp3)], check=True)
        report['voices'][body] = {'duration_seconds': round(duration, 3), 'wav_peak': round(peak, 4),
            'wav_rms': round(rms, 4), 'wav_bytes': wav.stat().st_size, 'mp3_bytes': mp3.stat().st_size,
            'sha256_mp3': hashlib.sha256(mp3.read_bytes()).hexdigest()}
    shutil.copy(repo / 'LICENSE', dist / 'CHIMERA-LICENSE.txt')
    (dist / 'render-report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__': main()
