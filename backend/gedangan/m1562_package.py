"""Index real captured evidence; refuse to certify an absent final movie."""
from .m1562_common import *
import subprocess

def probe(p):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=width,height,codec_name,avg_frame_rate','-show_entries','format=duration,size','-of','json',str(p)],text=True))

def main():
 evidence=DOC/'evidence';screens=[]
 for name in ['before-junction','before-rail','after-junction','after-rail','junction-close','station','frontage-close','vehicle-detail','overview','source-confidence-map']:
  p=evidence/(name+'.jpg')
  if not p.is_file():continue
  metadata=probe(p);assert metadata['streams'][0]['width']==1920 and metadata['streams'][0]['height']==1080
  screens.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'metadata':metadata,'source':'Actual internal browser page screenshot, full UI viewport clip; no synthetic assembly or rescale'})
 movie=ROOT/'GEDANGAN_M15_6_2_VISUAL_REVIEW.mp4';video=None
 if movie.is_file():
  metadata=probe(movie);assert 45<=float(metadata['format']['duration'])<=60;assert metadata['streams'][0]['width']==1920 and metadata['streams'][0]['height']==1080
  video={'path':movie.relative_to(ROOT).as_posix(),'sha256':sha(movie),'metadata':metadata,'source':'Actual getDisplayMedia tab capture, UI + animated WebGL. H264 delivery transcode; not still-frame animation.','edit':'Preserve entire49.933s raw capture; scale changing source dimensions to fixed1920x1080 delivery, square pixels. Source becomes native1920x1080 at5.685s; first5.685s contains viewport resizing and is not native1920. No still frames added, traffic values changed or motion synthesized.','capture_quality':'REVIEW REQUIRED; minor startup resize artifact and soft screen-capture UI text remain','raw_capture':'documentation/m1562/evidence/actual-playback.webm'}
 package={'created_utc':now(),'status':'ACTUAL_PACKAGE_READY_USER_REVIEW_REQUIRED'if video and len(screens)==10 else'SCREENSHOTS_READY_FINAL_TOUR_PENDING','visual_acceptance':'REVIEW REQUIRED','screenshots':screens,'video':video,'matched_comparisons':[{'before':'before-junction.jpg','after':'after-junction.jpg','camera':'junction','time':1796,'run':'cc419452a995456df324fd05'},{'before':'before-rail.jpg','after':'after-rail.jpg','camera':'rail','time':1796,'run':'cc419452a995456df324fd05'}],'limitations':['Height/roof/facade assumptions remain. No surveyed photorealism claim.','Frontage close-up shows frozen geography; no decorative traffic inserted into empty timestamp.','Station frontage remains partly obscured by source-mapped neighboring footprint; exact visibility depends camera.','Source landuse boundaries/material transitions can still appear coarse.','First-screen-review.webm retained as failed framing attempt; final video is separately named.']}
 save(DOC/'review-package.json',package)
 save(DOC/'environment-assets.json',{'modeling':'Native procedural Three.js; Blender NOT USED','footprints':'953 source polygon building bodies, source ID/version/timestamp preserved','detail':'219 priority-area facades; heights/roof/door/window/awnings assumed; station photo-referenced character only','ground':'10 source landuse polygons; tone/grain material assumed','textures':'Shared256px procedural grain canvases;512x128 station sign canvas; no protected image textures','gpu_resources':'Actual counts per benchmark-summary.json; renderer disposes geometries/materials/maps/RAF/listeners on switch','roads':'Frozen SUMO lane/junction/rail geometries; visual material transition only, no additional road/gate/drainage','license':'OpenStreetMap contributors ODbL1.0; photo reference Rizal Febri Ardiansyah CC BY-SA4.0','traffic':'Retained SUMO frame positions; vehicle models inherited, instanced; no decorative traffic'})
 from .m1562_reports import main as reports
 reports()
 candidates=list((ROOT/'frontend/src/m1562').rglob('*'))+list((ROOT/'frontend/dist-m1562').rglob('*'))+list((ROOT/'backend/gedangan').glob('m1562_*.py'))+list((ROOT/'tests/m1562').rglob('*.py'))+list((ROOT/'staging/m1562').rglob('*'))+list(DOC.rglob('*'))+list(ROOT.glob('M15_6_2*.md'))+[ROOT/'frontend/m1562.html',ROOT/'frontend/vite.m1562.config.ts',ROOT/'frontend/tsconfig.m1562.json']
 if movie.is_file():candidates.append(movie)
 files={p.relative_to(ROOT).as_posix():sha(p)for p in candidates if p.is_file()and'__pycache__'not in p.parts and p.name!='artifact-manifest.json'}
 save(DOC/'artifact-manifest.json',{'created_utc':now(),'network_sha256':sha(NETWORK),'visual_acceptance':'REVIEW REQUIRED','files':files})
 print({'screenshots':len(screens),'video':video is not None,'manifest_files':len(files),'status':package['status']})
if __name__=='__main__':main()
