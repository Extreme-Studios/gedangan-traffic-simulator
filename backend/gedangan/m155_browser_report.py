"""Replace previous browser blocker with measured, bounded-session evidence."""
from .m155_common import *
import statistics,subprocess
from collections import defaultdict
def main():
 raw=[dict(file=p.relative_to(ROOT).as_posix(),**load(p))for p in (DOC/'browser-performance').glob('*.json')];loads=[r for r in raw if r['kind']=='playback_load'];samples=[r for r in raw if r['kind']=='render_sample'];measured=[r for r in samples if 'fps_median'in r];groups=defaultdict(list)
 for r in measured:groups[(r['recording'],r['camera'])].append(r)
 summary=[]
 for (run,cam),rs in sorted(groups.items()):
  heaps=[r['js_heap']['used']/1048576 for r in rs if r.get('js_heap')];summary.append({'run_id':run,'camera':cam,'samples':len(rs),'median_of_window_fps_medians':statistics.median(r['fps_median']for r in rs),'minimum_window_p5_fps':min(r['fps_p5']for r in rs),'minimum_window_mean_fps':min(r['fps_mean']for r in rs),'maximum_rolling120_frame_stalls_over50ms':max(r['stalls_over_50ms']for r in rs),'active_range':[min(r['visible_vehicles']for r in rs),max(r['visible_vehicles']for r in rs)],'heap_mib_range':[min(heaps),max(heaps)]if heaps else None,'sample_elapsed_range_s':[min(r['session_elapsed_s']for r in rs),max(r['session_elapsed_s']for r in rs)],'playback_timestamp_range_s':[min(r['playback_time_s']for r in rs),max(r['playback_time_s']for r in rs)]})
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_entries','format=duration:stream=width,height,nb_read_frames','-of','json',str(DOC/'evidence/actual-playback.webm')],text=True));video={'file':'documentation/m155/evidence/actual-playback.webm','sha256':sha(DOC/'evidence/actual-playback.webm'),'probe':probe,'actual_run_id':'cc419452a995456df324fd05','mp4_file':'documentation/m155/evidence/actual-playback.mp4','mp4_sha256':sha(DOC/'evidence/actual-playback.mp4'),'playback_speed':1,'timestamp_start_s':3240,'export_note':'Live canvas resampled into1280x800 with timestamp and end metrics watermark. Actual sample movement; no synthetic positions. 12s recorder interval, encoded duration from probe.'}
 value={'status':'CONDITIONAL_PERFORMANCE_NOT_UNIVERSAL_SMOOTHNESS','created_utc':now(),'raw_files':len(raw),'raw_render_samples':len(samples),'samples_with_frame_median':len(measured),'groups':summary,'loads':[{'run_id':r['run_id'],'wall_ms':r['wall_ms'],'frames':r['frames'],'positions':r['positions'],'window':r['window']}for r in loads],'minimum_p5_all_retained_samples':min(r['fps_p5']for r in samples),'maximum_heap_mib_all_retained_samples':max(r['js_heap']['used']/1048576 for r in samples if r.get('js_heap')),'session_elapsed_max_s':max(r['session_elapsed_s']for r in raw),'video':video,'limitations':['Rolling120-frame windows, saved about every10s; not a lossless all-frame trace','Median of window medians is not global frame-weighted median','Minimum window p5 is reported; low samples retained, no cherry-picking','Stall count is a rolling window maximum, not sum of independent events','Heap is JS heap, not VRAM/system memory or proof of absence of leaks','Viewport1920x1080; embedded and expanded canvas differ','Browser page session duration is bounded, not a multi-hour soak test','Screenshot text soft at captured browser quality; readable DOM and exported video inspected separately']};save(DOC/'browser-performance-summary.json',value)
 visual={'status':'BROWSER_FUNCTIONAL_CHECKS_COMPLETED_WITH_LIMITS','verified_utc':now(),'url':'http://127.0.0.1:5201/','previous_blocker':'Resolved after Codex restart; initial server unavailable, restarted staging only','screenshots':[p.relative_to(ROOT).as_posix()for p in (DOC/'evidence').glob('*.jpg')],'actual_video':video,'performance_summary':'documentation/m155/browser-performance-summary.json','workflow':'documentation/m155/browser-workflow.json','visual_quality':'PENDING','performance_acceptance':'CONDITIONAL','geospatial_acceptance':'PARTIAL'};save(DOC/'visual-status.json',visual)
 header='2 November 2026, WIB. Staging http://127.0.0.1:5201/.\n\nMANUAL / RANDOM SCENARIO — NOT HISTORICAL OBSERVATION.\n\nPROVISIONAL GEDANGAN NETWORK — NOT FIELD CALIBRATED.\n\n'
 rows=['| Run / kamera | Sampel | Median window-median FPS | Minimum window p5 | Active range | Max rolling stalls >50ms | JS heap MiB |','| --- | --- | --- | --- | --- | --- | --- |']
 for q in summary:rows.append(f"| {q['run_id']} / {q['camera']} | {q['samples']} | {q['median_of_window_fps_medians']:.1f} | {q['minimum_window_p5_fps']:.1f} | {q['active_range']} | {q['maximum_rolling120_frame_stalls_over50ms']} | {q['heap_mib_range']} |")
 duration=float(probe['format']['duration']);frames=probe['streams'][0]['nb_read_frames']
 report=f'''# M15.5 — Visual Verification and Performance

{header}
## Keputusan setelah browser terbuka

**Browser functional workflow terverifikasi dengan batas pengujian; VISUAL QUALITY PENDING; PERFORMANCE CONDITIONAL; GEOSPATIAL PARTIAL.** Blocker Browser Use lama sudah teratasi setelah restart. Server5201 yang berhenti dinyalakan kembali. Laporan ini menggantikan status visual BLOCKED sebelumnya, bukan menaikkan validitas fisik jaringan.

## Pemeriksaan UI aktual

Rekaman500,1000,3000,5000 dipilih melalui UI. Kamera top-down, intersection dan rail, fullscreen/return, play/pause, kecepatan1/5/10, slider Home/End/PageUp/PageDown serta repeated switching diuji. Baseline3000 menampilkan1346tiba/568aktifakhir/1086pending terpisah dari current timestamp. Road selector `w562358500_s11_p0_0_f` menampilkan source562358500, lane2×101.25m, classes dan dua downstream connections. Pada t3240s:49active/49stopped,461distinct first-observed edge visits,600pendingorigin akhir. Count cohort tidak disebut count edge.

Save Scenario dan Duplicate→Save diuji. Input100 diubah999, kemudian Load memulihkan100. Generate dua kali pada nama original/salinan benar-benar menjalankan SUMO: run `db7bf706bc67e37ce0910eef` dan `9524cce7fcc0fd378229cf83`, exact road request cohort sama. Keduanya100requested/routed/loaded/departed/moved,93arrived,7active,0pending,0failed; independent FCD/XML audits PASS. Tidak ada console error/warning pada pemeriksaan browser. Ini menambah dua audit terpisah di luar delapan eksperimen utama.

## Bukti visual aktual

`documentation/m155/evidence/topdown-3000.jpg`, `intersection-5000.jpg`, `connectivity-origin.jpg`, `rail-camera.jpg` adalah screenshot browser baru. Teks screenshot cenderung lunak pada kualitas capture; nilai diperiksa lewat DOM, video watermark diperiksa terpisah. Screenshot `rail-camera.jpg` pada t688s berada setelah event crossing. Bukti tambahan `rail-crossing-1796.jpg` pada baseline5000 memperlihatkan kereta aktual di rel crossing, barrier tertutup dan antrean road; audit FCD baseline5000 juga menghasilkan0recorded offtrack/steady-red-entry. Tidak mengklaim clearance fisik lapangan. Validasi red-entry/offtrack tetap berasal dari FCD/controller audit yang tersimpan.

Video actual `documentation/m155/evidence/actual-playback.webm`:1280×800, durasi{duration:.3f}s, {frames}decoded frames. Tombol recorder merekam live canvas baseline3000 pada1× sekitart3240s, dengan dua watermark, tanggal/WIB, timestamp dan statistik akhir. Frame5s diekstrak dengan FFmpeg dan diperiksa: gambar jalan/antrean aktual tampak, tulisan terbaca, tidak blank. Salinan MP4 H.264 juga tersedia di `actual-playback.mp4` untuk pemutaran umum. Ini rekaman aktual yang diberi overlay teks, bukan kendaraan sintetis/animasi pengganti. `video-frame-5s.png` adalah frame video, bukan screenshot UI.

![Frame actual video baseline3000](documentation/m155/evidence/video-frame-5s.png)

Renderer geometry/movement dipertahankan. Perubahan `world.tsx` hanya menambahkan telemetry median/camera/time/network version; bukan desain ulang atau perbaikan geometri. Kendaraan/road/context masih sederhana; visual tidak diberi premium/presentation aesthetic PASS. Desktop1920×1080 diuji; default panel sempit tidak otomatis mendapat sertifikasi layout responsif.

## Performa browser terukur

Raw {len(raw)}files / {len(samples)}render samples, {len(measured)}sudah mempunyai FPSmedian. Retain semua sample lama dan baru, termasuk rendah. Page session maksimum tercatat{value['session_elapsed_max_s']:.1f}s. Ini durasi halaman terbuka, **bukan klaim seluruh waktu merupakan playback kontinu**. Segmen playback kontinu5000 teramati darit0s ke1494.2s pada10x (sekitar149s wall), kemudian seek1796untuk crossing dan resume menuju horizon. Long playback yang teramati dan timestamp ada di raw sample; background/offscreen serta switching tetap memengaruhi pengukuran. Tidak menyebut seluruh horizon60min dimainkan kontinu1× atau soak test berjam-jam.

{chr(10).join(rows)}

Minimum p5 di seluruh sample yang dipertahankan:{value['minimum_p5_all_retained_samples']:.2f}FPS. JS heap maksimum{value['maximum_heap_mib_all_retained_samples']:.1f}MiB. Penurunan/stalls saat switching/video/fullscreen tidak dibuang. Tidak ada klaim seluruh sesi lancar atau bebas memory leak. Raw viewport, visibility/focus, speed, time, active, draw calls, memory dan run ID tersedia per file pada `browser-performance/`.

Pemuatan rekaman:

| Run | Wall ms | Frame | Positions |
| --- | --- | --- | --- |
'''+ '\n'.join(f"| {r['run_id']} | {r['wall_ms']:.1f} | {r['frames']} | {r['positions']} |"for r in loads)+'''

FPSwindow memakai rolling120frame; median dari window medians bukan median seluruh frame. P5 minimum adalah window terburuk yang tersimpan; stall rolling tidak dijumlahkan sebagai unique events. Raw sampling sekitar10s tidak menangkap semua stall. JS heap bukanVRAM. Perlu lebih banyak uji perangkat, sesi berjam-jam dan layout panel sempit sebelum janji stabilitas umum.

## Build, regression dan batas

TypeScript dan Vite isolated build terbaru PASS; chunk JS~832KB memberi warning>500KB. Backend model/permission/network tidak diubah saat visual QA. Regresi sebelumnya395tes/394pass/1skip tetap bukti backend; focused17 M15.5 diuji ulang setelah browser QA. Source/output manifests dan snapshot baseline dipertahankan. Original2984files diperiksa ulang saat finalisasi. Tidak menganggap API success sebagai bukti UI; workflow browser aktual dicatat di `browser-workflow.json`.

GeoJSON/source overlays tersedia, tetapi gate station/median/nama/double-track/clearance dan timing resmi belum dipastikan. Pending832lainnya tetapUNRESOLVED. Tidak ada flyover/M16/finalEXE/deletion/GitHub upload.
'''
 (ROOT/'M15_5_VISUAL_VERIFICATION.md').write_text(report,encoding='utf-8')
 p=ROOT/'M15_5_ACCEPTANCE_REPORT.md';s=p.read_text(encoding='utf-8');s=s.replace('browser visual/performance BLOCKED/PENDING','browser workflow terverifikasi dengan batas; visual quality PENDING; performance CONDITIONAL');s=s.replace('UI still unverified','UI Save/Load/Duplicate dan dua Generate aktual juga terverifikasi');s=s.replace('| Visual inspector usability / real video | BLOCKED | Browser Use disabled in Work settings; no M15.5 UI evidence yet |','| Visual inspector usability / real video | VERIFIED with limits | Road selector/source/permissions/actual counts; new screenshots and actual11.94s watermarked video; capture text soft |');s=s.replace('| Visual quality / sustained performance | PENDING | Retained simplified renderer; FPS/loading/memory/session QA not measured |','| Visual quality / sustained performance | PENDING / CONDITIONAL | Actual loads/FPSmedian/p5/stalls/heap recorded; low samples retained; no multi-hour stability guarantee |');s=s.replace('831KB JS','832KB JS');s=s.replace('Aktifkan Browser Use dan jalankan checklist visual/performance, simpan screenshot/video M15.5 aktual; verifikasi','Browser QA dan video kini tersedia; lanjutkan soak test lebih panjang dan review mutu visual pengguna. Verifikasi');s+='\n\n## Pembaruan browser setelah restart\n\nBlocker Browser Use sudah terselesaikan. Lihat laporan visual terbaru, `documentation/m155/browser-workflow.json`, `browser-performance-summary.json` dan `visual-status.json`. Keempat load level sudah dibuka, dua simulasi100kendaraan dijalankan dari UI dengan cohort identik, dan video actual telah diperiksa. Belum ada alasan menaikkan geospatialPARTIAL, full causalUNRESOLVED, visualqualityPENDING atau performanceCONDITIONAL menjadi PASS penuh.\n';p.write_text(s,encoding='utf-8')
 print(json.dumps({'render_samples':len(samples),'median_samples':len(measured),'minimum_p5_all':value['minimum_p5_all_retained_samples'],'session_elapsed_max_s':value['session_elapsed_max_s'],'video_duration':duration},ensure_ascii=True),flush=True)
if __name__=='__main__':main()
