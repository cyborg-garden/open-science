"""Exercise the real greenhouse page over HTTP with headless Chromium.

From the repository root, with Playwright's Chromium installed:
  uv run --with playwright python scripts/chimera-greenhouse/qa.py
The test serves the actual page and audio with byte-range support. Set
CHIMERA_QA_OUTPUT to choose a screenshot directory. QA_MUTATION=broken-sync
or duplicate-loop injects a regression that the suite must reject.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import json
import os
import re
import tempfile
import time
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2] / 'docs/experiments/chimera-greenhouse'
OUTPUT = Path(os.environ.get('CHIMERA_QA_OUTPUT', tempfile.mkdtemp(prefix='chimera-qa-')))
OUTPUT.mkdir(parents=True, exist_ok=True)

class QuietHandler(SimpleHTTPRequestHandler):
    """Static handler with the byte-range support media seeking requires."""
    def send_head(self):
        byte_range = self.headers.get('Range')
        if not byte_range:
            return super().send_head()
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()
        try:
            file = open(path, 'rb')
        except OSError:
            self.send_error(404, 'File not found')
            return None
        size = os.fstat(file.fileno()).st_size
        match = re.fullmatch(r'bytes=(\d+)-(\d*)', byte_range)
        if not match:
            file.close()
            self.send_error(400, 'Unsupported Range header')
            return None
        start = int(match.group(1))
        end = int(match.group(2)) if match.group(2) else size - 1
        if start >= size or end < start:
            file.close()
            self.send_response(416)
            self.send_header('Content-Range', f'bytes */{size}')
            self.end_headers()
            return None
        end = min(end, size - 1)
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(end - start + 1))
        self.end_headers()
        file.seek(start)
        return _LimitedFile(file, end - start + 1)

    def log_message(self, *_args):
        pass

    def copyfile(self, source, outputfile):
        try:
            return super().copyfile(source, outputfile)
        except (BrokenPipeError, ConnectionResetError):
            # Browsers cancel obsolete media responses during rapid voice changes.
            return None

class DelayedTimelineHandler(QuietHandler):
    def do_GET(self):
        if self.path == '/timeline.json':
            time.sleep(0.7)
        super().do_GET()

class DelayedVoiceHandler(QuietHandler):
    def do_GET(self):
        if self.path.endswith('.mp3'):
            time.sleep(0.8)
        super().do_GET()

class FailedTimelineHandler(QuietHandler):
    def do_GET(self):
        if self.path == '/timeline.json':
            time.sleep(0.7)
            self.send_error(503)
            return
        super().do_GET()

class FailedVoiceHandler(QuietHandler):
    def do_GET(self):
        if self.path == '/audio/greenhouse-male.mp3':
            time.sleep(0.8)
            self.send_error(503)
            return
        super().do_GET()

class _LimitedFile:
    def __init__(self, file, remaining):
        self.file = file
        self.remaining = remaining
    def read(self, size=-1):
        if self.remaining <= 0:
            return b''
        if size < 0 or size > self.remaining:
            size = self.remaining
        data = self.file.read(size)
        self.remaining -= len(data)
        return data
    def close(self):
        self.file.close()

class MutationHandler(QuietHandler):
    def do_GET(self):
        mutation = os.environ.get('QA_MUTATION')
        if mutation and self.path in ('/', '/index.html'):
            body = (ROOT / 'index.html').read_text()
            if mutation == 'duplicate-loop':
                needle = "if(pending.resume)audio.play().then(setPlayIcon)"
                replacement = "if(pending.resume)audio.play().then(() => { setPlayIcon(); requestAnimationFrame(tick); })"
            elif mutation == 'broken-sync':
                needle = 'const nextTime = currentSongTime(), nextPlaying = isSinging();'
                replacement = 'const nextTime = 0, nextPlaying = isSinging();'
            else:
                raise ValueError(mutation)
            assert needle in body
            body = body.replace(needle, replacement, 1).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            if self.command != 'HEAD':
                self.wfile.write(body)
            return
        super().do_GET()

server = ThreadingHTTPServer(('127.0.0.1', 0), partial(MutationHandler, directory=str(ROOT)))
thread = Thread(target=server.serve_forever, daemon=True)
thread.start()
url = f'http://127.0.0.1:{server.server_port}/'
results = {}
errors = []
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1280, 'height': 900})
        page.on('pageerror', lambda error: errors.append(str(error)))
        response = page.goto(url, wait_until='networkidle')
        assert response and response.ok, f'page status: {response.status if response else None}'
        page.wait_for_function('head.notes.length === 28')
        assert page.locator('.score-note').count() == 28
        results['timeline_and_score'] = {'notes': 28, 'score_rects': 28}
        contrast = page.evaluate('''() => {
          function luminance(rgb) {
            const c = rgb.match(/[\\d.]+/g).slice(0,3).map(Number).map(v => v/255).map(v => v <= .04045 ? v/12.92 : ((v+.055)/1.055)**2.4);
            return c[0]*.2126+c[1]*.7152+c[2]*.0722;
          }
          function ratio(a,b) { const [hi,lo]=[luminance(a),luminance(b)].sort((x,y)=>y-x); return (hi+.05)/(lo+.05); }
          const paper = getComputedStyle(document.body).backgroundColor;
          const white = getComputedStyle(document.querySelector('.score-box')).backgroundColor;
          const muted = getComputedStyle(document.querySelector('.lede')).color;
          const copper = getComputedStyle(document.querySelector('.eyebrow')).color;
          const lyric = getComputedStyle(document.querySelector('.hero h1 em')).color;
          const lyricNum = getComputedStyle(document.querySelector('.lyric .num')).color;
          const forest = getComputedStyle(document.querySelector('.player')).backgroundColor;
          const playSub = getComputedStyle(document.querySelector('.play-sub')).color;
          const voiceNote = getComputedStyle(document.querySelector('.player-note')).color;
          const scoreLabels = [...document.querySelectorAll('#score text')].map(el => ratio(getComputedStyle(el).fill, white));
          return {muted: ratio(muted,paper), copper: ratio(copper,white), lyric: ratio(lyric,paper), lyricNum: ratio(lyricNum,paper), playSub: ratio(playSub,forest), voiceNote: ratio(voiceNote,forest), scoreLabels};
        }''')
        assert all(v >= 4.5 for v in contrast.values() if isinstance(v, float)), contrast
        assert len(contrast['scoreLabels']) >= 8 and all(v >= 4.5 for v in contrast['scoreLabels']), contrast
        assert contrast['copper'] >= 3, contrast
        results['contrast'] = contrast
        vowel_shapes = page.evaluate('[...Array(head.notes.length)].map((_,i) => head.vowelAt(i).jaw)')
        assert len(vowel_shapes) == 28 and all(v > 0 for v in vowel_shapes), vowel_shapes
        results['vowel_shapes'] = {'mapped_notes': len(vowel_shapes), 'open_jaw_values': sorted(set(round(v,2) for v in vowel_shapes))}
        # A paused frame is a snapshot of the current sung note, never a forced rest mouth.
        page.locator('#seek').evaluate('(el) => { el.value = "1.04"; el.dispatchEvent(new Event("input", {bubbles: true})); }')
        page.wait_for_function('Math.abs(audio.currentTime - 1.04) < 0.15 && Math.abs(head.currentTime - 1.04) < 0.15')
        page.wait_for_timeout(750)
        paused_shape = page.evaluate('({note: head.activeNoteUsed?.note.note, jaw: head._jaw, lipRound: head._lipRound, time: head.currentTime, playing: head.playing})')
        assert paused_shape['note'] == 'F#4' and paused_shape['jaw'] == 0.45 and paused_shape['lipRound'] == 0.6, paused_shape
        results['paused_note_shape'] = paused_shape
        # Render geometry for every body and measure the projected cranium bounds.
        for voice in ['female', 'male', 'child']:
            page.locator(f'.voice[data-voice="{voice}"]').click()
            page.wait_for_function(f'activeVoice === "{voice}" && audio.readyState >= 1')
            page.evaluate('window.scrollTo(0, 0)')
            page.wait_for_function('head.visible === true')
            bounds = page.evaluate('''() => {
              // Measure real canvas paths, not nominal geometry or layout guesses.
              const context = head.ctx, originalMove = context.moveTo, originalLine = context.lineTo;
              const originalArc = context.arc, originalStroke = context.stroke;
              let points = [], current = [];
              context.moveTo = function(x, y) { if (current.length) points.push(...current); current = [[x, y]]; return originalMove.call(this, x, y); };
              context.lineTo = function(x, y) { current.push([x, y]); return originalLine.call(this, x, y); };
              context.arc = function(x, y, r) { points.push([x-r,y-r],[x+r,y+r]); return originalArc.apply(this, arguments); };
              context.stroke = function() { if (current.length) points.push(...current); current = []; return originalStroke.call(this); };
              const originalDraw = head.draw.bind(head);
              head.draw = function() { points = []; current = []; originalDraw(0); };
              head._snapshotKey = null;
              head.drawNow();
              head.draw = originalDraw;
              context.moveTo = originalMove; context.lineTo = originalLine; context.arc = originalArc; context.stroke = originalStroke;
              const xs = points.map(p => p[0]), ys = points.map(p => p[1]);
              return {voice: head.voice, top: Math.min(...ys), bottom: Math.max(...ys),
                left: Math.min(...xs), right: Math.max(...xs), width: head.w, height: head.h, points: points.length};
            }''')
            assert bounds['top'] >= 8 and bounds['bottom'] <= bounds['height'] - 8 and bounds['left'] >= 8 and bounds['right'] <= bounds['width'] - 8, bounds
            results[f'geometry_{voice}'] = bounds
            page.locator('.hero-art').screenshot(path=str(OUTPUT / f'head-{voice}.png'))
        # Idle after metadata restoration must not start the head's rendering loop.
        idle_draws = page.evaluate('''() => new Promise(resolve => {
          const original = head.draw.bind(head);
          let count = 0;
          head.draw = (...args) => { count++; return original(...args); };
          setTimeout(() => { head.draw = original; resolve({count, raf: head._raf, playing: head.playing}); }, 450);
        })''')
        assert idle_draws['count'] == 0 and idle_draws['raf'] == 0, idle_draws
        results['idle_rendering'] = idle_draws
        # A visible, playing head stops rendering offscreen and resumes when visible again.
        page.locator('#play').click()
        page.wait_for_function('!audio.paused && audio.currentTime > 0.25 && head._raf > 0')
        page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        page.wait_for_function('head.visible === false && head._raf === 0')
        page.evaluate('window.scrollTo(0, 0)')
        page.wait_for_function('head.visible === true && head._raf > 0')
        page.locator('#play').click()
        page.wait_for_function('audio.paused && !head.playing && playerFrame === 0')
        results['offscreen_rendering'] = 'stopped and resumed'
        # Return to the original playback scenario.
        page.locator('#seek').evaluate('(el) => { el.value = "0"; el.dispatchEvent(new Event("input", {bubbles: true})); }')
        page.wait_for_function('Math.abs(audio.currentTime) < 0.15 && Math.abs(head.currentTime) < 0.15')
        results['initial'] = page.evaluate('({voice: head.voice, time: head.currentTime, playing: head.playing, jaw: head._jaw})')
        page.locator('#play').click()
        page.wait_for_function('!audio.paused && audio.currentTime > 0.25')
        page.wait_for_timeout(650)
        results['playing'] = page.evaluate('({audioTime: audio.currentTime, headTime: head.currentTime, headPlaying: head.playing, jaw: head._jaw, frame: playerFrame})')
        assert results['playing']['headPlaying'] is True
        assert abs(results['playing']['audioTime'] - results['playing']['headTime']) < 0.15
        assert results['playing']['jaw'] > 0.05
        page.locator('#play').click()
        page.wait_for_function('audio.paused && !head.playing && playerFrame === 0')
        results['paused'] = page.evaluate('({audioTime: audio.currentTime, headTime: head.currentTime, headPlaying: head.playing, frame: playerFrame})')
        assert results['paused']['headPlaying'] is False
        assert abs(results['paused']['audioTime'] - results['paused']['headTime']) < 0.15
        assert results['paused']['frame'] == 0
        # Seek directly to the final held F#5 (16.55 to 18.425 seconds).
        page.locator('#seek').evaluate('(el) => { el.value = "16.8"; el.dispatchEvent(new Event("input", {bubbles: true})); }')
        try:
            page.wait_for_function('Math.abs(audio.currentTime - 16.8) < 0.15 && Math.abs(head.currentTime - 16.8) < 0.15', timeout=5000)
        except Exception:
            print('SEEK DIAGNOSTIC', page.evaluate('''({readyState: audio.readyState, networkState: audio.networkState,
              currentSrc: audio.currentSrc, currentTime: audio.currentTime, headTime: head.currentTime,
              duration: audio.duration, paused: audio.paused, error: audio.error && {code: audio.error.code, message: audio.error.message},
              seekable: [...Array(audio.seekable.length)].map((_,i)=>[audio.seekable.start(i),audio.seekable.end(i)]),
              buffered: [...Array(audio.buffered.length)].map((_,i)=>[audio.buffered.start(i),audio.buffered.end(i)]),
              slider: {value: seek.value, max: seek.max}, pageErrors: window.__qaErrors || []})'''), flush=True)
            raise
        results['seek'] = page.evaluate('({audioTime: audio.currentTime, headTime: head.currentTime, note: head.noteAt(head.currentTime)?.note.note})')
        assert page.locator('#time').inner_text().startswith('0:16 /'), page.locator('#time').inner_text()

        assert abs(results['seek']['audioTime'] - 16.8) < 0.15
        assert abs(results['seek']['headTime'] - 16.8) < 0.15
        assert results['seek']['note'] == 'F#5'
        page.evaluate('window.scrollTo(0, 0)')
        page.wait_for_function('head.visible && head.activeNoteUsed?.note.note === "F#5" && head._jaw > 0.15')
        assert page.evaluate('head._jaw') > 0.15
        assert page.evaluate('head.activeNoteUsed?.note.note') == 'F#5'
        assert 'F#5' in page.locator('#head-status').inner_text()
        assert 'paused' in page.locator('#head-status').inner_text()
        # Exercise all three voices with the real audio files and inspect the head.
        for voice in ['female', 'male', 'child']:
            page.locator(f'.voice[data-voice="{voice}"]').click()
            page.wait_for_function(f'activeVoice === "{voice}" && audio.readyState >= 1')
            page.wait_for_timeout(300)
            info = page.evaluate('({voice: head.voice, src: audio.currentSrc, scale: head.voiceScale, pitch: head.voicePitchMult, time: head.currentTime})')
            assert info['voice'] == voice
            assert info['src'].endswith(f'greenhouse-{voice}.mp3')
            assert abs(info['time'] - 16.8) < 0.15
            results[f'voice_{voice}'] = info
        page.locator('#play').click()
        page.wait_for_function('!audio.paused && audio.currentTime > 16.8')
        page.wait_for_timeout(400)
        page.locator('.voice[data-voice="female"]').click()
        page.wait_for_function('activeVoice === "female" && !audio.paused && audio.currentTime > 16.8')
        page.wait_for_timeout(350)
        loop_counts = page.evaluate('''() => new Promise(resolve => {
          let ticks = 0, displayed = 0;
          const originalTick = tick;
          tick = function() { ticks++; return originalTick(); };
          function displayFrame() {
            displayed++;
            if (displayed === 24) resolve({ticks, displayed});
            else requestAnimationFrame(displayFrame);
          }
          requestAnimationFrame(displayFrame);
        })''')
        assert loop_counts['ticks'] <= loop_counts['displayed'] + 1, loop_counts
        results['single_loop'] = loop_counts
        results['switch_during_play'] = page.evaluate('({voice: head.voice, audioTime: audio.currentTime, headTime: head.currentTime, playing: head.playing, frame: playerFrame})')
        assert results['switch_during_play']['playing'] is True
        assert results['switch_during_play']['frame'] > 0
        assert abs(results['switch_during_play']['audioTime'] - results['switch_during_play']['headTime']) < 0.15
        page.locator('#play').click()
        page.wait_for_function('audio.paused')
        page.wait_for_function('head.playing === false && playerFrame === 0')
        page.locator('.voice[data-voice="female"]').click()
        page.wait_for_function('activeVoice === "female" && audio.readyState >= 1')
        page.wait_for_timeout(200)
        page.locator('#play').click()
        page.wait_for_function('!audio.paused && audio.currentTime > 0.25')
        page.wait_for_timeout(500)
        page.screenshot(path=str(OUTPUT / 'desktop-singing.png'), full_page=True)
        page.locator('#play').click()
        page.wait_for_function('audio.paused')
        page.wait_for_function('head.playing === false && playerFrame === 0')
        page.locator('.voice[data-voice="female"]').click()
        page.wait_for_function('activeVoice === "female" && audio.readyState >= 1')
        page.wait_for_timeout(200)
        page.evaluate('() => { seek.value = "16.8"; seek.dispatchEvent(new Event("input", {bubbles: true})); }')
        page.wait_for_function('Math.abs(audio.currentTime - 16.8) < 0.15 && Math.abs(head.currentTime - 16.8) < 0.15')
        page.wait_for_timeout(200)
        page.screenshot(path=str(OUTPUT / 'desktop.png'), full_page=True)
        results['desktop_overflow'] = page.evaluate('document.documentElement.scrollWidth > innerWidth')
        mobile = browser.new_page(viewport={'width': 390, 'height': 844})
        mobile.on('pageerror', lambda error: errors.append('mobile: ' + str(error)))
        mobile.goto(url, wait_until='networkidle')
        mobile.wait_for_function('head.notes.length === 28')
        mobile.locator('#play').click()
        mobile.wait_for_function('!audio.paused && audio.currentTime > 0.25')
        mobile.wait_for_timeout(500)
        mobile.screenshot(path=str(OUTPUT / 'mobile-singing.png'), full_page=True)
        mobile.locator('#play').click()
        mobile.wait_for_function('audio.paused')
        mobile.wait_for_function('head.playing === false && playerFrame === 0')
        results['mobile_overflow'] = mobile.evaluate('document.documentElement.scrollWidth > innerWidth')
        assert not results['desktop_overflow']
        assert not results['mobile_overflow']
        mobile.screenshot(path=str(OUTPUT / 'mobile.png'), full_page=True)
        reduced = browser.new_page(viewport={'width': 390, 'height': 844}, reduced_motion='reduce')
        reduced.on('pageerror', lambda error: errors.append('reduced: ' + str(error)))
        reduced.goto(url, wait_until='networkidle')
        reduced.wait_for_function('head.notes.length === 28')
        assert reduced.evaluate('head._raf') == 0
        results['reduced_motion'] = {'initial_raf': 0}
        reduced.locator('#play').click()
        reduced.wait_for_function('!audio.paused && audio.currentTime > 0.25')
        reduced.wait_for_timeout(500)
        assert reduced.evaluate('head._jaw') > 0.05
        assert reduced.evaluate('head.activeNoteUsed !== null')
        reduced_draws = reduced.evaluate('''() => new Promise(resolve => {
          const original = head.draw.bind(head);
          let count = 0, samples = [];
          head.draw = (...args) => { count++; samples.push({time: audio.currentTime, note: head.noteAt(head.currentTime)?.index, visible: head.visible, reduced: head.reducedMotion.matches, snapshot: head._snapshotKey}); return original(...args); };
          setTimeout(() => { head.draw = original; resolve({count, samples}); }, 350);
        })''')
        print('REDUCED DRAWS', reduced_draws, reduced.evaluate('({time: audio.currentTime, visible: head.visible, reduced: head.reducedMotion.matches, snapshot: head._snapshotKey})'), flush=True)
        assert reduced_draws['count'] <= 2, reduced_draws
        results['reduced_motion']['draws_in_350ms'] = reduced_draws['count']
        reduced.locator('.voice[data-voice="male"]').click()
        reduced.wait_for_function('activeVoice === "male" && audio.readyState >= 1')
        reduced.wait_for_timeout(250)
        pixels = reduced.evaluate('''() => {
          const c = head.canvas, data = c.getContext('2d').getImageData(0,0,c.width,c.height).data;
          let lit = 0;
          for (let i=0; i<data.length; i+=4) if (data[i]+data[i+1]+data[i+2] > 30) lit++;
          return lit;
        }''')
        assert pixels > 1000, pixels
        results['reduced_motion']['playing_and_voice_pixels'] = pixels
        reduced.locator('#play').click()
        reduced.wait_for_function('audio.paused && !head.playing && playerFrame === 0')
        reduced.locator('#seek').evaluate('(el) => { el.value = "16.8"; el.dispatchEvent(new Event("input", {bubbles: true})); }')
        reduced.wait_for_function('Math.abs(head.currentTime - 16.8) < 0.15')
        assert reduced.evaluate('head._raf') == 0
        assert reduced.locator('#time').inner_text().startswith('0:16 /')
        results['reduced_motion']['seek_time'] = reduced.evaluate('head.currentTime')
        results['reduced_motion']['raf_after_seek'] = 0
        reduced.emulate_media(reduced_motion='no-preference')
        reduced.locator('#play').click()
        reduced.wait_for_function('head._raf > 0')
        reduced.emulate_media(reduced_motion='reduce')
        reduced.wait_for_function('head._raf === 0')
        results['reduced_motion']['preference_changes'] = 'pass'
        results['page_errors'] = errors
        assert not errors
        # Paused seeking before the timeline arrives must redraw when data lands.
        late = browser.new_page(viewport={'width': 1280, 'height': 900})
        late.on('pageerror', lambda error: errors.append('late: ' + str(error)))
        delayed_server = ThreadingHTTPServer(('127.0.0.1', 0), partial(DelayedTimelineHandler, directory=str(ROOT)))
        delayed_thread = Thread(target=delayed_server.serve_forever, daemon=True)
        delayed_thread.start()
        delayed_url = f'http://127.0.0.1:{delayed_server.server_port}/'
        late.goto(delayed_url, wait_until='domcontentloaded')
        late.wait_for_function('head.notes.length === 0 && audio.readyState >= 1')
        late.locator('#seek').evaluate('(el) => { el.value = "16.8"; el.dispatchEvent(new Event("input", {bubbles: true})); }')
        late.wait_for_function('Math.abs(audio.currentTime - 16.8) < 0.15 && head.notes.length === 0')
        late.wait_for_function('head.notes.length === 28 && head.activeNoteUsed?.note.note === "F#5"')
        assert 'F#5' in late.locator('#head-status').inner_text()
        results['late_timeline'] = {'note': late.evaluate('head.activeNoteUsed.note.note'), 'status': late.locator('#head-status').inner_text()}
        # Overlapping switches must restore only the final selection, never old closures.
        late.evaluate('''() => {
          document.querySelector('.voice[data-voice="male"]').click();
          document.querySelector('.voice[data-voice="child"]').click();
          document.querySelector('.voice[data-voice="female"]').click();
          document.querySelector('.voice[data-voice="child"]').click();
        }''')
        late.wait_for_function('activeVoice === "child" && pendingVoiceRestore === null && audio.readyState >= 1')
        late.wait_for_timeout(250)
        assert late.evaluate('activeVoice') == 'child'
        assert late.evaluate('audio.currentSrc.endsWith("greenhouse-child.mp3")')
        print('RAPID SWITCH STATE', late.evaluate('({voice: activeVoice, src: audio.currentSrc, time: audio.currentTime, head: head.currentTime, paused: audio.paused, generation: voiceGeneration, pending: pendingVoiceRestore, seek: seek.value})'), flush=True)
        assert abs(late.evaluate('audio.currentTime') - 16.8) < 0.15
        assert late.evaluate('audio.paused')
        results['rapid_voice_switches'] = late.evaluate('({voice: activeVoice, time: audio.currentTime, paused: audio.paused, generation: voiceGeneration})')
        late.locator('#play').click()
        late.wait_for_function('!audio.paused && audio.currentTime > 16.8')
        late.evaluate('document.querySelector(\'.voice[data-voice="male"]\').click()')
        late.wait_for_function('pendingVoiceRestore !== null')
        late.locator('#play').click()
        late.wait_for_function('pendingVoiceRestore === null && audio.readyState >= 1')
        late.wait_for_timeout(200)
        assert late.evaluate('audio.paused'), late.evaluate('({src: audio.currentSrc, paused: audio.paused, pending: pendingVoiceRestore})')
        results['pause_during_voice_load'] = late.evaluate('({voice: activeVoice, time: audio.currentTime, paused: audio.paused})')
        early_lyric = browser.new_page(viewport={'width': 1280, 'height': 900})
        early_lyric.on('pageerror', lambda error: errors.append('early lyric: ' + str(error)))
        early_lyric.goto(delayed_url, wait_until='domcontentloaded')
        early_lyric.wait_for_function('timelineReady !== null && lineStarts === null')
        early_lyric.locator('.lyric[data-line="3"]').click()
        early_lyric.wait_for_function('document.querySelector("#audio-status").textContent.includes("Loading the melody timing")')
        early_lyric.wait_for_timeout(150)
        assert early_lyric.evaluate('audio.paused') and early_lyric.evaluate('audio.currentTime') == 0
        early_lyric.wait_for_function('lineStarts !== null && !audio.paused && audio.currentTime > 13.425')
        assert early_lyric.evaluate('currentLine') == 3
        assert early_lyric.locator('.lyric[data-line="3"]').get_attribute('aria-current') == 'true'
        results['early_lyric_waits_for_timeline'] = early_lyric.evaluate('({time: audio.currentTime, line: currentLine, paused: audio.paused})')
        delayed_server.shutdown()
        delayed_server.server_close()
        delayed_thread.join(timeout=3)
        delayed_server = ThreadingHTTPServer(('127.0.0.1', 0), partial(DelayedVoiceHandler, directory=str(ROOT)))
        delayed_thread = Thread(target=delayed_server.serve_forever, daemon=True)
        delayed_thread.start()
        delayed_url = f'http://127.0.0.1:{delayed_server.server_port}/'
        # A paused seek while a new voice loads must replace, not be overwritten by,
        # the position captured when the voice was selected.
        pending_seek = browser.new_page(viewport={'width': 1280, 'height': 900})
        pending_seek.goto(delayed_url, wait_until='networkidle')
        pending_seek.wait_for_function('head.notes.length === 28 && audio.readyState >= 1')
        pending_seek.locator('#seek').evaluate('(el) => { el.value = "16.8"; el.dispatchEvent(new Event("input", {bubbles: true})); }')
        pending_seek.wait_for_function('Math.abs(audio.currentTime - 16.8) < 0.15')
        pending_seek.evaluate('document.querySelector(\'.voice[data-voice="male"]\').click()')
        pending_seek.wait_for_function('pendingVoiceRestore !== null')
        pending_seek.locator('#seek').evaluate('(el) => { el.value = "1.04"; el.dispatchEvent(new Event("input", {bubbles: true})); }')
        pending_seek.wait_for_function('pendingVoiceRestore === null && audio.readyState >= 1')
        pending_seek.wait_for_function('Math.abs(audio.currentTime - 1.04) < 0.15 && Math.abs(head.currentTime - 1.04) < 0.15')
        assert pending_seek.evaluate('head.activeNoteUsed?.note.note') == 'F#4'
        assert abs(pending_seek.evaluate('Number(seek.value)') - 1.04) < 0.15
        results['seek_during_voice_load'] = pending_seek.evaluate('({voice: activeVoice, time: audio.currentTime, note: head.activeNoteUsed?.note.note, paused: audio.paused})')
        # Lyric clicks are seek intents too and must survive delayed metadata while playing.
        pending_seek.evaluate('document.querySelector(\'.voice[data-voice="female"]\').click()')
        pending_seek.wait_for_function('pendingVoiceRestore === null && audio.readyState >= 1')
        pending_seek.locator('#seek').evaluate('(el) => { el.value = "0"; el.dispatchEvent(new Event("input", {bubbles: true})); }')
        pending_seek.locator('#play').click()
        pending_seek.wait_for_function('!audio.paused && audio.currentTime > 0.25')
        pending_seek.evaluate('document.querySelector(\'.voice[data-voice="child"]\').click()')
        pending_seek.wait_for_function('pendingVoiceRestore !== null')
        pending_seek.locator('.lyric[data-line="3"]').click()
        pending_seek.wait_for_function('pendingVoiceRestore === null && audio.readyState >= 1')
        pending_seek.wait_for_function('!audio.paused && audio.currentTime > 13.3 && audio.currentTime < 16')
        pending_seek.wait_for_function('currentLine === 3')
        assert pending_seek.evaluate('activeVoice') == 'child'
        assert abs(pending_seek.evaluate('audio.currentTime') - pending_seek.evaluate('head.currentTime')) < 0.15
        assert pending_seek.locator('.lyric[data-line="3"]').get_attribute('aria-current') == 'true'
        results['lyric_during_voice_load'] = pending_seek.evaluate('({voice: activeVoice, time: audio.currentTime, headTime: head.currentTime, line: currentLine, paused: audio.paused})')
        # Seek then pause while loading must preserve both intents and never
        # start playback when metadata eventually arrives.
        pending_seek.locator('#play').click()
        pending_seek.wait_for_function('audio.paused')
        pending_seek.evaluate('document.querySelector(\'.voice[data-voice="female"]\').click()')
        pending_seek.wait_for_function('pendingVoiceRestore === null && audio.readyState >= 1')
        pending_seek.locator('#seek').evaluate('(el) => { el.value = "0"; el.dispatchEvent(new Event("input", {bubbles: true})); }')
        pending_seek.locator('#play').click()
        pending_seek.wait_for_function('!audio.paused && audio.currentTime > 0.25')
        pending_seek.evaluate('document.querySelector(\'.voice[data-voice="child"]\').click()')
        pending_seek.wait_for_function('pendingVoiceRestore !== null')
        pending_seek.locator('#seek').evaluate('(el) => { el.value = "13.33"; el.dispatchEvent(new Event("input", {bubbles: true})); }')
        pending_seek.locator('#play').click()
        pending_seek.wait_for_function('pendingVoiceRestore === null && audio.readyState >= 1')
        pending_seek.wait_for_timeout(300)
        paused_pending = pending_seek.evaluate('({voice: activeVoice, audio: audio.currentTime, head: head.currentTime, slider: Number(seek.value), paused: audio.paused, status: document.querySelector("#head-status").textContent})')
        assert paused_pending['paused'] and abs(paused_pending['audio'] - 13.33) < 0.15, paused_pending
        assert abs(paused_pending['head'] - paused_pending['audio']) < 0.15, paused_pending
        assert abs(paused_pending['slider'] - paused_pending['audio']) < 0.15, paused_pending
        results['seek_then_pause_during_voice_load'] = paused_pending
        # A lyric jump and its highlight share the exact same timestamp.
        pending_seek.locator('.lyric[data-line="3"]').click()
        pending_seek.wait_for_function('!audio.paused && audio.currentTime > 13.425')
        pending_seek.wait_for_timeout(350)
        lyric_state = pending_seek.evaluate('({line: currentLine, time: audio.currentTime, head: head.currentTime, status: document.querySelector("#head-status").textContent})')
        assert lyric_state['line'] == 3, lyric_state
        assert pending_seek.locator('.lyric[data-line="3"]').get_attribute('aria-current') == 'true'
        assert 'singing' in lyric_state['status'], lyric_state
        results['settled_lyric_and_status'] = lyric_state
        # Normal seek to a rest must update both the drawing and its textual state.
        pending_seek.locator('#play').click()
        pending_seek.wait_for_function('audio.paused')
        pending_seek.locator('#seek').evaluate('(el) => { el.value = "13.1125"; el.dispatchEvent(new Event("input", {bubbles: true})); }')
        pending_seek.wait_for_function('Math.abs(audio.currentTime - 13.1125) < 0.15 && Math.abs(head.currentTime - 13.1125) < 0.15')
        assert pending_seek.evaluate('head.activeNoteUsed') is None
        pending_seek.wait_for_function('document.querySelector("#head-status").textContent.includes("between notes")')
        assert 'between notes' in pending_seek.locator('#head-status').inner_text()
        results['rest_seek_status'] = pending_seek.locator('#head-status').inner_text()
        delayed_server.shutdown()
        delayed_server.server_close()
        delayed_thread.join(timeout=3)
        delayed_server = ThreadingHTTPServer(('127.0.0.1', 0), partial(FailedTimelineHandler, directory=str(ROOT)))
        delayed_thread = Thread(target=delayed_server.serve_forever, daemon=True)
        delayed_thread.start()
        delayed_url = f'http://127.0.0.1:{delayed_server.server_port}/'
        failed_timeline = browser.new_page(viewport={'width': 1280, 'height': 900})
        failed_timeline.on('pageerror', lambda error: errors.append('failed timeline: ' + str(error)))
        failed_timeline.goto(delayed_url, wait_until='domcontentloaded')
        failed_timeline.wait_for_function('timelineReady !== null && lineStarts === null && audio.readyState >= 1')
        failed_timeline.locator('#play').click()
        failed_timeline.wait_for_function('!audio.paused')
        failed_timeline.locator('.lyric[data-line="3"]').click()
        failed_timeline.wait_for_function('timelineFailed && lineStarts === null')
        assert failed_timeline.locator('#audio-status').inner_text().startswith('Melody timing could not load')
        assert not failed_timeline.evaluate('audio.paused')
        failed_timeline.locator('#seek').evaluate('(el) => { el.value = "2"; el.dispatchEvent(new Event("input", {bubbles: true})); }')
        failed_timeline.wait_for_function('Math.abs(audio.currentTime - 2) < 0.15')
        results['failed_timeline_during_playback'] = failed_timeline.evaluate('({failed: timelineFailed, status: document.querySelector("#audio-status").textContent, paused: audio.paused, time: audio.currentTime})')
        failed_timeline.locator('#play').click()
        failed_timeline.wait_for_function('audio.paused')
        delayed_server.shutdown()
        delayed_server.server_close()
        delayed_thread.join(timeout=3)
        delayed_server = ThreadingHTTPServer(('127.0.0.1', 0), partial(FailedVoiceHandler, directory=str(ROOT)))
        delayed_thread = Thread(target=delayed_server.serve_forever, daemon=True)
        delayed_thread.start()
        delayed_url = f'http://127.0.0.1:{delayed_server.server_port}/'
        failed_voice = browser.new_page(viewport={'width': 1280, 'height': 900})
        failed_voice.on('pageerror', lambda error: errors.append('failed voice: ' + str(error)))
        failed_voice.goto(delayed_url, wait_until='networkidle')
        failed_voice.wait_for_function('head.notes.length === 28 && audio.readyState >= 1')
        failed_voice.locator('.voice[data-voice="male"]').click()
        failed_voice.wait_for_function('pendingVoiceRestore !== null')
        failed_voice.locator('.lyric[data-line="3"]').click()
        failed_voice.wait_for_function('pendingVoiceRestore === null && audio.error !== null')
        assert failed_voice.evaluate('audio.paused') and not failed_voice.evaluate('isSinging()')
        assert failed_voice.evaluate('playerFrame') == 0
        assert failed_voice.locator('#play').get_attribute('aria-label') == 'Play song'
        assert 'could not load' in failed_voice.locator('#audio-status').inner_text()
        results['failed_voice_clears_pending'] = failed_voice.evaluate('({pending: pendingVoiceRestore, paused: audio.paused, singing: isSinging(), frame: playerFrame, label: play.getAttribute("aria-label"), status: document.querySelector("#audio-status").textContent})')
        failed_voice.locator('.voice[data-voice="child"]').click()
        failed_voice.wait_for_function('activeVoice === "child" && pendingVoiceRestore === null && audio.readyState >= 1')
        results['recovery_after_voice_failure'] = failed_voice.evaluate('({voice: activeVoice, paused: audio.paused, pending: pendingVoiceRestore})')
        delayed_server.shutdown()
        delayed_server.server_close()
        delayed_thread.join(timeout=3)
        # Natural completion must leave the media, slider, and head on the same clock.
        for completion_page in [page, reduced]:
            completion_page.evaluate('() => { audio.currentTime = audio.duration - 0.08; audio.play(); }')
            completion_page.wait_for_function('audio.ended')
            completion_page.wait_for_function('!head.playing && head._raf === 0 && playerFrame === 0')
            ended = completion_page.evaluate('({audio: audio.currentTime, head: head.currentTime, slider: Number(seek.value), status: document.querySelector("#head-status").textContent})')
            assert abs(ended['audio'] - ended['head']) < 0.05, ended
            assert abs(ended['audio'] - ended['slider']) < 0.05, ended
            assert 'between notes' in ended['status'], ended
            results[f'ended_{"reduced" if completion_page is reduced else "normal"}'] = ended
        browser.close()
finally:
    server.shutdown()
    server.server_close()
    thread.join(timeout=3)
print(json.dumps(results, indent=2))
print(f'Screenshots: {OUTPUT}')
