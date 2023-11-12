import path from 'path'

import react from '@vitejs/plugin-react-swc'
import { defineConfig } from 'vite'

export default () => {
  const serverConfig = {
    host: true,
    port: 3000,
    proxy: {
      '/api': 'http://localhost:8000',
    },
  }

  return defineConfig({
    plugins: [react()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
        fastui: path.resolve(__dirname, '../frontend/fastui'),
      },
    },
    server: serverConfig,
    preview: serverConfig,
  })
}
