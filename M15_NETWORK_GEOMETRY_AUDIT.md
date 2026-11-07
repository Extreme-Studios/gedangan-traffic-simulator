# M15 — Existing Network Geometry Audit

2 November 2026, WIB. Scope M15 only. All traffic inputs are MANUAL INPUT SCENARIO or RANDOMIZED SCENARIO — NOT FIELD OBSERVATION. No empirical Gedangan traffic calibration or claimed field capacity.

Staging: `http://127.0.0.1:5200/`; build `frontend/dist-m15/`; launcher `staging/m15/START_M15.ps1`. The existing M14 source/build/results and M12 release remain separate. Existing network `simulation\network\m051\provisional\network.net.xml`, SHA-256 `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. No flyover or M16 implementation. No permission override, forced insertion, new road/turn, geometry widening or removal of queued demand.

## Gate: GEOSPATIAL ACCEPTANCE = PARTIAL
The retained OSM/Overpass reference is dated 2026-10-31T04:34:22Z. Raw source hash `4bc46117ffae23aa90ade1e9c155601cfd90217cbca82c5bcc69fedbae0849f1`. The comparison projects EPSG:4326 to EPSG:32749 and applies the preserved SUMO netOffset [-690790.39, -9182879.52]. OSM agreement is not independent field/survey verification or proof of a complete 2026 network.

| Check | Measured result |
| --- | --- |
| Road edges with OSM provenance | 1961 |
| OSM junction node comparisons | 1040 |
| Maximum projected source/node difference m | 0.012178 |
| Median road center/source-way offset m | 1.593831 |
| Maximum road center/source-way offset m | 3.731212 |
| Renderer/SUMO lane-shape error m | 0.0 |
| External lanes shorter than5m | 546 |
| Internal lanes shorter than5m | 1911 |
| New road edges/connections | 0 / 0 |

Centerline differences include lane offsets and junction trimming; no invented physical tolerance declares these safe. Very short edges occur at source splits, dead ends, signal/crossing segments and compact connectors. They are audited candidates, not automatically repaired by stretching or snapping. Lane widths remain inherited assumptions: {'3.2': 5299, '3.0': 13, '2.0': 17}. Source lane/direction tags and parameter statuses are preserved in `source-geometry-comparison.json`; speed, width, priority and capacity are often ASSUMPTION/MISSING.

## Corridor/name and rail coverage
| Corridor | Named edges | Status |
| --- | --- | --- |
| A. Yani | 16 | OSM_NAMED_REFERENCE |
| Sukodono | 67 | OSM_NAMED_REFERENCE |
| Ketajen | 124 | OSM_NAMED_REFERENCE |
| Frontage | 17 | OSM_NAMED_REFERENCE |
| Sedati | 0 | UNVERIFIED_NAME_NOT_FOUND_IN_RETAINED_EXTENT |
| Jenggolo | 0 | UNVERIFIED_NAME_NOT_FOUND_IN_RETAINED_EXTENT |
| Jenggala | 0 | UNVERIFIED_NAME_NOT_FOUND_IN_RETAINED_EXTENT |

Northbound and southbound arterial directions are backed by directed source edges and signed connection chains. Sedati/Jenggolo/Jenggala names cannot be verified within this retained extent; they are not silently relabelled as Ketajen. M05.1 rail uses one directed mapped centerline and shared road crossing; a reverse track, precise physical gate/stop-line position and clearance remain UNVERIFIED. Existing restriction relations: 72; current network restrictions are retained.

## Boundaries and storage
| Cohort | Origin edge | Origin m | Upstream route m | Exit edge | Exit m |
| --- | --- | --- | --- | --- | --- |
| ketajen | w266287937_s5_p0_0_r | 85.25 | 457.46 | w266287931_s20_p0_0_r | 24.92 |
| sukodono | w266287931_s19_p0_0_f | 91.25 | 510.26 | w266287937_s9_p0_0_f | 68.28 |
| southbound | w512351908_s1_p0_0_f | 169.3 | 550.57 | w562358499_s0_p0_0_f | 609.77 |
| northbound | w562358500_s11_p0_0_f | 101.25 | 437.93 | w512351906_s1_p0_0_f | 141.84 |
| frontage | w1181141358_s0_p0_0_f | 186.25 | 186.25 | w321936840_s0_p0_0_f | 730.56 |
| rail_crossing | w266287934_s0_p0_0_f | 6.63 | 38.76 | w266287937_s9_p0_0_f | 68.28 |

These are experiment cohort entry/exit points inside the mapped network, not a surveyed external cordon. Rail-crossing origin is only6.63m long and has limited immediate insertion storage; its upstream chain ends after38.76m because the inherited same-role chain changes function. Frontage anchor is in the northern corridor, roughly1.4km from the central crossing; its default cohort does not fully represent central-frontage interchange demand. Ketajen and rail-crossing cohorts overlap the same corridor: they are distinct scenario IDs entering at different origins, not independent field traffic counts. Spatial/storage adequacy remains PARTIAL.

## Inspectable artifacts
- `documentation/m15/network-source-overlay.geojson`: georeferenced EPSG:4326 source/SUMO layers.
- `network-source-overlay.svg`, `technical-map.json`, `source-geometry-comparison.json`, `short-lanes.json`, `geometry-audit.json`.
- Interactive2D map in staging shows actual source, SUMO geometry, controllers, rail, route candidates, entry/exit and actual stopped-time hotspots.
- `documentation/m15/evidence/technical-map-sukodono-left.png`.

Legacy build note: the first build command selected the pre-existing M05.1 validation config and regenerated its compiled cache from unchanged source. M15 switched to unique `m15.html`/`vite.m15.config.ts`/`dist-m15`. All476 recorded primary M05.1 artifact hashes match the previous manifest. Prior compiled-cache byte parity is not independently asserted because its pre-turn digest was not recorded; see `legacy-build-note.json`. M14 and M12 were not overwritten.

No network derivative was justified: the proven fix is in catalog/routing through existing connections. Geometry doubts stay explicit. No flyover geometry is present.
