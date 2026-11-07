"""Record the actual browser review without promoting appearance to location truth."""
from .m1561_common import *
import subprocess

def main():
 protect()
 evidence=DOC/'evidence'
 names=['overview','intersection','railway-crossing','frontage-relationship','presentation']
 def probe(path):
  return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=width,height','-show_entries','format=duration,size','-of','json',str(path)],text=True))
 images=[]
 for name in names:
  path=evidence/(name+'.jpg'); metadata=probe(path)
  assert metadata['streams'][0]=={'width':1920,'height':1080},metadata
  images.append({'path':path.relative_to(ROOT).as_posix(),'sha256':sha(path),'width':1920,'height':1080})
 video=evidence/'actual-playback.webm'; metadata=probe(video)
 assert 45<=float(metadata['format']['duration'])<=60
 assert metadata['streams'][0]=={'width':1920,'height':1080}
 status={'reviewed_utc':now(),'status':'BROWSER_QA_COMPLETE_REQUIRES_VISUAL_REWORK','browser':'Internal browser; actual local page http://127.0.0.1:5203/','screenshots':images,'video':{'path':video.relative_to(ROOT).as_posix(),'sha256':sha(video),'probe':metadata},'old_evidence_reused':False,'console_errors_warnings':[],'render_review':'No metropolitan skyline. Low-rise roof, shutter, station context and actual traffic visible. Buildings remain repetitive, sparse and generic; ground and roads retain a toy-like model appearance. Not presentation-grade real-location reconstruction.','performance':'Brief UI FPS observations only; no sustained benchmark or heap acceptance. Parent memory limitation remains unresolved.','network_sha256':sha(NETWORK),'traffic_source':'M15.5 baseline-3000 actual stored SUMO output; no new SUMO experiment','frame_review':['video-frame-01.jpg','video-frame-30.jpg','video-frame-48.jpg']}
 save(DOC/'visual-status.json',status)
 section='''
## Pemeriksaan browser aktual — 2 November 2026

Browser internal berhasil diakses setelah restart dan server port 5203 dihidupkan kembali. Lima screenshot aktual 1920×1080 tersedia pada `documentation/m1561/evidence`: overview.jpg, intersection.jpg, railway-crossing.jpg, frontage-relationship.jpg, dan presentation.jpg. Tangkapan memakai clip viewport eksplisit; hasil awal screenshot default terpotong sehingga diganti dengan tangkapan penuh, tanpa resize atau gambar buatan.

Video `actual-playback.webm` berasal dari recorder live canvas, 1920×1080, durasi **49.942472 detik**, ukuran 12,795,630 byte. Metadata diperiksa dengan ffprobe; frame detik 1, 30, dan 48 dirender dan diperiksa. Timestamp maju dari sekitar 1796 ke 1846 detik. Kamera overview/presentation beralih ke intersection selama perekaman. Video merekam canvas kendaraan/lingkungan beserta watermark; seluruh dashboard dan peta kecil ditunjukkan dalam screenshot, bukan disertakan sebagai DOM dalam video. Log warning/error browser yang dikembalikan saat pemeriksaan kosong.

Rekaman memakai hasil tersimpan M15.5 baseline-3000: 3000 diminta, 1914 berangkat/bergerak, 1346 tiba, 568 aktif akhir, 1086 belum berangkat. Ini playback aktual skenario random, bukan observasi lalu lintas Gedangan dan bukan pengujian SUMO baru. Kereta terlihat pada screenshot railway-crossing t=1796 detik; kendaraan dan antrean mengikuti rekaman.

**Keputusan visual: REQUIRES VISUAL REWORK.** Arah metropolitan sudah tidak terlihat. Ruko, rumah beratap genteng, workshop dan konteks stasiun rendah lebih sesuai konteks Indonesia. Namun bangunan masih berulang dan generik, jarak antarbangunan renggang, tanah relatif kosong, material dan detail tepi jalan sederhana. Jalan dan lingkungan masih terasa model/mainan. Kamera frontage memperlihatkan hubungan geografis, tetapi pada jarak itu bangunan dan kendaraan terlalu kecil untuk menilai detail. Identitas Gedangan terutama berasal dari jaringan jalan/rel dan anchor stasiun; bentuk lingkungan belum merupakan rekonstruksi lokasi yang dapat diverifikasi.

Target arah low-rise terpenuhi; target kualitas lingkungan realistis untuk presentasi belum lulus. Jangan menyebut hasil ini photorealistic, final release, atau real-location model tervalidasi. Prioritas perbaikan berikutnya dalam M15.6.1 adalah referensi footprint/facade koridor yang dapat diverifikasi, kontinuitas lingkungan tepi jalan, variasi aset, material tanah/tepi jalan dan framing frontage yang lebih terbaca, tanpa mengubah network atau traffic model.

Sepuluh tes konteks dijalankan ulang dan lulus. FPS UI singkat selama perekaman sekitar 59–72 dan setelah pause sekitar 106–120; ini bukan benchmark berkelanjutan atau bukti memory target lulus. Tidak ada klaim masalah heap M15.6 telah diperbaiki. Hash dan metadata bukti ada di `documentation/m1561/visual-status.json`.
'''
 for name in ['M15_6_1_GEDANGAN_ENVIRONMENT_REPORT.md','M15_6_1_LOCATION_CONTEXT_REVIEW.md']:
  path=ROOT/name; content=path.read_text(encoding='utf-8')
  if '\n## Pemeriksaan browser aktual' in content: content=content.split('\n## Pemeriksaan browser aktual')[0]
  # Supersede old blocker text rather than retaining a contradictory acceptance claim.
  content=content.replace('Arah visual baru sudah diimplementasikan. **Visual acceptance masih PENDING karena Browser Use ditolak oleh Work settings.** Lima screenshot 1920×1080 dan video aktual 45–60 detik belum tersedia. Build atau pemeriksaan source tidak dipakai sebagai pengganti inspeksi browser. Bukti M15.6 tidak diberi label ulang sebagai M15.6.1.','Arah visual baru sudah diimplementasikan dan diperiksa dalam browser. Lima screenshot 1920×1080 dan video aktual 49.94 detik tersedia. **Visual acceptance: REQUIRES VISUAL REWORK**, dengan alasan dan bukti pada pemeriksaan browser aktual di bawah.')
  content=content.replace('**Recorder belum dijalankan pada M15.6.1 karena browser diblokir.** Tombol siap tidak berarti video telah tersedia. FPS/heap M15.6.1 belum diukur; masalah memori M15.6 belum dinyatakan selesai.','Recorder telah dijalankan; video aktual dan metadata tersedia. Hanya FPS UI singkat yang diamati; masalah memori M15.6 belum dinyatakan selesai.')
  content=content.replace('## Pekerjaan yang tertahan','## Rencana pemeriksaan awal (sudah dilaksanakan; hasil di bawah)')
  content=content.replace('**Implementasi selesai pada source/build; review visual belum selesai.** Browser Use ditolak oleh Work settings. Lima screenshot baru dan video aktual 45–60 detik belum tersedia. Status kualitas lokasi tetap **PENDING**, bukan PASS.','**Review browser selesai.** Lima screenshot baru dan video aktual 49.94 detik tersedia. Kualitas lokasi **REQUIRES VISUAL REWORK**, bukan PASS. Tabel berikut adalah checkpoint source awal; penilaian aktual menggantikannya pada bagian akhir.')
  content=content.replace('Belum dinilai di browser','Tidak terlihat skyline/CBD dalam browser')
  content=content.replace('Menunggu overview, crossing, dan frontage inspection','Terlihat konteks low-rise dan rail; identitas bangunan masih generik')
  content=content.replace('Menunggu live close-up; tidak ada klaim photorealism','Close-up masih terasa model/mainan; tidak photorealistic')
  content=content.replace('Menunggu video aktual dan review pengguna','Lebih sesuai arah low-rise; belum presentation-grade')
  content=content.replace('Daftar lima screenshot dan video yang belum dikerjakan tersedia pada `visual-status.json`.','Daftar lima screenshot dan metadata video aktual tersedia pada `visual-status.json`.')
  content=content.replace('**Visual/location acceptance belum lulus.** Jika setelah browser QA lingkungan masih metropolitan, terlalu generik, atau seperti mainan, status tetap PENDING/REQUIRES REWORK.','**Visual/location acceptance belum lulus: REQUIRES VISUAL REWORK** karena terlalu generik dan seperti model/mainan, meskipun arah metropolitan sudah dihindari.')
  path.write_text(content+section,encoding='utf-8')
 build=load(DOC/'build-verification.json');build.update(actual_browser='REVIEWED',actual_video='VERIFIED_49.942472_SECONDS_1920x1080',screenshots='FIVE_VERIFIED_1920x1080',visual_acceptance='REQUIRES_VISUAL_REWORK');save(DOC/'build-verification.json',build)
 print(json.dumps({'status':status['status'],'screenshots':len(images),'duration':metadata['format']['duration']}))

if __name__=='__main__':main()
