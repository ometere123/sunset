/** Refuses a signed transaction unless local CLI, alias, RPC and chain match. */
import { existsSync, readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const root = resolve(fileURLToPath(new URL('.', import.meta.url)), '..');
const cli = resolve(root, 'node_modules', '.bin', 'genlayer');
const rpc = 'https://studio.genlayer.com/api';
const chainId = 61999;
const version = '0.39.1';
const contract = process.argv[2];
const args = process.argv.slice(3);

function deny(message) { throw new Error(`DEPLOY BLOCKED: ${message}`); }
function run(params) {
  const p = spawnSync(cli, params, { cwd: root, encoding: 'utf8' });
  if (p.error || p.status !== 0) deny(`${params.join(' ')} failed: ${p.stderr || p.error}`);
  return `${p.stdout}\n${p.stderr}`;
}

if (!['contracts/sunset.py', 'contracts/sunset_gate.py'].includes(contract)) deny('contract not audited');
if (contract === 'contracts/sunset.py' && args.length) deny('Sunset has no constructor arguments');
if (contract === 'contracts/sunset_gate.py' &&
    (args.length !== 3 || !/^0x[0-9a-fA-F]{40}$/.test(args[0]) ||
     !/^[A-Za-z0-9_-]{3,64}$/.test(args[1]) || !/^[0-9a-fA-F]{64}$/.test(args[2]))) {
  deny('SunsetGate arguments: contract address, rule ID, 64-character fingerprint');
}
for (const [key, value] of [
  ['GENLAYER_RPC_URL', rpc], ['GENLAYER_CHAIN_ID', String(chainId)],
  ['GENLAYER_NETWORK', 'studionet'],
]) {
  if (process.env[key] && process.env[key] !== value) deny(`conflicting ${key}`);
}
if (!existsSync(cli)) deny('run npm ci to install the repository-local CLI');
const pkg = JSON.parse(readFileSync(resolve(root, 'node_modules/genlayer/package.json'), 'utf8'));
if (pkg.version !== version) deny(`found GenLayer CLI ${pkg.version}, expected ${version}`);
const network = run(['network', 'info']);
if (!/studionet/i.test(network) || !network.includes(rpc) ||
    !new RegExp(`\\b${chainId}\\b`).test(network)) {
  deny(`CLI network info must show studionet, ${chainId} and ${rpc}.\n${network}`);
}
const response = await fetch(rpc, {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ jsonrpc: '2.0', method: 'eth_chainId', params: [], id: 1 }),
  signal: AbortSignal.timeout(12000),
});
if (!response.ok) deny(`RPC HTTP ${response.status}`);
const data = await response.json();
if (!/^0x[0-9a-f]+$/i.test(data.result ?? '') ||
    Number.parseInt(data.result, 16) !== chainId) deny('independent RPC chain ID mismatch');

console.log(`PRE-SIGN PASS: local genlayer@${version} | studionet ${chainId} | ${rpc}`);
const cmd = ['deploy', '--contract', contract];
if (args.length) cmd.push('--args', ...args);
const deployed = spawnSync(cli, cmd, {
  cwd: root, stdio: 'inherit', env: { ...process.env, GENLAYER_RPC_URL: rpc },
});
if (deployed.error) deny(deployed.error.message);
if (deployed.status !== 0) deny(`CLI deploy exited ${deployed.status}`);
console.log('Deployment submitted. Independently verify FINALIZED plus successful execution.');
