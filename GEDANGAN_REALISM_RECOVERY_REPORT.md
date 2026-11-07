# Gedangan — Functional Realism Recovery

Dibuat dari actual outputs, 1 November 2026. Status penelitian: **belum dikalibrasi terhadap observasi Gedangan 2026**.

## Keputusan penerimaan

**Core research engine implemented and exercised. H internal-browser functional smoke test PASS; user acceptance remains pending. Empirical traffic validity and engineering approval NOT established.** Ini research runner baru; EXE M12 lama tetap cached presentation viewer dan tidak diperbarui.

## Status A–H

| Tahap | Hasil | Batas |
| --- | --- | --- |
| A | Audit/overlay/connectivity tersedia | Sedati/Jenggolo dan akses persil perlu verifikasi |
| B | SQLite/schema/provenance/coverage tersedia | Target2026 MISSING |
| C | Date/WIB/class demand berjalan | Historical transfer; no all-day interpolation |
| D | 18 actual SUMO matrix +5 supplemental +API run | Not calibrated; source/controller assumptions |
| E | S00–04 actual changes | S05 BLOCKED second controller missing |
| F | A/B deck executable, construction executable | UNVERIFIED ENGINEERING CONCEPT |
| G | Per-edge/OD/class/reroute/spillback proxy exports | No field impact claim |
| H | Loopback API actual run/export PASS; controls implemented | Browser new SUMO run/playback/comparison PASS; user acceptance pending |

## Buka dan jalankan

Saat layanan aktif: [Research experiments](http://127.0.0.1:5196/). Untuk menjalankan kembali, double-click [START_GEDANGAN_RESEARCH.bat](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/START_GEDANGAN_RESEARCH.bat>). Memerlukan `.venv` proyek dan toolchain SUMO1.28.0 lokal. Belum paket portable baru; jangan memindahkan launcher sendirian.

Pilih tanggal/jam, sumber dan pengakuan asumsi, horizon/warm-up/kelas, intervensi, lalu **Periksa demand → Jalankan SUMO baru**. Hasil tersimpan dengan run ID; pilih actual result untuk trace, baseline setara untuk comparison, JSON/CSV untuk ekspor. Pilih reference07/12/17 atau synthetic eksplisit; jangan berharap exact2026 tersedia. Example missing5Mei16:00 ditolak.

## Perubahan source

Namespace `backend/gedangan/recovery_*.py`: checkpoint/audit, source-evidence database, observed lookup, demand, permissions/pathfinding, derivative NETCONVERT, actual SUMO run, comparison, analysis, loopback service, launcher, acceptance dan report generation. Frontend `frontend/realism_recovery/` adalah technical2D inspection, tanpa redesign3D. Tests di `tests/recovery/`. Sumber M01–M12 tidak diedit.

## Bukti uji

Main suite **PASS_WITH_DATA_AND_ENGINEERING_LIMITATIONS**, 18 runs, 72 checks;5supplemental multiclass/targeted reroute actual runs PASS; HTTP API creates real SUMO experiment and serves traces/exports. Source/data contracts test log: [contracts-tests.log](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/contracts-tests.log>). API integration PASS. Browser kemudian berhasil diakses: penolakan MISSING, playback WIB/elapsed, comparable flyover result dan new SUMO run264ede0fdfcecd93104bda52 diuji langsung. Screenshot browser-flyover-actual.png dan browser-new-experiment.png tersedia; browser-acceptance.json mencatat lingkup uji.18 data/source contracts PASS.

| Check | Status |
| --- | --- |
| Unsupported target time rejected | PASS |
| Unsupported target time rejected | PASS |
| No invented second corridor controller | PASS |
| 07 and17 use different input cohort and source counts | PASS |
| Source weekday/weekend changes real demand | PASS |
| morning_base mass balance | PASS |
| morning_base no illegal permissions or teleports | PASS |
| morning_base warmup vehicles loaded | PASS |
| evening_base mass balance | PASS |
| evening_base no illegal permissions or teleports | PASS |
| evening_base warmup vehicles loaded | PASS |
| midday_reference mass balance | PASS |
| midday_reference no illegal permissions or teleports | PASS |
| midday_reference warmup vehicles loaded | PASS |
| signal_adjustment mass balance | PASS |
| signal_adjustment no illegal permissions or teleports | PASS |
| signal_adjustment warmup vehicles loaded | PASS |
| turn_management mass balance | PASS |
| turn_management no illegal permissions or teleports | PASS |
| turn_management warmup vehicles loaded | PASS |
| frontage_coordination mass balance | PASS |
| frontage_coordination no illegal permissions or teleports | PASS |
| frontage_coordination warmup vehicles loaded | PASS |
| heavy_schedule mass balance | PASS |
| heavy_schedule no illegal permissions or teleports | PASS |
| heavy_schedule warmup vehicles loaded | PASS |
| flyover_A mass balance | PASS |
| flyover_A no illegal permissions or teleports | PASS |
| flyover_A warmup vehicles loaded | PASS |
| flyover_B mass balance | PASS |
| flyover_B no illegal permissions or teleports | PASS |
| flyover_B warmup vehicles loaded | PASS |
| construction_partial mass balance | PASS |
| construction_partial no illegal permissions or teleports | PASS |
| construction_partial warmup vehicles loaded | PASS |
| construction_full mass balance | PASS |
| construction_full no illegal permissions or teleports | PASS |
| construction_full warmup vehicles loaded | PASS |
| morning_without_trains mass balance | PASS |
| morning_without_trains no illegal permissions or teleports | PASS |
| morning_without_trains warmup vehicles loaded | PASS |
| morning_signal_off mass balance | PASS |
| morning_signal_off no illegal permissions or teleports | PASS |
| morning_signal_off warmup vehicles loaded | PASS |
| offpeak_explicit_synthetic mass balance | PASS |
| offpeak_explicit_synthetic no illegal permissions or teleports | PASS |
| offpeak_explicit_synthetic warmup vehicles loaded | PASS |
| direction_split_low mass balance | PASS |
| direction_split_low no illegal permissions or teleports | PASS |
| direction_split_low warmup vehicles loaded | PASS |
| direction_split_high mass balance | PASS |
| direction_split_high no illegal permissions or teleports | PASS |
| direction_split_high warmup vehicles loaded | PASS |
| volume_upper_sensitivity mass balance | PASS |
| volume_upper_sensitivity no illegal permissions or teleports | PASS |
| volume_upper_sensitivity warmup vehicles loaded | PASS |
| weekend_reference mass balance | PASS |
| weekend_reference no illegal permissions or teleports | PASS |
| weekend_reference warmup vehicles loaded | PASS |
| signal_adjustment equivalent cohort comparison | PASS |
| turn_management equivalent cohort comparison | PASS |
| frontage_coordination equivalent cohort comparison | PASS |
| heavy_schedule equivalent cohort comparison | PASS |
| flyover_A equivalent cohort comparison | PASS |
| flyover_B equivalent cohort comparison | PASS |
| construction_partial equivalent cohort comparison | PASS |
| construction_full equivalent cohort comparison | PASS |
| flyover_A actual vehicles traversed new network | PASS |
| flyover_B actual vehicles traversed new network | PASS |
| morning_without_trains physically changes results | PASS |
| morning_signal_off physically changes results | PASS |
| Full closure changes routes or exposes unaccommodated demand | PASS |


## Pemeriksaan integritas akhir

Final evidence verification: **PASS, 27 saved actual runs**. Seluruh output hashes, network hashes, sumber runner sesuai revision, cohort demand dan mass balance diperiksa. Bukti: documentation/realism_recovery/final-evidence-verification.json. Tidak mengklaim seluruh historical milestone regression tests dijalankan ulang; preexisting files diverifikasi SHA256.

## Preservasi dan reproducibility

13208 preexisting files SHA256 unchanged. Satu receipt checkpoint baru yang tertangkap kosong saat command mulai dikecualikan eksplisit; baseline hash tidak diedit. Old finalZIP SHA256 `5a0b36c4f8a20ec86a3bcb8d5b906ff0b3814cfa3465f376fc7df7cc8e76d520` tetap sama. Source checkpointZIP dan inventory: [checkpoint](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/checkpoint>); hasil [preservation-verification.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/preservation-verification.json>).

Setiap successful run menyimpan request, deterministic cohort, network manifest/hash, runner modules, registry dan binary hashes, commands, input/output manifests. Failed attempts dipertahankan dan tidak dihitung sebagai successful run. Run kembali lewat module/actual request menggunakan revision sumber yang dicatat; exact matching cache harus lolos output hashes. Main matrix dapat diulang `.venv/Scripts/python.exe -m backend.gedangan.recovery_acceptance`; analysis dan reports melalui module bernama sama. Tidak mengubah data lama atau upload GitHub.

## Blockers dan pekerjaan berikut yang belum diklaim selesai

1. Directional/class/turning/signal/rail/queue/travel-time survey target2026 belum ada. Perlu input sah dan review, lalu kalibrasi/validasi independen.
2. S05 membutuhkan representasi controller koridor kedua berbukti; bukan menambahkan lampu palsu.
3. Flyover membutuhkan approved DED/ROW/lahan/clearance/KAI/swept path/constructability dan staging akses yang benar. Konsep sekarang hanya sensitivitas traffic.
4. Hambatan Work settings teratasi pada pemeriksaan ulang. Browser smoke test dan screenshot tersedia; penerimaan pengguna, semua variasi kontrol serta ukuran layar lain belum diuji menyeluruh.
5. Baseline kontrol27phase individual dan boundary demand perlu kalibrasi. High queue dan banyak unfinished trips bukan bukti kemacetan nyata Gedangan.
6. Belum ada EXE research baru atau final3D redesign. Release lama tetap preserved. Tidak ada GitHub upload atau penghapusan research dataset.

Laporan rinci: [GEDANGAN_NETWORK_GROUND_TRUTH_AUDIT.md](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/GEDANGAN_NETWORK_GROUND_TRUTH_AUDIT.md>), [GEDANGAN_HISTORICAL_DATA_COVERAGE.md](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/GEDANGAN_HISTORICAL_DATA_COVERAGE.md>), [GEDANGAN_TIME_DEPENDENT_DEMAND.md](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/GEDANGAN_TIME_DEPENDENT_DEMAND.md>), [GEDANGAN_PEAK_HOUR_SUMO_TEST.md](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/GEDANGAN_PEAK_HOUR_SUMO_TEST.md>), [GEDANGAN_FLYOVER_ALTERNATIVES.md](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/GEDANGAN_FLYOVER_ALTERNATIVES.md>), [GEDANGAN_CONSTRUCTION_DIVERSION.md](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/GEDANGAN_CONSTRUCTION_DIVERSION.md>), [GEDANGAN_NETWORK_IMPACT_REPORT.md](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/GEDANGAN_NETWORK_IMPACT_REPORT.md>).


Bukti lengkap: [acceptance-results.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/acceptance-results.json>), [supplemental-acceptance.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/supplemental-acceptance.json>), [api-acceptance.json](<C:/Users/ROG ALLY/Documents/EXTREME STUDIOS/PROJECT/Simulasi Kemacetan Lalu Lintas/documentation/realism_recovery/api-acceptance.json>).
