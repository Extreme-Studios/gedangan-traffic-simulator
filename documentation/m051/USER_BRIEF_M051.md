# MILESTONE 05.1 — GEDANGAN TRAFFIC SIMULATOR
## Railway Geometry Remediation, Spillback Causality & Final Validation

MODEL: GPT-6.1 SOL MEDIUM

Lanjutkan proyek Gedangan Traffic Simulator dari M01 sampai M05.

Kerjakan MILESTONE 05.1 SAJA.

Tujuan utama adalah menyelesaikan dua temuan terbuka M05:
1. M05-GEO-01: Railway crossing geometry adaptation.
2. M05-SPILL-01: Gedangan spillback causality verification.

Jangan memulai M06.

---

# 1. PROJECT DIRECTORY

Gunakan folder:

`C:\Users\ROG ALLY\Documents\EXTREME STUDIOS\PROJECT\Simulasi Kemacetan Lalu Lintas`

Baca seluruh laporan dan implementasi terkait, terutama:

- MILESTONE_05_REPORT.md
- MILESTONE_04_5_REPORT.md
- MILESTONE_03_REPORT.md
- M05 initial regression logs.
- M05 network lineage.
- crossing-endpoint-adaptations.json.
- baseline-audit.json.
- safety-audits.json.
- queue-timeline.json.
- spillback candidate results.
- Railway source audit.
- SUMO 1.28.0 configuration.
- M05 experiment manifests.

Audit implementasi aktual, bukan hanya laporan.

Jangan menghapus, mengganti, atau menimpa pekerjaan sebelumnya.

Sebelum perubahan, simpan snapshot dan SHA256 manifest seluruh baseline.

# 2. STATUS WARISAN M05

M05 sudah berhasil membangun:

- Mixed traffic behavior.
- Traffic signal.
- Railway pilot pada jaringan Gedangan.
- Built-in SUMO rail crossing.
- Kereta bergerak pada railway network.
- Kendaraan berhenti saat crossing ditutup.
- Kendaraan kembali bergerak setelah crossing aman.
- Queue measurement.
- E2 detector.
- Positive-control spillback fixture.
- Internal browser playback.
- SUMO-GUI inspection.

M05 mempunyai 134 automated tests yang lulus.

Dua masalah belum terselesaikan:

A. NETCONVERT melakukan adaptasi lokal pada geometri crossing:
- 4 adjacent edge endpoints.
- 7 adjacent lane shapes.
- Internal connector dan junction envelope.

B. Kandidat spillback Gedangan belum mempunyai bukti kausal yang memadai.

Jangan mengulang implementasi fitur yang sudah berhasil.

# 3. M5.1-A — RAILWAY GEOMETRY AUDIT

## Tujuan

Memastikan geometri jalan, lajur, dan rel di sekitar perlintasan pilot Gedangan tidak mengalami distorsi yang membuat simulasi tidak representatif.

Sumber lokasi pilot:

- Railway ways 1330582009.
- Railway way 562358494.
- Railway way 1330582010.
- Crossing source node 859708050.
- Road source way 1240685448.
- Nearby siding 1268453702.

Gunakan data sumber M02 dan turunan M05.

## A. Geometric comparison

Buat pemeriksaan perbandingan:

1. Raw OSM geometry.
2. M04.5 original road geometry.
3. M05 converted road geometry.
4. M05 railway geometry.
5. M05 internal junction geometry.

Periksa:
- Source node coordinates.
- Edge endpoints.
- Lane shape endpoints.
- Rail centerline.
- Crossing angle.
- Crossing position.
- Stop-line position.
- Distance between rail and stop line.
- Road lane alignment.
- Internal connector geometry.
- Junction envelope.
- Adjacent edge continuity.
- Vehicle path through crossing.

Buat visual comparison yang dapat diperiksa melalui internal browser.

Gunakan overlay:
- Original geometry.
- M05 geometry.
- Difference vectors.
- Crossing center.
- Road lanes.
- Railway centerline.
- Stop lines.
- Vehicle conflict region.

Jangan hanya membandingkan jumlah node atau edge.

## B. Geometric error measurement

Hitung jika data memungkinkan:

- Endpoint displacement.
- Lane shape displacement.
- Crossing center offset.
- Rail-road intersection angle.
- Stop-line-to-crossing distance.
- Lane alignment error.
- Connector continuity error.

Gunakan satuan meter dan CRS yang benar.

Setiap hasil harus mencatat metode pengukuran dan sumber koordinat.

Jangan menetapkan toleransi arbitrer untuk menyatakan geometri aman.

Jika tidak ada toleransi resmi atau data survei, tampilkan hasil numeriknya dan beri status NEEDS FIELD VERIFICATION.

## C. Geometric remediation

Jika ditemukan kesalahan yang dapat diperbaiki dengan bukti geografis:

- Buat turunan jaringan M05.1.
- Pertahankan source OSM IDs.
- Pertahankan road access policy.
- Pertahankan oneway.
- Pertahankan frontage.
- Pertahankan railway source.
- Jangan menggeser koordinat source nodes tanpa bukti.
- Jangan menciptakan koneksi baru.
- Jangan memperbaiki geometri hanya agar SUMO-GUI terlihat rapi.

Jika NETCONVERT membutuhkan perubahan geometri lokal, dokumentasikan secara eksplisit.

Jika geometri asli belum cukup untuk menentukan posisi stop line atau bentuk crossing secara presisi, jangan mengarang hasil perbaikan.

Tandai sebagai NEEDS SURVEY.

## D. Physical geometry inspection

Periksa:
- Apakah kereta benar-benar melintas di lokasi crossing yang sesuai.
- Apakah road lane berhenti pada posisi yang masuk akal.
- Apakah vehicle path melewati crossing secara kontinu.
- Apakah internal connector tidak memotong jalur rel.
- Apakah kendaraan tidak menembus area crossing saat tertutup.
- Apakah kereta tidak bertabrakan dengan road network.
- Apakah lane direction tetap konsisten.

Perhatikan bahwa screenshot visual saja tidak membuktikan swept path atau clearance kendaraan.

Khusus trailer, bus, dan truk berat, jangan mengklaim legalitas atau clearance fisik sebelum data lapangan tersedia.

## E. Geometric acceptance

M5.1-A dapat FULL PASS hanya jika:

1. Seluruh adaptasi geometri terdokumentasi.
2. Perubahan edge dan lane shape dapat dijelaskan.
3. Perlintasan mempunyai koneksi topologis yang valid.
4. Road dan railway path tidak saling bertabrakan secara tidak sah.
5. Posisi stop line dan crossing mempunyai dasar geometris yang dapat dipertanggungjawabkan.
6. Tidak ada distorsi atau pergeseran yang tidak terjelaskan.
7. Rebuild dapat direproduksi.

Jika membutuhkan survei lapangan untuk membuktikan posisi atau clearance, status harus PARTIAL — NEEDS FIELD SURVEY.

Jangan menyatakan FULL PASS hanya karena SUMO berhasil menjalankan kereta.

# 4. M5.1-B — SPILLBACK CAUSALITY VERIFICATION

## Tujuan

Membuktikan apakah antrean yang terdeteksi di jaringan Gedangan benar-benar menyebabkan pergerakan dari ruas hulu terhambat akibat ruang downstream tidak tersedia.

Jangan menyamakan:
- Long queue.
- Signal-induced queue.
- Railway-induced queue.
- Downstream congestion.
- Actual spillback.

Spillback harus mempunyai bukti kausal.

## A. Audit detector yang sudah ada

Periksa:
- Queue tail position.
- Queue head position.
- Downstream lane occupancy.
- Downstream storage.
- Upstream planned next edge.
- Upstream vehicle movement.
- Available signal movement.
- Junction priority.
- Foe relationships.
- Lane permissions.
- Vehicle routes.
- Queue duration.
- Discharge opportunity.

Periksa apakah kandidat spillback sebelumnya sebenarnya dipengaruhi oleh:
- Red signal.
- Conflicting traffic movement.
- SUMO right-of-way.
- Unavailable downstream lane.
- Blocked connector.
- Railway crossing closure.
- Route restriction.
- Network boundary.

Jangan menyimpulkan penyebab hanya dari kendaraan yang berhenti.

## B. Causal spillback definition

Suatu peristiwa hanya boleh disebut VERIFIED SPILLBACK apabila:

1. Downstream storage benar-benar terisi oleh antrean.
2. Queue tail mencapai area yang mengganggu akses dari ruas hulu.
3. Kendaraan upstream memiliki rute valid.
4. Kendaraan upstream memiliki kesempatan legal untuk bergerak.
5. Pergerakannya tertahan karena downstream tidak menyediakan ruang.
6. Kondisi berlangsung secara kontinu sesuai threshold yang didefinisikan.
7. Bukti temporal dan spasial tersedia.
8. Gangguan upstream berkurang setelah downstream storage tersedia kembali.

Jika salah satu syarat kausal tidak dapat dibuktikan, klasifikasikan sebagai CANDIDATE atau UNRESOLVED.

Jangan mengklaim spillback hanya berdasarkan occupancy tinggi.

## C. Periksa signal dan priority confounding

Ini sangat penting.

Ketika kendaraan upstream berhenti, periksa apakah:
- Lampu sedang merah.
- Fase hijau belum tersedia.
- Gerakan kendaraan tertahan oleh konflik prioritas.
- Koneksi belok tidak tersedia.
- Downstream lane benar-benar penuh.

Jika lampu merah menjadi penyebab utama, kategorikan sebagai SIGNAL_QUEUE.

Jika perlintasan kereta menjadi penyebab utama, kategorikan sebagai RAILWAY_QUEUE.

Jika ruang downstream penuh dan menghalangi kendaraan yang seharusnya dapat bergerak, evaluasi sebagai SPILLBACK.

Jika terdapat beberapa penyebab, gunakan MULTI_CAUSAL_EVENT dan jelaskan kontribusinya.

Jangan memaksakan satu penyebab tunggal jika bukti menunjukkan beberapa faktor.

## D. Controlled experiments

Gunakan eksperimen SUMO terkontrol.

Lakukan perbandingan:

A. Baseline free-flow.

B. Traffic signal tanpa downstream blockage.

C. Downstream queue dengan upstream green dan legal movement available.

D. Railway closure tanpa downstream queue.

E. Combined signal dan downstream blockage.

F. High demand dengan downstream storage terbatas.

G. Recovery setelah downstream queue terurai.

Gunakan demand, vehicle composition, network, seed, dan observation horizon yang sama ketika mengisolasi satu variabel.

Gunakan beberapa seed jika waktu memungkinkan.

Jangan mengubah posisi kendaraan secara manual.

Jangan memaksa hasil spillback menggunakan TraCI speed atau position override.

## E. Gedangan network investigation

Prioritaskan area:

- Perempatan Gedangan.
- Koridor utama Sidoarjo–Surabaya.
- Pendekat frontage.
- Akses feeder yang terhubung.
- Area crossing Ketajen/Stasiun Gedangan.
- Junction yang mempunyai downstream storage terbatas.

Gunakan data M05 dan hasil SUMO yang benar-benar dihasilkan.

Identifikasi edge mana yang:
- Menjadi lokasi antrean.
- Menjadi lokasi queue tail.
- Menghambat pergerakan hulu.
- Mempunyai downstream storage terbatas.
- Terpengaruh sinyal.
- Terpengaruh kereta.

Jika tidak ada bukti spillback pada jaringan saat ini, laporkan hasil negatif secara jujur.

Jangan membuat geometri atau koneksi buatan untuk memaksa spillback Gedangan.

Positive-control isolated fixture tetap boleh dipakai untuk menguji detector, tetapi jangan menganggapnya sebagai bukti kondisi Gedangan.

## F. Spillback metrics

Sediakan:
- Queue count.
- Queue extent.
- Queue duration.
- Downstream occupancy.
- Downstream storage.
- Upstream blocked vehicle count.
- Upstream blocked duration.
- Blocked movement.
- Cause classification.
- Event start/end.
- Recovery duration.
- Affected edge IDs.
- Confidence/evidence level.

Pastikan definisi setiap metrik terdokumentasi.

Bedakan SUMO output aktual dari derived metrics.

## G. Spillback acceptance

M5.1-B dapat FULL PASS jika:

1. Positive-control fixture tetap berhasil.
2. Negative-control fixture menolak false positives.
3. Traffic signal queue dapat dibedakan.
4. Railway queue dapat dibedakan.
5. Candidate spillback Gedangan dianalisis dengan trace prioritas.
6. Event classification dapat direproduksi.
7. Jika spillback Gedangan terjadi, terdapat bukti downstream blockage yang menghambat legal upstream movement.
8. Jika spillback tidak terjadi, hasil negatif tetap diterima dan tidak dipaksakan.

Catatan: keberhasilan algoritma deteksi tidak sama dengan bukti bahwa spillback benar-benar terjadi di Gedangan.

# 5. M5.1-C — INTERNAL BROWSER AUDIT

Gunakan internal browser Codex sebagai tempat pemeriksaan utama.

Buat halaman M05.1 validation view.

Tampilkan:

A. Railway geometry:
- Original road.
- Adjusted road.
- Railway centerline.
- Crossing node.
- Stop lines.
- Geometry differences.
- Distance measurement.
- Validation status.

B. Spillback:
- Queue timeline.
- Queue tail.
- Downstream occupancy.
- Upstream blocked movements.
- Signal state.
- Railway state.
- Causal classification.

C. Event inspection:
- Event ID.
- Start/end time.
- Affected edges.
- Cause.
- Supporting evidence.
- Confidence status.

Semua data harus berasal dari output aktual dan hasil analisis yang tersimpan.

Jangan menggambar event palsu.

Pertahankan viewer M05.

Lakukan browser QA desktop 1920×1080 dan mobile 390×844.

# 6. M5.1-D — SAFETY & REGRESSION

Pastikan:

- M03 network immutable.
- M04.5 corrected network immutable.
- M05 source outputs tetap tersedia.
- Vehicle access policy tidak berubah tanpa alasan.
- Oversize tetap diblokir.
- Frontage tetap terpisah.
- Railway crossing safety tetap bekerja.
- Tidak ada illegal lane access.
- Tidak ada unexplained teleport.
- Tidak ada collision.
- Tidak ada data sintetis yang masuk observed_data.

Jalankan seluruh 134 regression tests dari M05.

Tambahkan tests untuk:
- Geometry differences.
- Crossing topology.
- Lane continuity.
- Stop-line positioning.
- Signal queue classification.
- Railway queue classification.
- Downstream blockage.
- Upstream movement availability.
- Causal spillback.
- False-positive rejection.
- Event reproducibility.
- Source immutability.

Jangan menghapus test yang gagal untuk memperoleh status PASS.

# 7. REPRODUCIBILITY

Buat:
- SHA256 manifests.
- Network comparison manifests.
- Experiment configs.
- Demand hashes.
- Run manifests.
- Event evidence.
- Geometry comparison outputs.
- Regression logs.

Rebuild M05.1 harus menghasilkan data yang konsisten dengan input yang sama.

Pertahankan seed dan SUMO version 1.28.0.

# 8. BATASAN

Jangan:
- Memulai M06.
- Memasukkan volume lalu lintas aktual tanpa data.
- Mengkalibrasi demand.
- Mengubah jadwal kereta menjadi jadwal aktual.
- Mengklaim clearance fisik terverifikasi.
- Mengubah geometri asli tanpa sumber.
- Memaksakan spillback.
- Mengubah posisi kendaraan secara manual.
- Mengubah source network M03 atau M04.5.
- Membangun ulang seluruh frontend.
- Mengembangkan fitur visual baru yang tidak diperlukan.

Fokus pada dua temuan M05 yang belum selesai.

# 9. ACCEPTANCE CRITERIA

M5.1 dinyatakan FULL PASS apabila:

1. Railway geometry audit selesai.
2. Seluruh perubahan geometri dapat dijelaskan.
3. Crossing topology valid.
4. Stop line dan lane continuity diperiksa.
5. Spillback causal detector lolos positive control.
6. Negative control tidak menghasilkan false positives.
7. Signal queue dan railway queue dapat dibedakan.
8. Gedangan candidate events dianalisis.
9. Status spillback Gedangan ditetapkan berdasarkan bukti.
10. Tidak ada klaim fisik yang tidak terverifikasi.
11. Internal browser menampilkan audit.
12. SUMO-GUI tetap berfungsi.
13. Seluruh regression tests lulus.
14. Source M03–M05 tidak rusak.
15. Seluruh hasil dapat direproduksi.

Jika geometri membutuhkan survei lapangan, atau kausalitas Gedangan belum dapat dibuktikan karena data tidak cukup, jangan memaksakan FULL PASS.

Gunakan status PARTIAL — NEEDS FIELD DATA jika memang demikian.

# 10. FINAL REPORT

Buat:

`MILESTONE_05_1_REPORT.md`

Dan:

`MILESTONE_05_1_README.md`

Laporan harus memuat:

1. Executive summary.
2. Status M5.1.
3. Railway geometry before/after.
4. Edge endpoint comparison.
5. Lane shape comparison.
6. Stop-line and crossing measurements.
7. Railway topology validation.
8. SUMO crossing tests.
9. Spillback causal model.
10. Positive-control results.
11. Negative-control results.
12. Gedangan candidate event analysis.
13. Signal and railway confounding analysis.
14. Verified events atau unresolved events.
15. Internal browser screenshots.
16. SUMO-GUI evidence.
17. Regression tests.
18. Reproducibility.
19. Missing field data.
20. Acceptance criteria satu per satu.
21. Rekomendasi M06.

Jangan memulai M06 sebelum pengguna menyetujui hasil M5.1.

**MULAI MILESTONE 05.1 SEKARANG.**

Prioritaskan pembuktian geometri dan kausalitas dibandingkan sekadar membuat seluruh acceptance criteria terlihat hijau.