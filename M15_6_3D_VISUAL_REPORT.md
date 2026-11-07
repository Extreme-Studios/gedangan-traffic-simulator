# M15.6 — 3D Visual Report

2 November 2026, WIB. Separate staging http://127.0.0.1:5202/.

**MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.**

**PROVISIONAL NETWORK — NOT FIELD CALIBRATED.**

Network SHA256 `0b470d7ab9dff823efe96a2e286ec59a6c02b7735db9e653b666b15e567bb53c`. M12/M14/M15/M15.5 retained; no flyover, added road, permission change, GitHub upload or final EXE.

## Scope and evidence

Renderer changes live only in `frontend/src/m156`, build `frontend/dist-m156`, staging5202. Network/source lane arrays, junction boundaries and signal head coordinates equal the frozen original. Original demand builder, routing screens and controllers are inherited. No simulated road positions, widths, median openings, legal turns, frontage or rail alignment were altered for appearance.

## Environment

Shared procedural asphalt micrograin, neutral pavement tone, source-lane markings, stop-line render strips near the existing signal heads, rail steel/ballast/sleepers and controller-driven barrier geometry replace the colour-role map as default. Markings, sleeper gauge/spacing, furniture and assumed lane widths remain visual/model assumptions; not surveyed road paint. No unsupported sidewalk/shoulder/median infrastructure was invented. Source road ribbons/junction polygons remain, including sharp or irregular model junction boundaries; the milestone does not cosmetically move those into a smoother fictional road.

Lighting uses daylight hemisphere/key light, ACES output and static1024px soft context shadows. Vehicles retain local contact-shadows. Cars do not cast expensive per-vehicle dynamic shadow maps; ground-contact silhouette is a rendering approximation. This tradeoff is explicit, not a photometric validation claim.

Building request status: UNAVAILABLE. Two bounded requests to Overpass returned502; the second used a smaller bbox. No footprint dataset was recovered. Neutral off-road massing is therefore used, with clearly labelled assumed shapes/heights/furniture. It uses inherited clearance exclusion from road/rail polylines, avoiding generated mass on those paths; not certification against actual buildings. No arbitrary facade/window layout is presented as actual Gedangan. This is context, separate from the validated traffic graph.

The [OSM building-level documentation](https://wiki.openstreetmap.org/wiki/Key:building:levels) distinguishes a level tag from measured height. Because no footprint data was retrieved, no levels-derived or surveyed building height was claimed. Request provenance/errors are retained in `documentation/m156/building-source.json`.

## Movement, overlays and camera

Every moving vehicle comes from actual retained FCD or a new actual M15.6 SUMO run; no decorative traffic or pending vehicle instances. Endpoint samples stay unchanged. Inherited0.5s position/heading interpolation is a visual interpolation, not extra physical measurements. A train-normalization regression was found in actual camera QA and fixed before the final soak: road-envelope scaling now excludes the80m train contact footprint, preserving eight full-size coaches. Before-fix evidence is retained as failed QA, not acceptance evidence. `train-asset-audit.json` checks8coach lengths9–10.1m and10m spacing. Rail coaches follow inherited rail polyline sampling; signal lamps/barriers read recorded controller events. Selection follows actual vehicle IDs. No proof of continuous swept-path clearance is inferred.

Ten camera presets were inspected in the live browser: elevated, topdown, aerial, main, reverse, junction, rail, frontage, follow and orbit. Presenter can pan/orbit/zoom, reset camera and switch presets with smooth transition. Mouse interaction holds the user camera until a preset/reset instead of snapping back. Camera/viewport changes never alter simulation time or statistics.

Density overlay uses occupied length fraction on recorded lanes; stopped/queue overlay uses actual sampled speed<0.3m/s and sampled lane tail. Role/direction highlighting is network-derived. Vehicle label toggle is an actual-ID/speed roster capped12, not thousands of invented labels. Road label toggle is a source-name legend, not accurately geolocated text on every road. Signal/crossing status is recorded state. Network Inspector remains available outside presentation and hidden by default.

## Visual review status

**VISUAL QUALITY: REVIEW REQUIRED.** Materials, scale, context and presentation improved, but neutral placeholders, simplified wheels/riders/bodywork, coarse procedural grain in close views and inherited irregular road geometry remain visible. Do not call this a surveyed photorealistic Gedangan reconstruction or unconditionally professional-grade approved art. User visual review remains necessary. All actual preset screenshots, before/after views, model comparison and live video are under `documentation/m156/evidence/`; screenshot text is soft at the browser capture quality, while video watermarks were separately checked for readability.
