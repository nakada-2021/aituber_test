import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    lib: {
      entry: resolve(__dirname, 'src/main.ts'),
      name: 'Live2DCubismFramework',
      fileName: 'bundle',
      formats: ['umd']
    },
    rollupOptions: {
      output: {
        globals: {
          'live2dcubismcore': 'Live2DCubismCore'
        }
      }
    }
  },
  root: '/workspace/Demo',
  resolve: {
    alias: {
      '@framework': resolve(__dirname, '../Framework/src')
    }
  },
  define: {
    'globalThis.crypto': {
      getRandomValues: (arr) => require('crypto').randomFillSync(arr)
    }
  }
}); 