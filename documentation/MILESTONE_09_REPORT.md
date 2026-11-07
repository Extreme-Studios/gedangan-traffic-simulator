# MILESTONE 09 — GEDANGAN TRAFFIC SIMULATOR

**PRESENTATION DEMO READY · TECHNICAL ILLUSTRATIVE RELEASE**

2026-10-31T22:06:23.705358+00:00

## 1. Implementasi yang digunakan kembali

Audit M01–M08.5 dan source relevan disimpan di `m09/source-audit.json`. Registry/dimensi/access legality/OD M04–M04.5, geometri dan control M05/M05.1, data/provenance M06, projections M07, actual runs/guard M08 dan field-readiness M08.5 digunakan kembali. Tidak membangun simulator baru, mengubah engine, menimpa output atau mempromosikan synthetic ke observed. Permintaan M09 secara eksplisit mengizinkan demand ilustratif untuk presentasi; ini tidak membuka gate empirical calibration.

Pre-implementation checkpoint: 6.381 old files / sekitar 16.66 GB hashes, source ZIP 629 files, dependencies/toolchain/live SQLite/cache/M09 dikecualikan secara eksplisit. Source checkpoint dan scope lengkap di `m09/baseline-scope.json`. Regresi awal325 tests PASS, 128.574 s.

## 2. Implementasi baru

`backend/gedangan/m09_checkpoint.py`, `m09_export.py`, `m09_server.py`, `m09_reporting.py`; `frontend/presentation.html`, `src/m09/`, `vite.presentation.config.ts`; root launchers; `tests/m09/`; cache, manifests, QA dan dokumen `presentation_demo/m09/`. Semua namespace baru. Cache memuat 23 actual M08 recordings dan17paired comparisons. Tidak ada fresh SUMO run M09 yang diklaim: semuanya ekspor tervalidasi dari SUMO 1.28.0 yang benar-benar dijalankan pada M08.

## 3. 3D geometry methodology

SUMO local meters → Three.js: X=x−originX, Z=−(y−originY), Y=source Z atau 0 + surface offset. Original `.net.xml`/geometry authoritative. Lane strip memakai modeled width, junction memakai actual polygon, internal connectors tetap dibedakan, rail bukan road. Model area mengikuti convBoundary sekitar 4.3 × 4.5 km. Source attribution © OpenStreetMap contributors, ODbL 1.0, retained snapshot 2026-10-31.

Road/junction surfaces digabung untuk mengurangi draw calls, marking/material/furniture hanya render-only. Empty triangulation zero-area tidak dibaca sebagai vertex fiktif; perbaikan ini menghilangkan NaN tanpa mengganti centerline/topology. Lajur ~0.10 m dan inherited M05.1 shape displacement sampai ~7.178 m tetap dicatat, tidak diakali demi tampilan. Tidak ada elevation/bridge/ramp/connection baru. Model furniture dan geometri dekoratif bukan lokasi fisik yang disurvei.

## 4. SUMO playback synchronization

Ekspor streaming FCD XML0.5 s membentuk chunks 200 frames. Posisi/heading/speed/lane/type/IDs berasal langsung dari FCD. Independent same-vehicle matching terhadap snapshot TraCI5 s membuktikan label FCD+0.5 s cocok dalam <=0.03 m rounding pada setiap recording; clock tersebut dipakai pula untuk control events.

Interpolation hanya antar consecutive 0.5 s samples ID yang sama, angle memakai shortest wrap. Tidak muncul sebelum first frame atau setelah disappearance; gap/implausible displacement di-hold, bukan dirutekan ulang. Vehicle visual center berada setengah panjang di belakang FCD front bumper. Running-at-end tetap ada pada frame akhir; tidak dibuat arrival fiktif. Controls disampling 1 s, fidelity ini ditampilkan, tanpa mengarang missing intermediate state.

## 5. Vehicle visual design

Procedural low-poly motorcycle dengan roda/rider/handlebar; car dengan body/cabin/glazing/lights; pickup dengan bed; minibus/bus dengan jendela dan proporsi berbeda; light/medium/heavy trucks dengan cab/cargo/axles; corrugated trailer/container; kereta8 segmen 10 m mengikuti rail polyline di belakang recorded front. Instancing per part / type dan shared geometry menghindari ribuan object per vehicle.

Sembilan kelas jalan dan kereta difoto lewat actual vehicle picker pada 2040 HIGH. Dimensi berasal registry M04/model train, masih assumptions bukan hasil ukur armada Gedangan. Oversize tidak mempunyai valid record dan tidak ditampilkan. Colour/silhouette bukan pengenal identitas pribadi.

## 6. Railway / signal evidence

Actual crossing controller `osm_859708050` dan road controller `m05_gedangan` dibaca dari recorded events. Signal heads hanya dibuat untuk actual controlled connections dan linkIndex masing-masing; priority junction tidak diberi APILL rekaan. Scrub/reset menggunakan state terakhir yang sudah direkam pada clock sama.

Boom angles G/up, yellow/intermediate, red/down adalah schematic model state, bukan rekaman sudut sensor palang. Kereta/road response mengikuti trace aktual. Closed/train105.5 s dan release160s difoto. Tidak ada klaim actual timing/jadwal/stop line/gate/clearance atau swept-path field verified.

## 7. Camera system

Delapan mode: aerial master, main corridor, reverse, intersection, railway, frontage, follow selected vehicle dan free orbit. Anchor berasal lane geometry, controlled heads dan source crossing. Smooth exponential transitions, min height 7 m, orbit constraints dan reset. Split view menyalin pose/target kamera baseline; kedua panel memakai clock sama. Whole-network aerial membuat kendaraan skala meter kecil; close corridor/follow disediakan. Followtrain adalah closeup, bukan jaminan seluruh 80 m terbingkai; railway preset menunjukkan konteks keseluruhan.

## 8. Dashboard / UI

Satu entry GEDANGAN TRAFFIC SIMULATOR, EXTREME STUDIOS. Tujuh nav, scene dominan, compact selector, class filters, current active/stopped vehicle display, per-link APILL/crossing badges, horizon cards, collapsible analysis dan fullscreen. Tidak ada terminal/JSON/debug payload pada flow default.

Status per exact year/growth/scenario: RECORDED, NOT RUN, NOT SIMULATION READY atau CONCEPT ONLY. Source cohort metrics tetap utuh saat filter visual diubah; active-record counter diberi nama yang tidak mengklaim semua kendaraan sedang terlihat. Geometry/status/coreAPI errors ditampilkan jelas, tanpa fallbacktrajectory palsu.

## 9. 2026–2040 demo outputs

Seluruh45 M07conditional demand tables tersedia untuk 2026–2040×LOW/REFERENCE/HIGH. Recorded baseline REFERENCE untuk 2026/2030/2035/2040. S00–S04 hanya selectable sebagai rekaman bila exact combination tersedia; bukan semua combination otomatis dijalankan. Daftar23recordings di bawah adalah existing actual outputs; angka bukan pengamatan atau prakiraan resmi.

| Year | Growth | Scenario | Run | Requested | Arrived | Unserved at35 min |
|---|---|---|---|---|---|---|
| 2026 | REFERENCE | S00 | `7e4475b8c3ecdfa4b025` | 240 | 183 | 57 |
| 2026 | REFERENCE | S01 | `e123699c6b6c1169a364` | 240 | 185 | 55 |
| 2026 | REFERENCE | S02 | `edec692f96b10c6f9bd1` | 240 | 182 | 58 |
| 2026 | REFERENCE | S03 | `b508acf039d081329c7a` | 240 | 178 | 62 |
| 2026 | REFERENCE | S04 | `21a640bd45c810fef10d` | 240 | 181 | 59 |
| 2030 | REFERENCE | S00 | `af98a52bc855e571a5da` | 269 | 210 | 59 |
| 2030 | REFERENCE | S01 | `0e8e117bc8c9dd748d17` | 269 | 215 | 54 |
| 2030 | REFERENCE | S02 | `1f27e42dd39f9c37396b` | 269 | 210 | 59 |
| 2030 | REFERENCE | S03 | `40885ba6cee2c9e75912` | 269 | 203 | 66 |
| 2030 | REFERENCE | S04 | `8561749ea3a307e46086` | 269 | 204 | 65 |
| 2035 | REFERENCE | S00 | `7f08e6ef5870623160e4` | 311 | 240 | 71 |
| 2035 | REFERENCE | S01 | `e920640d22cc237763de` | 311 | 242 | 69 |
| 2035 | REFERENCE | S03 | `b11d31e57167222aea7c` | 311 | 230 | 81 |
| 2035 | REFERENCE | S04 | `a20837c2168d59bc80b2` | 311 | 235 | 76 |
| 2040 | HIGH | S00 | `f6b49f6119ee784cf062` | 500 | 356 | 144 |
| 2040 | HIGH | S01 | `9c9e07a0a18d0cfec64f` | 500 | 328 | 172 |
| 2040 | LOW | S00 | `e21233cd873d98ccfde9` | 252 | 194 | 58 |
| 2040 | LOW | S01 | `0db16f329f2618e4c381` | 252 | 197 | 55 |
| 2040 | REFERENCE | S00 | `60628c2402702667a3f0` | 360 | 282 | 78 |
| 2040 | REFERENCE | S01 | `6588c128003ce0c8dbbb` | 360 | 282 | 78 |
| 2040 | REFERENCE | S02 | `9438c051a9846e38c62b` | 360 | 278 | 82 |
| 2040 | REFERENCE | S03 | `c026e1d4667c65fc441b` | 360 | 255 | 105 |
| 2040 | REFERENCE | S04 | `565ddf032b0934470df8` | 360 | 272 | 88 |

## 10. Before / after evidence

M08guard memeriksa same original demand cohort, year/growth/seed/fixedhorizon, registry/projection/rail settings serta declared derivative delta. Ada17paired comparisons, dua trace terpisah. S01 memakai training-choice green 8 s dari seed 11 dan evaluationseed 42; bukan field optimization. S02/S03 mempersempit existing movement; S04 explicit deferral cost tetap dicatat. Tidak ada hidden demand disappearance/new road.

Requested = failed_routes + arrived + running_at_end + not_departed. Mean waiting/elapsed bersyarat pada departed cohort dan unfinished dipertahankan. Arrived-only benefit disuppressed ketika censored/unserved. Throughput arrivals/hour over35 min bukan measuredcapacity. Split screenshot menunjukkan posisi berbeda pada clock/kamera sama, tanpa overallpolicywinner.

## 11. Presentation workflow

START PRESENTATION menunggu5 main recordings selesai preload. Sepuluh bagian: intro, overview, main/frontage, railway, baseline, growth, congestion, valid operational intervention, comparison, fieldneeds. Talking points Bahasa Indonesia, next / previous, arrows, Space, Escape, fast restart dan fullscreen diuji. Escape kini diproses sebelum focus guard tombol; fullscreenchange juga menutup mode dengan benar. Sesi dapat diselesaikan tanpa terminal/JSON. Source notes jangan menyebut model sebagai pengukuran Gedangan.

## 12. Offline launcher

Root BAT dan wrapper presentation_demo/m09 memeriksa local Python / build / cache, cold-start read-only Python host, port 5185, meminta OS membuka dashboard, reuse duplicate service, error jelas dan clean shutdown. Cold launcher benar-benar dieksekusi; listener5185 dan HTML200/523bytes diverifikasi. OSbrowser-open request diuji melalui launcher; native default-browser pixels tidak diklaim terinspeksi. Actual sameURLrender/interactions diperiksa pada isolatedChrome.

Cache preload dan self-contained Vitebuild tidak perlu Node / SUMO live / internet untuk rapat. No firewall/security setting changes. Host / Origin exact loopback, self-only CSP, bounded inputs, file whitelist and chunked transport. Tidak ada simulation mutation endpoint. Native internal preview request returned queued; actualQA memakai bundled Playwright + installed Chrome.

## 13. Actual visual QA

18 automated browser flows PASS, nol current console errors / missing assets / external page requests, desktop 1920×1080, tablet 1024×768, mobile 390×844 tanpa horizontal overflow. Sepuluh actual class views PASS. Actual screenshots ditinjau; bukan mockup/rendersynthetic di luar recording. Browser external requests diblok selamaQA; adapter internet global tidak diubah.

Initial NaN berasal empty junction index fallback, diperbaiki hanya di renderer. Initial keyboard Escape focusbug diperbaiki dan assertions diperketat. Test harness networkidle diganti explicit asset / preload readiness. Full regression attempt pernah bersamaan rebuild dist sehingga FileNotFound; final serialized run PASS. Bukti awal tidak dijadikan PASS dan log relevan dipertahankan. Detail actual images dan limits di M09_VISUAL_QA_REPORT.md.

## 14. Regression tests

**344 Python tests PASS (125.889s): 325 legacy +19 M09.** Core 22 assertions PASS untuk transforms/frontbumper/heading/interpolation/birth/arrival/discontinuity/signalclock/runmatching/cameras. Browser 18 flows +10 actual class views terpisah, tidak dijumlahkan menjadi testcount buatan. TypeScript/build PASS. 6381 protected old-file hashes tetap cocok, mencakup source/config/dataset/output/reports / build lama; live SQLite/dependencies/cache scope dijelaskan pada checkpoint. Tidak menulis ulang M08.5 atau M06 status.

## 15. Performance evidence

Actual isolated Chrome 1920×1080 WebGL2 menggunakan ANGLE (AMD, AMD Radeon Graphics (0x000015BF) Direct3D11 vs_5_0 ps_5_0, D3D11). Playback full35 min pada16× selesai tanpa crash. Steady end window mean~119.8FPS, minimum reported p5 pada window tersebut~117.6FPS; target 30 FPS terlampaui pada pengukuran ini. Ini bukan worst case seluruh scenario atau native IAB benchmark. High density actual recording juga dijalankan/difoto; tidak diberi FPS garansi seluruh hardware.

JS heap sesudah GC sebelum 131,631,780B, sesudah131,793,156B. Bounded test ini tidak membuktikan nol leaks pada semua durasi/driver. Dispose geometry / material / textures / renderer / RAF / ResizeObserver diimplementasikan. WMI host Ryzen Z1 Extreme / AMD Radeon; physical memory / AdapterRAM advisory disimpan di hardware evidence. Tidak mengklaim6 GB VRAM terverifikasi.

## 16. Limitations

EMPIRICAL BASELINE tetap BLOCKED; OBSERVED GEDANGAN DATA belum dikumpulkan; source M08.5 tetap PARTIAL historis. Growth/demand/control/vehicleparameters assumptions. Buildings/trees/displaymarkings/poles/boom bukan physical survey. Source short lanes / angular junction dan unverified elevations tidak disembunyikan. No structural flyover / underpass/no false clearance or legal bypass. State fidelity1 s, FCD0.5 s; bukan live TraCI dashboard. Aerial far view intentionally overview. Browsercache warmup diperlukan sebelumStart; technical acceptance bukan final installer EXE atau photorealistic/as-built certification.

Independent selected-run export memberi identical 21 trajectory chunks masing-masing S00 / S01 dan semantically identical scene / metrics. Content-addressed shared scene dapat menyimpan first M08 network alias path, sedangkan independentexport memakai path byte-copy lain dengan hash sama; path provenance dan dependent digest dapat berbeda. Tidak mengklaim seluruhpackage byteidentical bila pathaliases berbeda. Dua Vite builds identikbyte-for-byte.

## 17. Acceptance per fitur

**PRESENTATION DEMO READY — untuk demonstrasi teknis ilustratif.** Empirical / policy / engineering feasibility gates tidak dipromosikan.

| Feature | Acceptance | Evidence / boundary |
|---|---|---|
| One-click launcher | PASS | Actual root BAT cold-started service; HTML200, auto-open request and duplicate/shutdown tests. |
| 3D source geometry | PASS_WITH_MODEL_LIMITS | M051/M08 lane/junction shapes unchanged; known ~0.10m lanes retained. |
| Vehicle visual classes | PASS | Nine actual road classes plus actual train photographed. Oversize not fabricated. |
| Recorded SUMO movement | PASS | 23 M08 recordings, .5 s FCD; independently checked +.5 s clock alignment. |
| Railway crossing | PASS_WITH_FIDELITY_LIMIT | Recorded road-link state and rail trajectories; schematic boom, 1 s state sampling. |
| Traffic signals | PASS_WITH_FIDELITY_LIMIT | Actual controlled links only, per-link recorded state; no invented priority-junction lamps. |
| Eight camera modes | PASS | Six presets, follow selection and free orbit; smooth transition/shared comparison camera. |
| Playback controls | PASS | Play/pause/reset/scrub/speed/filter/fullscreen exercised in browser. |
| Year and growth selection | PASS | Four main years recorded; all45 demand tables; unrecorded combinations NOT RUN. |
| Scenario selection | PASS | S00–S04 available where recorded; S05 blocked, S06/S07 concept only. |
| Statistics matched to run | PASS | Hash identities, fixed-horizon accounting and source metrics verified. |
| Before/after comparison | PASS | 17 fair pairs; separate traces, synchronized camera/time, M08 parity guard. |
| Presentation workflow | PASS | Ten steps, preloading, fullscreen, keyboard, restart/end and notes tested. |
| Offline demo | PASS | All page resources loopback; external requests blocked during QA; precomputed cache. |
| Runtime and layouts | PASS | No current console errors/missing assets; desktop/tablet/mobile and full35 min replay. |
| Visual review | PASS_FOR_TECHNICAL_MODEL | Actual screenshots reviewed; stylized context remains explicit. |
| Performance | PASS_SCOPED | Target30FPS exceeded in measured steady baseline windows; no all-workload/VRAM claim. |
| Regression / preservation | PASS | 344 Python tests +22 core assertions; 6381 old-file hashes unchanged. |
| Empirical validity | BLOCKED | No measured Gedangan baseline, policy recommendation or infrastructure feasibility certified. |

## 18. Remaining tasks for M10

Tidak ada M10–M12 dimulai. Kandidat pekerjaan berikutnya hanya dicatat: feedback presenter / instansi, broader headful / IAB / performance / hardware matrix, additional exact year / scenario actual runs sesuai kebutuhan, visual context yang memakai surveyed / authorized footprints bila tersedia, serta engineering review atas source short lane / elevation / clearance. Empirical calibration menunggu field data / review / independent validation dan instruksi terpisah. M09 tidak menghasilkan rekomendasi kebijakan atau klaim efektivitas riil.
