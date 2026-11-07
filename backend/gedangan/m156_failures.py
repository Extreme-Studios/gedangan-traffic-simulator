"""Read-only explanation of rejected cohort routes, without rerouting/substitution."""
from functools import lru_cache
from collections import Counter
from .m156_common import *
from .m155_network import catalog
from .m14_vehicles import registry
from .recovery_routing import graph
@lru_cache(maxsize=240)
def explain(typ,approach,turn):
 v=next(v for v in registry()if v['id']==typ);a=next(a for a in catalog()['approaches']if a['id']==approach);movement=a['movements'].get(turn)
 if not movement or not movement['available']:return {'reason':'MOVEMENT_NOT_VERIFIED_IN_SELECTED_CATALOG','message':'Gerakan ini belum tersedia pada katalog koneksi yang diaudit. Tidak dibuat belokan atau tujuan pengganti.','blocked_candidates':[]}
 if v['sumo_vclass']=='bicycle':return {'reason':'NO_BICYCLE_LANE_PERMISSION','message':'Lane baseline belum mengizinkan sepeda/becak nonmotor. Tipe kendaraan dipertahankan sebagai permintaan gagal.','blocked_candidates':[]}
 adj,legal,reasons=graph(str(NETWORK.resolve()),sha(NETWORK),v['source_type_id']);evidence=[]
 for c in movement['candidates']:
  ids=c['prefix']+c['suffix'];bad=[{'edge':eid,'reason':reasons.get(eid,'NOT_IN_ELIGIBLE_GRAPH')}for eid in ids if eid not in legal]
  if not bad:bad=[{'from':a,'to':b,'reason':'NO_PERMITTED_LANE_CONNECTION'}for a,b in zip(ids,ids[1:])if b not in adj.get(a,{})]
  evidence.append({'destination':c['destination_edge'],'rejections':bad[:8],'note':'First8 failing edges; remaining route retained in candidate catalog'})
 return {'reason':'ACCESS_DIMENSION_CONNECTION_SCREEN','message':'Rute ditolak oleh pemeriksaan izin kelas, fungsi jalan, ukuran atau koneksi. Lihat edge penyebab; ini bukan izin legal lapangan.','blocked_candidates':evidence}
def summarize(demand):
 grouped=Counter((q['vehicle_type_id'],q['approach'],q['turn'])for q in demand['requests']if not q['edges']);return [{'class':typ,'approach':a,'turn':turn,'count':n,**explain(typ,a,turn)}for (typ,a,turn),n in grouped.items()]
