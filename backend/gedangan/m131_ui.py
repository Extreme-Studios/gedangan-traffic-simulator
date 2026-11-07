"""Add multi-year evidence controls in a new frontend; M13 sources stay unchanged."""
import shutil
from .m13_common import ROOT
def build():
 src=ROOT/'frontend/m13';dst=ROOT/'frontend/m13_1';dst.mkdir(exist_ok=True)
 for name in ['index.html','style.css','app.js']:shutil.copy2(src/name,dst/name)
 p=dst/'index.html';s=p.read_text(encoding='utf-8').replace('Gedangan M13 —','Gedangan M13.1 —').replace('GEDANGAN · MILESTONE 13','GEDANGAN · MILESTONE 13.1').replace('1 Agustus – 31 Oktober 2026 · Asia/Jakarta (WIB)','Arsip lintas tahun · Asia/Jakarta (WIB) · Bukti publik dan observasi terverifikasi')
 s=s.replace('<div id="months" class="months"></div>','<div class="fields"><label>Bulan dan tahun<input id="month-picker" type="month" min="1900-01" max="2100-12" value="2026-08"></label><button id="show-month">Tampilkan bulan</button></div><p id="archive-summary"></p><div id="months" class="months"></div>')
 s=s.replace('<details><summary>Impor dan verifikasi data baru</summary>','<details><summary>Arsip kategori C — agregat, bukan observasi per jam</summary><p>Hitungan12jam dan smp/jam dipertahankan pada interval/satuan aslinya. Tidak dibagi menjadi jam, arah, atau kelas lain dan tidak mengaktifkan kalender historis.</p><button id="aggregate-load">Lihat agregat asli yang diperiksa</button><pre id="aggregate-result"></pre></details><details><summary>Impor dan verifikasi data baru</summary>')
 s=s.replace('<label>Jenis sumber<select id="source-type">','<label>Kualitas sumber<select id="quality"><option>A</option><option>B</option><option>C</option><option>D</option><option>E</option></select></label><label>Jenis sumber<select id="source-type">');p.write_text(s,encoding='utf-8')
 p=dst/'app.js';s=p.read_text(encoding='utf-8').replace("const months=['2026-08','2026-09','2026-10'];","let months=['2026-08'];").replace('const source={source_type:',"const source={quality_class:$('#quality').value,source_type:")
 s+='''
$('#show-month').onclick=()=>{const value=$('#month-picker').value;if(!/^\\d{4}-\\d{2}$/.test(value))return fail(Error('Pilih bulan/tahun'));months=[value];selectedDate=null;selectedHour=null;$('#hours').textContent='';$('#day-summary').textContent='Pilih tanggal pada bulan ini; tanggal tidak diganti otomatis.';$('#use-hour').disabled=true;refresh().catch(fail)};
$('#aggregate-load').onclick=async()=>{try{const r=await api('references');$('#aggregate-result').textContent=JSON.stringify(r,null,2)}catch(e){fail(e)}};
api('archive').then(r=>{$('#archive-summary').textContent='Bulan observasi A/B terverifikasi: '+(r.verified_observation_months.join(', ')||'belum ada')+'. Bulan dalam arsip agregat kategori C: '+(r.reference_aggregate_months.join(', ')||'belum ada')+'. Agregat tidak mengaktifkan pilihan jam historis.'}).catch(fail);
''';p.write_text(s.replace('Bulan dalam arsip agregat kategori C','Bulan arsip B tertahan / C agregat'),encoding='utf-8')
 p=dst/'index.html';s=p.read_text(encoding='utf-8').replace('Arsip kategori C — agregat, bukan observasi per jam','Arsip B tertahan / C referensi — bukan observasi per jam').replace('Hitungan12jam dan smp/jam dipertahankan','Observasi parsialB dengan interval12jam masihquarantine. Hitungan12jam dan smp/jam dipertahankan');p.write_text(s,encoding='utf-8')
if __name__=='__main__':build()
