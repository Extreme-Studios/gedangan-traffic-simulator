import unittest,json,gzip,array,sys,xml.etree.ElementTree as ET
from pathlib import Path
from shapely.geometry import Polygon
from pyproj import Transformer
from backend.gedangan.m1562_common import ROOT,DOC,DATA,NETWORK,EXPECTED,sha,load

class Integrity(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.scene=load(DOC/'scene.json');cls.old=load(ROOT/'documentation/m1561/scene.json')
 def test_network_immutable(self):self.assertEqual(sha(NETWORK),EXPECTED)
 def test_frozen_scene(self):
  for key in ['lanes','junctions','heads','crossing','presets','origin_local','bounds']:self.assertEqual(self.scene[key],self.old[key],key)
 def test_source_positions_not_invented(self):
  tree=ET.parse(DOC/'sources/gedangan.osm').getroot();ns={n.get('id'):(float(n.get('lon')),float(n.get('lat')))for n in tree.findall('node')};ways={w.get('id'):w for w in tree.findall('way')};t=Transformer.from_crs('EPSG:4326','EPSG:32749',always_xy=True)
  for b in self.scene['environment']['buildings']:
   expected=[]
   for n in ways[b['source_id']].findall('nd'):
    x,y=t.transform(*ns[n.get('ref')]);expected.append([x-690790.39,y-9182879.52])
   self.assertEqual(b['polygon'],expected)
 def test_confidence_labels(self):
  for b in self.scene['environment']['buildings']:
   self.assertEqual(b['footprint_confidence'],'SOURCE-MAPPED FOOTPRINT');self.assertEqual(b['height_confidence'],'ASSUMED 3D HEIGHT');self.assertNotIn('VERIFIED',b['appearance_confidence'])
 def test_station(self):
  stations=[b for b in self.scene['environment']['buildings']if b['kind']=='station'];self.assertEqual(len(stations),1);self.assertEqual(stations[0]['source_id'],'472866576');self.assertAlmostEqual(stations[0]['area_m2'],392.6255246698245)
 def test_no_guessed_infill(self):
  self.assertEqual(self.scene['buildings'],[]);self.assertTrue(all(b['id'].startswith('osm-way-')for b in self.scene['environment']['buildings']))
 def test_preservation(self):
  for path,digest in load(DOC/'preservation-before.json').items():self.assertEqual(sha(ROOT/path),digest,path)
 def test_lossless_all_values(self):
  results=[]
  for key in ['cc419452a995456df324fd05','569df9741bf6f16d1cffa31e']:
   source=ROOT/'simulation/runs/m155'/key;packed=DATA/'recordings'/key;index=load(packed/'index.json');original=load(source/'playback-index.json');self.assertEqual(index['vehicles'],original['vehicles']);self.assertEqual(index['events'],original['events']);self.assertEqual(index['metrics'],original['metrics']);count=0;frames=0
   for name,chunk in zip(original['chunks'],index['chunks']):
    with gzip.open(source/name,'rt',encoding='utf-8')as f:rows=json.load(f)
    with gzip.open(packed/chunk['file'],'rb')as f:buffer=array.array('d');buffer.frombytes(f.read())
    if sys.byteorder!='little':buffer.byteswap()
    expected=array.array('d',(v for frame in rows for pose in frame['p']for v in pose));self.assertEqual(buffer,expected);offset=0
    for frame,descriptor in zip(rows,chunk['frames']):self.assertEqual(descriptor,[frame['t'],offset,len(frame['p'])]);offset+=len(frame['p'])*6;count+=len(frame['p']);frames+=1
    self.assertEqual(sha(source/name),index['source_chunk_sha256'][name])
   self.assertEqual(count,index['positions']);self.assertEqual(frames,7200);results.append({'run':key,'positions':count,'frames':frames,'all_six_fields':'EXACT_FLOAT64_EQUAL'})
  (DOC/'lossless-verification.json').write_text(json.dumps(results,indent=2),encoding='utf-8')

if __name__=='__main__':unittest.main()
