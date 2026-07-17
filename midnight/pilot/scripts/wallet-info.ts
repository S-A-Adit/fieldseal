import { setNetworkId } from '@midnight-ntwrk/midnight-js-network-id';
import type { EnvironmentConfiguration } from '@midnight-ntwrk/testkit-js';
import pino from 'pino';

import { getConfig } from '../src/config.ts';
import { MidnightWalletProvider, resolveWalletSecret } from '../src/wallet.ts';

async function main(): Promise<void> {
  const config = getConfig();
  const secretProfile = process.env['MIDNIGHT_NETWORK'] ?? 'local';
  setNetworkId(config.networkId);
  const environment: EnvironmentConfiguration = {
    walletNetworkId: config.networkId,
    networkId: config.networkId,
    indexer: config.indexer,
    indexerWS: config.indexerWS,
    node: config.node,
    nodeWS: config.nodeWS,
    faucet: config.faucet,
    proofServer: config.proofServer,
  };
  const logger = pino({ level: 'silent' });
  const wallet = await MidnightWalletProvider.build(
    logger,
    environment,
    resolveWalletSecret(secretProfile),
  );

  process.stdout.write(`${JSON.stringify({
    network: config.networkId,
    unshieldedAddress: wallet.unshieldedKeystore.getBech32Address().toString(),
  })}\n`);
}

main().catch((error: unknown) => {
  const message = error instanceof Error ? error.message : 'Unable to derive the wallet address.';
  process.stderr.write(`${JSON.stringify({ ok: false, error: message })}\n`);
  process.exitCode = 1;
});
