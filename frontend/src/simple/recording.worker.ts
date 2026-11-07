/// <reference lib="webworker" />

async function readChunk(url: string, expectedBytes: number): Promise<ArrayBuffer> {
  let received = 0;
  for (let attempt = 0; attempt < 3; attempt++) {
    const response = await fetch(url, {cache: 'no-store'});
    if (!response.ok) throw Error('Gagal memuat rekaman (' + response.status + ')');
    const buffer = await response.arrayBuffer();
    received = buffer.byteLength;
    if (received === expectedBytes) return buffer;
  }
  throw Error('Rekaman tidak lengkap. Diterima ' + received + ' dari ' + expectedBytes + ' byte.');
}

self.onmessage = async (event: MessageEvent) => {
  try {
    const base = '/api/packed/' + event.data + '/';
    const response = await fetch(base + 'index.json', {cache: 'no-store'});
    if (!response.ok) throw Error('Indeks rekaman gagal dimuat.');
    const index = await response.json();
    self.postMessage({kind: 'index', index});
    for (const chunk of index.chunks) {
      const buffer = await readChunk(base + chunk.file, chunk.byte_length);
      self.postMessage({kind: 'chunk', chunk, buffer}, [buffer]);
    }
    self.postMessage({kind: 'complete'});
  } catch (error) {
    self.postMessage({kind: 'error', error: String(error)});
  }
};
