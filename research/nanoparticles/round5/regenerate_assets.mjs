// Regenerate through the snapshotted production renderer and verify exact bytes.
// Default is read-only verification. Pass --write to restore the bound assets.
import { readFile,writeFile } from 'node:fs/promises';
import { createHash,webcrypto } from 'node:crypto';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { renderNanoSignal,exportNanoSignal } from './production/nanolab-model.mjs';
if (!globalThis.crypto) Object.defineProperty(globalThis,'crypto',{value:webcrypto});
const root=path.dirname(fileURLToPath(import.meta.url));
const inputs=JSON.parse(await readFile(path.join(root,'inputs.json'),'utf8'));
for(const kind of ['two-tone','am','baseband','carrier']){
  const render=renderNanoSignal({kind,carrierHz:375,rateHz:23.4375,durationSec:2,gainDb:-24});
  const output=await exportNanoSignal(render);
  for(const [extension,bytes] of [['wav',output.wav],['json',output.manifest]]){
    const name=`assets/${kind}.${extension}`;
    const digest=createHash('sha256').update(bytes).digest('hex');
    if(digest!==inputs.files[name].sha256)throw new Error(`Production regeneration mismatch: ${name}`);
    if(process.argv.includes('--write'))await writeFile(path.join(root,name),bytes);
  }
}
console.log('Four actual production WAVs and manifests regenerate byte-for-byte.');
