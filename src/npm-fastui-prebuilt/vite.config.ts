import path from 'path'

import react from '@vitejs/plugin-react-swc'
import { defineConfig, HttpProxy } from 'vite'

export default () => {
  const serverConfig = {
    host: true,
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        configure: (proxy: HttpProxy.Server) => {
          proxy.on('error', (err, _, res) => {
            const { code } = err as any
            if (code === 'ECONNREFUSED') {
              res.writeHead(502, { 'content-type': 'text/plain' })
              res.end('vite-proxy: Proxy connection refused')
            }
          })
        },
      },
    },
  }

  return defineConfig({
    // @ts-expect-error - no need to type check this file
    plugins: [react()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
        fastui: path.resolve(__dirname, '../npm-fastui/src'),
        'fastui-bootstrap': path.resolve(__dirname, '../npm-fastui-bootstrap/src'),
      },
    },
    server: serverConfig,
    preview: serverConfig,
    build: {
      sourcemap: true,
      // we don't need hashes in URLs, we the URL will change when we release a new version
      rollupOptions: {
        output: {
          entryFileNames: `assets/[name].js`,
          chunkFileNames: `assets/[name].js`,
          assetFileNames: `assets/[name].[ext]`,
        },
      },
    },
  })
}
