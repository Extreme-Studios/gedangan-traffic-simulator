import React, {useEffect, useMemo, useRef, useState} from 'react';
import {createRoot} from 'react-dom/client';
import {World} from './world';
import {loadRecording} from './RecordingLoader';
import {type D, type Recording} from './core';
import './style.css';
import './simple.css';

const mix = [
  ['motorcycle', 'Motor', 65], ['car', 'Mobil', 22], ['angkot', 'Angkot', 6],
  ['light_truck', 'Truk ringan', 4], ['heavy_truck', 'Truk berat', 2], ['trailer', 'Trailer', 1],
] as const;

function composition(total: number) {
  const rows = mix.map(([id, label, percent]) => {
    const exact = total * percent / 100;
    return {id, label, count: Math.floor(exact), remainder: exact - Math.floor(exact)};
  });
  const order = rows.map((row, index) => ({...row, index}))
    .sort((a, b) => b.remainder - a.remainder || a.index - b.index);
  for (const row of order.slice(0, total - rows.reduce((sum, row) => sum + row.count, 0))) {
    rows[row.index].count++;
  }
  return rows;
}

async function api(path: string, body?: unknown) {
  const response = await fetch('/api/' + path, body === undefined ? {} : {
    method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body),
  });
  const data = await response.json();
  if (!response.ok) throw Error(data.error || 'Permintaan gagal');
  return data;
}

function App() {
  const [input, setInput] = useState('3000');
  const [scene, setScene] = useState<D>();
  const [recording, setRecording] = useState<Recording>();
  const [time, setTime] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState('Isi jumlah kendaraan, lalu jalankan simulasi.');
  const [error, setError] = useState('');
  const [camera, setCamera] = useState('junction');
  const [selected, setSelected] = useState<number | null>(null);
  const controller = useRef<AbortController | null>(null);
  const shared = useRef(null);
  const mounted = useRef(true);
  const total = Number(input);
  const valid = input.trim() !== '' && Number.isInteger(total) && total >= 1 && total <= 20000;
  const rows = composition(valid ? total : 0);

  useEffect(() => {
    api('scene').then(setScene).catch(error => setError(error.message));
    return () => {mounted.current = false; controller.current?.abort();};
  }, []);

  useEffect(() => {
    if (!playing || !recording) return;
    let frame = 0;
    let last = performance.now();
    const tick = (now: number) => {
      const elapsed = (now - last) / 1000;
      last = now;
      setTime(value => {
        const next = Math.min(recording.duration_s, value + elapsed * 5);
        if (next === recording.duration_s) setPlaying(false);
        return next;
      });
      frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [playing, recording]);

  async function start(event: React.FormEvent) {
    event.preventDefault();
    if (!valid || busy) return;
    setBusy(true);
    setError('');
    setPlaying(false);
    controller.current?.abort();
    const current = new AbortController();
    controller.current = current;
    try {
      setMessage('Menyiapkan komposisi dan menjalankan simulasi…');
      const job = await api('generate', {total});
      let complete: D;
      while (true) {
        await new Promise(resolve => setTimeout(resolve, 1000));
        if (current.signal.aborted) return;
        const state = await api('jobs/' + job.job_id);
        if (state.status === 'FAILED') throw Error(state.error);
        if (state.status === 'COMPLETE') {complete = state; break;}
        const progress = state.progress;
        setMessage(progress?.elapsed_s !== undefined
          ? 'Menghitung ' + Math.round(progress.elapsed_s / 3600 * 100) + '% · ' +
            progress.departed + ' kendaraan berangkat'
          : 'Menyiapkan rute kendaraan…');
      }
      setMessage('Membuka hasil simulasi…');
      const result = await loadRecording(complete.run_id, current.signal);
      if (current.signal.aborted) return;
      setRecording(result);
      setTime(0);
      setSelected(null);
      setPlaying(true);
      setMessage('Hasil ' + total.toLocaleString('id-ID') + ' kendaraan siap. Pemutaran 5×.');
    } catch (problem) {
      if (!current.signal.aborted) setError(problem instanceof Error ? problem.message : String(problem));
    } finally {
      if (mounted.current) setBusy(false);
    }
  }

  const vehicleTypes = useMemo(() => [...new Set<string>((recording?.vehicles || []).map((vehicle: D) => String(vehicle.type)))], [recording]);
  const result = recording?.metrics;
  return <main className="simple-app">
    <header className="simple-header">
      <span>EXTREME STUDIOS</span>
      <h1>Simulasi Lalu Lintas Gedangan</h1>
      <p>Masukkan jumlah kendaraan. Komposisi dan rute diatur otomatis untuk simulasi satu jam.</p>
    </header>
    <form className="simple-input" onSubmit={start}>
      <label htmlFor="total">Jumlah kendaraan</label>
      <div className="simple-entry">
        <input id="total" type="number" min="1" max="20000" step="1" value={input}
          disabled={busy} onChange={event => setInput(event.target.value)}
          aria-describedby="input-help" required />
        <button type="submit" disabled={!valid || busy || !scene}>
          {busy ? 'Sedang menghitung…' : 'Jalankan simulasi'}
        </button>
      </div>
      <small id="input-help">1–20.000 kendaraan selama satu jam</small>
      <div className="simple-mix" aria-label="Komposisi otomatis">
        {rows.map(row => <div key={row.id}><span>{row.label}</span><b>{row.count.toLocaleString('id-ID')}</b></div>)}
      </div>
      <p className="simple-note">Angkot memakai model van dengan parameter asumsi.
        Pejalan kaki belum tersedia karena jaringan belum memiliki jalur legal pejalan kaki.
        Trailer mengikuti pemeriksaan izin dan clearance rute.</p>
    </form>
    <p className="simple-status" role="status">{message}</p>
    {error && <p className="simple-error" role="alert">{error}</p>}
    {result && <div className="simple-results" aria-label="Hasil simulasi">
      {[['Diminta', result.requested], ['Berangkat', result.departed], ['Tiba', result.arrived],
        ['Masih di jalan', result.active], ['Menunggu masuk', result.not_departed],
        ['Rute ditolak', result.failed_routes]].map(([label, value]) =>
        <div key={String(label)}><span>{label}</span><b>{Number(value).toLocaleString('id-ID')}</b></div>)}
    </div>}
    <section className="simple-scene">
      <div className="simple-controls">
        <button disabled={!recording} onClick={() => setPlaying(value => !value)}>
          {playing ? 'Jeda' : 'Putar'}
        </button>
        <button disabled={!recording} onClick={() => {setTime(0); setPlaying(false);}}>Ulang dari awal</button>
        <label>Kamera<select value={camera} onChange={event => setCamera(event.target.value)}>
          <option value="junction">Simpang Gedangan</option>
          <option value="rail">Perlintasan kereta</option>
          <option value="main">Koridor utama</option>
          <option value="frontageClose">Frontage</option>
          <option value="overview">Gambaran area</option>
        </select></label>
        <span>{(time / 60).toFixed(1)} / 60 menit</span>
      </div>
      <div className="viewport">
        {scene && recording ? <World scene={scene} recording={recording} time={time}
          filter={vehicleTypes}
          camera={camera} cameraReset={0} bookmark={null} shared={shared}
          selected={selected} onSelect={setSelected} context={true} overlay="none"
          concept={false} onStats={() => {}} statusLabels={true} /> :
          <div className="simple-empty">Hasil simulasi akan tampil di sini.</div>}
      </div>
      {recording && <input className="timeline" aria-label="Waktu playback" type="range"
        min="0" max={recording.duration_s} step=".5" value={time}
        onChange={event => {setTime(Number(event.target.value)); setPlaying(false);}} />}
    </section>
    <footer>Skenario otomatis · Geometri sumber OSM · Tinggi dan fasad bangunan asumsi ·
      Jaringan provisional, belum terkalibrasi data lapangan.</footer>
  </main>;
}

createRoot(document.getElementById('root')!).render(<App />);

