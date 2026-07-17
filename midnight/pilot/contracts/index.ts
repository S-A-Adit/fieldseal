import { CompiledContract } from '@midnight-ntwrk/midnight-js-protocol/compact-js';
import path from 'node:path';

export {
  Contract,
  ledger,
  type Ledger,
  type Witnesses,
} from './managed/receipt-registry/contract/index.js';
import {
  Contract,
  type Witnesses,
} from './managed/receipt-registry/contract/index.js';
import type { ReceiptPrivateState } from '../src/private-state.ts';

const currentDir = path.resolve(new URL(import.meta.url).pathname, '..');
export const zkConfigPath = path.resolve(currentDir, 'managed', 'receipt-registry');

const witnesses: Witnesses<ReceiptPrivateState> = {
  localSecret(context) {
    return [context.privateState, context.privateState.issuerSecret];
  },
};

export const CompiledReceiptContract = CompiledContract.make<
  Contract<ReceiptPrivateState>,
  ReceiptPrivateState
>(
  'EsenseReceiptRegistry',
  Contract,
).pipe(
  CompiledContract.withWitnesses(witnesses),
  CompiledContract.withCompiledFileAssets(zkConfigPath),
);
