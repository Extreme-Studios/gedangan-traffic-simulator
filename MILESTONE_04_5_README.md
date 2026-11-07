# Gedangan M04.5 — Multiclass permission remediation

**SYNTHETIC TEST — NOT CALIBRATED GEDANGAN TRAFFIC.** M05 belum dimulai.

M03 asli memakai hardcoded passenger-only fixture. M04.5 membuat network turunan dengan policy per kelas, tanpa mengubah source/output M01–M04. Geometri, lajur, junction, internal shapes dan pasangan koneksi tetap identik; yang berubah hanya permissions dan provenance. Tidak ada legalitas lapangan atau clearance oversize yang diklaim.

## Jalankan dan rebuild

Dari folder `C:\Users\ROG ALLY\Documents\EXTREME STUDIOS\PROJECT\Simulasi Kemacetan Lalu Lintas`:

- `START_MULTICLASS_M045.bat`: preview di **http://127.0.0.1:5178/multiclass.html**, buka melalui browser internal Codex. Ctrl+C menghentikan preview. `--check` memeriksa prasyarat/port tanpa menjalankan server.
- `REBUILD_MULTICLASS_M045.bat`: permission-only rebuild NETCONVERT 1.28.0, compatibility 10 tipe × 9 OD pada dua varian, dua coverage simulations dan enam profil LOW/MEDIUM/STRESS. Hasil turunan M04.5 ditimpa; baseline M03/M04 tidak berubah. Tidak ada download.

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
cd frontend
.\node_modules\.bin\tsc.cmd --noEmit
.\node_modules\.bin\vite.cmd build --config vite.multiclass.config.ts
```

Build terpisah di `frontend/dist-m045/`. Registry dan OD/config M04 dibaca langsung tanpa diubah. Script tidak menjalankan growth, kalibrasi, kereta atau M05.

## Policy dan batas penting

`configuration/access-m045/policy.json` memisahkan enam SUMO vClasses dari sepuluh kategori lokal. Tag OSM yang paling spesifik berlaku dalam hierarki access → vehicle → motor_vehicle → mode. Conditional/lane-specific access yang belum dapat ditafsirkan ditahan secara konservatif; source turn restrictions tetap berlaku. Fitur yang telah dikecualikan M03 tidak dipulihkan.

Main arterial: ordinary light classes dan bus memakai INFERRED classification rule. Truck/trailer tanpa tag eksplisit hanya ASSUMPTION pada provisional main arterial. Strict tidak menganggap akses heavy yang hilang sebagai izin. Frontage: light classes saja; bus/truck/trailer membutuhkan bukti eksplisit, bukan otomatis disamakan dengan arterial. Local/service/private tidak dibuka otomatis untuk heavy. Service tanpa akses positif ditahan strict; provisional light access diberi ASSUMPTION.

INFERRED bukan kepastian hukum Indonesia. Tidak ada dokumen otoritas jalan yang telah memverifikasi izin spesifik rute ini. Route gate juga menerapkan eligibility/dimensi M04, numeric source restrictions dan clearance. Trailer standard hanya percobaan provisional arterial dengan nominal lane width margin 0,4m dan connector deflection ≤25°; belum swept-path/permit approval. Oversize selalu ditahan.

## Output dan viewer

- `backend/gedangan/m045_access.py`: policy, isolated M04 adapter, permission patch, audits, routing/geometry screens, simulation/export/manifests.
- `configuration/access-m045/`: input policy, rebuild dan preview launcher.
- `simulation/network/m045/{strict,provisional}/`: original-net + plain permission patches, NETCONVERT config/log, corrected network, source access ledger, exact geometry/permission audits, manifests.
- `simulation/demand/m045/`: request/trip/route/failure/interval records, compatibility dan manifests.
- `simulation/runs/m045/`: actual FCD setiap 1 detik, tripinfo, states, per-type lifecycle, metrics, config/log/manifests.
- `documentation/m045/`: QA, reproducibility, regression, screenshots dan issue resolution.

Viewer menyediakan **Network family** original/corrected, strict/provisional, coverage/LOW/MEDIUM/STRESS, type filter, class permission map, edge inspector per status, failures dan playback FCD. Angka original/corrected ditampilkan sebagai dua hasil software terpisah; tidak dipakai membuktikan manfaat kebijakan lalu lintas. Permission layer berbasis **vClass**; oversize memakai trailer vClass tetapi tetap diblokir oleh type-level clearance gate.

## SUMO-GUI

```powershell
& '.\toolchain\sumo-win64-1.28.0\bin\sumo-gui.exe' -c '.\simulation\runs\m045\m045-provisional-smoke-seed20261031\run.sumocfg'
```

Config menulis output run yang sama. Bila membuka GUI untuk inspeksi tambahan, override output ke direktori lain agar manifest headless tidak berubah, atau rebuild sesudahnya. Bukti GUI M04.5 memakai `documentation/m045/gui-*.xml` terpisah.

Laporan lengkap: `MILESTONE_04_5_REPORT.md` atau `documentation/MILESTONE_04_5_REPORT.md`.
