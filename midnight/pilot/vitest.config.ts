import { defineConfig } from 'vitest/config';
import { loadEnv } from 'vite';

const network = process.env['MIDNIGHT_NETWORK'] ?? 'local';
const isRemote = network !== 'local';

export default defineConfig({
  test: {
    environment: 'node',
    globals: true,
    testTimeout: 10 * 60_000,
    hookTimeout: isRemote ? 90 * 60_000 : 15 * 60_000,
    env: isRemote ? loadEnv(network, process.cwd(), '') : {},
    include: ['src/**/*.test.ts'],
    reporters: ['default'],
    sequence: { concurrent: false },
  },
});
