"""Reproducible reports from preserved sources and measured browser evidence."""
from .m1562_common import *
import subprocess

def main():
 protect();audit=load(DOC/'footprint-audit.json');bench=load(DOC/'benchmark-summary.json')
 baseline=load(DOC/'preservation-before.json');changed=[p for p,h in baseline.items()if not(ROOT/p).is_file()or sha(ROOT/p)!=h]
 ancestor=load(ROOT/'documentation/m155/preservation-before.json')['files'];ancestor_changed=[p for p,h in ancestor.items()if not(ROOT/p).is_file()or sha(ROOT/p)!=h]
 preservation={'checked':len(baseline),'changed':changed,'ancestor_checked':len(ancestor),'ancestor_changed':ancestor_changed,'network_sha256':sha(NETWORK)};assert not changed and not ancestor_changed,preservation;save(DOC/'preservation-after.json',preservation)
 header='2 November 2026, WIB. Staging terpisah: http://127.0.0.1:5204/.\n\n**REVIEW REQUIRED — menunggu pengguna memeriksa video aktual.**\n\nMANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION. PROVISIONAL NETWORK — NOT FIELD CALIBRATED.\n\n'
 source=f'''# M15.6.2 — Location Source Report

{header}## Sumber yang benar-benar diperoleh

[OSM API v0.6](https://wiki.openstreetmap.org/wiki/API_v0.6) berhasil mengembalikan map terbatas bbox 112.718,-7.402,112.736,-7.374. Raw XML 14,346,506 byte berada di `documentation/m1562/sources/gedangan.osm`, SHA256 `{audit['source_sha256']}`. Ditemukan {audit['source_total_building_ways']} building ways, termasuk Stasiun Gedangan way 472866576. OSM adalah sumber pemetaan publik, bukan survei independen kondisi bangunan 2026. Atribusi [OpenStreetMap contributors / ODbL 1.0](https://www.openstreetmap.org/copyright) ditampilkan pada peta sumber aplikasi.

Dataset lokal lama `geodata/raw/gedangan-network.json` berisi 52.013 elemen namun nol tag building. Ini menjelaskan mengapa ekstraksi jaringan lama tidak bisa menjadi inventaris bangunan. Tidak mengubah dataset lama atau mengartikan nol building sebagai tidak ada bangunan.

Karakter stasiun mengacu pada [foto Stasiun Gedangan 2020](https://commons.wikimedia.org/wiki/File:Stasiun_Gedangan_2020.jpg), Rizal Febri Ardiansyah, 12 September 2020, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Foto asli retained benar-benar diperiksa: dinding cream, band abu, shutter, teritis/bracket dan atap genteng rendah. Tidak ditempel menjadi aerial background. Bentuk detail model merupakan interpretasi, bukan hasil fotogrametri. Metadata foto Wikimedia 2022 diperoleh, tetapi download original mengembalikan HTTP403; tidak diterobos dan tidak mengklaim foto 2022 sudah dilihat.

## Alternatif yang diperiksa

[Geofabrik Java PBF](https://download.geofabrik.de/asia/indonesia/java.html) tersedia sekitar 857 MB; tidak diunduh karena source OSM bounded 14 MB sudah memenuhi kebutuhan footprint. [Overture](https://docs.overturemaps.org/getting-data/) mendukung ekstrak bbox; client resmi dipasang dan CLI diperiksa, tetapi data Overture tidak diekstrak atau dicampur seolah sudah diperiksa. [Informasi pemetaan Kecamatan Gedangan](https://gedangan.sidoarjokab.go.id/001/1784184566) ditemukan, tetapi berita workshop bukan dataset koordinat footprint yang bisa digunakan. Dataset bangunan pemerintah yang dapat dipakai pada pekerjaan ini tetap UNAVAILABLE. Tidak memakai citra satelit/street-view terlindungi atau bypass akses.

## Keyakinan dan tiga area prioritas

| Area | Anchor/sumber | Keyakinan posisi | Penampilan |
| --- | --- | --- | --- |
| Simpang utama | Frozen SUMO road/signal + footprint OSM sekitarnya | Source-mapped; registrasi UTM deterministik | Tinggi/fasad/atap/material asumsi |
| Stasiun/perlintasan | Way 472866576 + frozen rail/crossing + foto 2020 | Footprint sumber, tanpa pergeseran | PHOTO-REFERENCED APPEARANCE hanya karakter stasiun; ukuran detail asumsi |
| Koridor/frontage | Preset/lanes frozen + footprint OSM di area prioritas | Frontage tetap di koordinat asli | Tinggi/fasad dan material asumsi; close-up terpisah |

Source-confidence map menampilkan footprint sumber hijau, stasiun dengan referensi karakter foto emas, serta seluruh tinggi/fasad berlabel asumsi. Area di luar cakupan render tidak diisi bangunan rekaan. Semua URL, hash, kegagalan dan alasan alternatif ada di `source-attempts.json`.
'''
 footprints=f'''# M15.6.2 — Building Footprint Report

{header}## Hasil

{audit['source_total_building_ways']} closed building ways ditemukan dalam source map. Seleksi area simpang, stasiun, frontage dan strip koridor menghasilkan **{audit['selected_rendered']} footprint sumber yang dirender**, {audit['detailed']} dengan detail fasad. Ini penggantian 550 footprint rekaan, bukan penambahan ratusan bangunan fiksi. Sepuluh polygon landuse sumber memberi konteks permukaan; warna/materialnya tetap asumsi.

{len(audit['withheld_network_conflicts'])} footprint ditahan karena overlap envelope jaringan model. Daftarnya tersimpan lengkap dalam `footprint-audit.json`; polygon sumber tetap di raw XML. Bangunan tidak dipindah, diperkecil atau diputar agar lolos. Tidak memperbaiki jalan dengan menggeser sumber. Tidak ada guessed infill. Relation/multipolygon kompleks tidak dirakit menjadi klaim bangunan lengkap; ruang lingkup ini closed ways dengan node lengkap dan polygon valid.

## Koordinat dan tinggi

WGS84 diproyeksikan ke EPSG:32749 (UTM49S), kemudian memakai netOffset frozen (-690790.39,-9182879.52). Konversi SUMO XY ke Three.js X/-Z tidak mengubah graph. `footprints-wgs84.geojson` memakai lon/lat; `footprints-local.geojson` adalah ekspor koordinat lokal untuk audit dan diberi label sistem koordinat lokal. Scene menyimpan setiap vertex sumber, version, timestamp, tag, dan OSM ID.

Tidak ditemukan height/building:levels pada building ways yang diperiksa. Semua tinggi adalah **ASSUMED 3D HEIGHT**: station 4m wall, bangunan kecil 3.4m, menengah 5.8m dan besar 7.2m, ditambah atap asumsi. Angka tersebut bukan konversi tag lantai atau pengukuran. Orientasi berasal dari oriented rectangle footprint, sedangkan body tetap memakai polygon penuh. Atap/fasad adalah interpretasi visual; atap persegi panjang dipakai hanya bila polygon mengisi >94% oriented rectangle, lainnya memakai roof polygon datar. Ini tidak memvalidasi bentuk atap aktual.

Stasiun source way 472866576 berluas sekitar **392.63 m²**. Body memakai footprint itu persis, tanpa offset buatan M15.6.1. Referensi foto tidak menyediakan height survey atau seluruh elevasi; fasad dan kedalaman teritis tetap approximation.

## Label wajib

- SOURCE-MAPPED FOOTPRINT: vertex OSM yang berhasil diperoleh dan diproyeksikan.
- PHOTO-REFERENCED APPEARANCE: karakter stasiun berdasarkan foto 2020; bukan seluruh gedung rekonstruksi presisi.
- ASSUMED 3D HEIGHT: seluruh tinggi bangunan.
- ASSUMED VISUAL CONTEXT: fasad selain karakter stasiun, roof form, warna, material, awning dan trim.
- UNAVAILABLE: height survey, facade inventory koridor, georeferenced imagery terbaru dan footprint pemerintah yang dapat dipakai.

Delapan tes integritas lulus, termasuk pemeriksaan setiap vertex render terhadap node OSM sumber. Network SHA256 tetap `{EXPECTED}`.
'''
 rows='\n'.join(f"| {r['label']} | {r['samples']} | {r['median_window_fps']:.1f} | {r['worst_window_p5_fps']:.1f} | {r['heap_max_mib']:.1f} | {r['typed_buffers_mib']:.1f} | {r['conservative_heap_plus_typed_mib']:.1f} |"for r in bench['measurements']if r['status']=='MEASURED')
 memory=f'''# M15.6.2 — Memory Optimization Report

{header}## Akar beban dan perubahan

Decoder lama menahan seluruh posisi sebagai array JavaScript bersarang: 3,441,615 posisi pada demand3000 dan 4,550,529 pada demand5000. Loading empat chunk JSON sekaligus juga membuat object graph sementara. Renderer lama memindai semua frame untuk capacity kendaraan. Ini menjelaskan overhead yang ditargetkan; bukan klaim heap profiler membuktikan setiap byte atau leak tertentu.

Transport baru mengemas enam field asli dalam Float64 little-endian. Tidak menggunakan Float32/quantization, tidak memotong frame, posisi, vehicle totals atau SUMO output. Worker mengambil chunk berurutan lalu mentransfer ArrayBuffer; main thread menyimpan buffer dan descriptor frame. Maksimum tiga frame yang dimaterialisasi menjadi tuple disimpan dalam cache. Capacity maksimum dihitung dari seluruh rekaman di preprocessing. Switch membatalkan worker sebelumnya, dan unmount membatalkan loading. Peta sumber diperbarui satu kali/detik; frame traffic tetap mengikuti timestamp asli dan interpolasi warisan.

Verifikasi penuh membandingkan **semua enam field di semua 7,992,144 posisi** kedua run, termasuk times/frame descriptors, vehicle registry, events dan metrics. Dua run masing-masing tetap 7200 frame. Hasil EXACT_FLOAT64_EQUAL ada di `lossless-verification.json`. Buffer source3000 157.54 MiB; source5000 208.31 MiB. File SUMO/JSON/gzip asli hanya dibaca.

## Before/after aktual

| Kasus | Sampel | Median window FPS | Worst window p5 FPS | Max browser heap MiB | Typed MiB | Heap + typed konservatif MiB |
| --- | --- | --- | --- | --- | --- | --- |
{rows}

Satu interval45s per kasus, analisis detik5–45, perangkat sama, viewport1920×1080/DPR1, kamera junction, context on, speed1x, overlay none, mulai t1800. Baseline memakai source/build M15.6.1 melalui server5205 dengan telemetry diarahkan ke folder M15.6.2; corrected5204 memakai build `{bench['protocol'].get('final_build')}`. Raw exploratory windows, transisi dan pengamatan yang lebih lama tetap disimpan; tidak dicampur untuk mempercantik interval final. Semua raw filename/UTC dan resource GPU ada di `benchmark-summary.json`.

`performance.memory` adalah metrik browser, bukan total process RAM/VRAM. Typed bytes disajikan terpisah; penjumlahan konservatif bisa menghitung sebagian byte dua kali karena accounting browser. Target lama3000≤800MiB terpenuhi pada interval ini, termasuk penjumlahan konservatif. Pada5000, penjumlahan konservatif masih melebihi800MiB; jangan klaim semua demand memenuhi batas tersebut. Garbage collection saat switch tidak dipaksa. Penurunan heap bukan sertifikat bebas leak atau kapasitas VRAM.

Aset lingkungan dibatch per material; kendaraan tetap instanced. Cleanup renderer lama dipertahankan untuk controls, RAF, resize observer, listeners, geometry, materials, textures dan renderer. Tidak ada salinan texture per bangunan; hanya tekstur grain bersama dan sign stasiun. Peta SVG dimemoisasi. Capture memakai stream layar aktual, potongan data video sementara, timer tour dihentikan pada stop dan semua media tracks dihentikan. Rekaman video dapat menambah RAM sementara; bukan bagian interval benchmark.

Tidak dilakukan soak multi-jam atau GPU memory profiler. Device/power/thermal/background activity tidak dikendalikan sebagai eksperimen laboratorium; perubahan FPS tidak boleh dipresentasikan sebagai hasil penelitian lalu lintas Gedangan. M15.6 historis pernah mencapai>1.5GiB; tabel ini adalah pengukuran baru dengan protokol tercatat, bukan menulis ulang laporan lama.
'''
 visual=f'''# M15.6.2 — Visual Improvement Report

{header}## Defect register sebelum implementasi

Delapan cacat berperingkat ditulis sebelum implementasi dalam `documentation/m1562/DEFECT_REGISTER.md` dan JSON terkait. Screenshot overview/rail M15.6.1, video aktual dan laporan M15.6/performance diperiksa. Prioritas: sumber footprint, nested playback memory, stasiun generik, terrain kosong, kamera frontage terlalu jauh, aset berulang, video canvas-only dan lifecycle switching.

## Perubahan yang terlihat

Footprint rekaan dihapus dari scene turunan dan diganti polygon OSM sumber di tiga area prioritas. Kontinuitas permukiman mengikuti lokasi polygon, bukan generator populasi acak. Tinggi, orientasi detail dan material tetap berlabel asumsi. Stasiun memakai footprint sumber dan karakter cream/grey, shutter, band, teritis/bracket, plinth dan sign GEDANGAN berdasarkan foto2020; belum merupakan rekonstruksi terukur.

Ground beige seragam diganti tone terrain lebih tenang, micrograin bersama dan10 polygon landuse sumber. Road-edge material transition selebar0.6m total di bawah permukaan asphalt adalah asumsi render saja, bukan sidewalk, drainase, shoulder legal atau road geometry tambahan. Roof/material dan trim dibatch; tidak menambah pohon dekoratif berlebihan, tiang/utilitas rekaan, nama usaha, stasiun gate atau infrastruktur rel baru. Existing crossing furniture, rail alignment dan recorded controller events dipertahankan.

Kamera station, junction close-up dan frontage close-up baru melengkapi preset lama. Frontage relationship tetap overview geografis berjarak; detail memakai kamera terpisah. Tidak memindahkan frontage atau memampatkan jarak. Matched before/after memakai kamera warisan junction/rail dan timestamp1796 pada baseline3000 yang sama. Peta keyakinan sumber interaktif menandai provenance footprint dan approximation.

Blender **tidak digunakan**. Geometri ini berupa polygon map, detail sederhana dan material berulang; batching procedural Three.js dipakai agar sumber/transform bisa diaudit. Tidak ada GLB/BLEND atau klaim pipeline Blender. Laporan Blender opsional tidak dibuat. Aset kendaraan warisan tetap mengikuti actual SUMO recording. Tidak ada flyover, fictional sensors atau V2I live claim.

## Batas visual

Geografi bangunan lebih berdasar dibanding M15.6.1, tetapi facade/roof dan material masih sederhana, belum photorealistic atau as-built. Tidak ada data street-level koridor terbaru yang terverifikasi. Ground dan station furnishing belum diverifikasi kondisi2026. Peta OSM bisa tidak lengkap/bergeser relatif jaringan model. Konflik render ditahan dan dicatat, bukan ditutup dengan bangunan fiksi. Status tetap REVIEW REQUIRED sampai pengguna menilai video.

Screenshot dan video aktual, beserta hash/metadata, tercantum dalam `review-package.json`. Video delivery memang merekam UI lengkap dan tur lima kamera secara aktual. Raw berdurasi49.933s memiliki pergantian ukuran awal; output mempertahankan seluruh rekaman lalu scale ke ukuran delivery1920×1080, sehingga5.685s awal masih berisi perubahan viewport dan bukan source native1920. Sesudah itu source native1920×1080. Tidak menambah still frame atau mensintesis gerakan. Ketajaman teks screen-capture lebih rendah daripada screenshot langsung; kualitas capture tetap perlu review. Video awal retained `first-screen-review.webm` memiliki framing stasiun terhalang; percobaan324×546 retained `failed-small-viewport-tour.webm`. Keduanya tidak dihapus atau dipromosikan menjadi proof final tour.
'''
 review_path=DOC/'review-package.json';package=load(review_path)if review_path.exists()else{'status':'EVIDENCE_IN_PROGRESS'}
 acceptance=f'''# M15.6.2 — Acceptance Report

{header}## Keputusan

**Teknis/source: pemeriksaan yang dijalankan lulus. Visual: REVIEW REQUIRED.** Pengguna harus memeriksa actual video sebelum visual acceptance dapat berubah. Tidak membuat final EXE atau memulai milestone lanjutan.

| Pemeriksaan | Hasil |
| --- | --- |
| Footprint sumber | {audit['selected_rendered']} source-mapped, nol footprint rekaan; {len(audit['withheld_network_conflicts'])} konflik ditahan |
| Tinggi/fasad | Seluruh tinggi asumsi; karakter stasiun photo-referenced; tidak ada klaim surveyed |
| Network | SHA256 `{EXPECTED}` sama; alignment/signals/rail/turn/routes/counts/physics tidak diubah |
| Rekaman traffic | 7200 frame tiap run; 7,992,144 posisi kedua run diperiksa exact Float64 |
| Tes baru | 8 unittest integritas lulus; TypeScript dan isolated Vite build lulus; chunk warning>500KB masih ada |
| Preservasi | {len(baseline)} file checkpoint M15.6/M15.6.1 dan {len(ancestor)} file ancestor hash-equal; laporan lama tidak ditulis ulang |
| Memori/FPS | Before/after aktual pada dua demand; batas dan accounting ada pada laporan memori |
| Paket screenshot/video | {package['status']} — lihat review-package.json untuk berkas dan metadata aktual |
| Aksi dibatasi | Tidak menghapus file, upload GitHub, membuat EXE final, flyover, atau demand/route baru |

Regression scope: tes kontrak geometri/registry/recording/preservasi untuk perubahan renderer ini, bukan klaim menjalankan ulang seluruh suite M01–M15.6.1 atau SUMO eksperimen baru. Hasil actual SUMO lama dibaca sebagai playback; scenario random tidak diubah menjadi pengukuran historis Gedangan. Risiko tersisa: ketidakpastian source map, tinggi/fasad/roof asumsi, kualitas presentasi perlu penilaian manusia, GC/long-term memory belum tersertifikasi dan video screen-capture bisa lebih lunak daripada screenshot langsung.

## Reproduksi dari source yang diserahkan

Gunakan `.venv/Scripts/python.exe -m backend.gedangan.m1562_context` untuk scene dari XML cached; `-m backend.gedangan.m1562_recording` untuk dua buffer dari source asli. Source retrieval optional tersedia pada `m1562_sources.py` dan memakai cache. Build frontend dengan `tsc -p frontend/tsconfig.m1562.json`, lalu Vite memakai `vite.m1562.config.ts` dari folder frontend. Jalankan `staging/m1562/START_M1562.ps1`. Loader preprocessing membuat packed recording baru di namespace sendiri bila pengguna membuka run lain. Jangan menjalankan bootstrap/wire migrasi ulang pada source final; source final sudah memuat hasil migrasi. Source/build turunan terpisah; M12–M15.6.1 tidak ditimpa.
'''
 for suffix,text in [('LOCATION_SOURCE_REPORT',source),('BUILDING_FOOTPRINT_REPORT',footprints),('VISUAL_IMPROVEMENT_REPORT',visual),('MEMORY_OPTIMIZATION_REPORT',memory),('ACCEPTANCE_REPORT',acceptance)]:
  (ROOT/f'M15_6_2_{suffix}.md').write_text(text,encoding='utf-8')
 print({'reports':5,'preservation':preservation,'visual':'REVIEW REQUIRED'})
if __name__=='__main__':main()
