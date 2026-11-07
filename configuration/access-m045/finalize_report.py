"""Integrity audit and M04.5 report from actual recorded outputs."""
from pathlib import Path
import hashlib
import json
import shutil
import sys
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from backend.gedangan.m045_access import DOC,NET,RUNS,DEMAND,CONF,BASE,load,save,sha,baseline_check,adapter

def main():
    baseline_check();runs=load(DOC/'run-summary.json');compat=load(DOC/'compatibility-results.json');policy=load(CONF/'policy.json');browser=load(DOC/'browser-qa.json');assert browser['status']=='PASS' and browser['positionsMatchRecordedSUMO'] and not browser['console']
    count=0
    for base in [NET,DEMAND,RUNS]:
        for p in base.rglob('manifest.json'):
            manifest=load(p)
            for name,h in manifest['files'].items():assert sha(p.parent/name)==h,(p,name)
            for name,h in manifest['input_sha256'].items():assert sha(ROOT/name)==h,(p,name)
            count+=1
    before=load(DOC/'reproducibility.json')['after'];current={'networks':{mode:hashlib.sha256(ET.tostring(ET.parse(NET/mode/'network.net.xml').getroot())).hexdigest() for mode in ['strict','provisional']},'trajectories':{str(p.relative_to(RUNS)).replace('\\','/'):sha(p) for p in RUNS.rglob('trajectory.json')}};assert before==current
    web=ROOT/'frontend/public/access/m045';dist=ROOT/'frontend/dist-m045/access/m045'
    for p in web.iterdir():
        if p.is_file():assert p.read_bytes()==(dist/p.name).read_bytes(),p
    tests=(DOC/'tests.txt').read_text(encoding='utf-8-sig');assert 'Ran 112 tests' in tests and tests.rstrip().endswith('OK')
    for mode in ['strict','provisional']:
        assert load(NET/mode/'geometry-audit.json')['geometry_sections_changed']==[];assert not load(NET/mode/'permission-audit.json')['internal_lane_mismatches']
    roots=load(DOC/'root-cause-audit.json');lifes={mode:load(RUNS/next(r['run_id'] for r in runs if r['network_variant']==mode and r['profile']=='smoke')/'class-lifecycle.json') for mode in ['strict','provisional']}
    byid={v['id']:v for v in adapter.registry()}
    coverage='\n'.join(f"| {v['label']} | {v['sumo_vclass']} | {lifes['strict'][v['id']]['routable']} / 9 | {lifes['provisional'][v['id']]['routable']} / 9 | {lifes['provisional'][v['id']]['loaded']} | {lifes['provisional'][v['id']]['departed']} | {lifes['provisional'][v['id']]['moved']} | {lifes['provisional'][v['id']]['arrived']} | {9-lifes['provisional'][v['id']]['routable']} |" for v in adapter.registry())
    matrix='\n'.join('| '+v['label']+' | '+' | '.join(next(r['route_status'] for r in compat['provisional'] if r['vehicle_type_id']==v['id'] and r['od_id']==od) for od in ['northbound','southbound','frontage_continuity','feeder_to_main','station_junction'])+' |' for v in adapter.registry())
    totals='\n'.join(f"| {r['network_variant']} | {r['profile']} | {r['requested_trips']} | {r['routable_trips']} | {r['failed_routes']} | {r['loaded_vehicles']} | {r['departed_vehicles']} | {r['moved_vehicles_recorded']} | {r['arrived_vehicles']} | {r['teleported_vehicles']} |" for r in runs)
    policyrows=[]
    for mode in ['strict','provisional']:
        for vc,counts in load(NET/mode/'permission-audit.json')['decision_counts'].items():policyrows.append(f"| {mode} | {vc} | {counts.get('VERIFIED_ALLOW',0)} | {counts.get('INFERRED_ALLOW',0)} | {counts.get('ASSUMPTION_ALLOW',0)} | {counts.get('MISSING_DENY',0)} |")
    perf='\n'.join(f"| {r['network_variant']} / {r['profile']} | {r['wall_seconds']:.3f} | {r['process_cpu_seconds']:.3f} | {r['peak_working_set_bytes_sampled']/1048576:.1f} |" for r in runs)
    report=f'''# MILESTONE 04.5 — Multiclass Network Permission Remediation

Tanggal: **31 Oktober 2026**. Proyek: `C:\\Users\\ROG ALLY\\Documents\\EXTREME STUDIOS\\PROJECT\\Simulasi Kemacetan Lalu Lintas`.

**SYNTHETIC TEST — NOT CALIBRATED GEDANGAN TRAFFIC.**

## Hasil utama dan status

**M04.5 selesai untuk remediation software, uji multiclass dan acceptance teknis dengan batas sumber yang eksplisit.** Sembilan kategori non-oversize terbukti dirutekan, dimuat, berangkat, berpindah posisi dan tiba pada corrected provisional main corridor. Strict juga menjalankan motorcycle, passenger, pickup/van, minibus dan bus sesuai policy. Oversize tetap ditolak. Seluruh 112 tes, TypeScript/production build, internal browser dan pemeriksaan SUMO-GUI lulus.

Original M03/M04 dipertahankan. Tidak ada geometri, junction, lane shape/dimensi atau pasangan koneksi baru. Tidak ada vClass ignoring, override TraCI, auto route repair, restorasi ruas yang sudah dikecualikan M03, data survei rekaan atau pekerjaan M05. **Izin model yang inferred/provisional tidak sama dengan legalitas lapangan terverifikasi.**

## Akar masalah

`configuration/network-m03/build_network.py` baris **{roots['literal_locations'][0]['line']}** menulis literal `'allow':'passenger'` ke setiap plain XML edge. Itu filter fixture passenger M03, bukan hasil pemetaan OSM per kelas. NETCONVERT mewariskan batas tersebut ke external lanes dan internal links. Original strict mempunyai 323 road lanes dan provisional 2.043 road lanes, semuanya passenger-only. Permission probe M04 menolak kelas lain secara benar berdasarkan input ini; penyebabnya bukan kegagalan vehicle registry atau bug SUMO.

Audit meliputi converter/policy M03, plain edge/lane XML, NETCONVERT input/output, class permissions, OSM tags/raw restriction relations, registry M04, compatibility dan issue M03-PERM-01. Detail sumber, hash dan literal ada di `m045/root-cause-audit.json`. Tidak ada explicit per-class access tag pada 83 arterial edges dan 17 frontage edges sumber. Karena itu, pembukaan kelas tambahan tidak diberi status VERIFIED tanpa tag positif.

## Source code dan struktur turunan

- `backend/gedangan/m045_access.py`: evaluator access hierarchy; permission patch/NETCONVERT; audit geometri dan internal permissions; private M04 adapter; physical/type/route screens; simulation, FCD, lifecycle dan manifest.
- `configuration/access-m045/policy.json`: class hierarchy, road-role rules, status/provenance, conditional quarantine dan trailer trial guard.
- `configuration/access-m045/rebuild.py`, `start_preview.py`, `finalize_report.py`; root `REBUILD_MULTICLASS_M045.bat` dan `START_MULTICLASS_M045.bat`.
- `simulation/network/m045/{{strict,provisional}}/`: corrected networks, `.edg.xml`/`.con.xml` permission patches, NETCONVERT config, access decisions, geometry/permission audits, logs dan manifests.
- `simulation/demand/m045/`: compatibility/request/trips/routes/failure records, OD interval counts dan manifests.
- `simulation/runs/m045/`: delapan actual runs, tripinfo, FCD, state/metric/per-type lifecycle, config/log/manifests.
- `frontend/multiclass.html`, `src/m045/`, config/build `dist-m045/`; viewer baru terpisah dari M04.
- `tests/m045/`: 24 tests tambahan; 88 tests M01–M04 tetap utuh.

M04 registry, OD matrix, profiles dan model Krauss/LC2013 digunakan tanpa diubah. Adapter memuat modul M04 dalam instance privat; tidak mengganti global pada modul original atau mengubah output lamanya. Reuse route checks diperluas untuk menghormati **corrected connection-class permission** dan access hierarchy, bukan hanya blanket passenger filter.

## Kebijakan akses dan provenance

Urutan evaluasi: explicit OSM access hierarchy → dokumen jalan terverifikasi bila tersedia → classification inference terdokumentasi → provisional assumption bila diizinkan. Belum ada dokumen otoritas jalan spesifik yang memverifikasi izin/clearance kendaraan untuk ruas ini; tier tersebut tetap MISSING, tidak diganti dengan klaim hasil riset.

Hierarchy memakai access → vehicle → motor_vehicle → motorcycle/motorcar/goods/psv/bus/hgv/hgv:articulated. Key lebih spesifik, termasuk arah forward/backward sesuai source order, mengalahkan key umum. `yes/designated` eksplisit diberi VERIFIED terhadap tag OSM. `no/private/destination/customers/delivery/permit` dan purpose limits lain ditolak sesuai hierarki; nilai ambigu ditahan. Conditional dan lane-specific access yang belum dapat ditafsirkan dikarantina, bukan dianggap yes. Generic turn restrictions dan class-specific/conditional/via-way relations juga diperiksa; exception M03 tidak dipakai untuk memulihkan gerakan yang telah diblokir.

| Road role | Strict access tanpa tag positif | Tambahan provisional | Batas |
|---|---|---|---|
| Main arterial / trunk | motorcycle, passenger, delivery, bus: INFERRED | truck/trailer: ASSUMPTION | Bukan izin legal lokal yang sudah disurvei |
| Frontage / tertiary | motorcycle, passenger, delivery: INFERRED | Tidak ada heavy otomatis | Bus/truck/trailer butuh explicit class evidence |
| Feeder / collector | motorcycle, passenger, delivery: INFERRED | bus: ASSUMPTION | Type-specific M04 eligibility/dimensi tetap membatasi full-size bus |
| Local residential/living street | light classes: INFERRED; tag eksplisit diprioritaskan | Tidak ada heavy otomatis | Ketiadaan larangan tidak diubah menjadi kepastian hukum |
| Service | Positive source only; missing ditahan | light classes: ASSUMPTION | Bus/truck/trailer tidak otomatis diizinkan |
| Private/limited/conditional | Sesuai restriction paling spesifik; unresolved ditahan | Tidak dibuka sebagai jalan umum | M03 exclusions tidak dipulihkan |

`VERIFIED` berarti tag sumber mendukung keputusan, bukan legalitas lapangan. `INFERRED` adalah interpretasi classification/hierarchy untuk model. `ASSUMPTION` adalah temporary access trial. `MISSING` berarti dasar izin belum cukup sehingga ditahan. Tiap edge/class menyimpan keputusan, status, basis, source way/tags, provenance M045-ACCESS-01 dan field_legal_verified=false.

| Variant | vClass | VERIFIED allow edges | INFERRED allow edges | ASSUMPTION allow edges | MISSING denied edges |
|---|---|---:|---:|---:|---:|
{chr(10).join(policyrows)}

Angka dihitung per directed edge, bukan jalan fisik atau hasil survei. Dua edge provisional bertag access=permissive ditahan konservatif sebagai akses yang tidak cukup pasti. Explicit class-positive evidence dapat mengalahkan generic access, tetapi tidak memulihkan ruas/topologi yang sudah hilang dari baseline M03.

### Heavy dan oversize gate

Registry M04 menjaga bus besar/truk sedang/berat/trailer pada main arterial, serta minimal nominal width = vehicle width + 0,4m. Truk ringan juga tunduk pada class truck policy, sehingga tidak otomatis masuk permukiman/service. Source maxwidth/height/length diperiksa numerik; unknown/unit/conditional clearance ditahan. Source weight/axle restrictions ditahan karena registry tidak mempunyai mass/load bersumber.

Trailer nominal 16,5m × 2,55m × 4m hanya percobaan **provisional arterial**, margin width nominal dan source-centreline connector deflection ≤25°. Ini screen konfigurasi sementara, bukan swept-path analysis, clearance jembatan/tinggi/beban atau permit. Kurva internal tetap hasil engine M03. Oversize 20m × 3m × 4,5m selalu NOT_ROUTABLE sampai geometri/legalitas/swept-path clearance tersedia. Walaupun vClass-nya sama dengan trailer, type-level gate tidak membiarkannya masuk accepted routes.

## Network sebelum dan sesudah

SUMO NETCONVERT **1.28.0** lokal memuat original `.net.xml` bersama plain permission edge/lane/connection patches. `.net.xml` final tidak diedit manual. Connection permission adalah irisan izin from/to lane, dipersempit restriction sumber. Tidak ada permission pada internal lane yang lebih luas dari union gerakan yang menggunakannya.

| Variant | Original → corrected nodes | Edges | Road lanes | External lane connections | New movements | Geometry sections changed |
|---|---:|---:|---:|---:|---:|---:|
| Strict | 225 → 225 | 241 → 241 | 323 → 323 | 242 → 242 | 0 | 0 |
| Provisional | 1022 → 1022 | 1961 → 1961 | 2043 → 2043 | 2874 → 2874 | 0 | 0 |

Audit exact XML mempertahankan location/projection/offset, node/junction coordinates dan shapes, seluruh external/internal edge IDs, lane shapes/length/width/speed dan connection tuples. Tidak ada join/straightening/connection baru. Oneway, withheld U-turn, boundary, barrier dan restriction M03 tetap berlaku. Main dan frontage tetap mempunyai source way terpisah. M03 source exclusions, 29 source components dan batas legal-turn/control sebelumnya tidak dianggap selesai oleh perubahan izin ini.

Audit internal: zero mismatches pada kedua varian. NETCONVERT warning mengenai terminal/withheld connections tetap disimpan, tidak disembunyikan. Fixture traffic signal/rail dinamis tidak ditambahkan.

## Compatibility dan lifecycle per kategori

Coverage memakai sepuluh kategori × sembilan OD = 90 requested cases per varian. Departures diselang 3s untuk pemeriksaan kendaraan, berbeda dari fixture coverage M04 yang lebih awal. Ini bukan demand lapangan dan bukan kontrol eksperimen kinerja trafik. LOW/MEDIUM/STRESS tetap memakai OD/type/departures M04 yang identik, hanya ID prefix dan network family yang dibedakan.

| Kategori | vClass | Strict routable / requested | Provisional routable / requested | Loaded provisional | Departed | Moved in FCD | Arrived | Failed provisional |
|---|---|---:|---:|---:|---:|---:|---:|---:|
{coverage}

Loaded per tipe berasal dari actual tripinfo records; departure/arrival dari vehicle states, movement dari perubahan posisi >1m pada FCD 1s. Seluruh kategori non-oversize mempunyai actual northbound arrival dan displacement >50m. Total teleport **0** membuktikan tidak ada kelas yang menyelesaikan perjalanan melalui teleport pada run ini. Failure tetap disimpan per requested ID.

| Kategori — provisional | Main NB | Main SB | Frontage continuity | Feeder → main | Station/Ketajen |
|---|---|---|---|---|---|
{matrix}

Minibus dan full-size bus berbagi vClass bus tetapi mempunyai eligibility M04 berbeda; izin lajur bus tidak otomatis membuktikan bus besar cocok untuk semua feeder. Strict masih menahan empat OD branch/endpoint lama: feeder→main, main→feeder, frontage exit dan station east. Permission remediation tidak menciptakan belokan atau endpoint agar seluruh rute berhasil.

## LOW, MEDIUM dan STRESS corrected runs

Tiga profil sintetis M04 digunakan: 40/120/300 requested trips per 900s, seed 20261031, baseline schema 2026. Simulasi 0–2100s, step 1s, M04 car-following/lane-change/dimensi tetap ASSUMPTION. DELIBERATE failure tidak dihapus dari denominator. DUAROUTER repair=false; ignore-errors melanjutkan kasus lain tetapi setiap yang tidak terbit direkonsiliasi ke ledger.

| Variant | Profile | Requested | Routable | Failed | Loaded | Departed | Moved | Arrived | Teleports |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
{totals}

Pada delapan run corrected: exit 0, warning SUMO kosong, pending insertion/running at end 0, dan semua accepted tiba. Penundaan insertion sesaat masih mungkin; GUI heavy truck mencatat depart delay 9s. Pending akhir nol tidak berarti tidak pernah ada attempt tertunda. Summary/tripinfo lengkap dipertahankan. Route failure warnings dan NETCONVERT warnings tetap ada di log masing-masing.

Original M04 runs tetap tersedia terpisah dan tidak ditimpa. Coverage original strict 5/90 dan provisional 9/90, semuanya passenger; corrected strict 21/90 dan provisional 48/90. Angka ini menunjukkan coverage software/izin, **bukan** kenaikan kapasitas, kelancaran atau manfaat kebijakan. FCD original 5s dan corrected 1s juga berbeda; jumlah movement samples tidak dibandingkan sebagai metrik kinerja trafik.

## SUMO-GUI dan browser evidence

SUMO-GUI 1.28.0 actual membuka corrected provisional coverage. Vehicle Chooser memperlihatkan motor, pickup, minibus, bus, truk dan trailer. Truk berat northbound yang dipilih berada di lane w35344052_s3_p0_0_f_0 dengan odometer **553,57m**, posisi 72,38m dan speed 8,29m/s. Run GUI berhenti sekitar 104s: loaded 41, inserted/running 26, arrived 0, collisions/teleports 0. Tidak mengklaim GUI pendek ini menuntaskan demand; arrival dibuktikan run headless 2100s. Output GUI terpisah, tidak merusak manifest hasil utama.

![SUMO-GUI multiclass IDs](m045/sumo-gui-multiclass-list.jpg)

![Actual heavy vehicle parameters](m045/sumo-gui-heavy-parameters.jpg)

Internal browser menguji seluruh 16 family/variant/profile combinations, sepuluh type selectors, actual lifecycle/route ledger, permission/OD layer, source edge lookup, frontage heavy denial, arterial ASSUMPTION dan oversize failure. Playback 0→83s memuat berbagai kelas, dan semua marker pada frame 83s cocok dengan actual FCD x/y. Reset/scrub sampai 646s berfungsi. Desktop 1920×1080 dan viewport 390×844 tidak overflow horizontal; console warn/error kosong. Build produksi diverifikasi terpisah; UI QA memakai dev preview, bukan deployment. Lihat BROWSER_QA.md dan browser-qa.json.

![M04.5 browser](m045/browser-final.jpg)

![Frontage heavy access withheld](m045/browser-frontage-permissions.jpg)

## Regression, build dan reproducibility

**112/112 tests PASS**: 88 M01–M04 dan 24 M04.5. Tes memeriksa baseline hashes, private adapter isolation, root cause, exact geometry/structural connections, hierarchy/conditional/private/directional rules, heavy/frontage/service policy, source status, actual external/internal lane permissions, class-specific restrictions, numeric clearance, actual routes/lifecycle kedua arah, oversize rejection, OD/type/departure conservation, manifests dan viewer export.

TypeScript noEmit dan Vite production build `dist-m045/` PASS. Peringatan createRoot saat hot reload viewer diperbaiki dengan reuse root host M04.5; reload dan interaksi akhir mempunyai console bersih. Tidak ada kebutuhan install dependency baru. Source/output preexisting yang dijaga berjumlah **633 file** dan seluruh SHA-256 tetap sama, termasuk network M03, registry/config/OD dan hasil M04. Tidak ada data sintetis masuk observed_data.

Full rebuild benar-benar dijalankan: semantic XML network pada kedua varian dan seluruh delapan recorded trajectory JSON identik hash sebelum/sesudah. XML timestamp comments dan wall/CPU/RAM readings tidak dijanjikan byte-identik. Manifest mencatat original/corrected network hash, source policy/registry/config/OD/raw/mapping/code hashes, SUMO version, seed, simulation period dan seluruh output. Files baru M04.5 dibangun dari sumber lokal tanpa fetch.

## Performance observations

Pengukuran proses headless lokal, bukan benchmark GPU/VRAM atau klaim kondisi trafik. Windows process working-set disampel sekitar 20ms; proses pendek bisa melewatkan peak. Horizon tiap run 2100s. Profil diuji bertingkat, paling besar 300 requested, bukan ribuan kendaraan serentak.

| Variant / profile | Wall seconds | CPU process seconds | Sampled peak working set MiB |
|---|---:|---:|---:|
{perf}

## Acceptance dan isu yang belum selesai

| Kriteria | Status dan batas |
|---|---|
| Seluruh regresi M01–M04 lulus | PASS; 88 lama + 24 baru |
| Motor dan beberapa non-passenger bergerak | PASS; sembilan kategori non-oversize main NB provisional, lima kategori strict |
| Parameter akses/source jelas | PASS; per-edge/class ledger, hierarchy, tier/status dan missing authority evidence |
| Frontage terpisah | PASS; source/geometri tetap, heavy tidak otomatis diizinkan |
| Original M03 immutable | PASS; original beserta M04 outputs tetap identik |
| Corrected reproducible | PASS; full semantic network/trajectory rebuild proof |
| Tidak ada bypass legalitas | PASS pada model/source constraints; tidak berarti legalitas lapangan tersertifikasi |
| Oversize tetap dibatasi | PASS; 0 routed/loaded/departed/arrived |
| Browser dan SUMO-GUI actual | PASS; screenshot, logs dan FCD match |
| Sintetis tidak dipresentasikan sebagai pengukuran | PASS; labels dan provenance tetap eksplisit |

M03-PERM-01 **remediated pada turunan M04.5**, bukan ditutup dengan menulis ulang baseline. Masih perlu verifikasi otoritas/lapangan atas akses per kelas, load/height/width dan operasi frontage; swept-path kendaraan panjang; legal restriction conditional/via-way yang sekarang dikarantina; source roads yang dikecualikan M03; serta control/connector geometry assumptions dan empat OD strict yang gagal. SUMO lane compatibility tidak membuktikan kemampuan fisik kendaraan articulated atau izin melintas nyata.

Kesiapan menuju M05: fondasi multiclass teknis kini tersedia untuk tahap berikutnya dengan batas tersebut. Kalibrasi perilaku, operasi rel/palang, signal plan final, OD/volume aktual, growth dan flyover comparison **belum dikerjakan**. **M05 tidak dimulai dan menunggu persetujuan pengguna.**

## Referensi

- [OSM access hierarchy](https://wiki.openstreetmap.org/wiki/Key:access): hubungan generic/mode-specific restriction; bukan dokumen izin lokal Indonesia.
- [OSM highway classification](https://wiki.openstreetmap.org/wiki/Key:highway): dasar classification inference model yang dinyatakan eksplisit.
- [OSM conditional restrictions](https://wiki.openstreetmap.org/wiki/Conditional_restrictions): kondisi yang belum terselesaikan ditahan.
- [SUMO Plain XML](https://eclipse.dev/sumo/docs/Networks/PlainXML.html): patch plain XML melalui NETCONVERT, tanpa hand edit network.
- [SUMO vehicle permissions](https://eclipse.dev/sumo/docs/Simulation/VehiclePermissions.html): vClass dan lane access; diperiksa pada toolchain 1.28.0 lokal.
- [OpenStreetMap contributors / ODbL](https://www.openstreetmap.org/copyright): sumber geografis M02/M03 yang dipertahankan.
'''
    (ROOT/'documentation/MILESTONE_04_5_REPORT.md').write_text(report,encoding='utf-8');(ROOT/'MILESTONE_04_5_REPORT.md').write_text(report.replace('(m045/','(documentation/m045/'),encoding='utf-8')
    save(DOC/'final-validation.json',{'status':'PASS_TECHNICAL_REMEDIATION_WITH_DOCUMENTED_ACCESS_ASSUMPTIONS','tests_passed':112,'prior_tests_passed':88,'preserved_files':633,'verified_manifests':count,'browser_qa':'PASS','geometry_drift':False,'new_connections':0,'all_corrected_runs_arrived_without_teleport':all(r['routable_trips']==r['arrived_vehicles'] and r['teleported_vehicles']==0 for r in runs),'rebuild_semantic_networks_and_trajectories_identical':True,'oversize_routed':0,'field_legal_verified':False,'m05_started':False})
    review=Path(r'C:\Users\ROG ALLY\Documents\Codex\2026-10-31\files-pasted-by-the-user-milestone\outputs\Gedangan-M04-5');review.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/'documentation/MILESTONE_04_5_REPORT.md',review/'MILESTONE_04_5_REPORT.md');shutil.copy2(ROOT/'MILESTONE_04_5_README.md',review/'MILESTONE_04_5_README.md');shutil.copytree(DOC,review/'m045',dirs_exist_ok=True);shutil.copy2(CONF/'policy.json',review/'access-policy.json')
    print(json.dumps(load(DOC/'final-validation.json'),indent=2));print('Review outputs:',review)

if __name__=='__main__':main()
