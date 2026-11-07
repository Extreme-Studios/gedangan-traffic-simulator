# M03 Connectivity and QA Report

This report separates weak node geometry connectivity from permitted edge transitions. Neither is field-validated traffic legality.

| Variant | Nodes | Edges | Lanes | Weak node components | Weak transition components | Strong transition components |
|---|---:|---:|---:|---:|---:|---:|
| strict | 225 | 241 | 323 | 15 | 78 | 241 |
| provisional | 1022 | 1961 | 2043 | 23 | 67 | 1030 |

## Unresolved findings

Strict excludes unsupported directions/cross-way turns. Provisional admits direction assumptions only for a highway whitelist. No components are joined to reduce the count. Every resulting geometric component maps to one original M02 component; see each connectivity.json.

NETCONVERT warnings remain in the complete initial/final log JSON: sharp radii/angles, intersecting lane turns in provisional initial construction, and missing incoming/outgoing lane connections. Generated junction curves and lane assignment are assumptions. No automatic geometry straightening, intersection merging or field repair is claimed.

### strict
- No incoming movement: 78 edges; no outgoing: 78. These include boundary terminals, barrier quarantines and deliberate withheld turns.
- Warning lines: initial 5, final 13; repeated-message summaries mean this is not a count of unique physical defects.
- Automatically generated lane connections removed: 66; unapproved connections remaining: 0.
- Source decisions: {'INCLUDED': 215, 'EXCLUDED': 1202}.
- Source restriction IDs applied/quarantined: [9529520, 13817610, 13850953, 13850954, 14983465, 14998364, 15973419, 17165949, 17167748, 17419538].

- direction: {'VERIFIED': 241}
- lanes: {'ASSUMPTION': 144, 'VERIFIED': 97}
- speed: {'ASSUMPTION': 227, 'VERIFIED': 14}
- lane_width: {'ASSUMPTION': 241}
- capacity: {'MISSING': 241}
### provisional
- No incoming movement: 358 edges; no outgoing: 357. These include boundary terminals, barrier quarantines and deliberate withheld turns.
- Warning lines: initial 16, final 26; repeated-message summaries mean this is not a count of unique physical defects.
- Automatically generated lane connections removed: 51; unapproved connections remaining: 0.
- Source decisions: {'INCLUDED': 1055, 'EXCLUDED': 362}.
- Source restriction IDs applied/quarantined: [9529520, 13817610, 13850953, 13850954, 14983465, 14998364, 15973419, 17044859, 17165949, 17167748, 17419538].

- direction: {'ASSUMPTION': 1720, 'VERIFIED': 241}
- lanes: {'ASSUMPTION': 1864, 'VERIFIED': 97}
- speed: {'ASSUMPTION': 1947, 'VERIFIED': 14}
- lane_width: {'ASSUMPTION': 1947, 'INFERRED': 14}
- capacity: {'MISSING': 1961}

## Restrictions and grade separation

Via-node restrictions prohibit exact source from/to ways. Via-way and conditional restrictions are conservatively quarantined at the from-way entry into via-ways, possibly blocking otherwise permitted movements; no claim of exact dynamic restriction modelling. Explicit U-turns/reverse movements are globally withheld. Missing turn/access tags do not prove real-world legality.

Access/private/no/destination/customer/permit-class restrictions are excluded for the passenger test harness; mapped barrier nodes block transitions conservatively. Actual dynamic crossing operations and signal timing are deferred.

Bridge/tunnel flags and node IDs are retained; different OSM nodes are never joined for spatial proximity, including grade-separated crossings. OSM source topology itself still needs field review.

Both directions of the main corridor were tested by DUAROUTER. Strict has deliberately failed branch/endpoint cases; provisional successes are assumptions, not a calibrated traffic model. See route-test-results.json for endpoints, exact edge sequence, router execution and failure reasons.
