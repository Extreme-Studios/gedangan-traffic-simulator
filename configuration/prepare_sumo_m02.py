"""Portable official stable SUMO, project-local only. No registry/PATH changes."""
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import urllib.request
import zipfile

ROOT=Path(__file__).resolve().parents[1]
VERSION='1.28.0'
URL=f'https://sumo.dlr.de/releases/{VERSION}/sumo-win64-{VERSION}.zip'

def main():
    target=ROOT/'toolchain'; downloads=target/'downloads';downloads.mkdir(parents=True,exist_ok=True)
    archive=downloads/f'sumo-win64-{VERSION}.zip'
    if not archive.exists():
        temp=archive.with_suffix('.part')
        print('Downloading official stable Windows x64 zip:',URL,flush=True)
        with urllib.request.urlopen(URL,timeout=90) as response,temp.open('wb') as out:
            size=response.headers.get('Content-Length');total=0
            while chunk:=response.read(1024*1024):
                out.write(chunk);total+=len(chunk)
                if total % (32*1024*1024)==0:print(total,'bytes /',size,flush=True)
        temp.rename(archive)
    with zipfile.ZipFile(archive) as z:
        for entry in z.infolist():
            dest=(target/entry.filename).resolve()
            if not dest.is_relative_to(target.resolve()):raise ValueError('Archive path outside project toolchain')
        bad=z.testzip()
        if bad:raise ValueError(f'ZIP CRC failed: {bad}')
        roots={Path(n).parts[0] for n in z.namelist() if Path(n).parts}
        if len(roots)!=1:raise ValueError('Unexpected archive layout')
        home=target/next(iter(roots))
        if not home.exists():
            print('Extracting project-local SUMO',flush=True);z.extractall(target)
    required=['sumo.exe','sumo-gui.exe','netedit.exe','netconvert.exe']
    for exe in required:
        if not (home/'bin'/exe).is_file():raise ValueError(f'Missing {exe}')
    if not (home/'tools/traci/__init__.py').is_file():raise ValueError('Bundled TraCI missing')
    if not (home/'tools/sumolib/__init__.py').is_file():raise ValueError('Bundled sumolib missing')
    config={'version':VERSION,'sumo_home_relative':str(home.relative_to(ROOT)).replace('\\','/'),'download_url':URL,'official_downloads_page':'https://eclipse.dev/sumo/docs/Downloads.html','archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'hash_verification':'Local SHA256 recorded; ZIP CRC tested; no independent publisher checksum compared','prepared_at_utc':datetime.now(timezone.utc).isoformat(),'scope':'project-local portable distribution; no system environment change','python_interfaces':'Bundled tools/traci and tools/sumolib from same archive; no separate pip versions'}
    (ROOT/'configuration/sumo-m02.json').write_text(json.dumps(config,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(config,indent=2),flush=True)

if __name__=='__main__':main()
