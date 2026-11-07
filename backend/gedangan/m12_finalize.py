"""Data-gated acceptance and final portable archive. No blanket validation claim."""
import json,zipfile,shutil,platform,hashlib,re
from datetime import datetime,timezone,timedelta
from .m12_release import ROOT,REL,APP,DOC,digest,copy,manifest
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def main():
 qa=DOC/'qa';app=load(qa/'application.json');survey=load(qa/'survey.json');present=load(qa/'presentation.json');dist=load(qa/'distribution.json');sync=load(qa/'synchronization-performance.json');source=load(DOC/'SOURCE_INTEGRITY_AUDIT.json');protected=load(DOC/'baseline-final-verification.json')
 for label,v in [('application',app),('survey',survey),('presentation',present),('distribution',dist),('synchronization',sync),('source',source)]:assert v['status']=='PASS',(label,v)
 assert dist['exe_sha256']==digest(APP/'GEDANGAN_TRAFFIC_SIMULATOR.exe'),'Portable QA is stale for this executable'
 assert protected=={'files':9236,'changed':[]},protected
 regression=(DOC/'regression-python.txt').read_text(encoding='utf-8-sig');assert 'Ran 344 tests' in regression and 'OK (skipped=1)' in regression
 assert 'Final M10 core assertions 31' in (DOC/'regression-m10-core.txt').read_text(encoding='utf-8-sig')
 date=datetime.now(timezone(timedelta(hours=7))).date().isoformat();gates={'SOFTWARE FUNCTIONALITY':'PASS','3D DIGITAL TWIN':'PASS','SUMO SIMULATION INTEGRITY':'PASS','PRESENTATION READINESS':'PASS','OFFLINE DEPLOYMENT':'PASS','WINDOWS PORTABILITY':'PASS','FIELD SURVEY WORKBENCH':'PASS','REPORT EXPORT':'PASS','EMPIRICAL BASELINE':'BLOCKED','INFRASTRUCTURE FEASIBILITY':'CONCEPT ONLY','HUMAN ACCEPTANCE':'PENDING'}
 result={'product':'Gedangan Traffic Simulator v1.0.0','release_status':'PRESENTATION-READY ILLUSTRATIVE RELEASE','software_release':'SOFTWARE RELEASE READY','presentation':'PRESENTATION READY','release_date':date,'gates':gates,'scope':'Windows x64 frozen portable host tested on this Windows 11 machine, not a clean VM or another physical PC','browser_prerequisite':'Installed Chrome/Edge with WebGL2','protected_files':9236,'python_regression':{'run':344,'passed':343,'skipped':1,'skip_reason':'M09 separate presentation service absent; release duplicate lifecycle tested in actual EXE'},'m10_core_assertions':31,'new_sumo_runs':False,'live_sumo_execution_bundled':False,'calibration_execution':'Requires separately preserved research toolchain after QC; playback distribution has M06 import preview, not a live calibration engine','human_field_validation':False}
 (REL/'FINAL_ACCEPTANCE_REPORT.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
 lines=['# FINAL ACCEPTANCE REPORT',f'Gedangan Traffic Simulator v1.0.0 | EXTREME STUDIOS | {date}','', '**PRESENTATION-READY ILLUSTRATIVE RELEASE**. SOFTWARE RELEASE READY dan PRESENTATION READY untuk penggunaan ilustratif yang diuji. Bukan field-validated production model.','', '| Gate | Status |','|---|---|']+[f'| {k} | {v} |' for k,v in gates.items()]
 lines+=['','## Bukti teknis','- Frozen Windows x64 EXE berjalan tanpa Python/Node/SUMO eksternal; browser Edge/Chrome dengan WebGL2 tetap prerequisite.','- Ekstraksi ke folder baru dengan spasi dan PATH hanya Windows/System32. Tiga cold start, duplicate same PID, clean shutdown, restart persistence, missing-asset rejection dan foreign-port rejection diuji.','- Chrome aktual: tahun 2026/2030/2035/2040, HIGH, pasangan APILL, split sinkron, kamera, fullscreen, preset kualitas, sepuluh bagian presentasi, video Full HD dan ekspor aktual PDF/CSV/JSON.','- Semua non-loopback network request diblokir pada level browser selama QA. Tidak ada request keluar tercatat. Tidak ada firewall/security setting diubah.','- Audit source memverifikasi 23 recording indexes/chunks/scenes dan hash SUMO output asli, bukan membaca laporan saja. Accounting seluruh run tetap benar.','- Regresi: 344 tests dijalankan; 343 lulus, satu skip service M09 terpisah. 31 assertion inti M10 lulus. 9.236 berkas baseline M01-M11 tidak berubah.','- Survey: manual count, shortcut, timestamp, pause/resume, IndexedDB setelah koneksi gagal, browser recovery, duplicate idempotency, SQLite checkpoint/backup/restore, video hash/play/pause/step/annotation/rewind, enam CSV dan JSON lewat importer M06, dan mobile counter diuji.','- PPTX asli 15 slide dan 15 notes, PDF M11, MP4 dan semua 15 gambar dipertahankan. HTML salinan distribusi mengeluarkan inline script ke berkas lokal agar sesuai CSP.','', '## Batas acceptance','- PASS survei adalah acceptance browser/software pada fixture SYNTHETIC_TEST. Lokasi, izin, clock, coverage dan data lapangan tetap memerlukan review manusia.','- Baseline empiris BLOCKED; tidak ada observasi Gedangan yang dipromosikan menjadi verified pada pekerjaan ini.','- Flyover/underpass CONCEPT ONLY. Tidak ada bypass clearance, legalitas, swept path, lane permission atau oversize.','- Runtime distribusi memutar hasil SUMO yang direkam, bukan menjalankan simulasi/kalibrasi SUMO baru. M06 preview dan dataset versioning tersedia. Eksekusi kalibrasi baru memakai toolchain riset terpisah sesudah QC; baseline lama tidak ditimpa.','- Uji Windows dilakukan di mesin ini, bukan clean VM, PC kedua, ponsel fisik atau proyektor fisik. Binary belum ditandatangani sertifikat penerbit.','- HUMAN ACCEPTANCE tetap PENDING. Tidak ada klaim FULLY VALIDATED.','', '## Mulai','Ekstrak seluruh paket lalu buka APPLICATION/GEDANGAN_TRAFFIC_SIMULATOR.exe. Alternatif: START_GEDANGAN_TRAFFIC_SIMULATOR.bat. Tutup melalui tombol aplikasi atau STOP_GEDANGAN_TRAFFIC_SIMULATOR.bat. Baca DOCUMENTATION/QUICK_START_ID.pdf.']
 acceptance='\n'.join(lines)+'\n';(REL/'FINAL_ACCEPTANCE_REPORT.md').write_text(acceptance,encoding='utf-8')
 (REL/'README_FIRST.md').write_text(f'''# GEDANGAN TRAFFIC SIMULATOR v1.0.0
3D Traffic Digital Twin & Scenario Analysis - EXTREME STUDIOS

Rilis {date}: PRESENTATION-READY ILLUSTRATIVE RELEASE.

1. Ekstrak seluruh folder ke lokasi lokal yang dapat ditulis. Jangan jalankan langsung dari ZIP atau pindahkan EXE sendirian.
2. Buka APPLICATION/GEDANGAN_TRAFFIC_SIMULATOR.exe. Tidak perlu Codex, terminal developer, Python, Node atau SUMO.
3. Microsoft Edge atau Chrome dengan WebGL2 perlu sudah terpasang. Browser tidak dibundel. Tidak perlu koneksi internet setelah ekstraksi.
4. Pilih menu simulasi, comparison, field data, reports atau presentation. PDF/HTML/video tersedia sebagai cadangan.
5. Akhiri dengan Tutup layanan atau STOP_GEDANGAN_TRAFFIC_SIMULATOR.bat. Menutup tab saja tidak menghentikan host.

Data Anda tersimpan di USER_DATA. Backup setelah layanan ditutup; video sumber disimpan terpisah. USER_DATA sengaja tidak diisi dengan survei QA.

Dokumen: DOCUMENTATION/QUICK_START_ID.pdf, USER_MANUAL_ID.pdf, TECHNICAL_MANUAL_ID.pdf. Hasil gate terpisah di FINAL_ACCEPTANCE_REPORT.md.

Baseline empiris BLOCKED - DATA REQUIRED. Infrastruktur besar CONCEPT ONLY. Penerimaan manusia PENDING. Ini playback actual SUMO dengan demand ilustratif; eksekusi kalibrasi/rekaman baru memerlukan toolchain riset terpisah setelah data lolos QC.
''',encoding='utf-8')
 (REL/'RELEASE_NOTES.md').write_text('''# Release notes v1.0.0
- Frozen portable Windows host; Python runtime dan dependency yang diperlukan dibundel.
- Satu navigasi aplikasi membungkus build 3D M10 dan workbench M08.5 tanpa menimpa source lama.
- Empat launcher, host/manifest checks, duplicate control, bounded loopback server dan token shutdown.
- Export PDF/CSV/JSON berdasarkan angka asli. CSV menyertakan baseline dan delta; hasil negatif tidak disembunyikan.
- Performance/Balanced/Presentation mengubah drawing resolution, bukan trace, geometry atau parameter SUMO. Balanced default.
- M12 response adapter memperbaiki desktop kecil dan intrinsic-grid overflow survei mobile; label historis M08.5 diperbarui hanya di lapisan release.
- HTML M11 salinan distribusi diadaptasi ke external local scripts/CSP dan tautan port M12. PPTX/PDF/video/gambar M11 byte-identical.
- Ketergantungan browser terpasang tetap eksplisit. Tidak ada SUMO executable, research venv, Node, source workspace lengkap atau video lapangan di paket.
- Data update berupa versioned session/export + preview M06. Live calibration execution tidak dibundel; tetap memerlukan toolchain riset dan QC lapangan.
- Limitasi: belum code-signed; pengujian satu PC Windows 11, bukan sertifikasi semua perangkat atau proyektor fisik.
''',encoding='utf-8')
 surveytext='''# M12 SURVEY READINESS / penutupan QA browser M08.5
**BROWSER SOFTWARE ACCEPTANCE PASS dalam distribusi M12.** Status laporan M08.5/M11 historis tidak ditimpa.

Fixture SYNTHETIC_TEST terisolasi. Manual count, class/shortcut, WIB timestamps, pause/resume, IndexedDB saat command request diputus, browser restart/retry exactly once, SQLite checkpoint, backup/restore cabang baru, duplicate command prevention, CSV/JSON export dan 12 preview importer M06 lulus. File video MP4 lokal benar-benar di-hash, diregister, dimainkan, dijeda, di-step dan dianotasi; rewind tidak membuka kembali token yang sudah dicatat. Mobile 390x844 counter dan save diuji di Chrome viewport, bukan ponsel fisik.

Percobaan ulang pada video dengan SHA yang sudah pernah dihitung ditolak sebagai replay/rewind lintas sesi. Ini kontrol duplikasi yang benar; acceptance final memakai workspace kosong. QA tidak mematikan kontrol tersebut.

Lokasi/izin/bukti field belum disetujui. SYNTHETIC_TEST tetap DEMO_SYNTHETIC pada M06; tidak dipromosikan menjadi OBSERVED_FIELD. Reviewer manusia dan QC sebelum kalibrasi tetap wajib. Empirical baseline BLOCKED. Workbench software lulus, kesiapan operasi survei lapangan belum disahkan manusia.
'''
 (REL/'M12_SURVEY_READINESS.md').write_text(surveytext,encoding='utf-8')
 (REL/'M12_PRESENTATION_ACCEPTANCE.md').write_text('''# M12 PRESENTATION ACCEPTANCE
PASS untuk software/offline. Paket M11 digunakan kembali: 15-slide PPTX (15 notes), 15-page PDF, 15 rendered slide images, local HTML, Full HD MP4, naskah 5/15 menit, panduan diskusi, checklist dan lampiran. Fifteen-slide HTML navigation/keyboard/technical notes dan setiap tautan entry diuji aktual dalam Chrome; gambar lengkap. PPTX/slide/PDF/video asli byte-identical. Font Arial tersedia pada mesin QA; PPTX pada mesin lain memerlukan pembaca Office/font yang sesuai, PDF/HTML menggunakan render lokal.

Sepuluh bagian guided demo M12 dan fullscreen diuji. Semua halaman manual dan contoh report dirender dengan Poppler dan diperiksa visual. Rehearsal M11 5 dan 15 menit merupakan bukti historis terpisah, tidak diklaim diulang M12. PowerPoint native GUI tidak dibuka ulang di M12. Proyektor fisik dan HUMAN ACCEPTANCE tetap PENDING. Beberapa slide M11 menyebut status browser M08.5 saat M11; lihat M12_SURVEY_READINESS.md untuk hasil penutupan terbaru.
''',encoding='utf-8')
 (REL/'M12_OFFLINE_TEST.md').write_text('''# M12 OFFLINE TEST
PASS pada scope yang diuji. Paket diekstrak ke folder baru dengan spasi. Frozen EXE dijalankan dengan PATH hanya Windows/System32, tanpa PYTHONPATH/PYTHONHOME/VIRTUAL_ENV/CONDA_PREFIX/SUMO_HOME/NODE_PATH. Tiga clean start/shutdown dan duplicate same PID lulus. SQLite pulih sesudah host restart. Aset hilang menolak startup; foreign port tidak diambil alih.

Chrome aktual memblokir semua HTTP(S) non-loopback pada level browser, bukan menonaktifkan adaptor OS. 3D playback, 2026/2030/2035/2040 HIGH, split comparison, local presentation, actual MP4 dan export PDF/CSV/JSON berjalan; tidak ada external request. OS firewall/security tidak diubah. Windows/Chrome sendiri mungkin memiliki background services; itu di luar request aplikasi yang direkam.

Browser Chrome/Edge WebGL2 terpasang merupakan prerequisite. Browser engine tidak dibundel. Uji dilakukan pada PC ini, bukan clean VM atau perangkat kedua. Final ZIP CRC/hash tercatat di MANIFESTS/ARCHIVE_MANIFEST.json di luar ZIP untuk menghindari hash sirkular.
''',encoding='utf-8')
 perf='\n'.join(f"- {s['quality']}: measured mean {s['stats']['fps_mean']:.2f} FPS, p5 {s['stats']['fps_p5']:.2f}; {s['stats']['stalls_over_50ms']} stalls >50 ms; draw calls {s['stats']['draw_calls']}." for s in sync['samples'])
 hardware=load(DOC/'hardware-ram.json');ram=hardware['TotalPhysicalMemory']/1024**3
 qatext=f'''# M12 QA REPORT
PASS teknis sesuai gate FINAL_ACCEPTANCE_REPORT.md. Bukan field validation.

- Regresi Python: 344 run / 343 pass / 1 service-dependent skip. Inti M10: 31 assertions pass.
- Application actual Chrome: {len(app['checks'])} checks, 0 fatal page errors, 0 failed responses, 0 external request.
- Survey: {len(survey['checks'])} browser checks; state/provenance dan importer M06 dipertahankan.
- Distribusi: {len(dist['cycles'])} cold starts; duplicate launch memakai PID sama; restart, missing-asset dan port conflict diuji.
- Empat waktu uji cocok dengan signal/rail source event; renderer/build M10 unchanged.
- Resolusi 1920x1080, 1366x768 dan field-workbench viewport 390x844 diuji. Tidak ada klaim ponsel fisik/proyektor.

## Hardware/performance aktual
Windows 11 Pro, AMD Radeon Graphics, RAM terlihat OS {ram:.2f} GiB. WMI AdapterRAM dilaporkan terpisah dan bukan konfirmasi VRAM fisik 6 GB. Chrome melaporkan ANGLE AMD Direct3D11, bukan jaminan perangkat target lain. Sampel rolling render-loop sekitar 9 detik per preset, satu baseline 2026; proses authoring/QA lain dapat berlangsung bersamaan. Ini bukan benchmark lengkap semua rekaman.
{perf}
Balanced dipilih sebagai default; preset hanya membatasi rasio drawing pixel.

## Temuan dan perbaikan
- Missing SUMO helper saat frozen import diperbaiki dengan hidden import helper; engine SUMO tidak dieksekusi atau dibundel.
- Mobile intrinsic grid overflow diperbaiki di M12 response stylesheet.
- Slide HTML inline script dieksternalisasi dalam salinan distribusi agar berjalan dengan CSP lokal; duplicate CSP directive dibersihkan.
- Windows sempat menahan port setelah listener fault injection. Handler startup kini tidak membuka dialog di child service; bind failure dilaporkan cepat. Uji foreign port memakai port tersendiri agar tidak menyamakan TIME_WAIT dengan aplikasi aktif.
- Re-run video yang sama ditolak replay guard secara benar; final survey memakai dataset QA kosong.
- Uji yang gagal atau terhenti bukan bukti PASS; hasil final eksplisit tersedia di QA_EVIDENCE.
'''
 (REL/'M12_QA_REPORT.md').write_text(qatext,encoding='utf-8')
 (REL/'MILESTONE_12_REPORT.md').write_text(acceptance+'\n'+qatext+'\n'+surveytext,encoding='utf-8')
 for p in qa.iterdir():
  if p.is_file() and p.suffix in ['.json','.png','.pdf','.csv'] and 'failure' not in p.name and 'initial-' not in p.name:copy(p,REL/'QA_EVIDENCE'/p.name)
 for name in ['SOURCE_INTEGRITY_AUDIT.json','baseline-final-verification.json','regression-python.txt','regression-m10-core.txt','hardware-ram.json','hardware-gpu.json']:copy(DOC/name,REL/'QA_EVIDENCE'/name)
 for p in qa.glob('*.png'):copy(p,REL/'SCREENSHOTS'/p.name)
 for name in ['FINAL_ACCEPTANCE_REPORT.md','M12_QA_REPORT.md','M12_SURVEY_READINESS.md','M12_OFFLINE_TEST.md','M12_PRESENTATION_ACCEPTANCE.md','RELEASE_NOTES.md','MILESTONE_12_REPORT.md']:copy(REL/name,DOC/name)
 copy(REL/'MILESTONE_12_REPORT.md',ROOT/'documentation/MILESTONE_12_REPORT.md')
 metadata=load(REL/'MANIFESTS/RELEASE_METADATA.json');metadata['release_date']=date;metadata.pop('release_date_status',None);(REL/'MANIFESTS/RELEASE_METADATA.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
 manifest();files={p.relative_to(REL).as_posix():{'sha256':digest(p),'bytes':p.stat().st_size} for p in REL.rglob('*') if p.is_file() and p.name!='BUILD_MANIFEST.json' and 'USER_DATA' not in p.relative_to(REL).parts and p.name!='ARCHIVE_MANIFEST.json'}
 build={'version':'1.0.0','release_date':date,'files':files,'baseline_inventory_sha256':digest(DOC/'BASELINE_SHA256.json'),'baseline_files':9236,'tested_exe_sha256':dist['exe_sha256'],'build_recipe':'documentation/m12/GEDANGAN_TRAFFIC_SIMULATOR.spec; backend.gedangan.m12_release; m12_docs; m12_audit; tests/m12; m12_finalize','browser_prerequisite':'Chrome or Edge with WebGL2, already installed'}
 (REL/'BUILD_MANIFEST.json').write_text(json.dumps(build,indent=2),encoding='utf-8');copy(REL/'BUILD_MANIFEST.json',REL/'MANIFESTS/BUILD_MANIFEST.json')
 target=ROOT/'FINAL_RELEASE/GEDANGAN_TRAFFIC_SIMULATOR_v1.0.0_PORTABLE.zip'
 with zipfile.ZipFile(target,'w')as z:
  for p in REL.rglob('*'):
   if p.is_file() and 'USER_DATA' not in p.relative_to(REL).parts and p.name!='ARCHIVE_MANIFEST.json':z.write(p,'GEDANGAN_TRAFFIC_SIMULATOR/'+p.relative_to(REL).as_posix(),compress_type=zipfile.ZIP_STORED if p.suffix in ['.gz','.png','.pdf','.pptx','.mp4']else zipfile.ZIP_DEFLATED)
 with zipfile.ZipFile(target)as z:assert z.testzip()is None;count=len(z.namelist())
 archive={'file':target.name,'bytes':target.stat().st_size,'sha256':digest(target),'files':count,'archive_crc':'PASS','tested_exe_sha256':dist['exe_sha256']};(ROOT/'FINAL_RELEASE/ARCHIVE_MANIFEST.json').write_text(json.dumps(archive,indent=2),encoding='utf-8')
 (ROOT/'FINAL_RELEASE/README_FIRST.md').write_text('Ekstrak GEDANGAN_TRAFFIC_SIMULATOR_v1.0.0_PORTABLE.zip lalu buka APPLICATION/GEDANGAN_TRAFFIC_SIMULATOR.exe di folder hasil ekstraksi. Salinan siap pakai juga berada di GEDANGAN_TRAFFIC_SIMULATOR/. Lihat FINAL_ACCEPTANCE_REPORT.md untuk gate dan batas yang diuji.\n',encoding='utf-8')
 print(json.dumps({'acceptance':result,'archive':archive}),flush=True)
if __name__=='__main__':main()
