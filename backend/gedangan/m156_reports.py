"""Evidence-based M15.6 release review; targets may fail, no invented acceptance."""
from .m156_common import *
from datetime import datetime
import statistics,subprocess
def dt(s):return datetime.fromisoformat(s.replace('Z','+00:00')).timestamp()
def table(head,rows):return '\n'.join(['| '+' | '.join(head)+' |','| '+' | '.join(['---']*len(head))+' |']+['| '+' | '.join(str(v).replace('|',' / ')for v in row)+' |'for row in rows])
def main():
 protect();soak=load(DOC/'soak-final.json');assert soak['elapsed_wall_s']>=900,soak
 raw=[dict(file=p.relative_to(ROOT).as_posix(),**load(p))for p in (DOC/'browser-performance').glob('*.json')];st=dt(load(DOC/'soak-start.json')['start_utc']);end=dt(soak['end_utc']);allfinal=[r for r in raw if st<=dt(r['recorded_utc'])<=end];rs=[r for r in allfinal if 'fps_p5'in r];benches=[]
 for case in load(DOC/'benchmark-intervals.json'):
  start=dt(case['start_utc']);selected=[r for r in rs if start+5<=dt(r['recorded_utc'])<=start+45 and r.get('recording')==case['run']and r.get('camera')=='junction'and r.get('speed')==1 and r.get('window')==[1920,1080]]
  assert selected,case
  median=statistics.median(r['fps_median']for r in selected);p5=min(r['fps_p5']for r in selected);window_heap=max(r['js_heap']['used']/1048576 for r in selected if r.get('js_heap'));heap=max(r['js_heap']['used']/1048576 for r in rs if r.get('recording')==case['run'] and r.get('js_heap'));total=int(case['case']);target={'median':45,'p5':30}if total==3000 else{'median':30,'p5':20}if total==5000 else None
  benches.append({'case':total,'run_id':case['run'],'camera':'junction','viewport':[1920,1080],'speed':1,'start_timestamp_s':1800,'analysis_wall_s':[5,45],'samples':len(selected),'median_of_window_fps_medians':median,'minimum_window_p5_fps':p5,'max_window_stalls_over50ms':max(r['stalls_over_50ms']for r in selected),'heap_max_mib':heap,'heap_analysis_window_mib':window_heap,'active_range':[min(r['visible_vehicles']for r in selected),max(r['visible_vehicles']for r in selected)],'rendered_instance_range':[min(r.get('rendered_instances',0)for r in selected),max(r.get('rendered_instances',0)for r in selected)],'target':target,'fps_target_status':'PASS'if target and median>=target['median']and p5>=target['p5']else'NOT MET'if target else'REFERENCE','heap800_mib_status':('PASS'if heap<=800 else'NOT MET')if total==3000 else'NOT APPLICABLE','raw_files':[r['file']for r in selected]})
 loads=[{'run_id':r['run_id'],'wall_ms':r['wall_ms'],'frames':r['frames'],'positions':r['positions']}for r in allfinal if r['kind']=='playback_load'];summary={'created_utc':now(),'status':'ALL_TARGETS_MET'if all(q['fps_target_status']!='NOT MET'and q['heap800_mib_status']!='NOT MET'for q in benches)else'TARGETS_NOT_FULLY_MET','cases':benches,'soak':soak,'raw_final_files':len(allfinal),'render_samples':len(rs),'minimum_p5_entire_soak':min(r['fps_p5']for r in rs),'maximum_heap_mib_entire_soak':max(r['js_heap']['used']/1048576 for r in rs if r.get('js_heap')),'loads':loads,'definitions':['Fixed45second wall window; seconds5–45 analysed for predeclared camera/load settling. No manual low-sample deletion.','Each renderer sample is rolling120frames, approximately10second logging. Median of window medians is not a lossless frame-weighted global median.','P5 target uses minimum saved window p5, not a favourable average. All transition/idle samples also retained.','Stall counts overlap across rolling windows; report maximum rather than invented unique-event sum.','Load timer covers fetch/decode, excludes reliable GPU first-present timing. GPU first-present latency MISSING.','JS heap is not physical RAM/VRAM; installed16GB, OS usable11.70GiB; GPU allocation6GB not independently verified.']};save(DOC/'performance-summary.json',summary)
 protection=verify();assert protection['status']=='PASS',protection
 eq=load(DOC/'traffic-equivalence.json');asset=load(DOC/'vehicle-asset-audit.json');workflow=load(DOC/'browser-workflow.json');source=load(DOC/'building-source.json');probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','format=duration:stream=width,height,nb_read_frames','-of','json',str(DOC/'evidence/actual-playback.webm')],text=True));save(DOC/'video-verification.json',{'probe':probe,'webm_sha256':sha(DOC/'evidence/actual-playback.webm'),'mp4_sha256':sha(DOC/'evidence/actual-playback.mp4'),'source':'Actual baseline3000 FCD/playback; live canvas with watermarked metadata','not_synthetic':True})
 head='2 November 2026, WIB. Separate staging http://127.0.0.1:5202/.\n\n**MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.**\n\n**PROVISIONAL NETWORK — NOT FIELD CALIBRATED.**\n\nNetwork SHA256 `'+EXPECTED+'`. M12/M14/M15/M15.5 retained; no flyover, added road, permission change, GitHub upload or final EXE.\n\n'
 def write(name,title,body):(ROOT/name).write_text('# M15.6 — '+title+'\n\n'+head+body.strip()+'\n',encoding='utf-8')
 write('M15_6_3D_VISUAL_REPORT.md','3D Visual Report',f'''
## Scope and evidence

Renderer changes live only in `frontend/src/m156`, build `frontend/dist-m156`, staging5202. Network/source lane arrays, junction boundaries and signal head coordinates equal the frozen original. Original demand builder, routing screens and controllers are inherited. No simulated road positions, widths, median openings, legal turns, frontage or rail alignment were altered for appearance.

## Environment

Shared procedural asphalt micrograin, neutral pavement tone, source-lane markings, stop-line render strips near the existing signal heads, rail steel/ballast/sleepers and controller-driven barrier geometry replace the colour-role map as default. Markings, sleeper gauge/spacing, furniture and assumed lane widths remain visual/model assumptions; not surveyed road paint. No unsupported sidewalk/shoulder/median infrastructure was invented. Source road ribbons/junction polygons remain, including sharp or irregular model junction boundaries; the milestone does not cosmetically move those into a smoother fictional road.

Lighting uses daylight hemisphere/key light, ACES output and static1024px soft context shadows. Vehicles retain local contact-shadows. Cars do not cast expensive per-vehicle dynamic shadow maps; ground-contact silhouette is a rendering approximation. This tradeoff is explicit, not a photometric validation claim.

Building request status: {source['status']}. Two bounded requests to Overpass returned502; the second used a smaller bbox. No footprint dataset was recovered. Neutral off-road massing is therefore used, with clearly labelled assumed shapes/heights/furniture. It uses inherited clearance exclusion from road/rail polylines, avoiding generated mass on those paths; not certification against actual buildings. No arbitrary facade/window layout is presented as actual Gedangan. This is context, separate from the validated traffic graph.

The [OSM building-level documentation](https://wiki.openstreetmap.org/wiki/Key:building:levels) distinguishes a level tag from measured height. Because no footprint data was retrieved, no levels-derived or surveyed building height was claimed. Request provenance/errors are retained in `documentation/m156/building-source.json`.

## Movement, overlays and camera

Every moving vehicle comes from actual retained FCD or a new actual M15.6 SUMO run; no decorative traffic or pending vehicle instances. Endpoint samples stay unchanged. Inherited0.5s position/heading interpolation is a visual interpolation, not extra physical measurements. A train-normalization regression was found in actual camera QA and fixed before the final soak: road-envelope scaling now excludes the80m train contact footprint, preserving eight full-size coaches. Before-fix evidence is retained as failed QA, not acceptance evidence. `train-asset-audit.json` checks8coach lengths9–10.1m and10m spacing. Rail coaches follow inherited rail polyline sampling; signal lamps/barriers read recorded controller events. Selection follows actual vehicle IDs. No proof of continuous swept-path clearance is inferred.

Ten camera presets were inspected in the live browser: elevated, topdown, aerial, main, reverse, junction, rail, frontage, follow and orbit. Presenter can pan/orbit/zoom, reset camera and switch presets with smooth transition. Mouse interaction holds the user camera until a preset/reset instead of snapping back. Camera/viewport changes never alter simulation time or statistics.

Density overlay uses occupied length fraction on recorded lanes; stopped/queue overlay uses actual sampled speed<0.3m/s and sampled lane tail. Role/direction highlighting is network-derived. Vehicle label toggle is an actual-ID/speed roster capped12, not thousands of invented labels. Road label toggle is a source-name legend, not accurately geolocated text on every road. Signal/crossing status is recorded state. Network Inspector remains available outside presentation and hidden by default.

## Visual review status

**VISUAL QUALITY: REVIEW REQUIRED.** Materials, scale, context and presentation improved, but neutral placeholders, simplified wheels/riders/bodywork, coarse procedural grain in close views and inherited irregular road geometry remain visible. Do not call this a surveyed photorealistic Gedangan reconstruction or unconditionally professional-grade approved art. User visual review remains necessary. All actual preset screenshots, before/after views, model comparison and live video are under `documentation/m156/evidence/`; screenshot text is soft at the browser capture quality, while video watermarks were separately checked for readability.
''')
 write('M15_6_VEHICLE_ASSET_REPORT.md','Vehicle Asset Report',f'''
## Asset system

Ten road definitions retain their SUMO dimensions. Procedural per-class assemblies contain geometry for body, glazing, wheels, hubs, lamps and class-specific structure. Motorcycles include rider/helmet/two wheels; cars have an extruded tapered shell; pickup has an open load bed; buses have long glazing and bus proportions; trucks differ in size/axle arrangement; trailer has a tractor cab/chassis, distinct coupling gap and long ribbed trailer with separate axle group. Becak and bicycle assemblies remain separate from passenger vehicles. Deterministic muted instance paints vary appearance without changing class or count.

{table(['ID','SUMO length × width × height m','Parts','Vertices','Envelope'],[[r['id'],' × '.join(str(x)for x in r['dimensions_sumo_lwh']),r['parts'],r['vertices'],r['envelope_status']]for r in asset['results']])}

Automated asset audit verifies all ten normalized geometry envelopes to1e-5m, minimum modelY=0 and ten distinct geometry hashes. Front-bumper FCD transforms subtract half actual length for render centre; render-surface offset is separate. Rail has eight coaches following the source rail path. Asset dimensions are model definitions, not measurements of a specific Indonesian vehicle fleet.

Trailer is visibly a tractor/gandengan assembly. It shares the SUMO heading as a rigid visual proxy; no independent trailer heading/physical articulation telemetry or swept-path certificate exists. Do not use the hitch gap to claim turn-clearance legality.

## Legal visibility and comparison

Live road traffic only instantiates IDs present in actual playback. Rejected bicycle/nonmotorized/heavy-route requests remain explicit failures and are not placed into roads. The stationary asset comparison is labelled MODEL PREVIEW ONLY — NOT ROUTED TRAFFIC, so all10definitions can be inspected without misrepresenting their route eligibility. Its screenshot proves visible form differences; actual movement proof remains FCD/ledger, not the gallery.

## Optimization

Per-material geometry is baked once, reused through dynamic InstancedMesh batches; maximum class capacities are computed in one pass through recordings. Source road surfaces are spatially tiled in200m render buckets without moving vertices. Camera-frustum tests exclude off-camera instances from draw batches. Glazing/wheel/hub detail drops beyond220m (LOD), while the body remains visible. Current active counts are computed from recordings, independent of culling or LOD. Shared procedural road/facade textures and instanced colours avoid per-vehicle image loads; no third-party texture atlas is required for these procedural assets. GPU resources are disposed when recordings change; old recording React state is cleared before loading the next. Entire actual frame data remains retained, not decimated to improve FPS.

Evidence: `vehicle-asset-audit.json`, `verify-assets.mjs`, `vehicle-assets.mjs`, registry snapshot and actual model-comparison screenshot. No paid/external vehicle assets or generated photographs were used.
''')
 write('M15_6_PRESENTATION_MODE_REPORT.md','Presentation Mode Report',f'''
## Presenter view

GEDANGAN TRAFFIC SIMULATOR is the title. The default view fills the browser viewport, with technical builder, comparisons and network debugging panels hidden behind controls. This is a full browser-viewport presentation mode, not a claim of OS-level exclusive fullscreen. Kembali exposes the full scenario builder; no manual/random functionality was removed.

HUD shows selected date/startWIB, duration/timestamp, total demand, actual active count/current mean speed/stopped count, end arrived/pending and end maximum queue extent. Vehicle composition comes from retained result classes. End statistics are explicitly labelled akhir; moving/current values are recomputed from the selected recording/time. Pending remains a number and never creates traffic instances. Two watermarks and assumed-context/source notes remain visible. All displayed traffic numbers retain their original actual definitions.

Controls: play/pause/reset, speed1/5/10 (also0.5/2), actual recording selection, ten camera presets, reset camera, viewport enlargement, video capture, context/vehicle-label/road-label/status toggles and actual density/stopped overlays. Vehicle-follow chooses an actual active ID or user-selected actual vehicle. No diagnostic knowledge is required to choose the primary presets.

## Workflow verification

Browser workflow evidence: `documentation/m156/browser-workflow.json`. Save/Load/Duplicate, preview, seed/date/time, manual/random controls, actual SUMO execution, comparison and Inspector were exercised. Actual M15.6 SUMO run `{eq['new_run']}` has the exact same physical request cohort and result counts as original100request run `{eq['original_run']}`:100routed/loaded/departed/moved,93arrived,7active,0pending,0failed. This confirms the visual wrapper did not change traffic in this tested cohort; it is not exhaustive proof for every possible input.

Video uses live3Dcanvas with timestamp/end-metric watermarks. Encoded metadata, hashes and frame verification are recorded in `video-verification.json`; no synthetic display traffic was substituted. Camera screenshots include static actual timestamps as well as running playback. Switching recordings pauses playback and preserves each run's actual end metrics.

## Limits

Neutral context is visibly approximate. Vehicle labels are a limited actual-ID roster and source road names are a legend; these are not screen-space labels anchored to every object. GPU first-present latency and a6GB VRAM allocation are not certified. No statistical outcome is presented as a calibrated historical measurement. Review the actual video and presets before presentation acceptance.
''')
 perf_table=table(['Demand','Samples','Median window medians FPS','Worst saved window p5 FPS','Max window stalls>50ms','Heap max MiB','Actual active','FPS target'],[[q['case'],q['samples'],f"{q['median_of_window_fps_medians']:.2f}",f"{q['minimum_window_p5_fps']:.2f}",q['max_window_stalls_over50ms'],f"{q['heap_max_mib']:.1f}",q['active_range'],q['fps_target_status']]for q in benches])
 write('M15_6_PERFORMANCE_REPORT.md','Performance Report',f'''
## Decision

**{summary['status']}.** All low samples are retained; no universal smoothness claim. Target3000:median≥45/windowp5≥30; target5000:median≥30/windowp5≥20. Heap target3000≤800MiB is assessed separately. The window p5 gate uses the lowest recorded window in the declared measurement interval, not an average chosen to pass.

{perf_table}

Heap maksimum per kasus memakai seluruh sampel final untuk run tersebut, termasuk transisi/idle; nilai window45s juga disimpan terpisah. Heap3000 gate: {next(q['heap800_mib_status']for q in benches if q['case']==3000)}. Raw result may have high frame medians while p5 drops sharply; this is not converted into a PASS. The reason for any long intervals is not proven as GPU saturation or browser throttling; visible/focus flags and raw durations remain evidence, not a diagnosis. CPU load/device state can affect results and the initial exploratory windows were kept separately, not silently merged into the final comparison.

## Consistent protocol

Same user Windows device,1920×1080/DPR1, fullscreen browser viewport, camera junction, speed1×, context on, no density/stopped overlay, nominal playbackt1800s. Each predeclared45s wall interval analyses seconds5–45 after5s settling. Actual stop time may be later due orchestration; the fixed analysis interval stays45s for everycase, recorded before inspection of results. Samples are logged about10s apart, each uses rolling120frames. Median of window FPS medians is reported, not a falsely precise lossless global frame median. Saved windows overlap; maximum stall count is not summed as unique stalls. Exact interval UTC boundaries and raw file list are in `benchmark-intervals.json` and `performance-summary.json`.

No demand totals, pending counts or active statistics were reduced to improve FPS. Rendered-instance range can be lower because actual camera frustum/LOD culls offscreen geometry; active remains actual recording count. No frame decimation or synthetic smoother flow was introduced.

## Browser soak

Final build tested: `{soak['build']}`. Start {soak['start_utc']}; end {soak['end_utc']}; elapsed wall {soak['elapsed_wall_s']:.1f}s, meeting minimum900s. Activity includes actual playback, four load levels, camera/recording switches, overlays, model review, inspector and UI operations. This is a mixed-activity soak, not15min uninterrupted playback at1×. Console errors/warnings at end: {soak.get('console_messages',[])}. All{len(rs)}saved renderer samples in this final session remain. Worst p5 across entire soak:{summary['minimum_p5_entire_soak']:.2f}FPS; maximum JS heap:{summary['maximum_heap_mib_entire_soak']:.1f}MiB, including transitions and idle. No claim of no memory leak from this bounded session.

## Device and loading

ASUS ROG Ally RC71L, installed RAM16GiB, OS usable11.70GiB, AMD Radeon Graphics/UMA.6GBVRAM allocation not independently certified. Heap is JavaScript heap, not total RAM/VRAM. Device state/thermal/power modes were not controlled as a laboratory benchmark. This evidence cannot certify every16GB/6GB Windows11 machine.

{table(['Run','Fetch/decode wall ms','Frames','Positions'],[[r['run_id'],f"{r['wall_ms']:.1f}",r['frames'],r['positions']]for r in loads])}

Loading timer measures actual recording fetch/decode. Reliable GPU first-present timing is MISSING; not included under a misleading loading claim. Raw renderer geometry/texture/drawcalls, viewport, speed, recordingID, active, camera, focus/visibility, and heap are preserved per sample. Bundle~848KB has Vite chunk>500KB warning; TypeScript and isolated build pass. No unsupported “6GB VRAM measured” or “all cameras always smooth” statement.
''')
 write('M15_6_REGRESSION_REPORT.md','Regression Report',f'''
## Results

Existing full suite:395tests,394passed,1legacy M09 presentation-service test skipped (service not running). Final focused M15.6 suite12testsPASS. One initial focused HTTP read failed with Windows connection reset on `/api/runs`; the initial log is retained, and the same unchanged test suite passed on rerun. No test was weakened or source network edited to force success. Logs: `regression-tests.txt`, `m156-tests-initial.txt`, `m156-tests.txt`.

Network byte hash stays `{EXPECTED}`. Scene lane/junction/head coordinate arrays exactly match export of frozen network. No edge/connection/rail/permission differences. Original M15.5 references include SHA256 result and output manifests; tests verify those retained results did not change.

Actual new100request run `{eq['new_run']}` compared against `{eq['original_run']}`: exact vehicle IDs/classes/routes/departure cohort equality and actual end statistics equality. Independent XML/FCD auditPASS, input/source/output manifests retained. Generator reproducibility, unsupported bicycle failure retention, manual exact totals, parent/new recording API access and manual save/load are tested. No override to force an illegal class through the network.

Live UI tests are separate from backend tests: Save/Load/Duplicate, date/time, rate/total/manual/random, preview, actual Generate, inspector, overlays, compare selector, playback controls, video and ten presets were exercised as recorded in `browser-workflow.json`. Ten vehicle envelopes/ground/distinctgeometry auditsPASS. GPU artwork approval and field calibration are not established by Python tests.

Preservation checkpoint: {protection['checked']}existingM15.5files checked, {protection['status']}, changed={protection['changed']}. Parent milestone snapshot of2984files also checked through prior preservation logic; M12 release and original network remain untouched. Staging5202 only writes newM156scenario/run/evidence namespaces. Old traffic code is imported read-only; new runner copies it only to select isolated output folders/source identity, not to change demand/control mathematics.
''')
 write('M15_6_ACCEPTANCE_REPORT.md','Acceptance Report',f'''
## Decision

**NOT AN UNCONDITIONAL PRESENTATION-GRADE ACCEPTANCE.** Visual implementation and functional checks delivered; network/traffic preservation verified. Visual quality requires user review; performance status **{summary['status']}**. Geospatial acceptance remains inheritedPARTIAL. A material/facade improvement is not a field-valid digital-twin certification.

{table(['Gate','Status','Evidence / boundary'],[
 ['Network/permissions/demand freeze','PASS within verified scope',EXPECTED],
 ['No flyover/road/frontage/rail change','PASS','Same XML and exported lane/junction/head coordinates'],
 ['Class-specific assets','PASS model audit / REVIEW artwork','10distinctgeometries, dimensions/ground contact exact; actual screenshots'],
 ['Trailer gandengan','VISIBLE assembly / LIMITED articulation','Tractor, coupling gap, cargo and axle group; rigidSUMOheading proxy'],
 ['Only actual moving traffic','PASS recorded checks','Retained FCD; rejected classes not placed in roads; separate labelled static asset preview'],
 ['Lights / barriers / train','PASS sampled model consistency','Actual event playback and rail traces; physical interlocking/clearance unverified'],
 ['Cameras / presentation / workflow','FUNCTIONAL with limits','10presets,pan/orbit/reset/follow, Save/Load/Duplicate, Generate, Inspector and overlays'],
 ['Actual screenshots / video','AVAILABLE','Allpreset captures, before/after, assetreview, livewatermarkedvideo'],
 ['Performance benchmark','COMPLETE / '+summary['status'],'4fixedwindows; low p5 retained; JS heap measured'],
 ['15minute browser soak','COMPLETED',f"{soak['elapsed_wall_s']:.1f}s mixed activity, not hours of stability"],
 ['Regression','PASS with one old skip','395existingtests/394pass/1skip;12focusedpass; assetaudits'],
 ['Preservation',protection['status'],str(protection['checked'])+'existingM15.5files equal plus ancestorcheckpoint'],
 ['Building physical accuracy','NOT VERIFIED','Public footprint download502; neutral assumed massing only'],
 ['Professional visual approval','REVIEW REQUIRED','Simplified shapes, neutral context and source road irregularities remain'],
 ['Geospatial / historical calibration','PARTIAL / NOT CALIBRATED','Inheritedlimitations not removed by rendering']])}

## Deliverables

- `M15_6_3D_VISUAL_REPORT.md`
- `M15_6_VEHICLE_ASSET_REPORT.md`
- `M15_6_PRESENTATION_MODE_REPORT.md`
- `M15_6_PERFORMANCE_REPORT.md`
- `M15_6_REGRESSION_REPORT.md`
- `M15_6_ACCEPTANCE_REPORT.md`

Source `frontend/src/m156`, isolated build `frontend/dist-m156`, backend `m156_*`, new runs `simulation/runs/m156`, evidence `documentation/m156`, launcher `staging/m156/START_M156.ps1`. Read-only parent recordings use original IDs/hashes. `artifact-manifest.json` covers source/build/report/evidence and run input/source/output manifests. The live staging remains http://127.0.0.1:5202/.

## Remaining limits

Review real video and every camera for aesthetic approval. Placeholder context is not surveyed Gedangan. Road/source geometry sharpness, provisional lane widths, restricted classes, one-direction rail and pending root-cause limitations remain. No attempt to smooth traffic by modifying model, inventing roads, hiding pending demand or replacing failures. Further optimization should address measured low frame windows and memory/load limits, with repeat measurements rather than sample deletion. No next milestone, final EXE, destructive cleanup or external upload was started.
''')
 print(json.dumps({'reports':6,'performance':summary['status'],'soak_wall_s':soak['elapsed_wall_s'],'preservation':protection},ensure_ascii=True),flush=True)
if __name__=='__main__':main()
