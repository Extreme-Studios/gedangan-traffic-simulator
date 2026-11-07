"""Presentation PDF from final slide renders, plus printable field discussion handout."""
from pathlib import Path
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import ParagraphStyle
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'presentation_demo/m11'

def main():
 pdfmetrics.registerFont(TTFont('ArialM11','C:/Windows/Fonts/arial.ttf'))
 pdfmetrics.registerFont(TTFont('ArialM11B','C:/Windows/Fonts/arialbd.ttf'))
 # Static printable counterpart of the verified final PPTX render; PPTX retains editable text/chart/tables.
 target=OUT/'M11_PRESENTASI_TEKNIS_GEDANGAN.pdf';c=canvas.Canvas(str(target),pagesize=(960,540));c.setTitle('Presentasi Teknis Gedangan');c.setAuthor('EXTREME STUDIOS')
 for i in range(1,16):
  image=OUT/f'slides/slide-{i:02d}.png'
  if not image.is_file():raise ValueError('Slide render missing: '+str(i))
  c.drawImage(str(image),0,0,width=960,height=540);c.showPage()
 c.save()
 plan=json.loads((OUT/'M11_NUMERIC_DATA_AUDIT.json').read_text())['survey_plan'];style=ParagraphStyle('body',fontName='ArialM11',fontSize=9,leading=13,textColor=HexColor('#193440'));title=ParagraphStyle('title',parent=style,fontName='ArialM11B',fontSize=20,leading=25,spaceAfter=15);head=ParagraphStyle('heading',parent=style,fontName='ArialM11B',fontSize=12,leading=17,spaceAfter=9)
 def P(s):return Paragraph(s,style)
 story=[Paragraph('Lembar diskusi lapangan Gedangan',title),P('EXTREME STUDIOS. Simulasi ilustratif, baseline 2026 belum dikalibrasi. Seluruh keputusan tetap kosong sampai peserta menyepakatinya.'),Spacer(1,12),P('Tanggal/pertemuan: _______________________ &nbsp; Pencatat: _______________________'),Spacer(1,10),P('Peserta/instansi: __________________________________________________________'),Spacer(1,18),Paragraph('Calon titik observasi M06/M08.5',head)]
 values=[[P('Titik model'),P('Arah model'),P('Status / keputusan lapangan')]]+[[P(r['location_id']),P({'northbound':'Ke utara (model)','southbound':'Ke selatan (model)','eastbound':'Ke timur (model)','westbound':'Ke barat (model)','source_direction':'Perlu verifikasi'}.get(r['direction'],r['direction'])),P('BELUM DISETUJUI<br/>____________________________')] for r in plan]
 t=Table(values,colWidths=[165,115,235],rowHeights=[28]+[45]*7);t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#dfe8df')),('GRID',(0,0),(-1,-1),.4,HexColor('#a7b5ae')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7)]));story+=[t,Spacer(1,14),P('Geometri edge sumber bukan posisi kamera yang sudah diizinkan. Reconnaissance harus menilai coverage, akses aman, occlusion dan izin. Tidak ada jam puncak lapangan yang diklaim.'),Spacer(1,12),P('Peninjau lokasi/metode: _____________________ &nbsp; Tanggal tinjau: _______________'),PageBreak(),Paragraph('Keputusan metode dan penanggung jawab',title)]
 topics=['Ruas, arah dan gerakan prioritas','Reconnaissance, izin dan posisi aman','Hari/jam, cuaca, event khusus','Count per kelas/arah dan turning','OD dan endpoint travel time','Signal head, fase, cycle, offset','Warning/tutup/lewat/clearance/buka kereta','Antrean meter, count, referensi dan batas pandang','Hambatan samping, insiden dan geometri','Jam acuan, provenance, QC dan coverage','PIC, penyimpanan, akses dan retensi data','Kalibrasi/holdout terpisah dan kelengkapan']
 values=[[P('Topik'),P('Keputusan / koreksi'),P('PIC / tenggat')]]+[[P(v),P('_______________________<br/>_______________________'),P('_________________<br/>_________________')]for v in topics]
 t=Table(values,colWidths=[195,185,135],rowHeights=[28]+[38]*len(topics));t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#dfe8df')),('GRID',(0,0),(-1,-1),.4,HexColor('#a7b5ae')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6)]));story+=[t,Spacer(1,15),P('Missing bukan nol. Partial count bukan volume interval lengkap. Count antrean bukan meter. Catat censoring, perbedaan pengamat dan koreksi. M08.5 masih PARTIAL_BROWSER_ACCEPTANCE_PENDING, belum disahkan untuk survei produksi.'),Spacer(1,12),P('Persetujuan / catatan peninjau: ______________________________________________')]
 def footer(c,doc):
  c.setFont('ArialM11',8);c.setFillColor(HexColor('#587169'));c.drawString(40,24,'Calon lokasi dan metode perlu persetujuan. Tidak ada keputusan infrastruktur otomatis.');c.drawRightString(A4[0]-40,24,str(doc.page))
 doc=SimpleDocTemplate(str(OUT/'M11_LEMBAR_DISKUSI_LAPANGAN.pdf'),pagesize=A4,leftMargin=40,rightMargin=40,topMargin=38,bottomMargin=42);doc.build(story,onFirstPage=footer,onLaterPages=footer)
 from pypdf import PdfReader
 result={'presentation_pages':len(PdfReader(target).pages),'handout_pages':len(PdfReader(OUT/'M11_LEMBAR_DISKUSI_LAPANGAN.pdf').pages),'presentation_pdf':'Rasterized final slide render, 1920x1080 source, static offline PDF; editable source is PPTX','handout':'Printable decision fields, unfilled; no approval fabricated'}
 (OUT/'qa/pdf-structure.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(result)
if __name__=='__main__':main()

