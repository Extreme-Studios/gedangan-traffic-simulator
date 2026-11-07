// Software-only fixture; checks the exact browser hashing implementation.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),vm=require('node:vm');
const root=path.resolve(__dirname,'../..');const esbuild=require(path.join(root,'frontend/node_modules/esbuild'));
const module85={exports:{}};vm.runInNewContext(esbuild.transformSync(fs.readFileSync(path.join(root,'frontend/src/m085/sha256.ts'),'utf8'),{loader:'ts',format:'cjs',target:'es2020'}).code,{module:module85,exports:module85.exports,Uint8Array,Uint32Array,BigInt});
const {SHA256}=module85.exports;let checks=0;
for(const n of [0,1,3,55,56,63,64,65,127,128,129,1048576+129]){const input=Buffer.alloc(n);for(let i=0;i<n;i++)input[i]=(i*31+7)%256;const expected=crypto.createHash('sha256').update(input).digest('hex');for(const size of [1,63,64,65,1048576]){const h=new SHA256();for(let i=0;i<n;i+=size)h.update(input.subarray(i,i+size));if(h.hex()!==expected)throw Error(`SHA256 mismatch n=${n}, chunk=${size}`);checks++}}
for(const text of ['', 'abc', 'Gedangan · uji UTF-8']){const input=Buffer.from(text);if(new SHA256().update(input).hex()!==crypto.createHash('sha256').update(input).digest('hex'))throw Error('UTF8 hash mismatch');checks++}
const fixture=fs.readFileSync(path.join(root,'tests/fixtures/m085/synthetic-annotation.mp4'));const h=new SHA256();for(let i=0;i<fixture.length;i+=1048576)h.update(fixture.subarray(i,i+1048576));if(h.hex()!==crypto.createHash('sha256').update(fixture).digest('hex'))throw Error('Video hash mismatch');checks++;
console.log(JSON.stringify({checks,passed:true,video_bytes:fixture.length,video_sha256:crypto.createHash('sha256').update(fixture).digest('hex'),whole_video_loaded_in_this_small_test_only:true,production_worker_slice_bytes:1048576}));
