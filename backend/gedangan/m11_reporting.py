"""M11 release decision from actual artifact, source and browser evidence."""
from pathlib import Path
import json,re,hashlib,zipfile,shutil,subprocess
from datetime import datetime
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'presentation_demo/m11';DOC=ROOT/'documentation';QA=OUT/'qa'
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()

def main():
 a=load(QA/'REHEARSAL_A.json');b=load(QA/'REHEARSAL_B.json');c=load(QA/'REHEARSAL_C_FINAL.json');projector=load(QA/'projector-qa.json');fallback=load(QA/'fallback-qa.json');source=load(QA/'source-audit.json');pdf=load(QA/'pdf-structure.json');visual=load(QA/'visual-review.json');numeric=load(OUT/'M11_NUMERIC_DATA_AUDIT.json');baseline=load(QA/'baseline/browser-qa.json');native=load(DOC/'m11/deck-validation.json');content=load(OUT/'M11_PRESENTATION_CONTENT.json');package_smoke=load(QA/'package-smoke.json')
 assert 'Final M10 core assertions 31' in (DOC/'m11/baseline-m10-core.txt').read_text(encoding='utf-8-sig')
 reg=(DOC/'m11/baseline-regression.txt').read_text(encoding='utf-8-sig');match=re.search(r'Ran (\d+) tests in ([\d.]+)s\s+OK',reg);old=int((DOC/'m11/protected-files-verification.txt').read_text(encoding='utf-8-sig').strip());launcher=load(DOC/'m11/actual-launcher.txt');reuse=load(DOC/'m11/actual-launcher-reuse.txt')
 assert len(content['slides'])==15
 with zipfile.ZipFile(OUT/'M11_PRESENTASI_TEKNIS_GEDANGAN.pptx')as z:
  slides=[n for n in z.namelist()if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)];assert len(slides)==15;assert z.testzip()is None
  pptx_notes=''.join(z.read(n).decode()for n in z.namelist()if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n));assert '7e4475b8c3ecdfa4b025'in pptx_notes and '9c9e07a0a18d0cfec64f'in pptx_notes
 assert sha(OUT/'GEDANGAN_3D_DEMO.mp4')==sha(ROOT/'presentation_demo/m10/GEDANGAN_3D_DEMO.mp4')
 for row in numeric['rows']:
  m=row['metrics'];assert m['requested']==m['routable']+m['failed_routes'];assert m['routable']==m['departed']+m['not_departed'];assert m['departed']==m['arrived']+m['running_at_end']
 rehearsals=all(x['status'].startswith('PASS')for x in[a,b,c]);live=baseline['overall'].startswith('PASS')and len(baseline['checks'])==18
 gates=[('M10 visual application works',live),('One-click launcher / port detection / reuse',launcher['status']=='READY_TO_PRESENT'and reuse['instance_reused']),('Required actual recordings available',source['original_recordings']==23),('3D timed presentation rehearsals',rehearsals and a['duration_s']>=300 and b['duration_s']>=900),('Camera / playback controls',live),('Railway and signal demonstration',live and rehearsals),('Year selection',rehearsals),('Comparable scenario and adverse result',rehearsals),('Correct labels and all-run accounting',len(numeric['rows'])==23),('Complete presentation deck',len(slides)==15 and visual['status']=='PASS'),('PDF presentation',pdf['presentation_pages']==15),('Presenter scripts',all((OUT/f'M11_NASKAH_PRESENTASI_{v}_MENIT.md').is_file()for v in[5,15])),('Field discussion handout',pdf['handout_pages']==2),('Offline fallback and actual video',fallback['status']=='PASS'and c['status']=='PASS'and package_smoke['status']=='PASS'),('Native Chrome viewport/zoom/fullscreen QA',projector['status']=='PASS'and len(projector['cases'])==6),('No unexplained critical runtime errors',all(not x.get('errors',x.get('page_errors',[]))for x in[a,b,c,fallback,projector])),('Regressions',bool(match)and int(match[1])==344),('Old files preserved',old==8104),('No fabricated traffic measurements',source['empirical_gate'].startswith('BLOCKED')),('Infrastructure still conceptual',source['S06_S07']=='CONCEPT_ONLY')]
 status='TECHNICAL_PRESENTATION_PACKAGE_READY_PASS'if all(v for _,v in gates)else'PARTIAL'
 decision={'status':status,'date_local':'2026-11-01','gates':[{'criterion':n,'pass':v}for n,v in gates],'human_acceptance':'HUMAN FIELD / PROJECTOR ACCEPTANCE PENDING','empirical_baseline':'2026 NOT EMPIRICALLY CALIBRATED','M12_started':False};write(OUT/'M11_TECHNICAL_PRESENTATION_ACCEPTANCE.json',decision)
 table='\n'.join(f'| {i+1} | {name} | {"PASS"if value else"PARTIAL"} |'for i,(name,value)in enumerate(gates))
 perf=[]
 for name,r in [('A',a),('B',b)]:
  samples=r.get('performance',[])
  perf.append({'rehearsal':name,'samples':len(samples),'mean_reported_fps':sum(v['fps_mean']for v in samples)/len(samples)if samples else None,'minimum_rolling_p5_fps':min(v['fps_p5']for v in samples)if samples else None,'max_over_50ms_in_rolling_window':max(v['stalls_over_50ms']for v in samples)if samples else None,'scope':'Overlapping browser windows, sampled every ~2 s during automated presentation. Authoring/other desktop work may be concurrent. Do not sum stalls or infer physical VRAM.'})
 write(QA/'rehearsal-performance-summary.json',{'scope':'Measured current sessions, not a new universal hardware guarantee','results':perf})
 limitations='''- Baseline 2026 belum terkalibrasi empiris. Semua angka lalu lintas yang dipakai berasal dari simulasi dengan demand/kontrol/pertumbuhan provisional.
- Bangunan, vegetasi, marka/furniture dan dimensi model belum menjadi geometri/armada hasil survei.
- Short/internal lanes, rail/stop-line alignment dan clearance tetap memiliki batas jaringan sumber. M11 tidak mengubah topologi atau mengesahkan legalitas.
- Native PowerPoint GUI dan proyektor fisik belum diperiksa. PPTX telah divalidasi struktur, diimpor ulang dan dirender melalui Artifact Tool; PDF memakai render final tersebut. Penerimaan presenter manusia dan ruangan rapat tetap terpisah.
- M08.5 tetap PARTIAL_BROWSER_ACCEPTANCE_PENDING. Lembar diskusi/form preview tidak mengesahkan workbench untuk survei produksi.
- Bila launcher memakai ulang layanan M10 lama tanpa adapter M11, halaman awal menjelaskan perlunya menutup layanan melalui aplikasi dan menjalankan launcher M11 kembali untuk layout ringkas pada layar kecil/zoom besar. Tidak ada layanan lain yang dihentikan diam-diam.
- Presenter sebaiknya memakai zoom 100%/125% di 1366×768 agar ruang 3D lebih luas. Zoom 150% telah diuji dengan adapter M11 dan seluruh kontrol tetap dapat diakses.
- Internet tidak diperlukan untuk demo. Python 3.12+ lokal tetap diperlukan untuk layanan 3D; deck HTML/PDF/video tersedia tanpa server.
- M12 tidak dimulai. Tidak ada klaim official forecast, solusi terbaik, efektivitas lapangan atau kesiapan konstruksi.'''
 (OUT/'M11_TECHNICAL_PRESENTATION_ACCEPTANCE.md').write_text(f'''# Penerimaan paket presentasi M11

**{status.replace('_',' ')}**

1 November 2026. **HUMAN FIELD / PROJECTOR ACCEPTANCE PENDING** adalah gate terpisah.

| No | Kriteria | Hasil |
|---|---|---|
{table}

Angka pada deck dan dua tingkat penjelasan memakai M11_NUMERIC_DATA_AUDIT.json yang sama. Tidak ada data observasi yang dikarang. M12 tidak dimulai.
''',encoding='utf-8')
 report=f'''# MILESTONE 11 — Paket Presentasi Teknis Gedangan

**{status.replace('_',' ')}**

Tanggal: 1 November 2026, Asia/Jakarta. Lingkup hanya M11.

## Executive summary

Paket berisi aplikasi M10 yang dipakai kembali, launcher satu langkah, deck 15 slide Indonesia, PDF 15 halaman, deck HTML offline dengan penjelasan Eksekutif/Teknis, video M10 aktual 106,4 detik, naskah 5/15 menit, lembar diskusi dua halaman, checklist, lampiran teknis dan referensi tanya jawab. Posisi produk: GEDANGAN TRAFFIC SIMULATOR, 3D Traffic Digital Twin & Scenario Analysis, EXTREME STUDIOS. Status ilmiah PRESENTATION-READY ILLUSTRATIVE TRAFFIC SIMULATION; baseline 2026 NOT EMPIRICALLY CALIBRATED.

## Source audit dan reuse M10

Laporan M09/M10, initial/final audit, acceptance, contact sheet, video, browser/class evidence, source renderer/runtime, 23 recording indexes, scenario manifests, M06 empirical gate dan kesiapan M08.5 diperiksa. Audit sumber dan hash per berkas tersimpan pada qa/source-audit.json. {source['M10_manifest_files_verified']} berkas manifest M10 cocok. Video M11 adalah salinan byte-identical dari video M10 dan benar-benar dimainkan melalui elemen video Chrome. Tidak ada footage simulasi buatan. Sumber/caption screenshot M10 dipertahankan.

Checkpoint M11 melindungi {old} file lama, 17.301.071.597 byte, source checkpoint 726 file. Daftar hash dan scope berada di documentation/m11. Exclusions: M11 namespace, installed dependencies/toolchain, caches/locks, SQLite hidup/WAL dan telemetry append-only M09/M10. M11 testing menggunakan port terisolasi dan log M11; output/source/network/data M01–M10 tidak ditimpa.

## Changes made

Tidak ada frontend 3D baru. Build dan renderer M10 tetap byte-identical. m11_launch.py memakai host M10 yang sama, protokol service/port detection yang kompatibel, preflight hash seluruh cache, instance reuse dan clean shutdown. Service yang dibuat M11 mengalihkan telemetry ke namespace M11. Port produksi 5186; port 5187/5188 hanya uji terisolasi.

Adapter presentasi M11 menambahkan stylesheet/skrip lewat response HTML, bukan menulis ulang build M10. CSS ringkas memperbaiki ruang kanvas pada 1366×768 dengan zoom 150%. Skrip hanya memperjelas pesan pemulihan agar path teknis tidak tampil kepada audiens. Tidak mengubah metrics, routes, controller, FCD, camera math, demand atau playback lifecycle. Halaman awal lokal memisahkan verifikasi disk dari preload browser: START tetap diblokir sampai preload M10 selesai. Pemilihan rekaman lain memiliki indikator loading dan tidak memakai run pengganti.

## Deck dan bahan pertemuan

Urutan 15 slide mengikuti brief: cover, pertanyaan lalu lintas, area, 3D, kendaraan/simpang/rel, SUMO, baseline, growth, indikator, skenario, comparison, konsep infrastruktur, keterbatasan, survei dan penutup. Native tables pada slide 7/10, native chart pada slide 8, editable text dan speaker notes. Grafik memakai snapshot literal dari angka audit; tidak mengklaim formula source workbook dipertahankan. Final PPTX lolos pemeriksaan integritas/layout/font/chart workbook dan first-party import. Semua slide final diimpor ulang dan dirender. PDF statis memakai render 1920×1080 tersebut; bukan file kosong. Review individual dan contact sheet ada pada qa/visual-review.json dan M11_SLIDE_CONTACT_SHEET.png.

Naskah menjelaskan tampilan, sumber, makna, batas dan pertanyaan audiens pada sepuluh bagian. Durasi naskah merupakan target, bukan klaim kecepatan bicara manusia. Mode Eksekutif/Teknis pada deck HTML hanya mengganti kedalaman catatan dari satu file konten, tanpa dataset kedua. Materi utama bebas terminal, raw JSON, benchmark dan stack trace. Lampiran audit/provenance disimpan terpisah.

Tujuh calon lokasi M06/M08.5 dipertahankan dan tidak dianggap disetujui. Lembar rapat menyediakan ruang keputusan tentang ruas/arah, izin, posisi aman, sesi, kelas, turning, event palang, fase sinyal, travel time, antrean/count/meter/censoring, hambatan samping, QC, PIC dan kelengkapan. Tidak ada keputusan peserta yang diisi otomatis.

## Numeric data audit

Semua 23 run memiliki ID, tahun, scenario/growth, seed, horizon, manifest/index hash, units, definisi dan provisional classification. Accounting: requested=routable+failed routes; routable=departed+not departed; departed=arrived+running; not arrived=requested-arrived. Baseline 2026 S00 REFERENCE: requested240, routable/departed206, arrived183, running23, failed34, not departed0, not arrived57. Identitas ini diverifikasi terhadap index asli.

Pasangan 2040 HIGH comparable: S00 f6b49f6119ee784cf062 arrived356 / requested500; S01 9c9e07a0a18d0cfec64f arrived328 / requested500. Delta -28, WORSENED IN THIS SIMULATION untuk arrived. Running80/102, not departed8/14, failed routes56/56, not arrived144/172. Waiting mean departed bersyarat, bukan manfaat seluruh demand. Growth REFERENCE requested240/269/311/360 untuk 2026/2030/2035/2040. Rate mobil3,5%/tahun, motor umum2,5% dan override northbound4% adalah asumsi M07, bukan prakiraan resmi.

## Actual rehearsal A / B / C

| Rehearsal | Hasil | Durasi / batas |
|---|---|---|
| A eksekutif | {a['status']} | {a['duration_s']:.2f} s, sepuluh bagian, start/replay/overview/shutdown |
| B teknis | {b['status']} | {b['duration_s']:.2f} s, sepuluh bagian, tahun/skenario/adverse comparison |
| C gangguan | {c['status']} | {c.get('duration_s',0):.2f} s, service stop, refused reload, browser restart, offline deck/video, cache reverify dan recovery |

A/B adalah UI otomatis bertimed dengan screenshot tiap bagian, console/failed responses, loading dan frame pacing. Tidak ada klaim presenter manusia menjalankan naskah. Percobaan awal A terputus saat sesi berganti dan disimpan sebagai interrupted, bukan PASS. A/B penuh kemudian dijalankan ulang dalam helper tersembunyi. C memiliki log console/request failures yang menandai connection-refused saat shutdown sebagai gangguan disengaja. Video C merekam sesi aktual sebelum/sesudah restart; video utama cadangan tetap MP4 M10.

## Projector UX, offline, fallback dan recovery

Enam kombinasi native Chrome: 1920×1080 dan1366×768 pada zoom100/125/150%, fullscreen guided presentation, camera change dan split. Batas presenter/kanvas, horizontal overflow, comparison banner serta actual screenshots diperiksa. Ini viewport simulasi, bukan proyektor fisik. Semua aset/font sistem/gambar/video lokal, external request0 pada uji yang memblokir akses luar.

Missing-index fault injection benar-benar mengembalikan404 pada fetch browser terisolasi. Start tetap disabled, canvas tidak menampilkan run lain, pesan recovery jelas. Setelah fault dilepas, reload kembali ke rekaman valid. Deck HTML15slide dan MP4 tersedia saat host berhenti. Uji C menutup host test sungguhan, merestart browser/server dan memverifikasi ulang23recordings. Tidak ada output sumber yang dihapus untuk mensimulasikan kerusakan. Paket ZIP diekstrak ke lokasi uji yang diperiksa, cold-start dengan global Python, lalu actual Chrome membuka renderer, CSS M11, baseline 2026, kamera rel dan playback. Seluruh 23 recording lolos preflight dan host hasil ekstraksi berhenti bersih. Bukti qa/package-smoke.json, package-browser-smoke.json dan package-extracted-runtime.png.

## Regression dan performa

{int(match[1])if match else'UNCONFIRMED'} tes Python legacy lulus dalam {match[2]if match else'—'} s. M10 core31 assertions dan baseline18browser flows lulus terpisah. M11 menambah timed rehearsals, enam projector cases, fault/fallback dan pemeriksaan dokumen/numeric/source. Count ini tidak digabung menjadi jumlah Python test fiktif.

Frame pacing aktual A/B: {json.dumps(perf,ensure_ascii=False)}. Window saling tumpang tindih dan dapat mencakup transisi/loading serta aktivitas authoring lain. Jangan menjumlahkan stalls atau menafsirkan shared GPU memory sebagai kapasitas VRAM. Benchmark M10 tetap bukti historis terpisah, tidak ditulis ulang sebagai hasil M11.

## Issues found and fixed

- Canvas terlalu kecil pada1366×768 zoom150%: CSS adapter M11, rerun enam kasus PASS.
- Selector link entry offline tidak valid: ganti ke ID eksplisit, fallback QA rerun PASS.
- Wording recovery menampilkan path teknis: adapter pesan presenter, detail terpisah dari tampilan utama.
- Font API awal mengabaikan family: gunakan typeface Arial, verifikasi final148text-script uses. Chart memakai style font sendiri.
- Kesalahan konfigurasi finalizer/table policy/runtime modules/receipt path diperbaiki, lalu final artifact berhasil divalidasi. Tidak dianggap kegagalan simulator.
- Uji C awal memiliki syntax harness error, kemudian jalur auto-C mengalami race dengan halaman chrome-error setelah service mati. Harness dibetulkan dengan tab baru sesudah refused navigation. Uji C lengkap terpisah (console, failure, actual video, restart) lulus; log awal tetap dipertahankan.

## Remaining limitations dan M12

{limitations}

M11 siap sebagai paket teknis menurut 20 gate yang tercatat. Penerimaan lapangan/proyektor tetap pending secara terpisah. Kesiapan ini bukan izin otomatis memulai M12 atau klaim release produksi/efektivitas kebijakan.
'''
 # Keep ordinary Indonesian prose readable.
 for oldtext,newtext in [('requested240','requested 240'),('routable/departed206','routable/departed 206'),('arrived183','arrived 183'),('running23','running 23'),('failed34','failed 34'),('not departed0','not departed 0'),('not arrived57','not arrived 57'),('arrived356','arrived 356'),('requested500','requested 500'),('arrived328','arrived 328'),('Running80/102','Running 80/102'),('departed8/14','departed 8/14'),('routes56/56','routes 56/56'),('arrived144/172','arrived 144/172'),('requested240/269/311/360','requested 240/269/311/360'),('mobil3,5','mobil 3,5'),('umum2,5','umum 2,5'),('northbound4','northbound 4'),('dan1366','dan 1366'),('zoom100','zoom 100'),('request0','request 0'),('mengembalikan404','mengembalikan 404'),('HTML15slide','HTML 15 slide'),('ulang23recordings','ulang 23 recordings'),('core31','core 31'),('baseline18browser','baseline 18 browser'),('pada1366','pada 1366'),('zoom150','zoom 150'),('final148text-script','final 148 text-script')]:report=report.replace(oldtext,newtext)
 (OUT/'MILESTONE_11_REPORT.md').write_text(report,encoding='utf-8')
 (OUT/'M11_PRESENTATION_QA.md').write_text(f'''# QA presentasi M11

**{status.replace('_',' ')}**. Hanya viewport simulasi dan browser terpasang yang diuji.

| Pengujian | Hasil / bukti |
|---|---|
| Python M01–M10 | 344 PASS, documentation/m11/baseline-regression.txt |
| M10 baseline controls | 18 PASS, qa/baseline/browser-qa.json |
| M10 core | 31 assertions, documentation/m11/baseline-m10-core.txt |
| Source preservation | {old} hashes unchanged |
| Rehearsal A | {a['duration_s']:.2f}s, qa/REHEARSAL_A.json |
| Rehearsal B | {b['duration_s']:.2f}s, qa/REHEARSAL_B.json |
| Interruption / recovery | qa/REHEARSAL_C_FINAL.json, actual before/after video |
| Projector viewports / native zoom | six cases PASS, qa/projector-qa.json |
| Fault / offline fallback | PASS, qa/fallback-qa.json; injected404 classified as deliberate |
| PPTX | 15slides, two editable tables, one editable chart with workbook snapshot, final import/render PASS |
| PDF / handout | 15pages / 2pages, Poppler renders visually inspected |
| Video | 106.4s,1920×1080, copied byte-identical and browser-played |
| Visual review | qa/visual-review.json, M11_SLIDE_CONTACT_SHEET.png |

No simulated physical projector, human speech, official traffic prediction or field effectiveness is claimed. No M01–M10 output was overwritten. Browser-independent fallback HTML/PDF/video remains available without local server. Actual default BAT cold-start/reuse and isolated shutdown/restart were exercised. Details and initial failures/fixes are in MILESTONE_11_REPORT.md.
''',encoding='utf-8')
 for name in ['MILESTONE_11_REPORT.md','M11_PRESENTATION_QA.md','M11_TECHNICAL_PRESENTATION_ACCEPTANCE.md','M11_FIELD_MEETING_CHECKLIST.md']:shutil.copy2(OUT/name,DOC/name)
 files=[]
 for folder in [OUT/'assets',OUT/'slides',QA,ROOT/'tests/m11']:
  files += [p for p in folder.rglob('*')if p.is_file()and '__pycache__'not in str(p)and not p.name.endswith('.progress.json')and p.suffix!='.webm'and p.name not in ['runtime.log','launch-latest.json','launch-error.txt']]
 files += [p for p in OUT.glob('*')if p.is_file()and p.suffix in['.md','.json','.html','.pdf','.pptx','.mp4','.png','.bat']and p.name not in['M11_DELIVERY_MANIFEST.json','package-manifest.json']]
 files+=list((ROOT/'backend/gedangan').glob('m11_*.py'))+[ROOT/'START_PRESENTASI_TEKNIS_GEDANGAN.bat',OUT/'build/deck.mjs',OUT/'build/render-final.mjs']
 manifest={'status':status,'date_local':'2026-11-01','human_acceptance':'HUMAN FIELD / PROJECTOR ACCEPTANCE PENDING','slide_count':15,'M12_started':False,'old_files_verified':old,'shared_runtime':'Unchanged M10 build/renderer/cache. M11 response adapter only adds presenter CSS and readable recovery wording.','mutable_runtime_files_excluded':['readiness.js','qa/runtime.log','qa/launch-latest.json','qa/launch-error.txt','runtime/'],'shared_recording_manifest_sha256':sha(ROOT/'presentation_demo/m09/M09_DEMO_MANIFEST.json'),'files':{p.relative_to(ROOT).as_posix():sha(p)for p in sorted(set(files))}}
 write(OUT/'M11_DELIVERY_MANIFEST.json',manifest);write(DOC/'M11_DELIVERY_MANIFEST.json',manifest);print(json.dumps({'status':status,'criteria_passed':sum(v for _,v in gates),'slides':15,'old_files':old,'rehearsal_seconds':[a['duration_s'],b['duration_s'],c.get('duration_s')]}),flush=True)
if __name__=='__main__':main()
