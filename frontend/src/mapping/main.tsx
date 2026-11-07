import React,{useEffect,useRef,useState} from 'react';
import {createRoot} from 'react-dom/client';
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import './mapping.css';

type Geometry={type:string;coordinates:any};
type Feature={id:string;geometry:Geometry;properties:Record<string,any>};
type Bundle={type:string;crs:string;origin_utm_m:number[];station_lonlat:number[];layers:Record<string,Feature[]>;source:Record<string,any>;qa:Record<string,any>;selection:Record<string,any>};
const layers=[
 ['main_arterial_road','Jalan utama','#f5a35c'],['frontage_road','Frontage road','#57dfb4'],['feeder_road','Jalan pengumpan','#7fa9ed'],['collector_road','Jalan kolektor','#668da3'],['local_access_road','Akses lokal','#405f71'],['service_road','Jalan servis','#38515e'],['connector_road','Penghubung','#c0b1df'],['railways','Jalur rel','#f3d182'],['stations','Stasiun','#ffffff'],['crossings','Perlintasan','#ed8097'],['junctions','Persimpangan','#94b6c5'],['access_points','Akses / merge kandidat','#9b9bef'],['traffic_signals','Sinyal OSM','#aece9d'],['barriers','Hambatan OSM','#bb7e7e'],['boundaries','Batas studi','#658778']
];
const colorFor=(id:string)=>layers.find(l=>l[0]===id)?.[2]||'#ffffff';
const defaults=Object.fromEntries(layers.map(([id])=>[id,!['service_road','access_points','traffic_signals','barriers','junctions'].includes(id)]));

function MapCanvas({bundle,visible,selected,onSelect,view,onReady,onError}:{bundle:Bundle;visible:Record<string,boolean>;selected:Feature|null;onSelect:(f:Feature)=>void;view:{area:'core'|'context';reset:number};onReady:(s:string)=>void;onError:(s:string)=>void}){
 const host=useRef<HTMLDivElement>(null);const world=useRef<{groups:Record<string,THREE.Group>;render:()=>void;highlight:(f:Feature|null)=>void;fit:(area:string)=>void}|null>(null);
 const selectedRef=useRef(selected);selectedRef.current=selected;
 const visibleRef=useRef(visible);visibleRef.current=visible;
 useEffect(()=>{
  const el=host.current!;let renderer:THREE.WebGLRenderer;
  try{renderer=new THREE.WebGLRenderer({antialias:true,powerPreference:'low-power'});}catch(e){onError('WebGL tidak tersedia: '+String(e));return;}
  renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));renderer.setClearColor('#101e29');renderer.domElement.setAttribute('aria-label','Peta geografis Gedangan Three.js; klik ruas untuk atribut');el.appendChild(renderer.domElement);
  const scene=new THREE.Scene();const camera=new THREE.OrthographicCamera(-1000,1000,1000,-1000,.1,30000);
  const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=false;controls.minZoom=.15;controls.maxZoom=80;controls.maxPolarAngle=Math.PI/2.15;controls.screenSpacePanning=true;
  const [ox,oy]=bundle.origin_utm_m;const groups:Record<string,THREE.Group>={};const selectable:THREE.Object3D[]=[];const ray=new THREE.Raycaster();const mouse=new THREE.Vector2();let highlightObject:THREE.Object3D|null=null;let moved=false;let startX=0,startY=0;let currentArea='core';
  const position=(p:number[],height=2)=>new THREE.Vector3(p[0]-ox,height,-(p[1]-oy));
  const render=()=>{if(!el.clientWidth||!el.clientHeight)return;renderer.render(scene,camera);
    const origin=new THREE.Vector3(0,0,0).project(camera),north=new THREE.Vector3(0,0,-100).project(camera);
    const compass=el.parentElement?.querySelector<HTMLElement>('.north');if(compass)compass.style.transform=`rotate(${Math.atan2((north.x-origin.x)*el.clientWidth,(north.y-origin.y)*el.clientHeight)*180/Math.PI}deg)`;
    el.querySelectorAll<HTMLElement>('[data-map-label]').forEach(label=>{const id=label.dataset.mapLabel!;const feature=labelFeatures.find(f=>f.feature.id===id);if(!feature)return;const projected=position(feature.coordinate).project(camera);const x=(projected.x+1)/2*el.clientWidth,y=(-projected.y+1)/2*el.clientHeight;label.style.left=`${x+feature.offset[0]}px`;label.style.top=`${y+feature.offset[1]}px`;label.style.display=x<10||x>el.clientWidth-10||y<40||y>el.clientHeight-60||!visibleRef.current[feature.layer]?'none':'block';});
  };
  const makeLines=(geometry:Geometry,material:THREE.LineBasicMaterial,height:number,parent:THREE.Group,feature:Feature,pick:boolean)=>{
    let paths:number[][][]=[];
    if(geometry.type==='LineString')paths=[geometry.coordinates];
    else if(geometry.type==='MultiLineString')paths=geometry.coordinates;
    else if(geometry.type==='Polygon')paths=geometry.coordinates;
    else if(geometry.type==='MultiPolygon')paths=geometry.coordinates.flat();
    paths.forEach(coords=>{const line=new THREE.Line(new THREE.BufferGeometry().setFromPoints(coords.map(p=>position(p,height))),material);line.userData.feature=feature;parent.add(line);if(pick)selectable.push(line);});
  };
  for(const [id,features] of Object.entries(bundle.layers)){
    const group=new THREE.Group();group.visible=visibleRef.current[id]??false;groups[id]=group;scene.add(group);
    const isRoad=id.endsWith('_road');const material=new THREE.LineBasicMaterial({color:colorFor(id),transparent:true,opacity:id==='boundaries'?.34:['local_access_road','service_road'].includes(id)?.65:1});
    const height=id==='boundaries'?0:id==='railways'?6:isRoad?3:8;
    for(const feature of features){
      if(feature.geometry.type==='Point'){
        const geom=new THREE.BufferGeometry().setFromPoints([position(feature.geometry.coordinates,height)]);
        const dot=new THREE.Points(geom,new THREE.PointsMaterial({color:colorFor(id),size:id==='stations'?13:id==='crossings'?7:id==='junctions'?3:4,sizeAttenuation:false}));dot.userData.feature=feature;group.add(dot);selectable.push(dot);
      }else makeLines(feature.geometry,material,height,group,feature,isRoad||id==='railways');
    }
  }
  const dispose=(object:THREE.Object3D)=>object.traverse(obj=>{if(obj instanceof THREE.Line||obj instanceof THREE.Points||obj instanceof THREE.Mesh){obj.geometry.dispose();const materials=Array.isArray(obj.material)?obj.material:[obj.material];materials.forEach(m=>m.dispose());}});
  const highlight=(feature:Feature|null)=>{
    if(highlightObject){scene.remove(highlightObject);dispose(highlightObject);highlightObject=null;}
    if(feature){const group=new THREE.Group();makeLines(feature.geometry,new THREE.LineBasicMaterial({color:'#ffffff'}),12,group,feature,false);highlightObject=group;scene.add(group);}render();
  };
  const fit=(area:string)=>{
    currentArea=area;const boundary=bundle.layers.boundaries.find(f=>f.id===`boundary:${area}`)!;const points:THREE.Vector3[]=[];
    const traverse=(coords:any)=>{if(typeof coords[0]==='number')points.push(position(coords));else coords.forEach(traverse);};traverse(boundary.geometry.coordinates);
    const box=new THREE.Box3().setFromPoints(points);const size=box.getSize(new THREE.Vector3());const center=box.getCenter(new THREE.Vector3());const aspect=el.clientWidth/Math.max(1,el.clientHeight);const span=Math.max(size.z,size.x/aspect)*1.16;
    camera.left=-span*aspect/2;camera.right=span*aspect/2;camera.top=span/2;camera.bottom=-span/2;camera.zoom=1;camera.position.set(center.x,10000,center.z+.1);controls.target.set(center.x,0,center.z);camera.updateProjectionMatrix();controls.update();render();
  };
  const resize=()=>{renderer.setSize(el.clientWidth,el.clientHeight);fit(currentArea);};const observer=new ResizeObserver(resize);observer.observe(el);controls.addEventListener('change',render);
  const down=(e:PointerEvent)=>{moved=false;startX=e.clientX;startY=e.clientY;};
  const move=(e:PointerEvent)=>{if(Math.hypot(e.clientX-startX,e.clientY-startY)>5)moved=true;};
  const up=(e:PointerEvent)=>{
    if(moved)return;const rect=renderer.domElement.getBoundingClientRect();mouse.set((e.clientX-rect.left)/rect.width*2-1,-(e.clientY-rect.top)/rect.height*2+1);ray.params.Line={threshold:(camera.right-camera.left)/camera.zoom/rect.width*7};ray.params.Points={threshold:ray.params.Line.threshold*1.3};ray.setFromCamera(mouse,camera);
    const hits=ray.intersectObjects(selectable.filter(obj=>obj.parent?.visible),false);if(hits[0])onSelect(hits[0].object.userData.feature);
  };
  const lost=(e:Event)=>{e.preventDefault();onError('Konteks WebGL terputus. Muat ulang preview.');};renderer.domElement.addEventListener('webglcontextlost',lost);renderer.domElement.addEventListener('pointerdown',down);renderer.domElement.addEventListener('pointermove',move);renderer.domElement.addEventListener('pointerup',up);
  world.current={groups,render,highlight,fit};resize();highlight(selectedRef.current);onReady('WEBGL READY · EPSG:32749');
  return()=>{observer.disconnect();controls.dispose();renderer.domElement.removeEventListener('webglcontextlost',lost);renderer.domElement.removeEventListener('pointerdown',down);renderer.domElement.removeEventListener('pointermove',move);renderer.domElement.removeEventListener('pointerup',up);dispose(scene);renderer.dispose();renderer.domElement.remove();world.current=null;};
 },[bundle]);
 useEffect(()=>{if(world.current){for(const [id,group] of Object.entries(world.current.groups))group.visible=visible[id]??false;world.current.render();}},[visible]);
 useEffect(()=>{world.current?.highlight(selected&&(!selected.properties.road_function||visible[selected.properties.road_function])?selected:null);},[selected,visible]);
 useEffect(()=>{world.current?.fit(view.area);},[view]);
 const labelFeatures=[
  {feature:bundle.layers.stations[0],layer:'stations',text:'Stasiun Gedangan',offset:[18,-30]},
  {feature:bundle.layers.main_arterial_road.find(f=>f.properties.osm_id===266287935),layer:'main_arterial_road',text:'Ahmad Yani · utama',offset:[-150,-25]},
  {feature:bundle.layers.frontage_road.find(f=>f.properties.osm_id===1120215176),layer:'frontage_road',text:'Frontage Gedangan',offset:[18,-10]},
  {feature:bundle.layers.junctions.find(f=>f.properties.osm_id===2718664260),layer:'main_arterial_road',text:'Simpang Gedangan',offset:[-145,18]},
  {feature:bundle.layers.junctions.find(f=>f.properties.osm_id===1720713565),layer:'frontage_road',text:'Simpang frontage / Ketajen',offset:[18,18]}
 ].filter(item=>item.feature).map(item=>({...item,feature:item.feature!,coordinate:item.feature!.geometry.type==='Point'?item.feature!.geometry.coordinates:item.feature!.geometry.coordinates[Math.floor(item.feature!.geometry.coordinates.length/2)]}));
 return <div ref={host} className="map-canvas">{labelFeatures.map(label=><button data-map-label={label.feature.id} className="map-label" key={label.feature.id} onClick={()=>onSelect(label.feature)}>{label.text}</button>)}</div>;
}

function App(){
 const [bundle,setBundle]=useState<Bundle|null>(null);const [error,setError]=useState('');const [ready,setReady]=useState('MEMUAT DATA');const [visible,setVisible]=useState(defaults);const [selected,setSelected]=useState<Feature|null>(null);const [view,setView]=useState<{area:'core'|'context';reset:number}>({area:'core',reset:0});const [search,setSearch]=useState('');const [pane,setPane]=useState<'layers'|'quality'|'source'>('layers');
 useEffect(()=>{const abort=new AbortController();fetch('/geodata/m02/map-utm49s.json',{signal:abort.signal}).then(r=>{if(!r.ok)throw Error(`HTTP ${r.status}`);return r.json();}).then((d:Bundle)=>{if(d.crs!=='EPSG:32749'||!d.layers?.main_arterial_road?.length||!d.layers?.railways?.length)throw Error('Kontrak data peta tidak sesuai');setBundle(d);}).catch(e=>{if(e.name!=='AbortError')setError('Data geografis gagal dimuat: '+String(e));});return()=>abort.abort();},[]);
 const roads=bundle?Object.entries(bundle.layers).filter(([k])=>k.endsWith('_road')).flatMap(([,fs])=>fs):[];
 const matches=search.trim()?roads.filter(f=>(f.properties.name||f.id).toLowerCase().includes(search.toLowerCase())||String(f.properties.osm_id).includes(search)).slice(0,20):[];
 const choose=(f:Feature)=>{setSelected(f);const layer=f.properties.road_function;if(layer)setVisible(v=>({...v,[layer]:true}));};
 const p=selected?.properties;const fmt=(value:any)=>value===null||value===undefined?'Unknown / null':typeof value==='boolean'?value?'Ya':'Tidak':String(value);
 return <div className="mapping-app"><header><a className="mapping-brand" href="/mapping.html" title="Gedangan Geographic Mapping M02"><span>g↗</span><div>GEDANGAN<small>TRAFFIC RESEARCH PLATFORM</small></div></a><div className="header-title"><b>Geographic Mapping</b><span>MILESTONE 02 <i>/</i> BASELINE 2026</span></div><div className="phase"><span className="state-dot"/>MAPPING ONLY <small>ENGINE NOT CONNECTED</small></div></header>
 <div className="mapping-toolbar"><div><span className="eyebrow">GEOGRAPHIC WORKSPACE</span><h1>Gedangan, dari jaringan sebenarnya.</h1><p>Referensi OSM · posisi proporsional dalam meter · belum diverifikasi lapangan.</p></div><div className="area-switch" aria-label="Cakupan studi"><button className={view.area==='core'?'active':''} onClick={()=>setView(v=>({area:'core',reset:v.reset+1}))}>Core area</button><button className={view.area==='context'?'active':''} onClick={()=>setView(v=>({area:'context',reset:v.reset+1}))}>Context area</button><button onClick={()=>setView(v=>({...v,reset:v.reset+1}))} title="Reset kamera" aria-label="Reset kamera">↺</button></div></div>
 <div className="mapping-body"><aside className="map-sidebar"><div className="panel-tabs">{[['layers','Layer'],['quality','Kualitas'],['source','Sumber']].map(([id,label])=><button key={id} className={pane===id?'active':''} onClick={()=>setPane(id as typeof pane)}>{label}</button>)}</div>
 {pane==='layers'&&<><div className="section-label">VISIBILITY & LEGENDA</div><div className="layer-list">{layers.map(([id,label,color])=><label key={id}><input type="checkbox" checked={visible[id]} onChange={e=>setVisible(v=>({...v,[id]:e.target.checked}))}/><span className="legend-line" style={{background:color}}/><span>{label}</span><small>{bundle?.layers[id]?.length??'—'}</small></label>)}</div><div className="sidebar-note"><b>Garis ≠ lebar jalan.</b><p>Warna menunjukkan fungsi riset. Lebar simbol dan titik dibuat untuk keterbacaan, bukan ukuran fisik.</p></div><div className="section-label">CARI & PILIH RUAS</div><input className="search" aria-label="Cari ruas jalan" placeholder="Nama jalan / ID OSM…" value={search} onChange={e=>setSearch(e.target.value)}/><div className="search-results">{matches.map(f=><button key={f.id} onClick={()=>choose(f)}><b>{f.properties.name||'Tanpa nama OSM'}</b><small>{f.id}</small></button>)}{search&&!matches.length&&<p>Tidak ada ruas yang cocok.</p>}</div></>}
 {pane==='quality'&&<div className="quality-panel"><span className="quality-badge">PARTIALLY VERIFIED</span><h2>Format diperiksa.<br/>Lapangan belum.</h2><p>Geometri menyalin node OSM. Ini tidak membuktikan seluruh atribut atau koneksi legal kendaraan benar.</p>{bundle&&<><dl><dt>Segmen jalan</dt><dd>{bundle.qa.counts.road_segments}</dd><dt>Komponen undirected</dt><dd>{bundle.qa.topology.undirected_component_count}</dd><dt>Ujung / batas jaringan</dt><dd>{bundle.qa.topology.deadend_or_boundary_nodes_count}</dd><dt>Geometri jalan invalid</dt><dd>{bundle.qa.geometry.invalid_or_empty_road_ids.length}</dd><dt>Duplikasi identik</dt><dd>{bundle.qa.geometry.duplicate_geometry_pairs.length}</dd><dt>Arah belum bertag</dt><dd>{bundle.qa.topology.unknown_oneway_segments}</dd></dl><h3>Atribut belum tersedia</h3><dl>{Object.entries(bundle.qa.missing_attributes).map(([key,val])=><React.Fragment key={key}><dt>{key}</dt><dd>{String(val)}</dd></React.Fragment>)}</dl></>}<p>Batas context adalah hipotesis cakupan riset. Kecukupannya terhadap antrean perlu diuji pada tahap kalibrasi.</p><a href="/geodata/m02/quality_report.json" target="_blank" rel="noreferrer">Buka laporan QA JSON ↗</a></div>}
 {pane==='source'&&<div className="source-panel"><span className="quality-badge">RESEARCH REFERENCE</span><h2>OpenStreetMap</h2><p>© OpenStreetMap contributors · ODbL 1.0</p><dl><dt>Snapshot</dt><dd>{bundle?.source.osm_base_timestamp??'—'}</dd><dt>Diambil (UTC)</dt><dd>{bundle?.source.retrieved_at_utc??'—'}</dd><dt>Simpan</dt><dd>EPSG:4326 · lon, lat</dd><dt>Analisis / display</dt><dd>EPSG:32749 · meter</dd><dt>Survei lapangan</dt><dd>Belum dilakukan</dd></dl><a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noreferrer">Lisensi & atribusi ↗</a><p>Batas studi adalah hasil pemilihan jaringan dengan anchor OSM. Batas bukan batas administratif atau hasil pengukuran panjang antrean.</p><a href="/geodata/m02/all_features.geojson" download>Unduh GeoJSON EPSG:4326 ↓</a><div className="sidebar-note"><b>Observasi pengguna · Unverified</b><p>Frontage relatif lancar; kapasitas alternatif arus utama menuju Surabaya belum memadai. Belum dibuktikan dengan pengukuran.</p></div></div>}
 </aside><section className="map-stage" aria-label="Visualisasi geografis"><div className="canvas-top"><span><i/>OSM NETWORK <b>{view.area.toUpperCase()} STUDY AREA</b></span><span className="north">N ↑</span></div>{bundle&&<MapCanvas bundle={bundle} visible={visible} selected={selected} onSelect={choose} view={view} onReady={setReady} onError={setError}/>}{!bundle&&!error&&<div className="map-loading">Memuat geometri referensi OSM…</div>}{error&&<div role="alert" className="map-error">{error}</div>}<div className="map-bottom"><span role="status">{error?'RENDER / DATA ERROR':ready}</span><span>Drag: orbit · Roda: zoom · Klik ruas: atribut</span></div><div className="attribution">© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noreferrer">OpenStreetMap contributors</a> · ODbL 1.0</div></section><aside className="feature-panel"><div className="section-label">FEATURE INSPECTOR</div><h2>{p?.name|| (selected?'Objek tanpa nama OSM':'Pilih ruas jalan.')}</h2><p className="inspect-intro">{selected?'Atribut sumber dan informasi yang masih belum tersedia.':'Klik garis pada peta atau cari nama ruas di panel kiri untuk memeriksa atributnya.'}</p>{selected?<><span className="quality-badge">{p?.verification_status?.toUpperCase()}</span><dl className="feature-attributes">{[['ID',selected.id],['OSM',`${p?.osm_type??'derived'} ${p?.osm_id??''}`],['Fungsi riset',p?.road_function],['Arah OSM',p?.oneway],['Pergerakan',p?.movement_direction],['Lajur (tag)',p?.lanes],['Lebar (m)',p?.width_m],['Batas kecepatan (km/jam)',p?.maxspeed_kmh],['Panjang geometri (m)',p?.length_m],['Akses (tag)',p?.access],['Sumber',p?.source_id],['Versi OSM',p?.osm_version],['Survei lapangan',p?.field_survey_check],['Kapasitas kendaraan/jam',p?.capacity_vehicles_per_hour]].map(([key,val])=><React.Fragment key={key}><dt>{key}</dt><dd>{fmt(val)}</dd></React.Fragment>)}</dl>{p?.osm_url&&<a href={p.osm_url} target="_blank" rel="noreferrer">Buka objek OSM ↗</a>}<details><summary>Tag OSM asli</summary><pre>{JSON.stringify(p?.tags??{},null,2)}</pre></details><p className="footnote">Panjang dihitung dari geometri OSM pada UTM 49S. Bukan pengukuran lapangan. Unknown tidak berarti nol.</p></>:<><div className="empty-feature">⌕<span>NO FEATURE SELECTED</span></div><div className="scope-card"><span className="eyebrow">PRIORITAS PENELITIAN</span><h3>Sidoarjo → Surabaya</h3><p>Jalan utama dan frontage ditampilkan terpisah. Arus, kapasitas, waktu tempuh dan tingkat kemacetan belum diukur.</p></div></>}<div className="inspector-footer">M02 / GEOGRAPHY & TOOLCHAIN<br/>Tidak ada kendaraan atau simulasi aktif.</div></aside></div><footer><span>GEDANGAN TRAFFIC SIMULATOR <i>/</i> GEOGRAPHIC REFERENCE BUILD 0.2</span><span>Batas berbasis konektivitas · Geometri OSM · Data lalu lintas belum dikalibrasi</span></footer></div>;
}
// Retain the root across Vite updates; avoid duplicate createRoot during HMR.
const rootHost=document.getElementById('root')! as HTMLElement & {m02Root?:ReturnType<typeof createRoot>};
(rootHost.m02Root??=createRoot(rootHost)).render(<App/>);
