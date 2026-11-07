"""Evidence-gated M10 release report. Run with local Python that already has Pillow."""
from pathlib import Path
import json,re,hashlib,shutil,subprocess,zipfile

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'presentation_demo/m10'
DOC=ROOT/'documentation'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def visuals():
 from PIL import Image,ImageDraw,ImageFont
 names=['01_intro','02_aerial','03_main_corridor','04_intersection','05_railway_closed','06_railway_open','07_frontage','08_vehicle_closeup','09_2026_baseline','10_2040_high','11_before_after','12_presentation']
 font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',18)
 sheet=Image.new('RGB',(1920,1720),'#172e38');d=ImageDraw.Draw(sheet);d.text((24,18),'GEDANGAN / M10 — ACTUAL SUMO PLAYBACK',font=font,fill='#e7d3a1');d.text((24,49),'Illustrative demand · stylized context · empirical baseline not calibrated',font=font,fill='#bbc9c9')
 for i,n in enumerate(names):
  p=OUT/'screenshots'/f'{n}.png';im=Image.open(p).convert('RGB')
  if im.size!=(1920,1080):raise ValueError('Screenshot is not Full HD: '+n)
  x=(i%3)*640;y=95+(i//3)*400;im.thumbnail((624,351));sheet.paste(im,(x+8,y));d.text((x+12,y+359),n.replace('_',' '),font=font,fill='#e3e9e2')
 target=OUT/'M10_VISUAL_CONTACT_SHEET.png';sheet.save(target);shutil.copy2(target,DOC/target.name)
 for label,before,after in [('main','main-corridor-2026','main-corridor-2026'),('intersection','gedangan-intersection','gedangan-intersection'),('railway','railway-closed-train','railway-closed-train'),('vehicle','class-car','class-car')]:
  a=OUT/'baseline'/f'{before}.png';b=OUT/'qa'/f'{after}.png'
  panel=Image.new('RGB',(1920,640),'#eef1eb');draw=ImageDraw.Draw(panel);draw.text((20,8),'M09 / BEFORE',font=font,fill='#344b50');draw.text((980,8),'M10 / AFTER',font=font,fill='#344b50')
  for x,p in [(0,a),(960,b)]:
   im=Image.open(p).convert('RGB');im.thumbnail((944,531));panel.paste(im,(x+8,45))
  draw.text((20,597),'Actual screenshots. Camera framing and UI changed; this is not a paired traffic-performance comparison.',font=font,fill='#5a6c67');panel.save(OUT/'screenshots'/f'before-after-{label}.png')
 return names

def main():
 names=visuals();qa=read(OUT/'qa/browser-qa.json');base=read(OUT/'baseline/browser-qa.json');classes=read(OUT/'qa/class-qa.json');perf=read(OUT/'qa/performance-workloads.json');capture=read(OUT/'capture-screenshots.json');zoom=read(OUT/'qa/zoom-and-baseline-extra.json');video=read(OUT/'capture-video.json');review=read(OUT/'qa/visual-review.json');invariants=read(OUT/'qa/visual-invariants.json');package_smoke=read(OUT/'qa/package-smoke.json')
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(OUT/'GEDANGAN_3D_DEMO.mp4')],text=True));vs=next(v for v in probe['streams'] if v['codec_type']=='video');duration=float(probe['format']['duration'])
 reg=(DOC/'m10/initial-regression.txt').read_text(encoding='utf-8-sig');match=re.search(r'Ran (\d+) tests in ([\d.]+)s\s+OK',reg);protected=int((DOC/'m10/protected-files-verification.txt').read_text(encoding='utf-8-sig').strip())
 cases=perf.get('cases',[]);visual=review.get('status')=='PASS_TECHNICAL_STYLIZED_PRESENTATION'
 gates=[('Professional world composition',visual),('Road and railway distinction',visual),('Nine road classes and actual train close-ups',visual and len(classes['classes'])==10 and classes['status']=='PASS'),('Rail closure/open demonstration',capture['status']=='PASS'),('Eight cameras / bookmark / framing',visual and perf['status']=='PASS_MEASURED'),('Accurate smooth recorded playback',len(qa['checks'])==18 and qa['overall'].startswith('PASS')),('Understandable actual-data overlays',visual and capture['status']=='PASS' and invariants['status']=='PASS'),('1080p readability and responsive UI',visual and capture['status']=='PASS' and zoom['status']=='PASS'),('Correct statistics and accounting',True),('Honest before/after including adverse result',capture['status']=='PASS'),('Ten-scene uninterrupted presentation',any(v['name']=='ten_step_presentation_end_to_end_keyboard_and_restart' for v in qa['checks'])),('Actual Full HD screenshots',len(names)==12),('Actual screenshot contact sheet',True),('No critical browser errors',not qa['errors'] and not perf['errors'] and not capture['errors'] and not video['errors']),('Offline presentation',not qa['external_requests'] and not qa['failed_responses'] and not capture['external'] and package_smoke['status']=='PASS'),('Regression tests',bool(match) and int(match[1])==344 and base['overall'].startswith('PASS')),('Original sources and simulation protected',protected==7055),('Measured demonstration performance',perf['status']=='PASS_MEASURED' and perf['target_30fps_all'])]
 video_ok=video['status']=='PASS' and 60<=duration<=120 and vs['width']==1920 and vs['height']==1080 and vs['codec_name']=='h264'
 core=(DOC/'m10/core-tests.txt').read_text(encoding='utf-8-sig');gates[8]=(gates[8][0],'Final M10 core assertions 31' in core)
 status='VISUAL_PRESENTATION_READY_PASS' if all(v for _,v in gates) and video_ok else 'PARTIAL'
 acceptance={'status':status,'date_local':'2026-11-01','gates':[{'criterion':k,'pass':v} for k,v in gates],'demo_video':{'pass':video_ok,'duration_s':duration,'width':vs['width'],'height':vs['height'],'codec':vs['codec_name'],'sha256':digest(OUT/'GEDANGAN_3D_DEMO.mp4')},'empirical_baseline':'BLOCKED — DATA REQUIRED','M11_started':False,'M12_started':False};write(OUT/'acceptance.json',acceptance)
 rows='\n'.join(f'| {i+1} | {k} | {"PASS" if v else "PARTIAL"} |' for i,(k,v) in enumerate(gates))
 table='\n'.join(f"| {v['name']} | {v['mean_fps']:.1f} | {v['p5_min']:.1f} | {v['max_stalls_over_50ms_in_rolling_window']} | {v['heap_bytes']/1048576:.1f} |" for v in cases)
 (DOC/'M10_PRESENTATION_ACCEPTANCE.md').write_text(f'''# M10 presentation acceptance — 1 November 2026

**{status.replace('_',' ')}**

| Gate | Criterion | Result |
|---|---|---|
{rows}

Actual demonstration video: {'PASS' if video_ok else 'PARTIAL'}, {duration:.2f} s, {vs['width']}×{vs['height']}, {vs['codec_name']}. Screenshots and video use actual browser playback, not generated imagery.

Technical stylized visualization acceptance is separate from empirical traffic validation. Demand/timing/context remain assumptions; there are no verified Gedangan field measurements. No recommendation of real-world intervention effectiveness is made. M11/M12 are not started.

See `presentation_demo/m10/acceptance.json`, visual-review.json, browser/class QA, performance-workloads.json, core/regression logs and protected-file verification for evidence and limits.
''',encoding='utf-8')
 limitations='\n'.join('- '+v for v in review['limitations'])
 (DOC/'M10_FINAL_VISUAL_QA.md').write_text(f'''# M10 final visual QA — 1 November 2026

**{status.replace('_',' ')}**

Actual M09 baseline screenshots were inspected before polish. M10 actual screenshot contact sheet, twelve Full HD frames and ten actual class views were reviewed after functional testing. Review decisions and individual image findings: `presentation_demo/m10/qa/visual-review.json`.

Before/after panels: `presentation_demo/m10/screenshots/before-after-main.png`, `before-after-intersection.png`, `before-after-railway.png`, `before-after-vehicle.png`. Framing and layout intentionally differ; these are visual comparisons, not paired measurements of traffic benefit.

The internal browser was independently opened and operated on port 5186. Road/rail scene, actual train, closure badge and stopped-vehicle overlay were visibly verified. The saved internal-browser stats are one paused rendering window, not the full workload benchmark. A subsequent final reload returned Local browser use is disabled in Work settings; no final-IAB-matrix success is claimed. A Codex panel open request was queued separately, which is not a rendered-state verification. Chrome/Playwright captures supply the Full HD artifact evidence.

Final browser QA: {len(qa['checks'])} flows, {len(qa['errors'])} errors, {len(qa['failed_responses'])} missing/error responses, {len(qa['external_requests'])} external requests. Class views: {len(classes['classes'])}; oversize not fabricated. Capture status: {capture['status']}; actual demo video: {video['status']}.

Issues found during development were retained as failed evidence: presenter controls initially exceeded the 1080p viewport. The layout was changed to bounded flex allocation and all 18 flows rerun. Aerial framing was subsequently fitted to modeled bounds for four aspect ratios; final screenshots must show the full network rather than merely a tiny or cropped diagram.

| Workload | Mean FPS | Minimum rolling p5 FPS | Maximum >50 ms stalls in a rolling window | JS heap after GC MiB |
|---|---|---|---|---|
{table}

Additional renderer checks: {len(invariants['checks'])} PASS, including pixel-stable paused screenshots, visible context/overlay toggles, separate unavailable causal-map/geometry warnings, and S07 no-traffic schematic. Browser zoom 125%/150% verified in isolated native Chrome settings.

Preload: {perf['preload_ms']} ms. Renderer: {perf['webgl']['renderer']}. Samples: eight rolling windows per workload after warmup, same installed Chrome/native WebGL. Stall counts overlap between windows and must not be summed. JS heap is not total process/GPU memory. Repeated transitions: {perf.get('repeated_transitions')}. No physical VRAM capacity inferred. Background desktop activity may affect measurements.

Remaining boundaries:

{limitations}
''',encoding='utf-8')
 (DOC/'MILESTONE_10_REPORT.md').write_text(f'''# MILESTONE 10 — Gedangan Traffic Simulator

**{status.replace('_',' ')}** · 1 November 2026 · M10 only

M10 adds a separate visual application and leaves M09 intact. Source: `frontend/src/m10/`; build: `frontend/dist-m10/`; read-only stdlib host: `backend/gedangan/m10_server.py`; launch: `START_GEDANGAN_M10.bat`; rebuild: `REBUILD_VISUAL_M10.bat`; URL: http://127.0.0.1:5186/visual.html.

Actual M09 screenshots identified broken dash phase/seams, repetitive tall context, floating/duplicated motorcycle wheels, plain vehicle silhouettes, weak camera composition, small labels and incorrect UNSERVED terminology. The initial audit documents priorities and evidence before renderer edits; source inspection alone was not used to judge appearance.

Road ribbons now share bounded miter vertices and dash phase follows polyline distance. Main and frontage remain separate, with distinct surface treatment and optional role colors. Direction indicators follow directed SUMO lane shapes; they are visual assumptions, not surveyed road markings. Junctions still use the original polygons; source topology is not edited to conceal geometric limitations. Railway keeps authoritative polylines, track gauge display, ballast, sleepers and actual controller states.

Context uses lower, spaced massing with roof caps, textured windows, trunk/canopy vegetation, contact shading and limited streetlights rejected near retained roads/rail. No landmark, building footprint, curb/shoulder or engineering clearance is invented as measured fact. Daylight is the default; lighting/shadow budgets favor readable roads and vehicles.

Vehicle models preserve M04/M09 registry dimensions and actual FCD identities. Cars gain tapered body geometry; truck/bus/trailer/minibus retain distinct proportions, wheels, windows, lamps and cargo/cab structure. Motorcycle duplicate wheels were removed; ground offsets align tires to the planar displayed road. Static local parts are baked per material/coach and instanced, reducing submission overhead without altering trajectories. Train coaches follow the existing retained rail chain. No oversize record is fabricated.

All eight cameras remain. Corridor/junction/rail views are closer, follow is heading-aware and dimension-aware, train follow uses a wider lateral view, aerial distance fits retained bounds/aspect ratio, and a session bookmark restores a saved viewpoint. Zoom/pan/tilt constraints and reset remain. Presentation layout reserves room for controls and notes within fullscreen rather than overflowing the projector viewport.

Playback preserves the M09 interpolation/visibility logic: 0.5 s FCD, 1 s control samples, +0.5 s FCD/TraCI clock alignment, no early spawn, no interpolation across invalid gaps, shortest-angle heading, real departures/arrivals. No movement data, demand, network permission or control sequence is changed.

Stopped-body/tail, occupied-length and role overlays use actual poses/lanes. Occupied intervals are merged; stopped threshold is 0.3 m/s. Overlays are sampled spatial indicators, not detector occupancy, verified queues, causal congestion or measured Gedangan traffic. Verified spillback on the dashboard is a horizon metric; no instantaneous cause map is fabricated. Conceptual infrastructure is separately labelled; S06/S07 show schematic transparent massing, no alignment/ramps/clearance or vehicles through an unvalidated concept.

Requested, routable, failed routes, loaded, departed, not departed, running at end and arrived are separated. NOT ARRIVED BY SIMULATION END = requested − arrived. All 23 cached run accounting identities were checked: requested=routable+failed; routable=departed+not departed; departed=arrived+running. Completion gives arrived/requested and 35-minute horizon. Throughput remains a fixed-horizon model rate, not measured capacity.

Comparison retains paired cohort/seed/horizon checks and shared camera/clock. Fullscreen includes the scoped result status and arrival counts. The adverse 2040 HIGH case shows S00 356 versus S01 328 arrived / 500 requested, WORSENED IN THIS SIMULATION · ARRIVED ONLY. Actual OD-specific arrived/running/not-departed/waiting deltas expose tradeoffs, with conditional-cohort warnings. Other metrics remain available; no global best solution or real-world effectiveness is inferred.

Validation: baseline M09 {len(base['checks'])} browser flows and 10 class views; M01–M09 {int(match[1]) if match else 'UNCONFIRMED'} Python tests in {match[2] if match else '—'} s; M10 31 core assertions including all-run accounting and camera bounds; TypeScript/build with byte-identical repeat build; six actual host/launcher checks; final M10 {len(qa['checks'])} browser flows and ten class views; responsive/capture checks, native Chrome zoom 125% and 150%; eight measured workloads and 12 repeated transitions. Functional and visual tests are reported separately, not added into an invented Python test count. The 35-minute recording completed at 16× without page crash.

Original protection: {protected} file hashes still match the pre-M10 checkpoint, including old source/config/data/network/outputs/reports/builds. Scope/exclusions are in `documentation/m10/baseline-scope.json`. M09 append-only browser telemetry is explicitly excluded. The M10 host hashes every original index, chunk and scene before use; original source cache is read-only. Extracted offline package was cold-started with global Python (stdlib only, no research venv/Node/SUMO), served the build and original recording gzip, returned 23 recordings and the correct acceptance status, then shut down cleanly on port 5187. Evidence: qa/package-smoke.json. This is a distribution runtime check, not a claim that the entire 16 GB research workspace is packaged.

Performance and hardware evidence: `M10_FINAL_VISUAL_QA.md`, `presentation_demo/m10/qa/performance-workloads.json`, `documentation/m10/hardware.json`. Results are per actual workload; no VRAM or universal hardware guarantee is inferred. The internal browser was visibly verified; the full matrix uses installed Chrome/Playwright. Preload {perf['preload_ms']} ms; all measured mean/p5 windows meet 30 FPS: {perf.get('target_30fps_all')}.

Deliverables: twelve actual 1920×1080 screenshots under `presentation_demo/m10/screenshots/`, contact sheet `M10_VISUAL_CONTACT_SHEET.png`, actual H.264 Full HD demo `presentation_demo/m10/GEDANGAN_3D_DEMO.mp4` ({duration:.2f} s), final visual QA, README, 18-gate acceptance and evidence manifests. Video is screen capture of real local playback; no AI-generated traffic footage or fake measurement is used.

Remaining boundaries and candidates for later work:

{limitations}

M11/M12 are not started. Empirical calibration requires verified field observations and independent validation; M10 does not promote historical M08.5 status or legal/engineering feasibility. Later work is recorded as a candidate only, not authorized by this report.
''',encoding='utf-8')
 for name in ['MILESTONE_10_REPORT.md','MILESTONE_10_README.md','M10_INITIAL_VISUAL_AUDIT.md','M10_FINAL_VISUAL_QA.md','M10_PRESENTATION_ACCEPTANCE.md']:shutil.copy2(DOC/name,OUT/name)
 files=[]
 for folder in [ROOT/'frontend/src/m10',ROOT/'frontend/dist-m10',ROOT/'tests/m10',OUT/'screenshots',OUT/'qa']:
  files.extend(p for p in folder.rglob('*') if p.is_file() and p.name!='browser-performance.jsonl')
 files += [ROOT/'START_GEDANGAN_M10.bat',ROOT/'REBUILD_VISUAL_M10.bat',ROOT/'frontend/vite.visual.config.ts',ROOT/'frontend/visual.html',OUT/'acceptance.json',OUT/'GEDANGAN_3D_DEMO.mp4',OUT/'M10_VISUAL_CONTACT_SHEET.png']
 files += list((ROOT/'backend/gedangan').glob('m10_*.py'))
 write(OUT/'delivery-manifest.json',{'status':status,'date_local':'2026-11-01','protected_files_verified':protected,'M11_started':False,'M12_started':False,'baseline_manifest_sha256':digest(ROOT/'presentation_demo/m09/M09_DEMO_MANIFEST.json'),'shared_read_only_recordings':'presentation_demo/m09/cache; each index/chunk/scene verified by host','files':{p.relative_to(ROOT).as_posix():digest(p) for p in files}})
 print(json.dumps({'status':status,'gates_passed':sum(v for _,v in gates),'video_duration_s':duration,'protected_files':protected}),flush=True)
if __name__=='__main__':main()
