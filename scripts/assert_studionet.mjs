/** Verify the live RPC identity before any deployment or integration claim. */
const rpc = 'https://studio.genlayer.com/api';
const expected = 0xf22f;
const response = await fetch(rpc, {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ jsonrpc: '2.0', method: 'eth_chainId', params: [], id: 1 }),
  signal: AbortSignal.timeout(12000),
});
if (!response.ok) throw new Error(`RPC HTTP ${response.status}`);
const body = await response.json();
if (!/^0x[0-9a-f]+$/i.test(body.result ?? '') ||
    Number.parseInt(body.result, 16) !== expected) {
  throw new Error(`Expected eth_chainId 0xf22f, received ${body.result ?? '<missing>'}`);
}
console.log(`StudioNet RPC verified: ${rpc} | eth_chainId=${body.result}`);
