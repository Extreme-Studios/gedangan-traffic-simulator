from .m1562_common import *
from datetime import datetime,timedelta
from statistics import median

def main():
 protocol=load(DOC/'benchmark-protocol.json');output=[]
 for label,key,demand,folder in [('baseline_3000','baseline_3000_start',3000,'baseline/browser-performance'),('baseline_5000','baseline_5000_start',5000,'baseline/browser-performance'),('corrected_3000','corrected_3000_start',3000,'browser-performance'),('corrected_5000','corrected_5000_start',5000,'browser-performance')]:
  if key not in protocol:continue
  start=datetime.fromisoformat(protocol[key].replace('Z','+00:00'));rows=[];all_rows=[]
  for path in(DOC/folder).glob('*.json'):
   r=load(path);when=datetime.fromisoformat(r['recorded_utc'].replace('Z','+00:00'))
   if r.get('kind')=='render_sample'and start<=when<=start+timedelta(seconds=45)and r.get('window')==[1920,1080]and r.get('playing')and r.get('camera')=='junction':
    all_rows.append((path,r))
    if when>=start+timedelta(seconds=5):rows.append((path,r))
  if not rows:output.append({'label':label,'status':'MISSING_VALID_WINDOW'});continue
  heap=max(r['js_heap']['used']for _,r in all_rows);typed=(165197520 if demand==3000 else 218425392)if label.startswith('corrected')else 0
  output.append({'label':label,'demand':demand,'status':'MEASURED','start_utc':protocol[key],'analysis_interval_s':[5,45],'samples':len(rows),'median_window_fps':median(r['fps_median']for _,r in rows),'worst_window_p5_fps':min(r['fps_p5']for _,r in rows),'max_stalls_over50ms_per120frames':max(r['stalls_over_50ms']for _,r in rows),'heap_max_mib':heap/1048576,'typed_buffers_mib':typed/1048576,'conservative_heap_plus_typed_mib':(heap+typed)/1048576,'active_range':[min(r['visible_vehicles']for _,r in rows),max(r['visible_vehicles']for _,r in rows)],'gpu_geometry_count_max':max(r['geometries']for _,r in rows),'gpu_texture_count_max':max(r['textures']for _,r in rows),'draw_calls_max':max(r['draw_calls']for _,r in rows),'triangle_count_max':max(r['triangles']for _,r in rows),'raw_files':[p.relative_to(ROOT).as_posix()for p,_ in all_rows]})
 save(DOC/'benchmark-summary.json',{'protocol':protocol,'measurements':output,'interpretation':'performance.memory is a browser metric, not total process RAM or VRAM. Typed bytes are shown separately and conservatively added even though accounting may overlap. No frame records discarded. One bounded interval per case; no long-term leak-free certification.'});print(json.dumps(output,ensure_ascii=True))
if __name__=='__main__':main()
