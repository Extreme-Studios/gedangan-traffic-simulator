"""Evidence-based M15 reports. Partial gates stay partial."""
import statistics,collections,re
from .m15_common import *
def table(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(str(v).replace('|','/')for v in row)+' |'for row in rows])+'\n'
def write(name,value):(ROOT/name).write_text(value.strip()+'\n',encoding='utf-8')
def main():
 rs=load(DOC/'one-hour-results.json');r=next(v for v in rs if v['requested']==3000);g=load(DOC/'geometry-audit.json');parent=load(DOC/'m14-reconstruction/reconstructed-result.json');changes=load(DOC/'approach-changes.json');signal=load(DOC/'signal-sensitivity.json');rail=load(DOC/'rail-sensitivity.json');turn=load(DOC/'actual-turns.json');manual=load(DOC/'manual-one-hour.json');fifteen=load(DOC/'total3000-15min.json');stop=load(DOC/'explanations'/(r['run_id']+'.json'));oldstop=load(DOC/'m14-reconstruction/stop-explanation.json');signal_audit=load(DOC/'signal-service-audit.json');before=load(DOC/'preservation-before.json');common=f"""
2 November 2026, WIB. Scope M15 only. All traffic inputs are MANUAL INPUT SCENARIO or RANDOMIZED SCENARIO — NOT FIELD OBSERVATION. No empirical Gedangan traffic calibration or claimed field capacity.

Staging: `http://127.0.0.1:5200/`; build `frontend/dist-m15/`; launcher `staging/m15/START_M15.ps1`. The existing M14 source/build/results and M12 release remain separate. Existing network `{str(NETWORK.relative_to(ROOT))}`, SHA-256 `{sha(NETWORK)}`. No flyover or M16 implementation. No permission override, forced insertion, new road/turn, geometry widening or removal of queued demand.
"""
 bt=table(['Requested','Routed','Loaded','Departed','Moved','Arrived','Active end','Pending end','Failed','Generation s','SUMO wall s','Total wall s'],[[v[k]for k in ['requested','routed','loaded','departed','moved','arrived','active','not_departed','failed_routes']]+[round(v[k],3)for k in ['generation_wall_s','simulation_wall_s','total_wall_s']]for v in rs]);at=table(['Approach','Input','Routed','Departed','Arrived','Active','Pending','Failed','Mean insertion delay s','Mean speed m/s','Mean waiting s'],[[a[k]for k in ['approach','input','routed','entering','exiting','active_at_horizon','pending','failed']]+[round(a[k],3)if a[k]is not None else'MISSING'for k in ['mean_insertion_delay_s_departed','mean_speed_m_s_analysis','mean_waiting_s_departed_censored']]for a in r['analysis']['approaches']]);oldat=table(['Approach','Input','Departed','Pending','Failed','Mean insertion delay s'],[[a[k]for k in ['approach','input','entering','pending','failed']]+[round(a['mean_insertion_delay_s_departed'],3)]for a in parent['analysis']['approaches']]);ct=table(['Approach','M14 catalog turns','M15 catalog turns','M14 route m','M15 route m'],[[a['approach'],', '.join(a['m14_turns']),', '.join(a['m15_turns']),round(a['m14_route_length_m'],2),round(a['m15_route_length_m'],2)]for a in changes]);boundary=table(['Cohort','Origin edge','Origin m','Upstream route m','Exit edge','Exit m'],[[a['approach'],a['origin_edge'],a['origin_length_m'],a['upstream_route_m'],a['exit_edge'],a['exit_length_m']]for a in g['boundaries']])
 def pair(p):return table(['Configuration','Run ID','Departed','Arrived','Mean waiting s','Signal transitions'],[[k,v['run_id'],v['departed'],v['arrived'],round(v['departed_mean_waiting_s'],4),v['signal_transitions']]for k,v in p.items()])
 perf=[]
 for q in (DOC/'browser-performance').glob('*.json'):
  v=load(q)
  if v.get('kind')=='render_sample':perf.append(v)
 pr=[]
 for v in [x for x in rs if x['requested']in [3000,5000]]:
  ss=[s for s in perf if s.get('recording')==v['run_id']and s.get('playing')and s.get('build')=='m15-ui-2-memo-map'];fps=[s['fps_mean']for s in ss];p5=[s['fps_p5']for s in ss];heap=[s['js_heap']['used']/1024**2 for s in ss if s.get('js_heap')];loads=[load(p)for p in (DOC/'browser-performance').glob('*.json')if load(p).get('kind')=='playback_load'and load(p).get('run_id')==v['run_id']];pr.append([v['requested'],len(ss),round(min(fps),2)if fps else'MISSING',round(statistics.median(fps),2)if fps else'MISSING',round(min(p5),2)if p5 else'MISSING',max((s['visible_vehicles']for s in ss),default=0),max((s['draw_calls']for s in ss),default=0),sum(s.get('stalls_over_50ms',0)for s in ss),round(max(heap),1)if heap else'MISSING',round(loads[-1]['wall_ms']/1000,3)if loads else'MISSING'])
 summary={'created_utc':now(),'rows':pr,'session_max_elapsed_s':max((p.get('session_elapsed_s',0)for p in perf),default=0),'note':'Active playback, memo-map build only. Stalls are sum of overlapping rolling-window observations, not unique stall count. Heap is JS telemetry, not whole browser/VRAM. Hardware not independently benchmarked.'};save(DOC/'performance-summary.json',summary);pt=table(['Demand/h','Samples','FPS min','FPS median','p5 min','Max active sampled','Max draw calls','Rolling stall observations','JS heap peak MiB','Latest load s'],pr)
 write('M15_NETWORK_GEOMETRY_AUDIT.md',f"""# M15 — Existing Network Geometry Audit
{common}
## Gate: GEOSPATIAL ACCEPTANCE = PARTIAL
The retained OSM/Overpass reference is dated {g['source_metadata']['osm_base_timestamp']}. Raw source hash `{g['raw_source_sha256']}`. The comparison projects EPSG:4326 to EPSG:32749 and applies the preserved SUMO netOffset {g['offset']}. OSM agreement is not independent field/survey verification or proof of a complete 2026 network.

{table(['Check','Measured result'],[['Road edges with OSM provenance',g['road_edge_count']],['OSM junction node comparisons',g['node_osm_comparisons']],['Maximum projected source/node difference m',round(g['max_node_projection_error_m'],6)],['Median road center/source-way offset m',round(g['median_centerline_source_offset_m'],6)],['Maximum road center/source-way offset m',round(g['max_centerline_source_offset_m'],6)],['Renderer/SUMO lane-shape error m',g['renderer_lane_shape_error_m']],['External lanes shorter than5m',g['short_external_under5m']],['Internal lanes shorter than5m',g['short_internal_under5m']],['New road edges/connections','0 / 0']])}
Centerline differences include lane offsets and junction trimming; no invented physical tolerance declares these safe. Very short edges occur at source splits, dead ends, signal/crossing segments and compact connectors. They are audited candidates, not automatically repaired by stretching or snapping. Lane widths remain inherited assumptions: {g['lane_widths_m']}. Source lane/direction tags and parameter statuses are preserved in `source-geometry-comparison.json`; speed, width, priority and capacity are often ASSUMPTION/MISSING.

## Corridor/name and rail coverage
{table(['Corridor','Named edges','Status'],[[n['corridor'],len(n['matched_edges']),n['status']]for n in g['named_corridors']])}
Northbound and southbound arterial directions are backed by directed source edges and signed connection chains. Sedati/Jenggolo/Jenggala names cannot be verified within this retained extent; they are not silently relabelled as Ketajen. M05.1 rail uses one directed mapped centerline and shared road crossing; a reverse track, precise physical gate/stop-line position and clearance remain UNVERIFIED. Existing restriction relations: {g['source_turn_restrictions']}; current network restrictions are retained.

## Boundaries and storage
{boundary}
These are experiment cohort entry/exit points inside the mapped network, not a surveyed external cordon. Rail-crossing origin is only6.63m long and has limited immediate insertion storage; its upstream chain ends after38.76m because the inherited same-role chain changes function. Frontage anchor is in the northern corridor, roughly1.4km from the central crossing; its default cohort does not fully represent central-frontage interchange demand. Ketajen and rail-crossing cohorts overlap the same corridor: they are distinct scenario IDs entering at different origins, not independent field traffic counts. Spatial/storage adequacy remains PARTIAL.

## Inspectable artifacts
- `documentation/m15/network-source-overlay.geojson`: georeferenced EPSG:4326 source/SUMO layers.
- `network-source-overlay.svg`, `technical-map.json`, `source-geometry-comparison.json`, `short-lanes.json`, `geometry-audit.json`.
- Interactive2D map in staging shows actual source, SUMO geometry, controllers, rail, route candidates, entry/exit and actual stopped-time hotspots.
- `documentation/m15/evidence/technical-map-sukodono-left.png`.

Legacy build note: the first build command selected the pre-existing M05.1 validation config and regenerated its compiled cache from unchanged source. M15 switched to unique `m15.html`/`vite.m15.config.ts`/`dist-m15`. All476 recorded primary M05.1 artifact hashes match the previous manifest. Prior compiled-cache byte parity is not independently asserted because its pre-turn digest was not recorded; see `legacy-build-note.json`. M14 and M12 were not overwritten.

No network derivative was justified: the proven fix is in catalog/routing through existing connections. Geometry doubts stay explicit. No flyover geometry is present.
""")
 write('M15_APPROACH_AND_TURNING_AUDIT.md',f"""# M15 — Approach and Turning Audit
{common}
## Root finding
M14 chose anchor-level signal connections. Ketajen, Sukodono and northbound signals are split points on a distributed junction, with only a straight immediate connection. Legal model branches occur at priority nodes after those signal splits. Thus straight-only lists were partly catalog extraction/boundary limitations, not proof that all other field turns are forbidden.

M15 traverses existing explicit connections from each signal anchor across compact split nodes, ending at the first longer outgoing corridor (over70m or accumulated200m; bounded16-link search). Local/service branches are not promoted to default primary corridor choices. Macro straight/left/right labels are INFERRED from incoming/outgoing headings; legality is screened per vehicle over all underlying lane-to-lane connections. No macro U-turn is invented. A turn absent from this selected catalog is not a blanket statement about every location in Gedangan.

{ct}
Changed catalog candidate chains, source edge IDs, origin/destination and route length before/after are in `documentation/m15/approach-changes.json`. Different exit choices/lengths mean M14 and M15 totals are not an isolated intervention comparison.

## Actual SUMO proof
Run `{turn['run_id']}`:120 manual cars,20 per cohort, distributed across all offered macro turns. Routed120; loaded{turn['loaded']}; departed{turn['departed']}; moved{turn['moved']}; arrived{turn['arrived']}; active{turn['active']}; failed{turn['failed_routes']}. Every offered approach/turn has at least one actual arrival. Each route follows explicit existing connections and class/access screens. `actual-turns.json`, run vehicle ledger/FCD and independent audit retain every ID. `actual-route-samples.geojson` exports12 actually traveled FCD trajectories (one per approach/turn) in EPSG:4326, including internal movement, with vehicle IDs and input/output provenance.

## Six-cohort limits
These six cohorts are useful model fixtures, not a complete directional OD survey. Frontage is northern. Railway road traffic also has a westbound connection but it is not a seventh selected cohort. Source U-turn connections elsewhere are not automatically offered. Named Sedati/Jenggolo/Jenggala coverage remains UNVERIFIED. User-selectable candidate examples are topology references, not permission for every class: heavy vehicles can still be denied feeder/local/width/conditional access routes.

Random default uses73%motorcycle,22%car,3%pickup/van,2%becak motor, all nominal assumptions supported on the default six straight routes. Bus/truck/trailer remain custom choices with per-approach compatibility shown. Bicycle/nonmotor becak are never converted to motorcycles; unsupported custom demand remains failed.
""")
 write('M15_DEMAND_CAPACITY_ANALYSIS.md',f"""# M15 — Demand Capacity and Insertion Analysis
{common}
## Input meaning
TOTAL3000/15min =3000 physical requests and12,000veh/h equivalent. RATE3000veh/h for15min =750 physical requests. RATE3000veh/h for60min =3000 requests. Conversion is displayed before Generate, recorded in `demand.json` and result.volume, and uses explicit half-up rounding for fractional physical counts. Manual per-class rates use largest-remainder allocation to the displayed converted physical total. Weighted mix/approach allocation preserves total and seed; no unsupported class substitution.

## Reconstructed M14 baseline
Source run `m14/67e1a759e0845754c09be215`:3000requested,2920routed,1271departed,566arrived,705active,1649pending,80failed. Read-only reconstruction uses original FCD/tripinfo with their hashes and a documented0.5s FCD-to-post-step clock offset.

{oldat}
Of 80 failed requests, 39 are bicycle-class denials; the other41 are19 light trucks,12 heavy trucks and10 buses. Detailed per-edge reconstruction shows truck lane-permission denials and bus road-function eligibility denials on the selected routes. Repeated blocked edges are not counted as extra vehicles; evidence is in `m14-reconstruction/failed-route-details.json`. No demand is lost. The1649pending are816northbound,725southbound,79Ketajen and29Sukodono. Their late insertion is measurable: original northbound departed vehicles average120.970s insertion delay, southbound82.078s. These are censored departed-cohort means, not delays for all requests.

## One-hour actual load tests
{bt}
These are tests of this uncalibrated model/configuration, not estimates of true Gedangan capacity. At500 and1000 demand/h all requests enter. At3000, pending1086; at5000, pending2615. Original phase/service, conservative route boundaries, priority/internal links and growing downstream queues can constrain throughput. No capacity/geometry parameter is inflated to force insertion.

## Explicit same-total duration contrast
The separate M15 TOTAL3000/15min run `{fifteen['run_id']}` produced{fifteen['departed']}departed,{fifteen['arrived']}arrived,{fifteen['active']}active and{fifteen['not_departed']}pending, with0failed routes. The one-hour run has the same physical request total at one quarter of the average demand rate. Train event times and analysis horizon also differ, so this is a descriptive duration/load contrast rather than an isolated causal timing test.

## Measured evidence versus inference
Delayed-insertion counts flag actual departDelay greater than one0.5s simulation step, separating ordinary discretization from longer delay. Mean insertion delay includes all departed vehicles. Each pending sample every10s records origin, class, approach, scheduled time, oldest censored delay, lane length/permission, active occupancy, observed local entry-free distance and nominal length+minGap requirement. The origin/class gap calculation is a conservative local proxy; it does not reproduce every SUMO braking, route-lane, downstream priority or crossing safety check, and cannot certify a precise rejection cause. A gap that looks sufficient can still fail safe insertion.

3000/60min grouped insertion sample classifications: {r['analysis']['pending_cause_counts']}. Counts are sampled groups, not unique vehicles. Queue boundary samples are not certified field spillback. At the horizon the live TraCI pending count agrees with scheduled-not-departed accounting. Per-ID insertion delay and censoring are in vehicle-results.json. No max-depart-delay removal or forced movement is used.

## Inspectable charts
`documentation/m15/evidence/pending-insertion-diagnostics.png`/`.pdf`, `one-hour-demand-accounting.png`; source hashes in chart-provenance.json. Interactive pending/active timeline and approach comparison remain visible in staging, including failed/pending demand.

Method reference: [SUMO Vehicle Insertion](https://sumo.dlr.de/userdoc/Simulation/VehicleInsertion.html). The application follows delayed-insertion accounting without applying insertion bypasses suggested as optional controls in other workflows.
""")
 write('M15_3000_VEHICLES_ONE_HOUR_TEST.md',f"""# M15 — 3,000 Vehicles / One Hour Test
{common}
## Actual run
ID `{r['run_id']}`. Seed42; date2026-11-02,start07:00WIB; rate3000veh/h; duration3600s; physical requested3000. Nominal runnable random mix, weighted actual approaches, uniform departures across12five-minute bins of250 requests each. Warm-up is first300s of this same horizon; analysis window300–3600s, without hidden extra demand. Signal assumption12/3/2s per protected phase, cycle153s; three assumed nominal KA events600/1800/3000s. Schedule is not official.

{table(['Lifecycle','Count'],[[k,r[k]]for k in ['requested','routed','scheduled_departure','loaded','departed','delayed_insertion_departed','moved','arrived','active','not_departed','failed_routes']])}
Requested=Routed+Failed; Routed=Departed+NotDeparted; Departed=Arrived+Active. All equalities hold. SUMO wall time{r['simulation_wall_s']:.3f}s; total compute{r['total_wall_s']:.3f}s. {r['quality']}. Teleports{len(r['teleports'])}, collisions{len(r['collisions'])}, illegal permission events{len(r['illegal_permissions'])}.

## Per direction
{at}
Northbound and southbound pending dominate. Low frontage waiting is not proof that all frontage traffic is uncongested: that selected cohort is smaller and spatially remote. Travel time is arrived-only and therefore censored; unfinished trips are retained. Means of waiting include departed but unfinished vehicles. Mean speed/density/stopped-time analysis excludes the warm-up window.

## Output/replay
`simulation/runs/m15/{r['run_id']}/`:demand.json, run.sumocfg, demand.rou.xml, controls.add.xml, FCD, summary/tripinfo/statistics XML, vehicle ledger, phase transitions, input/source snapshots/output hashes, approach/edge/insertion diagnostics and gzip playback chunks. TraCI samples0.5s; FCD interval-start clock +0.5s is checked against actual playback coordinates in independent XML audit. The original geometry hash is unchanged.

Video `documentation/m15/evidence/GEDANGAN_M15_3000_ONE_HOUR_ACTUAL.mp4` demonstrates a real excerpt of this one-hour run. It is not60minutes of realtime video or observed Gedangan footage. Video source/provenance and ffprobe metadata are saved separately. Screenshots show actual renderer positions, not decorative traffic.

## Conclusion
The one-hour request is actually executed and every ID accounted for. The model does not admit all3000within the hour under these assumptions. This is a documented model bottleneck, not a claim of measured road capacity or proof of presentation readiness.
""")
 write('M15_SIGNAL_RAILWAY_TEST.md',f"""# M15 — Signal and Railway Test
{common}
## Assumed controllers, no fictitious priority-node lights
M05_gedangan is an inherited distributed controller with27phases and9controlled links; baseline cycle153s. Each controlled link receives12s green per cycle (about7.84%); yellow3s and all-red2s per isolated-link sequence. At two-lane approaches the links are separate protected phases, not simultaneous full-road service. This conservative uncalibrated arrangement is a credible model constraint, not evidence of actual Gedangan timing.

All phase states/link indices and topology remain unchanged; edited durations are loaded as a separate M15 tlLogic program. Priority nodes downstream of split stop-lines are not converted to traffic lights. Detailed per-link red/green allocation: `signal-service-audit.json`. Actual transitions are recorded from SUMO.

## Paired signal test, one-hour500requests northbound
{pair(signal)}
Same seed/cohort/departure/network; green12→30s, cycle153→315s. Actual waiting and arrival change, proving controls affect traffic. This sensitivity is not a calibrated optimization or recommendation of official timing. The longer cycle also changes service to other links by design.

## Assumed railway test
One existing N_TO_S rail route,80m train, passing time converts to nominal speed; event list, delay, approach/closing headway, opening delay/time and minimum open/recovery are editable. Event frequency is controlled by the explicit arrival list. A nominal arrival is converted to an approximate free-flow departure; actual crossing samples and state transitions can differ. No reverse rail connection or exact official daily schedule is fabricated.

{pair(rail)}
400car requests on rail-crossing cohort, same seed/cohort; three assumed events versus none. Waiting changes from{rail['without_trains']['departed_mean_waiting_s']:.5f}s to{rail['with_trains']['departed_mean_waiting_s']:.5f}s. Arrival totals can be identical while queue/wait changes. This demonstrates in-model influence; it is not field closure evidence. Stop explanation samples and signals.json expose controller states at actual times.

Sources: inherited pilot config and network tlLogic; [SUMO Traffic Lights](https://sumo.dlr.de/docs/Simulation/Traffic_Lights.html), [SUMO Railways](https://sumo.dlr.de/docs/Simulation/Railways.html). Timing official verification remains MISSING.
""")
 write('M15_TRAFFIC_BEHAVIOR_REPORT.md',f"""# M15 — Traffic Behavior and Bottleneck Report
{common}
## Direction comparison,3000/60min
{at}
Entering/exiting here mean actual depart/arrival of the selected route cohort, not measured counts across a field cordon. Vehicle density is computed only where lane storage length and sampled vehicle-seconds exist: mean vehicle-seconds / analysis duration / lane-km. It includes the sampled edge's modeled lanes and is not calibrated saturation density. Stopped means speed<0.3m/s.

## Why vehicles stop
Recorded-control explanation at10s samples for3000/60min: {stop['counts']}. M14 reconstructed baseline: {oldstop['counts']}. A stopped head near a controlled link with recorded red/yellow is labelled as observed control state; downstream entry occupied is only a proxy. Queue bodies and head-near-junction priority/safety cases remain unresolved where evidence cannot distinguish causes. These sample counts overlap vehicles across time; they are not unique delayed vehicle counts or causal duration shares.

## Largest stopped-time model hotspots
{table(['Edge','Stopped vehicle-seconds','Max stopped/lane','Max stopped span m','Mean speed m/s','Mean density veh/lane/km'],[[e['edge'],round(e['stopped_vehicle_seconds'],1),e['max_stopped'],round(e['max_queue_extent_m'],2),round(e['mean_speed_m_s'],3),round(e['mean_density_veh_per_lane_km'],2)]for e in r['analysis']['bottleneck_candidates'][:10]])}
The congested mainline edges include upstream origins, so congestion cannot be summarized as an isolated central-junction queue. Pending accumulates outside the active network; its delay must not be omitted from a smooth-looking3D scene. Source geometry includes very short edges; controller service, priority links and finite storage jointly matter. No unsupported geometry correction is justified solely by a low throughput number.

## Interactive evidence
Preview also lists failed request counts by class/approach/turn and the first failing edge with an Indonesian explanation. The2D view overlays actual source/SUMO shapes, candidate routes, source-tag provenance, route entry/exit, signals/crossing and stopped-time hotspots. Choose an approach to inspect input/routed/entered/arrived/pending/failed; route candidates show explicit connection chains and destination choices. Saved-run comparison is descriptive and warns against causal interpretation across different inputs. Graphs show pending over time rather than hiding uninserted demand.

Data: `explanations/<run>.json`, per-run edge-diagnostics.json, insertion-samples.json, approach-analysis.json, demand-timeline.json and vehicle-results.json. Queue extent is a sampled model span. Boundary censoring is not certified physical spillback.
""")
 write('M15_PERFORMANCE_REPORT.md',f"""# M15 — Performance and Playback Report
{common}
## Actual compute
{bt}
Runs use SUMO1.28.0, step0.5s. Wall times include real local concurrent workloads; no isolated hardware certification. All5000requests are processed, but only{rs[-1]['departed']}depart and{rs[-1]['max_active']}is the maximum active count. Requested must not be equated with visible vehicles. Gzip playback loads the actual one-hour traces (7200frames), not generated decorative trajectories.

## Browser measurements
{pt}
These rows use active playback on the memo-map build. Measurements record mean FPS,p5, rolling stalls>50ms, sampled active count, draw calls, canvas/window dimensions, visibility/focus, session elapsed time and JS heap. A sum of rolling stall observations can double-count a stall; raw windows are preserved. Renderer active counts include recorded train objects when present and do not mean that every instance lies within the camera view; road accounting excludes the separately scheduled trains. FPS/counters update at sampled intervals. The viewport target was1920×1080, canvas height is smaller due controls. Heap is JavaScript telemetry only; it is not full browser RAM or VRAM. Compare actual per-sample dimensions in raw files.

## Performance finding and change
The first M15 build re-rendered the static SVG/source map and analysis table on every parent playback timestamp update. This produced low FPS despite the retained instanced3D renderer. React memoization now keeps static map/diagnostics work separate unless their result/selection changes. The M14 world/core renderer is retained; no premium redesign or fake fallback traffic was added. Early low/stalled samples remain in the audit, rather than being dropped to claim success.

Repeated run loading,3k→5k switching, high-active playback and camera switches were exercised in the internal browser. Latest observed session span{summary['session_max_elapsed_s']:.1f}s. Long-session memory is a bounded local observation only: garbage collection/load peaks and stalls remain visible; this is not a leak-free endurance certification. No promise of smooth performance across every Windows/AMD machine is made.

## Gate
PERFORMANCE ACCEPTANCE = CONDITIONAL. Actual playable workloads and the tested FPS/heap are evidenced, but initial stalls and short local endurance scope prevent an unconditional presentation-ready claim. See `performance-summary.json`, raw browser-performance files, browser QA evidence, video probe and screenshot artifacts.
""")
 reg=(DOC/'regression-tests-final.txt').read_text(encoding='utf-8')if(DOC/'regression-tests-final.txt').exists()else'PENDING';m15=(DOC/'m15-tests.txt').read_text(encoding='utf-8');match=re.search(r'Ran (\d+) tests',reg);test_count=int(match.group(1))if match else 0;test_ok='\nOK' in reg;xml=load(DOC/'xml-audit-summary.json')if(DOC/'xml-audit-summary.json').exists()else[];pres=load(DOC/'preservation-after.json')if(DOC/'preservation-after.json').exists()else{'status':'PENDING'}
 write('M15_ACCEPTANCE_REPORT.md',f"""# M15 — Acceptance Report
{common}
## Decision
FUNCTIONAL / ACCOUNTING: PASS within the tested existing model. GEOSPATIAL ACCEPTANCE: PARTIAL. PERFORMANCE / PRESENTATION: CONDITIONAL. The simulator now explains modeled congestion and pending insertion with inspectable evidence, but retained OSM alignment and backend tests do not establish field-valid or presentation-ready Gedangan behavior.

{table(['Gate','Status','Evidence / limit'],[
['Existing source alignment','PARTIAL','OSM/source/SUMO overlay; independent survey and naming gaps remain'],['Road/rail topology','MODEL VALID / PARTIAL physical','Existing connection graph unchanged; single rail direction'],['Approach provenance','PASS selected cohorts','Source IDs, anchor nodes and boundary table; not complete field OD'],['Legal model turns / no fabricated turn','PASS','120 actual cars across all offered turns arrived; connection/type screens'],['Volume total vs rate','PASS','3000/h ×15min=750; TOTAL3000/15min=12000/h equivalent'],['Seed/composition conservation','PASS','Reproducible generator and manual-rate rounding tests'],['Unsupported classes warned','PASS','Per-approach support and explicit rejection reasons shown; custom failures retained'],['3000/60min actual SUMO','PASS','3000routed,1914departed,1346arrived,568active,1086pending'],['Mass balance/no missing vehicles','PASS','Requested/routed/departed partitions and XML audit'],['Pending explained','PASS with causal limits','Origin/class/time/gap/permission and queue evidence; unresolved cases explicit'],['Bottleneck location','PASS model evidence','Per-edge stopped time, storage boundary and control samples'],['Signal influence','PASS model sensitivity','Edited duration actually loaded; arrival/wait changes'],['Railway influence','PASS model sensitivity','Same400-car cohort with/without trains, actual wait change'],['Playback actual traces','PASS tested','FCD/TraCI0.5s clock check; no renderer fallback traffic'],['No flyover / M16','PASS','Existing geometry hash unchanged; no added topology'],['Inspectable2D map','PASS','Interactive source/SUMO/route/control/queue/pending view'],['Regression','See final test logs','Missing old M14 service corrected before final rerun'],['Preservation','{status}'.format(status=pres['status']),str(len(before['files']))+' source/input/output hashes compared'],['Performance assurance','CONDITIONAL','Measured workloads, stalls, memory and bounded session scope'],['Field calibration / official timing','MISSING','Manual/random scenarios are not historical observations']])}
## Validation evidence
Final regression: {test_count} tests, status {'PASS'if test_ok else'PENDING_OR_FAILED'}, one M09 presentation-service CLI test skipped because that legacy presentation service is not running. The remaining {test_count-1} passed. Logs: `documentation/m15/regression-tests-final.txt` and `m15-tests-final.txt` (21 M15 tests pass after the final failure-explanation endpoint was added). TypeScript type check and isolated production build pass. Browser Generate100/hour also completed3600s:100routed/departed/moved,93arrived,7active,0pending,0failed; Save/Duplicate/Load restored the100/hour request. See `browser-workflow.json`. Independent XML/FCD audits currently{len(xml)}runs, all pass={bool(xml)and all(a['status']=='PASS'for a in xml)}; final artifact manifest records source/output hashes. Initial regression failures were two old M14 HTTP tests because its service was not running; source was not changed to bypass them. The original M14 service was started and the suite rerun. M15 staging is separate5200.

## Remaining issues
Retained geometry/width/clearance and official signal/train timing remain unverified. Sedati/Jenggolo/Jenggala naming and full boundary/approach coverage are incomplete. Frontage is spatially remote; Ketajen/rail-crossing fixtures overlap corridor space. Pending1086at3000/h and2615at5000/h are retained; no model capacity inflation hides them. Gap and spillback indicators are proxies where direct cause is not available. The data cannot be presented as measured traffic or an empirically calibrated capacity study.

## Deliverables and workflow
Eight root M15 reports; separate frontend/backend staging; source/network GeoJSON/SVG overlay; route changes and samples; actual one-hour500/1000/3000/5000runs; manual multiclass and actual-turn tests; paired signal/rail tests; per-ID/edge/approach insertion diagnostics; charts, real3D screenshots and a real excerpt video. Save/Load/Duplicate and descriptive comparison use scenario-only JSON storage.

Open localhost5200, choose date/startWIB, total/rate and60min, edit mix/seed/approaches, Preview, Generate SUMO, inspect progress/result/pending causes and Play. Save a scenario or compare a retained run. No source or data is uploaded to GitHub, no research deletion, no replacement M12 EXE and no M16/flyover work.
""")
 print('8 M15 reports written',flush=True)
if __name__=='__main__':main()
