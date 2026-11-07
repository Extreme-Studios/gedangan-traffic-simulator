"""Bootstrap failures are recorded even before the host is imported."""
if __name__=='__main__':
 try:
  from backend.gedangan.m12_host import main
  main()
 except Exception:
  import sys,traceback,os
  from pathlib import Path
  root=Path(os.environ.get('M12_DATA_DIR',str(Path(sys.executable).parent.parent/'USER_DATA')));root.mkdir(parents=True,exist_ok=True)
  (root/'bootstrap-error.txt').write_text(traceback.format_exc(),encoding='utf-8')
  if '--no-open' not in sys.argv and '--serve' not in sys.argv:
   import ctypes
   ctypes.windll.user32.MessageBoxW(None,'Aplikasi belum dapat dibuka. Ekstrak seluruh paket terlebih dahulu. Rincian: USER_DATA/bootstrap-error.txt','Gedangan Traffic Simulator',16)
  sys.exit(1)
