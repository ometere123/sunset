import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { readFile, writeFile } from 'node:fs/promises';
import { createClient } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';

const endpoint = 'https://studio.genlayer.com/api';
const gate = '0x0d5983F08d80b9771Bf8e3973C7bc2Ca8c6E03E4';
const deploymentHash = '0xc0f7bb96621f3a3b4f7e3c4b0dbd929a4139214cbbbb66c1c10cca87fad7899c';
const executionHash = '0xc3a47f55d2e29144bd98d6ef935ce94a18edc1c84079751c82ee270c97deed7d';
const operation = 'unicode-review-v1';
const sourceCommit = 'b328c6be1e8b5c3bfb6d1c6113722410076c4fd3';
const sourcePath = 'contracts/sunset_gate.py';
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex');
const root = new URL('../', import.meta.url);

async function rpc(method, params = []) {
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method, params }),
    signal: AbortSignal.timeout(20000),
  });
  const body = await response.json();
  if (!response.ok || body.error || body.result == null) {
    throw new Error(`Missing or failed RPC response for ${method}`);
  }
  return body;
}

const chain = await rpc('eth_chainId');
if (chain.result !== '0xf22f') throw new Error('Expected StudioNet chain 61999');

async function finalized(hash) {
  const [transaction, receipt] = await Promise.all([
    rpc('eth_getTransactionByHash', [hash]),
    rpc('eth_getTransactionReceipt', [hash]),
  ]);
  const tx = transaction.result;
  if (tx.hash !== hash || receipt.result.transactionHash !== hash ||
      tx.to_address?.toLowerCase() !== gate.toLowerCase() ||
      tx.status !== 'FINALIZED' || tx.consensus_data?.leader_receipt?.[0]?.execution_result !== 'SUCCESS') {
    throw new Error(`Expected finalized successful gate transaction ${hash}`);
  }
  return { transaction, receipt };
}

const client = createClient({ chain: studionet, endpoint });
async function read(method, args = []) {
  const result = await client.readContract({ address: gate, functionName: method, args, rawReturn: true });
  const decoded = await client.readContract({ address: gate, functionName: method, args });
  return { address: gate, method, args, raw_calldata_result: result,
    decoded: typeof decoded === 'bigint' ? decoded.toString() : decoded };
}

const [deployment, execution, count, consumed] = await Promise.all([
  finalized(deploymentHash), finalized(executionHash),
  read('get_execution_count'), read('is_executed', [operation]),
]);
if (String(count.decoded) !== '1' || consumed.decoded !== true) {
  throw new Error('Gate state does not match the demonstrated execution');
}
const deployed = Buffer.from(deployment.transaction.result.data.contract_code, 'base64');
const committed = execFileSync('git', ['show', `${sourceCommit}:${sourcePath}`], { cwd: root });
const local = await readFile(new URL(sourcePath, root));
if (!deployed.equals(committed) || !deployed.equals(local)) throw new Error('Source bytes differ');

const evidence = {
  rpc: endpoint, chain, gate, deployment, execution,
  readbacks: [count, consumed],
  source_comparison: {
    source_commit: sourceCommit, path: sourcePath,
    deployed_source_field: 'deployment.transaction.result.data.contract_code',
    deployed_source_encoding: 'base64', bytes: deployed.length,
    deployed_sha256: sha256(deployed), committed_sha256: sha256(committed),
    local_sha256: sha256(local), exact_byte_match: true,
  },
};
// RPC node configuration can include credential-shaped fields. Keep the
// transaction evidence while omitting values of those fields from publication.
function omitCredentials(key, value) {
  if (/(api.?key|private.?key|mnemonic|password|secret|authorization|access.?token)/i.test(key)) {
    return value == null ? value : '[redacted]';
  }
  return value;
}
const json = JSON.stringify(evidence, omitCredentials, 2) + '\n';
if (process.argv[2]) {
  await writeFile(process.argv[2], json, { flag: 'wx' });
} else {
  process.stdout.write(json);
}
