/** Compute the exact SunsetGate action commitment used by sunset_gate.py. */
import { keccak_256 } from '@noble/hashes/sha3';

const [registry, ruleId, fingerprint, operationId, payload] = process.argv.slice(2);
if (!/^0x[0-9a-fA-F]{40}$/.test(registry) ||
    !/^[A-Za-z0-9_-]{3,64}$/.test(ruleId) ||
    !/^[0-9a-fA-F]{64}$/.test(fingerprint) ||
    !/^[A-Za-z0-9_-]{3,64}$/.test(operationId) ||
    typeof payload !== 'string' || payload.length < 1 || payload.length > 2048) {
  throw new Error('usage: node scripts/action_commitment.mjs <registry> <rule-id> <fingerprint> <operation-id> <payload>');
}
const value = JSON.stringify({
  domain: 'SUNSET_GATE_ACTION_V1',
  fingerprint,
  operation_id: operationId,
  payload,
  registry: registry.toLowerCase(),
  rule_id: ruleId,
});
console.log(Buffer.from(keccak_256(new TextEncoder().encode(value))).toString('hex'));
