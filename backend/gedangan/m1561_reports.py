"""Location-direction evidence and honest incomplete visual acceptance."""
from .m1561_common import *
from collections import Counter
import math
def main():
 protect();s=load(DOC/'scene.json');b=s['environment']['buildings'];audit=load(DOC/'context-placement-audit.json');refs=load(DOC/'source-register.json');p=verify();assert p['status']=='PASS',p
 ancestor=load(ROOT/'documentation/m155/preservation-before.json')['files'];changed=[q for q,h in ancestor.items()if not(ROOT/q).is_file()or sha(ROOT/q)!=h];assert not changed,changed;save(DOC/'ancestor-preservation.json',{'checked':len(ancestor),'changed':changed,'status':'PASS','method':'Read-only hash comparison; no parent report rewritten'})
 header='2 November 2026, WIB. Staging terpisah: http://127.0.0.1:5203/.\n\n**ASSUMED CONTEXT MODEL.** Bentuk/posisi/tinggi bangunan bukan hasil survei.\n\n**MANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.**\n\n**PROVISIONAL GEDANGAN NETWORK — NOT FIELD CALIBRATED.**\n\n'
 context=Counter(x['kind']for x in b);station=next(x for x in b if x['kind']=='station');point=s['environment']['station']['point'];offset=math.hypot(station['x']-point[0],station['y']-point[1])
 environment=f'''# M15.6.1 — Gedangan Environment Report

{header}
## Status

Arah visual baru sudah diimplementasikan. **Visual acceptance masih PENDING karena Browser Use ditolak oleh Work settings.** Lima screenshot 1920×1080 dan video aktual 45–60 detik belum tersedia. Build atau pemeriksaan source tidak dipakai sebagai pengganti inspeksi browser. Bukti M15.6 tidak diberi label ulang sebagai M15.6.1.

## Lingkungan yang diubah

Blok massing lama diganti dengan {len(b)} model rendah: {context['ruko']} ruko, {context['house']} rumah, {context['workshop']} workshop, dan satu model konteks stasiun. Tinggi dinding maksimum {audit['height_max_wall_m']:.2f} m; termasuk atap maksimum {audit['height_max_total_m']:.2f} m. Tidak ada tower, gedung kaca, skyline CBD, atau skybox perkotaan.

Ruko memakai modul rolling shutter, kanopi, dan bukaan lantai atas bila dua lantai. Rumah memakai atap pelana berwarna genteng, bukaan sederhana, dan pagar rendah. Workshop memakai atap metal. Palet cream, abu, sage, dan bata dibuat tenang. Beberapa plot mempunyai pohon kecil, bentuk tanaman menyerupai palem, dan tiang utilitas. Bentuk, spesies, ukuran, jumlah, posisi, dan pemakaian plot semuanya asumsi visual.

Ada {sum(math.hypot(x['x'],x['y'])<500 for x in b)} model dalam radius 500 m koordinat lokal simpang. Bangunan mengikuti arah koridor sumber dengan setback dan celah bervariasi. Tidak ada akses jalan baru yang dibuat untuk bangunan. Area yang tidak lolos pemeriksaan ruang tetap dibiarkan kosong.

## Stasiun dan referensi lokasi

Anchor stasiun berasal dari retained OSM node 1359952188. Model konteks memakai dinding cream/grey, atap genteng miring, teritis, dan bukaan berulang. Referensi karakter adalah [foto Stasiun Gedangan 2020](https://commons.wikimedia.org/wiki/File:Stasiun_Gedangan_2020.jpg), karya Rizal Febri Ardiansyah, 12 September 2020, berlisensi [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Foto lokal benar-benar diperiksa; hash dan atribusi ada pada source register. Foto tidak ditempel sebagai facade, aerial background, atau pengganti model 3D.

Model stasiun berukuran asumsi 12×27 m, dinding 4.1 m dan atap 1.7 m. Anchor render berjarak {offset:.2f} m dari node sumber agar tidak menutupi road/rail buffer. Ini keputusan penempatan visual, bukan ukuran footprint atau gate stasiun yang terverifikasi. Label GEDANGAN menandai konteks, bukan sertifikasi rekonstruksi gedung aktual.

[Kajian PTDI-STTD 2024](https://digilib.ptdisttd.ac.id/8270/) memberi konteks simpang utama, simpang stasiun, frontage, dan rel. Teks publik diperiksa, tetapi screenshot PDF timeout; tidak mengklaim foto PDF berhasil diperiksa. Proposal infrastruktur dalam penelitian tidak dimasukkan sebagai kondisi eksisting.

Retained OSM 31 Oktober 2026 dan [Peta Jalan Pemkab Sidoarjo](https://sidoarjokab.go.id/peta-jalan) tetap menjadi referensi geografis road/rail. Attempt baru untuk building footprint melalui Overpass Kumi timeout. Tidak ada footprint baru, citra satelit, atau rekonstruksi posisi dari street view yang berhasil diperoleh. Karena itu semua bangunan tetap **ASSUMED CONTEXT MODEL**. Foto historis tidak dipakai untuk mengklaim kondisi lengkap 2026.

## Jaringan dibekukan dan ruang kendaraan dilindungi

Network SHA256 tetap `{EXPECTED}`. Lane shape, junction polygon, signal heads, presets, crossing, dan bounds sama persis dengan scene M15.6. Alignment jalan/rel, frontage, width, median, legal turning, permissions, demand, traffic model, dan statistik tidak diubah.

Polygon penuh setiap model, termasuk margin kanopi dan pad, diperiksa terhadap seluruh lane asli. Buffer road memakai setengah lebar SUMO ditambah 2.5 m; rail memakai buffer 7 m dari centerline. Hasil: nol overlap dengan envelope tersebut dan nol overlap antarmodel. Transform yaw mengikuti konversi XY SUMO ke X/−Z renderer. Pemeriksaan ini adalah screen geometri model, bukan sertifikat clearance bangunan atau swept path lapangan.

Kereta, lampu, palang, kendaraan, dan arah gerak tetap memakai actual playback. Tidak ada track balik, platform operasional, akses stasiun, atau jalan tambahan yang dibuat. Kelas yang gagal rute tetap gagal; konteks visual tidak menambah kendaraan bergerak.

## UI dan kamera

Dashboard/header gelap, viewport dominan, analytics, current/end statistics, Inspector, dan watermark dipertahankan. Preset baru adalah Overview Gedangan, Frontage Relationship, dan Presentation Dashboard. Kamera main corridor, close-up junction, rail, follow, top-down, aerial, dan orbit tetap tersedia.

Frontage Relationship memakai midpoint antara preset frontage asli dan crossing. Frontage tidak dipindah agar terlihat dekat. Peta jaringan kecil memakai koordinat SUMO dan titik kendaraan aktual yang disampel untuk keterbacaan; active count tidak dikurangi. Material aspal dihaluskan melalui noise dan UV rendering, bukan perubahan geometri.

Recorder disiapkan untuk 50 detik live canvas 1920×1080 dengan watermark, timestamp, dan end counts. **Recorder belum dijalankan pada M15.6.1 karena browser diblokir.** Tombol siap tidak berarti video telah tersedia. FPS/heap M15.6.1 belum diukur; masalah memori M15.6 belum dinyatakan selesai.

## Aset dan Blender

Blender tidak digunakan. Aset dibuat native procedural Three.js agar batching, material, dan provenance penempatan dapat diperiksa langsung. Tidak ada file blend/GLB atau klaim export Blender. Karena Blender tidak dipakai, laporan Blender opsional tidak dibuat.

Daftar aset ada di `documentation/m1561/environment-assets.json`: ruko rendah, rumah beratap genteng, workshop, konteks stasiun, vegetasi, utilitas, dan plot tanah. Source berada di `frontend/src/m1561/LocalContext.ts`. Vehicle asset dan traffic logic lama dipertahankan. Tidak ada paid asset, generated photo, aerial-photo-as-3D, atau brand bangunan rekaan.

## Pengujian dan preservasi

Sepuluh tes M15.6.1 lulus: network hash, kesamaan scene, batas low-rise, label asumsi, pemeriksaan polygon penuh, pemisahan bangunan, batas anchor stasiun, hash foto, hasil parent tetap utuh, dan XML identik. TypeScript dan isolated Vite build lulus. Chunk JS sekitar 850.57 KB masih memberi warning lebih dari 500 KB. Ini bukti kode/model, bukan bukti kualitas visual atau performa browser.

Preservasi M15.6: {p['checked']} file lama diperiksa, status {p['status']}, tanpa perubahan. Checkpoint ancestor {len(ancestor)} file juga hash-equal melalui pembandingan read-only; laporan parent tidak ditulis ulang.

Staging berada di port 5203, source `frontend/src/m1561`, build `frontend/dist-m1561`, evidence/data `documentation/m1561`, dan launcher `staging/m1561/START_M1561.ps1`. M12 hingga M15.6 tidak ditimpa. Tidak ada penghapusan, upload GitHub, final EXE, atau milestone lanjutan.

## Pekerjaan yang tertahan

Setelah Browser Use aktif: ambil screenshot overview, intersection, railway crossing, frontage relationship, dan presentation mode pada 1920×1080. Periksa atap, facade, ground contact, coverage koridor/stasiun, serta posisi kendaraan dan kereta. Rekam actual playback 45–60 detik lalu periksa frame awal/tengah/akhir serta metadata. Nilai kecocokan lokasi secara jujur; jangan memberikan PASS jika masih terasa metropolitan atau seperti arena mainan.
'''
 review=f'''# M15.6.1 — Location Context Review

{header}
## Keputusan

**Implementasi selesai pada source/build; review visual belum selesai.** Browser Use ditolak oleh Work settings. Lima screenshot baru dan video aktual 45–60 detik belum tersedia. Status kualitas lokasi tetap **PENDING**, bukan PASS.

| Pertanyaan | Bukti source/model | Review visual aktual |
| --- | --- | --- |
| Masih terasa CBD/kota besar? | Tidak ada tower atau skyline; seluruh model rendah, maksimum {audit['height_max_total_m']:.2f} m termasuk atap | Belum dinilai di browser |
| Konteks Gedangan mulai terasa? | Road/rail freeze, OSM station anchor, referensi foto stasiun Gedangan, ruko/rumah beratap genteng | Menunggu overview, crossing, dan frontage inspection |
| Bangunan masih terlalu generik? | Ya, masih archetype. Footprint, posisi, tinggi, dan facade tetap asumsi | Harus tetap dicatat walaupun tampilannya nanti lebih baik |
| Jalan masih seperti mainan? | Source junction/centerline tidak diubah; hanya material dihaluskan | Menunggu live close-up; tidak ada klaim photorealism |
| Lebih cocok untuk presentasi Gedangan? | Arah desain dan UI sudah disesuaikan | Menunggu video aktual dan review pengguna |

## Approximation yang tetap ada

- Semua {len(b)} building footprint, tinggi, posisi, jumlah, dan pemakaian plot; bukan inventaris aktual Gedangan.
- Modul ruko, shutter, kanopi, rumah, workshop, facade, warna, pagar, vegetasi, dan utilitas.
- Model stasiun 12×27 m dengan dinding 4.1 m dan atap 1.7 m. Penempatan render berjarak {offset:.2f} m dari node OSM untuk menjaga envelope road/rail; bukan hasil ukur gedung.
- Road paint, furniture, lane-width/control assumptions warisan dan render height offsets.
- Kamera dan peta kecil adalah alat presentasi; tidak memberi kalibrasi lapangan baru.

## Sumber dan kekosongan data

Foto Stasiun Gedangan 2020 benar-benar diperiksa untuk karakter bangunan rendah; tidak mengesahkan kondisi 2026. Teks kajian PTDI-STTD 2024 memberi konteks geografis. OSM dan peta publik retained memberi road/rail provenance. Download footprint baru timeout. Citra satelit dan street-view positional reconstruction tidak diperoleh. Tidak ada foto udara ditempel atau skybox metropolitan.

## Paket review

- `M15_6_1_GEDANGAN_ENVIRONMENT_REPORT.md`.
- `documentation/m1561/source-register.json` dan foto sumber beratribusi.
- `environment-assets.json`, `context-placement-audit.json`, `context-tests.txt`.
- `preservation-after.json`, `ancestor-preservation.json`, `visual-status.json`.
- Source/build/staging terpisah di port 5203.

Bukti screenshot/video M15.6 tidak dipromosikan menjadi hasil M15.6.1. Blender tidak digunakan; tidak dibuat laporan Blender seolah ada export. Daftar lima screenshot dan video yang belum dikerjakan tersedia pada `visual-status.json`.

## Batas acceptance

Preservasi jaringan dan pemeriksaan geometri statis lulus. TypeScript, build, dan sepuluh tes konteks lulus. **Visual/location acceptance belum lulus.** Jika setelah browser QA lingkungan masih metropolitan, terlalu generik, atau seperti mainan, status tetap PENDING/REQUIRES REWORK. Tidak ada release final atau pekerjaan milestone berikutnya yang dimulai.
'''
 (ROOT/'M15_6_1_GEDANGAN_ENVIRONMENT_REPORT.md').write_text(environment,encoding='utf-8');(ROOT/'M15_6_1_LOCATION_CONTEXT_REVIEW.md').write_text(review,encoding='utf-8');save(DOC/'build-verification.json',{'typescript':'PASS','vite':'PASS','js_bundle':'m1561-DqEr7EEI.js','js_kb':850.57,'warning':'Vitechunksize>500KB','context_tests':10,'context_tests_status':'PASS','actual_browser':'BLOCKED_BY_WORK_SETTINGS','actual_video':'NOT_CREATED','screenshots':'NOT_CREATED','blender_used':False});print(json.dumps({'reports':2,'preservation':p,'ancestor_files':len(ancestor),'visual':'PENDING_BROWSER_BLOCKED'},ensure_ascii=True),flush=True)
if __name__=='__main__':
 main()
 if (DOC/'evidence/actual-playback.webm').is_file():
  from .m1561_visual_review import main as review_actual
  review_actual()
