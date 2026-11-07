from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'tests/storage_cleanup';OUT.mkdir(exist_ok=True)
for name in ['application.cjs','survey.cjs','synchronization.cjs','presentation.cjs']:
 text=(ROOT/'tests/m12'/name).read_text(encoding='utf-8-sig').replace("'documentation/m12/qa'","'documentation/storage_cleanup/qa'").replace('http://127.0.0.1:5192','http://127.0.0.1:5198').replace('process.env.M12_TEST_PORT||5192','process.env.M12_TEST_PORT||5198')
 (OUT/name).write_text(text,encoding='utf-8')
print('Maintenance copies of existing M12 actual-browser harness prepared. Original QA evidence remains unchanged.')
