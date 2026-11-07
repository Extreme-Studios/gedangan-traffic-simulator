"""Class-permitted component diagnostics for existing operational topology only."""
import xml.etree.ElementTree as E
from .m04_demand import ROOT,load,save,sha
from .m08_reporting import DOC,results
CLASSES=['motorcycle','passenger','delivery','bus','truck','trailer']
def permits(element,cls):
 allow=element.get('allow');deny=element.get('disallow','').split()
 return (allow is None or cls in allow.split()) and cls not in deny and 'all' not in deny
def components(adjacency):
 nodes=set(adjacency);reverse={v:set() for v in nodes}
 for a,bs in adjacency.items():
  for b in bs:reverse[b].add(a)
 seen=set();order=[]
 for start in sorted(nodes):
  if start in seen:continue
  seen.add(start);stack=[(start,iter(adjacency[start]))]
  while stack:
   a,children=stack[-1];b=next(children,None)
   if b is None:order.append(a);stack.pop()
   elif b not in seen:seen.add(b);stack.append((b,iter(adjacency[b])))
 def groups(starts,graph):
  visited=set();sizes=[]
  for a in starts:
   if a in visited:continue
   visited.add(a);stack=[a];size=0
   while stack:
    v=stack.pop();size+=1
    for b in graph[v]:
     if b not in visited:visited.add(b);stack.append(b)
   sizes.append(size)
  return sorted(sizes,reverse=True)
 strong=groups(reversed(order),reverse);weak=groups(sorted(nodes),{a:adjacency[a]|reverse[a] for a in nodes})
 return {'permitted_road_edges':len(nodes),'permitted_movements':sum(map(len,adjacency.values())),'weak_components':len(weak),'strong_components':len(strong),'largest_weak_component_edges':weak[0] if weak else 0,'largest_strong_component_edges':strong[0] if strong else 0}
def graph(path,cls):
 root=E.parse(path).getroot();lanes={l.get('id'):l for e in root.findall('edge') for l in e.findall('lane')};edges={e.get('id'):e for e in root.findall('edge') if e.get('function')!='internal' and not e.get('id').startswith('m05_rail_') and any(permits(l,cls) for l in e.findall('lane'))};adj={eid:set() for eid in edges}
 for c in root.findall('connection'):
  a,b=c.get('from'),c.get('to')
  if a not in edges or b not in edges:continue
  fromlane=lanes[a+'_'+c.get('fromLane')];tolane=lanes[b+'_'+c.get('toLane')];via=lanes.get(c.get('via'))
  if permits(c,cls) and permits(fromlane,cls) and permits(tolane,cls) and (via is None or permits(via,cls)):adj[a].add(b)
 return components(adj)
def main():
 unique={r['network_sha256']:r for r in results()};values=[];memo={}
 for r in unique.values():
  manifest=r['intervention_manifest'];before=ROOT/manifest['parent_network'];after=ROOT/r['network_path'];row={'scenario':r['solution_id'],'family':r['network_variant'],'network_sha256':sha(after),'parent_sha256':sha(before),'scope':'External road-edge graph using lane/via/connection vClass permissions; graph reachability is not physical vehicle eligibility. Actual OD routing still applies M045 width/trailer/conditional/type screens.','classes':{}}
  for cls in CLASSES:
   def metrics(path):
    key=(sha(path),cls)
    if key not in memo:memo[key]=graph(path,cls)
    return memo[key]
   a,b=metrics(before),metrics(after);row['classes'][cls]={'before':a,'after':b,'delta':{k:b[k]-a[k] for k in a}}
  values.append(row)
 save(DOC/'topology-audits.json',values);print('Permission-graph component audits:',len(values),'unique networks',flush=True)
if __name__=='__main__':main()
